# PHASE 5: ACTIVITIES
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION A: NPC ACTIVITIES (ESCALATING)

All NPC activities use the Three-Choice Format (Pattern L):
- **Emotional** — conversation, builds love, may build corruption
- **Physical** — opens sub-menu of unlocked intensity options
- **Neutral** — quick interaction, small love +1, conserves energy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### JAKE ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#### Activity: Drawing Session with @jake

- **Pattern**: A (standard escalation)
- **Location**: `loc_jakes_room`
- **Schedule**: 12:00-15:00
- **NPC**: `npc_jake`
- **Unlock**: `drawing_started` (set by Beat 7 Jake variant or early interactions)
- **Priority**: 1
- **Energy**: 15
- **is_repeatable**: true, max_triggers_per_day = 1

**Base Scene Variants:**

DEFAULT (SAFE/OPEN quadrant):
> "Jake's room. Afternoon light through the window. He's already set up — sketchbook open, pencils arranged, the eraser he chews on when he's concentrating sitting on the bedside table. He looks up when you walk in. 'Hey.' Small smile. He pushes his glasses up. 'The light's really good right now.'"

WITHDRAWN variant (post-crisis / CONFLICTED):
> "Jake's door is cracked but not open. He's drawing something — not you. Landscapes. The pencil moves mechanically. He glances up when you enter. 'Oh. Hey.' Looks back at the page. The chair he usually pulls out for you is against the wall."

WARM variant (high stats / OPEN):
> "He's already cleared space for you on the bed. The sketchbook is open to a half-finished portrait — your face, the way you looked yesterday when you laughed at something Ryan said. He's captured a version of you that's more beautiful than any mirror. 'I was hoping you'd come by.' His voice is steady. His eyes aren't."

**Choice Progression (Three-Choice Format):**

| Choice | Condition | Node | Effects |
|--------|-----------|------|---------|
| **"Talk to him while he draws" (Emotional)** | always | emotional_node | jake_love +2, jake_trust +1 |
| **"Pose for him" (Physical)** | `exposure_unlock` | physical_submenu | see sub-menu below |
| **"Watch him work" (Neutral)** | always | exit | jake_love +1, energy -15 |

**Emotional Node — Conversation Topics (group variants by relationship phase):**

| Phase | Topic | Effects |
|-------|-------|---------|
| Pre-kiss | Talk about art school, his portfolio, what he wants to be. He opens up about Ryan mocking his art. | jake_love +2, jake_trust +1 |
| Post-kiss | Talk about what this is between them. "We shouldn't." "I know." He draws while they talk — her face comes out softer. | jake_love +2, jake_trust +1, corruption +1 |
| Post-intimacy | He tells her he loves her. Simple. Terrified. True. The conversation is about whether this survives Mom's return. | jake_love +3, jake_trust +2 |

**Physical Sub-Menu:**

| Choice | Condition | Effects | Video Placeholder |
|--------|-----------|---------|-------------------|
| "Hold the pose a little longer" | `exposure_unlock` | jake_love +1, corruption +1 | Image — posing, charged eye contact |
| "Flirt while posing" | `flirt_unlock` + corruption >= 40 | jake_love +1, jake_corruption +2, corruption +2 | Image — flirtatious posing, teasing |
| "Pose provocatively" | `tease_unlock` + corruption >= 55 | jake_corruption +2, corruption +2 | Video — provocative posing, deliberate |
| "Kiss him" | `kiss_unlock` + corruption >= 70 + jake_love >= 15 | jake_love +2, jake_corruption +2, corruption +2 | Video — tender kiss, art room |
| "Guide his hand" | `handjob_unlock` + corruption >= 100 + jake_love >= 20 | jake_corruption +3, corruption +3 | Video — handjob, tender, his room |
| "Get on your knees" | `blowjob_unlock` + corruption >= 140 + jake_love >= 25 | jake_corruption +4, corruption +4 | Video — oral, tender, bedroom |
| "Take him to bed" | `sex_unlock` + corruption >= 180 + jake_love >= 30 | jake_corruption +5, corruption +5 | Video — sex, eye contact, intimate, bed |

---

#### Activity: Studying with @jake

- **Pattern**: A (limited escalation — caps at kiss tier)
- **Location**: `loc_library`
- **Schedule**: 15:00-17:00
- **NPC**: `npc_jake`
- **Unlock**: `first_week_complete`
- **Priority**: 1
- **Energy**: 15

**Base Scene:**

DEFAULT:
> "Library basement. Fluorescent lights and the smell of old paper. Jake is at a study carrel, glasses on, textbook open. He pulls out the chair next to him without looking up. Their knees touch under the table. Neither moves."

WITHDRAWN:
> "He's at the far carrel today. Didn't save a seat. Headphones on, though nothing seems to be playing."

WARM:
> "He saved her spot. There's a coffee from the campus café on her side. Still warm. A sticky note on the cup: a tiny sketch of her face, asleep. He drew this from memory."

**Choice Progression:**

| Choice | Condition | Node | Effects |
|--------|-----------|------|---------|
| **"Ask about his classes" (Emotional)** | always | talk | jake_love +1, jake_trust +2 |
| **"Touch his hand under the table" (Physical)** | `exposure_unlock` | physical | see below |
| **"Study quietly together" (Neutral)** | always | exit | jake_love +1, jake_trust +1 |

**Physical Sub-Menu (limited — public location):**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Brush his hand" | `exposure_unlock` | jake_love +1, corruption +1 |
| "Play footsie under the table" | `flirt_unlock` + corruption >= 40 | jake_corruption +1, corruption +1 |
| "Kiss him between the shelves" | `kiss_unlock` + corruption >= 70 + jake_love >= 15 | jake_love +2, corruption +2 |

Caps at kiss — library is too public for more.

---

#### Activity: Creek Swimming with @jake

- **Pattern**: A (standard escalation)
- **Location**: `loc_creek`
- **Schedule**: 15:00-17:00
- **NPC**: `npc_jake`
- **Unlock**: `first_swim`
- **Priority**: 1
- **Energy**: 30

**Base Scene:**

DEFAULT:
> "Creek. Late afternoon. The water catches light through the branches. Jake is already in — up to his waist, pale skin bright against the dark water. He pushes wet hair from his eyes when he sees her. The creek is where pretense dissolves. She's in whatever she's wearing to swim — the improvised sports bra, the bikini Ryan bought, or something from the shop. The water makes everything cling."

WITHDRAWN:
> "He's in the water but further downstream than usual. Not waving her over. Just floating, looking at the sky."

WARM:
> "He's waiting by the bank. Not in the water yet. 'Wanted to go in together.' He takes her hand as they wade in. Cold water, warm hand."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk in the water" (Emotional)** | always | jake_love +2, corruption +1, fitness +2 |
| **"Swim closer" (Physical)** | `exposure_unlock` | physical sub-menu |
| **"Float separately" (Neutral)** | always | jake_love +1, fitness +2 |

**Physical Sub-Menu:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Swim next to him" | `exposure_unlock` | jake_love +1, jake_corruption +1, corruption +2 |
| "Splash fight" | `flirt_unlock` + corruption >= 40 | jake_love +1, jake_corruption +2, corruption +2 |
| "Kiss him in the water" | `kiss_unlock` + corruption >= 70 | jake_love +2, jake_corruption +2, corruption +3 |
| "Hands under the water" | `handjob_unlock` + corruption >= 100 | jake_corruption +3, corruption +4 |
| "Pull him to the bank" | `sex_unlock` + corruption >= 180 | jake_corruption +5, corruption +5 |

Video placeholders: Creek/outdoor setting, bodies in water, escalating intimacy.

---

#### Activity: Late-Night Wall Knocking

- **Pattern**: A (limited escalation)
- **Location**: `loc_lily_room`
- **Schedule**: 22:00-01:00
- **NPC**: `npc_jake` (through the wall)
- **Unlock**: `first_week_complete` + jake_love >= 8
- **Priority**: 1
- **Energy**: 0 (free)

**Base Scene:**

DEFAULT:
> "Late night. Lily's room is dark. Through the wall: tap. Tap-tap. Jake's knock. Their ritual. She knocks back. Silence. Then his muffled voice, barely audible: 'You awake?'"

WITHDRAWN:
> "No knock tonight. She lies there listening. Nothing."

WARM:
> "The knock comes earlier than usual. Tap-tap-tap. Three knocks instead of two. She can hear him smiling through the wall."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk through the wall" (Emotional)** | always | jake_love +2, jake_trust +1 |
| **"Knock back, invite him over" (Physical)** | `kiss_unlock` + jake_love >= 15 | → he comes to her room, physical sub-menu |
| **"Knock back, go to sleep" (Neutral)** | always | jake_love +1 |

**Physical (when he comes to her room):**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Lie next to him" | `kiss_unlock` + corruption >= 70 | jake_love +2, corruption +2 |
| "Kiss in the dark" | `kiss_unlock` + corruption >= 70 | jake_love +2, jake_corruption +2, corruption +3 |
| "More than kissing" | `handjob_unlock` + corruption >= 100 | jake_corruption +3, corruption +4 |
| "Invite him into your bed" | `sex_unlock` + corruption >= 180 | jake_corruption +5, corruption +5 |

---

#### Activity: Park Sketching (Weekends)

- **Pattern**: A (limited — caps at kiss)
- **Location**: `loc_park`
- **Schedule**: 15:00-17:00
- **NPC**: `npc_jake`
- **Unlock**: `town_access` + `drawing_started`
- **Weekdays**: [5,6] (Sat/Sun only)
- **Priority**: 1
- **Energy**: 15

**Base Scene:**

DEFAULT:
> "Park bench. Jake has his sketchbook. Lily has nothing to do but sit near him and watch him draw the pond, the ducks, the old man on the next bench. After ten minutes his pencil drifts from the pond to her jawline. She pretends not to notice."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Tell me about this piece" (Emotional)** | always | jake_love +2, jake_trust +1 |
| **"Lean against his shoulder" (Physical)** | `exposure_unlock` | jake_love +1, corruption +1 |
| **"Sit in comfortable silence" (Neutral)** | always | jake_love +1, jake_trust +1 |

Physical caps at "Kiss on the bench" (`kiss_unlock`) — public park.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### RYAN ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#### Activity: Truck Ride with @ryan

- **Pattern**: A (standard escalation)
- **Location**: `loc_ryans_truck`
- **Schedule**: 15:00-17:00
- **NPC**: `npc_ryan`
- **Unlock**: `town_access`
- **Priority**: 1
- **Energy**: 10

**Base Scene Variants:**

DEFAULT:
> "Ryan's truck. Pine air freshener and the ghost of sawdust. He drives with one hand, radio on classic rock, window cracked. The bench seat leaves a gap between them — too small to ignore, too big to blame on the truck. 'Where to, college girl?'"

WITHDRAWN (post-crisis):
> "The truck is quiet. No radio. His jaw is set. He drives straight to wherever she needs to go. No detours. No commentary. The gap on the bench seat is wider than it used to be."

WARM:
> "He's already in the truck when she comes out. Engine running, her door open. He cleaned the passenger side — the empty cans are gone, the seat is wiped down. He doesn't mention it. 'Hey. Hop in.' Softer than he sounds in front of anyone else."

**Consequence Variants:**
- After `ryan_resisted`: "He opens her door without comment. The silence is careful — he's testing whether she's still afraid of him. She's not. That's worse."
- After `ryan_allowed`: "His hand is already on the center of the bench seat. An invitation with plausible deniability. The dirt road shortcut is becoming a habit."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk on the drive" (Emotional)** | always | ryan_love +2, ryan_trust +1 |
| **"Sit closer" (Physical)** | `exposure_unlock` | physical sub-menu |
| **"Ride in silence" (Neutral)** | always | ryan_love +1 |

**Physical Sub-Menu:**

| Choice | Condition | Effects | Video Placeholder |
|--------|-----------|---------|-------------------|
| "Sit in the middle" | `exposure_unlock` | ryan_love +1, corruption +1 | Image — truck cab, sitting close |
| "Flirt with him" | `flirt_unlock` + corruption >= 40 | ryan_corruption +2, corruption +2 | Image — flirting in truck |
| "Touch his thigh" | `tease_unlock` + corruption >= 55 | ryan_corruption +2, corruption +3 | Video — hand on thigh, driving |
| "Kiss him" | `kiss_unlock` + corruption >= 70 + ryan_love >= 12 | ryan_love +2, ryan_corruption +2, corruption +3 | Video — truck cab kiss, aggressive |
| "Reach over" | `handjob_unlock` + corruption >= 100 + ryan_corruption >= 25 | ryan_corruption +4, corruption +4 | Video — handjob, truck, urgent |
| "Pull over" | `blowjob_unlock` + corruption >= 140 + ryan_corruption >= 30 | ryan_corruption +4, corruption +5 | Video — oral in truck, raw |
| "Truck bed" | `sex_unlock` + corruption >= 180 + ryan_love >= 22 | ryan_corruption +5, corruption +6 | Video — sex, truck bed, outdoors |

---

#### Activity: Gym with @ryan

- **Pattern**: A (standard escalation)
- **Location**: `loc_gym`
- **Schedule**: 12:00-15:00
- **NPC**: `npc_ryan`
- **Unlock**: `town_access` + ryan_trust >= 5
- **Priority**: 1
- **Energy**: 30

**Base Scene:**

DEFAULT:
> "Gym. Fluorescent lights and the smell of rubber mats. Ryan is already on the bench press — arms flexing, sweat on his forehead, tank top dark with effort. He sees her and racks the weight. 'Ready to work?' He looks her over — whatever she's wearing, he has an opinion."

**Clothing-dependent openers (group variants):**
- Starting tier (sports bra + old shorts): "'You own gym clothes or...?' He's teasing. But he glances at her legs."
- Basic athletic: "He nods. Approving. 'Better.' Shows her the weight rack properly."
- Cute athletic: "His rep slows. His eyes track her from the door to the treadmill. He doesn't restart his set."
- Bold athletic: "'Jesus.' One word. He forgets what he was lifting."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Spot me / talk between sets" (Emotional)** | always | ryan_love +1, ryan_trust +2, fitness +3 |
| **"Work out near him" (Physical)** | `exposure_unlock` | physical sub-menu, fitness +3 |
| **"Do your own routine" (Neutral)** | always | ryan_love +1, fitness +3, confidence +1 |

**Physical Sub-Menu:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Stretch near him" | `exposure_unlock` | ryan_corruption +1, corruption +2 |
| "Ask him to show you a form" | `flirt_unlock` + corruption >= 40 | ryan_corruption +2, corruption +2 (his hands adjusting her position) |
| "Locker room hallway" | `tease_unlock` + corruption >= 55 | ryan_corruption +3, corruption +3 |
| "Kiss after the last set" | `kiss_unlock` + corruption >= 70 | ryan_love +2, ryan_corruption +2, corruption +3 |
| "Locker room" | `handjob_unlock` + corruption >= 100 | ryan_corruption +4, corruption +4 |
| "Shower together" | `sex_unlock` + corruption >= 180 | ryan_corruption +5, corruption +6 |

---

#### Activity: TV on the Couch

- **Pattern**: A (standard escalation — proximity-based)
- **Location**: `loc_living_room`
- **Schedule**: 19:00-22:00
- **NPC**: `npc_ryan` (Frank may also be present — group variant)
- **Unlock**: `first_week_complete`
- **Priority**: 1
- **Energy**: 15

**Base Scene:**

DEFAULT:
> "Living room. TV on. Ryan takes one end of the couch. Lily takes the other. The cushion between them is either a buffer or a bridge — depends on the night. If Frank is in the armchair, the dynamic shifts: everything is watched."

FRANK PRESENT variant:
> "Frank is in the armchair. Paper open. Not watching TV. Watching the couch. Ryan sits wider than he needs to — arm along the back. Frank's jaw tightens."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk about the show" (Emotional)** | always | ryan_love +2 |
| **"Sit closer" (Physical)** | `exposure_unlock` | physical sub-menu |
| **"Watch in silence" (Neutral)** | always | ryan_love +1 |

**Physical Sub-Menu (awareness of Frank if present):**

| Choice | Condition | Effects | Note |
|--------|-----------|---------|------|
| "Remove the buffer cushion" | `exposure_unlock` | ryan_love +1, corruption +1 | |
| "Lean against him" | `flirt_unlock` + corruption >= 40 | ryan_corruption +1, corruption +2 | If Frank present: frank_corruption +1 (he sees) |
| "His hand on your thigh" | `tease_unlock` + corruption >= 55 | ryan_corruption +2, corruption +2 | If Frank present: frank_corruption +2 |
| "Kiss during a commercial" | `kiss_unlock` + corruption >= 70 | ryan_love +2, corruption +3 | If Frank present: NOT available (too risky) |
| "Under the blanket" | `handjob_unlock` + corruption >= 100 | ryan_corruption +3, corruption +4 | Blanket hides it. If Frank present: corruption +6 (the risk) |

---

#### Activity: Job Site with @ryan

- **Pattern**: A (limited escalation — work environment)
- **Location**: `loc_workshop`
- **Schedule**: 09:00-12:00
- **NPC**: `npc_ryan` (Frank may be present)
- **Unlock**: `chores_started` + corruption >= 40
- **Priority**: 1
- **Energy**: 25

**Base Scene:**

DEFAULT:
> "Workshop. Sawdust and motor oil. Ryan is hauling materials — heavy lifting that makes his arms flex and his shirt ride up. He puts her to work: holding boards, sorting nails, sweeping. The pay is good ($40). The view is better."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Work and talk" (Emotional)** | always | ryan_love +1, ryan_trust +2, money +40 |
| **"Brush against him" (Physical)** | `exposure_unlock` | physical sub-menu, money +40 |
| **"Work quietly" (Neutral)** | always | ryan_trust +1, money +40, fitness +1 |

Physical caps at kiss — Frank may appear. Locker room/truck escalation happens elsewhere.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### FRANK ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#### Activity: Bookkeeping with @frank

- **Pattern**: A (standard escalation — the office is the arena)
- **Location**: `loc_franks_office`
- **Schedule**: 12:00-15:00
- **NPC**: `npc_frank`
- **Unlock**: `bookkeeping_started` (set by Beat 9, requires corruption >= 40)
- **Priority**: 1
- **Energy**: 20

**Base Scene Variants:**

DEFAULT:
> "Frank's office. Door closed. The amber desk lamp makes everything warmer than it should be. He's behind the desk — invoices, receipts, the mechanical click of his calculator. He pushes a stack of papers toward her chair. 'Column B needs reconciling.' She sits. Their knees are two feet apart. The room smells like leather and old paper and sawdust off his shirt."

WITHDRAWN (post-crisis):
> "Door open today. He left it open. The papers are on the desk with a note: 'Column B. Leave them when you're done.' He's not in the room. $25 on the counter."

WARM:
> "He pulls her chair next to his instead of across the desk. 'Easier to show you from here.' Their shoulders almost touch. He points at numbers with one hand. His other hand rests on the back of her chair. She can feel the heat from his arm."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk about the business" (Emotional)** | always | frank_love +1, frank_trust +2, money +25 |
| **"Lean closer" (Physical)** | `exposure_unlock` | physical sub-menu, money +25 |
| **"Do the work, leave" (Neutral)** | always | frank_trust +1, money +25 |

**Physical Sub-Menu:**

| Choice | Condition | Effects | Video Placeholder |
|--------|-----------|---------|-------------------|
| "Brush his hand reaching for a file" | `exposure_unlock` | frank_love +1, corruption +1 | Image — office proximity, hand contact |
| "Comment on his aftershave" | `flirt_unlock` + corruption >= 40 | frank_corruption +1, corruption +2 | Image — office flirtation |
| "Bend over the desk slowly" | `tease_unlock` + corruption >= 55 | frank_corruption +2, corruption +3 | Video — teasing in office, deliberate |
| "Kiss him over the ledger" | `kiss_unlock` + corruption >= 70 + frank_love >= 20 | frank_love +2, frank_corruption +2, corruption +3 | Video — office kiss, forbidden, desk |
| "Reach under the desk" | `handjob_unlock` + corruption >= 100 + frank_trust >= 22 | frank_corruption +4, corruption +4 | Video — under-desk handjob, power |
| "On your knees" | `blowjob_unlock` + corruption >= 140 + frank_love >= 28 | frank_corruption +5, corruption +5 | Video — office oral, dominance |
| "Lock the door" | `sex_unlock` + corruption >= 180 + frank_love >= 30 | frank_corruption +6, corruption +6 | Video — office sex, desk, authority |

---

#### Activity: Cooking Dinner with @frank

- **Pattern**: A (limited escalation — kitchen, others may interrupt)
- **Location**: `loc_kitchen`
- **Schedule**: 17:00-19:00
- **NPC**: `npc_frank`
- **Unlock**: `first_week_complete` + frank_trust >= 8
- **Priority**: 1
- **Energy**: 20

**Base Scene:**

DEFAULT:
> "Kitchen. Frank is chopping vegetables. His sleeves are rolled, forearms dusted with flour or sawdust — she's never sure which. He doesn't look up when she enters, but he nods at the cutting board next to him. 'Tomatoes need dicing.' Side by side at the counter. Close enough that their elbows touch when she reaches for the knife."

WITHDRAWN:
> "He's cooking alone. Didn't set out the second cutting board. 'Dinner's in twenty minutes.' Dismissal wrapped in information."

WARM:
> "He's waiting for her before starting. Two cutting boards, two knives, two glasses of wine he shouldn't have poured. 'Thought we'd try something different tonight.' He means the recipe. They both hear the other meaning."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk while cooking" (Emotional)** | always | frank_love +2, frank_trust +1 |
| **"Stand too close" (Physical)** | `exposure_unlock` | physical sub-menu |
| **"Cook efficiently, set the table" (Neutral)** | always | frank_trust +2 |

**Physical Sub-Menu (limited — kitchen, others may walk in):**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Brush against him reaching for a pan" | `exposure_unlock` | frank_love +1, corruption +1 |
| "Taste from his spoon" | `flirt_unlock` + corruption >= 40 | frank_corruption +1, corruption +2 |
| "His hand on her waist guiding her" | `tease_unlock` + corruption >= 55 | frank_corruption +2, corruption +2 |
| "Quick kiss (risky — someone could walk in)" | `kiss_unlock` + corruption >= 70 | frank_love +2, corruption +4 |

Caps at kiss in kitchen — too public for more. The office is Frank's escalation space.

---

#### Activity: "Overtime" Bookkeeping with @frank

- **Pattern**: A (high-tier escalation — evening, door locked)
- **Location**: `loc_franks_office`
- **Schedule**: 17:00-19:00 (Evening — alternative to dinner)
- **NPC**: `npc_frank`
- **Unlock**: `bookkeeping_started` + corruption >= 100 + frank_trust >= 18
- **Priority**: 1
- **Energy**: 20

**Base Scene:**

DEFAULT:
> "Evening. The house is loud with dinner sounds she's not part of tonight. Frank's office, door locked. The regular bookkeeping ended an hour ago but neither mentioned it. He pours whiskey. Two glasses. The invoices are a pretense now. Everyone knows it — especially Frank."

**This activity starts at kiss tier (corruption >= 100 gate means player is already deep).**

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk about what this really is" (Emotional)** | always | frank_love +3, frank_trust +2, money +60 |
| **"Close the distance" (Physical)** | always (gate is the activity unlock) | physical sub-menu, money +60 |
| **"Do overtime work, leave" (Neutral)** | always | frank_trust +1, money +60 |

**Physical Sub-Menu (starts higher — the gate IS the permission):**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Kiss him" | corruption >= 100 + `kiss_unlock` | frank_love +2, frank_corruption +3, corruption +3 |
| "His hands on you" | `handjob_unlock` + corruption >= 100 | frank_corruption +4, corruption +4 |
| "On your knees" | `blowjob_unlock` + corruption >= 140 | frank_corruption +5, corruption +5 |
| "His desk" | `sex_unlock` + corruption >= 180 | frank_corruption +6, corruption +6 |

---

#### Activity: Workshop Help with @frank

- **Pattern**: A (limited — work, early game trust-building)
- **Location**: `loc_workshop`
- **Schedule**: 07:00-09:00
- **NPC**: `npc_frank`
- **Unlock**: `first_week_complete`
- **Priority**: 1
- **Energy**: 25

**Base Scene:**

DEFAULT:
> "Workshop. 7 AM. Frank is already there — table saw silent, sorting lumber. He works with purpose — every movement efficient, practiced. He shows her what to do: hold this board, sort these nails, sweep the floor. Not much talking. But working next to someone in silence can be its own kind of intimacy."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Ask about the business" (Emotional)** | always | frank_love +1, frank_trust +2 |
| **"Hand him tools, stay close" (Physical)** | `exposure_unlock` | frank_love +1, corruption +1 |
| **"Work, get paid, leave" (Neutral)** | always | frank_trust +1, fitness +1 |

Physical caps at flirting — the workshop is Frank's professional space. Limited escalation here. The office is where things happen.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION B: MEAL CANVASES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Meals are free to enter (no energy cost to start). Three per day. Kitchen is the social hub.

### Breakfast

- **Canvas**: `meal_breakfast`
- **Location**: `loc_kitchen`
- **Schedule**: 07:00-09:00
- **NPC**: Frank + Jake usually present. Ryan sleeps in 50% of the time.
- **Priority**: 1
- **is_repeatable**: true

**Base Scene:**
> "Kitchen. Morning light. Coffee's already made — Frank's timer. Jake is at the table with cereal and his sketchbook. Frank reads the paper. Ryan's chair is either occupied (groggy, tank top, bed hair) or empty (sleeping in)."

**Choices:**

| Choice | Effect | Condition |
|--------|--------|-----------|
| **"Eat together" (Neutral)** | Energy +5, love +1 to each present NPC | Always |
| **"Talk over coffee" (Emotional)** | Love +2 to ONE chosen NPC (portrait click), no energy restore | Always |
| **"Sit closer / brush hands" (Physical)** | Corruption +1-2 to chosen NPC, no energy restore | After `exposure_unlock` |

**Dinner special mechanic**: At dinner, usually all three NPCs are present (Ryan out ~20%). Lily picks ONE portrait to interact with. The other two are watching. This creates the tension of choosing who to engage while others observe.

### Lunch

- **Canvas**: `meal_lunch`
- **Location**: `loc_kitchen`
- **Schedule**: 12:00-14:00
- **NPC**: Often solo or with Jake (Frank in office, Ryan at job site)
- **Priority**: 1
- **is_repeatable**: true

**Base Scene:**
> "Kitchen. Midday quiet. The house is mostly empty — Frank in the office, Ryan on the job site or in town. If Jake's home (weekends, after class), he's at the table with homework spread around a sandwich."

**Choices:**

| Choice | Effect | Condition |
|--------|--------|-----------|
| **"Eat" (Neutral)** | Energy +5, love +1 to present NPC | Always |
| **"Talk" (Emotional)** | Love +2 to present NPC | If Jake/Frank present |
| **"Sit close" (Physical)** | Corruption +1 to present NPC | After `exposure_unlock`, if NPC present |

### Dinner

- **Canvas**: `meal_dinner`
- **Location**: `loc_kitchen`
- **Schedule**: 17:00-19:00
- **NPC**: Usually all three (Ryan absent ~20%)
- **Priority**: 1
- **is_repeatable**: true

**Base Scene:**
> "Kitchen. Evening. The table is set for four — Frank cooked, or Lily did, or they both did. This is the ONE time all three men are in the same room with her. The tension varies by day: sometimes it's just a meal. Sometimes it's a minefield of glances."

**Group dynamic**: When all three present, Lily chooses ONE NPC portrait to interact with. Others see the choice.

**Choices:**

| Choice | Effect | Condition |
|--------|--------|-----------|
| **"Eat together" (Neutral)** | Energy +10, love +1 to each present NPC | Always |
| **"Talk to [chosen NPC]" (Emotional)** | Love +2 to chosen, others see you chose | Always |
| **"Foot under the table / brush hands" (Physical)** | Corruption +1-2 to chosen, others may notice | After `exposure_unlock` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION C: UTILITY CANVASES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Chores / Jobs

| Canvas | Name | Location | Schedule | Pay | Energy | Trust | Unlock | Max/Day |
|--------|------|----------|----------|-----|--------|-------|--------|---------|
| `utility_house_cleaning` | House Cleaning | `loc_kitchen` | 09:00-12:00 | $20 | 25 | frank_trust +1 (if home) | `chores_started` | 1 |
| `utility_bookkeeping` | Bookkeeping | `loc_franks_office` | 12:00-15:00 | $25 | 20 | frank_trust +1 | `bookkeeping_started` | 1 |
| `utility_job_site` | Job Site Labor | `loc_workshop` | 09:00-12:00 | $40 | 25 | ryan_trust +1 | corruption >= 40 | 1 |
| `utility_diner_shift` | Diner Waitressing | `loc_diner` | 17:00-19:00 | $45 | 20 | — | confidence >= 30 + `town_access` | 1 |
| `utility_art_modeling_clothed` | Art Modeling (Clothed) | `loc_jakes_room` | 12:00-15:00 | $30 | 15 | jake_love +1 | corruption >= 50 | 1 |
| `utility_art_modeling_nude` | Art Modeling (Nude) | `loc_jakes_room` | 12:00-15:00 | $80 | 15 | jake_corruption +2 | corruption >= 130 | 1 |
| `utility_overtime_bookkeeping` | "Overtime" Bookkeeping | `loc_franks_office` | 17:00-19:00 | $60 | 20 | frank_corruption +1 | corruption >= 100 | 1 |
| `utility_ryans_favors` | Ryan's "Favors" | `loc_ryans_truck` | 19:00-22:00 | $100 | 20 | ryan_corruption +2 | corruption >= 150 | 1 |
| `utility_franks_arrangement` | Frank's "Arrangement" | `loc_franks_office` | 22:00-01:00 | $150 | 20 | frank_corruption +3 | corruption >= 180 | 1 |

**Note**: Art modeling (clothed/nude) and overtime/favors/arrangement are ALSO NPC activities with escalating choices (covered in Section A). The utility table above captures the MONEY component. When these fire as activities, the player gets both the pay and the NPC interaction choices.

### Time Advancement / Rest

| Canvas | Name | Location | Schedule | Effect | Unlock |
|--------|------|----------|----------|--------|--------|
| `utility_sleep` | Go to Sleep | `loc_lily_room` | 22:00-01:00 | Energy → max (100, or 110 at fitness 61+). Advances to Early Morning. | Always |
| `utility_nap` | Afternoon Nap | `loc_lily_room` | 12:00-15:00 | Energy +20. Advances 120 min. | Always |
| `utility_shower` | Shower | `loc_bathroom` | Any | Energy +10. Prevents beauty decay. Free. | Always |
| `utility_morning_routine` | Morning Routine | `loc_bathroom` | 05:00-07:00 | Shower + grooming + optional makeup. Sets polished state if all conditions met. | Always |

### Morning Routine Detail

The morning routine canvas is the daily beauty/presentation decision:

**Canvas**: `utility_morning_routine`
**Location**: `loc_bathroom`
**Schedule**: 05:00-07:00
**Priority**: 2
**is_repeatable**: true

**Choices:**

| Choice | Energy | Beauty Effect | Polished? |
|--------|--------|---------------|-----------|
| "Shower only" | +10 | Prevents decay | No |
| "Shower + Grooming" | +5 | Prevents decay, enables "groomed" | No (need makeup + Cute+ outfit) |
| "Shower + Grooming + Makeup" | +5 | Prevents decay, +1-2 beauty buff | Yes (if Cute+ outfit equipped after) |
| "Skip everything" | +0 | Beauty decays | No |

After routine → `utility_change_outfit` at `loc_lily_room` to select clothing.

### Shopping / Travel

| Canvas | Name | Location | Schedule | Effect | Notes |
|--------|------|----------|----------|--------|-------|
| `utility_bus_to_town` | Take the Bus | `loc_property` | Any | money -2, 40 min travel time. Arrives at `loc_town`. | Nobody knows where she went. |
| `utility_ryan_ride` | Ride with Ryan | `loc_property` | 15:00-17:00 | Free, 15 min. Arrives at `loc_town`. | Ryan sees everything — what she buys, where she goes. |
| `utility_grocery_shopping` | Grocery Shopping | `loc_general_store` | Any | money -20 (food contribution). Covers 5 days of food. | Required to avoid frank_trust penalty. |
| `utility_clothing_shopping` | Clothing Shopping | `loc_clothing_store` | Any | Variable cost. Wardrobe items by corruption tier. | Gated by `town_access`. |
| `utility_beauty_shopping` | Beauty Products | `loc_general_store` | Any | Variable cost. Makeup kits, skincare, perfume. | |

### Recurring Expense Canvases

| Canvas | Name | Trigger | Cost | Effect | Timer |
|--------|------|---------|------|--------|-------|
| `utility_bus_pass` | Bus Pass Due | days_since(`bus_pass_paid`) >= 30 | $80 | Maintains bus access for 30 days | Monthly |
| `utility_art_supplies` | Art Supplies Due | days_since(`art_supplies_paid`) >= 30 | $60 | Maintains campus events | Monthly |
| `utility_phone_bill` | Phone Bill Due | days_since(`phone_bill_paid`) >= 30 | $45 | Maintains phone access | Monthly |
| `utility_food_contribution` | Food Contribution | days_since(`food_paid`) >= 7 | $50 | Avoids frank_trust -3 | Weekly |

These fire as priority 2 events when the timer triggers. If the player can't afford them (money < cost), the canvas presents the choice to pay or skip with consequences per Phase 2 non-payment table.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION D: SOLO ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Canvas | Name | Location | Schedule | Energy | Effect | Notes |
|--------|------|----------|----------|--------|--------|-------|
| `solo_yoga` | Yoga in Room | `loc_lily_room` | Any | 10 | fitness +1 | Always available. Low energy, low reward. Solo, private. |
| `solo_jog_property` | Morning Jog (Property) | `loc_yard` | 07:00-09:00 | 15 | fitness +1, confidence +1 | Jogging loops around the yard. No transport needed. |
| `solo_jog_park` | Jogging (Park) | `loc_park` | 12:00-15:00 | 20 | fitness +2, confidence +1 | Requires town access. Better gains than property. |
| `solo_campus_classes` | Art Classes | `loc_campus` | 09:00-12:00 | 15 | Mandatory Mon-Thu. Maintains campus events. | Requires bus or Ryan's ride. |
| `solo_journal` | Journal / Phone | `loc_lily_room` | Any | 5 | No stat gains. Advances time 60 min. Story reflections. | Hint system: journal entries suggest next steps. |
| `solo_spa_day` | Spa / Self-Care | `loc_lily_room` | 12:00-15:00 | 15 | beauty +2 permanent | Requires skincare products owned. |
| `solo_stargazing` | Stargazing | `loc_yard` | 22:00-01:00 | 10 | corruption +1 (alone, dark, vulnerable). | Atmospheric. Random encounter possible (any NPC coming outside). |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACTIVITY COVERAGE SUMMARY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### By NPC

| NPC | Activities | Locations | Escalation Cap |
|-----|-----------|-----------|----------------|
| **Jake** | Drawing Session, Studying, Creek Swimming, Wall Knocking, Park Sketching | Jake's Room, Library, Creek, Lily's Room, Park | Full (sex tier) |
| **Ryan** | Truck Ride, Gym, TV Couch, Job Site | Truck, Gym, Living Room, Workshop | Full (sex tier) |
| **Frank** | Bookkeeping, Cooking, Overtime, Workshop Help | Office, Kitchen, Workshop | Full (sex tier) |

### By Time Slot

| Period | Activities Available |
|--------|--------------------|
| **Early Morning** | Morning routine, shower |
| **Morning** | Breakfast, morning jog (property), workshop help (Frank) |
| **Late Morning** | Campus classes, house cleaning, job site labor |
| **Afternoon** | Lunch, bookkeeping (Frank), drawing session (Jake), gym (Ryan), art modeling, nap, park jog, beauty shopping |
| **Late Afternoon** | Creek swim, truck ride (Ryan), studying (Jake), park sketching (weekend), clothing shopping |
| **Evening** | Dinner, cooking (Frank), overtime bookkeeping (Frank), diner shift |
| **Night** | TV (Ryan/Frank), Jake's room visit, Frank's office late, journal, Ryan's favors |
| **Late Night** | Kitchen encounter (Frank random), wall knocking (Jake), Frank's arrangement, sleep, stargazing |

### No Dead Zones Check

At every point in the game, the player has 2+ NPC activities available per time slot:

| Corruption | Available NPC Activities |
|-----------|------------------------|
| 0-25 | Meals (all), Workshop (Frank), Wall knocking (Jake), TV (Ryan) — limited but present |
| 25-40 | + Drawing session (Jake), Truck ride (Ryan) — exposure_unlock opens physical sub-menus |
| 40-60 | + Bookkeeping (Frank), Job site (Ryan), Gym (Ryan) — flirt tier opens |
| 60-100 | + Art modeling (Jake), Cooking (Frank) — kiss tier opens |
| 100-140 | + Overtime (Frank) — handjob tier opens |
| 140-180 | + Modeling nude (Jake), Ryan's favors — blowjob tier opens |
| 180+ | + Frank's arrangement — sex tier opens, all activities at max escalation |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue to Phase 6: Story Arc,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━