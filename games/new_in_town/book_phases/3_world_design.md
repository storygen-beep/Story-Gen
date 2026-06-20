# PHASE 3: WORLD DESIGN
# New In Town

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: LOCATION HIERARCHY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Navigation Structure

```
Town Streets (external hub)
  ├── The Dusty Boot (container) → default_entry: loc_bar_floor
  │     └── Bar Floor (internal hub)
  │           ├── Stockroom
  │           ├── Emma's Room (upstairs)
  │           └── Jolene's Space (upstairs)
  ├── School (container) → default_entry: loc_school_classroom
  │     └── Classroom (internal hub)
  │           └── School Parking Lot
  ├── Diner
  ├── General Store
  ├── Church
  ├── Library
  ├── Deputy Station
  ├── Ray's Truck / Work Shed
  └── Mark's Office
```

**Total: 14 locations** (4 bar, 2 school, 8 standalone town)

---

### Location Details

#### EXTERNAL HUB

**`loc_town_streets`** — Town Streets / Main Road
- *Millfield's main road runs straight through town like a spine. One traffic light that nobody obeys, cracked sidewalks lined with pickups, and storefronts with hand-painted signs. Everyone's porch faces the street. Everyone's eyes follow the new schoolteacher when she walks past. Two thousand people, and every single one of them is watching.*
- Image search: "small rural American main street, pickup trucks, cracked sidewalks, storefronts, afternoon light, farming town"
- Type: hub (external)
- Navigation order: `[loc_dusty_boot, loc_school, loc_diner, loc_general_store, loc_church, loc_library, loc_deputy_station, loc_ray_truck_shed, loc_mark_office]`

---

#### THE DUSTY BOOT (container)

**`loc_dusty_boot`** — The Dusty Boot
- *Millfield's only bar. Neon sign in the window buzzes on at 5pm, half the letters dead. Two stories — the bar downstairs, rented rooms upstairs. The building smells like spilled beer, cigarette smoke that never quite leaves, and whatever Jolene is cooking in the back. It is the town's living room, gossip hub, and Emma's home.*
- Image search: "small town American bar exterior, neon sign, two-story building, evening, parking lot with pickup trucks"
- Type: container
- `is_container = true`
- `default_entry = loc_bar_floor`

---

**`loc_bar_floor`** — Bar Floor
- *Long wooden bar top scarred by decades of elbows and spilled drinks. Six stools, eight tables, a jukebox that only plays country, and a pool table with a tear in the felt. Jolene tends bar most nights. The regulars have assigned seats nobody official assigned. Friday nights the room fills — ranchers, mill workers, everyone. The light is amber and forgiving. Things look better in here than they do outside.*
- Image search: "small town American dive bar interior, wooden bar, stools, jukebox, pool table, warm amber lighting, country bar"
- Type: hub (internal)
- Entry from: `loc_town_streets` (via `loc_dusty_boot`)
- Navigation order: `[loc_bar_stockroom, loc_bar_emma_room, loc_bar_jolene_space]`
- Primary NPC associations: Ray (regular, evening stool), Jake (behind the bar), Jolene (owner/bartender)
- Activities: Bar Shifts (work), Evening at the Bar (Ray focus), Evening at the Bar (Jake focus), Friday Night Collision (shared)

---

**`loc_bar_stockroom`** — Stockroom
- *Behind a door marked "STAFF ONLY" — cases of beer stacked to the ceiling, spare kegs, boxes of napkins and cleaning supplies. A single overhead bulb on a pull chain. The door doesn't lock from the inside. Jolene is twenty feet away behind the bar. Customers on the other side of the wall. Private enough to do something stupid. Not private enough to get away with it.*
- Image search: "bar stockroom, beer cases stacked, dim overhead bulb, narrow space, industrial shelving"
- Type: room
- Entry from: `loc_bar_floor`
- Primary NPC associations: Jake (exclusive — endgame encounters)
- Activities: Stockroom encounter (Jake, gated: `jake_oral_unlocked`)

---

**`loc_bar_emma_room`** — Emma's Room (Upstairs)
- *A rented room above the bar. Single bed, a desk by the window, a bathroom barely big enough to turn around in. The mirror where she watches herself change. The walls are thin — she can hear the bar below, Jolene's TV through the wall, and whoever Jolene has over that night. The room started as temporary. It has become a confessional, a staging ground, and the place she invites men who shouldn't be here.*
- Image search: "small rented bedroom above bar, single bed, desk by window, simple, warm lamp, thin walls implied"
- Type: room
- Entry from: `loc_bar_floor`
- Primary NPC associations: Any NPC (when invited up), Solo (sleep, rest, mirror scenes)
- Activities: Sleep (utility), Rest (utility), Mirror scenes (story events), Inviting NPC over (gated per NPC)

---

**`loc_bar_jolene_space`** — Jolene's Space (Upstairs)
- *Jolene's room is everything Emma's isn't — lived-in, unapologetic, full. Silk robe thrown over a chair, ashtrays, wine bottles, a bed that's seen more action than the bar downstairs. A vanity mirror ringed with photos from her twenties. It smells like cigarette smoke and jasmine perfume. The door is rarely fully closed. Jolene doesn't believe in locked doors or keeping secrets.*
- Image search: "bohemian bedroom, silk robe on chair, vanity mirror, wine bottles, warm messy, cigarette ashtray, lived-in"
- Type: room
- Entry from: `loc_bar_floor`
- Primary NPC associations: Jolene (exclusive)
- Activities: Jolene Chats (mentor/strategy), Phase 1 corruption events

---

#### SCHOOL (container)

**`loc_school`** — Millfield Elementary School
- *Single-story brick building at the east end of Main Street. Flagpole out front, parking lot in back, playground that could use new paint. Twenty-three kids in Emma's class. The principal's office is down the hall and the door is always open. The building is professional space — and the most dangerous place in Millfield for Emma's double life, because this is where her reputation lives.*
- Image search: "small rural American elementary school exterior, brick building, flagpole, parking lot, single story"
- Type: container
- `is_container = true`
- `default_entry = loc_school_classroom`

---

**`loc_school_classroom`** — Classroom
- *Twenty-three small desks, a big one at the front that's hers. Alphabet border on the walls, construction paper projects taped to the windows, the smell of dry-erase markers and hand sanitizer. The door has a small window. Anyone walking past can see inside. After hours, the hallway goes quiet, the fluorescent lights hum, and the classroom becomes something different — intimate, charged, the desk between her and Mark the only barrier between professional and catastrophic.*
- Image search: "elementary school classroom, small desks, teacher desk at front, alphabet wall border, construction paper, fluorescent lights"
- Type: hub (internal)
- Entry from: `loc_town_streets` (via `loc_school`)
- Navigation order: `[loc_school_parking]`
- Primary NPC associations: Mark (conferences, fundraiser work), Solo (teaching, tutoring)
- Activities: Teaching (mandatory weekday mornings), Parent Conferences (Mark), Tutoring (money/reputation), School Events (reputation), Fundraiser Work (Mark proximity)

---

**`loc_school_parking`** — School Parking Lot
- *Cracked asphalt behind the school. Staff spots on the left, visitor parking on the right. After dark, the one working light covers half the lot. The other half is shadow. His car is always in the same spot — third row, visitor side. At night, the school is locked, the streets are empty, and the parking lot is the most private public space in Millfield. Private enough. Almost.*
- Image search: "school parking lot at night, cracked asphalt, single working light, dark shadows, empty lot"
- Type: room
- Entry from: `loc_school_classroom`
- Primary NPC associations: Mark (exclusive — after-hours encounters)
- Activities: Parking lot encounter (Mark, gated: `mark_sex_unlocked`)

---

#### STANDALONE TOWN LOCATIONS

**`loc_diner`** — Millfield Diner
- *Vinyl booths, formica counter, coffee that's been sitting since 6am. A bell above the door announces everyone who enters. The waitress knows your order before you sit down. It's where the town eats breakfast and where nothing stays secret for more than one refill. Tom sits in the same booth every lunch break. The window faces Main Street — anyone walking by can see who's eating with whom.*
- Image search: "small town American diner interior, vinyl booths, formica counter, coffee pot, window facing main street"
- Type: room
- Entry from: `loc_town_streets`
- Primary NPC associations: Tom (primary — coffee dates), Solo (weekend cafe shifts)
- Activities: Coffee with Tom (NPC repeatable), Weekend Cafe Job (money)

---

**`loc_general_store`** — General Store
- *Narrow aisles of everything from bread to boot polish. Mrs. Hewitt runs the register and runs the gossip — same skill set. She knew everyone's grandparents and has opinions about everyone's choices. The checkout counter is a confessional whether you want it to be or not. Buy wine and she raises an eyebrow. Buy condoms and the whole town knows by supper.*
- Image search: "small town American general store interior, narrow aisles, old register, elderly shopkeeper, packaged goods"
- Type: room
- Entry from: `loc_town_streets`
- Primary NPC associations: Solo
- Activities: Grocery Shopping (survival utility), Neighborly Visits (reputation)

---

**`loc_church`** — Millfield Community Church
- *White clapboard, steeple that leans slightly east, parking lot of clean trucks on Sunday morning. Inside: wooden pews, a hymnal in every rack, sunlight through plain glass windows. Pastor Davis gives the same sermon structure every week. The women sit on the right, the families in the middle, the single men in the back. Emma sits where the new teacher should sit — third row, center, visible. Mark and Karen sit five rows back, their son between them. She can feel his eyes on the back of her neck.*
- Image search: "small town white clapboard church, steeple, Sunday morning, parking lot, wooden pews inside, plain glass windows"
- Type: room
- Entry from: `loc_town_streets`
- Primary NPC associations: Solo (reputation maintenance), Mark (visible but untouchable — Karen present)
- Activities: Church Attendance (Sunday mandatory for reputation), Sunday School Volunteering (reputation repair)

---

**`loc_library`** — Millfield Library
- *Two rooms in the back of the Town Hall. Three thousand books, most donated, a study table with four chairs, and a children's section with beanbags. Quiet hours enforced by Mrs. Paulsen, who can hear a whisper through drywall. Private enough for tutoring. Quiet enough that a hand on a knee under the table would be invisible — and audible.*
- Image search: "small town library, two rooms, study table, bookshelves, children's section, quiet, warm light"
- Type: room
- Entry from: `loc_town_streets`
- Primary NPC associations: Tom (tutoring proximity), Solo (tutoring)
- Activities: Tutoring (money + reputation), Library Time with Tom (secondary NPC activity)

---

**`loc_deputy_station`** — Deputy Station
- *Millfield doesn't have a police station — it has a desk in the back of the Town Hall with a phone, a filing cabinet, and a chair that squeaks. Tom's desk. His dad's desk before him. A coffee mug with "World's Best Deputy" that he got himself because nobody else did. A window that looks out at the parking lot. He perks up like a retriever every time Emma walks past.*
- Image search: "small town deputy desk, filing cabinet, coffee mug, simple desk in back room, window, American small town law enforcement"
- Type: room
- Entry from: `loc_town_streets`
- Primary NPC associations: Tom (exclusive — engineered visits)
- Activities: Visit Tom at the Station (NPC activity — engineering proximity, early game)

---

**`loc_ray_truck_shed`** — Ray's Truck / Work Shed
- *A battered blue F-150 parked behind whatever building Ray is working on today. The truck bed has a toolbox bolted down, a tarp, and sawdust that never quite clears. The cab smells like work sweat and pine air freshener. His work shed behind the bar is corrugated metal, open on one side — a table saw, hand tools on pegboard, sawhorses. Physical space. His space. It smells like cut wood and engine oil and something male. Nobody comes here unless they have a reason — or unless they're making one.*
- Image search: "old blue pickup truck parked behind building, toolbox in bed, nearby corrugated metal work shed, hand tools on pegboard, sawhorses"
- Type: room
- Entry from: `loc_town_streets`
- Primary NPC associations: Ray (exclusive)
- Activities: Shed Scene (gate event), Truck encounters (gated), Help with Work (NPC activity — Ray proximity)

---

**`loc_mark_office`** — Mark's Office
- *Insurance agency on Main Street, between the hardware store and the post office. Glass front door with "MILLFIELD INSURANCE — MARK BRENNAN, AGENT" in gold lettering. Inside: beige walls, a fern that's dying, two client chairs across from his desk. The blinds are always half-open. Anyone on the sidewalk can see in. He keeps the door unlocked during business hours. A lunch visit looks professional. What happens when the blinds close doesn't.*
- Image search: "small town insurance office, glass door with gold lettering, beige walls, desk with two client chairs, half-open blinds"
- Type: room
- Entry from: `loc_town_streets`
- Primary NPC associations: Mark (exclusive)
- Activities: Lunch Visit (Mark, gated: `mark_groping_unlocked`), "Insurance question" (early game proximity excuse)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: TIME SYSTEM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Starting Conditions

- **Starting hour**: 14:00 (Afternoon — Emma arrives mid-day with two suitcases)
- **Starting day**: Day 1 (Monday — she starts teaching the next day)
- **Starting week**: Week 1 of 10 (65-day game)

### Time Periods

| Period | Hours | Duration | Mood |
|--------|-------|----------|------|
| Early Morning | 05:00-07:00 | 2h | Quiet. The town is still asleep. Jogging path along the fields. Optional energy recovery. |
| Morning | 07:00-09:00 | 2h | **SCHOOL (mandatory Mon-Fri).** Coffee in the teachers' lounge. Twenty-three kids waiting. |
| Late Morning | 09:00-12:00 | 3h | **SCHOOL (mandatory Mon-Fri).** Teaching. Her public persona operates here. |
| Afternoon | 12:00-15:00 | 3h | Free. Tutoring, Tom's coffee, Mark's conferences. The first decision slot. |
| Late Afternoon | 15:00-17:00 | 2h | Free. Shopping, errands, Mark conferences (Tue/Thu), neighborly visits. |
| Evening | 17:00-19:00 | 2h | Bar opens. Dinner hour. NPC interactions begin. The town shifts from daytime to something else. |
| Night | 19:00-22:00 | 3h | Bar peak. Ray at his stool. Jake behind the counter. The charged hours. Bar shifts or NPC pursuit — not both. |
| Late Night | 22:00-01:00 | 3h | Bar closing. Streets empty. The most dangerous and rewarding time slot. Whoever she's with now — nobody else is watching. Maybe. |

### Weekday vs. Weekend Structure

**TOML Weekday Convention**: `0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun`. Empty array `[]` = all days.

**Weekday (Monday-Friday, `weekdays = [0,1,2,3,4]`):**
- Morning + Late Morning = SCHOOL (mandatory, non-negotiable)
- 5 usable slots: Afternoon, Late Afternoon, Evening, Night, Late Night
- But Evening/Night/Late Night overlap with bar activity — choosing work (shifts) vs. NPC pursuit vs. rest

**Weekend (Saturday-Sunday, `weekdays = [5,6]`):**
- All 8 slots free
- But NPCs have their own schedules:
  - Tom: On duty Saturday (limited availability). Off Sunday.
  - Ray: Works odd jobs Sat morning. Free Sat afternoon/evening. Bar Sun evening.
  - Mark: With family ALL WEEKEND. Only available if he invents an excuse (requires `desire >= 30`). Most risky time — Karen is tracking him.
  - Jake: Works bar Fri/Sat night (his busiest). Off Sunday.
- Sunday morning: Church (mandatory for reputation — skip at -5 rep cost)
- Saturday morning: Recovery from Friday night OR weekend cafe shifts ($45)
- Sunday cafe shift conflicts with church — choose money or reputation

### School Enforcement (Weekday Morning Canvas)

**Critical engine note**: The engine requires every canvas trigger to have a `location` field. There is no "fires at any non-school location" mechanism. School enforcement is implemented as a **morning choice canvas** that fires at `loc_bar_emma_room` (where Emma wakes up) on weekday mornings.

**Canvas: `utility_school_morning`**
- **Location**: `loc_bar_emma_room`
- **Weekdays**: `[0,1,2,3,4]` (Mon-Fri)
- **Time**: 07:00-09:00
- **Priority**: 10 (fires before other morning canvases)
- **Repeatable**: yes

**Choices**:
1. **"Head to school"** — Advances time to 12:00 (auto-completes teaching), normal day continues from Afternoon slot
2. **"Skip school today"** — `reputation -5`, sets `missed_school_today` flag, stays at current location, free morning slot

If `school_enforcement_warned` flag is set (from principal concern events), the skip penalty increases to `reputation -8`.

This design means school is a daily choice, not an automatic constraint. The player always starts at Emma's Room and decides whether to go to school.

### Activity Schedule Overview

| Time Period | Location | Activity | NPC | Type | Weekdays |
|-------------|----------|----------|-----|------|----------|
| **Early Morning** | | | | | |
| 05:00-07:00 | Town streets/fields | Morning jog | Solo | Utility (energy +10) | `[]` (all) |
| 05:00-07:00 | Emma's Room | Sleep in | Solo | Utility (energy +15, but loses the slot) | `[]` (all) |
| **Morning** | | | | | |
| 07:00-09:00 | Classroom | Teaching | Solo | Mandatory (weekday) | `[0,1,2,3,4]` |
| 07:00-09:00 | Diner | Weekend Cafe Job | Solo | Money ($45, Sat/Sun) | `[5,6]` |
| 07:00-09:00 | Church | Church Attendance | Solo | Reputation (+3, Sunday) | `[6]` |
| **Late Morning** | | | | | |
| 09:00-12:00 | Classroom | Teaching | Solo | Mandatory (weekday) | `[0,1,2,3,4]` |
| 09:00-12:00 | Diner | Weekend Cafe Job (cont.) | Solo | Money (part of morning shift) | `[5,6]` |
| 09:00-12:00 | Church | Sunday School Volunteering | Solo | Reputation (+4, Sunday) | `[6]` |
| 09:00-12:00 | Jolene's Space | Jolene Chat | Jolene | Mentor (weekday, off-school) | `[5,6]` |
| **Afternoon** | | | | | |
| 12:00-15:00 | Diner | Coffee with Tom | Tom | NPC repeatable | `[0,2,4]` (Mon/Wed/Fri) |
| 12:00-15:00 | Library/Classroom | Tutoring | Solo | Money ($30) + Reputation (+1) | `[0,2]` (Mon/Wed) |
| 12:00-15:00 | General Store | Grocery Shopping | Solo | Survival utility | `[]` (all) |
| 12:00-15:00 | Jolene's Space | Jolene Chat | Jolene | Mentor (if not done in late morning) | `[]` (all) |
| 12:00-15:00 | Mark's Office | Lunch Visit | Mark | NPC (gated: `mark_groping_unlocked`) | `[0,1,2,3,4]` |
| **Late Afternoon** | | | | | |
| 15:00-17:00 | Classroom | Parent Conferences (Mark) | Mark | NPC repeatable | `[1,3]` (Tue/Thu) |
| 15:00-17:00 | General Store | Grocery Shopping | Solo | Survival utility | `[]` (all) |
| 15:00-17:00 | General Store/Streets | Neighborly Visits | Solo | Reputation (+2) | `[]` (all) |
| 15:00-17:00 | Deputy Station | Visit Tom at Station | Tom | NPC (early game proximity) | `[0,1,2,3,4]` |
| 15:00-17:00 | Anywhere | Errands / Free | Solo | Shopping, clothes, prep | `[]` (all) |
| **Evening** | | | | | |
| 17:00-19:00 | Bar Floor | Bar Shift (evening) | Solo | Money ($50-80) | `[]` (all) |
| 17:00-19:00 | Bar Floor | Evening at the Bar (Ray) | Ray | NPC repeatable | `[]` (all) |
| 17:00-19:00 | Bar Floor | Evening at the Bar (Jake) | Jake | NPC repeatable | `[]` (all) |
| 17:00-19:00 | Emma's Room | Dinner / Rest | Solo | Utility (energy recovery) | `[]` (all) |
| **Night** | | | | | |
| 19:00-22:00 | Bar Floor | Bar Shift (night) | Solo | Money ($50-80) | `[]` (all) |
| 19:00-22:00 | Bar Floor | Evening at the Bar (Ray) | Ray | NPC repeatable | `[]` (all) |
| 19:00-22:00 | Bar Floor | Evening at the Bar (Jake) | Jake | NPC repeatable | `[]` (all) |
| 19:00-22:00 | Emma's Room | Invite NPC Over | Tom/Ray/Mark | NPC (gated per NPC) | `[]` (all) |
| 19:00-22:00 | Town streets | Walk with NPC | Tom/Ray | NPC (ambient/bridge event) | `[]` (all) |
| **Late Night** | | | | | |
| 22:00-01:00 | Emma's Room | Sleep | Solo | Utility (standard energy restore: 80) | `[]` (all) |
| 22:00-01:00 | Bar Stockroom | Stockroom encounter | Jake | NPC (gated: `jake_oral_unlocked`) | `[]` (all) |
| 22:00-01:00 | Ray's Truck/Shed | Truck encounter | Ray | NPC (gated: `ray_oral_unlocked`) | `[]` (all) |
| 22:00-01:00 | School Parking Lot | Parking Lot encounter | Mark | NPC (gated: `mark_sex_unlocked`) | `[]` (all) |
| 22:00-01:00 | Emma's Room | Late visit (any NPC) | Any | NPC (gated per NPC) | `[]` (all) |

### Sleep & Energy Mechanics

Sleep timing determines next-day energy:

| Sleep Time | Energy Restored | Notes |
|------------|----------------|-------|
| Night (19:00-22:00) — early sleep | 100 (full) | Loses the most valuable NPC window |
| Late Night (22:00-01:00) — standard | 80 | Normal. Most players will sleep here. |
| Skip Late Night (still out) | 60 | Shows up to school tired. Sustainable for 1-2 nights. |
| Skip 2 consecutive nights | Capped at 40 | `reputation -1` (principal notices). Dangerous. |
| Morning jog (if awake Early Morning) | +10 bonus | Stacks with sleep restore. Costs the early slot. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: ECONOMIC MODEL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Income Sources

| Source | Amount | Availability | Time Cost | Notes |
|--------|--------|-------------|-----------|-------|
| Teaching salary | $220/week (auto) | Always (Mon-Fri) | Morning + Late Morning (mandatory) | Fixed, reliable. Deposited automatically. |
| Tutoring | $30/session | After `school_started` | 1 Afternoon slot (Mon/Wed) | `reputation +1`. Safe, boring, reputation-useful after risky moves. |
| Bar shifts (Jolene) | $50 + tips ($10-30) | After `bar_shifts_available` (Day 8+) | 1 Evening OR Night slot | Good money. Kills NPC time. `confidence +1` hidden bonus. Overhear gossip/NPC intel. |
| Weekend cafe job | $45/shift | After `cafe_job_available` | Morning + Late Morning (Sat OR Sun) | Sunday shift conflicts with church. Saturday shift kills recovery. |

### Recurring Expenses

| Expense | Amount | Frequency | Trigger | Consequence If Missed |
|---------|--------|-----------|---------|----------------------|
| Rent | $180 | Weekly | `days_since_flag(rent_last_paid) >= 7` | Miss once: Jolene is understanding. Twice: warning. Three times: forced bar shifts — locks Evening time slots. |
| Groceries | $25 | Every 5 days | `days_since_flag(groceries_last_bought) >= 5` | Energy max drops by 20/day until restocked. Stacks. |
| Bar drinks | $5-8 | Per bar visit | Whenever interacting at bar | Required for Ray/Jake bar activities. Can't nurse air. |
| Clothes/appearance | Variable ($20-60) | Optional, one-time | Story-gated | Better clothes unlock confidence-gated NPC options. The dress Jolene buys (Day 9) is the first. |

### Major Story-Gated Purchases

| Purchase | Cost | When | Effect |
|----------|------|------|--------|
| Dress (Jolene buys) | $0 (gift) | Day 9, Phase 1 | `confidence +3`. The first transformation marker. Unlocks appearance-gated choices. |
| Nicer clothes (self) | $40 | After `phase_1_complete` | Unlocks higher-tier appearance choices with Ray and Mark. |
| Wine for Jolene sessions | $12 | Ongoing | Enhances Jolene Chat quality — better NPC intel, +1 extra `confidence`. |
| Gift for Ray's daughter | $25 | Optional, Act 2 Ray arc | `interest +3` (Ray) if given at the right time (her birthday week). Major trust boost. |
| Outfit for Mark | $60 | Act 2 Mark arc | Specific dress/outfit for conferences. `desire +2` (Mark) when worn. |
| Drinks/shots for Jake | $15-25 | Ongoing, Jake arc | Required to play the bar flirting game. Cost of engaging with him on his turf. |

### Economic Pressure Model

**Weekly burn rate**: $180 (rent) + $35 (groceries, averaged) + $10 (minimum bar visits) = **$225/week minimum**

**Income to break even**: Teaching salary alone ($220) falls **$5 short** of minimum weekly expenses. She MUST supplement income or she goes underwater.

**Income scenarios:**
- Teaching only: -$5/week (slowly sinking)
- Teaching + 1 tutoring session: +$25/week (barely stable)
- Teaching + 1 bar shift: +$25-55/week (stable but loses NPC time)
- Teaching + 1 bar shift + 1 tutoring: +$55-85/week (comfortable but two NPC slots lost)

**Time trade-off**: Each bar shift (1 Evening or Night slot) replaces one NPC interaction. Working 2 bar shifts/week costs 2 NPC windows. Tutoring costs an Afternoon slot — same time as Coffee with Tom or Mark's lunch visits. Every dollar earned is an NPC moment lost.

**Cash flow by phase:**
- **Phase 1 (Days 1-12)**: Starting $150. No rent due until Day 7. First salary Day 5. Grace period — she's learning the town, not spending. By Day 7: ~$190 after rent.
- **Early Phase 2 (Days 12-25)**: Tight. Salary covers rent but leaves almost nothing. She needs to start bar shifts or tutoring by Week 3 or she's skipping groceries.
- **Mid Phase 2 (Days 25-45)**: Pressure peaks. She wants to spend time with Ray and Mark but needs money. Clothes purchases for Mark arc strain the budget. A $60 outfit means two extra bar shifts.
- **Late Phase 2 (Days 45-65)**: Either managed (if disciplined) or in crisis (if she ignored finances). Jolene may demand bar shifts for unpaid rent — which forces her into Jake's proximity during his arc, creating an interesting forced-proximity dynamic.

**The Squeeze Math (from concept doc):**
$220 salary - $180 rent = $40 surplus. Food costs ~$35/week. That leaves $5. She literally cannot afford to go to the bar without picking up extra work. Every dollar spent on a dress for Mark is a tutoring session she'll need later.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: NPC SCHEDULES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Jolene's Daily Schedule

**TOML Schedule Weekdays**: `[]` (all days — lives at the bar, always present)

Jolene lives above the bar. She's always nearby but not always available. She runs the town's only bar — her day revolves around it.

| Time Period | Location | What She's Doing | Available for Activity? |
|-------------|----------|-----------------|----------------------|
| Early Morning (05:00-07:00) | Jolene's Space | Asleep. Door open. Silk robe on the chair. | No. |
| Morning (07:00-09:00) | Jolene's Space / Bar | Slow start. Coffee, cigarette on the porch. Stocking the bar for the day. | Brief overlap — morning porch chat possible. |
| Late Morning (09:00-12:00) | Bar / Jolene's Space | Bar prep, inventory, phone calls. Relaxed, chatty. | **Jolene Chat available.** Her most talkative window. |
| Afternoon (12:00-15:00) | Bar / Errands | Might run errands in town. Might be in the bar office. | Jolene Chat available (if not out). |
| Late Afternoon (15:00-17:00) | Bar | Setting up for evening. Stocking, cleaning. | Available for quick conversation only. |
| Evening (17:00-19:00) | Bar Floor | Behind the bar. Working. | Available between customers. Observes Emma's interactions. |
| Night (19:00-22:00) | Bar Floor | Peak hours. She's working hard. | Not available for private chat. She's watching though. |
| Late Night (22:00-01:00) | Bar Floor / Upstairs | Closing up. Then upstairs — might have company. | Brief availability at closing. Phase 1 late-night events fire here. |

**Jolene movement pattern**: She is the bar. The bar is her. She doesn't leave Millfield. Her territory is the Dusty Boot — downstairs for business, upstairs for everything else. Getting Jolene out of the bar is rare and significant (the shopping trip on Day 9 is one of the only times).

---

### Tom's Daily Schedule

**TOML Schedule Weekdays**: `[]` (all days — same base routine daily, with Saturday/Sunday overrides noted below)

Tom is a creature of routine. His life runs on a loop — patrol, station, diner, home — until Emma disrupts it.

| Time Period | Location | What He's Doing | Available for Activity? |
|-------------|----------|-----------------|----------------------|
| Early Morning (05:00-07:00) | On patrol / Home | Morning patrol route. Drives the town perimeter. | No (on duty). Random encounter possible on streets. |
| Morning (07:00-09:00) | Deputy Station | Desk work. Paperwork from yesterday. Coffee from the diner. | Visit Tom at Station (early game, low-key). |
| Late Morning (09:00-12:00) | On patrol / Station | Patrol + station rotation. Responds to calls (rarely anything serious). | Not reliably available. Patrol schedule unpredictable. |
| Afternoon (12:00-15:00) | Diner | **Lunch break. Same booth every day.** This is his routine. | **Coffee with Tom — PEAK TOM HOURS.** (Mon/Wed/Fri) |
| Late Afternoon (15:00-17:00) | Deputy Station / On patrol | Wrapping up. Patrol through school area (coincidence? No.). | Visit Tom at Station. He "happens to be" near the school. |
| Evening (17:00-19:00) | Home / Town streets | Off duty. Goes home. Might walk the town. | Available if she engineers an encounter. Not scheduled. |
| Night (19:00-22:00) | Home / Bar (rare) | Usually home. Goes to the bar occasionally — out of his element. | Available if invited to her room. Bar overlap rare. |
| Late Night (22:00-01:00) | Home | In bed by 22:30. Early riser. | Late visit only if invited + high `devotion` (Tom). |

**Tom schedule notes:**
- **Saturday**: On duty half the day (morning patrol + station). Free afternoon/evening. Might show up at the bar (awkward, trying too hard).
- **Sunday**: Off duty. Church in the morning (same church as Emma — he sits in the back, steals glances). Free rest of day.
- **Tom movement pattern**: Completely predictable. Station → Diner → Station → Home. He gravitates toward wherever Emma is but tries to make it look accidental. The Diner at lunchtime is the guaranteed intercept point.

---

### Ray's Daily Schedule

**TOML Schedule Weekdays**: `[]` (all days — bar every evening, work hours vary)

Ray goes where the work is. His schedule shifts by the day, but his evening routine is locked — he's at the bar.

| Time Period | Location | What He's Doing | Available for Activity? |
|-------------|----------|-----------------|----------------------|
| Early Morning (05:00-07:00) | His place / Job site | Already working. Starts early, especially in summer. | No. He's miles away or up a ladder. |
| Morning (07:00-09:00) | Job site | Working. Roof repair, plumbing, fencing. Wherever he was hired today. | No. He doesn't stop for morning chat. |
| Late Morning (09:00-12:00) | Job site / Bar area | Working. If the job is at the bar, he's around. | Help with Work (if his job is bar-adjacent). |
| Afternoon (12:00-15:00) | Job site / Truck (lunch) | Breaks for lunch in his truck cab. Sandwich, thermos, radio. Back to work. | Possible overlap if she brings him something (calculated proximity). |
| Late Afternoon (15:00-17:00) | Job site → Bar area | Wrapping up. Cleaning tools. Loads the truck. Heads to the bar area. | He starts becoming available. Shed encounters possible. |
| Evening (17:00-19:00) | Bar Floor | **First beer. His stool. End of every day.** | **Evening at the Bar (Ray) — AVAILABLE.** |
| Night (19:00-22:00) | Bar Floor | **Settled in. 2-3 beers. Quiet. Watching the room.** | **Evening at the Bar (Ray) — PEAK RAY HOURS.** |
| Late Night (22:00-01:00) | Bar → Truck → Home | Last beer. Walks to his truck. Drives home (shouldn't, but does). | **Truck encounter (gated).** The walk to the truck is the window. |

**Ray schedule notes:**
- **Saturday**: Works a half day. At the bar by 3pm. Drinks more on Saturdays.
- **Sunday**: Doesn't work. Might do personal projects at his place. At the bar Sunday evening. Visits his daughter in the next town over 2 Sundays/month — UNAVAILABLE those days.
- **Ray movement pattern**: Job → Bar → Home. Repeat. His world is small. The bar is his social life. She has to enter his world to reach him — the bar, his truck, his work sites. He doesn't come to her.

---

### Mark's Daily Schedule

**TOML Schedule Weekdays**: `[0,1,2,3,4]` (weekdays only — weekends he's with family, available only via gated excuses)

Mark's schedule is the most constrained — because Karen monitors it. Every hour he spends with Emma is an hour he has to account for.

| Time Period | Location | What He's Doing | Available for Activity? |
|-------------|----------|-----------------|----------------------|
| Early Morning (05:00-07:00) | Home (with family) | Getting ready. Family breakfast. | No. |
| Morning (07:00-09:00) | Mark's Office | Opens the agency. Client calls. | No — public-facing, staff present. |
| Late Morning (09:00-12:00) | Mark's Office | Working. Might have a gap between clients. | "Insurance question" (very early game proximity). |
| Afternoon (12:00-15:00) | Mark's Office / Lunch | Lunch break. Sometimes at the diner. | **Lunch Visit to Office (gated: `mark_groping_unlocked`).** |
| Late Afternoon (15:00-17:00) | School (Tue/Thu) / Office | **Parent conferences. "Fundraiser planning."** | **Parent Conferences — PEAK MARK HOURS.** (Tue/Thu only) |
| Evening (17:00-19:00) | Home (with family) | Family dinner. Karen expects him home by 6:00. | No — unless he has an "excuse" (`desire >= 40` (Mark)). |
| Night (19:00-22:00) | Home (with family) | Family time. Helping kid with homework. TV with Karen. | **Her room (gated: `mark_oral_unlocked`).** He invents excuses — "meeting," "client dinner." Huge risk. |
| Late Night (22:00-01:00) | Home | Karen is asleep by 10:30. He could leave — if he dares. | **School Parking Lot / Her room (highest risk).** "Couldn't sleep, going for a drive." Karen might wake up. |

**Mark schedule notes:**
- **Saturday**: WITH FAMILY ALL DAY. Little league, errands, home. Available ONLY if he invents an excuse. Every Saturday absence is tracked by Karen.
- **Sunday**: Church with family (they sit together — Emma must perform normalcy). Family lunch. Maybe a "quick errand" in the afternoon if `desire >= 40` (Mark).
- **Mark movement pattern**: Office → School → Home. His world is a triangle. Every deviation is an alibi he has to construct. The school is the only legitimate overlap with Emma. His office is plausible ("she had an insurance question"). His car at her bar is a bomb waiting to detonate.

---

### Jake's Daily Schedule

**TOML Schedule Weekdays**: `[]` (all days — bartends nightly, busiest Fri/Sat)

Jake is a night creature. His life starts when the bar opens.

| Time Period | Location | What He's Doing | Available for Activity? |
|-------------|----------|-----------------|----------------------|
| Early Morning (05:00-07:00) | His place | Asleep. Dead. | No. |
| Morning (07:00-09:00) | His place | Still asleep. Doesn't wake before 10 most days. | No. |
| Late Morning (09:00-12:00) | His place / Town | Eventually wakes up. Coffee somewhere. Errands. Gym maybe. | Random street encounter possible. Not scheduled. |
| Afternoon (12:00-15:00) | His place / Around town | Whatever he does during the day. Nobody pays attention. | Not reliably available. He's not avoiding her — he's just elsewhere. |
| Late Afternoon (15:00-17:00) | Bar (arriving) | Shows up to set up. Stocking, cleaning glasses, turning on the neon. | Brief overlap. Bar isn't open yet — she'd have to have a reason to be there. |
| Evening (17:00-19:00) | Bar Floor (behind counter) | **Working. Pouring drinks. Flirting with customers.** | **Evening at the Bar (Jake) — AVAILABLE.** He's behind the bar. |
| Night (19:00-22:00) | Bar Floor (behind counter) | **Peak hours. In his element. Cocky, charming, performing.** | **Evening at the Bar (Jake) — PEAK JAKE HOURS.** |
| Late Night (22:00-01:00) | Bar Floor → Stockroom | **Closing time. Cleaning up. Last customers leave. Bar empties.** | **Stockroom encounter (gated). This is his most vulnerable window.** Bar is empty. Jolene is upstairs. It's just them. |

**Jake schedule notes:**
- **Friday/Saturday night**: His busiest. The bar is packed. He's performing for the crowd. Harder to isolate him — but she can still play the flirting-with-other-men game to make him watch.
- **Sunday**: Bar is closed or quiet. Jake might be off. Sometimes at a woman's place in the next town. Unreliable.
- **Jake movement pattern**: Home → Bar → Home (or someone else's home). His world IS the bar at night. He doesn't exist during the day in any useful way. She can only reach him in HIS territory — behind the counter, in the amber light, on his turf. Until she flips it.

---

### Schedule Overlap & Conflict Map

This shows when NPCs compete for Emma's time and create forced trade-offs:

| Time Period | Available NPCs | Tension Point |
|-------------|---------------|---------------|
| Early Morning (05:00-07:00) | None | Solo time. Energy recovery or morning jog. |
| Morning (07:00-09:00) | None (weekday: school) | Mandatory school. Weekend: church or cafe job. |
| Late Morning (09:00-12:00) | Jolene (weekday) | Mandatory school on weekdays. Weekend: Jolene chat or volunteering. |
| **Afternoon (12:00-15:00)** | **Tom (Diner), Mark (Office, gated)** | **CHOICE: Coffee with Tom OR Tutoring ($30) OR Mark lunch visit. Can only pick one.** |
| **Late Afternoon (15:00-17:00)** | **Tom (Station), Mark (School, Tue/Thu)** | **CHOICE: Visit Tom at station OR Mark conference. Same time window.** |
| **Evening (17:00-19:00)** | **Ray (Bar), Jake (Bar)** | **CHOICE: Ray or Jake? Both are at the bar. She can focus on one. Pursuing both in one evening raises the other's awareness.** |
| **Night (19:00-22:00)** | **Ray (Bar), Jake (Bar), Mark (gated, her room)** | **HIGH TENSION. Ray and Jake at the bar. Mark might show up at her door. Bar shift available for money. Maximum competition.** |
| **Late Night (22:00-01:00)** | **Ray (Truck), Jake (Stockroom), Mark (Parking lot), Tom (invited)** | **MAXIMUM TENSION. All NPCs potentially available in their gated spaces. Who does she visit? Whose door does she knock on? Every choice excludes the others.** |

**The critical trade-off window is Evening through Late Night (17:00-01:00)** — 3 time slots, 4 possible NPCs, plus bar shifts for money. She can interact with at most 2-3 NPCs in an evening, but doing so risks one NPC noticing attention to another (especially Ray and Jake, who share the bar).

### NPC Time Competition — The Impossible Calendar

The schedule guarantees she cannot pursue all NPCs optimally:

| NPC | Best Time Slots | Competes With |
|-----|----------------|---------------|
| Tom | Afternoon (Mon/Wed/Fri) | Tutoring ($30), Mark lunch visit |
| Ray | Evening + Night (daily) | Jake (same location), Bar shifts ($50-80) |
| Mark | Late Afternoon (Tue/Thu), Night (gated) | Tom (station visit), Ray/Jake (if she's at bar instead) |
| Jake | Evening + Night (daily) | Ray (same location), Bar shifts (she's working, not playing) |

**Worst collision**: Friday Night. All NPCs are potentially in the same building:
- Tom off duty, at the bar (rare, awkward)
- Ray at his stool
- Jake behind the counter
- Mark... shouldn't be here but is (Karen thinks he's at a "meeting")
- She has to choose who to focus on while others watch.
- `friday_collision` flag fires when 3+ NPCs are at the bar simultaneously.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: REPUTATION SYSTEM DETAIL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Since this is a small-town game where public perception is a survival mechanic, the reputation system deserves additional design:

### Reputation Sources — Gains

| Source | Rep Gain | Frequency | Notes |
|--------|---------|-----------|-------|
| Church attendance (Sunday) | +3 | Weekly | Mandatory to maintain. Skipping = -5. |
| Sunday School volunteering | +4 | Weekly (after church) | Emergency reputation repair. Burns the full Sunday morning. |
| Tutoring sessions | +1 | Per session (Mon/Wed) | Slow, steady, safe. |
| School events (PTA, bake sale) | +2 to +4 | 1-2 per week (random) | Skipping = -3. Mandatory for rep maintenance. |
| Neighborly visits | +2 | 2x/week available | Also provides gossip intel (early warning system). |
| Professional behavior at conferences | +1 | When Mark conferences stay clean | Only if she doesn't escalate — missed opportunity for Mark stat gains. |

### Reputation Sources — Losses

| Source | Rep Loss | Trigger | Notes |
|--------|---------|---------|-------|
| Skipping church | -5 | Sunday morning not at church | The town NOTICES. Biggest single-event reputation hit. |
| Skipping school events | -3 | Event fires, she's not present | Principal tracks this. |
| Bar visits (noticed) | -1 | Per visit if gossips see | "The teacher was at the bar again." Small but cumulative. |
| Buying wine/condoms at general store | -1 | Per purchase | Mrs. Hewitt talks. |
| Closed-door conferences with Mark | -2 | When `mark_kiss_unlocked` and door is closed | Other teachers notice. |
| Mark parking lot (seen) | -3 | Late night, if spotted | Small chance per occurrence. |
| Public affection with any NPC | -2 to -3 | In public locations | Touching, standing too close, visible flirting. |
| Karen confrontation | -5 to -8 | Story event: `karen_school_confrontation` | Major single hit. Hardest to recover from. |
| Looking tired at school | -1 | Skip 2 nights sleep | Principal notices. |
| Bar stockroom encounter (Jolene notices) | -3 | `jake_stockroom` event | Jolene isn't judging, but she comments — and others might hear. |
| Tom sees her with Ray | -2 | `tom_saw_ray` flag fires | Tom is hurt. Others might notice his reaction. |

### Reputation Threshold Events

| Rep Level | Status | Consequence |
|-----------|--------|-------------|
| 80-100 | **Golden** | The town adores her. "Sweetest teacher we've ever had." Provides a buffer for mistakes. |
| 60-79 | **Good** | Normal standing. No special treatment. Safe operating range. |
| 45-59 | **Concerning** | `principal_concern_1`: "Just wanted to check in, Emma. Everything alright?" Warning shot. |
| 30-44 | **Watched** | `principal_concern_2`: Active monitoring. Unannounced classroom visits. Gossip circles tighten. Church ladies whisper. |
| 15-29 | **Danger** | `principal_formal_warning`: School board meeting. Job at risk. NPC activities in public spaces become extremely risky. Karen's suspicion intensifies. |
| 1-14 | **Critical** | One more incident ends it. Town has made up its mind. Only extreme reputation recovery can save her. |
| 0 | **Game Over** | Fired. Reputation destroyed. She has to leave Millfield. |

### Reputation Asymmetry — The Core Design

**Reputation is designed to be easy to damage and hard to repair.** This is intentional:

- Fastest gain: Sunday School Volunteering (+4) — but costs entire Sunday morning
- Fastest loss: Karen confrontation (-5 to -8) — one story event
- Weekly best-case gain (if she does NOTHING risky): +3 (church) + +4 (volunteering) + +2 (tutoring) + +2 (neighborly visit) = **+11/week**
- Weekly worst-case loss (if she's reckless): -5 (church skip) + -3 (school event skip) + -2 (bar visits) + -3 (Mark door closed) + -1 (tired) = **-14/week**
- The math: she can lose reputation faster than she gains it. If she's pursuing NPCs aggressively AND maintaining reputation, she's spending real time on church, volunteering, and neighborly visits — time that could go to NPCs or money.

### Reputation Recovery Mode

When `reputation < 45`, the flag `reputation_recovery_mode` activates:
- Church attendance gains increase to +5 (the town is watching to see if she "shapes up")
- Volunteering gains increase to +6
- BUT all reputation losses are also doubled (she's under a microscope)
- This creates a knife-edge: she can recover faster, but one slip while recovering is devastating

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 3 complete. Type "proceed" to continue to Phase 4: Story Events,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
