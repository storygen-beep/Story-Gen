# PHASE 2: CHARACTERS & STAT ECONOMY
# New In Town

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## TOML TRANSLATION CONVENTIONS

The following conventions apply when translating this book to TOML for the engine:

### NPC IDs (TOML `npc_` prefix required)

| Book Name | TOML ID |
|-----------|---------|
| Tom | `npc_tom` |
| Ray | `npc_ray` |
| Mark | `npc_mark` |
| Jake | `npc_jake` |
| Jolene | `npc_jolene` |

### NPC Stat Naming (UNPREFIXED on NPC object)

NPC traits use **unprefixed names** scoped to their NPC. The book uses the NPC name for clarity, but the TOML trait name drops the prefix:

| Book Reference | TOML npcId | TOML trait_key | Starting | Direction |
|----------------|------------|----------------|----------|-----------|
| Tom: devotion | `npc_tom` | `devotion` | 0 | 0 → 100 |
| Ray: interest | `npc_ray` | `interest` | 0 | 0 → 100 |
| Mark: desire | `npc_mark` | `desire` | 0 | 0 → 100 |
| Mark: guilt | `npc_mark` | `guilt` | 0 | 0 → 50 |
| Jake: power | `npc_jake` | `power` | 100 | 100 → 0 |
| Jolene: mentorship | `npc_jolene` | `mentorship` | 0 | 0 → 100 |

**TOML effect example**: Book says "+2 devotion (Tom)" → TOML: `{ targetType = "npc", npcId = "npc_tom", trait = "devotion", op = "add", value = 2 }`

### Player Traits (TOML `[player].core_traits`)

| Trait | Starting | Clamp | Notes |
|-------|----------|-------|-------|
| `corruption` | 0 | default [0,100] | One-way — never decreases |
| `confidence` | 0 | default [0,100] | Can decrease from rejection |
| `reputation` | 80 | default [0,100] | Starts high (respectable teacher) |
| `energy` | 100 | default [0,100] | |
| `money` | 150 | **`clamp = false`** | Can go negative (debt) |

**TOML player block**:
```toml
[player]
id = "player"
name = "Emma"
core_traits = { corruption = 0, confidence = 0, reputation = 80, energy = 100, money = 150 }
```

### Gate Flag Naming

Per-NPC gate flags use `{npc}_{tier}_unlocked` format: `tom_kiss_unlocked`, `ray_groping_unlocked`, etc. Kissing Tom does NOT unlock kissing Ray — each NPC has independent gates.

Flags are **ONE-WAY** (set to true only, cannot be unset). The engine tracks `set_day` metadata automatically for `days_since_flag` conditions.

### Media Blocks

Throughout the book, media tags translate to TOML content blocks:
- `Media: IMAGE — "description"` → `{ type = "image", props = { search_queries = ["description"] } }`
- `Media: VIDEO — "description"` → `{ type = "video", props = { search_queries = ["description"] } }`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: PLAYER DEFINITION

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Name**: Emma (player-named, default: Emma)
**Age**: 23
**Portrait Reference**: Young woman, light brown hair usually pulled back in a ponytail, minimal makeup, clear skin, wide eyes that read as innocent. Attractive in a girl-next-door way she hasn't learned to weaponize yet. Dressed conservatively on arrival — cardigans, long skirts, modest necklines. Appearance transforms radically over 65 days.

### Background

Emma grew up in a devout Christian household in a mid-sized suburban town. Her parents were strict but loving. Church every Sunday, youth group on Wednesdays, a Christian summer camp every July. She was valedictorian at her Christian high school and attended a Christian college where she earned her education degree in four years without a single hangover.

She had one boyfriend — David — junior year. They dated for seven months. They had sex twice, missionary position, lights off, and she cried afterward both times from guilt. David broke up with her because she "couldn't relax." She told herself she wasn't ready. The truth she couldn't admit: she didn't feel anything. Not revulsion, not pleasure. Nothing. She filed it under "maybe someday" and threw herself into student teaching.

She applied to twelve schools. Millfield Elementary was the only one that offered. Population 2,000, 90 minutes from the nearest city, one bar, one church. She took it because she had no other option. She arrives with two suitcases, a Bible her mother packed, and zero awareness of what she's walking into.

She rents the upstairs room at The Dusty Boot bar because it's the only affordable room in town. Her landlady is a twice-divorced, chain-smoking, sexually unapologetic 42-year-old named Jolene. Emma's mother would faint.

### Starting Stats

| Stat | Starting Value | Clamp | Purpose |
|------|---------------|-------|---------|
| `corruption` | 0 | true (0-100), one-way — never decreases | Internal transformation tracker. Measures how far she's moved from the girl who arrived. Unlocks NPC attempts and bolder choices. |
| `confidence` | 0 | true (0-100), can decrease | Ability to initiate, escalate, and take control. Grows from successful seduction moves. Drops from humiliation, rejection, or getting caught. |
| `reputation` | 80 | true (0-100) | Town's perception of the sweet new teacher. Drops from risky behavior, gossip, being seen. **Game over if it reaches 0** (fired and driven out). Slow to rebuild (+2-4), fast to damage (-1 to -5). |
| `money` | 150 | false (can go negative) | Cash on hand. Teacher salary barely covers rent. Creates time pressure — work vs NPC time. |
| `energy` | 100 | true (0-100) | Daily pool. Drains from activities. Refills from sleep. Low energy unlocks "reckless" choices with higher stat gains but double reputation damage. |

**`reputation`** is the survival mechanic. At thresholds:
- 60: Subtle signs — a church lady mentions Emma was "at the bar again last night"
- 45: Principal pulls her aside: "Just want to make sure you're settling in okay..."
- 30: Active monitoring — principal checks in on her conferences, church whispers grow louder
- 15: Formal warning — school board meeting about "teacher conduct"
- 0: **Game over** — contract terminated, forced to leave Millfield

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Player Psychology

**Want**: A fresh start. Independence. To be a good teacher and prove to her parents (and herself) that she can survive on her own.

**Need**: To feel *alive*. She's spent 23 years performing goodness — being the valedictorian, the youth group leader, the girl who never breaks rules. She's never once asked herself what she actually *wants*. She needs to discover desire, agency, and the thrill of being the one who makes things happen rather than the one things happen to.

**Fear**: Being seen. Not in the sense of being caught — in the sense of being *known*. She's terrified that underneath the cardigan and the Bible is someone her parents, her church, and her old self wouldn't recognize. The corruption arc is the process of meeting that person and deciding whether to run from her or become her.

**Flaw**: She overcorrects. Once she discovers power, she pursues it without pausing to examine what it costs — to others or to herself. She doesn't mean to be cruel, but she's so intoxicated by the novelty of agency that she treats people as experiments. Tom's devotion, Ray's surprise, Mark's desperation, Jake's submission — she collects reactions like someone making up for 23 years of feeling nothing.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Player Emotional Phases

Emma's emotional journey maps to her corruption arc, not a single relationship. Each phase is triggered by a milestone in her overall transformation:

| Phase | Triggered By | Emma's Mindset | How It Shows in Narration |
|-------|-------------|---------------|--------------------------|
| INNOCENT | Arrival (Day 1) | Nervous, polite, overwhelmed | Notices environment and rules. Short, safe observations. "The bar smells like cigarettes and fried food. The stairs creak. My room is small but clean." |
| CURIOUS | Jolene's peek event (Day 6) | Uncomfortable but can't look away. Shame mixed with fascination. | Longer internal passages. Rationalizing. "I shouldn't have watched. I should have closed the door. But I didn't. Why didn't I?" |
| AWAKENED | Self-discovery milestone (Day 10) | The shame breaks. She starts wanting. | Narration becomes physical. She notices men's hands, shoulders, the way fabric stretches. "He lifted the box and his shirt pulled tight across his back. I watched." |
| HUNTING | First successful move on Tom (Day ~16) | Experimental. Giddy. Testing her power. | Playful, almost amused narration. "He turned red. I did that. I made that happen." Short, punchy sentences. Discovery energy. |
| CALCULATING | Ray notices her / Mark begins (Day ~28) | Strategic. She's thinking 2 moves ahead. | Narration shifts to planning. "If I wear the dress on Tuesday, he'll notice. If I brush against him when I hand back the papers, he won't be able to concentrate for the rest of the meeting." Deliberate, controlled. |
| PREDATORY | Jake submission arc begins (Day ~50) | Fully transformed. Power is the drug. | Direct, confident, unapologetic narration. "I told him where to put his hands. He obeyed. Of course he did." No hesitation, no qualification. She describes what she wants and takes it. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Player Internal Voice

**What Emma notices (evolves over time):**

| Phase | Notices | Example |
|-------|---------|---------|
| INNOCENT | Environment, structure, safety | "The town has one traffic light. The school is three blocks from the bar. The church is on the corner." |
| CURIOUS | Other people's bodies, sensations she can't name | "Jolene's robe slipped off one shoulder. She didn't fix it. I couldn't stop staring at her collarbone." |
| AWAKENED | Men specifically — physical details, how they react to her | "Tom's hands shook when he handed me the coffee. His fingers are long. I wonder what they'd feel like." |
| HUNTING | The effect she has — micro-reactions, pupils, breathing | "His eyes dropped to my neckline for half a second. He thought I didn't notice. I noticed." |
| CALCULATING | Vulnerabilities, schedules, patterns she can exploit | "Mark always comes alone on Tuesdays. Karen has book club. The classroom is empty by 4:30." |
| PREDATORY | Power dynamics, submission cues, the thrill itself | "Jake's jaw clenched when I told him to wait. He wanted to move. He didn't. That pause — that's the best part." |

**How Emma describes NPCs (evolves over time):**

| Phase | Description Style | Example |
|-------|------------------|---------|
| INNOCENT | Role-based, distant | "Tom is the deputy. He seems nice. Nervous." |
| CURIOUS | Noticing physical presence | "Tom is tall. Really tall. He has to duck through the door frame." |
| AWAKENED | Attraction-filtered | "Tom's uniform fits tight across his shoulders. He smells like laundry detergent and something underneath it." |
| HUNTING | Possessive, evaluating | "Tom blushes when I touch his arm. He's mine already. He just doesn't know it." |
| CALCULATING | Strategic, comparative | "Ray is harder than Tom. Tom gives you everything if you smile. Ray doesn't see you unless you make him." |
| PREDATORY | Proprietary, dominant | "Jake thinks he's in charge. Jake is wrong. He just hasn't figured it out yet." |

**Choice text framing (evolves over time):**

| Phase | Choice Tone | Example |
|-------|------------|---------|
| INNOCENT | Cautious, polite | "Thank him for checking the locks" / "Keep the conversation short" |
| CURIOUS | Internal, private | "Listen through the wall" / "Put in earplugs" |
| AWAKENED | Testing, uncertain | "Wear the dress to school" / "Wear the cardigan" |
| HUNTING | Playful, deliberate | "Lean close when you laugh" / "Keep your distance" |
| CALCULATING | Strategic, risk-aware | "Close the classroom door" / "Keep it open — too risky today" |
| PREDATORY | Direct, commanding | "Tell him to get on his knees" / "Make him wait another day" |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### The Mirror Mechanic

Four scripted scenes where Emma looks in her bathroom mirror. These are NOT optional — they're narrative checkpoints that make the transformation tangible.

**Mirror 1 — Day 1:**
She's unpacking. She catches herself in the bathroom mirror. Ponytail, no makeup, the cardigan her mother gave her. She looks young. She looks like someone's daughter. She smiles at herself — nervous, encouraging. "You can do this." She brushes her teeth, says a prayer, and goes to sleep at 9pm.

**Mirror 2 — Day 20:**
She's getting ready for the bar. She stops. The dress Jolene bought. Mascara she didn't own two weeks ago. Her hair is down. She tilts her head, studying herself like she's looking at a stranger. Something is different and she can't name it. It's in her eyes — they're not wider, they're *sharper*. She doesn't say a prayer. She finishes her wine and goes downstairs.

**Mirror 3 — Day 40:**
Morning. She stands in her underwear. She doesn't flinch — she used to flinch. She looks at her body the way she's learned men look at it. She turns. She knows what Ray's hands feel like on her hips. She knows what Tom's face looks like when she tells him what to do. She knows what Mark's text will say before she reads it. She doesn't feel guilt. She feels a thrum of something that might be power. She doesn't pray anymore. She can't remember the last time she did.

**Mirror 4 — Day 60:**
Night. She's getting ready for Jake. She looks at herself and doesn't recognize the girl who arrived with a cardigan and a Bible. It's not the clothes — it's the eyes. The way she holds her shoulders. The tilt of her chin. The girl with the Bible would be horrified. She smiles. The smile isn't kind. It isn't cruel either. It's the smile of someone who knows exactly what she wants and has learned exactly how to get it. She turns off the light and goes downstairs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: NPC DEFINITIONS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### CATALYST NPC: JOLENE — The Landlady

**NPC ID**: `npc_jolene`
**Role**: Non-romantic corruption catalyst (Phase 1) + ongoing mentor (Phase 2)
**Core Traits**: `{ mentorship = 0 }` — tracks depth of mentoring relationship (0 → 100)
**Note**: Jolene is NOT a seduction target. Corruption influence is tracked on the *player's* `corruption` trait, not on Jolene. The `mentorship` trait is used for narrative gating only (e.g., unlock later advice/shopping events).

---

#### Physical Appearance

Full-figured, unapologetic about it. 5'7", soft curves, sun-freckled shoulders. Auburn hair that she wears loose and wild. Laugh lines around her eyes that she calls "proof of a good time." Her hands are rough from bar work — strong grip, calluses, nails painted red and chipped.

Mornings: silk robe over nothing, barefoot, cigarette dangling, coffee in her other hand. She looks like a painting someone's mother would disapprove of.
Bar hours: low-cut top, jeans that fit, boots. Practical but she knows what she looks like. She didn't buy those jeans for comfort.
Late night: back to the robe, or a men's flannel shirt over underwear if she's had company.

What makes her compelling: she doesn't perform attractiveness — she inhabits it. She's 42 and moves like a woman who stopped apologizing for her body twenty years ago. The confidence is magnetic. Emma has never met anyone who treats their own sexuality with such casual certainty.

---

#### Personality Traits

**Surface**: Loud, direct, profane. She says "fuck" like punctuation. She'll tell you your ass looks great and ask about your mother in the same sentence. People who don't know her think she's trashy. People who do know her would die for her.

**Hidden**: Observant. Emotionally intelligent in ways that surprise people. She knew Emma was sheltered within ten minutes of meeting her. She knew why within twenty. She knows everyone's secrets in Millfield because she's the bartender and because she *listens*. Underneath the bravado is a woman who was Emma once — before two bad marriages and twenty years of learning not to give a shit what people think.

---

#### Psychology

Jolene married at 20 because that's what you did in Millfield. First husband was boring and she was bored. Left him at 25. Married again at 28 — this one hit. Left him at 31 with a bruise on her jaw and a bar she'd put the deposit on in her own name. She's been single since, by choice, and she's the happiest person Emma has ever met.

She sees Emma and recognizes the wound: a young woman who has been taught that desire is shameful, that her body is a problem to manage, that "good girls" don't want things. Jolene's corruption of Emma isn't malicious — it's liberation. She's giving Emma permission to be a person with appetites. She's the mentor who says "there's nothing wrong with you" at the exact moment Emma needs to hear it.

Her one vulnerability: loneliness she won't admit to. The bar is full every night but she goes to bed alone. She's built a life she loves but sometimes, at 2am, she wonders if the second marriage broke something she can't fix.

---

#### Speech Patterns

Direct. Short sentences. No qualifiers. She doesn't say "I think maybe you should consider" — she says "Do it." Her affection shows through nicknames (hon, sugar, girl) and blunt wisdom that sounds like jokes but isn't.

**Early**: "You're wound tighter than a banjo string, sugar. When's the last time you did something that wasn't in the Bible?"

**During corruption**: "That feeling in your stomach right now? That's not guilt. That's want. Learn the difference."

**As mentor**: "That man won't notice you until you stop asking permission to be noticed. Walk in there like you own the place. Because, honey, you do."

---
---

### NPC 1: TOM — The Deputy

**NPC ID**: `npc_tom`
**Primary Driver**: CORRUPTION (stat: `devotion`)
**Secondary Stat**: None — Tom's dynamic is single-axis. His devotion is the only metric that matters because once he's devoted, he's devoted completely.

---

#### Physical Appearance

Tall — 6'1", athletic but not bulky. Built from running and the occasional weight set in the station's back room. Sandy blond hair, clean-cut — he gets it trimmed every three weeks because his mother told him neat hair shows respect. Blue eyes, strong jaw, the kind of face that's handsome in an uncomplicated, yearbook-photo way. No tattoos, no piercings, no scars. He looks like exactly what he is: a small-town golden boy.

Mornings: crisp khaki deputy uniform, polished boots, badge centered. He looks like a recruitment poster. The uniform is a little tight across the shoulders — he's outgrown it but hasn't bought a new one.
Off duty: jeans, a flannel or plain t-shirt, sneakers. He dresses like his dad. No style instinct whatsoever. The plainness is part of the appeal — she gets to imagine what's underneath without any help from him.

What makes him physically attractive: the obliviousness. He doesn't know he's good-looking. He doesn't flex, doesn't pose, doesn't angle his jaw. When he blushes — and he blushes constantly around Emma — the red spreads from his neck to his ears. His hands are large and he doesn't know what to do with them when she's nearby. The appeal is that this body has never been commanded by someone who knew what they were doing.

---

#### Personality Traits

**Surface**: Polite, earnest, eager to help. He holds doors, calls women "ma'am," tips 25% at the diner. He volunteers for every event, coaches kids' soccer, and has never once told someone to go fuck themselves even when they deserved it. People like him. Nobody is intimidated by him.

**Hidden**: Deeply insecure about his lack of experience — with women, with the world, with anything beyond Millfield's borders. He became a deputy because his dad was sheriff, not because he chose it. He's never left the county. He's never been drunk, never been in a fight, never been naked with another person. He suspects he's the only 25-year-old virgin in America and the shame is constant, low-level, and never discussed.

---

#### Psychology

Tom was raised by a single father (his mother left when he was seven — she's somewhere in California, sends a card at Christmas). His dad was a good man, a good sheriff, and a terrible communicator. He taught Tom to be useful, respectful, and quiet. He did not teach Tom how to talk to women, how to recognize desire, or how to understand his own body.

Tom has a crush on Emma from the moment she arrives. It's immediate, physical, and completely paralyzing. He can't look at her without his brain short-circuiting. He's had crushes before — on teachers, on the girl at the diner, on women who passed through town — but they were abstract, safely impossible. Emma is HERE, she's his age, she smiles at him, and he has no idea what to do with any of it.

He wants someone to choose him. His mother didn't. His crushes never knew he existed. When Emma starts paying attention to him, it's the most significant thing that's ever happened to him. He'd do anything to keep it.

---

#### Internal Contradictions

1. **He wants Emma — but he doesn't know what "wanting" means.** His sexuality is almost entirely unexplored. He's masturbated, felt shame about it, and never discussed it with anyone. When Emma touches his arm, his body responds and his mind panics. He wants something he doesn't have the vocabulary for.

2. **He wants to be the protector — but she's the one in control.** His identity is "the deputy" — the guy who keeps people safe. With Emma, he's helpless. She leads every interaction. He follows. Part of him loves being led. Part of him is terrified by how much he loves it.

3. **He wants to be good — but she's teaching him to want things that "good boys" don't want.** His father raised him to be respectful, keep his hands to himself, never pressure a woman. Emma is dismantling those rules one by one. She's putting his hands where she wants them. She's telling him it's okay. He believes her, and each time he does, the boy his father raised gets a little smaller.

---

#### Resistance Pattern

| Stage | Resistance Behavior | What Triggers It |
|-------|-------------------|-----------------|
| MILD | Freezes. Goes completely still — doesn't pull away but doesn't respond. Stammers. "I, uh— I should probably—" Finds a reason to look at his shoes. | After any physical contact that registers as sexual. His body responds but his brain hasn't caught up. |
| MODERATE | Avoids her for 1-2 days. Takes shifts that keep him away from the bar and the school. If she texts, he responds hours later with something neutral: "Hey, sorry, busy day." He's not angry — he's overwhelmed and processing. | After a gate-unlocking event. He felt something he's never felt before and needs time to absorb it. |
| SEVERE | Doesn't exist. Tom has no severe resistance. He doesn't have the emotional infrastructure to push back hard. His worst response is silence + distance, never confrontation. This is part of his vulnerability and part of what makes corrupting him morally weighted — he CAN'T say no to her. | — |
| RECOVERY | He shows up. That's it. He just appears — at the diner, at the school, wherever she is. He doesn't have the words to explain what happened. He just needs to be near her again. If she smiles at him, the recovery is instant. | After any amount of time. He always comes back because he has nowhere else to go emotionally. |

---

#### Emotional Quadrant Behaviors

**Note**: Tom's quadrant is adapted — his "trust" axis is replaced by "awareness" (how much he understands about what's happening between them). His devotion only goes up; his awareness is what changes the texture.

| Quadrant | Tom's Specific Behaviors |
|----------|--------------------------|
| **LOW DEVOTION / LOW AWARENESS** (early game) | Stammers when she enters the room. Drops things. Can't complete a sentence if she's looking at him. Stands too far away, then too close, then too far away again. Laughs at things that aren't funny because he doesn't know what else to do. "Hey, Miss— uh, Emma— I mean, hi." |
| **HIGH DEVOTION / LOW AWARENESS** (mid-game, pre-sexual) | Follows her like a moon in orbit. Shows up wherever she might be, pretending it's coincidence. Brings her things — a coffee, a muffin, a wildflower he found on patrol. Stares when she's not looking. Turns scarlet when she catches him. Has no idea she's doing this on purpose. "I just happened to be in the area." (The school is not in his patrol area.) |
| **HIGH DEVOTION / HIGH AWARENESS** (post-sexual gates) | He KNOWS what they are now. The puppy-love behavior shifts to quiet, intense devotion. He stops stammering — not confident, but certain. He looks at her like she invented sunlight. He does whatever she asks without hesitation. "Yes" and "okay" and "tell me what you want." He's hers and he knows it. The awareness makes him better, not worse — he's learning. |
| **DEVOTED-ASSET** (late game) | He's not just a lover — he's a tool. She asks him to "forget" he saw her with Ray. He does. She asks him to make sure the parking lot is empty when Mark comes by. He does. She asks him to lie. He lies. His devotion has transcended the sexual into total compliance. He'd do anything. Anything. "Whatever you need." |

---

#### Emotional Tells by Stat Range

**Primary Stat — devotion (npc_tom):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-20 | Classic crush behavior. He's at the diner when she is — "coincidence." He straightens his uniform when he sees her. He overreacts to everything she says: she mentions it's cold, he appears with his jacket. Transparent but harmless. |
| 21-40 | He starts making excuses to be around her. Offers to "check her locks" again. Volunteers for school events he'd never attend. He's building his life around her schedule. He brings her coffee exactly the way she likes it without asking. He remembered. |
| 41-60 | Physical tells emerge. He leans toward her when she talks. His breathing changes when she touches him. He mirrors her body language unconsciously. When she says his name, he holds completely still — like a dog hearing a command. |
| 61-80 | He waits. Not in the creepy sense — in the devoted sense. He's where she needs him before she asks. He covers for her at church when the ladies ask questions. He tells small lies for her without being asked. His eyes follow her across any room. |
| 81-100 | Complete devotion. He says her name like a prayer. He doesn't question anything she asks. If she says "come here," he comes. If she says "wait," he waits. The nervousness is gone — replaced by something calm and absolute. He's found his purpose. She's it. |

---

#### Speech Patterns

**Early (devotion 0-30)**: Broken. Fragmented. He starts words and abandons them. "You look— I mean, your dress— it's, uh— I like your..." [trails off, ears red]. Sentences rarely complete themselves. The silence between words does more communicating than the words.

**Mid (devotion 31-60)**: He can speak in her presence now — but barely. Short, earnest sentences. "I brought you coffee. Two sugars, right?" "I was hoping you'd be here." He's brave enough to say small true things. Not brave enough for big true things yet.

**Late (devotion 61-100)**: Quiet certainty. He doesn't need to say much. "Yes." "Okay." "Whatever you want." When he does speak more, it's devastating in its simplicity: "I've never felt like this. About anyone. I didn't know I could." He doesn't stumble anymore. She's given him permission to exist, and he exists in her direction.

---

#### Starting Stats

| Stat | Value |
|------|-------|
| `devotion` (Tom) | 0 |

---
---

### NPC 2: RAY — The Handyman

**NPC ID**: `npc_ray`
**Primary Driver**: SEDUCTION (stat: `interest`)
**Secondary Stat**: None explicitly tracked — but Ray has a hidden narrative mechanic: if his `interest` exceeds 80, he begins developing real feelings, which creates an unplanned complication. This isn't stat-tracked — it's story-triggered.

---

#### Physical Appearance

Solid — 5'11", 200lbs, the build of a man who lifts things for a living, not for a mirror. Broad shoulders, thick forearms corded with veins. Weather-darkened skin — deep tan from years of outdoor work. Dark brown hair going grey at the temples, cut short and practical. Brown eyes with crow's feet from squinting in sunlight. Calloused hands. A small scar across his left knuckle from a saw accident. He looks older than 44 and doesn't care.

Working: worn jeans, work boots, a faded t-shirt or no shirt depending on heat. Sawdust on his forearms. Sweat on his neck. He looks like physical labor, and it suits him.
At the bar: same jeans, a clean flannel, the boots. He doesn't dress up. He doesn't have "going out" clothes. The lack of effort is part of the appeal — he is who he is regardless of context.

What makes him physically attractive: competence. His hands move with certainty. He swings a hammer, tightens a bolt, lifts a beam like each motion has been done ten thousand times. There's no wasted movement. The physical confidence of a man who trusts his body is fundamentally different from gym vanity — it's quieter and more magnetic. When he finally looks at Emma with those sun-squinted eyes and actually *sees* her, it hits different because he's so rarely moved by anything.

---

#### Personality Traits

**Surface**: Quiet. Economical with words and emotion. He answers questions with the minimum required words. Not unfriendly — just efficient. People mistake his quietness for dullness. He's not dull. He just doesn't see the point of saying something unless it needs to be said.

**Hidden**: Lonely. His daughter lives with his ex two towns over and he sees her every other weekend. He drinks at Jolene's bar every evening not because he likes drinking but because the alternative is an empty house. He notices more than he lets on. He watches people the way a man who fixes things watches things — looking for what's broken, what needs attention, what's about to fail.

---

#### Psychology

Ray married young, had a daughter, and watched the marriage die slowly from mutual disinterest. The divorce was amicable — no drama, no fighting, just two people admitting they'd stopped trying. He got the house. She got the kid. He told himself it was fair. It wasn't, and the wound is still there, buried under competence and quiet.

He doesn't date. Not because he can't — women in Millfield have tried — but because he's decided that particular type of vulnerability isn't worth the risk. His emotional stance is: I can fix a roof, I can fix a truck, but I can't fix a relationship, so I'll stop trying.

When Emma arrives, he registers her as "the new schoolteacher" and files her under "not my business." She's 23. She's practically a child. She's a nice kid. He means this genuinely and without condescension — she simply doesn't exist in his sexual awareness. That's the wall she has to break.

What scares him: feeling something. His indifference to Emma isn't strength — it's protection. When she finally forces him to see her as a woman, the wall doesn't crumble gracefully. It shatters. And what's behind it is a 44-year-old man who hasn't been wanted in years and doesn't know how to handle being wanted by someone like her.

---

#### Internal Contradictions

1. **He doesn't want to want her — but his body decides before his mind does.** He's spent years telling himself he's past this. Relationships are done. Women are fine but not necessary. Then she presses against him in the shed and his body answers before his brain can object. The contradiction is: his identity is "man who doesn't need anyone" and she's proving that identity is a lie.

2. **He thinks she's too young — but that's what makes it electrifying.** Every rational reason to stay away (she's 23, she's the teacher, people will talk) is also what makes the attraction feel forbidden and vital. He feels alive with her in a way he hasn't felt in a decade. The age gap that should be a barrier is actually part of the charge.

3. **He wants to keep it physical — but she makes him feel things.** He can handle sex. Sex is mechanics — he's good at mechanics. What he can't handle is the way she looks at him after, or the way she asked about his daughter, or the fact that she brought him a beer and sat on his tailgate and made him laugh. She's supposed to be a fling. She's becoming more than that, and it terrifies him.

---

#### Resistance Pattern

| Stage | Resistance Behavior | What Triggers It |
|-------|-------------------|-----------------|
| MILD | Doesn't exist in the traditional sense. His "mild resistance" is simply *not noticing*. She can stand next to him, touch his arm, wear the dress — he genuinely doesn't register it. This isn't a wall he's built; it's a category she doesn't fit. | Default state. She doesn't exist in his sexual awareness yet. |
| MODERATE | After she breaks the frame: he pulls back into formality. "Miss." "Ma'am." Re-establishes the distance she just demolished. Finds work to do somewhere she isn't. Not coldly — almost confused, like he's trying to re-file her into the old category and it won't fit anymore. | After the first crack — he notices her body and the noticing disturbs him. |
| SEVERE | Blunt, honest, not cruel. "This is a bad idea. You know that." He looks her in the eye when he says it. He means it. He also can't stop looking at her mouth while he says it. The honesty IS the resistance — he names what's happening because naming it is his last defense against it. | After the first physical escalation. He kissed her (or she kissed him) and he's trying to undo it with words. |
| RECOVERY | He shows up. Not with flowers or an apology — with himself. He's at the bar. He fixes something near her room. He leaves his truck parked where she can see it. The message is wordless: "I'm here. I couldn't stay away." When she approaches, he doesn't say much. He just looks at her and exhales like he's been holding his breath. | After 1-2 days. He doesn't have the capacity for extended emotional distance. He's too honest for games. |

---

#### Emotional Quadrant Behaviors

**Note**: Ray's "trust" axis is "emotional investment" — how much he's let himself care beyond the physical.

| Quadrant | Ray's Specific Behaviors |
|----------|--------------------------|
| **LOW INTEREST / LOW INVESTMENT** (default state) | Polite. Functional. "Evening, Miss." He holds the door because it's what you do, not because it's her. Orders his drink, sits at his spot, reads the paper or watches the game. She could be wallpaper. He's not being rude — she literally doesn't register. |
| **HIGH INTEREST / LOW INVESTMENT** (she's broken the frame but he's fighting it) | He's rattled. She catches him looking and he looks away — fast, almost angry. He grips his beer tighter when she sits nearby. His jaw works. He leaves earlier than usual. When she talks to him, his answers are shorter than they need to be. He's aware of her in the room the way you're aware of a match near gasoline. |
| **HIGH INTEREST / HIGH INVESTMENT** (post-sexual, feelings developing) | Dangerous territory. He starts doing things for her that aren't asked for. Her room's faucet is fixed before she mentions it. He saves a barstool for her. He looks at her differently — not just with heat, but with something softer that he'd deny if you named it. He asks questions: "You eat yet?" "You walking home alone?" Protective impulses he can't explain. |
| **FULLY INVESTED** (rare, late-game complication) | He tells her about his daughter unprompted. Not the surface version — the real one. How he cries in his truck after dropping her off. How he's afraid he's going to miss her growing up. He's let Emma into the part of himself he keeps locked. If she handles it well, the depth of his attachment becomes a narrative complication. If she handles it carelessly, it becomes a crisis. |

---

#### Emotional Tells by Stat Range

**Primary Stat — interest (npc_ray):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-20 | "Evening, Miss." Period. He acknowledges her existence the way he'd acknowledge a change in weather — briefly, without consequence. Doesn't look up from his drink when she enters. |
| 21-40 | He looks. That's the entire shift, but it's seismic for Ray. He watches her cross the bar. His eyes follow her when she sits down. He doesn't approach, doesn't speak, but he's *tracking* her now. When she catches his eye, he holds it for one beat before looking away. |
| 41-60 | He speaks first. This never happens. "Whiskey tonight?" He remembers what she drinks. He angles his body toward her. When she tells a story, he listens — really listens, not just waiting for his turn. He laughs at her jokes — a low, surprised sound, like he forgot he could do that. |
| 61-80 | Physical proximity shrinks. He stands close enough that she can smell sawdust and soap. His hand finds her lower back when they walk to the parking lot. He fixes things in her room without being asked and without mentioning it. He shows up at the bar earlier when he knows she'll be there. |
| 81-100 | He's in trouble and he knows it. He says her name — "Emma" — instead of "Miss." The first time he does it, they both notice. He lingers after the bar closes. He tells her things: about his daughter, about his marriage, about the house being empty. He's not performing vulnerability — he's unable to contain it anymore. The stoic man is leaking. |

---

#### Speech Patterns

**Early (interest 0-30)**: Minimal. Subject-verb-period. "Beer's cold." "Fence needs work." "Evening." He speaks to communicate facts, not feelings. Silence is his native language. A 10-word sentence from Ray is a speech.

**Mid (interest 31-60)**: He starts offering more. Still short, but with texture. "Didn't take you for a whiskey girl." "You're not what I expected." A rare dry joke: "You keep showing up, people are gonna talk." The humor is quiet and the pauses between sentences are long. When he says something real, he looks at the bar, not at her.

**Late (interest 61-100)**: Full sentences. Sometimes two in a row. "I was married for twelve years. I don't think about it much anymore. I'm starting to think about other things." His voice drops lower when they're alone — not intentionally, just physiologically. When he says "this is a bad idea," the roughness in his voice makes it sound like the opposite. He starts sentences with her name: "Emma." Then a pause. Then the thing he's been working up the courage to say.

---

#### Starting Stats

| Stat | Value |
|------|-------|
| `interest` (Ray) | 0 |

---
---

### NPC 3: MARK — The Student's Father

**NPC ID**: `npc_mark`
**Primary Driver**: FORBIDDEN (stat: `desire`)
**Secondary Stat**: `guilt` — not a traditional secondary stat. It's a manipulation mechanic. High guilt makes him desperate (comes back harder after pulling away). Low guilt makes him available but boring (the forbidden thrill dies). Emma must keep him in the sweet spot.

---

#### Physical Appearance

Handsome in a suburban, non-threatening way — 5'10", fit from a gym routine he maintains out of duty, not vanity. Dark hair with early grey at the temples. Clean-shaven jaw, straight nose, brown eyes that crinkle when he smiles. He looks like a man from a catalog — good-looking enough to notice, bland enough to be safe. That blandness is the point: underneath it is a man who is screaming.

School events: pressed khakis, a button-down with the sleeves rolled once (his one rebellion). He smells like department store cologne and the leather interior of his Volvo.
Casual: polo shirt, jeans that fit well. He looks like he's about to go to brunch or a PTA meeting. He is always about to go to brunch or a PTA meeting.

What makes him physically attractive: the hunger behind the wholesome surface. When Emma looks at him a beat too long, something behind his eyes — something Karen doesn't see anymore — wakes up. He doesn't preen or pose. He just... focuses. On Emma. With an intensity that says: *you're the first person who has looked at me like a man instead of a function in years.* The appeal isn't his body. It's his desperation, and how hard he's trying to hide it.

---

#### Personality Traits

**Surface**: Responsible. Dependable. Community-oriented. He coaches little league, chairs the fundraiser committee, shakes hands at church. Everyone in Millfield likes Mark. He is the definition of reliable. He has never had an interesting conversation at a dinner party in his life.

**Hidden**: Hollow. His marriage died years ago — they just forgot to bury it. Karen sleeps in the other bedroom. They haven't had sex in months. They don't fight because fighting requires caring enough to fight. He goes through each day performing the role of Mark-the-good-husband, Mark-the-good-father, Mark-the-good-citizen, and at 2am he lies awake wondering if this is all there is and the answer is always yes and the ceiling never answers back.

---

#### Psychology

Mark married Karen at 26 because she was pretty, his mother approved, and it was time. They had a son — Tyler — who is the only genuinely alive thing in Mark's world. He loves that kid with a ferocity that surprises even him. Everything else — the job, the marriage, the house, the routine — is infrastructure for Tyler's childhood. Mark doesn't live. He maintains.

He didn't intend to notice Emma. Parent-teacher conference, that's all. But she looked at him — not at "Tyler's father" or "Karen's husband" — at *him*. She asked a question and actually waited for the answer. She laughed at something he said and the sound did something to his chest. He went home and couldn't sleep.

He's not a predator and he's not looking for an affair. He's a man dying of thirst who's just been shown a glass of water, and the fact that the water is his son's teacher makes everything worse and more intoxicating at the same time.

What terrifies him: being discovered. Not the confrontation — the *revelation*. If Karen finds out, his son finds out. If his son finds out, he's not "Dad" anymore. He's "the dad who cheated with my teacher." Every escalation with Emma requires him to accept a little more risk to the only thing he actually loves. That's the real cost, and Emma controls the dial.

---

#### Internal Contradictions

1. **He wants Emma — but wanting her means being the man he promised himself he'd never be.** He's watched other men cheat. He's judged them. He told Karen he'd never be that guy. Now he's sitting in a school parking lot at 10pm texting his son's teacher things he'd never let Karen read. The contradiction between who he IS and who he SWORE he was is eating him alive.

2. **He wants to leave Karen — but he can't, because of Tyler.** The marriage is dead. He knows it. But divorce means custody battles, a broken home, Tyler shuffling between apartments. He stays in the corpse of his marriage for his son, which means every encounter with Emma is stolen from a cage he chose to stay in. The cage makes the escape sweeter. It also makes the guilt worse.

3. **He wants Emma to understand what she's risking — but he also wants her to not care.** Part of him needs her to see the weight of what they're doing: the family, the career, the town. Part of him — the hungry part — needs her to look at all of that and say "I don't care. I want you anyway." Her willingness to burn it all is terrifying and the most desired thing he's ever experienced.

---

#### Resistance Pattern

| Stage | Resistance Behavior | What Triggers It |
|-------|-------------------|-----------------|
| MILD | He overperforms normalcy. "So, Tyler's grades..." He steers every conversation back to his son, the school, the fundraiser. He laughs too loudly at nothing. He stands up when she gets too close. He checks his phone — "Karen just texted, I should head out." | After any charged moment. He's not pulling away from Emma — he's pulling back into the safe identity of "responsible father." |
| MODERATE | He cancels. "Something came up with Tyler." (Nothing came up with Tyler.) He doesn't come to the conference. He doesn't volunteer for the fundraiser. Radio silence on texts for 2-3 days. He's at church with his arm around Karen, performing the marriage harder than usual. | After a gate-unlocking event. He crossed a line and is trying to pretend it didn't happen. |
| SEVERE | Guilt explosion. "What are we doing? I have a son. He sits in YOUR classroom." He paces. His hands shake. He might cry. He says "this has to stop" and means it — in that moment, he truly means it. He looks at her like she's the most beautiful and terrible thing in his world. | After a near-discovery. Karen found a text. Someone saw them. The fantasy collided with reality. |
| RECOVERY | He breaks. After 3-5 days of absence, he shows up. Not at the school — at her door, at night. "Karen thinks I'm at a meeting." He doesn't have a speech. He just stands there, shaking, and the fact that he came back says everything. He chose the risk. Again. | After the guilt metabolizes. He can't stay away because the alternative — going back to feeling nothing — is worse than the fear. |

---

#### Emotional Quadrant Behaviors

**Note**: Mark's quadrants are defined by `desire` (primary) and `guilt` (secondary/manipulation stat).

| Quadrant | Mark's Specific Behaviors |
|----------|--------------------------|
| **LOW DESIRE / LOW GUILT** (baseline, pre-attraction) | Generic parent mode. "Thanks for looking after Tyler." Firm handshake, appropriate eye contact, leaves when the meeting's over. She's his son's teacher. Period. |
| **LOW DESIRE / HIGH GUILT** (rare — early guilt from noticing her) | Avoids her. Over-attends to Karen in public. Holds Karen's hand at school events with desperate, performative affection. Can't look at Emma without looking away immediately. His conscience is overreacting to an attraction that hasn't even fully formed. |
| **HIGH DESIRE / LOW GUILT** (mid-game, after guilt has been managed down) | Dangerous calm. He shows up relaxed, confident. He's accepted what he's doing. The texts are warm, the visits are regular, the excuses to Karen are practiced. He smiles at Emma across the classroom like he has a secret — because he does. This is where the affair becomes routine, and routine is where people get careless. |
| **HIGH DESIRE / HIGH GUILT** (the explosive combination) | The most volatile version of Mark. He wants her with a desperation that physically hurts and he HATES himself for it. He shows up at her door having clearly been crying. He fucks her like it's the last time and then stares at the ceiling and says nothing for ten minutes. He texts her "We need to stop" at midnight and "I miss you" at 12:04. He brings Tyler to the bar for dinner so he can see Emma in public and the guilt of his son sitting between them makes him want to throw up and also never leave. |

---

#### Emotional Tells by Stat Range

**Primary Stat — desire (npc_mark):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-20 | Polite parent mode. Makes eye contact during the conference and breaks it appropriately. Shakes her hand on arrival and departure. Mentions Karen naturally. She's wallpaper — pleasant wallpaper, but wallpaper. |
| 21-40 | He lingers. The conference ends but he doesn't stand up. He asks questions about Emma — "Where did you go to school?" — not Tyler. He notices what she's wearing and his eyes track her when she gets up to get a file. He laughs at things that aren't funny because her laugh makes him want to keep hearing it. |
| 41-60 | He creates reasons to be there. Volunteers for everything. "I can bring the supplies for the bake sale." "I'll stay late to help with the decorations." He texts her about school-related things that don't need texts. His messages get a little longer, a little warmer, include an emoji he'd never use with anyone else. |
| 61-80 | He's reckless. He shows up without a reason. "I was in the area." (His office is across town.) He stands too close and doesn't back up. His hand on her back when they walk through the classroom door. He texts her things he'd delete if Karen checked his phone — and he doesn't delete them. He wants evidence that this is real. |
| 81-100 | He's lost. He says things he can't unsay. "I think about you constantly." "I haven't felt like this since I was twenty." "She doesn't make me feel anything." He looks at Emma like she's the last real thing in a life made of cardboard. He's ready to destroy everything — and the worst part is, he knows it and he's choosing it. |

**Secondary Stat — guilt (npc_mark):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-10 | He's compartmentalized perfectly. Emma is one box. Karen is another. He can sit at church with his family on Sunday and text Emma on Monday without flinching. This is the functional affair state — smooth, managed, sustainable. |
| 11-20 | Small cracks. He flinches when Tyler mentions "Miss Emma" at dinner. He spaces out during Karen's conversations. He checks his phone in the bathroom — not to text Emma, just to look at her name. The boxes are leaking. |
| 21-30 | He overcompensates. Buys Karen flowers. Takes Tyler to the park. Performs the marriage with visible effort. When he's with Emma, there are moments where his face goes blank and she can tell he's thinking about his son. The guilt doesn't stop him from coming back — it just makes the experience bittersweet. |
| 31-40 | He starts confessing. Not to Karen — to Emma. "I feel like a terrible person." "Tyler asked why Daddy seems sad." He needs her to absolve him, which gives her enormous power. If she says "you're a good man," he'll do anything. If she says "maybe we should stop," he'll panic. |
| 41-50 | Breaking point. He can't hold both worlds. He's visibly exhausted. He cancels on Emma, then cancels on Karen, then sits in his car in the school parking lot for twenty minutes staring at the steering wheel. He might confess to Karen — which is the nuclear scenario. Emma must manage his guilt below this range or risk losing the game. |

---

#### Speech Patterns

**Early (desire 0-30)**: Professional, careful. Complete sentences, proper grammar. He speaks like a man at a business meeting — nothing personal, nothing exposed. "Tyler's reading scores are excellent, thank you. Karen and I really appreciate your dedication." Sentences designed to include Karen's name as a force field.

**Mid (desire 31-60)**: The force field cracks. Karen's name appears less. His sentences get personal. "Do you like it here? Millfield can be pretty quiet." "I noticed you started coming to the bar. That's... unexpected." He pauses before saying things, choosing words carefully but choosing different words than the safe ones.

**Late (desire 61-100)**: Raw and contradictory. "I shouldn't be here." (He's here.) "We need to stop." (He doesn't stop.) "Karen doesn't—" (he can't finish the sentence because finishing it means naming what Karen doesn't do). His most honest moments are physical — he says more with his hands on her than with any sentence. When he finally speaks the truth, it's brutal: "I feel more alive in this room with you than I have in ten years of marriage. What the fuck does that make me?"

---

#### Starting Stats

| Stat | Value |
|------|-------|
| `desire` (Mark) | 0 |
| `guilt` (Mark) | 0 |

---
---

### NPC 4: JAKE — The Bartender

**NPC ID**: `npc_jake`
**Primary Driver**: DOMINANCE (stat: `power`)
**Stat Direction**: Inverted — `power` starts at 100 (he's in control) and decreases as Emma takes over. At 50, the dynamic is balanced and crackling. At 20 or below, he's fully submissive.
**No secondary stat** — the single axis of power is the entire game with Jake.

---

#### Physical Appearance

Lean, cut — 5'11", the build of a man who does pull-ups but not squats. Visible forearms, tattoo sleeve on his left arm (abstract, black ink, looks expensive), another tattoo on his ribs that shows when his shirt rides up behind the bar. Dark hair, styled with effort he pretends he didn't make. Sharp jawline, two-day stubble, brown eyes with a lazy, knowing quality. A mouth that defaults to a half-smile, like he's permanently amused by something only he's noticed.

Behind the bar: fitted black t-shirt, jeans, boots. The t-shirt is tight and he knows it. He rolls the sleeves once to show the forearms. Every detail is calculated to look uncalculated.
Off duty: similar — he doesn't have a different mode. Jake is always performing "Jake." Leather jacket in winter. The wardrobe is a costume and the costume never comes off.

What makes him physically attractive: the performance. He leans on the bar like he's posing for a photo that isn't being taken. He makes eye contact like a weapon — holds it a beat too long, then smiles like he caught you looking. He flips bottles, wipes the bar with a flourish, makes pouring a beer look like seduction. It's all surface. All packaging. And it works on almost everyone. The fantasy isn't sleeping with Jake — it's making Jake realize his entire persona is a mask, and the man underneath it wants to take orders, not give them.

---

#### Personality Traits

**Surface**: Cocky, charming, effortlessly sexual. He flirts with every woman who walks in — it's reflex, not intention. He's the guy who says "What can I get you, beautiful?" and means it as both a drink order and an offer. He's funny, quick, socially dominant. He commands the bar like a stage.

**Hidden**: Empty. The confidence is a shell around nothing. He has no hobbies, no ambitions, no close friends. He bartends because he's good at it and being good at it feeds the ego that needs constant feeding. He's slept with dozens of women and remembers almost none of them. He's not a bad person — he's a hollow one. The swagger is what he built to fill the space where a personality should be. Underneath: a man who has never been challenged, never been refused, never been seen past the surface — and doesn't know if there's anything past the surface to see.

---

#### Psychology

Jake grew up pretty. That's the whole story. Pretty boy in school, pretty guy at the bar, pretty face that gets tips and phone numbers. He never needed to develop depth because surfaces always worked. He's never had a relationship longer than two months. He's never been dumped — he always gets bored first. He's never been in love. He doesn't think about whether this bothers him because thinking about it would require a kind of self-examination he's never attempted.

When "old Emma" — the cardigan-wearing newcomer — shut him down, he filed it under "prude" and moved on. He didn't take it personally because he doesn't take anything personally. Nothing touches him. That's his armor and his tragedy.

When "new Emma" starts playing him, he doesn't recognize what's happening at first. He thinks the game is the same game it's always been — he flirts, she responds, they fuck, he wins. The dawning realization that SHE is the one playing, that his cockiness is being weaponized against him, that he's performing for someone who sees right through the performance — that's the crisis. Not sexual. Existential. She's the first person who's looked at the real Jake and said "I see you" — and the real Jake doesn't know how to handle being seen.

---

#### Internal Contradictions

1. **He wants to fuck her — but she wants to own him, and the difference is everything.** He's used to sex as conquest — his terms, his pace, his bed. Emma isn't offering that. She's offering something he's never experienced: surrender. Part of him is horrified. Part of him — a part he's never met before — is desperate for it.

2. **He needs to be in control — but control is the thing he's worst at.** The "cocky bartender" persona IS the control. It's scripts and routines he's perfected. Take the script away — make him be present, be real, respond to HER instead of performing AT her — and he's lost. The dominance flip reveals that his control was always a performance. Her control is real.

3. **He doesn't want to feel anything — but she makes him feel everything.** Emotion is Jake's kryptonite. He's structured his entire life to avoid depth: short relationships, casual sex, surface-level charm. When Emma pins his hands and tells him what to do, the physical submission unlocks an emotional vulnerability he didn't know existed. He's not just submitting his body. He's submitting the part of himself he's been hiding behind the swagger for his entire adult life.

---

#### Resistance Pattern

| Stage | Resistance Behavior | What Triggers It |
|-------|-------------------|-----------------|
| MILD | Turns up the charm. Doubles down on the cocky persona. Flirts HARDER. "Playing hard to get? I like that." He interprets her control moves as part of the game — the familiar game he knows how to win. He doesn't realize the game has changed. | Early interactions. She rejects him, laughs at his moves, flirts with other men. He reads this as foreplay. |
| MODERATE | The cockiness develops cracks. He tries his best lines and she's unmoved. He laughs nervously — Jake never laughs nervously. He starts doing things he's never done: asking her questions, remembering her answers, showing up early to be there when she arrives. He doesn't understand why he's doing this and it irritates him. | After she's flipped enough interactions that his win rate is visibly declining. He can't charm his way through her and the unfamiliarity is unsettling. |
| SEVERE | Ego crisis. He snaps. "What the fuck do you want from me?" It's not anger — it's confusion and fear. He's never been in a dynamic where he wasn't in control. The swagger drops for a second and what's underneath is raw: a man who doesn't know who he is without the performance. He might overcompensate — try to reassert dominance by being aggressive, which she shuts down instantly. | After a major power-shift moment. She does something that makes it undeniable: he's not winning. She is. |
| RECOVERY | He submits. Not dramatically — quietly. He shows up and he's... different. The lazy smile is still there but it's uncertain. He asks instead of tells. "What do you want me to do?" The first time he says it, it's tentative. The second time, it's surrender. He discovers he LIKES the question. He likes not having to perform. She's given him permission to stop pretending, and the relief is overwhelming. | After he sits with the ego crisis and realizes: the way she makes him feel — seen, commanded, freed from the performance — is better than anything the "cocky Jake" persona ever provided. |

---

#### Emotional Quadrant Behaviors

**Note**: Jake's axes are `ego` (his performance) and `submission` (her control). As `power` (Jake) decreases (shifting toward her), ego drops and submission rises.

| Quadrant | Jake's Specific Behaviors |
|----------|--------------------------|
| **HIGH EGO / LOW SUBMISSION** (default Jake, power at 80-100%) | Full performance. Leans on the bar, sleeves rolled, lazy smile locked in. "What are you drinking, gorgeous?" He winks at her. He winks at everyone. He tells a story about the last woman who couldn't resist him. He's insufferable and magnetic and completely fake. |
| **HIGH EGO / HIGH SUBMISSION** (power at 40-60% — the crackle zone) | The best version of the dynamic. He still has the swagger but it's *fraying*. He makes a cocky comment and then looks to see if she's impressed. He flirts but his eyes ask for permission. He reaches for her and hesitates — waiting for her nod. The persona and the real man are fighting for control in real time. "I could kiss you right now." [pause] "If you wanted me to." |
| **LOW EGO / HIGH SUBMISSION** (power at 10-30% — full surrender) | The performance is gone. He's quiet behind the bar. He pours her drink without the flourish. He looks at her with an expression that's not charming — it's *open*. Vulnerable in a way he's never been with anyone. He does what she says. Not because he's weak — because doing what she says is the first authentic thing he's ever done. "Tell me what you want. I'll do it." |
| **LOW EGO / LOW SUBMISSION** (rare — crisis state) | He's not submissive and he's not performing. He's just... nothing. Empty. The swagger is gone and he hasn't found anything to replace it. He stares at the bar. He pours drinks mechanically. If she approaches, he doesn't have a script. "I don't know what you want from me. I don't know what I want either." This is the void she has to decide what to do with. |

---

#### Emotional Tells by Stat Range

**Primary Stat — power (npc_jake) — descending, starts at 100:**

| Range | Observable Behavior |
|-------|-------------------|
| 100-81 | Full Jake. She doesn't exist as a challenge. He flirts on autopilot. "Hey, teach. Loosen up." He's told this joke before. To other women. With the same timing. She's interchangeable to him. |
| 80-61 | She's registered as different. He tries harder with her specifically. His flirting gets targeted — he watches what she responds to and adjusts. He leans closer when she talks. He stops flirting with other women when she's in the room — the first real behavioral change. |
| 60-41 | The flip is visible. He's nervous. Jake. Is. Nervous. He drops a glass when she sits on the bar. He laughs at her jokes louder than they deserve. He asks her opinions: "What do you think of this song?" He's never asked anyone's opinion. He waits to see her reaction before he reacts. She's become the mirror he checks himself against. |
| 40-21 | Surrender in progress. He follows her with his eyes whenever she moves. He waits for instructions — not explicitly, but he's hovering, ready. She says "come here" and he comes. No delay. No quip. She says "not yet" and he stops mid-motion. His body has learned to respond to her voice before his brain processes the words. |
| 20-0 | Complete submission. He doesn't make decisions about them anymore — she does. Where, when, how, what he's allowed to do. He discovers this is the most peaceful he's ever felt. No performance, no charm, no scripts. Just: "What do you want?" The lazy smile is gone. What's there instead is something real. |

---

#### Speech Patterns

**Early (power 100-70)**: Polished, rehearsed, performative. Every sentence is a line. "You know, most girls warm up to me by the second drink." "I've been told I'm an acquired taste. Emphasis on taste." He speaks in winks. Everything is innuendo wrapped in confidence. Not a single genuine word.

**Mid (power 70-40)**: The lines start failing. He reaches for the script and it's not there. "You're different. I don't mean that as a line. I mean— shit, that sounds like a line." He interrupts himself. He repeats words. For the first time in his life, he can't talk his way through something. The charm is stuttering like a engine running out of fuel.

**Late (power 40-0)**: Stripped. Simple. He says what he means because he has nothing else left. "I don't know how to do this." "No one's ever made me feel like this." "Tell me what you want." The simplicity is the most genuine language he's ever produced. The man who talked for a living can finally only manage the truth. And the truth is: "I'll do whatever you say."

---

#### Starting Stats

| Stat | Value |
|------|-------|
| `power` (Jake) | 100 (fully in his control — decreases as Emma takes over) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: STAT ECONOMY DESIGN

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Multi-NPC Stat Tracking

Each NPC has an independent stat. Emma juggles all four:

| NPC | Primary Stat | Direction | Primary Driver |
|-----|-------------|-----------|---------------|
| Tom | `devotion` (Tom) | Ascending (0→100) | CORRUPTION |
| Ray | `interest` (Ray) | Ascending (0→100) | SEDUCTION |
| Mark | `desire` (Mark) | Ascending (0→100) | FORBIDDEN |
| Jake | `power` (Jake) | Descending (100→0) | DOMINANCE |

**Additional tracked stat**: `guilt` (Mark) (0-50, manipulation mechanic)

### Player Stat Growth

| Source | Stat | Gain | Frequency | Notes |
|--------|------|------|-----------|-------|
| Jolene Phase 1 events | `corruption` | +1 to +5 | One-time per event | 10 events, ~16 total corruption |
| Successful seduction move (any NPC) | `corruption` | +1 | Per move | Slow drip from activity choices |
| NPC gate unlock events | `corruption` | +3 to +5 | One-time per gate | Major jumps at milestones |
| Successful bold choice | `confidence` | +1 to +3 | Per activity | Higher for harder NPCs |
| Ray scenes (doubled) | `confidence` | +2 to +6 | Per activity | Ray treats her as a woman — accelerator |
| Jolene mentoring | `confidence` | +1 | Per visit | Slow but safe |
| Humiliation / rejection | `confidence` | -2 to -5 | Per event | Failing with Ray or Jake |
| Getting caught / near-miss | `confidence` | -1 to -3 | Per event | Depends on severity |
| Church attendance | `reputation` | +3 | Weekly (Sunday) | Mandatory for survival |
| School events / PTA | `reputation` | +2 to +4 | 1-2x per week | Time cost vs reputation gain |
| Volunteering | `reputation` | +4 | Weekly available | Emergency reputation repair |
| Neighborly visits | `reputation` | +2 | 2x per week | Also provides gossip intel |
| Risky NPC encounter | `reputation` | -1 to -5 | Per event | Scaled by public exposure |
| Gossip circulating | `reputation` | -1 to -2 | Passive | Triggered by prior risk events |
| Bar presence (too frequent) | `reputation` | -1 | Weekly threshold | If at bar 4+ nights/week |
| Karen confrontation | `reputation` | -5 to -8 | One-time | Major crisis event |

### NPC Stat Growth (per-NPC)

| Source | Gain | Frequency | Notes |
|--------|------|-----------|-------|
| Base activity exit (non-escalating option) | +1 NPC stat | Per visit | Showing up counts |
| Suggestive/warm choice | +2 NPC stat | Per visit | Stat threshold only |
| Kiss-tier choice | +2 NPC stat | Per visit | Stat + gate flag |
| Oral-tier choice | +2-3 NPC stat | Per visit | Stat + gate flag |
| Sex-tier choice | +3 NPC stat | Per visit | Stat + gate flag |
| Minor story event | +1-3 NPC stat | One-time | Bridge events |
| Major story event (gate-setter) | +3-8 NPC stat | One-time | Key moments |
| NPC-specific story bonus | Variable | One-time | e.g., Tom's vulnerability confession +5 devotion |

**Jake inversion note**: Jake's `power` (npc_jake) *decreases* by the same amounts. An activity where Emma wins a power interaction: power -2. A gate event: power -5 to -8. When Jake reaches 0, he's fully submissive.

### Mark Guilt Economy

| Source | Guilt Change | Notes |
|--------|-------------|-------|
| Any physical escalation | +1 to +3 | Proportional to the transgression |
| Seeing Tyler after an encounter | +2 to +4 | Story-triggered |
| Karen suspicion event | +3 to +5 | Major guilt spike |
| Emma says "you're a good man" | -2 to -3 | She can absolve him — her most powerful tool |
| Emma says "we both wanted this" | -1 to -2 | Shared responsibility reduces guilt |
| Emma says "you did what you wanted" | +1 to +2 | Ownership of guilt — powerful but destabilizing |
| Time passing without contact | -1 per 2 days | Guilt naturally decays when she's not reinforcing it |

**Sweet spot**: `guilt` (Mark) 15-30. Below 15: he's too comfortable, the forbidden thrill dies. Above 30: he starts spiraling, canceling, potentially confessing to Karen.

### Player Resource Flows

| Source | Amount | Frequency | Notes |
|--------|--------|-----------|-------|
| Teaching salary | +$220 | Weekly (auto, paid Friday) | Fixed, reliable |
| Tutoring session | +$30 | Per session (Mon/Wed afternoon) | Also `reputation +1` |
| Bar shift | +$50-80 | Per shift (Evening or Night) | $50 base + $10-30 tips |
| Cafe shift | +$45 | Per shift (Sat/Sun morning) | Conflicts with church on Sunday |
| Rent | -$180 | Weekly (7-day timer) | Miss it → Jolene demands bar shifts |
| Groceries | -$25 | Every 5 days | Miss it → energy max drops -20/day |
| Bar drinks | -$5-8 | Per visit | Required for bar NPC interactions |
| Clothes (optional) | -$30-80 | Per item | Unlocks confidence-gated options |

### Target Progression (Per NPC, if actively pursued)

**Tom (CORRUPTION — easiest):**

| Day Range | devotion (Tom) | Gate Status |
|-----------|-------------|-------------|
| Day 12-16 | 0-15 | None — engineering encounters |
| Day 16-20 | 15-30 | `kiss_unlocked_tom` (~day 18-20) |
| Day 20-25 | 30-50 | `groping_unlocked_tom` (~day 23-25) |
| Day 25-28 | 50-70 | `oral_unlocked_tom` (~day 26-28) |
| Day 28-31 | 70-85 | `sex_unlocked_tom` (~day 29-31) |
| Day 31+ | 85-100 | Devotion → asset phase |

**Ray (SEDUCTION — medium):**

| Day Range | interest (Ray) | Gate Status |
|-----------|-------------|-------------|
| Day 18-24 | 0-10 | None — he doesn't notice her |
| Day 24-30 | 10-25 | Frame breaking — first crack |
| Day 30-34 | 25-45 | `groping_unlocked_ray` (~day 30-32), `kiss_unlocked_ray` (~day 32-34) |
| Day 34-38 | 45-65 | `oral_unlocked_ray` (~day 36-38) |
| Day 38-42 | 65-85 | `sex_unlocked_ray` (~day 38-42) |
| Day 42+ | 85-100 | Feelings complication zone |

**Mark (FORBIDDEN — hard):**

| Day Range | desire (Mark) | guilt (Mark) | Gate Status |
|-----------|-------------|-----------|-------------|
| Day 28-35 | 0-15 | 0-5 | None — professional flirtation |
| Day 35-40 | 15-30 | 5-12 | `kiss_unlocked_mark` (~day 38-40) |
| Day 40-44 | 30-50 | 12-20 | `groping_unlocked_mark` (~day 42-44) |
| Day 44-49 | 50-65 | 15-25 | `oral_unlocked_mark` (~day 47-49) |
| Day 49-52 | 65-80 | 20-30 | `sex_unlocked_mark` (~day 50-52) |
| Day 52-58 | 80-95 | 15-35 | Guilt management phase — Karen crisis |

**Jake (DOMINANCE — endgame):**

| Day Range | power (Jake) | Gate Status |
|-----------|-----------|-------------|
| Day 40-48 | 100-80 | None — she's rejecting/humiliating him |
| Day 48-54 | 80-60 | `kiss_unlocked_jake` (~day 52-54) |
| Day 54-58 | 60-40 | `groping_unlocked_jake` (~day 54-56) |
| Day 58-62 | 40-20 | `oral_unlocked_jake` (~day 58-60) |
| Day 62-65 | 20-0 | `sex_unlocked_jake` (~day 60-63) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: GATE FLAG DESIGN

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Per-NPC Gate Flags

Each NPC has their own 4-flag gate chain. Kissing Tom doesn't unlock kissing Ray. Each gate is set by a one-time story event specific to that NPC.

#### Tom Gate Chain

| Gate | Story Event | Approx. Day | Stat Requirement | Unlocks |
|------|------------|-------------|-----------------|---------|
| `kiss_unlocked_tom` | "The Classroom Catch" — she "trips," he catches her, she looks up and waits, he freezes, she closes the distance | Day ~18-20 | `devotion >=20`, `confidence >= 10` | Kissing/touch choices in Tom activities |
| `groping_unlocked_tom` | "Movie Night" — she invites him over, sits close, hand on his thigh, she guides his hands to her body | Day ~23-25 | `devotion >=35`, `corruption >= 20` | Groping/foreplay choices |
| `oral_unlocked_tom` | "Good Boy" — she teaches him to go down on her. Patient, commanding, explicit instruction. "Slower. Like that. Good boy." | Day ~26-28 | `devotion >=55`, `corruption >= 30` | Oral/intimate choices |
| `sex_unlocked_tom` | "First Time" — she takes his virginity. She's on top. She's in complete control. His first time is her creation. | Day ~29-31 | `devotion >=70`, `corruption >= 35` | Full sex choices |

#### Ray Gate Chain

| Gate | Story Event | Approx. Day | Stat Requirement | Unlocks |
|------|------------|-------------|-----------------|---------|
| `groping_unlocked_ray` | "The Shed" — she asks him to teach her tools, presses back against him, he goes still, she feels him respond | Day ~30-32 | `interest >=30`, `confidence >= 30` | Groping/physical choices in Ray activities |
| `kiss_unlocked_ray` | "The Staircase" — bar closes, he walks her upstairs, she stops on the second step (eye level), he breaks and kisses her hard. Pulls back: "This is a bad idea." She: "I know." | Day ~32-34 | `interest >=40`, `confidence >= 35` | Kissing choices |
| `oral_unlocked_ray` | "The Truck" — she drops to her knees in the cab of his truck after a late bar night. He doesn't expect it. He grips the steering wheel. She's in control. | Day ~36-38 | `interest >=55`, `corruption >= 45` | Oral choices |
| `sex_unlocked_ray` | "Upstairs" — he pulls her up the stairs to her room. Raw, urgent, no pretense. He knows what he's doing. She discovers what it's like with a man who knows. | Day ~38-42 | `interest >=70`, `corruption >= 50` | Full sex choices |

**Note**: Ray's groping gate fires BEFORE the kiss gate — the physical precedes the romantic. He touches her before he admits he wants to, which is consistent with his SEDUCTION driver.

#### Mark Gate Chain

| Gate | Story Event | Approx. Day | Stat Requirement | Unlocks |
|------|------------|-------------|-----------------|---------|
| `kiss_unlocked_mark` | "The Rain" — walking to his car after a late session, sharing an umbrella, she shivers against him, he almost kisses her, pulls back. First texts that night. The "kiss" is the text exchange — the physical barrier breaks through screens first. | Day ~38-40 | `desire >=25`, `confidence >= 25`, `corruption >= 40` | Charged-proximity choices in Mark activities |
| `groping_unlocked_mark` | "Under the Desk" — late classroom session, she guides his hand to her thigh under the desk. He doesn't remove it. The door is closed. Other teachers are in the building. | Day ~42-44 | `desire >=40`, `guilt <35` | Foreplay/touch choices |
| `oral_unlocked_mark` | "The First Visit" — he shows up at her door at night. "Karen thinks I'm at a meeting." She doesn't rush it. She pushes him onto the bed. She controls the pace. | Day ~47-49 | `desire >=55`, `corruption >= 50`, `guilt <40` | Oral/intimate choices |
| `sex_unlocked_mark` | "No Hesitation" — he comes back the second time. No shaking hands. No preamble. He walks in and he knows what he's here for. She lets him think he's leading. He isn't. | Day ~50-52 | `desire >=70`, `corruption >= 55` | Full sex choices |

**Note**: Mark's gates have a GUILT CEILING — if `guilt` (Mark) is too high at the time the event would fire, it delays. Emma must manage his guilt below threshold to progress.

#### Jake Gate Chain

| Gate | Story Event | Approx. Day | Stat Requirement | Unlocks |
|------|------------|-------------|-----------------|---------|
| `kiss_unlocked_jake` | "Not Yet" — bar closing, she sits on the bar, he tries to kiss her, she puts one finger on his lips. "Not yet." She allows ONE kiss on her terms — brief, her hand on the back of his neck, pulling him in then pushing him away. | Day ~52-54 | `power <=65`, `confidence >= 55` | Kissing on HER terms |
| `groping_unlocked_jake` | "Permission" — she lets him touch her but controls exactly where and how. His hands go where she puts them. When he moves them without asking, she stops. He learns. | Day ~54-56 | `power <=50`, `corruption >= 60` | Touch choices — she dictates |
| `oral_unlocked_jake` | "The Stockroom" — she takes him to the stockroom behind the bar. Jolene's in the front. Customers 20 feet away. She puts him on his knees. "Someone could walk in." "Then you'd better be quick." | Day ~58-60 | `power <=35`, `corruption >= 70` | Oral — she receives, he serves |
| `sex_unlocked_jake` | "On Her Terms" — she's on top. She pins his hands. "Did I say you could touch?" He discovers he likes not being in charge. She discovers the final form of her power. | Day ~60-63 | `power <=20`, `corruption >= 75` | Full sex — she commands |

### Player-Level Corruption Thresholds

In addition to per-NPC gates, Emma's `corruption` stat must reach certain thresholds before she can even ATTEMPT certain NPCs:

| Threshold | Unlocks |
|-----------|---------|
| `corruption >= 10` | Phase 2 begins — she notices men, can start Tom arc |
| `corruption >= 20` | Bold physical moves available (touching, leaning close) |
| `corruption >= 40` | Can begin Mark arc — requires capacity for manipulation and deception |
| `corruption >= 55` | Can begin Jake arc — requires predatory confidence |
| `corruption >= 70` | Stockroom-level risk tolerance — extreme public-exposure content |
| `corruption >= 85` | Endgame content — full transformation, no hesitation |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: COMPLETE FLAG INVENTORY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Gate Flags (Per NPC)

```
tom_kiss_unlocked
tom_groping_unlocked
tom_oral_unlocked
tom_sex_unlocked

ray_groping_unlocked
ray_kiss_unlocked
ray_oral_unlocked
ray_sex_unlocked

mark_kiss_unlocked
mark_groping_unlocked
mark_oral_unlocked
mark_sex_unlocked

jake_kiss_unlocked
jake_groping_unlocked
jake_oral_unlocked
jake_sex_unlocked
```

### Phase 1 — Jolene Corruption Flags

```
jolene_arrival_complete         # Day 1-2: Settled in, met Jolene
jolene_thin_walls               # Day 3: Heard Jolene through the wall
jolene_wine_dinner              # Day 4-5: First wine, first frank sex talk
jolene_peek_event               # Day 6: Caught Jolene mid-act through cracked door
jolene_exposure_therapy         # Day 7-8: Vibrator in bathroom, laptop "accident"
jolene_shopping_trip            # Day 9: City shopping, the dress, confidence unlock
jolene_self_discovery           # Day 10: "Figure it out" milestone (player choice)
jolene_self_discovery_refused   # Day 10: Player refused (alternate path, slower corruption)
phase_1_complete                # Day 11-12: Phase 2 unlocks, she notices men
```

### Tom Story Progression Flags

```
tom_locks_checked               # She asks him to check her locks (first excuse)
tom_classroom_setup             # She invites him to help with classroom
tom_classroom_catch             # Gate event: the "trip," the catch, the kiss
tom_movie_night                 # Gate event: his hands on her body
tom_good_boy                    # Gate event: she teaches him oral
tom_first_time                  # Gate event: she takes his virginity
tom_asset_activated             # Late game: he starts covering for her
tom_devotion_confession         # "I've never felt like this about anyone" (triggers when devotion >= 80)
```

### Ray Story Progression Flags

```
ray_first_sentence              # "Didn't take you for a whiskey girl"
ray_plumbing_excuse             # She gets him to her room to "fix something"
ray_first_crack                 # He looks. She sees him look. He looks away.
ray_truck_conversation          # Tailgate beers, real conversation, forearm touch
ray_shed_scene                  # Gate event: pressed against him in the shed
ray_staircase_kiss              # Gate event: he breaks first, kisses her on the stairs
ray_truck_oral                  # Gate event: she drops to her knees in his truck
ray_upstairs                    # Gate event: raw, urgent sex
ray_daughter_story              # He opens up about his daughter (emotional complication)
ray_feelings_emerge             # Narrative flag: interest > 80, real feelings developing
```

### Mark Story Progression Flags

```
mark_first_conference           # First parent-teacher meeting — she notices his hunger
mark_fundraiser_volunteer       # He starts inventing reasons to see her
mark_rain_umbrella              # Gate event: the rain, the almost-kiss, first texts
mark_texting_escalation         # Texts go from warm to charged to explicit
mark_under_desk                 # Gate event: his hand on her thigh in the classroom
mark_first_visit                # Gate event: he comes to her door at night
mark_no_hesitation              # Gate event: he comes back, no guilt preamble
mark_parking_lot                # She pushes the taboo — his car after hours
mark_call_from_bedroom          # She makes him call her while Karen is downstairs
karen_finds_text                # Crisis: Karen discovers a suspicious text
karen_school_confrontation      # Crisis: Karen confronts Emma at school
mark_guilt_spiral               # Trigger if guilt (Mark) > 40
```

### Jake Story Progression Flags

```
jake_initial_rejection          # "Old Emma" shot him down (pre-Phase 2)
jake_second_attempt             # He tries again, she laughs at him
jake_jealousy_game              # She flirts with other men while he watches
jake_bar_sitting                # She sits on the bar, "Pour me one more"
jake_not_yet                    # Gate event: finger on his lips, "Not yet"
jake_permission                 # Gate event: she controls where his hands go
jake_stockroom                  # Gate event: on his knees in the stockroom
jake_on_her_terms               # Gate event: she's on top, hands pinned
jake_ego_crisis                 # "What the fuck do you want from me?"
jake_surrender                  # He asks: "What do you want me to do?"
jake_endgame_choice             # Keep him as submissive OR break it off
```

### Mirror Mechanic Flags

```
mirror_day_1                    # Cardigan girl, nervous smile, prayer
mirror_day_20                   # The dress, sharper eyes, no prayer
mirror_day_40                   # Underwear, no flinch, power thrum, no guilt
mirror_day_60                   # Unrecognizable, the smile that isn't kind
```

### Utility & Survival Flags

```
game_started                    # Initial game flag
school_started                  # First day of teaching
chores_explained                # Jolene explains rent/groceries expectations
bar_shifts_available            # Jolene offers bar work (Day 8+)
cafe_job_available              # Diner offers weekend shifts
rent_last_paid                  # Timer: days_since_flag for weekly rent ($180)
groceries_last_bought           # Timer: days_since_flag for food stocking ($25/5 days)
salary_last_paid                # Timer: days_since_flag for weekly salary ($220 Friday)
food_stocked                    # True when groceries current (5-day duration)
church_attended_this_week       # Weekly reset flag
missed_school_today             # Set when player skips school on a weekday morning
```

### Economic Escalation Flags

```
rent_missed_once                # First rent miss — Jolene warns, mild consequence
rent_missed_twice               # Second miss — Jolene demands bar shifts
forced_bar_shifts               # Player must work bar until rent debt cleared
```

### School Enforcement Flags

```
school_enforcement_warned       # Principal has warned about attendance (increases skip penalty)
principal_concern_triggered_60  # Reputation < 60: "Just checking in..." conversation fired
principal_concern_triggered_45  # Reputation < 45: Active monitoring conversation fired
principal_warning_triggered_30  # Reputation < 30: Formal school board warning fired
```

### Reputation & Crisis Flags

```
principal_concern_1             # "Just checking in..." (reputation < 60)
principal_concern_2             # Active monitoring (reputation < 45)
principal_formal_warning        # School board meeting (reputation < 30)
church_gossip_mild              # Ladies mention bar visits
church_gossip_moderate          # Active whispering about "the teacher"
karen_suspicious                # Karen is watching (pre-confrontation)
karen_confrontation_complete    # Karen confronted Emma at school
karen_backed_down               # Karen accepted Emma's explanation
karen_still_watching            # Karen didn't buy it — ongoing threat
reputation_recovery_mode        # Flag to boost rep gains when in danger zone
```

### Cross-NPC Complication Flags

```
tom_saw_ray                     # Tom notices Emma with Ray at the bar
tom_covers_for_emma             # Tom agrees to look the other way (requires devotion >= 60)
ray_sees_mark_text              # Ray glimpses a text from Mark on her phone
friday_collision                # All NPCs at the bar on the same night
juggling_detected               # Any NPC suspects she's seeing others
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 2 complete. Type "proceed" to continue to Phase 3: World Design,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
