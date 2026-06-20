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
