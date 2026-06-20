# PHASE 4: STORY EVENTS
# New In Town

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## TOML TRANSLATION NOTES

- **Media blocks**: `Media: IMAGE — "desc"` → TOML `{ type = "image", props = { search_queries = ["desc"] } }`. Same for VIDEO.
- **Stat references**: All NPC stats use **unprefixed names** scoped to their NPC. See Phase 2 for the full mapping table. E.g., "devotion +3 (Tom)" → `{ targetType = "npc", npcId = "npc_tom", trait = "devotion", op = "add", value = 3 }`
- **Exit locations**: Every canvas that moves the player between locations must specify an exit `locationId` via `destinationType = "specific"` in the final exit block.

## DRAMATIC SPINE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Central Tension

**"Can a woman discover who she really is by becoming someone her former self would despise — and is the power she gains worth what she loses?"**

This question threads through every arc:
- **Jolene Phase**: Can exposure to desire break shame — or just replace one cage with another?
- **Tom**: Can she corrupt innocence without guilt, when his innocence mirrors who she used to be?
- **Ray**: Can she earn the respect of a man who dismisses her — and does she want respect or conquest?
- **Mark**: Can she burn down a family for the thrill of being wanted — and does the destruction scare or excite her?
- **Jake**: Can she master a man who masters everyone — and what does she become when no one can resist her?
- **Overall**: Is she liberating herself, or building a prison of manipulation?

### Primary Conflicts

| Arc | Conflict Type | The Threat | First Appears | Peak |
|-----|--------------|-----------|---------------|------|
| Jolene (Phase 1) | INTERNAL | Her shame, her upbringing, her fear of desire | Day 1 (arrival shock) | Day 10 (self-discovery dare) |
| Tom | INTERNAL + MORAL | Guilt over corrupting someone innocent; his growing devotion becomes a leash | Day 14 (first deliberate manipulation) | Day 26 ("Good Boy" — she can't unknow what she likes) |
| Ray | INTERNAL + EXTERNAL | His refusal to see her; the age gap wall; his developing real feelings she didn't plan for | Day 18 (invisible wall frustration) | Day 38 (feelings complication) |
| Mark | EXTERNAL + MORAL | Karen's surveillance; reputation destruction; a child between them | Day 35 (Karen's presence at conferences) | Day 52-55 (Karen finds text / school confrontation) |
| Jake | INTERNAL + POWER | His ego vs. her dominance; the question of whether she's liberated or addicted to control | Day 42 (his second rejection rattles her) | Day 58 (ego crisis — "What the fuck do you want from me?") |
| Reputation | EXTERNAL (ongoing) | The town's gossip network; principal suspicion; church ladies; Mrs. Hewitt at the store | Day 1 (panopticon established) | Day 52-55 (Karen confrontation at school) |

### Tension Curve (Multi-Arc — Simplified)

```
PHASE 1 (Day 1-12)              PHASE 2 (Day 12-65)
Jolene Corruption Arc            Multi-NPC Hunt

    ↗ exposure                   TOM: ↗↗ easy ↗↗↗ GATES → devotion lock
   ↗ curiosity                   RAY: — flat — ↗ CRACK ↗↗↗ GATES → feelings complication
  ↗ shame fading                 MARK: ↗ tension ↗↗ GATES ↘↘ KAREN CRISIS ↗ recovery
 ↗ voyeurism                     JAKE: — rejection — ↘ humiliation ↗↗ FLIP ↗↗↗ SUBMISSION
ARRIVAL
  ↗↗ dare                        REPUTATION: ════════════ slow bleed ═══════ CRISIS ═══ recovery
   ↗↗↗ SELF-DISCOVERY            MIRROR:     Day 1        Day 20        Day 40        Day 60
    ↗↗↗↗ PHASE 2 UNLOCKS
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## OPENING SCENE — "Arrival in Millfield"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Canvas ID**: `opening_arrival`
**Location**: Town Streets → The Dusty Boot → Emma's Room
**Trigger**: None (starting canvas)
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

### NODE 1 — "Main Street"
**Location**: Town Streets

A bus stop on the main road. Two suitcases, a backpack with a Bible her mother packed, and a town that looks like it fell asleep in 1985 and nobody woke it up. Millfield. Population 2,000. One traffic light, one bar, one church steeple pointing at a sky that doesn't care.

She stands on the sidewalk and a pickup truck slows down. The driver tips his hat. A woman sweeping a porch across the street stops sweeping and stares. Three seconds in Millfield, and she's already being watched.

**Media**: IMAGE — "Young woman with two suitcases on a small-town main street, rural America, afternoon sun, pickup trucks, storefronts, feeling small"

**Exit**: "Find the bar" → Node 2

---

### NODE 2 — "The Dusty Boot"
**Location**: Bar Floor

The neon sign is half-dead. THE DU TY B OT. Inside smells like spilled beer and cigarette smoke and something cooking in a back kitchen. It's 2pm and three men sit at the bar. They all look up when the door opens.

Behind the counter: a woman in a tank top, hair piled up, cigarette tucked behind her ear. She looks at Emma — two suitcases, cardigan buttoned to her throat, wide eyes — and grins.

**JOLENE**: "You must be the teacher. Christ, you're younger than I thought. I'm Jolene. I own this disaster." She comes around the bar and takes one of Emma's suitcases without asking. "Room's upstairs. Walls are thin. I'll show you."

She doesn't wait for Emma to answer. She's already walking.

**Media**: IMAGE — "Older woman (42, tank top, confident, cigarette behind ear) behind a dive bar counter, greeting a young woman with suitcases, warm but overwhelming"

**Exit**: "Follow her upstairs" → Node 3

---

### NODE 3 — "The Room"
**Location**: Emma's Room

A single bed. A desk by the window. A bathroom the size of a closet. Through the wall, she can hear the bar below — muffled music, a man laughing.

Jolene leans against the doorframe. "Rent's $180 a week. Kitchen's shared — mine is down the hall. You can use the bar bathroom during the day but don't let the customers catch you in your robe. Church is Sunday, school starts Monday, and the whole town already knows your name because I told them." She grins. "Welcome to Millfield, honey."

She leaves. The door is open. Emma isn't sure if Jolene forgot to close it or just doesn't believe in closed doors.

Emma sits on the bed. Unpacks her Bible. Puts it on the nightstand. Looks at herself in the bathroom mirror.

**MIRROR MOMENT (Day 1)**: Cardigan, long skirt, hair in a ponytail. No makeup. She smiles at herself — nervous but hopeful. "You can do this." She says it out loud, to the mirror, the way she used to pray before tests. The girl in the mirror looks like she's never been touched. She hasn't. Not really.

**Media**: IMAGE — "Young woman looking at herself in a small bathroom mirror, cardigan, ponytail, hopeful nervous smile, simple room"

**Choices**:
- **"Unpack and settle in."** — Careful, organized, her mother's daughter.
  → Sets baseline. The room becomes hers. Energy restored.
- **"Go downstairs and meet the town."** — Brave face, first day energy.
  → +1 confidence (she's trying). Jolene approves: "Atta girl."

**Both set**: `game_started`, `jolene_arrival_complete`, `mirror_day_1`
**Time advance**: → Day 1, Evening (17:00)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 1: JOLENE'S CORRUPTION ARC (Days 1-12)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### JOLENE EVENT 1 — "Culture Shock" (Days 1-2)

**Canvas ID**: `jolene_culture_shock`
**Trigger**: `jolene_arrival_complete`, Day >= 1, 17:00-01:00
**Location**: Bar Floor → Jolene's Space
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_jolene_space`

---

**NODE 1 — The First Evening**

Emma comes downstairs for dinner. Jolene is behind the bar in a silk robe over underwear, pouring shots for two men who don't seem to think this is unusual. She pours Emma a Coke without asking.

"Sit. Eat." A plate of chili appears. "Made it myself. It's spicy. You look like you've never eaten anything spicy."

Jolene moves through the bar like she owns the air in it. She swears casually — "that asshole mayor," "this goddamn jukebox." She touches men's arms when she laughs. She's loud. She's comfortable. She's everything Emma was taught to find distasteful.

Emma eats her chili and tries not to stare.

**NODE 2 — Upstairs**

Later. Jolene walks through the upstairs hallway in just underwear and a tank top, carrying a wine glass. She sees Emma's door open (Emma reading her Bible) and leans in.

"You need anything? Extra blanket? The hot water takes a minute — bang the pipe twice."

She says it casually, standing in the hallway in her underwear, like her body isn't a thing she's supposed to be embarrassed about. Emma can't stop her eyes from dropping for a second. Jolene notices. Doesn't say anything. Just smiles.

"Night, hon."

**Stats**: `corruption +1`
**Sets**: `school_started` (next morning tutorial: school is mandatory)
**Flags set**: `chores_explained` (Jolene explains rent/groceries system during dinner)

---

### JOLENE EVENT 2 — "Thin Walls" (Day 3)

**Canvas ID**: `jolene_thin_walls`
**Trigger**: `jolene_arrival_complete`, Day >= 3, 22:00-01:00
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — Can't Sleep**

11pm. Emma is in bed. Through the thin wall — sounds. Jolene has company. A man's voice, low. Then Jolene's voice, not low at all. Then sounds that don't need translation.

Emma lies rigid under the covers. Her face is burning. She should put in earbuds. She should pray. She should do anything except what she's doing, which is lying perfectly still and listening.

It goes on. Jolene isn't quiet. The man isn't either. The bed frame hits the wall in a rhythm Emma can feel through her pillow.

She listens longer than she should. Much longer.

**Choices**:
- **Put in earbuds and pray.** — The "right" thing. She tries. She can still hear it through the earbuds. She prays harder. It doesn't help.
  → `corruption +1`. She chose to resist but couldn't fully. The seed is planted.
- **Listen. Don't pretend you're not.** — She stops fighting it. Lies there in the dark and listens to every sound until it ends.
  → `corruption +3`. She chose. For the first time, she chose curiosity over shame.

**Both set**: `jolene_thin_walls`

---

### JOLENE EVENT 3 — "Wine and Honesty" (Day 4-5)

**Canvas ID**: `jolene_wine_dinner`
**Trigger**: `jolene_thin_walls`, Day >= 4, 19:00-22:00
**Location**: Jolene's Space
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Invitation**

Jolene invites her for dinner upstairs. "Not the bar food. Real food. Bring yourself." She's made pasta from scratch — better than it has any right to be — and opens a bottle of red wine.

Emma: "Oh, I don't really drink—"

Jolene pours her a glass anyway. "Honey, you're wound tighter than a banjo string. One glass of wine isn't going to kill your Jesus."

**NODE 2 — The Questions**

Two glasses in. Jolene asks with zero preamble: "So when's the last time you had sex?"

Emma chokes on wine. "I — that's — I don't—"

"Because I'm looking at you and I'm seeing a woman who's never been properly fucked. Am I wrong?"

Silence. Emma's face is on fire.

"One boyfriend. David." She can barely say it. "Twice. It was... fine."

Jolene's expression changes. Not mocking — sad. Knowing. She pours more wine.

"Honey. 'Fine' is the saddest word in the English language when it comes to sex. You deserve better than fine. Everyone does."

Jolene talks. About her first husband, her second, the men between. About desire being a natural thing, not a sin. About the difference between being touched and being *wanted*.

Emma listens. Her glass is empty again and she doesn't remember drinking it.

**Stats**: `corruption +1, confidence +1`
**Sets**: `jolene_wine_dinner`

---

### JOLENE EVENT 4 — "The Cracked Door" (Day 6)

**Canvas ID**: `jolene_peek_event`
**Trigger**: `jolene_wine_dinner`, Day >= 6, 15:00-19:00
**Location**: Jolene's Space (door cracked) → Emma's Room
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

**NODE 1 — Coming Home Early**

Emma comes home from school mid-afternoon. The bar is quiet. She goes upstairs. Jolene's door is cracked open — not closed, not wide. Cracked.

Sounds. The same sounds from the thin walls, but now — closer. Visible.

Emma stops in the hallway. She can see through the crack. Jolene is on her bed with a man. They're not under the covers. Jolene is on top. The man's hands are on her hips. Jolene's back arches, her head thrown back, and the sound she makes is nothing like shame.

Jolene opens her eyes. Looks directly at the crack in the door. Sees Emma standing there.

She doesn't stop. She doesn't cover herself. She smiles. Holds Emma's gaze for three seconds — an invitation, a dare, a message — and then closes her eyes again.

**NODE 2 — The Aftermath**

Emma flees to her room. Sits on the bed. Her heart is hammering. Her hands are shaking. She's horrified. She's — something else she doesn't have a word for yet.

She saw. Jolene saw her seeing. And Jolene *smiled*.

At dinner, Jolene acts completely normal. Doesn't mention it. Pours Emma wine without asking. Tells a story about a customer. Normal.

But Emma knows: Jolene left that door cracked on purpose.

**Choices**:
- **Try to forget it.** — Push it down. She's good at pushing things down.
  → `corruption +3`. The attempt to suppress makes it louder in her head.
- **Think about what you saw.** — In bed that night, she replays it. The arch of Jolene's back. The sound. The smile.
  → `corruption +5`. She stopped pretending she didn't want to see.

**Both set**: `jolene_peek_event`

---

### JOLENE EVENT 5 — "Exposure Therapy" (Day 7-8)

**Canvas ID**: `jolene_exposure_therapy`
**Trigger**: `jolene_peek_event`, Day >= 7
**Location**: Shared bathroom → Emma's Room
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

**NODE 1 — The Accidents**

Day 7: Emma goes into the shared bathroom. On the counter — a vibrator. Bright purple, impossible to miss. Not hidden. Just... there. Like a toothbrush.

She stares at it. Touches it accidentally reaching for her toothbrush. Jerks her hand back.

Day 8: Jolene's laptop is open in the shared kitchen. The screen is on. What's on the screen is explicit. Jolene appears behind her: "Oh shit, sorry hon, I was — " She closes it. Not fast. Not embarrassed. "Forgot I left that open."

She didn't forget.

**Stats**: `corruption +2`
**Sets**: `jolene_exposure_therapy`

---

### JOLENE EVENT 6 — "The Shopping Trip" (Day 9)

**Canvas ID**: `jolene_shopping_trip`
**Trigger**: `jolene_exposure_therapy`, Day >= 9, 07:00-15:00
**Location**: Town Streets → Off-site (city)
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

**NODE 1 — The Drive**

Jolene: "Get in the truck. We're going to the city." No explanation. Emma gets in.

90 minutes of highway. Jolene smokes with the window down. Tells stories about her twenties — "I was hotter than sin and dumber than a fence post." Asks Emma about her parents, her college, her faith. Listens without judgment for once.

"You know what your problem is? You were taught that wanting things is the same as being bad. It's not. Wanting is being alive. You've been sleepwalking, honey."

**NODE 2 — The Store**

A clothing store in the city. Not a department store — a boutique. Jolene picks things off racks and holds them against Emma. "No. No. God, no. — This one."

A dress. Black. Short. Shorter than anything Emma has owned. Her arms would be bare. Her legs would be visible above the knee for the first time in public.

"I can't wear that."

Jolene holds it up to the mirror behind Emma. "You can. You've got legs, girl. Fucking use them."

**NODE 3 — The Dress**

Emma tries it on. Looks in the dressing room mirror.

She doesn't look like herself. She looks like someone who might be noticed. Someone who might be wanted. The thought hits her chest like a fist.

**Choices**:
- **"I'll take it."** — She buys into the transformation. Jolene beams.
  → `confidence +3`, `corruption +1`. The dress is the marker. She wears it to dinner that night and every man in the bar looks twice.
- **"It's not me."** — She can't. Not yet. Jolene buys it for her anyway and leaves it hanging on her door.
  → `confidence +1`, `corruption +1`. She tries it on alone that night. Likes what she sees. Isn't ready to admit it.

**Both set**: `jolene_shopping_trip`
**Unlocks**: Appearance-gated choices (wearing the dress changes how NPCs react)

---

### JOLENE EVENT 7 — "Figure It Out" (Day 10)

**Canvas ID**: `jolene_self_discovery`
**Trigger**: `jolene_shopping_trip`, Day >= 10, 22:00-01:00
**Location**: Jolene's Space → Emma's Room
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

**NODE 1 — The Dare**

Late night. Jolene's room. Wine. The conversation has been circling something for an hour. Jolene asks it directly:

"When's the last time you touched yourself?"

Emma is past choking on her wine. She's past blushing. But she still can't answer.

Jolene: "That's what I thought."

She stands up. Puts her wine glass down. Looks at Emma with something that isn't teasing — it's compassion.

"Go to your room. Lock the door. Lie down. Close your eyes. And figure it out."

"I don't — I've never—"

"I know you haven't. That's the whole fucking problem, Emma. You don't know what your body does. You don't know what you like. You don't know the first thing about yourself. And until you do, you're going to keep being the girl who had sex twice and called it 'fine.'"

She puts her hand on Emma's cheek. Gentle. The first time she's touched her with intention.

"You're not broken. You just haven't started yet. Go. Figure it out."

**NODE 2 — The Choice**

Emma's room. Door locked. She's sitting on the bed. Her heart is pounding.

**Choices**:
- **Do it.** — She lies down. Closes her eyes. Thinks about the sounds through the wall. Thinks about the cracked door. Thinks about the way Jolene looked — free, powerful, unapologetic. She figures it out. It takes longer than she expected. And when it happens, her whole body arches and she has to press her face into the pillow to keep quiet. Afterward, she lies in the dark and something in her is different. Something opened.
  → `corruption +5, confidence +3`. The game shifts. She knows her body now. She knows what she wants. The shame isn't gone, but it's losing.
  → Sets `jolene_self_discovery`
- **Can't do it.** — She tries. Can't. The shame is too deep. She lies in the dark and cries — not from sadness, from frustration. She *wants* to want this and can't get past 20 years of being told she shouldn't.
  → `corruption +2, confidence +1`. Slower path. The transformation will come, but later, through NPC interactions instead of self-discovery.
  → Sets `jolene_self_discovery_refused`

**Both choices advance Phase 1**.

---

### JOLENE EVENT 8 — "There She Is" (Day 11-12)

**Canvas ID**: `jolene_phase_1_complete`
**Trigger**: (`jolene_self_discovery` OR `jolene_self_discovery_refused`), Day >= 11
**Location**: Bar Floor → Emma's Room
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

**NODE 1 — The Shift**

Day 11. Emma is at the bar after school. She's wearing the dress. She ordered wine without hesitating. She's sitting at the bar — alone, comfortable, not hiding in a corner booth.

A man at the bar — Ray — leans over to grab a napkin and his arm brushes hers. She doesn't flinch. She looks at his forearm. The muscles. The sun-darkened skin. The hair.

She looks too long. She knows she's looking too long. She doesn't stop.

Across the bar, Jake pours a drink and catches her eye. Winks. She doesn't blush. She holds his gaze for two seconds, then looks away. On her terms.

Tom walks in, off duty, sees her at the bar, and his mouth literally opens. She's wearing the dress. She smiles at him — not her old smile, not polite and nervous. Something else. His ears turn red.

Jolene, watching from behind the counter, drying a glass with a slow grin:

"There she is."

**NODE 2 — The Mirror**

That night. Emma's room. She looks in the bathroom mirror.

She's not the girl who arrived 12 days ago. She can see it. The way she holds herself. The way her eyes aren't looking for permission anymore.

She thinks about three different men and the thought isn't frightening. It's... interesting.

**MIRROR MOMENT (interim)**: Not an official mirror scene (the Day 20 mirror is the formal one), but the Phase 1 close. She's noticing. She's hungry. She doesn't know what to do with it yet — but she's not pretending she doesn't feel it.

**Stats**: `corruption +2`
**Sets**: `phase_1_complete`
**Unlocks**: Phase 2 begins. Tom arc available. Ray arc available (but he won't notice her yet). Emma can begin actively pursuing NPCs. `bar_shifts_available` fires (Jolene offers bar work). `cafe_job_available` fires.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 2: TOM ARC — "The Innocent" (Days 12-31)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### TOM ACT 1 EVENT 1 — "The Excuse" (Day 12-14)

**Canvas ID**: `tom_locks_checked`
**Trigger**: `phase_1_complete`, Day >= 12, 17:00-22:00
**Location**: Deputy Station → Emma's Room
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

**NODE 1 — Jolene's Advice**

Jolene, during a chat: "You want to practice on someone? Start with the deputy. That boy's been drooling since you walked into town."

"What do I even say to him?"

"Tell him you don't feel safe alone at night. That you hear noises. He'll be at your door in thirty seconds. He's a golden retriever in a uniform."

**NODE 2 — The Station**

Emma goes to the deputy station. Tom is at his desk. Coffee mug that says "World's Best Deputy" (he bought it himself). He sees her and stands up so fast he bangs his knee on the desk.

"Miss — uh — Emma — hi. Is everything — can I help you with—"

"I just moved into the room above the bar. I've been hearing noises at night. Would you... check my locks? When you have time?"

His face lights up like she's just asked him to save her from a burning building. "I can — absolutely. Tonight? I could come tonight. If that's — I mean, only if—"

"Tonight would be great."

**NODE 3 — The Visit**

Tom at her door. He's changed out of his uniform into a clean shirt. He smells like he showered. For a lock check.

He inspects every window. Tests the door locks. Shows her how the deadbolt works. He's thorough because he's genuine — he actually wants her to feel safe. And she watches him — his hands, his height, the way he ducks through her doorframe — and thinks: this is going to be easy.

**Choices**:
- **"Thank you, Tom. I feel safer already."** — Warm, genuine. Let him float on it.
  → `devotion +2, confidence +1`. He'll replay "I feel safer already" in his head for days.
- **"Stay for coffee? I don't know anyone here yet."** — Extend the encounter. More time.
  → `devotion +3, confidence +1`. He stays for an hour. Can barely make sentences. Spills his coffee once.

**Both set**: `tom_locks_checked`

---

### TOM ACT 1 EVENT 2 — "Classroom Setup" (Day 15-17)

**Canvas ID**: `tom_classroom_setup`
**Trigger**: `tom_locks_checked`, `devotion >= 10`, Day >= 15, 12:00-17:00
**Location**: Classroom
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Invitation**

She asks Tom to help set up her classroom for a school event. "I need someone tall to hang decorations." She wears the dress. Not the cardigan. The dress.

Tom sees her and his hands forget how to hold things. He drops the banner twice. Can't get the ladder straight. She stands below him handing up decorations and every time she reaches up, the dress lifts and he looks and looks away and looks again.

**NODE 2 — Testing**

She starts experimenting. Stands too close. Touches his arm when she laughs at something he said (it wasn't funny). Bends over in front of him to pick up tape from the floor — slowly.

She watches his reactions like a scientist: the blush that crawls from his neck to his ears, the way his voice goes higher, the way he holds the ladder tighter when her hip grazes his leg.

She's learning. Every reaction is data. Every blush is proof she has power over this man, and the discovery is intoxicating.

**Choices**:
- **"You're so sweet for helping me."** — Keep him hooked with warmth. Pat the golden retriever.
  → `devotion +2, confidence +1`
- **Brush against him reaching for the same decoration.** — Deliberate contact. Test the response.
  → `devotion +3, confidence +2, corruption +1`

**Both set**: `tom_classroom_setup`

---

### TOM GATE 1 — "The Classroom Catch" (kiss_unlocked) (Day 18-20)

**Canvas ID**: `tom_classroom_catch`
**Trigger**: `tom_classroom_setup`, `devotion >= 20`, `confidence >= 10`, Day >= 18, 12:00-17:00
**Location**: Classroom
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Setup**

After school. They're alone in the classroom — she made sure of it. She's rearranging desks. He's helping because he always helps, because she asked, because she smiled.

She's wearing the dress. Heels she bought yesterday.

She "trips" over a desk leg. The trip is perfect — believable enough that he doesn't question it, dramatic enough that he lunges forward.

He catches her. His hands are on her waist. She's pressed against his chest. She can feel his heartbeat through his shirt — fast, panicked, alive.

**NODE 2 — The Freeze**

She looks up at him. He's holding her. She doesn't pull away.

"Tom."

He can't speak. His eyes are wide. His hands are shaking on her waist. He's never been this close to a woman who *wanted* him to be this close. He's frozen — not from fear, but from having no framework for what to do next.

She waits. Lets the silence stretch. Watches him struggle with something he's never felt before.

Then she closes the distance.

**Choices**:
- **Kiss him.** — Soft. Brief. She pulls back and watches his face rearrange itself.
  → `devotion +5, confidence +3, corruption +2`. He touched his lips three times on the drive home. She knows because she watched from the window.
- **Pull away slowly and whisper: "I should go."** — Don't kiss. Make him obsess. The almost-kiss is worse than the kiss for a boy like Tom.
  → `devotion +4, corruption +3`. He won't sleep tonight. He'll replay it. And he'll be back. Hungrier. The kiss comes two days later.

**Both set**: `tom_classroom_catch`, `tom_kiss_unlocked`
**Note**: Both choices unlock the kiss gate. The kiss either happens here or in a follow-up triggered 2 days later. Either way, she's in control.

---

### TOM BRIDGE EVENT — "Tom's Confession" (Day 20-22)

**Canvas ID**: `tom_devotion_confession`
**Trigger**: `tom_kiss_unlocked`, `devotion >= 30`, Day >= 20
**Location**: Diner
**Priority**: 8
**Is Repeatable**: false

---

Non-mechanical character development. No gates unlocked. Exists to deepen Tom as a person.

Coffee at the diner. He's relaxed — the kiss happened, the world didn't end. He tells her about his dad. The old sheriff. The heart attack on duty. How Tom inherited the badge and the town's expectations in the same breath. How he never left Millfield because leaving felt like abandoning his dad's ghost.

"Everyone here thinks I'm brave because I carry a badge. I'm not brave. I just never had anywhere else to go."

She sees it: he's her. He's who she was two weeks ago. Trapped by expectations, defined by other people's image of him, never having seen an alternative.

And she's about to break him out of that cage. The same way Jolene broke her out of hers.

**Stats**: `devotion +2` (he opened up; she listened)
**Sets**: `tom_devotion_confession`

---

### TOM GATE 2 — "Movie Night" (groping_unlocked) (Day 23-25)

**Canvas ID**: `tom_movie_night`
**Trigger**: `tom_kiss_unlocked`, `devotion >= 35`, `corruption >= 20`, Day >= 23, 19:00-01:00
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Invitation**

She invites him to her room. "I got a movie. No one to watch it with." Innocent. Plausible.

He arrives with flowers. Gas station flowers. It's the most heartbreaking thing she's ever seen.

The movie plays. She sits close. Her thigh against his. His entire body is rigid. She puts her head on his shoulder. He stops breathing.

**NODE 2 — The Education**

She takes his hand and puts it on her thigh. He makes a sound — barely audible, strangled.

"Tom. Relax."

He can't relax. She moves his hand higher. He's vibrating. She guides him — higher, under the hem of the dress, onto bare skin.

She puts her hand on his chest and pushes him back against the headboard. Kisses him — harder than the classroom, wetter, her tongue in his mouth. His hands don't know where to go. She takes them and puts them where she wants them.

She pulls back. Looks at him. He's wrecked.

"You're going to learn. And I'm going to teach you."

**Choices**:
- **Guide his hand to her breast.** — Direct. Start the education.
  → `devotion +4, corruption +2, confidence +2`. He touches her like she's made of glass. She'll teach him she isn't.
- **"Touch me where you want to."** — Give him freedom. See what he does.
  → `devotion +5, corruption +1, confidence +1`. His hand stays on her thigh. He's too scared to go further. She covers his hand with hers and moves it. "It's okay."

**Both set**: `tom_movie_night`, `tom_groping_unlocked`

---

### TOM GATE 3 — "Good Boy" (oral_unlocked) (Day 26-28)

**Canvas ID**: `tom_good_boy`
**Trigger**: `tom_groping_unlocked`, `devotion >= 55`, `corruption >= 30`, Day >= 26, 22:00-01:00
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Lesson**

He's in her room. They've been kissing. She pulls back and looks at him. She's made a decision.

"I want to teach you something."

She lies back on the bed. Takes his hand and pushes him downward.

"Go slow."

He doesn't know what he's doing. She tells him. Patient, direct, explicit. "Not there. Lower. Slower. Use your tongue. Like that."

She doesn't fake anything. She corrects him. She guides his head with her hand. And when he gets it right — when something finally clicks and her back arches and she gasps —

"Good boy."

She says it without thinking. And the moment she says it, she sees his eyes change. Not embarrassment. Not shame. Something deeper. He *liked* being told he did well. He liked being directed. He liked being her student.

**NODE 2 — The Realization**

Afterward. He's lying next to her, stunned, happy, devoted. She's staring at the ceiling.

She just taught a man to please her. She told him what to do and he did it. She called him "good boy" and he looked at her like she'd given him communion.

This is power. Not the power of being pretty or being wanted — the power of *directing*. Commanding. Controlling another person's pleasure and self-worth.

She likes it. She likes it more than the physical part.

**Choices**:
- **"You did so well."** — Reinforce the dynamic. He's hers.
  → `devotion +5, corruption +3, confidence +3`. He'll do anything she says now. Anything.
- **"Come here."** — Pull him close. Soften it. She's not a monster yet.
  → `devotion +4, corruption +2, confidence +2`. Warmth and control. The combo is effective.

**Both set**: `tom_good_boy`, `tom_oral_unlocked`

---

### TOM GATE 4 — "First Time" (sex_unlocked) (Day 29-31)

**Canvas ID**: `tom_first_time`
**Trigger**: `tom_oral_unlocked`, `devotion >= 70`, `corruption >= 35`, Day >= 29, 22:00-01:00
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — His First Time**

She decides tonight. Not him. Her.

She texts him: "Come over. Just you."

When he arrives, she's wearing something he's never seen her in. Not the dress. Less. She pulls him inside by the belt.

She's on top. She controls the pace, the position, everything. When he reaches for her hips, she pins his hands above his head.

"Not yet."

She takes his virginity the way she wants to take it — slowly, deliberately, watching his face the entire time. Every reaction is hers. His first time. Her creation.

He doesn't last long. She doesn't care. She laughs — not cruelly, but she *likes* that she did that to him. That she could make a man come apart in seconds just by choosing to.

**NODE 2 — Afterward**

He's lying there, staring at the ceiling, looking like someone rebuilt his entire world.

"I've never... I didn't know it could..."

"I know."

He turns to look at her. Absolute devotion. "I've never felt like this about anyone. I'd do anything for you."

And the thing is — he means it. He's not performing. He's the most honest person she's met in this town. And she's the most dishonest thing that's ever happened to him.

Something flickers in her. Guilt? Recognition? She pushes it down.

**Choices**:
- **"I know you would."** — Accept the devotion. He's an asset now.
  → `devotion +5, corruption +3`. He becomes her tool — covers for her, lies for her, looks the other way when he shouldn't.
  → Sets `tom_asset_activated`
- **"Don't say that."** — She can't hear it. Not yet. She's not ready to face what she's doing.
  → `devotion +4, confidence +2`. A flash of the old Emma. It passes.

**Both set**: `tom_first_time`, `tom_sex_unlocked`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 2: RAY ARC — "The Indifferent Man" (Days 18-42)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### RAY ACT 1 EVENT 1 — "The Invisible Wall" (Day 18-20)

**Canvas ID**: `ray_invisible_wall`
**Trigger**: `phase_1_complete`, `confidence >= 10`, Day >= 18, 17:00-22:00
**Location**: Bar Floor
**Priority**: 8
**Is Repeatable**: false

---

**NODE 1 — The Nothing**

Emma tries the Tom playbook on Ray. Sits near him at the bar. Smiles. Touches his arm when she talks. Laughs at his one-sentence responses.

Nothing. Zero reaction. He calls her "Miss" or "ma'am." Nods politely. Goes back to his beer.

She tries standing close. He doesn't notice — or doesn't register it as intentional. She's wallpaper. Background noise. She could be the barstool next to him.

**NODE 2 — The Frustration**

She goes to Jolene, frustrated.

"He didn't react. At ALL."

Jolene, amused: "Honey, that man isn't blind. He's decided you're a category he doesn't touch. You're 'the schoolteacher.' You're 'a nice kid.' He filed you in a drawer and locked it."

"So what do I do?"

"You break the drawer. You show him something that doesn't fit in the category. Make him see you for the first time."

**Stats**: `confidence -1` (first failure — the sting is useful)
**Sets**: `ray_invisible_wall` (unlocks new approach events)

---

### RAY ACT 1 EVENT 2 — "First Crack" (Day 22-24)

**Canvas ID**: `ray_first_crack`
**Trigger**: `ray_invisible_wall`, `confidence >= 15`, Day >= 22, 12:00-19:00
**Location**: Emma's Room → Bar Floor
**Priority**: 8
**Is Repeatable**: false
**Exit Location**: `loc_bar_floor`

---

**NODE 1 — The Plumbing Excuse**

She engineers it. Tells Jolene the bathroom faucet is leaking. Jolene sends Ray up.

When he knocks, she opens the door in a tank top and shorts. No bra. "Sorry, wasn't expecting you this early."

She expected him exactly when he came.

He walks past her. His eyes stay forward. Professional. He kneels under the sink. She stands behind him, leaning against the doorframe. Watching openly.

He feels it. The weight of being watched. He glances back and catches her looking at — not his face. His shoulders. His arms. The way his shirt stretches when he reaches.

He looks away. Quick. Quicker than a man who felt nothing would need to.

**First crack.**

**NODE 2 — "Not What I Expected"**

That evening at the bar. She doesn't try the sweet-teacher approach. She orders whiskey (badly — it burns, she doesn't wince). She sits at the bar alone. The dress. Hair down.

Ray notices. Not attraction yet — but *surprise*. He looks at her differently. Like she's out of focus and he's trying to readjust.

"Didn't take you for a whiskey girl."

First real sentence. Not "Miss." Not "ma'am." A real sentence directed at a real person.

"I'm full of surprises."

He almost smiles. Almost.

**Stats**: `interest +3, confidence +2`
**Sets**: `ray_first_sentence`, `ray_plumbing_excuse`, `ray_first_crack`

---

### RAY ACT 2 EVENT — "The Truck Conversation" (Day 28-30)

**Canvas ID**: `ray_truck_conversation`
**Trigger**: `ray_first_crack`, `interest >= 15`, `confidence >= 25`, Day >= 28, 17:00-22:00
**Location**: Ray's Truck / Shed
**Priority**: 8
**Is Repeatable**: false

---

**NODE 1 — The Tailgate**

He's fixing the fence behind the bar. She brings two beers. Sits on the tailgate of his truck. He's sweating. She holds out a beer. He takes it.

They sit. First real conversation. He tells her about his daughter. About the divorce — "She got the kid because she had the better lawyer and I had the worse temper." About visiting every other weekend and it never being enough.

She listens. Doesn't try to fix it, doesn't offer platitudes. Just sits and lets him talk. He tells her more in twenty minutes than he's told anyone in Millfield in years.

**NODE 2 — The Touch**

He says something about missing his daughter's birthday last year. His voice catches. Barely — but she hears it.

She touches his forearm. Not a brush, not an accident. She puts her hand on his arm and leaves it there.

He doesn't pull away. He looks at her hand. Then at her. Something changes in his expression — like he's seeing her clearly for the first time. Not the schoolteacher. Not the kid. Her.

"You're not what I expected, Miss."

"Emma."

"...Emma."

The way he says her name — slow, testing it — is worth more than anything Tom ever stammered.

**Stats**: `interest +4, confidence +3`
**Sets**: `ray_truck_conversation`

---

### RAY GATE 1 — "The Shed" (groping_unlocked) (Day 30-32)

**Canvas ID**: `ray_shed_scene`
**Trigger**: `ray_truck_conversation`, `interest >= 30`, `confidence >= 30`, Day >= 30, 15:00-19:00
**Location**: Ray's Truck / Shed
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Lesson**

She asks him to teach her to use tools. "I've never even held a saw." He looks at her like she's asked him to teach a cat to drive — but says okay.

The shed. He sets up a sawhorse and a piece of wood. Puts the saw in her hand. Shows her the angle. She "can't get it right."

He sighs. Steps behind her. His chest against her back. His arms alongside hers. His hands covering her hands on the saw. He guides the motion.

She presses back into him. Subtly. Her back against his chest. Her ass against his hips.

He goes completely still.

She can feel him respond. Hard, against her. His breathing changes. His hands tighten on hers.

Neither of them moves. The saw is forgotten. They stand there, pressed together, the only sound their breathing.

**Choices**:
- **Turn around and look at him.** — Direct confrontation. Force him to acknowledge it.
  → `interest +5, confidence +4, corruption +2`. She turns. Their faces are inches apart. His eyes are dark. His jaw is tight. "This is a bad idea," he says. He doesn't step back.
- **Stay pressed against him and keep "sawing."** — Torture him with plausible deniability.
  → `interest +4, corruption +4, confidence +3`. She resumes the sawing motion. Slowly. He makes a sound in the back of his throat and his hands grip her hips. Neither mentions it after. But he can't unsee her now.

**Both set**: `ray_shed_scene`, `ray_groping_unlocked`
**Note**: Ray's groping gate fires BEFORE the kiss gate — physical precedes emotional. His body admits what his mind won't.

---

### RAY GATE 2 — "The Staircase" (kiss_unlocked) (Day 32-34)

**Canvas ID**: `ray_staircase_kiss`
**Trigger**: `ray_groping_unlocked`, `interest >= 40`, `confidence >= 35`, Day >= 32, 22:00-01:00
**Location**: Bar Floor → Staircase
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

**NODE 1 — Bar Closing**

Friday night. Bar's closing. She's the last customer. He's been watching her all night — she felt it. He's at his stool, she's at a table. Neither has spoken since a brief exchange at 9pm.

Jolene flips chairs. "Get out, both of you. I need to mop."

**NODE 2 — The Staircase**

He walks her to the bottom of the stairs. She stops on the second step. They're eye level.

The hallway is dim. The bar is closed. Jolene is in the back.

He's looking at her and his face is open in a way it never is. No poker face. No "ma'am." Just a man looking at a woman he's been trying not to want for two weeks.

He kisses her. Hard. His hand on the back of her neck, pulling her in. Not tentative like Tom — Ray knows how to kiss. He's been kissing women for twenty years. But this one — she feels it — this one costs him something.

He pulls back. Breathes. "This is a bad idea."

"I know."

"You're the schoolteacher. You're twenty-three. I'm—"

"I know."

He looks at her mouth. Her hand reaches for his belt.

"Goodnight, Ray."

She walks upstairs. Doesn't look back. He stands at the bottom of the stairs for a long time.

**Stats**: `interest +5, confidence +5, corruption +2`
**Sets**: `ray_staircase_kiss`, `ray_kiss_unlocked`

---

### RAY BRIDGE EVENT — "The Daughter" (Day 34-36)

**Canvas ID**: `ray_daughter_story`
**Trigger**: `ray_kiss_unlocked`, `interest >= 45`, Day >= 34
**Location**: Ray's Truck / Shed
**Priority**: 8
**Is Repeatable**: false

---

Non-mechanical. Character depth.

His truck. After work. He's quieter than usual. She asks. He opens his wallet — shows her a photo of a girl, maybe nine, missing a front tooth, grinning.

"She's ten now. That picture's from last year. I keep meaning to take a new one but every time I see her the visit goes so fast."

He tells her about the custody fight. About losing. About driving to the next town every other weekend and pretending two days is enough. About the birthday he missed because his truck broke down and he couldn't afford the repair.

His eyes are wet. He doesn't wipe them. Ray doesn't perform emotions — this is just what's underneath when the wall comes down.

This is when Emma faces a complication she didn't plan for: Ray is becoming a real person to her. Not a conquest. Not a category. A man with a daughter he misses and hands that shake when he talks about her.

She didn't plan for feelings. Hers or his.

**Stats**: `interest +2`
**Sets**: `ray_daughter_story`

---

### RAY GATE 3 — "The Truck" (oral_unlocked) (Day 36-38)

**Canvas ID**: `ray_truck_oral`
**Trigger**: `ray_kiss_unlocked`, `interest >= 55`, `corruption >= 45`, Day >= 36, 22:00-01:00
**Location**: Ray's Truck / Shed
**Priority**: 10
**Is Repeatable**: false

---

Late bar night. She catches him at his truck. He's about to drive home (he shouldn't — he's had three beers, but he always does).

"Wait."

She gets in the passenger side. The cab is dark. The parking lot is empty. The bar lights are off.

She kisses him. Different than the staircase — she initiates this time. She controls it. Her hand on the back of his neck. Her tongue in his mouth.

Then she drops. Down between the seat and the dash. On her knees.

He doesn't expect it. His hands grip the steering wheel. "Jesus, Em—"

She doesn't let him finish the sentence.

In the cab of his truck, in the dark parking lot behind the Dusty Boot, she takes control of a man who is used to being in control. And for the first time with Ray — he lets her lead.

**Stats**: `interest +5, corruption +3, confidence +4`
**Sets**: `ray_truck_oral`, `ray_oral_unlocked`

---

### RAY TENSION EVENT — "Feelings" (Day 38-40)

**Canvas ID**: `ray_feelings_emerge`
**Trigger**: `ray_oral_unlocked`, `interest >= 60`, Day >= 38
**Location**: Bar Floor
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Shift**

Ray is acting different. Showing up at the bar earlier. Ordering less. Looking for her when she walks in. Saving the stool next to him.

He says things he's never said: "I was thinking about you today." "You look nice." These are sentences Ray doesn't say. These are symptoms.

**NODE 2 — The Problem**

Jolene pulls Emma aside.

"That man's falling for you. You know that, right?"

"I—"

"This isn't the deputy. Tom was a puppy. Ray is a grown man and he's developing real feelings. If you're playing him, you need to decide now — because if you break that man, he doesn't come back. He has a kid. He has a whole life that doesn't include getting wrecked by a twenty-three-year-old who's got other men on the side."

**Choices**:
- **"I know what I'm doing."** — Confidence. She's in control. Whatever happens, she chose it.
  → `corruption +3, confidence +2`. The calculation is cold and she knows it.
- **"I didn't plan for this."** — Honest. She didn't. The feelings complication wasn't in the playbook.
  → `corruption +1, confidence -1`. A crack in the armor. She's not as in control as she thought.

**Stats**: `interest -3` (his behavior shift creates temporary distance as he self-regulates)
**Sets**: `ray_feelings_emerge`

---

### RAY GATE 4 — "Upstairs" (sex_unlocked) (Day 38-42)

**Canvas ID**: `ray_upstairs`
**Trigger**: `ray_feelings_emerge`, `interest >= 70`, `corruption >= 50`, Day >= 38, 22:00-01:00
**Location**: Bar Floor → Emma's Room
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

Bar closing. Just them. He's been watching her all night — not the old dismissive watching. Hungry watching. He walks to the staircase. Stops. Looks at her.

"Are you coming up?"

She isn't asking. He follows.

Upstairs. Her room. He pushes her against the door. This isn't Tom — there's nothing tentative. Ray knows what he's doing. His hands, his mouth, the way he lifts her like she weighs nothing.

Sex with Ray is different than Tom. He's experienced. He takes charge. She gasps — actually gasps, unperformative — and for a moment, she's not the one in control.

Afterward, she lies there and realizes: she doesn't like it. Not the sex — the sex was incredible. She doesn't like NOT being in control. She doesn't like gasping. She wants to be the one *making* them gasp.

This is what Ray teaches her. Not by failing — by being too good. By being the man who shows her that competent sex isn't what she wants. She wants power. Pure power. And Ray is too much of an equal for that.

**Stats**: `interest +5, corruption +3, confidence +3`
**Sets**: `ray_upstairs`, `ray_sex_unlocked`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 2: MARK ARC — "The Forbidden" (Days 28-58)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### MARK ACT 1 EVENT 1 — "First Conference" (Day 28-30)

**Canvas ID**: `mark_first_conference`
**Trigger**: `phase_1_complete`, `corruption >= 40`, Day >= 28, 15:00-17:00
**Location**: Classroom
**Priority**: 8
**Is Repeatable**: false

---

**NODE 1 — The Meeting**

Parent-teacher conference. Mark comes alone — Karen has a "headache." He's in pressed slacks and a button-down. Handsome in a suburban way. Good jaw. He shakes her hand and his grip lingers a beat too long.

They discuss his son's grades. Professional. Normal. But she notices: he lingers. Asks questions unrelated to his kid. Laughs at her jokes — they aren't funny. He leans forward when she speaks. He's *starved* for attention from a woman who actually sees him.

She plays it clean. Holds eye contact a beat too long. Smiles. Touches his hand giving him the report card. "Your son is wonderful. He must get it from you."

He thinks about that sentence for three days.

**NODE 2 — The Read**

After he leaves, she sits at her desk and replays the meeting. She saw it. The hunger. The hollowness. A man who does everything right and feels nothing. A marriage that runs on obligation. A man who would burn his life down for someone who made him feel alive.

She can do that. She knows she can, now. Tom taught her she could attract. Ray taught her she could break frames. Mark requires something different: patience, manipulation, and the willingness to light a match in a room full of gasoline.

**Stats**: `desire +2, corruption +1`
**Sets**: `mark_first_conference`

---

### MARK ACT 1 EVENT 2 — "The Volunteer" (Day 32-35)

**Canvas ID**: `mark_fundraiser_volunteer`
**Trigger**: `mark_first_conference`, `desire >= 8`, Day >= 32, 15:00-17:00
**Location**: Classroom
**Priority**: 8
**Is Repeatable**: false

---

Mark volunteers for the school fundraiser. He invents the reason. "Karen usually does this but she's been busy." Karen isn't busy. He's manufacturing proximity.

They work late in the classroom. Counting supplies, making posters. He brings coffee from the diner. Conversation gets personal — his marriage, his job, his sense that he's been sleepwalking through a life someone else designed for him.

She creates emotional intimacy Karen doesn't provide. She asks questions no one asks him. She says: "That must be lonely." And the word "lonely" hits him like a brick because no one — not Karen, not his friends, not his therapist he saw twice and quit — has named it.

**Stats**: `desire +3, guilt +2, confidence +1`
**Sets**: `mark_fundraiser_volunteer`

---

### MARK GATE 1 — "The Rain" (kiss_unlocked) (Day 38-40)

**Canvas ID**: `mark_rain_umbrella`
**Trigger**: `mark_fundraiser_volunteer`, `desire >= 25`, `confidence >= 25`, `corruption >= 40`, Day >= 38, 15:00-19:00
**Location**: Classroom → Town Streets (parking area)
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_bar_emma_room`

---

**NODE 1 — The Walk**

Late fundraiser session. It starts raining — hard, sudden. They're the last ones in the building. He walks her out. One umbrella.

She's pressed against him under the umbrella. The rain is loud. Nobody else is outside. She shivers — exaggerated, deliberate. He puts his arm around her.

They stop walking. He's looking at her. Rain dripping off the umbrella's edge. She looks up at him.

The moment stretches. Five seconds. Ten. His eyes drop to her mouth. His arm tightens.

He almost kisses her. Pulls back. "I should go."

He drives away. She stands in the rain and smiles.

**NODE 2 — The Texts**

That night. Her phone.

**Mark**: "I'm sorry about earlier. I shouldn't have..."
**Emma**: "Shouldn't have what?"
**Mark**: "..."
**Mark**: "I had a really nice time tonight."
**Emma**: "Me too. 😊"

Innocent on the surface. He knows what it means. She knows what it means. The "kiss" happens here — not physically, but the barrier breaks through screens. The thing that can't be unsaid has been typed.

Over the next two days, the texts escalate. She controls the pace.
- "I keep thinking about the rain."
- "What would you have done if you hadn't stopped?"
- "I wish you hadn't stopped."

Each text is calculated. Each response is desperate.

**Stats**: `desire +5, guilt +3, corruption +2`
**Sets**: `mark_rain_umbrella`, `mark_kiss_unlocked`, `mark_texting_escalation`

---

### MARK GATE 2 — "Under the Desk" (groping_unlocked) (Day 42-44)

**Canvas ID**: `mark_under_desk`
**Trigger**: `mark_kiss_unlocked`, `desire >= 40`, `guilt < 35`, Day >= 42, 15:00-17:00
**Location**: Classroom
**Priority**: 10
**Is Repeatable**: false

---

Late afternoon conference. The door is closed — she closed it. "For privacy." Other teachers are in the building. The principal's office is down the hall.

They're sitting at her desk. Side by side, going over fundraiser numbers. Their knees are touching. It's deliberate. They both know it.

She takes his hand under the desk. Puts it on her thigh. He doesn't remove it. His breathing changes. His thumb moves against her skin — slow, exploratory, like he's memorizing the texture of the line he's crossing.

"Mark."

He looks at her. His eyes are dark. His hand moves higher. She lets him.

Footsteps in the hallway. They separate instantly. Professional smiles. The footsteps pass. They look at each other.

"Same time Thursday?"

"Same time Thursday."

**Stats**: `desire +4, guilt +3, corruption +2, reputation -2`
**Sets**: `mark_under_desk`, `mark_groping_unlocked`

---

### MARK BRIDGE EVENT — "The Phone Call" (Day 45-47)

**Canvas ID**: `mark_call_from_bedroom`
**Trigger**: `mark_groping_unlocked`, `desire >= 45`, `corruption >= 50`, Day >= 45
**Location**: Emma's Room (phone)
**Priority**: 8
**Is Repeatable**: false

---

Non-mechanical. Pushes the taboo.

She calls him at 10pm. He picks up on the first ring — whisper-quiet. "Karen's downstairs."

They talk. Soft, charged, dangerous. She asks him what he's thinking about. He tells her. She tells him what SHE's thinking about. His breathing gets ragged.

"Where are you right now?"

"In bed. Karen's watching TV."

"Touch yourself."

Silence. Then: "Emma, I can't—"

"Yes you can. She's downstairs. She won't hear."

She listens to him come apart over the phone while his wife is one floor below. The taboo isn't incidental — it's the engine. The closer Karen is, the hotter it burns.

Afterward: "I have to go. She'll come up to say goodnight."

"Goodnight, Mark."

She hangs up. Looks at the ceiling. No guilt. None. That's new.

**Stats**: `desire +3, guilt +4, corruption +3`
**Sets**: `mark_call_from_bedroom`

---

### MARK GATE 3 — "The First Visit" (oral_unlocked) (Day 47-49)

**Canvas ID**: `mark_first_visit`
**Trigger**: `mark_groping_unlocked`, `desire >= 55`, `corruption >= 50`, `guilt < 40`, Day >= 47, 19:00-01:00
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Door**

9pm. Knock on her door. She opens it. Mark is standing there. His hands are shaking.

"Karen thinks I'm at a meeting."

She pulls him inside.

**NODE 2 — The Room**

She doesn't rush it. Makes coffee. They sit. She lets the tension build — she's learned this from Jolene, from Tom, from Ray. Tension is a tool. You don't release it. You shape it.

They talk. He tells her he hasn't felt this way in years. That touching her thigh in the classroom was the most alive he's felt since his honeymoon. That he lies next to Karen at night and thinks about Emma and hates himself and can't stop.

She listens. Then she stands. Pulls him to the bed. Pushes him down.

She controls the pace. Undressing him slowly. Her mouth on his neck, his chest, his stomach. Lower.

He's desperate. Guilty. Desperate. The guilt makes him harder. She knows this. She's learning guilt the way she learned Tom's devotion — as a tool, a dial, a lever.

**Stats**: `desire +5, guilt +5, corruption +3, confidence +2`
**Sets**: `mark_first_visit`, `mark_oral_unlocked`

---

### MARK GATE 4 — "No Hesitation" (sex_unlocked) (Day 50-52)

**Canvas ID**: `mark_no_hesitation`
**Trigger**: `mark_oral_unlocked`, `desire >= 70`, `corruption >= 55`, Day >= 50, 19:00-01:00
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

He comes back. Three days later. This time — no shaking hands. No preamble. No "Karen thinks I'm at—."

He walks in and he knows what he's here for. She lets him think he's leading. He isn't.

The sex is different than Tom or Ray. Desperate, furtive, charged with the knowledge that a family is ticking like a bomb in the next town. Every sound could be the last if Karen calls and he doesn't answer.

Afterward, he panics. "What did I do. Oh God."

**Choices**:
- **"You did what you wanted."** — Dominance. She owns his guilt. She NAMES his desire.
  → `desire +4, guilt +5, corruption +3`. He looks at her like she's the devil and the only thing he's ever truly wanted. He'll come back tomorrow.
- **"We both wanted this."** — Tenderness. Make him feel safe. Reduce guilt.
  → `desire +3, guilt +2, confidence +2`. He calms down. She holds him. He's easier to manage at lower guilt. But the forbidden thrill softens.

**Both set**: `mark_no_hesitation`, `mark_sex_unlocked`

---

### MARK CRISIS — "Karen" (Day 52-55)

**Canvas ID**: `karen_crisis`
**Trigger**: `mark_sex_unlocked`, `guilt >= 20`, Day >= 52
**Location**: Classroom → Town Streets
**Priority**: 10
**Is Repeatable**: false
**Exit Location**: `loc_school_classroom`

---

**NODE 1 — The Text**

Karen finds a text on Mark's phone. Not explicit — but wrong. Too warm. Too late at night. "Can't wait to see you" at 11:47pm, to a contact saved as "School — Miss E."

Karen shows up at the school. Mid-morning. Emma's teaching. The door opens and a woman she's only seen at church is standing there with murder in her eyes.

"We need to talk. Now."

**NODE 2 — The Confrontation**

Hallway. Other teachers walking past. Karen's voice is controlled — barely. "My husband has been spending a lot of time on this 'fundraiser.' Late nights. Early mornings. Secret phone calls. Would you like to explain what exactly you need from a married man at 11pm?"

Emma plays it perfectly. Calm. Professional. Slightly hurt.

"Mark has been incredibly helpful with the fundraiser. I'm sorry if the schedule has been difficult for your family. I'll make sure to keep our meetings during school hours from now on."

Karen searches her face. Looking for the crack. The guilt. The tell.

She doesn't find it. Because Emma isn't guilty. She's performing. And she's better at it than Karen ever expected.

Karen backs down. "See that you do."

She walks out. Emma watches her go. Her hands are steady. Her heart rate is normal. She just looked a woman in the eyes and lied about sleeping with her husband, and she feels nothing.

**Stats**: `reputation -5 to -8`, `guilt +8`, `desire -3` (he's terrified)
**Sets**: `karen_finds_text`, `karen_school_confrontation`
**Reputation**: Major hit. The school is buzzing. Principal will follow up.

---

### MARK CRISIS REPAIR — "The Parking Lot" (Day 54-57)

**Canvas ID**: `mark_crisis_repair`
**Trigger**: `karen_school_confrontation`, `days_since_flag(karen_school_confrontation) >= 2`, Day >= 54, 22:00-01:00
**Location**: School Parking Lot
**Priority**: 10
**Exit Location**: `loc_school_parking_lot`

---

**NODE 1 — The Fallout**

Two days of silence. Mark doesn't come to conferences. Doesn't text. His son still comes to school — Karen brings him now. Sits in the car. Watches the building.

Then, Day 54 or later. 11pm. A text: "Parking lot. Please."

She finds him in his car. Engine off. Third row, visitor side. He looks wrecked. Three days of guilt, Karen's interrogation, sleepless nights.

"She knows. She doesn't have proof, but she knows."

"What did you tell her?"

"That it's about the fundraiser. That I'm being a good parent. She looked at me like she didn't recognize me." His voice breaks. "She's right. I don't recognize me."

**NODE 2 — The Choice**

**Choices**:
- **"Then stop. Go home. Be the man she thinks you are."** — Give him an exit. Release the guilt.
  → `guilt -10, desire -5`. He takes the exit. But he comes crawling back in 3-4 days because the hunger doesn't stop. The affair survives on lower heat.
  → Sets `karen_backed_down`
- **"She doesn't know who you are. I do."** — Pull him deeper. Name the truth Karen can't face.
  → `guilt +2, desire +5, corruption +3`. He stares at her. Then he kisses her in the parking lot of his son's school and she tastes tears on his face. The affair intensifies.
  → Sets `karen_still_watching`

**Both set**: `mark_crisis_repair_complete`
**Mark guilt management**: If guilt > 40 at this point, `mark_guilt_spiral` fires and he stops contacting her for 5+ days. She must wait or manage guilt through the repeatable conference activity (keeping it professional to reduce guilt).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PHASE 2: JAKE ARC — "The Endgame" (Days 40-65)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### JAKE ACT 1 EVENT 1 — "The Second Rejection" (Day 40-42)

**Canvas ID**: `jake_second_attempt`
**Trigger**: `phase_1_complete`, `corruption >= 55`, Day >= 40, 17:00-22:00
**Location**: Bar Floor
**Priority**: 8
**Is Repeatable**: false

---

**NODE 1 — The Try**

Jake has noticed the new Emma. The dress. The whiskey. The way she talks to men now. He leans over the bar.

"So, you finally loosened up. Changed your mind about that drink?"

He's using his standard move. The lazy smile. The lean. The eye contact that works on tourist girls and bored wives.

**NODE 2 — The Laugh**

She laughs. Not a blush, not a polite decline. She *laughs*. At him.

"That's your move? Really? You use that on every woman who walks in here."

His grin falters. Nobody laughs at Jake. Nobody. Women blush or play along or tell him to fuck off — they don't *laugh like it's funny that he tried*.

"I just thought—"

"I know what you thought." She picks up her drink. Takes a sip. Holds his eyes over the rim. "You thought wrong."

She turns back to her conversation with Ray, who saw the whole thing and is trying not to smile.

Jake stands behind the bar, holding a glass he forgot to dry, and for the first time in his adult life, processes rejection that doesn't sting — it *confuses*.

**Stats**: `power -5` (shifted toward her), `confidence +3, corruption +1`
**Sets**: `jake_second_attempt`

---

### JAKE ACT 1 EVENT 2 — "The Jealousy Game" (Day 44-48)

**Canvas ID**: `jake_jealousy_game`
**Trigger**: `jake_second_attempt`, `confidence >= 40`, Day >= 44, 17:00-22:00
**Location**: Bar Floor
**Priority**: 8
**Is Repeatable**: false

---

She starts a campaign. Not against Jake — around him.

She flirts with other men at the bar. Touches their arms. Whispers close to their ears. Laughs in a way that carries. She does this while sitting in Jake's line of sight. She glances at him — once, twice — to make sure he sees.

Goal isn't jealousy — it's reframing. She's showing him that she's the one being chosen, not the one chasing. Every man in the bar is responding to her except him — and she doesn't care. That's the message. You're not special. You're not the prize. I am.

Jake watches. His jaw tightens. His pour gets sloppier. He makes mistakes — wrong drink, wrong tab. Jolene notices: "Something on your mind?"

"No."

"Uh-huh."

**Stats**: `power -5`, `corruption +2`
**Sets**: `jake_jealousy_game`

---

### JAKE ACT 2 EVENT — "Pour Me One More" (Day 48-52)

**Canvas ID**: `jake_bar_sitting`
**Trigger**: `jake_jealousy_game`, `power <= 75`, `corruption >= 60`, Day >= 48, 22:00-01:00
**Location**: Bar Floor
**Priority**: 10
**Is Repeatable**: false

---

**NODE 1 — The Bar**

Bar closing. She's the last one. Chairs flipped, lights low. She sits on the actual bar — up on the surface, legs crossed.

"Pour me one more."

He pours. She takes the glass. Holds eye contact. Drinks slowly. The bar is silent except for the clock and his breathing.

"You want me so badly it's almost sweet."

His expression — genuine surprise. Then anger. Then something else. He reaches for her. She puts one finger on his lips.

"Not yet."

She slides off the bar. Walks to the stairs. Doesn't look back. She can feel his eyes boring into her. She counts his steps — he takes three toward the stairs, then stops.

He stands in the empty bar and she can hear him say, to nobody: "What the *fuck*."

**Stats**: `power -10`, `confidence +4, corruption +3`
**Sets**: `jake_bar_sitting`

---

### JAKE BRIDGE EVENT — "The Ego Crisis" (Day 52-54)

**Canvas ID**: `jake_ego_crisis`
**Trigger**: `jake_bar_sitting`, `power <= 65`, Day >= 52
**Location**: Bar Floor
**Priority**: 8
**Is Repeatable**: false

---

Non-mechanical. Character depth.

Jake is acting different. Showing up sober. Cleaning up better. He's stopped flirting with other women at the bar — not because he doesn't want to, but because he wants to show her he's not what she thinks he is.

He's never done this for anyone. He doesn't know what it means and it's scaring him.

He corners her by the jukebox.

"What the fuck do you want from me?"

It's not a line. It's genuine confusion. His ego — the thing he's built his entire identity on — is cracking. He's spent his life being the one who pursues, the one who chooses, the one in control. She's inverted everything and he doesn't have a framework for existing as the one who *wants without getting*.

"I want you to figure that out."

She walks away. He punches the jukebox (it skips two songs) and goes out the back door.

**Stats**: `power -5`
**Sets**: `jake_ego_crisis`

---

### JAKE GATE 1 — "Not Yet" (kiss_unlocked) (Day 52-54)

**Canvas ID**: `jake_not_yet`
**Trigger**: `jake_ego_crisis`, `power <= 65`, `confidence >= 55`, Day >= 52, 22:00-01:00
**Location**: Bar Floor
**Priority**: 10
**Is Repeatable**: false

---

Bar closing. Again. This time when he looks at her, there's no bravado.

"One kiss. Please."

That word — *please* — is something Jake has never said to a woman in his life.

She looks at him. Considers.

She steps forward. Puts her hand on the back of his neck. Pulls him in. ONE kiss — brief, her terms, her hand controlling the angle. She pulls away first.

"Good."

She walks upstairs. He stands there, touching his lips like they're someone else's.

**Stats**: `power -5, confidence +3, corruption +2`
**Sets**: `jake_not_yet`, `jake_kiss_unlocked`

---

### JAKE GATE 2 — "Permission" (groping_unlocked) (Day 54-56)

**Canvas ID**: `jake_permission`
**Trigger**: `jake_kiss_unlocked`, `power <= 50`, `corruption >= 60`, Day >= 54, 22:00-01:00
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

She lets him come upstairs. First time in her room.

"You can touch me. But only where I say."

He reaches for her waist. She takes his hands and moves them to her hips. He moves them up. She stops. Puts them back.

"Did I say you could move them?"

Something shifts in his eyes. Not anger. Recognition. He's discovering something about himself he didn't know existed — he *likes* being told what to do. The cocky bartender who runs the bar, runs the room, runs every interaction — he likes surrendering.

She places his hands where she wants them. Her waist. Her thighs. Her ass. Each time he moves without permission, she stops. He learns fast.

"Good. You're learning."

**Stats**: `power -10, corruption +3, confidence +3`
**Sets**: `jake_permission`, `jake_groping_unlocked`

---

### JAKE GATE 3 — "The Stockroom" (oral_unlocked) (Day 58-60)

**Canvas ID**: `jake_stockroom`
**Trigger**: `jake_groping_unlocked`, `power <= 35`, `corruption >= 70`, Day >= 58, 22:00-01:00
**Location**: Bar Stockroom
**Priority**: 10
**Is Repeatable**: false

---

Bar closing. Jolene's in the front. Customers just left. The stockroom door is right there.

She takes his hand. Leads him through the "STAFF ONLY" door. Cases of beer. One overhead bulb. The door doesn't lock.

"Someone could walk in." His voice is hoarse.

"Then you'd better be quick."

She puts him on his knees. In the stockroom. Twenty feet from Jolene. Behind a door that doesn't lock.

He goes down on her against the stack of beer cases. His hands on her thighs. Her hand in his hair. She controls everything — pace, duration, how far. She looks at the door while he worships her and thinks: three months ago she cried after missionary sex with the lights off.

**Stats**: `power -10, corruption +4, confidence +5`
**Sets**: `jake_stockroom`, `jake_oral_unlocked`
**Risk**: `reputation -3` (Jolene might hear; small chance a customer returns for their jacket)

---

### JAKE GATE 4 — "On Her Terms" (sex_unlocked) (Day 60-63)

**Canvas ID**: `jake_on_her_terms`
**Trigger**: `jake_oral_unlocked`, `power <= 20`, `corruption >= 75`, Day >= 60, 22:00-01:00
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

Her room. Her terms. She tells him when to arrive, what to wear, where to stand.

He complies. The cocky bartender follows instructions from a twenty-three-year-old schoolteacher.

She's on top. She pins his hands above his head. "Did I say you could touch?"

He doesn't fight it. He arches into it. He discovers — and she sees the moment of discovery in his face — that he LIKES not being in charge. That the ego was armor, not identity. That underneath the bravado is a man who has been waiting his entire life for someone to tell him what to do.

She pushes further. Controls everything. Makes him wait. Makes him ask.

"Please."

There it is again. Please. The most powerful word in the game when it comes from someone who's never said it before.

**Stats**: `power -10, corruption +5, confidence +5`
**Sets**: `jake_on_her_terms`, `jake_sex_unlocked`

---

### JAKE ENDGAME — "The Surrender" (Day 63-65)

**Canvas ID**: `jake_endgame_choice`
**Trigger**: `jake_sex_unlocked`, `power <= 10`, Day >= 63
**Location**: Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

Jake comes to her room. Not for sex — to talk. He sits on the edge of the bed and looks at his hands.

"What do you want me to do?"

Not in bed. In life. He's asking her to tell him what to be. The ego is gone. The cocky bartender who flirted with every woman in Millfield is sitting on a schoolteacher's bed asking for direction.

She built this. She broke him down and rebuilt him.

**Choices**:
- **"Stay."** — Keep him. He's hers completely. The submissive bartender who does what she says.
  → `power = 0`. `jake_surrender`. He's a permanent asset. She owns the bar dynamic now.
- **"I don't need you to do anything. That was the point."** — Break it off. Walk away. The power was the point, not the person.
  → `corruption +5, confidence +5`. `jake_endgame_walked_away`. The cruelest and most honest ending. She never needed him — she needed to prove she COULD.

**Both set**: `jake_endgame_choice`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## MIRROR SCENES (Day 20, Day 40, Day 60)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### MIRROR — Day 20

**Canvas ID**: `mirror_day_20`
**Trigger**: Day >= 20, Morning (any)
**Location**: Emma's Room

She stands in front of the mirror. The dress. Makeup she didn't own two weeks ago. Her hair is down. She tilts her head. Studies herself.

Something is different. Not the clothes — the eyes. They're not looking for permission anymore. They're measuring. Calculating.

She thinks about Tom. About how he looked at her in the classroom. About the sound he made when she kissed him. About the word "power" and how it doesn't feel abstract anymore.

The Bible is still on the nightstand. She hasn't opened it in a week.

**Sets**: `mirror_day_20`

---

### MIRROR — Day 40

**Canvas ID**: `mirror_day_40`
**Trigger**: Day >= 40, Morning (any)
**Location**: Emma's Room

She stands in front of the mirror in her underwear. No flinch. No arms crossed. She looks at her body the way she's learned men look at it — appraising, wanting, clinical.

She likes what she sees. Not vanity. Inventory. These legs made Ray forget she was "the schoolteacher." These lips said "good boy" to Tom and watched him melt. This body is a weapon she didn't know she carried.

She thinks about three different men and feels nothing resembling guilt. She thinks about Karen and feels — what? Not guilt. Not pity. Something like amusement. She thinks about Jake and feels hunger.

The Bible is in the nightstand drawer. She put it there last week. Face down.

**Sets**: `mirror_day_40`

---

### MIRROR — Day 60

**Canvas ID**: `mirror_day_60`
**Trigger**: Day >= 60, Morning (any)
**Location**: Emma's Room

She barely recognizes herself.

Not the clothes — those she chose. Not the body — that she learned. The eyes. The way she holds herself. The way her smile has changed from warm to something sharper. Something that calculates before it cares.

The girl who arrived with a cardigan and a Bible and said "gosh" unironically would be horrified. Would cry. Would pray.

Emma looks at that ghost in the mirror and smiles.

The smile isn't kind.

The Bible is gone. She threw it away three weeks ago. She doesn't remember which day.

**Sets**: `mirror_day_60`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## CROSS-NPC EVENTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### "Friday Night Collision"

**Canvas ID**: `friday_collision`
**Trigger**: Day is Friday, 19:00-22:00, `tom_kiss_unlocked` AND `interest >= 20`
**Location**: Bar Floor
**Priority**: 8
**Is Repeatable**: false

Friday night. The bar is full. Tom is here (off duty, out of uniform, uncomfortable). Ray is at his stool. Jake is behind the counter. Mark... is here. Without Karen. Catches her eye across the room.

Four men. One room. All of them aware of her. None of them aware of each other — yet.

She has to choose who to focus on.

**Choices**:
- **Sit with Tom** → `devotion +2, reputation +1` (public, safe, wholesome-looking)
- **Join Ray at the bar** → `interest +2, reputation -1` (older man, drinking, people notice)
- **Flirt with Jake across the counter** → `power -2, reputation -1` (the bartender? really?)
- **Catch Mark's eye and nod toward the door** → `desire +3, reputation -2, guilt +2` (the married man left the building with the teacher)

**Sets**: `friday_collision`

---

### "Tom Sees Ray"

**Canvas ID**: `tom_saw_ray`
**Trigger**: `tom_kiss_unlocked` AND `ray_kiss_unlocked`, Day >= 35, 17:00-22:00
**Location**: Bar Floor
**Priority**: 8
**Is Repeatable**: false

Tom comes to the bar (unusual — he came to see her). Sees her talking to Ray. The body language. The way she touches Ray's arm. The way Ray looks at her — not the dismissive way from before.

Tom's face changes. He sits in a corner booth. Orders a beer he doesn't drink. Watches.

When she comes over to say hi, he's different. Quieter. His "I'm fine" is too quick.

Later, a text: "Are you and that handyman... is something happening?"

**Choices**:
- **"Ray is just a friend."** — Lie. Protect both relationships.
  → `devotion -2` (he doesn't fully believe it), but the relationship survives.
- **"Tom. Look at me. You are the one I think about."** — Redirect. Give him what he needs.
  → `devotion +2, corruption +2`. She's managing him. He believes it because he needs to.
- **"It's complicated."** — Honest-ish. He's hurt but respects her honesty.
  → `devotion -3, reputation -2`. If `devotion >= 60`, he agrees to look the other way: `tom_covers_for_emma`.

**Sets**: `tom_saw_ray`

---

### "Ray Sees the Text"

**Canvas ID**: `ray_sees_mark_text`
**Trigger**: `ray_kiss_unlocked` AND `mark_kiss_unlocked`, Day >= 45, 17:00-22:00
**Location**: Bar Floor
**Priority**: 8
**Is Repeatable**: false

At the bar. Her phone buzzes. She glances at it — a text from Mark. Something charged. She puts the phone down. Ray, sitting next to her, saw the screen. He doesn't say anything.

Five minutes of silence.

"Who's Mark?"

"Nobody."

"Didn't look like nobody."

She redirects. Changes the subject. Touches his arm. He lets it go — but the seed is planted.

**Stats**: `interest -2`
**Sets**: `ray_sees_mark_text`

---

### "Juggling Detected"

**Canvas ID**: `juggling_detected`
**Trigger**: (`tom_saw_ray` AND `ray_sees_mark_text`) OR `friday_collision`, Day >= 45
**Location**: Any
**Priority**: 6
**Is Repeatable**: false

The town is small. Patterns are noticed. The schoolteacher has coffee with the deputy, drinks with the handyman, and the insurance agent's car has been near the bar after hours.

Mrs. Hewitt at the general store: "You've certainly made a lot of friends in town, haven't you, dear?"

The tone says everything the words don't.

**Stats**: `reputation -3`
**Sets**: `juggling_detected`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## FLAG CHAIN DIAGRAMS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Phase 1 (Jolene Corruption)

```
game_started → jolene_arrival_complete → mirror_day_1
  → jolene_thin_walls
    → jolene_wine_dinner
      → jolene_peek_event
        → jolene_exposure_therapy
          → jolene_shopping_trip
            → jolene_self_discovery (OR jolene_self_discovery_refused)
              → phase_1_complete
                → bar_shifts_available
                → cafe_job_available
```

### Tom Arc

```
phase_1_complete → tom_locks_checked
  → tom_classroom_setup
    → tom_classroom_catch → tom_kiss_unlocked (GATE 1)
      → [BRIDGE] tom_devotion_confession
        → tom_movie_night → tom_groping_unlocked (GATE 2)
          → tom_good_boy → tom_oral_unlocked (GATE 3)
            → tom_first_time → tom_sex_unlocked (GATE 4)
              → tom_asset_activated (optional)
```

### Ray Arc

```
phase_1_complete → ray_invisible_wall
  → ray_first_crack (ray_first_sentence + ray_plumbing_excuse)
    → ray_truck_conversation
      → ray_shed_scene → ray_groping_unlocked (GATE 1 — physical first)
        → ray_staircase_kiss → ray_kiss_unlocked (GATE 2)
          → [BRIDGE] ray_daughter_story
            → ray_truck_oral → ray_oral_unlocked (GATE 3)
              → [TENSION] ray_feelings_emerge
                → ray_upstairs → ray_sex_unlocked (GATE 4)
```

### Mark Arc

```
phase_1_complete (+ corruption >= 40) → mark_first_conference
  → mark_fundraiser_volunteer
    → mark_rain_umbrella → mark_kiss_unlocked (GATE 1) + mark_texting_escalation
      → mark_under_desk → mark_groping_unlocked (GATE 2)
        → [BRIDGE] mark_call_from_bedroom
          → mark_first_visit → mark_oral_unlocked (GATE 3)
            → mark_no_hesitation → mark_sex_unlocked (GATE 4)
              → [CRISIS] karen_finds_text → karen_school_confrontation
                → mark_crisis_repair_complete
                  → (karen_backed_down OR karen_still_watching)
```

### Jake Arc

```
phase_1_complete (+ corruption >= 55) → jake_second_attempt
  → jake_jealousy_game
    → jake_bar_sitting
      → [BRIDGE] jake_ego_crisis
        → jake_not_yet → jake_kiss_unlocked (GATE 1)
          → jake_permission → jake_groping_unlocked (GATE 2)
            → jake_stockroom → jake_oral_unlocked (GATE 3)
              → jake_on_her_terms → jake_sex_unlocked (GATE 4)
                → jake_endgame_choice (jake_surrender OR jake_endgame_walked_away)
```

### Cross-NPC

```
tom_kiss_unlocked + interest >= 20 → friday_collision
tom_kiss_unlocked + ray_kiss_unlocked → tom_saw_ray → (tom_covers_for_emma?)
ray_kiss_unlocked + mark_kiss_unlocked → ray_sees_mark_text
(tom_saw_ray + ray_sees_mark_text) OR friday_collision → juggling_detected
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GATE TIMELINE SUMMARY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| NPC | Gate | Set By Event | Key Requirements | ~Day |
|-----|------|-------------|-----------------|------|
| **Tom** | kiss_unlocked | "The Classroom Catch" | `devotion >= 20, confidence >= 10` | ~18-20 |
| **Tom** | groping_unlocked | "Movie Night" | `devotion >= 35, corruption >= 20` | ~23-25 |
| **Tom** | oral_unlocked | "Good Boy" | `devotion >= 55, corruption >= 30` | ~26-28 |
| **Tom** | sex_unlocked | "First Time" | `devotion >= 70, corruption >= 35` | ~29-31 |
| **Ray** | groping_unlocked | "The Shed" | `interest >= 30, confidence >= 30` | ~30-32 |
| **Ray** | kiss_unlocked | "The Staircase" | `interest >= 40, confidence >= 35` | ~32-34 |
| **Ray** | oral_unlocked | "The Truck" | `interest >= 55, corruption >= 45` | ~36-38 |
| **Ray** | sex_unlocked | "Upstairs" | `interest >= 70, corruption >= 50` | ~38-42 |
| **Mark** | kiss_unlocked | "The Rain" | `desire >= 25, confidence >= 25, corruption >= 40` | ~38-40 |
| **Mark** | groping_unlocked | "Under the Desk" | `desire >= 40, guilt < 35` | ~42-44 |
| **Mark** | oral_unlocked | "The First Visit" | `desire >= 55, corruption >= 50, guilt < 40` | ~47-49 |
| **Mark** | sex_unlocked | "No Hesitation" | `desire >= 70, corruption >= 55` | ~50-52 |
| **Jake** | kiss_unlocked | "Not Yet" | `power <= 65, confidence >= 55` | ~52-54 |
| **Jake** | groping_unlocked | "Permission" | `power <= 50, corruption >= 60` | ~54-56 |
| **Jake** | oral_unlocked | "The Stockroom" | `power <= 35, corruption >= 70` | ~58-60 |
| **Jake** | sex_unlocked | "On Her Terms" | `power <= 20, corruption >= 75` | ~60-63 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## COMPLETE EVENT INVENTORY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| # | Canvas ID | NPC/Type | Event Name | Day Range | Sets Gate? |
|---|-----------|----------|------------|-----------|------------|
| 1 | `opening_arrival` | Opening | Arrival in Millfield | Day 1 | — |
| 2 | `jolene_culture_shock` | Jolene | Culture Shock | Day 1-2 | — |
| 3 | `jolene_thin_walls` | Jolene | Thin Walls | Day 3 | — |
| 4 | `jolene_wine_dinner` | Jolene | Wine and Honesty | Day 4-5 | — |
| 5 | `jolene_peek_event` | Jolene | The Cracked Door | Day 6 | — |
| 6 | `jolene_exposure_therapy` | Jolene | Exposure Therapy | Day 7-8 | — |
| 7 | `jolene_shopping_trip` | Jolene | The Shopping Trip | Day 9 | — |
| 8 | `jolene_self_discovery` | Jolene | Figure It Out | Day 10 | — |
| 9 | `jolene_phase_1_complete` | Jolene | There She Is | Day 11-12 | phase_1_complete |
| 10 | `tom_locks_checked` | Tom Act 1 | The Excuse | Day 12-14 | — |
| 11 | `tom_classroom_setup` | Tom Act 1 | Classroom Setup | Day 15-17 | — |
| 12 | `tom_classroom_catch` | Tom Gate | The Classroom Catch | Day 18-20 | kiss_unlocked_tom |
| 13 | `tom_devotion_confession` | Tom Bridge | Tom's Confession | Day 20-22 | — |
| 14 | `tom_movie_night` | Tom Gate | Movie Night | Day 23-25 | groping_unlocked_tom |
| 15 | `tom_good_boy` | Tom Gate | Good Boy | Day 26-28 | oral_unlocked_tom |
| 16 | `tom_first_time` | Tom Gate | First Time | Day 29-31 | sex_unlocked_tom |
| 17 | `ray_invisible_wall` | Ray Act 1 | The Invisible Wall | Day 18-20 | — |
| 18 | `ray_first_crack` | Ray Act 1 | First Crack | Day 22-24 | — |
| 19 | `ray_truck_conversation` | Ray Act 2 | The Truck Conversation | Day 28-30 | — |
| 20 | `ray_shed_scene` | Ray Gate | The Shed | Day 30-32 | groping_unlocked_ray |
| 21 | `ray_staircase_kiss` | Ray Gate | The Staircase | Day 32-34 | kiss_unlocked_ray |
| 22 | `ray_daughter_story` | Ray Bridge | The Daughter | Day 34-36 | — |
| 23 | `ray_truck_oral` | Ray Gate | The Truck | Day 36-38 | oral_unlocked_ray |
| 24 | `ray_feelings_emerge` | Ray Tension | Feelings | Day 38-40 | — |
| 25 | `ray_upstairs` | Ray Gate | Upstairs | Day 38-42 | sex_unlocked_ray |
| 26 | `mark_first_conference` | Mark Act 1 | First Conference | Day 28-30 | — |
| 27 | `mark_fundraiser_volunteer` | Mark Act 1 | The Volunteer | Day 32-35 | — |
| 28 | `mark_rain_umbrella` | Mark Gate | The Rain | Day 38-40 | kiss_unlocked_mark |
| 29 | `mark_under_desk` | Mark Gate | Under the Desk | Day 42-44 | groping_unlocked_mark |
| 30 | `mark_call_from_bedroom` | Mark Bridge | The Phone Call | Day 45-47 | — |
| 31 | `mark_first_visit` | Mark Gate | The First Visit | Day 47-49 | oral_unlocked_mark |
| 32 | `mark_no_hesitation` | Mark Gate | No Hesitation | Day 50-52 | sex_unlocked_mark |
| 33 | `karen_crisis` | Mark Crisis | Karen | Day 52-55 | — |
| 34 | `mark_crisis_repair` | Mark Repair | The Parking Lot | Day 54-57 | — |
| 35 | `jake_second_attempt` | Jake Act 1 | The Second Rejection | Day 40-42 | — |
| 36 | `jake_jealousy_game` | Jake Act 1 | The Jealousy Game | Day 44-48 | — |
| 37 | `jake_bar_sitting` | Jake Act 2 | Pour Me One More | Day 48-52 | — |
| 38 | `jake_ego_crisis` | Jake Bridge | The Ego Crisis | Day 52-54 | — |
| 39 | `jake_not_yet` | Jake Gate | Not Yet | Day 52-54 | kiss_unlocked_jake |
| 40 | `jake_permission` | Jake Gate | Permission | Day 54-56 | groping_unlocked_jake |
| 41 | `jake_stockroom` | Jake Gate | The Stockroom | Day 58-60 | oral_unlocked_jake |
| 42 | `jake_on_her_terms` | Jake Gate | On Her Terms | Day 60-63 | sex_unlocked_jake |
| 43 | `jake_endgame_choice` | Jake Endgame | The Surrender | Day 63-65 | — |
| 44 | `mirror_day_20` | Mirror | Mirror — Day 20 | Day 20 | — |
| 45 | `mirror_day_40` | Mirror | Mirror — Day 40 | Day 40 | — |
| 46 | `mirror_day_60` | Mirror | Mirror — Day 60 | Day 60 | — |
| 47 | `friday_collision` | Cross-NPC | Friday Night Collision | Varies | — |
| 48 | `tom_saw_ray` | Cross-NPC | Tom Sees Ray | Day 35+ | — |
| 49 | `ray_sees_mark_text` | Cross-NPC | Ray Sees the Text | Day 45+ | — |
| 50 | `juggling_detected` | Cross-NPC | Juggling Detected | Day 45+ | — |

**Total: 50 story events**
- Jolene Phase 1: 8 events
- Tom arc: 6 events (2 setup + 4 gates)
- Tom extras: 1 bridge
- Ray arc: 7 events (3 setup + 4 gates)
- Ray extras: 1 bridge, 1 tension
- Mark arc: 8 events (2 setup + 4 gates + 1 crisis + 1 repair)
- Mark extras: 1 bridge
- Jake arc: 7 events (3 setup + 4 gates)
- Jake extras: 1 bridge, 1 endgame
- Mirror: 3 scenes (Day 1 mirror is in opening)
- Cross-NPC: 4 events

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## REPUTATION THRESHOLD EVENTS

These canvases fire automatically when Emma's reputation drops below critical thresholds. They serve as narrative warnings before game-over.

---

### REPUTATION EVENT 1: "Just Checking In" (Principal Concern)

- **Canvas ID**: `principal_concern_1`
- **Location**: `loc_school_classroom`
- **Schedule**: 12:00-15:00
- **Weekdays (TOML)**: `[0,1,2,3,4]`
- **Trigger condition**: `reputation < 60` (player trait), flag `principal_concern_triggered_60` NOT set
- **Priority**: 9
- **Is Repeatable**: false (one-time)
- **Exit Location**: `loc_school_classroom`

#### Scene

Afternoon. The classroom is empty — kids have gone home. Principal Davis appears in the doorway, coffee mug in hand, casual-but-not-casual smile. "Emma, got a minute?"

He sits on the edge of a student desk. The informality is deliberate — he wants this to feel like a conversation, not a meeting. "Just wanted to check in. How are you settling in? Everything going okay?"

His eyes are kind but attentive. She can feel him cataloging: the circles under her eyes, the fact that she missed the PTA meeting, the things Mrs. Hewitt from the General Store said to his wife at church.

"Small town, you know. People talk. I just want to make sure you're doing alright."

Media: IMAGE — "kind but concerned school principal talking to young teacher in empty classroom"

#### Effects
- Sets flag: `principal_concern_triggered_60`
- No stat changes (this is a warning, not a punishment)

---

### REPUTATION EVENT 2: "Active Monitoring" (Increased Scrutiny)

- **Canvas ID**: `principal_concern_2`
- **Location**: `loc_school_classroom`
- **Schedule**: 12:00-15:00
- **Weekdays (TOML)**: `[0,1,2,3,4]`
- **Trigger condition**: `reputation < 45` (player trait), flag `principal_concern_triggered_45` NOT set
- **Priority**: 9
- **Is Repeatable**: false (one-time)
- **Exit Location**: `loc_school_classroom`

#### Scene

Afternoon. Principal Davis again, but this time he closes the door behind him. No coffee mug. No casual lean on the desk.

"Emma, I need to be direct with you." He sits across from her, hands folded. "I've been hearing things. About your... social life. The bar visits. Some parents have raised concerns."

He pauses, letting it land.

"I hired you because you were exactly what this school needed — young, enthusiastic, a good role model. I still believe that. But I need you to understand: in a town like Millfield, perception IS reality. And right now, the perception isn't great."

He stands. "I'm going to be dropping by your classroom more often. Not because I don't trust you. Because I need to show the school board I'm paying attention."

Media: IMAGE — "serious principal sitting across from young female teacher, closed door, formal conversation"

#### Effects
- Sets flag: `principal_concern_triggered_45`
- Sets flag: `school_enforcement_warned` (increases school skip penalty from -5 to -8)

---

### REPUTATION EVENT 3: "Formal Warning" (School Board)

- **Canvas ID**: `principal_formal_warning`
- **Location**: `loc_school_classroom`
- **Schedule**: 12:00-15:00
- **Weekdays (TOML)**: `[0,1,2,3,4]`
- **Trigger condition**: `reputation < 30` (player trait), flag `principal_warning_triggered_30` NOT set
- **Priority**: 9
- **Is Repeatable**: false (one-time)
- **Exit Location**: `loc_school_classroom`

#### Scene

This time it's not just Principal Davis. Mrs. Henderson from the school board is sitting in Emma's classroom when she arrives. Two chairs pulled up to the front. They've been waiting.

"Miss Cooper, please sit down."

The meeting is formal. Short. Devastating. The school board has received "multiple complaints from community members about conduct unbecoming of an elementary school teacher." They don't name specifics — they don't have to. The specifics are written on Mrs. Henderson's face.

"We value you, Emma. But this is an official warning. One more substantiated complaint and we'll have to review your contract."

After they leave, Emma sits at her desk. The alphabet border on the wall stares at her. A, B, C. The kids' drawings are still taped to the windows. She came here to be a good teacher. She wonders when she stopped.

Media: IMAGE — "young teacher sitting alone at desk in empty classroom after serious meeting, alphabet decorations on walls, somber"

#### Effects
- Sets flag: `principal_warning_triggered_30`
- `confidence -3` (the warning hits hard)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 4 complete. Type "proceed" to continue to Phase 5: Activities,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
