# PHASE 5: ACTIVITIES
# New In Town

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION A: NPC ACTIVITIES (ESCALATING)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ═══════════════════════════════════════
# TOM ACTIVITIES (2)
# ═══════════════════════════════════════

---

## TOM ACTIVITY 1: "Coffee With Tom"

- **Pattern**: A (standard escalation)
- **Location**: `loc_diner` (default) or `loc_school_classroom` (alternate)
- **Schedule**: 12:00-15:00
- **NPC**: Tom
- **Unlock conditions**: `tom_locks_checked`
- **Priority**: 1
- **Is Repeatable**: true
- **Max triggers per day**: 1
- **Availability**: Mon / Wed / Fri
- **Weekdays (TOML)**: `[0, 2, 4]`
- **Energy Cost**: -10

---

### Base Scene (always shown)

**DEFAULT**: The diner. Afternoon. Tom is already there — he showed up fifteen minutes early and has been staring at the door. He's in his off-duty clothes: a clean flannel, jeans that fit like he thought about it. He stands up when she arrives, bumps the table, steadies his coffee mug. "Hey. Hi. You look — how are you?"

He always asks how she is before he tells her anything about himself. He's the only man in Millfield who does that.

**WITHDRAWN variant** (post-tension — e.g., after `tom_saw_ray`): He's at the booth but hasn't ordered for her. He smiles, but it doesn't reach his eyes. He asks about school, not about her. The questions feel like walls.

**WARM variant** (high `devotion`, post-`tom_groping_unlocked`): He's saved the booth in the back corner — their booth now. He ordered her coffee the way she takes it. When she slides in, his knee finds hers under the table immediately. He can't stop looking at her mouth.

**Media**: IMAGE — "Young couple at diner booth, small-town America, afternoon, coffee cups, him nervous and adoring, her confident and amused"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Ask about his day" | always | exit | +1 devotion |
| "Lean close when talking" | devotion >= 22 | warm | +2 devotion, +1 confidence |
| "Touch his thigh under the table" | devotion >= 42 + tom_kiss_unlocked | kiss | +3 devotion, +1 corruption |
| "Guide his hand between your legs" | devotion >= 62 + tom_groping_unlocked | foreplay | +4 devotion, +1 corruption, reputation -1 |

**Caps at foreplay** — this is a public diner. The risk of a public groping incident is the peak of what this location supports. Full escalation happens at Emma's Room.

### Escalation Nodes

**WARM NODE**: She leans across the table. Her hand on his arm. She says something — it doesn't matter what — while her thumb traces circles on the inside of his wrist. His pulse is visible. He loses his train of thought mid-sentence and just looks at her.

The waitress refills their coffee and says, "You two are cute." Tom turns the color of ketchup.

**Media**: IMAGE — "Young couple in diner booth, her leaning close, hand on his arm, intimate conversation, small town"

**Exit**: "Keep talking" → +2 devotion | "Smile and pull away" → +1 devotion, +1 confidence

---

**KISS NODE**: Under the table, her hand finds his thigh. She squeezes once. He freezes. His fork clatters. She doesn't move her hand. Just lets it rest there, warm, possessive, while they talk about nothing. Her fingers creep higher. His voice goes up half an octave.

"Emma, we're in—"

"I know where we are."

**Media**: VIDEO — "Woman's hand under diner table on man's thigh, hidden from other diners, charged tension"

**Exit**: "Pull away and smile" → +3 devotion, +1 corruption | "Whisper 'Later'" → +2 devotion, +2 corruption

---

**FOREPLAY NODE**: She takes his hand under the table. Guides it to her thigh. Higher. His breathing changes. The waitress is across the room. An older couple in the far booth. His fingers touch the hem of her skirt and he makes a sound that he covers with a cough.

She controls his hand — where it goes, how long it stays. She's looking at him the whole time, eating her pie with the other hand like nothing is happening.

"You're doing great, Tom."

He nearly dies.

**Media**: VIDEO — "Couple at diner booth, his hand under her skirt beneath table, her composed face, his red face, public setting, risky"

**Exit**: "That's enough for today" → +4 devotion, reputation -1 | "Let him continue" → +3 devotion, +2 corruption, reputation -2

---

**Hardship**: Afternoon slot — same time as tutoring ($30). Coffee with Tom earns devotion. Tutoring earns money and reputation. Can't do both.

---
---

## TOM ACTIVITY 2: "Visit Tom" (Emma's Room)

- **Pattern**: A (standard escalation)
- **Location**: `loc_bar_emma_room`
- **Schedule**: 19:00-01:00
- **NPC**: Tom
- **Unlock conditions**: `tom_kiss_unlocked`
- **Priority**: 1
- **Is Repeatable**: true
- **Max triggers per day**: 1
- **Availability**: Any day
- **Weekdays (TOML)**: `[]`
- **Energy Cost**: -15

---

### Base Scene

**DEFAULT**: She texts him. "Come over." He's at her door in twenty minutes, hair freshly combed, smelling like soap. He sits on the edge of her bed and can't figure out what to do with his hands. She puts on music — anything to fill the nervous silence.

**WITHDRAWN**: He comes over but sits in the chair, not the bed. Something's off. He's thinking about something — the handyman, the way she looked at someone else. He's here because she asked, but he's not fully hers tonight.

**WARM**: He doesn't knock anymore. Just opens the door. Sits next to her. Puts his arm around her without hesitating. He's learning. Slowly, but he's learning. "I missed you." He says it like it's a fact, not a line.

**Media**: IMAGE — "Young man sitting on edge of bed in small room, nervous but eager, woman standing by door, intimate setting"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Just talk" | always | exit | +1 devotion |
| "Kiss him" | devotion >= 42 + tom_kiss_unlocked | kiss | +2 devotion, +1 corruption |
| "Guide his hands" | devotion >= 62 + tom_groping_unlocked | foreplay | +2 devotion, +2 corruption |
| "Teach him" | devotion >= 82 + tom_oral_unlocked | intimate | +3 devotion, +1 confidence |
| "Take him to bed" | devotion >= 82 + tom_sex_unlocked | intense | +3 devotion, +2 corruption |

### Escalation Nodes

**KISS NODE**: She pulls him in by his collar. He still kisses like he's asking permission — soft, careful, his hands hovering near her waist. She grabs his hands and puts them on her hips. "You can touch me, Tom." He does. Gently. Too gently. She tightens his grip with her hands over his.

**Media**: VIDEO — "Young couple kissing in small bedroom, her guiding his hands, him tentative, her in control"

**Exit**: "Pull back" → +2 devotion | "Keep teaching" → +2 devotion, +1 corruption

---

**FOREPLAY NODE**: She puts him on the bed. Straddles him. Takes his hands and places them — here, then here, then here. He follows instructions. He's getting better at this. When she moans — real, not performed — his face lights up like he's solved something.

"There. Just like that."

**Media**: VIDEO — "Woman straddling man on bed, guiding his hands on her body, him eager and learning, small room"

**Exit**: "That's enough for tonight" → +2 devotion, +2 corruption | "Don't stop" → +3 devotion, +1 confidence

---

**INTIMATE NODE**: She pushes him back on the bed. "Your turn to practice." She's taught him technique over multiple visits and he's improved. He goes down on her with the earnest focus of a student who wants to pass. She directs: "Slower. Right there. Don't stop." When she finishes, she runs her fingers through his hair. "Good boy."

The words hit him like a drug. Every time.

**Media**: VIDEO — "Man performing oral on woman in bed, her hands in his hair, small bedroom, intimate"

**Exit**: "Hold him after" → +3 devotion, +1 confidence | "Tell him what he did right" → +2 devotion, +2 corruption

---

**INTENSE NODE**: She's on top. Always on top with Tom. She controls the pace, controls his hands, controls when he's allowed to finish. He's completely surrendered to her direction. When she pins his wrists, he doesn't resist — he arches into it.

Afterward, he lies there looking at her like she invented oxygen. She traces patterns on his chest and thinks about the next man she needs to see this week.

**Media**: VIDEO — "Couple having sex, woman on top, his hands pinned, small bedroom, she's in control, intense"

**Exit**: "Stay with him" → +3 devotion, +2 corruption | "Send him home" → +2 devotion, +1 confidence

---

# ═══════════════════════════════════════
# RAY ACTIVITIES (2)
# ═══════════════════════════════════════

---

## RAY ACTIVITY 1: "Evening at the Bar (Ray Focus)"

- **Pattern**: A (standard escalation)
- **Location**: `loc_bar_floor`
- **Schedule**: 17:00-22:00
- **NPC**: Ray
- **Unlock conditions**: `phase_1_complete`
- **Priority**: 1
- **Is Repeatable**: true
- **Max triggers per day**: 1
- **Availability**: Any day
- **Weekdays (TOML)**: `[]`
- **Energy Cost**: -15
- **Money Cost**: -5 to -8 (drinks)

---

### Base Scene

**DEFAULT**: The bar at evening. Ray is at his usual stool — end of the bar, back against the wall, clear sightline to the door. A beer in front of him, half-finished. He doesn't look up when she walks in. She sits two stools down. Orders whiskey. The silence between them is comfortable in a way conversation with Tom never is.

**WITHDRAWN variant** (post-`ray_feelings_emerge`): He's at his stool but further down the bar. Nursing his beer slower. He nods when she sits. Doesn't initiate. The warmth is there, buried, but something is pulling him back. He's fighting what he feels.

**WARM variant** (high `interest`): He's saved the stool next to him. When she sits, his knee touches hers under the bar. He orders her drink before she asks. "Whiskey. Neat." He knows. The smallest intimacy — knowing how someone takes their drink — means more from Ray than speeches mean from other men.

**Media**: IMAGE — "Man and woman at dive bar counter, evening, him weathered and quiet, her confident, whiskey glasses, amber light"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Sit near him, drink quietly" | always | exit | +1 interest |
| "Ask about his work, touch his forearm" | confidence >= 20 | warm | +2 interest, +1 confidence |
| "Whisper something about last time" | confidence >= 40 + ray_kiss_unlocked | kiss | +3 interest, reputation -1 if overheard |
| "Follow him to his truck in the parking lot" | corruption >= 50 + ray_groping_unlocked | foreplay | +4 interest, reputation -2 |

**Caps at foreplay** — the bar is public. Parking lot is semi-public. Higher escalation happens at Ray's shed/truck or Emma's room (via story events).

### Escalation Nodes

**WARM NODE**: She puts her hand on his forearm. Leaves it there. He looks at her hand. Then at her. His jaw tightens — not rejection. Control. He's controlling the response she can see. But underneath her palm, his pulse is faster than his face lets on.

"Tough day?"

"Every day's a tough day." He covers her hand with his for two seconds. Then removes it. Drinks his beer. But those two seconds — she felt his callouses, his warmth, the grip that held back.

**Media**: IMAGE — "Woman's hand on man's forearm at bar, intimate, him looking at her hand, amber lighting"

**Exit**: "Stay and drink" → +2 interest, +1 confidence | "Leave him wanting" → +1 interest, +2 confidence

---

**KISS NODE**: She leans close. Whispers in his ear — something about the staircase, about his hands, about what she's thinking right now. His grip on his beer tightens. The bartender (Jake) is ten feet away. Other drinkers around them.

"You can't say that here." His voice is low, rough.

"I just did."

**Media**: VIDEO — "Woman whispering in man's ear at bar, intimate, danger of being overheard, bar setting"

**Exit**: "Walk away smiling" → +3 interest, reputation -1 | "Hold his gaze" → +2 interest, +1 corruption

---

**FOREPLAY NODE**: Bar closing. She follows him to the parking lot. His truck is in the dark corner — always parked furthest from the door, old habit. She leans against the hood. He stands in front of her. The parking lot is empty but exposed — headlights from the road, the bar's back door ten yards away.

He puts his hands on the hood, either side of her. Trapping her. His mouth on her neck. Her back arches against the truck. His hand under her jacket, under her shirt, on the warm skin of her stomach.

"We shouldn't—"

"Then stop."

He doesn't stop.

**Media**: VIDEO — "Couple against pickup truck in dark parking lot, him pressing against her, hands under jacket, outdoor, risky"

**Exit**: "Push him away and go inside" → +4 interest, reputation -2 | "Pull him closer" → +3 interest, +2 corruption, reputation -2

---

**Hardship**: Evening bar time competes with Jake's evening schedule. Can't work on both Ray and Jake in the same night without one noticing.

---
---

## RAY ACTIVITY 2: "The Workshop" (Ray's Shed)

- **Pattern**: A (standard escalation)
- **Location**: `loc_ray_truck_shed`
- **Schedule**: 15:00-17:00
- **NPC**: Ray
- **Unlock conditions**: `ray_first_crack`
- **Priority**: 1
- **Is Repeatable**: true
- **Max triggers per day**: 1
- **Availability**: Tue / Thu / Sat
- **Weekdays (TOML)**: `[1, 3, 5]`
- **Energy Cost**: -15

---

### Base Scene

**DEFAULT**: Ray's workspace — a corrugated shed behind the bar, tools on pegboard walls, a workbench covered in sawdust, his truck parked outside with the tailgate down. He's fixing something — always fixing something. She shows up and he doesn't stop working, but he nods. "Hand me the three-eighths."

Working near Ray is its own kind of intimacy. He doesn't talk much, but he teaches her things: how to check a level, how to sand with the grain, how to tighten a bolt without stripping it. The lessons are excuses. They both know it.

**WITHDRAWN**: He's working but hasn't looked up. She has to stand closer than usual to get his attention. He hands her tools without making eye contact. The distance isn't cold — it's protective. He's holding something back.

**WARM**: He's been waiting. Left a pair of work gloves out for her — her size. When she picks up the saw, he comes up behind her to correct her grip without being asked. His hands over hers. He doesn't step back as quickly as he used to.

**Media**: IMAGE — "Man working in corrugated shed, workbench, tools, pickup truck outside, woman handing him tools, afternoon light"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Work alongside him" | always | exit | +1 interest, +1 confidence |
| "Stand closer while he works" | interest >= 22 | warm | +2 interest, +2 confidence |
| "Press against him while he shows you" | interest >= 42 + ray_groping_unlocked | foreplay | +3 interest, +2 corruption |
| "His truck. The cab. Now." | interest >= 62 + ray_oral_unlocked | intimate | +3 interest, +2 confidence |
| "Pull him to the workbench" | interest >= 82 + ray_sex_unlocked | intense | +3 interest, +2 corruption, +1 confidence |

### Escalation Nodes

**WARM NODE**: He's cutting a board. She stands at the end, holding it steady. Their eyes meet over the sawdust. The saw makes a rhythmic sound. Neither speaks. He finishes the cut. Looks at her. The board is cut but neither of them lets go of their end.

"You're a quick learner."

"I had a good teacher."

The compliment lands differently than it would from anyone else. From Emma to Ray, "good teacher" is a weapon.

**Media**: IMAGE — "Man and woman working with saw in shed, eye contact, sawdust in air, intimate labor"

**Exit**: "Keep working" → +2 interest, +2 confidence | "Let the moment stretch" → +2 interest, +1 corruption

---

**FOREPLAY NODE**: He's behind her again. Correcting her grip. But this time she pushes back deliberately — her body against his. His arms tighten around her. The tool clatters to the workbench. His hand spreads across her stomach. His breathing is in her ear.

She reaches back and grabs his belt. "Don't move."

He doesn't move. The man who takes orders from no one stands perfectly still because she told him to.

**Media**: VIDEO — "Man pressed against woman from behind at workbench, shed setting, his hands on her stomach, physical tension"

**Exit**: "Turn around and face him" → +3 interest, +2 corruption | "Stay like this" → +2 interest, +2 confidence

---

**INTIMATE NODE**: His truck. The cab. She leads him there by the hand — a reversal he notices. Inside, she takes control. The bench seat. The dark. Her hands on his belt. She drops down.

Ray is different than Tom — he doesn't freeze, doesn't need directions. But he lets her set the pace. His hand in her hair is firm but not controlling. He's letting her lead. From Ray, that's a revolution.

**Media**: VIDEO — "Woman giving oral in truck cab, dark, cramped, man's hand in her hair, parking lot behind shed"

**Exit**: "Come back up" → +3 interest, +2 confidence | "Finish him" → +3 interest, +2 corruption

---

**INTENSE NODE**: The workbench. She clears the sawdust with her arm and pushes him against it. The shed door is closed but not locked. The bar is fifty yards away. Someone could walk the path at any time.

Sex with Ray is physical — workbench edge digging into her back, his hands on her thighs, the shed smelling like motor oil and sawdust. He's strong enough to lift her. She wraps her legs around him. He buries his face in her neck.

Afterward — the part that complicates things — he doesn't immediately get dressed. He stands there, looking at her. His expression is unguarded for once. Soft. She doesn't want soft from Ray. She wanted the challenge.

"Same time Thursday?"

"Yeah."

**Media**: VIDEO — "Couple having sex on workbench in shed, rustic, physical, her legs around him, tools and sawdust around them"

**Exit**: "Get dressed and leave" → +3 interest, +2 corruption, +1 confidence

---

# ═══════════════════════════════════════
# MARK ACTIVITIES (1)
# ═══════════════════════════════════════

---

## MARK ACTIVITY 1: "Parent Conferences"

- **Pattern**: A (standard escalation)
- **Location**: `loc_school_classroom`
- **Schedule**: 15:00-17:00
- **NPC**: Mark
- **Unlock conditions**: `mark_first_conference`
- **Priority**: 1
- **Is Repeatable**: true
- **Max triggers per day**: 1
- **Availability**: Tue / Thu
- **Weekdays (TOML)**: `[1, 3]`
- **Energy Cost**: -10

---

### Base Scene

**DEFAULT**: Late afternoon. The classroom after hours. Mark arrives for a "conference" — his son's grades, the fundraiser, whatever excuse he manufactured this week. He sits across from her desk. Professional distance. Door open. Other teachers in the building.

He asks about his son. She answers. The answers are real — she's still a good teacher. But between the answers, their eyes hold a beat too long. His knee bounces under the desk. She tucks her hair behind her ear and he watches her fingers like they're performing surgery.

"So, everything looks good academically?"

"Perfect. He's doing really well."

"Good. That's... good."

Neither of them moves to end the meeting.

**WITHDRAWN variant** (post-`karen_school_confrontation`): He comes in but doesn't close the door. Doesn't sit. Quick, professional, eyes on the paperwork. "Just wanted to check on his reading log." He leaves before the silence can fill. His hands are shaking.

**WARM variant** (high `desire`, pre-crisis): He closes the door behind him — casually, like the hallway draft. "Drafty corridor." They both know what a closed door means now. He sits closer than the desk requires. Brings her coffee from the diner. The excuse is thin and getting thinner.

**Media**: IMAGE — "Man and woman at teacher's desk, classroom, after hours, professional but charged, door partially open"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Keep it professional, hold eye contact" | always | exit | +1 desire |
| "Brush against him when handing papers" | confidence >= 25 | warm | +2 desire, +1 guilt |
| "Close the door. Stand too close." | corruption >= 40 + mark_kiss_unlocked | kiss | +3 desire, +2 guilt, reputation -2 |
| "Lock the door. Tell him you missed him." | corruption >= 60 + mark_groping_unlocked | foreplay | +4 desire, +3 guilt, reputation -3 |

**Caps at foreplay** — this is a school. The principal's office is down the hall. Other teachers walk by. The forbidden driver thrives on the location — every escalation here is exponentially riskier than anywhere else.

### Escalation Nodes

**WARM NODE**: Handing him the report card. Their fingers touch. She doesn't pull away. Turns the paper so they're both reading it — which requires leaning in. Her shoulder against his. She smells his cologne — he put on cologne for a parent-teacher conference. For her.

"His handwriting is improving."

"Your influence, I'm sure."

The double meaning sits between them like a lit match.

**Media**: IMAGE — "Man and woman leaning over paperwork at desk, shoulders touching, classroom, charged moment"

**Exit**: "Pull away first" → +2 desire, +1 guilt | "Let him pull away" → +2 desire, +1 corruption

---

**KISS NODE**: She closes the classroom door. Stands between him and the desk. Too close. She can see his pulse in his neck.

"The fundraiser numbers look good." She puts her hand flat on the desk next to his hip. "Really good."

"Emma—"

"Mark."

Footsteps in the hallway. They both freeze. The footsteps pass. She exhales. He exhales. The shared breath is more intimate than a kiss.

She puts her hand on his chest. Feels his heartbeat hammering. Leans up and kisses the corner of his mouth — barely. Not enough to call it a kiss. Enough to call it everything.

"Same time Thursday?"

He can't speak. He nods.

**Media**: VIDEO — "Woman standing close to man at desk, hand on his chest, almost-kiss, classroom, forbidden, footsteps outside"

**Exit**: "Walk him to the door professionally" → +3 desire, +2 guilt, reputation -2

---

**FOREPLAY NODE**: Door locked. She said it was because of the janitor — "he keeps walking in." Mark doesn't question it. He can't question it. He's beyond questions.

She sits on the edge of her desk. He stands between her legs. His hands on her thighs — familiar now, shaking less. She unbuttons the top of her blouse. One button. His eyes drop. She takes his hand and places it on her collarbone, then lower.

"We have fifteen minutes before the janitor's next round."

Fifteen minutes of his hands under her clothes, his mouth on her neck, her hand on his belt, both of them listening for footsteps. The principal's office is thirty feet away. His son sat in this chair this morning.

Nothing about this should work. Everything about it does.

**Media**: VIDEO — "Couple in classroom, her on desk, his hands on her thighs, door locked, intense forbidden encounter"

**Exit**: "Fix yourselves. Leave separately." → +4 desire, +3 guilt, reputation -3

---

**Hardship**: This happens at her workplace. If `reputation < 40`, the principal starts "checking in" during these meeting times. If `reputation < 30`, the conferences are moved to the principal's presence — ending the private time entirely.

---

# ═══════════════════════════════════════
# JAKE ACTIVITIES (2)
# ═══════════════════════════════════════

---

## JAKE ACTIVITY 1: "Evening at the Bar (Jake Focus)"

- **Pattern**: A (standard escalation)
- **Location**: `loc_bar_floor`
- **Schedule**: 17:00-22:00
- **NPC**: Jake
- **Unlock conditions**: `phase_1_complete`
- **Priority**: 1
- **Is Repeatable**: true
- **Max triggers per day**: 1
- **Availability**: Any day (Jake works 5 nights a week)
- **Weekdays (TOML)**: `[]`
- **Energy Cost**: -15
- **Money Cost**: -5 to -8 (drinks)

---

### Base Scene

**DEFAULT**: Jake's behind the bar. He moves like he owns it — spinning bottles, flipping towels, charming tips out of women twice his age. When she sits down, he slides a drink across the bar without asking. "On me." The smile. The lean. The eye contact that lasts one beat too long. Every move is practiced, polished, weaponized.

She doesn't take the bait. She orders her own drink. Pays for it. Doesn't smile back.

**WITHDRAWN variant** (post-`jake_ego_crisis`): He's working but off his game. Drops a glass. Over-pours a pint. He keeps glancing at her and looking away before she catches him — except she always catches him. The bravado is cracked and what's underneath is confused, hungry, and scared.

**WARM variant** (high `power` toward her, post-`jake_kiss_unlocked`): He doesn't try the moves anymore. When she sits, he pours her drink correctly (neat, not the girly pour he used to give her) and sets it down without bravado. "Hey." Just "hey." The simplicity is more intimate than all his lines combined.

**Media**: IMAGE — "Bartender behind bar, tattoos, confident lean, woman sitting at bar with whiskey, challenge in her eyes"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Flirt and shut him down" | always | exit | +1 power (toward her) |
| "Flirt with another man while Jake watches" | confidence >= 35 | warm | +2 power, +1 corruption |
| "Lean over the bar, give him the view, walk away" | corruption >= 55 + jake_kiss_unlocked | kiss | +3 power |
| "Tell him to meet you in the stockroom" | corruption >= 70 + jake_oral_unlocked | intimate | +4 power, reputation -3 |

**Note**: Jake's `power` stat is inverted — higher numbers toward her mean she's winning. Gains here shift the power dynamic, not increase affection.

### Escalation Nodes

**WARM NODE**: She's at the bar. A man — nobody, a trucker passing through — sits next to her and tries a line. She laughs. Touches the trucker's arm. Whispers something in his ear that makes him grin.

She doesn't look at Jake once. She doesn't need to. Jake's jaw is tight. His pour is heavy. He slams a glass down harder than necessary.

"Problem, Jake?"

"No problem."

"Good."

She pays the trucker's tab and walks out. Jake watches her go.

**Media**: IMAGE — "Woman flirting with man at bar while bartender watches jealously, dive bar, tension"

**Exit**: "Don't look back" → +2 power, +1 corruption | "Glance at Jake at the door" → +1 power, +2 corruption

---

**KISS NODE**: She leans across the bar to grab a napkin. The angle gives him the full view down her neckline. She takes her time. Straightens up. Catches him looking.

"See something you like?"

"You know I do."

"Hmm." She finishes her drink. Sets the glass down. Turns and walks toward the stairs. His eyes follow every step.

She doesn't go upstairs. She goes to the bathroom. Comes back five minutes later and sits down like nothing happened.

The denial is the weapon. She gives and takes away. Gives and takes away. He's Pavlov's dog and she's ringing the bell without feeding him.

**Media**: VIDEO — "Woman leaning across bar, cleavage visible to bartender, her smirk, his frustrated expression"

**Exit**: "Order another drink like nothing happened" → +3 power

---

**INTIMATE NODE**: Bar closing. She catches his eye. Tilts her head toward the stockroom.

He follows. Through the STAFF ONLY door. Beer cases, one bulb, the door that doesn't lock. Jolene is closing out the register thirty feet away.

"On your knees."

He goes down. The cocky bartender kneels on the concrete floor of the stockroom and puts his mouth between her legs while she leans against the beer cases and listens to Jolene counting the drawer through the wall.

She runs her hand through his hair. Controls the pace. When he tries to speed up, she pulls his hair — gently. "Slower."

He slows.

Someone could walk in. The door doesn't lock. That's the point. The danger is part of the dominance — she's not just making him submit, she's making him submit where anyone could see.

**Media**: VIDEO — "Man on knees giving oral to woman in stockroom, beer cases, dim light, risk of discovery, she's in control"

**Exit**: "Enough. Go close the bar." → +4 power, reputation -3

---

**Hardship**: Evening slot competes with Ray. Jake and Ray are both at the bar — pursuing one while the other watches is risky. If she does the Jake focus AND the Ray focus in the same night, `reputation -2` (people notice the teacher working both sides of the bar).

---
---

## JAKE ACTIVITY 2: "Jake Upstairs" (Emma's Room)

- **Pattern**: A (standard escalation)
- **Location**: `loc_bar_emma_room`
- **Schedule**: 22:00-01:00
- **NPC**: Jake
- **Unlock conditions**: `jake_groping_unlocked`
- **Priority**: 6
- **Is Repeatable**: true
- **Max triggers per day**: 1
- **Availability**: Any day
- **Weekdays (TOML)**: `[]`
- **Energy Cost**: -20

---

### Base Scene

**DEFAULT**: After bar hours. She tells him to come upstairs. Not asks — tells. He changes out of his bar shirt. Comes up. Stands in her doorway, trying to find the old swagger. It doesn't fit anymore.

"Where do you want me?"

Not a line. A genuine question. He's asking for instructions. The man who ran every room he walked into is asking a twenty-three-year-old where to stand.

**WITHDRAWN**: He comes up but hovers by the door. The ego is fighting the pull. He's questioning — not her, but himself. "What are we doing?" Not a challenge. Fear.

**WARM**: He comes up and stands where she pointed last time. Already there. Already waiting. "I thought about today." He doesn't need to say what he thought about. They both know.

**Media**: IMAGE — "Man standing in doorway of small bedroom, uncertain expression, woman on bed with composed power, late night"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Talk" | always | exit | +1 power |
| "Tell him where to sit" | power <= 50 + jake_groping_unlocked | foreplay | +2 power, +2 corruption |
| "Put him on his knees" | power <= 35 + jake_oral_unlocked | intimate | +3 power, +2 corruption |
| "Take him to bed. On her terms." | power <= 20 + jake_sex_unlocked | intense | +3 power, +3 corruption, +1 confidence |

### Escalation Nodes

**FOREPLAY NODE**: She points to the bed. "Sit." He sits. She stands between his legs. Takes his hands. Places them — waist, hips, thighs. Each new placement requires her permission.

"Move them."

He moves his hands up.

"Did I say you could?"

She puts them back. He learns. Every session, the rules clarify. He's being trained the way she trained Tom — except Tom's training was gentle. This is not.

**Media**: VIDEO — "Woman standing over seated man, placing his hands on her body, controlling his touch, bedroom, power dynamic"

**Exit**: "Send him home" → +2 power, +2 corruption | "Keep going" → +3 power, +1 corruption

---

**INTIMATE NODE**: "On your knees." Not the stockroom — her bedroom. Private. No audience, no danger of discovery. Just them. He kneels. She sits on the edge of the bed. His mouth between her legs.

She directs everything. Pace, pressure, position. He responds to her voice the way Tom responds to praise — except Jake doesn't want to be told he's good. He wants to be told what to do. Different mechanism. Same result: she's in absolute control.

"Faster."
"Stop."
"Again."

When she finishes, she lets him stay on the floor for a beat. Just a beat. Then: "Come up here."

**Media**: VIDEO — "Man on knees performing oral on woman sitting on bed edge, she directs him, intense, her control"

**Exit**: "Let him lie next to you" → +3 power, +2 corruption | "Tell him to go home" → +2 power, +3 corruption

---

**INTENSE NODE**: She takes him to bed. Her bed. Her terms. She pins his hands above his head with one hand (he could break free — he's stronger — he doesn't). She rides him slowly. When he tries to thrust up, she stops. Waits. "I didn't say you could move."

He lies still. The effort is visible — his jaw clenched, his hands gripping the headboard rail, his body fighting the submission his mind has already accepted.

She controls every second. When to start, when to stop, how fast, how slow. She makes him ask before he's allowed to finish.

"Please."

"Please what?"

"Please let me."

She lets him. And the sound he makes — broken, grateful, destroyed — is the most powerful thing she's ever heard.

Afterward, she lies next to him and thinks: this is what Day 1 Emma would have nightmares about. This woman. This control. This calm cruelty.

She doesn't feel anything resembling guilt.

**Media**: VIDEO — "Woman on top of man, his hands pinned above head, she controls everything, intense, power dynamic reversal"

**Exit**: "Let him stay" → +3 power, +3 corruption | "Send him away" → +2 power, +4 corruption, +2 confidence

---

# ═══════════════════════════════════════
# JOLENE ACTIVITY (1)
# ═══════════════════════════════════════

---

## JOLENE ACTIVITY 1: "Jolene Chats"

- **Pattern**: A (standard — non-sexual, mentor/strategy)
- **Location**: `loc_bar_jolene_space` (primary) or `loc_bar_floor` (alternate)
- **Schedule**: 09:00-15:00
- **NPC**: Jolene
- **Unlock conditions**: `jolene_arrival_complete`
- **Priority**: 1
- **Is Repeatable**: true
- **Max triggers per day**: 1
- **Availability**: Any weekday
- **Weekdays (TOML)**: `[0, 1, 2, 3, 4]`
- **Energy Cost**: -5

---

### Base Scene

**DEFAULT**: Jolene's room or the bar kitchen. Coffee, cigarettes, her silk robe. She's perceptive in a way that catches Emma off-guard — she sees things before they're said. "You look like a woman with a problem. Sit."

She gives strategy tips embedded in conversation. Not game mechanics — actual advice filtered through decades of handling men. She's Emma's mentor, her wingwoman, and occasionally her conscience.

**WITHDRAWN variant** (rare — after a major reputation crisis): Jolene is serious. Not teasing. The cigarette burns long before she ashes it. "We need to talk about what people are saying." She's protective, not judgmental — but she's worried. The town is talking and she lives here too.

**WARM variant** (high corruption, late game): The relationship has shifted. Jolene doesn't lecture anymore — she consults. "What's next on your list?" She's proud. A little scared of what she created, but proud. Two women planning a campaign over coffee.

**Media**: IMAGE — "Two women sitting in kitchen/bedroom, one older in silk robe smoking, one younger with coffee, mentor conversation"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Ask for advice" | always | exit | +1 confidence |
| "Ask about a specific NPC" | any NPC arc started | strategy | +1 confidence, receives gameplay hint |
| "Ask about her past" | corruption >= 20 | personal | +1 confidence, +1 corruption |
| "Ask how to handle a crisis" | any crisis flag active | crisis | +2 confidence, receives recovery strategy |

**Note**: Jolene Chats don't escalate sexually. Jolene's role is mentor, not love interest. The intimacy here is emotional — trust, strategy, the bond between a woman who started the fire and the woman who's now wielding it.

### Strategy Hints (contextual — Jolene gives different advice based on game state)

**If Tom arc active, pre-kiss**: "That boy is clay. Soft clay. Don't mold him too fast or he'll crumble."

**If Ray arc active, pre-crack**: "Ray? Honey, you can't flirt him into noticing you. He's not blind — he's decided. You have to break the decision."

**If Mark arc active, pre-crisis**: "Careful with the married one. The sex is hot but the wife is hotter when she's angry. You do NOT want Karen on a warpath."

**If Jake arc active, pre-submission**: "Jake's ego is load-bearing. You pull it out, you better make sure you want what's underneath."

**If reputation < 50**: "People are talking. You need to show your face at church this Sunday. Bake something for the school. Smile at old ladies. Be boring for a week."

**If `karen_school_confrontation` active**: "Karen came to the school? Jesus. Okay. Here's what you do. Nothing. You do nothing. You be so goddamn professional that she looks crazy for accusing you. Let time do the work."

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION B: UTILITY CANVASES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Survival Activities

| Name | Canvas ID | Location | Schedule | Effects | Unlock Flag | Duration |
|------|-----------|----------|----------|---------|-------------|----------|
| Grocery Shopping | `chore_groceries` | loc_general_store | 12:00-17:00 | -$25, sets food_stocked (5-day timer), energy -10 | game_started | 90 min |
| Sleep (Early) | `utility_sleep_early` | loc_bar_emma_room | 19:00-22:00 | energy = 100, time → next morning | game_started | full night |
| Sleep (Standard) | `utility_sleep_standard` | loc_bar_emma_room | 22:00-01:00 | energy = 80, time → next morning | game_started | full night |
| Rent Payment | `expense_rent` | loc_bar_jolene_space | days_since(rent_last_paid) >= 7 | -$180, sets rent_last_paid | game_started | instant |

**Grocery Shopping narrative**: The general store. Mrs. Hewitt behind the counter, cataloguing Emma's purchases with her eyes. Bread, milk, eggs — normal. Wine — noted. Condoms — Mrs. Hewitt's eyebrow rises imperceptibly. Everything Emma buys in this store is public information by sundown.

Cost: $25. Effect: Sets `food_stocked` flag. Timer: 5 days. If food runs out: `energy_max` drops by 20 each day until restocked.

Risk: Buying wine → no penalty. Buying condoms → `reputation -1` (Mrs. Hewitt talks).

---

**Sleep narratives**:

*Sleep at Night (19:00-22:00)*: Early bed. She's in her room while the bar is still open below — music, laughter, glasses clinking. She pulls the pillow over her head. Full energy restore (100). She dreams about nothing.

*Sleep at Late Night (22:00-01:00)*: Standard. Bar has closed. Jolene's TV through the wall. The building settles. Energy restore to 80.

*Skip Late Night (stayed out)*: Only 60 energy next morning. Shows up to school with dark circles. If two nights in a row: energy capped at 40, `reputation -1` (the principal comments she looks "under the weather").

---

**Rent Payment narrative**: Every seven days. Jolene knocks on her door or catches her in the kitchen. "$180, hon." Said casually, like it's nothing. It's not nothing — it's 82% of her teaching salary.

If missed once: "Don't worry about it, hon. Next week." (Jolene is understanding.)
If missed twice: "We need to talk about money." (Warning.)
If missed three times: "You're working bar shifts until you're caught up." (Locks evening time slots — she works instead of pursuing NPCs.)

---

### Church & Reputation Activities

| Name | Canvas ID | Location | Schedule | Effects | Availability | Duration |
|------|-----------|----------|----------|---------|-------------|----------|
| Church Attendance | `activity_church` | loc_church | Sunday 07:00-09:00 | reputation +3, energy -10 | Every Sunday | 120 min |
| Sunday School Volunteering | `activity_sunday_school` | loc_church | Sunday 09:00-12:00 | reputation +4, energy -15 | Every Sunday | 180 min |
| Neighborly Visits | `activity_neighborly` | loc_town_streets | 15:00-17:00 | reputation +2, energy -10, sometimes gossip intel | 2x/week max | 90 min |
| School Events | `activity_school_events` | loc_school_classroom | Varies (1-2/week) | reputation +2 to +4, energy -15 | Random trigger | 120-180 min |

**Church Attendance narrative**: Sunday morning. She sits in the third pew. The town fills the church — ranchers in pressed shirts, wives in hats, kids fidgeting. The pastor talks about temptation. Emma keeps her face neutral. Mark's family is four rows ahead. Karen's posture says "I know everyone is watching me." Mark stares straight ahead. Emma stares at the back of his neck and thinks about what she did to him three days ago.

Mandatory for reputation. If skipped: `reputation -5` — the new teacher missing church is a five-alarm scandal in Millfield. The town notices. Mrs. Hewitt asks Jolene about it.

---

**Sunday School Volunteering narrative**: After church. She helps with the children's Sunday school session. Cutting paper, reading stories, being the sweet schoolteacher the town hired. It's exhausting — performing innocence when she's anything but.

Emergency reputation repair. Burns the entire Sunday morning. But `reputation +4` is the single biggest rep gain available per activity.

---

**Neighborly Visits narrative**: She visits townspeople. Mrs. Hewitt. The pastor's wife. The old woman who lives across from the school. Cookies, conversation, smiling until her face hurts.

Sometimes she overhears useful intel:
- "Karen's been calling her sister in Tulsa a lot lately." (Mark crisis incoming.)
- "The deputy's been seen at the diner every afternoon." (Tom's patterns exposed.)
- "That handyman's daughter is visiting next weekend." (Ray will be unavailable.)

---

**School Events narrative**: PTA meetings. Bake sales. Parent nights. School play rehearsals. They pop up 1-2 times per week, consuming an evening or late afternoon. Skipping them costs `reputation -3` and increases principal suspicion.

Parent night: Mark is there — with Karen. Emma has to be professional. She has to talk to Karen about her son. She has to shake Karen's hand and smile and not think about what she did with that woman's husband in this classroom.

---

### Money Activities

| Name | Canvas ID | Location | Schedule | Pay | Effects | Availability | Duration |
|------|-----------|----------|----------|-----|---------|-------------|----------|
| Tutoring | `job_tutoring` | loc_library / loc_school_classroom | 12:00-15:00 | $30 | money +30, reputation +1, energy -15 | Mon / Wed | 120 min |
| Bar Shift (Evening) | `job_bar_evening` | loc_bar_floor | 17:00-19:00 | $50 + tips ($10-30) | money +60-80, confidence +1, energy -25 | After Day 8 | 120 min |
| Bar Shift (Night) | `job_bar_night` | loc_bar_floor | 19:00-22:00 | $50 + tips ($10-30) | money +60-80, confidence +1, energy -25 | After Day 8 | 180 min |
| Weekend Cafe Job | `job_cafe_weekend` | loc_diner | 07:00-12:00 | $45 | money +45, energy -20 | Sat OR Sun | 300 min |

**Tutoring narrative**: The library or her classroom. A student at the table — sometimes Mark's son, which adds a private layer of tension. She helps with math, reading, spelling. She's good at this. She became a teacher because she loves teaching. That part of her hasn't changed, even as everything else has.

Safe, boring, reputation-positive. Conflicts with Tom's afternoon coffee (same time slot — money vs. devotion).

---

**Bar Shifts narrative**: Jolene puts her to work. Pull pints, clear tables, run the kitchen orders. The work is physical and humbling and it's the best money she can make outside teaching.

Evening shift: She's working while Ray is at his stool. She serves him beer but can't sit with him. Earning money, losing NPC time.

Night shift: Jake is working too. They're behind the bar together. His arm brushes hers reaching for glasses. Jolene watches with amusement. "Focus on the customers, both of you."

Hidden benefit: `confidence +1` (she gets used to men's attention in a controlled setting). She overhears gossip — useful NPC intel about who's saying what.

---

**Weekend Cafe Job narrative**: Saturday or Sunday morning at the Millfield Diner. Waitressing. Decent tips. Tom comes in for breakfast and turns red when she takes his order. The regulars are kind. The work is honest.

Sunday conflict: cafe job conflicts with church. Choose money ($45) or reputation (+3). Can't do both.

Saturday conflict: cafe job consumes the morning — she can't recover from Friday night's bar activities.

---

### Time Advancement

| Name | Canvas ID | Location | Choices | Duration |
|------|-----------|----------|---------|----------|
| Rest | `utility_rest` | loc_bar_emma_room | "Rest" — eyes closed, mind working | 120 min, +20 energy |
| Nap | `utility_nap` | loc_bar_emma_room | "Nap" — quick sleep | 180 min, +40 energy |

**Rest narrative**: She lies on her bed. Eyes closed. Not sleeping — thinking. Planning. Which man, which time slot, which excuse. The rest restores some energy but the mind doesn't stop.

**Nap narrative**: Quick afternoon sleep. She sets an alarm. Dreams she doesn't remember. Wakes groggy but functional.

---

### UTILITY CANVASES — Economic & School Enforcement

These utility canvases handle recurring game mechanics. They fire automatically based on timer conditions and location.

---

## UTILITY 1: "Payday" (Teaching Salary)

- **Canvas ID**: `utility_payday`
- **Location**: `loc_school_classroom`
- **Schedule**: 12:00-15:00
- **Weekdays (TOML)**: `[4]` (Friday only)
- **Trigger**: `days_since_flag(salary_last_paid) >= 7` OR first week (no flag set yet)
- **Priority**: 8
- **Is Repeatable**: true
- **NPC**: None (solo)

### Scene

Friday afternoon. The school secretary drops an envelope on Emma's desk with a polite smile. "Your paycheck, Miss." $220. It won't go far, but it's hers. She earned it standing in front of twenty-three kids who think she's the nicest teacher they've ever had.

### Effects
- `money +220` (player trait, `clamp = false`)
- Sets flag: `salary_last_paid`

### Exit
Continue with afternoon.

---

## UTILITY 2: "Rent Due" (Weekly Rent Reminder)

- **Canvas ID**: `utility_rent_due`
- **Location**: `loc_bar_emma_room`
- **Schedule**: 07:00-09:00
- **Weekdays (TOML)**: `[]` (any day)
- **Trigger**: `days_since_flag(rent_last_paid) >= 7`
- **Priority**: 9
- **Is Repeatable**: true
- **NPC**: None (but Jolene is referenced in narrative)

### Scene

Morning. A knock on her door. Jolene, cigarette in hand, silk robe, no preamble: "Rent day, sugar." $180. The number hasn't changed but it feels bigger every week.

### Choices

**Choice 1: "Pay rent" ($180)**
- **Requires**: `money >= 180`
- **Effects**: `money -180`, sets flag `rent_last_paid`
- **Narrative**: Emma counts out the bills. Jolene takes them, tucks them in her robe pocket without counting. "Good girl. Breakfast?"

**Choice 2: "Ask for more time"**
- **No money requirement**
- **Effects**:
  - If `rent_missed_once` NOT set: sets `rent_missed_once`. Jolene is understanding: "One time, hon. Don't make it a habit."
  - If `rent_missed_once` IS set: sets `rent_missed_twice`. Jolene's eyes go hard: "You're working the bar this week. Every night until you're square."
  - If `rent_missed_twice` IS set: sets `forced_bar_shifts`. Jolene assigns mandatory evening bar shifts — locks Emma's Evening time slot.
- **Narrative varies by escalation level.**

### Exit
Continue with morning.

---

## UTILITY 3: "Grocery Reminder"

- **Canvas ID**: `utility_grocery_reminder`
- **Location**: `loc_bar_emma_room`
- **Schedule**: 07:00-09:00
- **Weekdays (TOML)**: `[]` (any day)
- **Trigger**: `days_since_flag(groceries_last_bought) >= 5`
- **Priority**: 7
- **Is Repeatable**: true
- **NPC**: None (solo)

### Scene

Morning. The fridge is empty again. A sad carton of milk she's not sure about, a packet of crackers, and optimism. She needs to stop by the General Store today or she's eating bar peanuts for dinner again.

*Note: This is a narrative reminder only. The actual grocery purchase happens via the existing grocery shopping activity at `loc_general_store`.*

### Effects
- No direct effects — serves as a narrative nudge
- Energy max continues to drop (-20/day) until `groceries_last_bought` is refreshed at the General Store

### Exit
Continue with morning.

---

## UTILITY 4: "School Morning Check" (Weekday Attendance)

- **Canvas ID**: `utility_school_morning`
- **Location**: `loc_bar_emma_room`
- **Schedule**: 07:00-09:00
- **Weekdays (TOML)**: `[0, 1, 2, 3, 4]` (weekdays only)
- **Trigger**: No flag condition — fires every weekday morning
- **Priority**: 10 (highest — fires before rent/grocery reminders)
- **Is Repeatable**: true
- **NPC**: None (solo)

### Scene

Morning. Weekday. The alarm on her phone goes off and she can hear the school bus grinding down Main Street. Twenty-three kids are waiting for their teacher.

### Choices

**Choice 1: "Head to school"**
- **Effects**: Advances time by +300 minutes (to 12:00 Afternoon slot), auto-completes teaching
- **Narrative**: She pulls on her cardigan, grabs her bag, and walks the three blocks to school. The kids are loud. The chalk squeaks. It's the most normal thing in her life.

**Choice 2: "Skip school today"**
- **Effects**:
  - `reputation -5` (or `-8` if `school_enforcement_warned` flag is set)
  - Sets flag: `missed_school_today`
  - Stays at current location — free morning slot
- **Narrative**: She turns off the alarm and rolls over. The bus passes without her. She'll tell the principal she was sick. She doesn't feel sick. She feels like she has better things to do.

### Exit
Continue with morning (or afternoon if chose school).

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION C: SOLO ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Solo Activity 1: "Morning Jog"

- **Location**: `loc_town_streets`
- **Schedule**: 05:00-07:00 (Early Morning)
- **Unlock**: Always available
- **Is Repeatable**: true
- **Energy Cost**: -5 (net: energy +10 after boost)

**Narrative**: 5:30am. The town is asleep. She runs down Main Street in shorts and a t-shirt, past dark storefronts and sleeping trucks. The air is clean. For twenty minutes she's not the scheming teacher, not the corrupted innocent, not anyone's manipulation project. She's just a woman running.

Effect: `energy +10` (exercise boost). Time advances 60 min. The only activity that gives energy rather than draining it. Useful for recovering from late nights.

---

### Solo Activity 2: "Read / Study"

- **Location**: `loc_library` or `loc_bar_emma_room`
- **Schedule**: Any free slot
- **Unlock**: Always available
- **Is Repeatable**: true
- **Energy Cost**: -5

**Narrative**: She reads. Lesson plans for school (the job she still cares about), novels borrowed from the library (she's discovering taste — not the Christian fiction her mother sent, but real books), or research (she Googled "how to seduce an older man" once at the library and deleted the browser history three times).

Effect: Time advances 60 min. `+1 confidence` if corruption >= 25 (she's building knowledge). No money cost. Low energy cost. The filler activity for days when she can't afford anything else.

---

### Solo Activity 3: "Dress Up / Appearance"

- **Location**: `loc_bar_emma_room`
- **Schedule**: Any
- **Unlock**: `jolene_shopping_trip`
- **Is Repeatable**: true
- **Energy Cost**: -5

**Narrative**: She stands in front of her closet — which has expanded since Jolene's shopping trip. The dress. The heels. The underwear she bought in the city and hid in the back of the drawer. She tries things on. Studies herself in the mirror. Not the forced mirror scenes — just a woman deciding who she looks like today.

Effect: Time advances 30 min. If wearing "the dress" for a subsequent NPC encounter that day, certain confidence-gated choices unlock at 5 lower threshold. The dress isn't just clothes — it's armor.

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACTIVITY SUMMARY TABLE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### NPC Activities (8 total)

| # | Name | NPC | Location | Schedule | Max Tier | Pattern | Availability |
|---|------|-----|----------|----------|----------|---------|-------------|
| 1 | Coffee With Tom | Tom | Diner | 12:00-15:00 | Foreplay | A | Mon/Wed/Fri |
| 2 | Visit Tom | Tom | Emma's Room | 19:00-01:00 | Sex | A | Any |
| 3 | Evening at the Bar (Ray) | Ray | Bar Floor | 17:00-22:00 | Foreplay | A | Any |
| 4 | The Workshop | Ray | Ray's Shed | 15:00-17:00 | Sex | A | Tue/Thu/Sat |
| 5 | Parent Conferences | Mark | Classroom | 15:00-17:00 | Foreplay | A | Tue/Thu |
| 6 | Evening at the Bar (Jake) | Jake | Bar Floor | 17:00-22:00 | Intimate | A | Any |
| 7 | Jake Upstairs | Jake | Emma's Room | 22:00-01:00 | Sex | A | Any |
| 8 | Jolene Chats | Jolene | Jolene's Space | 09:00-15:00 | N/A (mentor) | A | Weekdays |

### Utility Canvases (10 total)

| # | Name | Canvas ID | Location | Type | Key Effect |
|---|------|-----------|----------|------|-----------|
| 1 | Grocery Shopping | chore_groceries | General Store | Survival | -$25, food_stocked |
| 2 | Sleep (Early) | utility_sleep_early | Emma's Room | Survival | energy = 100 |
| 3 | Sleep (Standard) | utility_sleep_standard | Emma's Room | Survival | energy = 80 |
| 4 | Rent Payment | expense_rent | Jolene's Space | Expense | -$180/week |
| 5 | Church Attendance | activity_church | Church | Reputation | +3 reputation |
| 6 | Sunday School Volunteering | activity_sunday_school | Church | Reputation | +4 reputation |
| 7 | Neighborly Visits | activity_neighborly | Town Streets | Reputation | +2 reputation, intel |
| 8 | School Events | activity_school_events | Classroom | Reputation | +2 to +4 reputation |
| 9 | Rest | utility_rest | Emma's Room | Time | +20 energy |
| 10 | Nap | utility_nap | Emma's Room | Time | +40 energy |

### Money Activities (4 total)

| # | Name | Canvas ID | Location | Pay | Schedule | Conflict |
|---|------|-----------|----------|-----|----------|----------|
| 1 | Tutoring | job_tutoring | Library/Classroom | $30 | Mon/Wed Afternoon | Tom coffee |
| 2 | Bar Shift (Evening) | job_bar_evening | Bar Floor | $60-80 | Evening | Ray/Jake time |
| 3 | Bar Shift (Night) | job_bar_night | Bar Floor | $60-80 | Night | NPC evening time |
| 4 | Weekend Cafe Job | job_cafe_weekend | Diner | $45 | Sat/Sun Morning | Church (Sun), Recovery (Sat) |

### Solo Activities (3 total)

| # | Name | Location | Key Feature |
|---|------|----------|-------------|
| 1 | Morning Jog | Town Streets | Only energy-positive activity |
| 2 | Read / Study | Library/Room | Confidence builder, filler |
| 3 | Dress Up / Appearance | Emma's Room | Lowers confidence thresholds |

---

### Schedule Conflict Map

The core game tension expressed through time:

```
AFTERNOON (12:00-15:00):
  Coffee with Tom (Mon/Wed/Fri)
  vs. Tutoring $30 (Mon/Wed)
  vs. Jolene Chats (any weekday)

LATE AFTERNOON (15:00-17:00):
  Parent Conferences - Mark (Tue/Thu)
  vs. The Workshop - Ray (Tue/Thu/Sat)
  vs. Neighborly Visits (2x/week)

EVENING (17:00-19:00):
  Bar (Ray focus) vs. Bar (Jake focus) vs. Bar Shift ($60-80)

NIGHT (19:00-22:00):
  Visit Tom vs. Bar Shift (Night) vs. School Events

LATE NIGHT (22:00-01:00):
  Jake Upstairs vs. Sleep (energy management)
  vs. Visit Tom (extended)

SUNDAY MORNING:
  Church (reputation +3) vs. Cafe Job ($45)
  Sunday School (reputation +4) if church attended
```

**The Squeeze**: She can never do everything. Every "yes" to one NPC is a "no" to another. Every dollar spent at the bar is a tutoring session she needs. Every late night with Jake is an energy deficit the next morning. The schedule is the game.

**GRAND TOTAL: 25 canvases** (8 NPC + 10 utility + 4 money + 3 solo)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 5 complete. Type "proceed" to continue to Phase 6: Story Arc,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
