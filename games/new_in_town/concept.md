# New In Town — Game Concept Document

**Game Name**: New In Town
**Protagonist**: Emma (female, player-controlled, 23)
**Genre**: Adult interactive fiction with video integration
**Theme**: Female corruption → female predator — innocence lost, power gained
**Tone**: Slow-burn Phase 1, increasingly bold and nasty Phase 2
**Setting**: Millfield — small rural farming town, population ~2,000

---

## Core Premise

Emma is a freshly graduated schoolteacher from a Christian college who moves to Millfield for her first teaching job. Sweet, sheltered, has had one boyfriend and felt guilty about it. She rents a room above the town's only bar from Jolene, the unapologetically sexual landlady.

**The Two-Phase Arc:**

- **Phase 1 (Days 1-12): Corruption** — Jolene exposes Emma to a world she's never seen. Thin walls, open sexuality, wine, dares. Emma goes from horrified to curious to awakened.
- **Phase 2 (Days 12-65): The Hunt** — Emma becomes the corruptor. She targets 4 male NPCs in town, each requiring a different strategy. She's not seducing them the same way — each man has a different resistance type, and she has to adapt.

**What Makes It Unique:**
- Female protagonist who BECOMES the predator — rare in the genre
- The corruption mechanic flips: first she's the subject, then she's the agent
- 4 NPCs with genuinely different seduction strategies (not just stat thresholds)
- Reputation system creates constant tension between her public persona (sweet teacher) and private actions (corrupting men)
- Small town setting means every risk could be witnessed — privacy is scarce

---

## Player Character: Emma

- **Age**: 23
- **Background**: Graduated from a Christian college with an education degree. First time living away from parents.
- **Sexual History**: One boyfriend, missionary position twice, felt guilty both times
- **Personality**: Genuinely kind, not fake-innocent — she just hasn't been exposed to anything. Wears cardigans and long skirts. Doesn't drink. Says "gosh" unironically.
- **Arc**: Her corruption isn't about becoming a bad person — it's about discovering she has desires she was taught to be ashamed of, and learning she *likes* having power over men.
- **The Mirror**: At Day 1, Day 20, Day 40, and Day 60, there's a scene where Emma looks in her bathroom mirror. The narration describes what she sees — and it changes each time. By Day 60, she doesn't recognize the girl who arrived with a cardigan and a Bible.

---

## Player Stats

| Stat | Start | Range | Purpose |
|------|-------|-------|---------|
| `corruption` | 0 | 0-100 | Her internal transformation — how far she's gone from who she was. One-way stat, never decreases. |
| `confidence` | 0 | 0-100 | Her ability to initiate, escalate, take control. Can drop if humiliated or caught. |
| `reputation` | 80 | 0-100 | Town's perception of her. Drops from risky behavior. Game over if it hits 0. Slow to rebuild, fast to damage. |
| `money` | 150 | 0+ (unclamped) | Teacher salary is tight, rent is due, creates time pressure. |
| `energy` | 100 | 0-100 | Drains from activities, refills from sleep. Late nights cost double. Low energy = worse choices. |

**The Key Tension:** `corruption` and `confidence` want to go UP. `reputation` wants to stay HIGH. Every bold move risks exposure. The game is about getting nastier while keeping the town fooled.

### Resource Pressure Math
- Weekly teaching salary: ~$220
- Weekly rent: $180
- Remaining for food, drinks, clothes: $40
- She is perpetually broke unless she picks up extra work — but extra work eats time slots she needs for NPCs

---

## The Catalyst: Jolene (The Landlady)

**Profile:**
- 42, owns The Dusty Boot bar, rents out the upstairs rooms
- Divorced twice, zero shame, chain-smokes on the porch in a silk robe
- Treats sex like appetite — something you satisfy, not something you agonize over
- Not predatory — she genuinely likes Emma and sees a version of her younger self
- Role: Phase 1 corruption engine. She doesn't touch Emma — she *exposes* her.

**Ongoing Phase 2 Role:** Mentor, advisor, wingwoman. Emma can go to her for strategy ("How do I get him to...?"), which gives gameplay hints. Jolene also runs the bar, so she controls access to some NPCs during evening hours.

### Jolene's Corruption Path (Phase 1 — Days 1-12)

| Day | Event | Effect |
|-----|-------|--------|
| 1-2 | Emma arrives, settles in. Jolene is warm but loud, walks around in underwear, swears freely. | Culture shock. Emma is uncomfortable. `corruption +1` |
| 3 | Thin walls — Emma hears Jolene with a man. Can't sleep. Listens longer than she should. | First voyeuristic moment. `corruption +2` |
| 4-5 | Jolene gives Emma wine at dinner. "Honey, you're wound tighter than a banjo string." Talks openly about sex, asks Emma about her experience. Emma admits almost nothing. | Jolene reads her instantly. `corruption +1, confidence +1` |
| 6 | Emma comes home early, catches Jolene mid-act through a cracked door. Jolene sees her watching. Doesn't stop. Smiles. | **Peek moment.** Emma runs to her room. Jolene doesn't mention it. `corruption +4` |
| 7-8 | Jolene starts leaving things around. A vibrator "accidentally" in the shared bathroom. Her laptop open to something explicit. "Oops, sorry hon." | Exposure therapy. Emma starts looking instead of looking away. `corruption +2` |
| 9 | Jolene takes Emma shopping in the city. Buys her a dress that's shorter than anything she's owned. "You've got legs, girl. Fucking use them." Emma wears it to dinner. Feels something. | **Confidence unlock.** She sees herself differently. `confidence +3` |
| 10 | Jolene asks directly: "When's the last time you touched yourself?" Emma's horrified. Jolene: "That's what I thought. Go to your room. Lock the door. Figure it out." | **Self-discovery milestone.** Player choice: do it or refuse. If yes: `corruption +5, confidence +3`. The game shifts. |
| 11-12 | Emma starts noticing men differently. The way the bartender's arms flex. The handyman's hands. She catches herself staring. Jolene notices. "There she is." | **Phase 1 complete.** Corruption threshold reached. Phase 2 unlocks. |

---

## NPC 1: Tom — The Deputy

**Profile:**
- 25, born and raised in Millfield, never left
- Became a deputy because his dad was sheriff before him
- Genuinely good guy — helps old ladies, rescues cats from trees
- Tall, fit from running, but has *no game*. Stammers around women. Blushes at cleavage.
- Has a crush on Emma from the moment she arrives but would never act on it
- Virgin. Has kissed two girls, both at church camp, both awkward.

**Driver:** CORRUPTION (she's corrupting his innocence)
**Resistance Type:** Innocence — he doesn't resist because he's strong, he resists because he genuinely doesn't know what's happening until it's too late
**Unique Stat:** `tom_devotion` — the higher it goes, the more he'll do for her (cover for her, lie for her, look the other way when she's with other men). He becomes an asset, not just a conquest.

**Why He's First:** Training wheels. Lowest difficulty. Emma practices on him while her confidence is still low. His innocence mirrors her old self — corrupting him is corrupting what she used to be.

### Tom's Story Arc

**Act 1 — The Excuse (Days 12-16)**
- Emma needs a reason to be around him. Jolene suggests: "Tell him you don't feel safe alone at night. That boy will be at your door in 30 seconds."
- She asks Tom to check her locks. He comes over, sweating, barely makes eye contact.
- She starts engineering encounters — walks past the station, brings him coffee, "accidentally" runs into him at the diner.
- He's pathetically grateful for every crumb of attention.

**Act 2 — The Education (Days 16-22)**
- She invites him to help set up her classroom. They're alone. She wears the dress Jolene bought.
- She starts testing: bending over in front of him, touching his arm when she laughs, standing too close.
- He turns red. Drops things. Can't form sentences.
- **Key scene:** She "trips" and he catches her. She doesn't pull away. He's holding her waist. She looks up at him and waits. He freezes. She can feel his heartbeat through his shirt.
- Player choice: **Kiss him** (`confidence +3`, fast track) or **Pull away slowly** (`corruption +2`, slow burn — makes him obsess)

**Act 3 — The Takeover (Days 22-30)**
- She invites him over to "watch a movie." Sits close. Hand on his thigh. He's vibrating.
- She has to lead *everything*. "Tom. Look at me." "Give me your hand." "Put it here."
- First time she touches him, he almost finishes immediately. She laughs — not cruelly, but she *likes* that she did that.
- **Milestone:** She teaches him to go down on her. Patient, direct, commanding. "No. Slower. Like that. Good boy."
- He's completely devoted. He'd do anything she says. She realizes: this is power. She wants more.

### Tom's Gate Flags
| Flag | Triggered By | Day (approx) |
|------|-------------|--------------|
| `kiss_unlocked_tom` | The classroom catch scene — she kisses him | Day 18-20 |
| `groping_unlocked_tom` | Movie night — she guides his hands | Day 23-25 |
| `oral_unlocked_tom` | She teaches him — "Good boy" scene | Day 26-28 |
| `sex_unlocked_tom` | She takes his virginity — she's on top, in control | Day 29-31 |

### Tom's Repeatable Activity: Coffee With Tom
- **Location:** Diner or her classroom
- **Time:** Afternoon (he's off duty)
- **Schedule:** Available Mon/Wed/Fri
- **Energy Cost:** -10
- **Base scene:** Casual conversation, she's friendly, he's nervous

| Requirement | Choice | Effect |
|-------------|--------|--------|
| Always | "Ask about his day" | `tom_devotion +1` |
| `confidence >= 10` | "Lean close when talking" | `tom_devotion +2, confidence +1` |
| `corruption >= 15` + `kiss_unlocked_tom` | "Touch his thigh under the table" | `tom_devotion +3, corruption +1` |
| `corruption >= 30` + `groping_unlocked_tom` | "Guide his hand between your legs" | `tom_devotion +4, reputation -1` (public place risk) |

**Hardship:** Afternoon slot — same time as tutoring ($30). Money vs seduction.

---

## NPC 2: Ray — The Handyman

**Profile:**
- 44, divorced, one daughter who lives with his ex two towns over
- Does odd jobs around town — fixes roofs, plumbing, fences
- Weathered, strong hands, quiet. Speaks in short sentences.
- Drinks at Jolene's bar every evening but never gets sloppy.
- He's been with women. He knows what he's doing.
- Thinks Emma is "a nice kid." Doesn't see her as a sexual being at first.

**Driver:** SEDUCTION (she must overcome his dismissal)
**Resistance Type:** Indifference — he's not fighting attraction, he genuinely doesn't register her as an option. The age gap, the power gap, the "schoolteacher" label. She has to shatter his mental category of her.
**Unique Mechanic:** Confidence accelerator — scenes with Ray give double `confidence` gains because he treats her like a woman, not a girl. But he might develop real feelings, creating a complication she didn't plan for.

**Why He's Second:** Requires more confidence than Tom. She can't stammer and blush her way through this — she has to be *deliberate*. Skills built corrupting Tom are her foundation.

### Ray's Story Arc

**Act 1 — The Invisible Wall (Days 18-24)**
- Ray does work at the bar. Emma sees him regularly. He's polite, calls her "Miss" or "ma'am."
- She tries the Tom playbook — standing close, laughing, touching his arm. He doesn't react. Not hiding it — he literally doesn't notice. She's wallpaper.
- **Frustration builds.** First NPC where the strategy doesn't just work.
- Jolene advice: "Honey, that man isn't blind. He's decided you're a category he doesn't touch. You have to break the category."

**Act 2 — Breaking The Frame (Days 24-32)**
- She stops being "the sweet teacher." Shows up at the bar at night. Drinks whiskey (badly at first). Wears the dress. Sits at the bar alone.
- Ray notices — not attraction yet, but *surprise*. "Didn't take you for a whiskey girl." First real sentence.
- She engineers a situation: asks him to fix something at her place. When he arrives, she's in a tank top and shorts. No bra. "Sorry, wasn't expecting you this early."
- He notices. She sees him notice. He looks away quickly. **First crack.**
- She starts showing up when he's working — brings him water on a hot day, watches him openly.
- **Key scene:** He's fixing the bar's back fence. She brings two beers, sits on the tailgate of his truck. First real conversation. He tells her about his daughter. She touches his forearm when he says something sad. He doesn't pull away.
- She lets the silence stretch. He looks at her differently. "You're not what I expected, Miss."

**Act 3 — The Reversal (Days 32-42)**
- Seduction shifts from her pushing to him *resisting something he now feels.*
- He starts finding reasons to be at the bar when she's there. Shows up to fix things that aren't broken.
- **Key scene:** She asks him to teach her to use tools. Shed behind the bar. She "can't get the angle right." He stands behind her to guide her hands. She presses back into him. He goes still. She can feel him hard against her.
- Player choice: **Turn around and look at him** (direct confrontation) or **Stay pressed against him and keep "sawing"** (torture him with plausible deniability)
- He breaks first. After bar closes, walking her to the stairs. She stops on the second step — eye level. He kisses her. Hard. Pulls back. "This is a bad idea."
- She says: "I know." Pulls him by the belt.
- Sex with Ray is different than Tom. He knows what he's doing. She doesn't have to lead. For the first time, someone makes *her* gasp. But afterward — she realizes she still wants control. She doesn't want to be the one gasping. She wants to be the one *making* them gasp.

### Ray's Gate Flags
| Flag | Triggered By | Day (approx) |
|------|-------------|--------------|
| `kiss_unlocked_ray` | Staircase kiss — he breaks first | Day 32-34 |
| `groping_unlocked_ray` | Shed scene — pressed against him | Day 30-32 |
| `oral_unlocked_ray` | She drops to her knees in his truck after a bar night | Day 36-38 |
| `sex_unlocked_ray` | He pulls her upstairs — raw, urgent | Day 38-42 |

### Ray's Repeatable Activity: Evening at the Bar (Ray Focus)
- **Location:** The Dusty Boot
- **Time:** Evening or Night
- **Energy Cost:** -15 (plus drink costs $5-8)
- **Base scene:** She sits at the bar. Ray's at his usual spot.

| Requirement | Choice | Effect |
|-------------|--------|--------|
| Always | "Sit near him, drink quietly" | `ray_interest +1` |
| `confidence >= 20` | "Ask about his work, touch his forearm" | `ray_interest +2` |
| `confidence >= 40` + `kiss_unlocked_ray` | "Whisper something about last time" | `ray_interest +3, reputation -1` if overheard |
| `corruption >= 50` + `groping_unlocked_ray` | "Follow him to his truck in the parking lot" | `ray_interest +4, reputation -2` (dark lot, anyone could see) |

---

## NPC 3: Mark — The Student's Father

**Profile:**
- 38, married to Karen (homemaker, PTA, passive-aggressive)
- Has a 10-year-old son in Emma's class
- Insurance agent — dull job, dull marriage, dull life. He knows it.
- Handsome in a suburban way — keeps fit, decent clothes, good jaw
- Comes to parent-teacher conferences. Coaches little league. Model citizen.
- Hasn't been touched with passion in years. Karen gives pecks on the cheek. Separate beds "because of his snoring."
- Not looking to cheat. Just... hollow.

**Driver:** FORBIDDEN (the taboo is the engine)
**Resistance Type:** Morality + Fear — he has a family, a reputation, a life that would detonate if this got out. His resistance is real and justified. She has to make the risk feel worth it.
**Unique Stat:** `mark_guilt` — manipulable. High guilt = he pulls away but comes crawling back harder. Low guilt = available but boring. She has to keep him in the sweet spot — guilty enough to be desperate, not so guilty he confesses to his wife.

**Why He's Third:** First NPC where stakes extend beyond the two of them. Getting caught destroys a family. `reputation` under serious threat. Needs confidence from Tom and Ray to attempt this.

### Mark's Story Arc

**Act 1 — The Crack in the Wall (Days 28-35)**
- Parent-teacher conference. Mark comes alone (Karen has a "headache"). Emma's wearing the dress — it's just what she wears now.
- Professional meeting. But she notices: he lingers. Asks questions unrelated to his kid. Laughs at things that aren't funny. He's *starved* for attention.
- She doesn't push. Just holds eye contact a beat too long. Smiles. Touches his hand giving him the report card. "Your son is wonderful. He must get it from you."
- He thinks about that sentence for three days.

**Act 2 — The Arrangement (Days 35-46)**
- Mark volunteers to help with the school fundraiser. Excuse to be around her.
- They work late in the classroom. He brings coffee. Conversation gets personal — his marriage, her "loneliness" (she plays it up). She creates emotional intimacy Karen doesn't provide.
- **Key scene:** After a late session, walking to his car. Raining. They share his umbrella. She's pressed against him. She shivers — exaggerated. He puts his arm around her. She looks up. The moment stretches. He almost kisses her. Pulls back. "I should go."
- She texts that night: "I had a really nice time tonight. 😊" Innocent on the surface. He knows what it means. He texts back.
- Texting escalates. She controls the pace: "I keep thinking about the rain." → "What would you have done if you hadn't stopped?" → "I wish you hadn't stopped."
- He starts making excuses to see her. She starts dressing specifically for the days she knows he's coming.

**Act 3 — The Fall (Days 46-58)**
- He shows up at her door one evening. "Karen thinks I'm at a meeting." His hands are shaking.
- She doesn't rush it. Makes coffee. Sits close. Talks. Lets the tension build until he breaks.
- First time: desperate, fast, guilt-ridden. He finishes and immediately panics. "What did I do. Oh god."
- Player choice: **"You did what you wanted"** (dominance — she owns his guilt) or **"We both wanted this"** (tenderness — makes him feel safe)
- He comes back. Of course he comes back. Each time the guilt fades faster.
- She starts pushing the taboo: his car in the school parking lot after hours. His office during lunch. "Call me from the bedroom. While she's downstairs."
- **Crisis point:** Karen finds a suspicious text. Shows up at Emma's school. Public confrontation. Emma plays innocent perfectly — "He's been helping with the fundraiser, that's all." Karen backs down but watches.
- `reputation` takes a hit. Player must manage fallout.

### Mark's Gate Flags
| Flag | Triggered By | Day (approx) |
|------|-------------|--------------|
| `kiss_unlocked_mark` | Rain/umbrella scene — almost-kiss, then first text exchange | Day 38-40 |
| `groping_unlocked_mark` | Late classroom session — she guides his hand to her thigh under the desk | Day 42-44 |
| `oral_unlocked_mark` | His first visit to her room — she pushes him onto the bed | Day 47-49 |
| `sex_unlocked_mark` | He comes back the second time — no hesitation | Day 50-52 |

### Mark's Repeatable Activity: Parent Conferences
- **Location:** School
- **Time:** Late Afternoon (scheduled)
- **Schedule:** Available Tue/Thu (he invents reasons to come)
- **Energy Cost:** -10
- **Base scene:** Professional meeting about his son. Door open. Other teachers in the building.

| Requirement | Choice | Effect |
|-------------|--------|--------|
| Always | "Keep it professional, hold eye contact" | `mark_desire +1` |
| `confidence >= 25` | "Brush against him when handing papers" | `mark_desire +2, mark_guilt +1` |
| `corruption >= 40` + `kiss_unlocked_mark` | "Close the door. Stand too close." | `mark_desire +3, mark_guilt +2, reputation -2` |
| `corruption >= 60` + `groping_unlocked_mark` | "Lock the door. Tell him you missed him." | `mark_desire +4, mark_guilt +3, reputation -3` |

**Hardship:** Happens AT HER WORKPLACE. Every escalation risks her career. Other teachers walk by. The principal's office is down the hall. If `reputation` drops below 40, the principal starts "checking in" during these meetings.

---

## NPC 4: Jake — The Bartender

**Profile:**
- 28, works at Jolene's bar, thinks he's God's gift
- Good-looking and knows it. Lean, tattoos, lazy smile.
- Flirts with every woman who walks in. Reflexive, not meaningful.
- Already tried his moves on Emma. She shot him down when she was still "old Emma."
- He assumes she's a prude. Filed her under "not happening."
- Sleeps around — currently seeing two women in the next town.
- His weakness: his ego. He *needs* to believe he's in control.

**Driver:** DOMINANCE (she dominates him — power reversal)
**Resistance Type:** Ego — he doesn't resist sex, he resists *submission*. He'll fuck her gladly, on his terms. The game is making it on HER terms. Making the cocky guy kneel.
**Unique Stat:** `jake_power` — tracks who's in control. Starts at his 100%. Every interaction she wins flips it toward her. At 50/50 the dynamic is hottest. At 80%+ hers, he's completely submissive.

**Why He's Last:** Endgame NPC. Requires maximum `corruption` and `confidence`. She's not seducing him — she's *breaking* him. Only works after she's become someone completely different from Day 1 Emma.

### Jake's Story Arc

**Act 1 — The Setup (Days 40-48)**
- Emma's a regular at the bar now. Drinks, flirts, not the cardigan girl anymore.
- Jake tries again. Leans over the bar: "So, you finally loosened up. Wanna get out of here?"
- She shuts him down — differently than before. Not flustered. She just *laughs*. "That's your move? Really?"
- He's rattled. No one laughs at him.
- She starts a game: flirts with OTHER men at the bar while Jake watches. Touches their arms. Whispers. Glances at Jake to make sure he sees.
- Goal isn't jealousy — it's making him realize she's not the one chasing.

**Act 2 — The Flip (Days 48-56)**
- He escalates attempts. She escalates rejections — each more humiliating, more fun for her.
- **Key scene:** Bar closing, she's the last one. He's cleaning up. She sits on the bar. "Pour me one more." He does. She takes the glass, holds eye contact, drinks slowly. "You want me so badly it's almost sweet."
- He tries to kiss her. She puts one finger on his lips. "Not yet." Gets off the bar. Walks upstairs. Doesn't look back.
- He's losing his mind. Starts doing things he's never done — showing up sober, actually listening, being *nice*. She's rewiring him.
- Jolene watches with amusement: "You've got that boy running in circles."

**Act 3 — The Submission (Days 56-65)**
- She lets him in. On her terms.
- Tells him exactly where to be, what to wear, when to show up. He complies. The cocky guy follows instructions.
- First time: she's on top. Controls pace, position, everything. He reaches for her hips — she pins his hands. "Did I say you could touch?"
- He's never experienced this. Discovers he *likes* not being in charge. Scares him.
- She pushes further each time. Tells him what to say. Makes him wait. Makes him beg.
- **Key scene:** She makes him get on his knees in the stockroom behind the bar. Jolene's in the front. Customers 20 feet away. "Someone could walk in." "Then you'd better be quick."
- **Endgame choice:** **Keep him as her submissive** (he's hers completely) or **Break it off and let him wonder** (she never needed him — the power was the point).

### Jake's Gate Flags
| Flag | Triggered By | Day (approx) |
|------|-------------|--------------|
| `kiss_unlocked_jake` | She finally allows one kiss — then walks away | Day 52-54 |
| `groping_unlocked_jake` | She lets him touch her but controls exactly where/how | Day 54-56 |
| `oral_unlocked_jake` | Stockroom scene — on his knees | Day 58-60 |
| `sex_unlocked_jake` | On her terms — she's on top, his hands pinned | Day 60-63 |

### Jake's Repeatable Activity: Evening at the Bar (Jake Focus)
- **Location:** The Dusty Boot
- **Time:** Evening or Night
- **Energy Cost:** -15 (plus drink costs $5-8)
- **Base scene:** She sits at the bar. Jake's behind the counter.

| Requirement | Choice | Effect |
|-------------|--------|--------|
| Always | "Flirt and shut him down" | `jake_power +1` toward her |
| `confidence >= 35` | "Flirt with another man while Jake watches" | `jake_power +2, jake_jealousy +1` |
| `corruption >= 55` + `kiss_unlocked_jake` | "Lean over the bar, give him the view, walk away" | `jake_power +3` |
| `corruption >= 70` + `oral_unlocked_jake` | "Tell him to meet you in the stockroom" | `jake_power +4, reputation -3` (Jolene's bar — she might notice) |

---

## Gate Flag System

Each NPC has independent gate flags. Gates are set by ONE-TIME story events per NPC.

### Per-NPC Gates
| NPC | kiss_unlocked | groping_unlocked | oral_unlocked | sex_unlocked |
|-----|---------------|------------------|---------------|--------------|
| Tom | Day ~18-20 | Day ~23-25 | Day ~26-28 | Day ~29-31 |
| Ray | Day ~32-34 | Day ~30-32 | Day ~36-38 | Day ~38-42 |
| Mark | Day ~38-40 | Day ~42-44 | Day ~47-49 | Day ~50-52 |
| Jake | Day ~52-54 | Day ~54-56 | Day ~58-60 | Day ~60-63 |

### Player-Level Gates (corruption thresholds)
| Threshold | Unlocks |
|-----------|---------|
| `corruption >= 10` | Phase 2 begins — she starts noticing men |
| `corruption >= 25` | Can attempt bold physical moves |
| `corruption >= 45` | Can pursue married NPC (Mark) |
| `corruption >= 65` | Can attempt dominance plays (Jake) |
| `corruption >= 85` | Endgame content — full power fantasy |

---

## Daily Schedule & Time System

8 time periods per day:

| Slot | Hours | Weekday Use | Weekend Use |
|------|-------|-------------|-------------|
| Early Morning | 05:00-07:00 | Wake up, optional jog (energy +10) | Free |
| Morning | 07:00-09:00 | **SCHOOL (mandatory)** | Free |
| Late Morning | 09:00-12:00 | **SCHOOL (mandatory)** | Free |
| Afternoon | 12:00-15:00 | Free — tutoring, errands, NPC time | Free |
| Late Afternoon | 15:00-17:00 | Free — NPC time, shopping, prep | Free |
| Evening | 17:00-19:00 | Dinner, bar opens, NPC time | Free |
| Night | 19:00-22:00 | Bar peak, NPC time, high-risk window | Free |
| Late Night | 22:00-01:00 | Bar closing, most dangerous/rewarding | Free |

**Weekdays:** 2 free daytime slots + 3 evening/night slots = 5 usable
**Weekends:** All 8 slots free, but NPCs have own schedules (Mark with family, Tom on duty sometimes)

---

## Economic Model

### Income Sources
| Source | Pay | Time Slot | Schedule | Notes |
|--------|-----|-----------|----------|-------|
| Teaching salary | $220/week (auto) | Morning + Late Morning | Mon-Fri (mandatory) | Fixed, reliable |
| Tutoring | $30/session | Afternoon | Mon/Wed available | `reputation +1` |
| Bar shifts (Jolene) | $50 + tips ($10-30) | Evening OR Night | Available after Day 8 | Good money, kills NPC time |
| Weekend cafe job | $45/shift | Morning + Late Morning | Sat OR Sun | Conflicts with church (Sun) and recovery (Sat) |

### Expenses
| Expense | Cost | Frequency | Consequence If Missed |
|---------|------|-----------|----------------------|
| Rent | $180 | Weekly (7-day timer) | Jolene warns once, then demands bar shifts |
| Groceries | $25 | Every 5 days | Energy max drops by 20/day until restocked |
| Bar drinks | $5-8 | Per visit | Required for bar NPC interactions |
| Clothes/appearance | Variable | Optional | Better clothes unlock confidence-gated options |

### The Squeeze
$220 salary - $180 rent = $40 surplus. Food costs ~$35/week. That leaves $5. She literally cannot afford to go to the bar without picking up extra work. Every dollar spent on a dress for Mark is a tutoring session she'll need later.

---

## Survival Activities

### Grocery Shopping
- **Location:** General store | **Time:** Afternoon or Late Afternoon
- **Cost:** $25 | **Energy:** -10
- **Effect:** Sets `food_stocked` flag (lasts 5 days)
- If food runs out: `energy` max drops by 20 each day until restocked
- **Risk:** Store owner is gossipy. Buying wine or condoms here → `reputation -1`

### Rent Payment
- **Trigger:** Every 7 days (`days_since_flag` timer)
- **Cost:** $180
- If missed once: Jolene is understanding. Twice: warning. Three times: Jolene demands bar shifts to cover it — locks evening time slots.

### Sleep
- **Location:** Her room | **Time:** Late Night (mandatory) or Night (early sleep)
- Sleep at Night (19-22): Full energy restore (100)
- Sleep at Late Night (22-01): Standard restore (80)
- Skip Late Night (out at bar): Only 60 energy next day
- Skip two nights: Energy capped at 40, `reputation -1` (shows up to school wrecked, principal notices)

### Church Attendance
- **Time:** Sunday Morning (mandatory for reputation)
- **Effect:** `reputation +3`
- If skipped: `reputation -5` — the town notices when the new teacher doesn't show
- Mark's family is at church. She sits three rows behind him. They can't look at each other. Karen watches.

### School Events
- **Trigger:** Random, 1-2 per week (PTA meeting, bake sale, parent night)
- **Time:** Evening, sometimes Late Afternoon
- **Effect:** `reputation +2-4`
- If skipped: `reputation -3` and principal suspicion increases
- Parent night: Mark is there — with Karen. She has to be professional.

---

## Money Activities

### Tutoring
- **Location:** Library or classroom | **Time:** Afternoon (Mon/Wed)
- **Pay:** $30 | **Energy:** -15
- **Effect:** `money +30, reputation +1`
- Safe, boring, but reputation boost is strategically useful after risky moves.

### Bar Shifts
- **Location:** The Dusty Boot | **Time:** Evening OR Night
- **Pay:** $50 + tips ($10-30) | **Energy:** -25
- Available after Day 8
- Evening bar shift = can't pursue Ray or Mark that night
- Night shift = she's there when Jake is, but she's working
- **Hidden benefit:** `confidence +1`, access to overhear gossip/NPC intel

### Weekend Cafe Job
- **Location:** Millfield Diner | **Time:** Morning + Late Morning (Sat OR Sun)
- **Pay:** $45 | **Energy:** -20
- Sunday shift conflicts with church — choose money or reputation
- Saturday morning = can't recover from Friday night

---

## Reputation Maintenance Activities

### Sunday School Volunteering
- **Time:** Sunday Late Morning (after church)
- **Energy:** -15
- **Effect:** `reputation +4`
- Emergency reputation repair button. Burns entire Sunday morning.

### Neighborly Visits
- **Time:** Late Afternoon, 2x/week
- **Energy:** -10
- **Effect:** `reputation +2`, occasionally gossip intel (early warning about Karen, rumors about "the teacher at the bar")
- Intel can be critical — hear Karen is suspicious → back off Mark before crisis hits.

---

## NPC Mentor Activity

### Jolene Chats
- **Location:** Bar or upstairs kitchen | **Time:** Late Morning (weekdays) or Afternoon
- **Energy:** -5
- **Effect:** Strategy tips, `confidence +1`, sometimes NPC intel
- Jolene drops hints: "Ray's daughter's birthday is next week, he gets real quiet" — exploitable info
- Minimal hardship but time investment that pays off indirectly.

---

## Hardship Design Principles

### 1. Scarcity Creates Drama
She can never do everything. Every "yes" to one NPC is a "no" to another. Every dollar spent on a dress is a tutoring session needed later.

### 2. Exhaustion Creates Mistakes
Low energy = worse choices appear. At `energy < 30`, risky options get a "reckless" tag — higher stat gains but double reputation damage. The game tempts her to push through exhaustion, which is when she gets caught.

### 3. Reputation Is The Slow Bleed
Doesn't crash overnight. Leaks: -1 here, -2 there. Player doesn't notice until suddenly at 45 and the principal is "having a word." Recovery is slow (+2-4 from church/volunteering) but damage is fast (-3 from bar, -2 from closed doors). Asymmetry is intentional.

### 4. NPCs Compete For Same Time Slots
Ray and Jake are both at the bar in the evening. Can't pursue both in the same night without one noticing. Tom wants afternoon time — same as tutoring and Mark's conferences. The schedule itself forces trade-offs.

### 5. Money Is The Invisible Chain
Never *enough*. Always one bad week from missing rent. Keeps her working when she'd rather be seducing, and seducing when she should be working.

---

## Overall Timeline

| Phase | Days | Focus | Emma's State |
|-------|------|-------|-------------|
| Phase 1 | 1-12 | Jolene corrupts Emma | Innocent → Awakened |
| Tom arc | 12-30 | First conquest — learns to lead | Experimenting |
| Ray arc | 18-42 | Real challenge — learns boldness | Confident |
| Mark arc | 28-58 | Dangerous game — learns manipulation | Calculating |
| Jake arc | 40-65 | Final boss — learns domination | Transformed |

**NPCs overlap** — she's juggling multiple men simultaneously. Tom is still devoted while she's working on Ray. Mark is texting her while she's teasing Jake. The schedule system makes her choose who to spend time with each slot.

---

## The Grind-to-Story Ratio

Ideal rhythm between story events:

```
STORY EVENT (big moment, gate unlock, plot advancement)
    ↓
3-5 days of ACTIVITIES (grinding stats, earning money, managing reputation)
    ↓
TENSION BUILD (small events — close call, jealous text, rumor)
    ↓
2-3 more days of ACTIVITIES (pressure mounting)
    ↓
NEXT STORY EVENT (earned through stats + flags + time passage)
```

Activities aren't filler — they're the foundation that makes story events land. When she finally gets Mark alone after juggling conferences, Tom's neediness, rent payments, and Karen's suspicion for 8 days — that moment MEANS something because she worked for it.

---

## Example Pressure Week (Week 3)

```
MONDAY
  Morning:     School (mandatory)
  Afternoon:   Tutoring ($30) OR Coffee with Tom — CAN'T DO BOTH
  Evening:     Groceries needed (food runs out tomorrow)
  Night:       Bar — Ray is there, but she worked all day, energy at 45
  Late Night:  Sleep (must, or tomorrow is wrecked)

TUESDAY
  Morning:     School — running on 80 energy
  Afternoon:   Mark conference scheduled — but she hasn't bought groceries
  Evening:     Bar shift available ($60) — she needs rent money
  Night:       Jake is working, she could stay after shift... energy at 35
  Late Night:  Sleep or crash

WEDNESDAY
  Morning:     School — energy at 60 because she stayed up
  Afternoon:   Tom wants coffee — she's been dodging him, devotion dropping
  Evening:     FREE — but rent is in 2 days and she's $40 short
  Night:       STORY EVENT: Ray asks her to help with a job
  Late Night:  She can't afford to say no but she's exhausted

THURSDAY
  Morning:     School — principal comments she looks tired. reputation -1
  Afternoon:   Mark conference — Karen drops him off. Watches from the car.
  Evening:     Bar shift (need money) — Jake flirts hard, she's distracted
  Night:       Tom texts: "Haven't seen you in a while. Everything ok?"
  Late Night:  RENT DUE TOMORROW. She has $175. Short $5.
               Jolene: "I'll cover it, but you owe me a Saturday shift."

FRIDAY
  Morning:     School — last day, energy shot
  Afternoon:   FREE — needs food AND reputation maintenance
  Evening:     Bar — all NPCs might be here. It's Friday night.
               Tom off duty (drinking). Ray at his spot. Jake working.
               Mark... here? Without Karen? Catches her eye across the room.
               She has to choose who to focus on while others watch.
  Night:       EVERYTHING COLLIDES.
```

---

## The Mirror Mechanic

Four transformation checkpoints where Emma looks in her bathroom mirror:

- **Day 1:** Cardigan, long skirt, no makeup. She smiles at herself — nervous but hopeful. "You can do this."
- **Day 20:** The dress. Makeup she didn't own two weeks ago. She tilts her head. Studies herself. Something is different and she can't name it.
- **Day 40:** She stands in her underwear. Looks at her body the way she's learned men look at it. She doesn't blush. She likes what she sees. She thinks about three different men and feels nothing resembling guilt.
- **Day 60:** She barely recognizes herself. Not the clothes — the eyes. The way she holds herself. The girl with the Bible would be horrified. She smiles. The smile isn't kind.

---

## Locations

| Location | Mood | Primary NPC | Activity Type |
|----------|------|-------------|---------------|
| **School — Classroom** | Professional, tense | Mark / Solo | Teaching, conferences, fundraiser work |
| **School — Parking Lot** | Risky, after-hours | Mark | Late-night car encounters |
| **The Dusty Boot — Bar** | Social, charged | Ray / Jake | Drinking, flirting, bar shifts |
| **The Dusty Boot — Stockroom** | Hidden, dangerous | Jake | Secret encounters |
| **The Dusty Boot — Upstairs (Emma's Room)** | Private, intimate | Any NPC | Inviting men over |
| **The Dusty Boot — Upstairs (Jolene's Space)** | Jolene's domain | Jolene | Corruption events, mentoring |
| **Diner** | Public, safe | Tom | Coffee dates, cafe shifts |
| **General Store** | Public, gossipy | Solo | Grocery shopping |
| **Church** | Public, performative | Solo / Mark (visible) | Reputation maintenance |
| **Library** | Quiet, intimate | Tom / Solo | Tutoring |
| **Deputy Station** | Professional | Tom | Engineered visits |
| **Ray's Truck / Shed** | Rough, private | Ray | Physical encounters |
| **Mark's Office** | Forbidden, risky | Mark | Lunch visits |
| **Town Streets** | Public | Any | Random encounters, being seen |

---

## Design Strengths

- **Female predator protagonist** — extremely rare in the genre, strong differentiator
- **Two-phase corruption arc** — she's the subject THEN the agent, unique mechanical flip
- **4 genuinely different seduction strategies** — not just stat thresholds, each NPC requires different psychology
- **Reputation as survival mechanic** — constant tension between private desire and public persona
- **Small town panopticon** — every risky move could be witnessed, privacy is scarce
- **Economic squeeze** — she can barely afford to exist, forcing trade-offs between survival and seduction
- **NPC overlap / juggling** — managing multiple men simultaneously creates scheduling drama
- **Escalating moral weight** — Tom is harmless fun, Mark destroys a family, Jake is pure power — each NPC raises the stakes
- **The Mirror** — visual transformation tracker gives narrative structure to the corruption
- **Jolene as mentor** — provides gameplay hints within the fiction, not as UI tips
