# EXTRACTION: Locations & Schedules
# Source: Phase 3 (World Design)

## LOCATION HIERARCHY (14 total)

```
loc_town_streets (external hub)
  loc_dusty_boot (container) -> default_entry: loc_bar_floor
    loc_bar_floor (internal hub)
      loc_bar_stockroom (room)
      loc_bar_emma_room (room)
      loc_bar_jolene_space (room)
  loc_school (container) -> default_entry: loc_school_classroom
    loc_school_classroom (internal hub)
      loc_school_parking (room)
  loc_diner (room)
  loc_general_store (room)
  loc_church (room)
  loc_library (room)
  loc_deputy_station (room)
  loc_ray_truck_shed (room)
  loc_mark_office (room)
```

---

## LOCATION DETAILS

### loc_town_streets
- Type: hub (external)
- Description: "Millfield's main road runs straight through town like a spine. One traffic light that nobody obeys, cracked sidewalks lined with pickups, and storefronts with hand-painted signs. Everyone's porch faces the street. Everyone's eyes follow the new schoolteacher when she walks past. Two thousand people, and every single one of them is watching."
- Image search: "small rural American main street, pickup trucks, cracked sidewalks, storefronts, afternoon light, farming town"
- Navigation order: [loc_dusty_boot, loc_school, loc_diner, loc_general_store, loc_church, loc_library, loc_deputy_station, loc_ray_truck_shed, loc_mark_office]

### loc_dusty_boot
- Type: container
- is_container = true
- default_entry = "loc_bar_floor"
- Description: "Millfield's only bar. Neon sign in the window buzzes on at 5pm, half the letters dead. Two stories -- the bar downstairs, rented rooms upstairs. The building smells like spilled beer, cigarette smoke that never quite leaves, and whatever Jolene is cooking in the back. It is the town's living room, gossip hub, and Emma's home."
- Image search: "small town American bar exterior, neon sign, two-story building, evening, parking lot with pickup trucks"

### loc_bar_floor
- Type: hub (internal)
- Entry from: loc_town_streets (via loc_dusty_boot)
- Navigation order: [loc_bar_stockroom, loc_bar_emma_room, loc_bar_jolene_space]
- NPC associations: Ray (regular, evening stool), Jake (behind bar), Jolene (owner/bartender)
- Activities: Bar Shifts, Evening at Bar (Ray), Evening at Bar (Jake), Friday Night Collision
- Description: "Long wooden bar top scarred by decades of elbows and spilled drinks. Six stools, eight tables, a jukebox that only plays country, and a pool table with a tear in the felt. Jolene tends bar most nights. The regulars have assigned seats nobody official assigned. Friday nights the room fills -- ranchers, mill workers, everyone. The light is amber and forgiving. Things look better in here than they do outside."
- Image search: "small town American dive bar interior, wooden bar, stools, jukebox, pool table, warm amber lighting, country bar"

### loc_bar_stockroom
- Type: room
- Entry from: loc_bar_floor
- NPC associations: Jake (exclusive -- endgame encounters)
- Activities: Stockroom encounter (Jake, gated: jake_oral_unlocked)
- Description: "Behind a door marked 'STAFF ONLY' -- cases of beer stacked to the ceiling, spare kegs, boxes of napkins and cleaning supplies. A single overhead bulb on a pull chain. The door doesn't lock from the inside. Jolene is twenty feet away behind the bar. Customers on the other side of the wall. Private enough to do something stupid. Not private enough to get away with it."
- Image search: "bar stockroom, beer cases stacked, dim overhead bulb, narrow space, industrial shelving"

### loc_bar_emma_room
- Type: room
- Entry from: loc_bar_floor
- NPC associations: Any NPC (when invited), Solo (sleep, rest, mirror scenes)
- Activities: Sleep, Rest, Mirror scenes, Inviting NPC over (gated per NPC)
- Description: "A rented room above the bar. Single bed, a desk by the window, a bathroom barely big enough to turn around in. The mirror where she watches herself change. The walls are thin -- she can hear the bar below, Jolene's TV through the wall, and whoever Jolene has over that night. The room started as temporary. It has become a confessional, a staging ground, and the place she invites men who shouldn't be here."
- Image search: "small rented bedroom above bar, single bed, desk by window, simple, warm lamp, thin walls implied"

### loc_bar_jolene_space
- Type: room
- Entry from: loc_bar_floor
- NPC associations: Jolene (exclusive)
- Activities: Jolene Chats (mentor/strategy), Phase 1 corruption events
- Description: "Jolene's room is everything Emma's isn't -- lived-in, unapologetic, full. Silk robe thrown over a chair, ashtrays, wine bottles, a bed that's seen more action than the bar downstairs. A vanity mirror ringed with photos from her twenties. It smells like cigarette smoke and jasmine perfume. The door is rarely fully closed. Jolene doesn't believe in locked doors or keeping secrets."
- Image search: "bohemian bedroom, silk robe on chair, vanity mirror, wine bottles, warm messy, cigarette ashtray, lived-in"

### loc_school
- Type: container
- is_container = true
- default_entry = "loc_school_classroom"
- Description: "Single-story brick building at the east end of Main Street. Flagpole out front, parking lot in back, playground that could use new paint. Twenty-three kids in Emma's class. The principal's office is down the hall and the door is always open. The building is professional space -- and the most dangerous place in Millfield for Emma's double life, because this is where her reputation lives."
- Image search: "small rural American elementary school exterior, brick building, flagpole, parking lot, single story"

### loc_school_classroom
- Type: hub (internal)
- Entry from: loc_town_streets (via loc_school)
- Navigation order: [loc_school_parking]
- NPC associations: Mark (conferences, fundraiser work), Solo (teaching, tutoring)
- Activities: Teaching (mandatory weekday mornings), Parent Conferences (Mark), Tutoring, School Events, Fundraiser Work
- Description: "Twenty-three small desks, a big one at the front that's hers. Alphabet border on the walls, construction paper projects taped to the windows, the smell of dry-erase markers and hand sanitizer. The door has a small window. Anyone walking past can see inside. After hours, the hallway goes quiet, the fluorescent lights hum, and the classroom becomes something different -- intimate, charged, the desk between her and Mark the only barrier between professional and catastrophic."
- Image search: "elementary school classroom, small desks, teacher desk at front, alphabet wall border, construction paper, fluorescent lights"

### loc_school_parking
- Type: room
- Entry from: loc_school_classroom
- NPC associations: Mark (exclusive -- after-hours encounters)
- Activities: Parking lot encounter (Mark, gated: mark_sex_unlocked)
- Description: "Cracked asphalt behind the school. Staff spots on the left, visitor parking on the right. After dark, the one working light covers half the lot. The other half is shadow. His car is always in the same spot -- third row, visitor side. At night, the school is locked, the streets are empty, and the parking lot is the most private public space in Millfield. Private enough. Almost."
- Image search: "school parking lot at night, cracked asphalt, single working light, dark shadows, empty lot"

### loc_diner
- Type: room
- Entry from: loc_town_streets
- NPC associations: Tom (primary -- coffee dates), Solo (weekend cafe shifts)
- Activities: Coffee with Tom, Weekend Cafe Job
- Description: "Vinyl booths, formica counter, coffee that's been sitting since 6am. A bell above the door announces everyone who enters. The waitress knows your order before you sit down. It's where the town eats breakfast and where nothing stays secret for more than one refill. Tom sits in the same booth every lunch break. The window faces Main Street -- anyone walking by can see who's eating with whom."
- Image search: "small town American diner interior, vinyl booths, formica counter, coffee pot, window facing main street"

### loc_general_store
- Type: room
- Entry from: loc_town_streets
- NPC associations: Solo
- Activities: Grocery Shopping, Neighborly Visits
- Description: "Narrow aisles of everything from bread to boot polish. Mrs. Hewitt runs the register and runs the gossip -- same skill set. She knew everyone's grandparents and has opinions about everyone's choices. The checkout counter is a confessional whether you want it to be or not. Buy wine and she raises an eyebrow. Buy condoms and the whole town knows by supper."
- Image search: "small town American general store interior, narrow aisles, old register, elderly shopkeeper, packaged goods"

### loc_church
- Type: room
- Entry from: loc_town_streets
- NPC associations: Solo (reputation maintenance), Mark (visible but untouchable -- Karen present)
- Activities: Church Attendance (Sunday mandatory), Sunday School Volunteering
- Description: "White clapboard, steeple that leans slightly east, parking lot of clean trucks on Sunday morning. Inside: wooden pews, a hymnal in every rack, sunlight through plain glass windows. Pastor Davis gives the same sermon structure every week. The women sit on the right, the families in the middle, the single men in the back. Emma sits where the new teacher should sit -- third row, center, visible. Mark and Karen sit five rows back, their son between them. She can feel his eyes on the back of her neck."
- Image search: "small town white clapboard church, steeple, Sunday morning, parking lot, wooden pews inside, plain glass windows"

### loc_library
- Type: room
- Entry from: loc_town_streets
- NPC associations: Tom (tutoring proximity), Solo (tutoring)
- Activities: Tutoring, Library Time with Tom
- Description: "Two rooms in the back of the Town Hall. Three thousand books, most donated, a study table with four chairs, and a children's section with beanbags. Quiet hours enforced by Mrs. Paulsen, who can hear a whisper through drywall. Private enough for tutoring. Quiet enough that a hand on a knee under the table would be invisible -- and audible."
- Image search: "small town library, two rooms, study table, bookshelves, children's section, quiet, warm light"

### loc_deputy_station
- Type: room
- Entry from: loc_town_streets
- NPC associations: Tom (exclusive -- engineered visits)
- Activities: Visit Tom at Station
- Description: "Millfield doesn't have a police station -- it has a desk in the back of the Town Hall with a phone, a filing cabinet, and a chair that squeaks. Tom's desk. His dad's desk before him. A coffee mug with 'World's Best Deputy' that he got himself because nobody else did. A window that looks out at the parking lot. He perks up like a retriever every time Emma walks past."
- Image search: "small town deputy desk, filing cabinet, coffee mug, simple desk in back room, window, American small town law enforcement"

### loc_ray_truck_shed
- Type: room
- Entry from: loc_town_streets
- NPC associations: Ray (exclusive)
- Activities: Shed Scene (gate event), Truck encounters (gated), Help with Work
- Description: "A battered blue F-150 parked behind whatever building Ray is working on today. The truck bed has a toolbox bolted down, a tarp, and sawdust that never quite clears. The cab smells like work sweat and pine air freshener. His work shed behind the bar is corrugated metal, open on one side -- a table saw, hand tools on pegboard, sawhorses. Physical space. His space. It smells like cut wood and engine oil and something male. Nobody comes here unless they have a reason -- or unless they're making one."
- Image search: "old blue pickup truck parked behind building, toolbox in bed, nearby corrugated metal work shed, hand tools on pegboard, sawhorses"

### loc_mark_office
- Type: room
- Entry from: loc_town_streets
- NPC associations: Mark (exclusive)
- Activities: Lunch Visit (gated: mark_groping_unlocked), "Insurance question" (early game)
- Description: "Insurance agency on Main Street, between the hardware store and the post office. Glass front door with 'MILLFIELD INSURANCE -- MARK BRENNAN, AGENT' in gold lettering. Inside: beige walls, a fern that's dying, two client chairs across from his desk. The blinds are always half-open. Anyone on the sidewalk can see in. He keeps the door unlocked during business hours. A lunch visit looks professional. What happens when the blinds close doesn't."
- Image search: "small town insurance office, glass door with gold lettering, beige walls, desk with two client chairs, half-open blinds"

---

## NPC SCHEDULES

### Jolene Schedule (weekdays: [] -- all days)
| Period | Location | Doing | Available? |
|--------|----------|-------|-----------|
| Early Morning 05-07 | Jolene's Space | Asleep | No |
| Morning 07-09 | Jolene's Space / Bar | Coffee, porch, stocking | Brief overlap |
| Late Morning 09-12 | Bar / Jolene's Space | Bar prep, inventory, phone | **Jolene Chat available** |
| Afternoon 12-15 | Bar / Errands | Errands or bar office | Jolene Chat (if not out) |
| Late Afternoon 15-17 | Bar | Setting up for evening | Quick conversation only |
| Evening 17-19 | Bar Floor | Working behind bar | Between customers |
| Night 19-22 | Bar Floor | Peak hours | Not available for chat |
| Late Night 22-01 | Bar Floor / Upstairs | Closing up | Brief at closing |

### Tom Schedule (weekdays: [] -- all days)
| Period | Location | Doing | Available? |
|--------|----------|-------|-----------|
| Early Morning 05-07 | Patrol / Home | Morning patrol | No (random encounter) |
| Morning 07-09 | Deputy Station | Desk work | Visit Tom at Station |
| Late Morning 09-12 | Patrol / Station | Patrol rotation | Not reliable |
| Afternoon 12-15 | Diner | **Lunch break, same booth** | **Coffee with Tom (Mon/Wed/Fri)** |
| Late Afternoon 15-17 | Station / Patrol | Wrapping up | Visit Tom at Station |
| Evening 17-19 | Home / Streets | Off duty | If engineered |
| Night 19-22 | Home / Bar (rare) | Usually home | If invited to room |
| Late Night 22-01 | Home | In bed by 22:30 | Late visit if high devotion |

Saturday: On duty half day, free afternoon/evening. Sunday: Off. Church. Free rest of day.

### Ray Schedule (weekdays: [] -- all days)
| Period | Location | Doing | Available? |
|--------|----------|-------|-----------|
| Early Morning 05-07 | His place / Job site | Already working | No |
| Morning 07-09 | Job site | Working | No |
| Late Morning 09-12 | Job site / Bar area | Working | Help with Work (if bar-adjacent) |
| Afternoon 12-15 | Job site / Truck | Lunch in truck | Calculated proximity possible |
| Late Afternoon 15-17 | Job site -> Bar area | Wrapping up | Shed encounters possible |
| Evening 17-19 | Bar Floor | **First beer, his stool** | **Evening at Bar (Ray)** |
| Night 19-22 | Bar Floor | **Settled in, 2-3 beers** | **PEAK RAY HOURS** |
| Late Night 22-01 | Bar -> Truck -> Home | Last beer, walks to truck | **Truck encounter (gated)** |

Saturday: Works half day, bar by 3pm. Sunday: Doesn't work, bar evening. Visits daughter 2 Sundays/month (UNAVAILABLE).

### Mark Schedule (weekdays: [0,1,2,3,4] -- weekdays only)
| Period | Location | Doing | Available? |
|--------|----------|-------|-----------|
| Early Morning 05-07 | Home | Family breakfast | No |
| Morning 07-09 | Mark's Office | Opens agency | No (public-facing) |
| Late Morning 09-12 | Mark's Office | Working | "Insurance question" (early) |
| Afternoon 12-15 | Office / Lunch | Lunch break | **Lunch Visit (gated: mark_groping_unlocked)** |
| Late Afternoon 15-17 | School (Tue/Thu) / Office | **Parent conferences** | **PEAK MARK HOURS (Tue/Thu)** |
| Evening 17-19 | Home | Family dinner | No (unless excuse, desire >= 40) |
| Night 19-22 | Home | Family time | **Her room (gated: mark_oral_unlocked)** |
| Late Night 22-01 | Home | Karen asleep 10:30 | **Parking lot / room (highest risk)** |

Saturday/Sunday: WITH FAMILY ALL DAY. Only available with invented excuse (desire >= 40).

### Jake Schedule (weekdays: [] -- all days)
| Period | Location | Doing | Available? |
|--------|----------|-------|-----------|
| Early Morning 05-07 | His place | Asleep | No |
| Morning 07-09 | His place | Still asleep | No |
| Late Morning 09-12 | His place / Town | Eventually wakes | Random encounter |
| Afternoon 12-15 | His place / Around | Day activities | Not reliable |
| Late Afternoon 15-17 | Bar (arriving) | Setting up | Brief overlap |
| Evening 17-19 | Bar Floor (counter) | **Working, flirting** | **Evening at Bar (Jake)** |
| Night 19-22 | Bar Floor (counter) | **Peak hours, performing** | **PEAK JAKE HOURS** |
| Late Night 22-01 | Bar -> Stockroom | **Closing, cleaning** | **Stockroom encounter (gated)** |

Fri/Sat: Busiest. Bar packed. Sunday: Closed/quiet. Off. Unreliable.

---

## SCHEDULE CONFLICT MAP

| Period | Available NPCs | Tension |
|--------|---------------|---------|
| Early Morning 05-07 | None | Solo: energy recovery or jog |
| Morning 07-09 | None (school) | School mandatory weekday. Weekend: church or cafe |
| Late Morning 09-12 | Jolene (weekday) | School weekday. Weekend: Jolene/volunteering |
| **Afternoon 12-15** | **Tom (Diner), Mark (Office, gated)** | **CHOICE: Tom OR Tutoring ($30) OR Mark lunch** |
| **Late Afternoon 15-17** | **Tom (Station), Mark (School Tue/Thu)** | **CHOICE: Tom station OR Mark conference** |
| **Evening 17-19** | **Ray (Bar), Jake (Bar)** | **CHOICE: Ray or Jake? Both at bar.** |
| **Night 19-22** | **Ray (Bar), Jake (Bar), Mark (gated, room)** | **HIGH TENSION. 3 NPCs + bar shifts.** |
| **Late Night 22-01** | **Ray (Truck), Jake (Stockroom), Mark (Parking), Tom (invited)** | **MAXIMUM TENSION. All NPCs gated.** |

### NPC Competition
| NPC | Best Time | Competes With |
|-----|-----------|---------------|
| Tom | Afternoon Mon/Wed/Fri | Tutoring ($30), Mark lunch |
| Ray | Evening + Night daily | Jake (same location), bar shifts |
| Mark | Late Afternoon Tue/Thu, Night (gated) | Tom station, Ray/Jake bar |
| Jake | Evening + Night daily | Ray (same location), bar shifts |

**Worst collision**: Friday Night. All NPCs potentially in same building. `friday_collision` flag when 3+ NPCs at bar simultaneously.
