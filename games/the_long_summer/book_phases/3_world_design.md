# PHASE 3: WORLD DESIGN
# The Long Summer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: LOCATION HIERARCHY

Two-hub topology: **Frank's Property** (primary) + **Millhaven** (secondary), separated by a one-hour walk on the driveway + town-walk path. Most locations sit two levels deep from the hub root (NLP-inspired hub-and-spoke; avoids the six-equal-regions failure mode). Phase-1-gated locations are *visible* as nodes for ambient reference but not entered.

### Top-level structure

```
                 ┌──────────────────────┐
                 │   FRANK'S PROPERTY    │
                 │     (primary hub)     │
                 │                       │
                 │   House + Yard +      │
                 │   Creek + Trail +     │
                 │   Ryan's Shop         │
                 └──────────┬───────────┘
                            │
                      1 hr walk
                   (gravel + county road)
                            │
                 ┌──────────┴───────────┐
                 │       MILLHAVEN       │
                 │    (secondary hub)    │
                 │                       │
                 │   Main Street +       │
                 │   Diner + Stores +    │
                 │   Church + College    │
                 └──────────────────────┘
```

### HUB 1 — Frank's Property

**`loc_property`** — Frank's Property (container)
*Gravel driveway, a sprawling contractor's spread at the south edge of Millhaven. Pines pushing in at the back. Heat that holds even at night. The smell of creek water and cut pine when the wind's right.*
- Image search: *rural Southern contractor property, farmhouse, wooden porch, gravel driveway, fields behind, pine trees, summer heat*
- Type: container
- Default entry: `loc_front_porch`
- Children: front porch, back porch, hallway, kitchen, living room, bathroom, Maya's bedroom, Frank's office, Ryan's room, Jake's room, yard, creek, trail head, driveway, Ryan's shop

---

#### Inside the house

**`loc_front_porch`** — Front Porch
*Two rocking chairs, a small table with Frank's ashtray he stopped using, the porch light Frank asks Maya not to leave on past midnight. Wasps under the eaves some summers; Diana swats at them without standing up. The sound of the screen door is the sound of the house.*
- Image search: *Southern front porch, wooden rocking chairs, screen door, porch light, pine boards*
- Type: room
- Entry from: `loc_property`
- Primary NPCs: Frank (evenings 9pm+), Ryan (sometimes)
- Activities: porch sitting, porch whiskey with Frank, porch reading with Diana (Sunday afternoons), Saturday coffee-and-newspaper

**`loc_hallway`** — Hallway
*Transit. Three bedroom doors, the bathroom, the living-room arch. A single overhead bulb. The hall runs louder than it should; Maya hears Jake's typing through the wall and Frank's paper rustling from the kitchen.*
- Image search: *wood-paneled rural hallway, bedroom doors, single ceiling light, nighttime dim*
- Type: room (transit)
- Entry from: `loc_front_porch`
- Connects: kitchen, living room, bathroom, all three bedrooms, Frank's office

**`loc_kitchen`** — Kitchen
*The social hub. Butcher-block counter worn pale at the center. Five chairs at a four-person table — Frank added one when Maya moved in. The coffee maker starts at 6 a.m. because Diana's standing over it. The refrigerator hums loud enough to narrate pauses in conversation. The window above the sink looks out on the back yard.*
- Image search: *farmhouse kitchen with butcher block counter, coffee maker, window over sink looking at yard, morning light*
- Type: room (hub)
- Entry from: `loc_hallway`
- Primary NPCs: Diana (mornings, late afternoons), Frank (breakfast + dinner), Ryan (brief morning overlap), Jake (1 pm lunch, 5 pm kitchen)
- Activities: breakfast scenes, dinner prep, family dinner, cook-for-herself, late-night kitchen encounters

**`loc_living_room`** — Living Room
*Television against the long wall. Couch deep enough to lie down on. Lamp Diana brought from the old house. Coffee table with coasters nobody uses. The porch visible through the front window. Frank reads here some evenings when the office gets stale. **This is the room where the catch-trigger fires.***
- Image search: *rural living room, deep couch, old television, lamp, porch window, Southern evening*
- Type: room
- Entry from: `loc_hallway`
- Primary NPCs: Frank (8–9 pm reading), Ryan (some evenings), any combination
- Activities: TV, reading, ambient, **solo masturbation (living-room variant — triggers Frank catch at corruption ≥ 50)**

**`loc_bathroom`** — Bathroom
*Shared. One tub/shower, one toilet, one sink, a small window over the tub that opens onto the side yard. A single hook for a towel — Diana added a second when Maya arrived. Steam hangs after Frank's morning shower for an hour.*
- Image search: *small rural bathroom, clawfoot tub, side window, single towel hook, steam*
- Type: room
- Entry from: `loc_hallway`
- Primary NPCs: rotating; morning rush produces ambient encounters
- Activities: shower, mirror-look (corruption-tier scene), hygiene restore

**`loc_mayas_bedroom`** — Maya's Bedroom
*Was a guest room. Twin bed against the far wall. Small desk Maya claimed for sketching. Window looks onto the front yard and the driveway. Shares a wall with Jake's room — thin enough that she can hear his keyboard after midnight.*
- Image search: *small guest bedroom, twin bed, desk with sketchbook, window to driveway, summer light*
- Type: room
- Entry from: `loc_hallway`
- Primary NPC: Maya (solo)
- Activities: sleep, sketch-in-room, journal, brochure-look, solo masturbation (bedroom variant), wardrobe changes

**`loc_franks_office`** — Frank's Office
*The door stays closed when Frank isn't in it. Metal filing cabinets older than the house. A desk facing the window so he can see the yard while working. Paper everywhere — neat piles, but piles. Whiskey and two glasses in the bottom drawer Maya was not supposed to know about.*
- Image search: *rural home office, metal filing cabinets, wooden desk facing window, paper stacks, whiskey bottle drawer*
- Type: room (entry-gated)
- Entry from: `loc_hallway` (requires `frank_home_and_invited` flag OR specific scheduled bookkeeping session)
- Primary NPC: Frank
- Activities: help with bookkeeping (paid), office Phase-B variants, possible Frank Crack scene (late Phase B)

**`loc_ryans_room`** — Ryan's Room
*Door usually closed when he's in the yard. Bed unmade. Posters for bands he hasn't listened to in five years. Truck parts on the dresser. Smells faintly of engine degreaser and clean laundry at the same time.*
- Image search: *rural young man's bedroom, unmade bed, band posters, truck parts on dresser*
- Type: room (access-gated via `ryan_invites` or after specific arc tiers)
- Entry from: `loc_hallway`
- Primary NPC: Ryan
- Activities: very limited Phase 1 — Ryan mostly works in the yard/shop; room scenes Phase 2+

**`loc_jakes_room`** — Jake's Room
*Door cracked at night when he's awake; closed when he's out. Desk under the window — laptop, drawing tablet, sketchbooks stacked crooked. A bed that's usually made, which surprised Maya the first time she saw it. Smells like pencil shavings and the cheap coffee he drinks cold. Shares the wall with Maya's room. **The caught-beat fires here.***
- Image search: *young man's room with drawing desk, tablet, laptop, sketchbooks stacked, small bed made neatly*
- Type: room (access-gated via Jake's arc tier)
- Entry from: `loc_hallway`
- Primary NPC: Jake
- Activities: sketch-with-Jake, watch-Jake-sketch, knock-on-door, Caught scene, Hand scene, post-Hand Keep variants

---

#### Outside the house

**`loc_back_porch`** — Back Porch
*Where Saturday dinners happen. A long outdoor table Frank built one summer. String lights Diana hung two summers back. Faces the yard; the creek trail starts from here.*
- Image search: *Southern back porch with long dinner table, string lights, view of backyard*
- Type: room
- Entry from: `loc_kitchen` OR `loc_yard`
- Activities: Saturday outdoor dinner, evening ambient, trail-head launch point

**`loc_yard`** — Back Yard
*Grass that holds up through August because Diana waters it. Ryan's work area is at the far side — tarps, an ongoing project or two, the riding mower. Jake sometimes sketches from the back porch toward the creek. The yard is visible from the kitchen window.*
- Image search: *rural backyard, grass, distant work tarp, creek treeline at back edge*
- Type: room (open)
- Entry from: `loc_back_porch` OR `loc_driveway`
- Primary NPCs: Ryan (weekday 8am-3pm), Jake (sometimes)
- Activities: help-Ryan-in-yard, watch-Ryan-working, bring-water, sunbathing, sketch-Jake-outside

**`loc_creek`** — The Creek
*Fifteen minutes' walk behind the property. Shallow, cold year-round, sandy bottom in one stretch, smooth stones in another. Maya sketches here when the kitchen is too crowded. Ryan swam here as a kid. Jake knows the sand stretch but doesn't go.*
- Image search: *Southern creek, shallow water, smooth stones, pine trees reflected, summer afternoon*
- Type: room (remote)
- Entry from: `loc_yard` (via trail)
- Activities: sketch-at-creek, creek swim (fitness + hygiene), solo contemplation

**`loc_trail_head`** — Trail Head
*Rises off the back porch, thirty minutes of moderate walk into pine. A rest stop halfway — a fallen log that's been sat on for decades — and beyond that, the isolated stretch of creek where the water gets deeper and the trees close over. Phase 2+ surface mostly.*
- Image search: *pine forest trail, fallen log rest stop, dappled summer light*
- Type: room (remote, Phase 2+ depth)
- Entry from: `loc_back_porch`
- Activities: solo hike, ambient exploration, fitness gain

**`loc_driveway`** — Driveway / Town-Walk Path
*Gravel for fifty yards, then the county road. One hour of walking to Main Street at Maya's pace. The first ten minutes of the walk pass Ryan's shop on the property edge. The rest is county road under pine and kudzu. Ambient encounters land here — a truck slowing, a church woman's car, a sheriff's nod from the window.*
- Image search: *rural gravel driveway, county road through pine, summer heat haze*
- Type: room (transit)
- Entry from: `loc_front_porch` OR `loc_yard`
- Connects: property → Millhaven
- Activities: walk to town, walk from town, ambient corruption encounters

**`loc_ryans_shop`** — Ryan's Shop (container)
*On the property edge, a hundred yards past the driveway bend. Converted outbuilding, big roll-up door, a yard of equipment waiting for parts or a buyer. Inventory visible from the county road — deliberately, Ryan has said — so drive-bys know what's there.*
- Image search: *rural outbuilding converted to small equipment shop, roll-up door, tractors and small engines in yard, sign hand-painted*
- Type: container
- Entry from: `loc_driveway`
- Default entry: `loc_shop_customer_area`
- Children: inventory yard, work bay, customer-facing area

  - **`loc_shop_customer_area`** — Customer Facing Area. *Counter with a ledger, two folding chairs, a fan, a small fridge of Gatorade. Where deals close. Where Maya works once the Help tier opens.*
  - **`loc_shop_work_bay`** — Work Bay. *Concrete floor, tool wall, the guts of whatever Ryan is currently fixing. Hydraulic lift in the corner. Ryan stands here most of the afternoon.*
  - **`loc_shop_inventory`** — Inventory Yard. *Tractors, small engines, a riding mower, a trailer, a truck on blocks. Visible from the road. Where ride-alongs start.*

---

### HUB 2 — Millhaven

**`loc_main_street`** — Main Street
*Three blocks of one-story brick storefronts. Mostly intact. The diner anchors the middle of the strip; the general store anchors the far end. Two churches visible at opposite ends (the Baptist one the Church crowd attends, a smaller Methodist one with an older congregation). A stoplight that takes ninety seconds on red.*
- Image search: *small Southern town Main Street, brick storefronts, diner sign, single stoplight, summer*
- Type: container / hub
- Entry from: `loc_driveway` (end of town-walk path)
- Default entry: `loc_main_street_sidewalk`
- Children: diner, general store, post office, gas station, college admin office, church front

**`loc_main_street_sidewalk`** — Main Street Sidewalk (ambient node)
*Where Maya walks between destinations. The trucker-crowd nods. The church-crowd turns politely.*
- Type: transit node
- Activities: ambient encounters (rep_road / rep_church), Sunday walking past church

**`loc_diner`** — The Diner (container)
*Marge's place. A long counter with chrome trim, six booths along the window, four tables in the middle. The grill behind the counter is always running. The jukebox plays country the year it thinks it is, which isn't this one. Smells like bacon and coffee grounds. Open 6 am to 10 pm Monday through Saturday; closed Sunday. **Maya's primary workplace.***
- Image search: *classic American diner, chrome counter, booths, jukebox, grill behind counter, small-town Southern*
- Type: container
- Entry from: `loc_main_street`
- Default entry: `loc_diner_front`
- Children: front floor, back booth, kitchen, Marge's office

  - **`loc_diner_front`** — Front Floor. *Where Maya works. Counter, booths, tables. Every tier plays out here.*
  - **`loc_diner_back_booth`** — Back Booth (T3 gate). *The corner booth after close. Specifically kept available by Marge for shift-close. Not accessible to general customers after 9 p.m.*
  - **`loc_diner_kitchen`** — Kitchen. *Cookie's domain during dinner. Grill, fryer, walk-in fridge in the back. Maya passes through on pickups.*
  - **`loc_diner_office`** — Marge's Office. *Tiny. A desk, a filing cabinet, a phone with a cord, the till at night. The key Marge hands Maya is the back-door key, kept on a hook by the office door.*

**`loc_general_store`** — General Store
*Run by the same family for three generations. Groceries, basic dry goods, hardware odds and ends, a small section of women's essentials. Smells like cardboard and cold-air from the cooler in the back. The clerk (ambient, unnamed) watches Maya's purchases without comment.*
- Image search: *small-town general store interior, wooden shelves, old cash register, Southern*
- Type: room
- Entry from: `loc_main_street`
- Activities: browse, buy groceries, ambient

**`loc_gas_station`** — Gas Station
*Two pumps. A convenience store inside with chips, soda, beer, magazines. Parking lot wide enough for trucks. Ryan fills up here. Half the rep_road crowd stops by daily.*
- Image search: *small-town gas station with two pumps, convenience store, Southern*
- Type: room
- Entry from: `loc_main_street`
- Activities: errand, ambient rep_road encounter

**`loc_post_office`** — Post Office
*Small. The postmaster knows everyone's box number by the second week. Open 9–5 Mon–Sat.*
- Image search: *small-town post office, PO boxes, service window, Southern*
- Type: room
- Entry from: `loc_main_street`
- Activities: mail, pick up packages, ambient

**`loc_college_admin`** — College Admin Office
*One room off Main Street — the community college has a small administrative satellite here for locals who can't make it to campus. A clerk, a brochure rack, an application desk. Open 9–4 Mon–Fri. Maya visits once (brochure + information). Subsequent visits blocked until admission money is paid.*
- Image search: *small community college admin satellite office, brochure rack, wooden desk*
- Type: room (single-visit, then gated)
- Entry from: `loc_main_street`
- Activities: single visit canvas (sets `college_brochure_taken`), then gated

**`loc_church_front`** — Church Front (Baptist)
*Maya attends the lawn and the front steps — the parking-lot-to-steps walk is where rep_church accumulates without her entering the sanctuary. The church interior is gated in Phase 1.*
- Image search: *small-town Baptist church exterior, white clapboard, steeple, gravel parking lot, Sunday morning*
- Type: room (exterior only)
- Entry from: `loc_main_street`
- Activities: Sunday attendance (ambient; front-steps register), rep_church tick

### PHASE 1 — GATED LOCATIONS (visible, not entered)

Listed as nodes for ambient reference. Entry blocked in Phase 1 via `entry_conditions` (Engine F2).

| Location | Gate condition | Phase 2+ role |
|---|---|---|
| `loc_truck_stop_bar` | `phase_2_open = true` | Road-crowd nexus; Friday-night content |
| `loc_fairground` | `season = august AND phase_2_open = true` | Seasonal week, carnival + community beats |
| `loc_hs_stadium` | `season = fall AND phase_2_open = true` | Friday-night football |
| `loc_church_interior` | `rep_church >= 60 AND phase_2_open = true` | Diana arc content |
| `loc_college_campus` | `college_admission_paid = true` | Classes, library, quad; Jake arc bleed |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: TIME SYSTEM

### Starting state

| Key | Value |
|---|---|
| **Start day / time** | Saturday, Week 1, 17:00 (5 p.m.) |
| **Prologue handoff** | Prologue ends with Maya pulling into the driveway; Phase 1 opens on the porch at arrival |
| **Calendar** | Sunday only in Phase 1; no Friday football, no Saturday market, no fair |
| **Week structure** | Mon–Sat diner open; Sun diner closed; rent due Sunday morning |

### Time periods

Six slots per day. Scheduled activities and NPC presences map cleanly to these slots.

| Period | Hours | Duration | Mood |
|---|---|---|---|
| **Morning** | 06:00–09:00 | 3 hr | Diana's coffee; Frank at the table; the kitchen belongs to older people |
| **Mid-morning** | 09:00–12:00 | 3 hr | Maya's solo block; Frank at work; Ryan in the yard; Jake in his room |
| **Afternoon** | 12:00–17:00 | 5 hr | Lunch + the longest block of the day; heat peaks; Ryan's shop busiest |
| **Evening** | 17:00–21:00 | 4 hr | Dinner block; Frank home; Maya often at diner (5–10 p.m. shift) |
| **Late** | 21:00–00:00 | 3 hr | Porch with Frank; TV; Jake gaming; kitchen empty enough for a late encounter |
| **Overnight** | 00:00–06:00 | 6 hr | Sleep slot; rare late-kitchen scenes at high corruption |

### Diner hours (locked)

- **Monday through Saturday**: 6 a.m. – 10 p.m.
- **Sunday**: closed.
- **Maya's standard shift**: 5 p.m. – 10 p.m. (overlaps with Cookie's cook shift; evening rush at 6–8 p.m.; Thursday late block for T3 gate-open scenes).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: NPC SCHEDULES

Transcribed from `Game_Redesign.md` §8. Schedules define *overlap windows* — where scenes can happen.

### Frank (Mon–Fri)

| Slot | Activity | Location |
|---|---|---|
| 05:30 wake | Dresses | `loc_mayas_bedroom`-adjacent hallway transit |
| 06:30–07:30 | Coffee, paper, breakfast | `loc_kitchen` |
| 07:30 depart | Leaves for work | outside Phase 1 scope |
| 08:00–16:00 | At work | NOT in house |
| 16:00–16:30 | Returns, showers | `loc_bathroom` briefly |
| 16:30–17:30 | Relaxes | `loc_front_porch` |
| 17:30–18:30 | Cooking dinner | `loc_kitchen` |
| 18:30–19:30 | Family dinner | `loc_kitchen` |
| 19:30–20:00 | Dishes | `loc_kitchen` |
| 20:00–21:00 | Paperwork OR TV | `loc_franks_office` OR `loc_living_room` |
| 21:00–22:30 | Porch whiskey OR continued office | `loc_front_porch` OR `loc_franks_office` |
| 22:30–23:00 | Bed | `loc_franks_bedroom` (not player-accessible) |

### Frank (Saturday / Sunday)

- Saturday: porch + hardware-store run AM, yard work + projects afternoon, grill dinner outdoor, longer porch whiskey.
- Sunday: porch coffee + paper AM, church ~10 a.m. every third week, lazy day, simple dinner, early bed.

### Ryan (Mon–Fri)

| Slot | Activity | Location |
|---|---|---|
| 06:30–07:00 | Wakes | `loc_ryans_room` |
| 07:00–08:00 | Kitchen (brief, overlaps Frank) | `loc_kitchen` |
| 08:00–12:00 | Yard + shop work | `loc_yard` / `loc_ryans_shop` |
| 12:00–13:00 | Lunch (often outside) | `loc_back_porch` or yard |
| 13:00–15:00 | Yard / fixing | `loc_yard` / `loc_ryans_shop` |
| 15:00–17:00 | Truck mechanic stuff OR nap | `loc_driveway` / `loc_ryans_room` |
| 17:00–18:00 | Cleans up | `loc_bathroom` briefly |
| 18:00–19:30 | Family dinner | `loc_kitchen` |
| 19:30–21:00 | Porch OR TV | `loc_front_porch` / `loc_living_room` |
| 21:00–23:00 | Out Fridays (bar, reserved Phase 2+) OR home | — |
| 23:00–01:00 | Bed | `loc_ryans_room` |

### Ryan (Saturday / Sunday)

- Saturday: wakes 8 a.m.; helps Frank with errands OR truck work; paid side-work for Maya available; evening out with friends.
- Sunday: wakes 9 a.m.; fixes things; evening home.

### Jake (Mon–Fri)

| Slot | Activity | Location |
|---|---|---|
| 08:00–09:00 | Wakes | `loc_jakes_room` |
| 09:00–10:00 | Sketches, studies | `loc_jakes_room` |
| 10:00–12:00 | College (if in session) OR room | `loc_jakes_room` or off-property |
| 12:00–13:00 | Lunch | `loc_kitchen` (brief) |
| 13:00–17:00 | Sketching, gaming, online | `loc_jakes_room` |
| 17:00–18:00 | Kitchen | `loc_kitchen` |
| 18:00–19:30 | Family dinner | `loc_kitchen` |
| 19:30–22:00 | Room OR yard sketching | `loc_jakes_room` / `loc_yard` |
| 22:00–01:00 | Gaming/online late | `loc_jakes_room` |
| 01:00+ | Bed | `loc_jakes_room` |

### Jake (Saturday / Sunday)

- Wakes 10 a.m.+; mostly in his room; Sunday even more so.

### Diana (Mon–Sun)

| Slot | Activity | Location |
|---|---|---|
| 05:30–06:30 | Coffee, starts breakfast | `loc_kitchen` |
| 06:30–08:30 | Breakfast with Frank + ambient | `loc_kitchen` |
| 08:30–11:00 | Garden spring–fall | side yard |
| 11:00–12:00 | Errands (less than weekly) | `loc_main_street` or home |
| 12:00–13:00 | Lunch (alone or with Maya if Maya's home) | `loc_kitchen` |
| 13:00–17:00 | Household, reading, garden | house / porch |
| 17:00–18:30 | Dinner prep (leads) | `loc_kitchen` |
| 18:30–19:30 | Family dinner (holds it) | `loc_kitchen` |
| 19:30–20:30 | Dishes, cleanup | `loc_kitchen` |
| 20:30–21:30 | Reading OR TV | `loc_living_room` |
| 21:30 | Bed | (not player-accessible) |

### Diana (Sunday)

- 05:30 wake as usual
- 08:30 departs for church
- 10:00–11:30 church service
- 12:00 lunch with whoever's home
- 13:00–16:00 porch reading alone — **the quiet Sunday afternoon signature beat**
- Evening: simple dinner, early bed

### Marge (Mon–Sat)

At the diner essentially all open hours (6 a.m. – 10 p.m.). Lives above the diner — small apartment with outside stair entry off the back alley. Takes Sundays fully off.

### Cookie (Mon–Sat)

- 17:00–22:00 cook shift (overlaps Maya).
- Takes Sunday off.

### Diner regulars (named, surfacing by schedule)

| Regular | When | rep_road effect |
|---|---|---|
| The Trucker (Mr. Hollis) | Friday 18:00–20:00 | +1 on each pleasant exchange |
| The Church Couple | Saturday 12:00–13:00 (Sunday closed) | rep_church +1 per polite service |
| The Older Mechanic (Pete) | Tuesday 12:00–13:00 | +1 rep_road baseline, big bump if Maya remembers his coffee order |
| The College Kids | Fri/Sat 21:00–22:00 | rep_college +1 each visible visit |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: ECONOMIC MODEL

### Locked numbers (2026-04-22 — this plan)

| Line | Amount |
|---|---|
| **Starting money** | $400 |
| **Weekly rent to Frank** | **$60** |
| **Weekly food contribution (groceries / household)** | **$15** |
| **Bus fare** | **$3 round-trip** (deferred: Phase 1 map is walk-only; Phase 2+ bus surfaces if needed) |
| **College admission target (stretch goal for the summer)** | **$1,500** |
| **Art supplies** | ~$10/week (sketchbook, pencils, occasional pen) |
| **Hygiene + personal** | ~$5/week (soap, shampoo, the small things Diana doesn't keep in the shared bathroom) |

**Weekly fixed costs**: $60 rent + $15 food + $15 personal + art = **$95/week baseline**.

### Diner tier income (re-stated from Phase 2B)

| Tier | Base wage | Tips | Net per 5-hour shift |
|---|---|---|---|
| T0 Distance | $45 | $0–5 | $45–50 |
| T1 Play along | $45 | $8–20 | $53–65 |
| T2 Work the floor | $45 | $25–60 | $70–105 |
| T3 Back booth after close | $45 base + extras $50–200 | varies | $95–245 per scene |

### Ryan shop cuts

| Tier | Typical cut per close | Frequency |
|---|---|---|
| Help (small-ticket) | $10–25 | 2–3 per week |
| Partner (mid-ticket) | $25–60 | 1–2 per week |
| Big deal (Crack tier) | $80–300 | 1 time Phase 1 (by design) |

### The math

| Strategy | Weekly net (after $95 fixed) | Weeks to $1,500 target |
|---|---|---|
| **Pure T0** (5 × $45 = $225 gross) | $130 | ~11 weeks — close to impossible |
| **T0 + T1 mix** ($275 gross) | $180 | ~8.5 weeks |
| **T1 + Ryan Help** ($275 + $60) | $240 | ~6 weeks |
| **T2 sustained + Ryan Partner** ($450 + $100) | $455 | ~3.5 weeks |
| **T2 + Partner + one big-ticket** | $455 + $200 one-off | 3 weeks + stretch |
| **T3 scene + full stack** | can compress to 2 weeks but costs rep_church | — |

### Economic pressure analysis

- Base T0 alone meets rent and groceries with a small margin. Survival is possible; savings is not.
- T1 opens at `corruption 25+ / rep_road 15+ / beauty 45+`. The beauty gate is the slowest — walking/creek-swim/basic hygiene rises fitness and beauty over 1–2 weeks.
- Hitting the $1,500 target *requires* at least two corruption-tier unlocks: T2 sustained OR T1 + Ryan Partner. Neither path is available in Chapter 1 (which closes on `first_rent_paid` — a Week-1 or Week-2 beat).
- The mid-summer reality check (forced event, §3.7) fires if Maya's savings trajectory crosses a projection flag. It is the moment the math becomes legible to the player-as-Maya, not to the player-as-strategist.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: WARDROBE / AMBIENT ENCOUNTERS

### Wardrobe — minimal in Phase 1

Per Engine F2, the clothing-enabled gate is removed. Phase 1 does *not* implement a full wardrobe tier system. Maya's outfits are **narrative texture** — referenced in prose, used for diner-tier ambient variants — but are not a mechanical gate.

Starting wardrobe:
- 3 pairs of jeans
- 6 t-shirts (mix of plain and faded band shirts)
- 1 hoodie
- 1 pair of shorts (cut-offs)
- 1 simple dress (the one Diana bought her a year ago for a funeral; Maya brought it because she could)
- sneakers + one pair of sandals
- basic underwear rotation

Wardrobe *changes* across Phase 1 are narrated, not quantified. At Operating corruption she buys one blue top from the general store that "runs two dollars more per table than the grey." At Saturated she's added a second. That's all. Full wardrobe tiers are a Phase 2+ expansion.

### Ambient encounter catalog — Phase 1

Ambient encounters fire passively at ~1/shift or 1/town-walk. They tick reputation sub-stats, corruption (slowly), and seed NPC awareness.

| # | Location | Encounter | Stat effect |
|---|---|---|---|
| 1 | `loc_driveway` (walk to town) | Pickup truck slows down; driver gives her a long look and moves on | corruption +1, rep_road +1 |
| 2 | `loc_main_street_sidewalk` | Older church woman nods at her | rep_church +1 if Maya smiles back, else 0 |
| 3 | `loc_main_street_sidewalk` | Mechanic at the gas station lifts a hand from under a hood | rep_road +1 |
| 4 | `loc_gas_station` | Clerk adds a Gatorade to the bag unasked on a hot day | rep_road +1 |
| 5 | `loc_diner_front` | Trucker regular calls her over to the counter for a refill and holds the look | corruption +1, rep_road +1 |
| 6 | `loc_diner_front` | College kid table asks if she's new in town | rep_college +1 |
| 7 | `loc_church_front` | Pastor shakes Maya's hand on the front steps | rep_church +2 |
| 8 | `loc_property` (ambient morning) | Maya catches Ryan watching her through the yard window | ryan.arousal modifier_effect (duration_hours = 4) |

Eight ambient encounters is the Phase 1 floor; more can be authored during content writing without disturbing the structure.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## VALIDATION

- **Every Phase-1-active location has at least one scheduled activity.** ✅
- **NPC schedules don't conflict** (no NPC in two locations at the same clock time). ✅
- **All container locations have `default_entry`**: `loc_property → loc_front_porch`, `loc_ryans_shop → loc_shop_customer_area`, `loc_diner → loc_diner_front`, `loc_main_street → loc_main_street_sidewalk`. ✅
- **Economic math is transparent**: base survivable at $130/week net; college target out of reach without corruption-tier unlock. ✅
- **Rent / groceries / tuition locked**: $60 / $15 / $1,500. ✅
- **Town locked**: Millhaven, North Alabama. ✅
- **Gated locations are visible (nodes exist)** but have `entry_conditions` blocking. ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End of Phase 3 — World Design. Proceed to Phase 4: Story Events.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
