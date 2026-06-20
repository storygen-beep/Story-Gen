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
