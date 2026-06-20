# NEW IN TOWN
# Complete Game Design Book

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Genre**: Adult interactive fiction with video integration
**Protagonist**: Emma (female, player-controlled), age 23
**Setting**: Millfield — small rural American town, population ~2,000
**NPCs**: Tom (deputy, 25), Ray (handyman, 44), Mark (student's father, 36), Jake (bartender, 27) + Jolene (catalyst, 42)
**Duration**: 65 calendar days (day-by-day, all playable)
**Total Canvases**: 25 activities + 50 story events = 75 total content units
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 1: FOUNDATION
# New In Town

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GAME IDENTITY

**Title**: New In Town
**Protagonist**: Emma (female, player-controlled), 23 years old
**Genre**: Adult interactive fiction with video integration
**Perspective**: Female protagonist — player IS the woman
**Theme**: Female corruption → female predator. Innocence lost, power gained.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## STRUCTURAL INNOVATION: TWO-PHASE CORRUPTION ARC

This game inverts the standard single-NPC escalation model. Instead of a male player pursuing a female NPC, a female player is FIRST corrupted, THEN becomes the corruptor of multiple male NPCs. Key structural decisions:

### Phase 1: The Corruption (Days 1-12)
- Emma is the *subject* of corruption. Jolene (female NPC, non-romantic) is the catalyst.
- No male NPC sexual content in this phase. Pure psychological awakening.
- Jolene doesn't touch Emma — she *exposes* her. Voyeurism, conversation, dares.
- Phase 1 ends when Emma's `corruption` stat crosses the threshold and she begins noticing men differently.

### Phase 2: The Hunt (Days 12-65)
- Emma becomes the *agent*. She targets 4 male NPCs, each with different psychology.
- NPCs have overlapping timelines — she's juggling multiple men simultaneously.
- Each NPC requires a fundamentally different seduction strategy (not just higher stat thresholds).
- Her internal transformation is tracked through the Mirror mechanic (Day 1/20/40/60 self-reflection).

### Multi-NPC Structure
- **4 male NPCs**, each as a distinct seduction route with unique mechanics
- **1 female catalyst NPC** (Jolene) who drives Phase 1 and serves as ongoing mentor
- **Each NPC has their own primary driver** (different resistance and escalation textures)
- **Each NPC has independent stat tracking** (4 separate NPC stats)
- **Gate flags are PER-NPC** (kissing Tom doesn't unlock kissing Ray)
- **Player-level corruption thresholds** gate which NPCs she can even attempt
- **Reputation system** creates cross-route risk — every NPC interaction can be witnessed
- **Time is the scarce resource** — 5 usable weekday slots, 4 NPCs + survival competing for attention
- **NPCs share physical spaces** — Ray and Jake are both at the bar; Tom, Mark, and Emma are all connected through the school/town. Pursuing one in front of another creates complications.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## THE CATALYST NPC: JOLENE — The Landlady

**Vibe**: Unapologetic, warm, sexually liberated. The woman who's already lived the life Emma hasn't started yet. Think "chain-smoking mentor in a silk robe who says what everyone else won't."

**What makes her compelling**: She's not a villain or a seductress. She's a 42-year-old woman who treats sex like appetite — something you satisfy, not agonize over. She sees Emma and recognizes the girl she was 20 years ago: wound tight, full of shame about natural desire. Jolene's gift isn't teaching Emma *how* to seduce — it's giving her *permission* to want.

**Role**: Non-romantic NPC. She doesn't touch Emma sexually. Her corruption method is exposure: thin walls, open doors, frank conversation, dares, and the refusal to be ashamed of anything. She's the Phase 1 engine and the Phase 2 advisor.

**Profile**:
- 42, owns The Dusty Boot (Millfield's only bar), rents the upstairs rooms
- Divorced twice — "First one was boring, second one was mean. I'm done picking."
- Chain-smokes on the porch in a silk robe. Walks around in underwear like it's nothing.
- Has men over regularly. Makes no effort to be quiet about it.
- Ran the bar for 15 years. Knows every person in town, every secret, every affair.
- Genuinely kind underneath the bluntness. Protective of Emma once she decides she likes her.

**Phase 2 Ongoing Role**: Mentor and wingwoman. Emma can visit Jolene for strategy hints ("How do I get him to...?"), NPC intel ("Ray's daughter's birthday is next week — he gets real quiet"), and confidence boosts. Jolene also controls bar access — she can assign Emma shifts (money but lost NPC time) or give her free nights (NPC access but no income).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## THE NPCs

### NPC 1: Tom — The Deputy

**Vibe**: Earnest, bumbling, painfully wholesome. The big puppy who'd follow you home if you smiled at him once. Think "small-town golden boy who has never been touched by a woman who knew what she was doing."

**What makes him appealing**: He's the opposite of a challenge — and that's the point. The fantasy isn't conquering him, it's *owning* him. He's tall, fit, objectively attractive, and completely helpless around her. Every stammer, every blush, every dropped coffee cup is proof of her effect on him. The appeal is power over someone who gives it willingly.

**Relationship**: Town deputy. He patrols Millfield, sees her around town, develops an instant crush he can't hide.

**Primary Driver**: CORRUPTION (stat: `tom_devotion`)
- She is corrupting his innocence. He's a virgin who has kissed two girls at church camp.
- He doesn't resist because he's strong — he resists because he doesn't understand what's happening until it's too late.
- No secondary driver. Pure innocence corruption.

**Driver fit**: Tom's arc mirrors Emma's Phase 1 in reverse. She was the innocent one being corrupted by Jolene. Now she IS Jolene — and Tom is the version of herself she left behind. Corrupting him is corrupting what she used to be. The driver is CORRUPTION because he's not seduced (he already wants her), he's *transformed* — from a boy who can't look at cleavage to a man on his knees saying "Good boy."

**Difficulty**: EASY — training wheels. First NPC she pursues. She's still building confidence, and Tom requires minimal skill. Every move works on him.

---

### NPC 2: Ray — The Handyman

**Vibe**: Weathered, quiet, competent. The man who fixes things and doesn't waste words. Strong hands, sun-darkened skin, eyes that have seen enough to be unimpressed by most things. Think "the guy at the end of the bar who doesn't need to perform for anyone."

**What makes him appealing**: He doesn't notice her. That's the fantasy — making the unimpressed man *impressed*. He's not playing hard-to-get. He genuinely doesn't see her as a sexual being. She's "the schoolteacher." She's "a nice kid." The appeal is shattering that frame — the moment his eyes change, when he sees her for the first time as a woman and can't unsee it.

**Relationship**: Local handyman. Does odd jobs around town, including work at Jolene's bar. Drinks there every evening.

**Primary Driver**: SEDUCTION (stat: `ray_interest`)
- She must overcome his genuine indifference. The age gap (44 vs 23), her profession, and his mental category of her as "off-limits kid" are real barriers.
- His resistance isn't moral or emotional — it's perceptual. She literally doesn't exist in his sexual awareness until she forces herself into it.
- No secondary driver. Pure seduction against indifference.

**Driver fit**: SEDUCTION because the engine is her active pursuit against his passive dismissal. He's not fighting attraction — he doesn't feel it yet. She has to create it from nothing. This is harder than Tom because charm alone won't work. She needs to reinvent how he sees her, which requires confidence, deliberate physical presence, and patience.

**Difficulty**: MEDIUM — requires confidence built from Tom. The strategies that worked on Tom (proximity, smiling, accidental touches) bounce off Ray completely. She has to learn a new approach.

---

### NPC 3: Mark — The Student's Father

**Vibe**: Handsome, hollow, respectable. The suburban dad who does everything right and feels nothing. Good jaw, pressed shirts, firm handshake. Think "the man who coaches little league on Saturday and lies awake at 2am wondering where his life went."

**What makes him appealing**: He's forbidden. He's married. He has a kid in her class. His wife is on the PTA. Getting caught doesn't just hurt Emma — it detonates a family. The appeal is the danger itself, and the power of being the thing he risks everything for. She can give him what his wife can't: desire that actually sees him, not just the role he plays.

**Relationship**: Parent of a student. Comes to parent-teacher conferences. Volunteers for school events. Their only legitimate reason to interact is his son's education.

**Primary Driver**: FORBIDDEN (stat: `mark_desire`)
- The taboo is the engine. Teacher-parent. The professional boundary, the marriage, the child between them, the PTA wife who's always watching.
- His resistance is real — he has genuine reasons to say no. Family, reputation, morality. She has to make the risk feel worth the cost.
- Secondary driver: SEDUCTION — he's not seeking an affair, she's engineering one. She must actively pursue while maintaining plausible deniability.

**Driver fit**: FORBIDDEN because the transgression itself is the escalation mechanic. Every step forward is a line crossed that can't be uncrossed. The stat isn't measuring attraction (he's attracted from the start) — it's measuring how much of his life he's willing to burn. The secondary SEDUCTION layer captures the deliberate manipulation: she creates situations, engineers proximity, and controls the pace through texting.

**Difficulty**: HARD — highest external stakes. First NPC where getting caught has consequences beyond the relationship. Karen is a persistent threat. Reputation damage is severe. Requires manipulation skills built from Tom and Ray.

**Unique Complication**: `mark_guilt` stat. She must manage his guilt like a throttle — too much and he confesses to Karen or stops coming; too little and the forbidden thrill dies. The sweet spot is: guilty enough to be desperate, not so guilty he self-destructs.

---

### NPC 4: Jake — The Bartender

**Vibe**: Cocky, tattooed, effortlessly attractive. The guy who leans on the bar and says "What can I get you, beautiful?" to every woman who walks in. Lazy smile, lean build, zero depth. Think "the man who's never had to try — and has no idea what happens when a woman stops letting him win."

**What makes him appealing**: He's the final boss — not because he's hard to sleep with (he'd fuck her tonight if she said yes), but because the game isn't sex. The game is *submission*. He's spent his life being the confident one, the pursuer, the one in control. The fantasy is making him kneel. Making the cocky guy beg. Stripping away the persona and finding the man underneath who *wants* to be told what to do.

**Relationship**: Bartender at Jolene's bar. He tried his moves on "old Emma" and got shut down. He's filed her under "prude." He has no idea what she's become.

**Primary Driver**: DOMINANCE (stat: `jake_power`)
- Power reversal. The stat tracks who controls the dynamic — starts at his 100%, shifts toward her with every interaction she wins.
- He doesn't resist sex — he resists *not being in charge*. His ego is his armor. She has to crack it, not seduce past it.
- No secondary driver. Pure power play.

**Driver fit**: DOMINANCE because the escalation isn't about getting him into bed — it's about getting him on his knees. She can fuck him any time. The game is making him WANT to submit. At 50/50 power, the dynamic crackles. At 80%+ her power, he's hers completely. The tension is: how far does she push? Does she want a partner or a possession?

**Difficulty**: ENDGAME — requires maximum `corruption` (65+) and `confidence` to even attempt. Not because he's hard to attract, but because the dominance play requires a version of Emma that doesn't exist until she's been transformed by the previous three NPCs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SETTING

**Type**: Small town — domestic + social + professional environments intersecting

**Millfield**: Population ~2,000. One main street. One bar (The Dusty Boot), one diner, one church, one school. Farming community surrounded by fields and back roads. The nearest city is 90 minutes away.

**Why this setting works**:

- **Panopticon effect** — everyone knows everyone. Gossip travels in hours, not days. Every risky move could be witnessed by someone who'll tell someone who'll tell someone. Privacy is the game's scarcest resource alongside money and time.
- **Overlapping spaces** — the bar is where Ray drinks, Jake works, Jolene lives, and Emma lives. The school is where she teaches, Mark visits, and her professional reputation exists. The church is where the whole town gathers and she performs normalcy. There's no escaping cross-contamination between her targets.
- **Economic trap** — Millfield has limited income opportunities. Teacher salary barely covers rent. The bar, diner, and tutoring are the only side jobs. She can't just "get a better job" — the town IS the economy.
- **Contrast engine** — the gap between who Emma IS (increasingly corrupted, manipulative, sexually aggressive) and who Millfield THINKS she is (sweet Christian schoolteacher) is the central tension. The smaller the town, the wider the gap, the more dangerous it becomes.
- **Isolation** — the nearest city is 90 minutes away. She can't escape to anonymity. If she wants to be someone else, she has to do it here, under everyone's nose.

**Key Locations**:

| Location | Mood | Primary NPC | Activity Type |
|----------|------|-------------|---------------|
| **School — Classroom** | Professional, tense | Mark / Solo | Teaching (mandatory), conferences, fundraiser work |
| **School — Parking Lot** | Risky, after-hours | Mark | Late-night car encounters |
| **The Dusty Boot — Bar Floor** | Social, charged, public | Ray / Jake | Drinking, flirting, bar shifts, Friday night collisions |
| **The Dusty Boot — Stockroom** | Hidden, dangerous | Jake | Secret encounters behind the bar |
| **The Dusty Boot — Upstairs (Emma's Room)** | Private, intimate | Any NPC | Inviting men over — each visit raises stakes |
| **The Dusty Boot — Jolene's Space** | Jolene's domain | Jolene | Phase 1 corruption events, Phase 2 mentoring |
| **Diner** | Public, safe, daytime | Tom | Coffee dates, weekend cafe shifts |
| **General Store** | Public, gossipy | Solo | Grocery shopping — store owner notices what you buy |
| **Church** | Performative, suffocating | Solo / Mark (visible) | Sunday reputation maintenance. Karen watches. |
| **Library** | Quiet, semi-private | Tom / Solo | Tutoring sessions |
| **Deputy Station** | Professional, small-town | Tom | Engineered visits, asking for "help" |
| **Ray's Truck / Work Shed** | Rough, private, physical | Ray | Outdoor encounters, tool lessons, truck bed |
| **Mark's Office** | Forbidden, fluorescent | Mark | Lunch visits, escalating risk |
| **Town Streets / Main Road** | Public, exposed | Any | Random encounters, being seen together |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## CORE PREMISE

**The "What If?" Hook**:

What if a sheltered, churchgoing schoolteacher moved to a small town, was corrupted by her landlady — and then discovered she *liked* having power over men? What if the sweet new teacher was the most dangerous person in Millfield, and nobody knew?

**Emotional Journey**:

Emma arrives as a genuine innocent — not performatively naive, but truly unexposed. She's never been drunk. She's had sex twice and felt guilty both times. She says "gosh." She wears cardigans to her wrists. Jolene, her landlady, cracks her open in 12 days — not through seduction, but through exposure. Thin walls, frank conversations, dares, and the simple refusal to be ashamed of desire.

Once awakened, Emma doesn't just discover sexuality — she discovers *power*. She targets four men, each requiring a different version of herself: the patient teacher (Tom), the bold woman (Ray), the manipulative temptress (Mark), the dominant predator (Jake). Each conquest teaches her something about control, risk, and who she's becoming.

The emotional core is TRANSFORMATION. The game tracks it through the Mirror mechanic — four scenes where Emma looks at herself and sees someone different each time. By Day 60, the girl with the Bible wouldn't recognize the woman in the mirror. The question the game asks isn't "how far will she go?" — it's "does she like who she's becoming?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## TONE

**Slow-burn Phase 1, escalating aggression Phase 2, with NPC-dependent pacing**

- **Phase 1 / Jolene arc (Days 1-12)**: Atmospheric, voyeuristic, internal. The narration is Emma's inner voice — shame, curiosity, the moment shame starts losing to curiosity. Sensual but not sexual. The corruption is psychological, not physical.

- **Tom arc (Days 12-30)**: Playful, experimental, gently cruel. Emma is testing her new power on someone safe. The tone is discovery — she's figuring out what she likes, what works, how far she can push. There's humor in Tom's helplessness. The cruelty is gentle — she's not hurting him, she's *enjoying* his devotion more than she should.

- **Ray arc (Days 18-42)**: Deliberate, physical, earned. The tone shifts to tension and frustration. Ray doesn't respond to charm — she has to become someone harder, more direct. When he finally sees her, the payoff is physical and raw. The narration gets blunter. Fewer thoughts, more sensation.

- **Mark arc (Days 28-58)**: Dangerous, manipulative, morally charged. The tone becomes calculating. She engineers situations, controls information, manages his guilt like a dial. There's heat in the transgression — doing it in his car, in her classroom, texting him while his wife is in the next room. The narration acknowledges she's crossing lines she can't uncross, and she doesn't care.

- **Jake arc (Days 40-65)**: Dominant, nasty, triumphant. The tone reaches its final form. She's not shy, not experimenting, not manipulating — she's *commanding*. The narration is confident, direct, almost predatory. She tells Jake what to do. He does it. The language is explicit and unapologetic.

**Overall atmosphere**: The gap between Emma's public face (sweet, wholesome, "gosh") and her private reality (increasingly dominant, sexually aggressive, manipulative) should be visible in the narration. Public scenes use softer language. Private scenes use harder language. The contrast IS the tone.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GAME SCOPE

| Element | Target | Notes |
|---------|--------|-------|
| In-game days | 65 | Day-by-day play. No time-skips. Every day is playable. |
| Locations | 14 | 3 school, 4 bar, 1 diner, 1 store, 1 church, 1 library, 1 station, 1 outdoors (Ray), 1 off-site (Mark's office) |
| NPC activities (per NPC) | 1-2 primary | Each NPC has 1 main repeatable activity + 1 secondary unlockable |
| Total NPC activities | 6-8 | Across 4 routes + Jolene mentor sessions |
| Story events (per NPC) | 6-8 | Act 1 setup (2-3), Act 2 escalation (2-3), Act 3 climax (2-3) per NPC |
| Jolene story events | 10-12 | Day-by-day Phase 1 corruption sequence |
| Shared/cross-NPC events | 4-6 | Friday night bar collisions, church sightings, reputation crises |
| Total story events | 38-46 | Per-NPC routes + Jolene + shared events |
| Utility canvases | 10-12 | Grocery shopping, rent payment, sleep, church, school events, tutoring, bar shifts, cafe shifts, volunteering, neighborly visits |
| Mirror scenes | 4 | Day 1, Day 20, Day 40, Day 60 transformation checkpoints |

### NPC Overlap Timeline

NPCs are NOT sequential — their arcs overlap. Emma is juggling multiple men at different stages:

```
Day:  1----5----10----15----20----25----30----35----40----45----50----55----60----65
      |← JOLENE PHASE 1 →|
                    |←─────── TOM: Excuse → Education → Takeover ──────→|
                         |←───── RAY: Invisible Wall → Breaking Frame → Reversal ────→|
                                            |←────── MARK: Crack → Arrangement → Fall ──────→|
                                                              |←─── JAKE: Setup → Flip → Submission ──→|
```

By Day 40, she's simultaneously: maintaining Tom's devotion, sleeping with Ray, escalating texts with Mark, and starting to toy with Jake. The schedule system makes her choose — she can't be everywhere at once.

### Daily Time Budget

| Slot | Hours | Weekday | Weekend |
|------|-------|---------|---------|
| Early Morning | 05:00-07:00 | Wake, optional jog (+10 energy) | Free |
| Morning | 07:00-09:00 | **SCHOOL (mandatory Mon-Fri)** | Free |
| Late Morning | 09:00-12:00 | **SCHOOL (mandatory Mon-Fri)** | Free |
| Afternoon | 12:00-15:00 | Free: tutoring / Tom / errands | Free |
| Late Afternoon | 15:00-17:00 | Free: Mark conferences / shopping | Free |
| Evening | 17:00-19:00 | Free: dinner / bar opens | Free |
| Night | 19:00-22:00 | Bar peak: Ray / Jake / shifts | Free |
| Late Night | 22:00-01:00 | Bar closing: highest risk/reward | Free |

**Weekday usable slots**: 5 (Afternoon through Late Night)
**Weekend usable slots**: 8 (all free, but NPCs have own schedules)

### Economic Pressure

| Income | Amount | Time Cost |
|--------|--------|-----------|
| Teaching salary | $220/week (auto) | Morning + Late Morning, Mon-Fri |
| Tutoring | $30/session | 1 Afternoon slot (Mon/Wed) |
| Bar shifts | $50-80/shift | 1 Evening OR Night slot |
| Cafe shifts | $45/shift | Morning + Late Morning (Sat/Sun) |

| Expense | Amount | Frequency |
|---------|--------|-----------|
| Rent | $180 | Weekly |
| Groceries | $25 | Every 5 days |
| Bar drinks | $5-8 | Per visit |
| Clothes (optional) | Variable | Unlocks confidence options |

**Weekly math**: $220 income - $180 rent - $35 food = $5 surplus. She is broke. Every extra dollar requires a time slot sacrifice. Every time slot at work is a time slot not pursuing an NPC.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## RECOMMENDED DIRECTION

**New In Town** is a female-corruption-to-predator adult game set in a small town where privacy doesn't exist and the sweet new schoolteacher is the most dangerous person nobody suspects.

The game's structural innovation is the **two-phase arc**: Emma is corrupted first (by Jolene, through exposure and psychological liberation), then becomes the corruptor of four men who each require a completely different strategy. Tom is conquered through his innocence. Ray is conquered through deliberate reinvention. Mark is conquered through forbidden manipulation. Jake is conquered through dominance and power reversal.

The setting is the pressure cooker. Millfield is 2,000 people who all know each other, one bar, one church, one school. Every interaction risks being seen. The `reputation` stat is the ticking bomb — it drops from risky behavior and recovers slowly. If the town figures out who Emma really is, the game ends. She has to maintain the performance of being "the sweet teacher" while privately escalating to increasingly nasty and dominant sexual encounters.

The economic squeeze ensures she can't just pursue NPCs all day. She's broke. She has to work bar shifts and tutor kids to make rent, and every hour spent working is an hour she's not with Tom, or Ray, or Mark, or Jake. The scarcity of time and money makes every choice meaningful.

The four NPCs are the differentiator. Most games in this genre feature a single seduction target. Here, Emma is running four simultaneous campaigns with overlapping timelines, competing time slots, and the constant risk that one man will see her with another. Each NPC teaches her something different about power — and each conquest makes the next one possible.

The Mirror mechanic (Day 1/20/40/60 self-reflection scenes) provides narrative structure to the transformation. The game doesn't just track stats — it shows Emma looking at herself and seeing someone new. By the end, the question isn't whether she'll succeed — it's whether she recognizes the woman she's become, and whether she likes her.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 2: CHARACTERS & STAT ECONOMY
# New In Town

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

**Role**: Non-romantic corruption catalyst (Phase 1) + ongoing mentor (Phase 2)
**No stat tracking** — Jolene is a narrative NPC, not a seduction target.

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

**Primary Driver**: CORRUPTION (stat: `tom_devotion`)
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

**Primary Stat (tom_devotion):**

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
| `tom_devotion` | 0 |

---
---

### NPC 2: RAY — The Handyman

**Primary Driver**: SEDUCTION (stat: `ray_interest`)
**Secondary Stat**: None explicitly tracked — but Ray has a hidden narrative mechanic: if his `ray_interest` exceeds 80, he begins developing real feelings, which creates an unplanned complication. This isn't stat-tracked — it's story-triggered.

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

**Primary Stat (ray_interest):**

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
| `ray_interest` | 0 |

---
---

### NPC 3: MARK — The Student's Father

**Primary Driver**: FORBIDDEN (stat: `mark_desire`)
**Secondary Stat**: `mark_guilt` — not a traditional secondary stat. It's a manipulation mechanic. High guilt makes him desperate (comes back harder after pulling away). Low guilt makes him available but boring (the forbidden thrill dies). Emma must keep him in the sweet spot.

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

**Primary Stat (mark_desire):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-20 | Polite parent mode. Makes eye contact during the conference and breaks it appropriately. Shakes her hand on arrival and departure. Mentions Karen naturally. She's wallpaper — pleasant wallpaper, but wallpaper. |
| 21-40 | He lingers. The conference ends but he doesn't stand up. He asks questions about Emma — "Where did you go to school?" — not Tyler. He notices what she's wearing and his eyes track her when she gets up to get a file. He laughs at things that aren't funny because her laugh makes him want to keep hearing it. |
| 41-60 | He creates reasons to be there. Volunteers for everything. "I can bring the supplies for the bake sale." "I'll stay late to help with the decorations." He texts her about school-related things that don't need texts. His messages get a little longer, a little warmer, include an emoji he'd never use with anyone else. |
| 61-80 | He's reckless. He shows up without a reason. "I was in the area." (His office is across town.) He stands too close and doesn't back up. His hand on her back when they walk through the classroom door. He texts her things he'd delete if Karen checked his phone — and he doesn't delete them. He wants evidence that this is real. |
| 81-100 | He's lost. He says things he can't unsay. "I think about you constantly." "I haven't felt like this since I was twenty." "She doesn't make me feel anything." He looks at Emma like she's the last real thing in a life made of cardboard. He's ready to destroy everything — and the worst part is, he knows it and he's choosing it. |

**Guilt Stat (mark_guilt):**

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
| `mark_desire` | 0 |
| `mark_guilt` | 0 |

---
---

### NPC 4: JAKE — The Bartender

**Primary Driver**: DOMINANCE (stat: `jake_power`)
**Stat Direction**: Inverted — `jake_power` starts at 100 (he's in control) and decreases as Emma takes over. At 50, the dynamic is balanced and crackling. At 20 or below, he's fully submissive.
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

**Note**: Jake's axes are `ego` (his performance) and `submission` (her control). As `jake_power` decreases (shifting toward her), ego drops and submission rises.

| Quadrant | Jake's Specific Behaviors |
|----------|--------------------------|
| **HIGH EGO / LOW SUBMISSION** (default Jake, power at 80-100%) | Full performance. Leans on the bar, sleeves rolled, lazy smile locked in. "What are you drinking, gorgeous?" He winks at her. He winks at everyone. He tells a story about the last woman who couldn't resist him. He's insufferable and magnetic and completely fake. |
| **HIGH EGO / HIGH SUBMISSION** (power at 40-60% — the crackle zone) | The best version of the dynamic. He still has the swagger but it's *fraying*. He makes a cocky comment and then looks to see if she's impressed. He flirts but his eyes ask for permission. He reaches for her and hesitates — waiting for her nod. The persona and the real man are fighting for control in real time. "I could kiss you right now." [pause] "If you wanted me to." |
| **LOW EGO / HIGH SUBMISSION** (power at 10-30% — full surrender) | The performance is gone. He's quiet behind the bar. He pours her drink without the flourish. He looks at her with an expression that's not charming — it's *open*. Vulnerable in a way he's never been with anyone. He does what she says. Not because he's weak — because doing what she says is the first authentic thing he's ever done. "Tell me what you want. I'll do it." |
| **LOW EGO / LOW SUBMISSION** (rare — crisis state) | He's not submissive and he's not performing. He's just... nothing. Empty. The swagger is gone and he hasn't found anything to replace it. He stares at the bar. He pours drinks mechanically. If she approaches, he doesn't have a script. "I don't know what you want from me. I don't know what I want either." This is the void she has to decide what to do with. |

---

#### Emotional Tells by Stat Range

**Power Stat (jake_power — descending, starts at 100):**

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
| `jake_power` | 100 (fully in his control — decreases as Emma takes over) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: STAT ECONOMY DESIGN

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Multi-NPC Stat Tracking

Each NPC has an independent stat. Emma juggles all four:

| NPC | Primary Stat | Direction | Primary Driver |
|-----|-------------|-----------|---------------|
| Tom | `tom_devotion` | Ascending (0→100) | CORRUPTION |
| Ray | `ray_interest` | Ascending (0→100) | SEDUCTION |
| Mark | `mark_desire` | Ascending (0→100) | FORBIDDEN |
| Jake | `jake_power` | Descending (100→0) | DOMINANCE |

**Additional tracked stat**: `mark_guilt` (0-50, manipulation mechanic)

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

**Jake inversion note**: Jake's `jake_power` *decreases* by the same amounts. An activity where Emma wins a power interaction: `jake_power -2`. A gate event: `jake_power -5 to -8`. When Jake reaches 0, he's fully submissive.

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

**Sweet spot**: `mark_guilt` 15-30. Below 15: he's too comfortable, the forbidden thrill dies. Above 30: he starts spiraling, canceling, potentially confessing to Karen.

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

| Day Range | tom_devotion | Gate Status |
|-----------|-------------|-------------|
| Day 12-16 | 0-15 | None — engineering encounters |
| Day 16-20 | 15-30 | `kiss_unlocked_tom` (~day 18-20) |
| Day 20-25 | 30-50 | `groping_unlocked_tom` (~day 23-25) |
| Day 25-28 | 50-70 | `oral_unlocked_tom` (~day 26-28) |
| Day 28-31 | 70-85 | `sex_unlocked_tom` (~day 29-31) |
| Day 31+ | 85-100 | Devotion → asset phase |

**Ray (SEDUCTION — medium):**

| Day Range | ray_interest | Gate Status |
|-----------|-------------|-------------|
| Day 18-24 | 0-10 | None — he doesn't notice her |
| Day 24-30 | 10-25 | Frame breaking — first crack |
| Day 30-34 | 25-45 | `groping_unlocked_ray` (~day 30-32), `kiss_unlocked_ray` (~day 32-34) |
| Day 34-38 | 45-65 | `oral_unlocked_ray` (~day 36-38) |
| Day 38-42 | 65-85 | `sex_unlocked_ray` (~day 38-42) |
| Day 42+ | 85-100 | Feelings complication zone |

**Mark (FORBIDDEN — hard):**

| Day Range | mark_desire | mark_guilt | Gate Status |
|-----------|-------------|-----------|-------------|
| Day 28-35 | 0-15 | 0-5 | None — professional flirtation |
| Day 35-40 | 15-30 | 5-12 | `kiss_unlocked_mark` (~day 38-40) |
| Day 40-44 | 30-50 | 12-20 | `groping_unlocked_mark` (~day 42-44) |
| Day 44-49 | 50-65 | 15-25 | `oral_unlocked_mark` (~day 47-49) |
| Day 49-52 | 65-80 | 20-30 | `sex_unlocked_mark` (~day 50-52) |
| Day 52-58 | 80-95 | 15-35 | Guilt management phase — Karen crisis |

**Jake (DOMINANCE — endgame):**

| Day Range | jake_power | Gate Status |
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
| `kiss_unlocked_tom` | "The Classroom Catch" — she "trips," he catches her, she looks up and waits, he freezes, she closes the distance | Day ~18-20 | `tom_devotion >= 20`, `confidence >= 10` | Kissing/touch choices in Tom activities |
| `groping_unlocked_tom` | "Movie Night" — she invites him over, sits close, hand on his thigh, she guides his hands to her body | Day ~23-25 | `tom_devotion >= 35`, `corruption >= 20` | Groping/foreplay choices |
| `oral_unlocked_tom` | "Good Boy" — she teaches him to go down on her. Patient, commanding, explicit instruction. "Slower. Like that. Good boy." | Day ~26-28 | `tom_devotion >= 55`, `corruption >= 30` | Oral/intimate choices |
| `sex_unlocked_tom` | "First Time" — she takes his virginity. She's on top. She's in complete control. His first time is her creation. | Day ~29-31 | `tom_devotion >= 70`, `corruption >= 35` | Full sex choices |

#### Ray Gate Chain

| Gate | Story Event | Approx. Day | Stat Requirement | Unlocks |
|------|------------|-------------|-----------------|---------|
| `groping_unlocked_ray` | "The Shed" — she asks him to teach her tools, presses back against him, he goes still, she feels him respond | Day ~30-32 | `ray_interest >= 30`, `confidence >= 30` | Groping/physical choices in Ray activities |
| `kiss_unlocked_ray` | "The Staircase" — bar closes, he walks her upstairs, she stops on the second step (eye level), he breaks and kisses her hard. Pulls back: "This is a bad idea." She: "I know." | Day ~32-34 | `ray_interest >= 40`, `confidence >= 35` | Kissing choices |
| `oral_unlocked_ray` | "The Truck" — she drops to her knees in the cab of his truck after a late bar night. He doesn't expect it. He grips the steering wheel. She's in control. | Day ~36-38 | `ray_interest >= 55`, `corruption >= 45` | Oral choices |
| `sex_unlocked_ray` | "Upstairs" — he pulls her up the stairs to her room. Raw, urgent, no pretense. He knows what he's doing. She discovers what it's like with a man who knows. | Day ~38-42 | `ray_interest >= 70`, `corruption >= 50` | Full sex choices |

**Note**: Ray's groping gate fires BEFORE the kiss gate — the physical precedes the romantic. He touches her before he admits he wants to, which is consistent with his SEDUCTION driver.

#### Mark Gate Chain

| Gate | Story Event | Approx. Day | Stat Requirement | Unlocks |
|------|------------|-------------|-----------------|---------|
| `kiss_unlocked_mark` | "The Rain" — walking to his car after a late session, sharing an umbrella, she shivers against him, he almost kisses her, pulls back. First texts that night. The "kiss" is the text exchange — the physical barrier breaks through screens first. | Day ~38-40 | `mark_desire >= 25`, `confidence >= 25`, `corruption >= 40` | Charged-proximity choices in Mark activities |
| `groping_unlocked_mark` | "Under the Desk" — late classroom session, she guides his hand to her thigh under the desk. He doesn't remove it. The door is closed. Other teachers are in the building. | Day ~42-44 | `mark_desire >= 40`, `mark_guilt < 35` | Foreplay/touch choices |
| `oral_unlocked_mark` | "The First Visit" — he shows up at her door at night. "Karen thinks I'm at a meeting." She doesn't rush it. She pushes him onto the bed. She controls the pace. | Day ~47-49 | `mark_desire >= 55`, `corruption >= 50`, `mark_guilt < 40` | Oral/intimate choices |
| `sex_unlocked_mark` | "No Hesitation" — he comes back the second time. No shaking hands. No preamble. He walks in and he knows what he's here for. She lets him think he's leading. He isn't. | Day ~50-52 | `mark_desire >= 70`, `corruption >= 55` | Full sex choices |

**Note**: Mark's gates have a GUILT CEILING — if `mark_guilt` is too high at the time the event would fire, it delays. Emma must manage his guilt below threshold to progress.

#### Jake Gate Chain

| Gate | Story Event | Approx. Day | Stat Requirement | Unlocks |
|------|------------|-------------|-----------------|---------|
| `kiss_unlocked_jake` | "Not Yet" — bar closing, she sits on the bar, he tries to kiss her, she puts one finger on his lips. "Not yet." She allows ONE kiss on her terms — brief, her hand on the back of his neck, pulling him in then pushing him away. | Day ~52-54 | `jake_power <= 65`, `confidence >= 55` | Kissing on HER terms |
| `groping_unlocked_jake` | "Permission" — she lets him touch her but controls exactly where and how. His hands go where she puts them. When he moves them without asking, she stops. He learns. | Day ~54-56 | `jake_power <= 50`, `corruption >= 60` | Touch choices — she dictates |
| `oral_unlocked_jake` | "The Stockroom" — she takes him to the stockroom behind the bar. Jolene's in the front. Customers 20 feet away. She puts him on his knees. "Someone could walk in." "Then you'd better be quick." | Day ~58-60 | `jake_power <= 35`, `corruption >= 70` | Oral — she receives, he serves |
| `sex_unlocked_jake` | "On Her Terms" — she's on top. She pins his hands. "Did I say you could touch?" He discovers he likes not being in charge. She discovers the final form of her power. | Day ~60-63 | `jake_power <= 20`, `corruption >= 75` | Full sex — she commands |

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
tom_devotion_confession         # "I've never felt like this about anyone"
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
mark_guilt_spiral               # Trigger if mark_guilt > 40
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
rent_last_paid                  # Timer: days_since_flag for weekly rent
groceries_last_bought           # Timer: days_since_flag for food stocking
food_stocked                    # True when groceries current (5-day duration)
church_attended_this_week       # Weekly reset flag
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


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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

**Weekday (Monday-Friday):**
- Morning + Late Morning = SCHOOL (mandatory, non-negotiable)
- 5 usable slots: Afternoon, Late Afternoon, Evening, Night, Late Night
- But Evening/Night/Late Night overlap with bar activity — choosing work (shifts) vs. NPC pursuit vs. rest

**Weekend (Saturday-Sunday):**
- All 8 slots free
- But NPCs have their own schedules:
  - Tom: On duty Saturday (limited availability). Off Sunday.
  - Ray: Works odd jobs Sat morning. Free Sat afternoon/evening. Bar Sun evening.
  - Mark: With family ALL WEEKEND. Only available if he invents an excuse (requires `mark_desire >= 30`). Most risky time — Karen is tracking him.
  - Jake: Works bar Fri/Sat night (his busiest). Off Sunday.
- Sunday morning: Church (mandatory for reputation — skip at -5 rep cost)
- Saturday morning: Recovery from Friday night OR weekend cafe shifts ($45)
- Sunday cafe shift conflicts with church — choose money or reputation

### Activity Schedule Overview

| Time Period | Location | Activity | NPC | Type |
|-------------|----------|----------|-----|------|
| **Early Morning** | | | | |
| 05:00-07:00 | Town streets/fields | Morning jog | Solo | Utility (energy +10) |
| 05:00-07:00 | Emma's Room | Sleep in | Solo | Utility (energy +15, but loses the slot) |
| **Morning** | | | | |
| 07:00-09:00 | Classroom | Teaching | Solo | Mandatory (weekday) |
| 07:00-09:00 | Diner | Weekend Cafe Job | Solo | Money ($45, Sat/Sun) |
| 07:00-09:00 | Church | Church Attendance | Solo | Reputation (+3, Sunday) |
| **Late Morning** | | | | |
| 09:00-12:00 | Classroom | Teaching | Solo | Mandatory (weekday) |
| 09:00-12:00 | Diner | Weekend Cafe Job (cont.) | Solo | Money (part of morning shift) |
| 09:00-12:00 | Church | Sunday School Volunteering | Solo | Reputation (+4, Sunday) |
| 09:00-12:00 | Jolene's Space | Jolene Chat | Jolene | Mentor (weekday, off-school) |
| **Afternoon** | | | | |
| 12:00-15:00 | Diner | Coffee with Tom | Tom | NPC repeatable (Mon/Wed/Fri) |
| 12:00-15:00 | Library/Classroom | Tutoring | Solo | Money ($30) + Reputation (+1) (Mon/Wed) |
| 12:00-15:00 | General Store | Grocery Shopping | Solo | Survival utility |
| 12:00-15:00 | Jolene's Space | Jolene Chat | Jolene | Mentor (if not done in late morning) |
| 12:00-15:00 | Mark's Office | Lunch Visit | Mark | NPC (gated: `mark_groping_unlocked`) |
| **Late Afternoon** | | | | |
| 15:00-17:00 | Classroom | Parent Conferences (Mark) | Mark | NPC repeatable (Tue/Thu) |
| 15:00-17:00 | General Store | Grocery Shopping | Solo | Survival utility |
| 15:00-17:00 | General Store/Streets | Neighborly Visits | Solo | Reputation (+2) |
| 15:00-17:00 | Deputy Station | Visit Tom at Station | Tom | NPC (early game proximity) |
| 15:00-17:00 | Anywhere | Errands / Free | Solo | Shopping, clothes, prep |
| **Evening** | | | | |
| 17:00-19:00 | Bar Floor | Bar Shift (evening) | Solo | Money ($50-80) |
| 17:00-19:00 | Bar Floor | Evening at the Bar (Ray) | Ray | NPC repeatable |
| 17:00-19:00 | Bar Floor | Evening at the Bar (Jake) | Jake | NPC repeatable |
| 17:00-19:00 | Emma's Room | Dinner / Rest | Solo | Utility (energy recovery) |
| **Night** | | | | |
| 19:00-22:00 | Bar Floor | Bar Shift (night) | Solo | Money ($50-80) |
| 19:00-22:00 | Bar Floor | Evening at the Bar (Ray) | Ray | NPC repeatable |
| 19:00-22:00 | Bar Floor | Evening at the Bar (Jake) | Jake | NPC repeatable |
| 19:00-22:00 | Emma's Room | Invite NPC Over | Tom/Ray/Mark | NPC (gated per NPC) |
| 19:00-22:00 | Town streets | Walk with NPC | Tom/Ray | NPC (ambient/bridge event) |
| **Late Night** | | | | |
| 22:00-01:00 | Emma's Room | Sleep | Solo | Utility (standard energy restore: 80) |
| 22:00-01:00 | Bar Stockroom | Stockroom encounter | Jake | NPC (gated: `jake_oral_unlocked`) |
| 22:00-01:00 | Ray's Truck/Shed | Truck encounter | Ray | NPC (gated: `ray_oral_unlocked`) |
| 22:00-01:00 | School Parking Lot | Parking Lot encounter | Mark | NPC (gated: `mark_sex_unlocked`) |
| 22:00-01:00 | Emma's Room | Late visit (any NPC) | Any | NPC (gated per NPC) |

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
| Gift for Ray's daughter | $25 | Optional, Act 2 Ray arc | `ray_interest +3` if given at the right time (her birthday week). Major trust boost. |
| Outfit for Mark | $60 | Act 2 Mark arc | Specific dress/outfit for conferences. `mark_desire +2` when worn. |
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
| Late Night (22:00-01:00) | Home | In bed by 22:30. Early riser. | Late visit only if invited + high `tom_devotion`. |

**Tom schedule notes:**
- **Saturday**: On duty half the day (morning patrol + station). Free afternoon/evening. Might show up at the bar (awkward, trying too hard).
- **Sunday**: Off duty. Church in the morning (same church as Emma — he sits in the back, steals glances). Free rest of day.
- **Tom movement pattern**: Completely predictable. Station → Diner → Station → Home. He gravitates toward wherever Emma is but tries to make it look accidental. The Diner at lunchtime is the guaranteed intercept point.

---

### Ray's Daily Schedule

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

Mark's schedule is the most constrained — because Karen monitors it. Every hour he spends with Emma is an hour he has to account for.

| Time Period | Location | What He's Doing | Available for Activity? |
|-------------|----------|-----------------|----------------------|
| Early Morning (05:00-07:00) | Home (with family) | Getting ready. Family breakfast. | No. |
| Morning (07:00-09:00) | Mark's Office | Opens the agency. Client calls. | No — public-facing, staff present. |
| Late Morning (09:00-12:00) | Mark's Office | Working. Might have a gap between clients. | "Insurance question" (very early game proximity). |
| Afternoon (12:00-15:00) | Mark's Office / Lunch | Lunch break. Sometimes at the diner. | **Lunch Visit to Office (gated: `mark_groping_unlocked`).** |
| Late Afternoon (15:00-17:00) | School (Tue/Thu) / Office | **Parent conferences. "Fundraiser planning."** | **Parent Conferences — PEAK MARK HOURS.** (Tue/Thu only) |
| Evening (17:00-19:00) | Home (with family) | Family dinner. Karen expects him home by 6:00. | No — unless he has an "excuse" (`mark_desire >= 40`). |
| Night (19:00-22:00) | Home (with family) | Family time. Helping kid with homework. TV with Karen. | **Her room (gated: `mark_oral_unlocked`).** He invents excuses — "meeting," "client dinner." Huge risk. |
| Late Night (22:00-01:00) | Home | Karen is asleep by 10:30. He could leave — if he dares. | **School Parking Lot / Her room (highest risk).** "Couldn't sleep, going for a drive." Karen might wake up. |

**Mark schedule notes:**
- **Saturday**: WITH FAMILY ALL DAY. Little league, errands, home. Available ONLY if he invents an excuse. Every Saturday absence is tracked by Karen.
- **Sunday**: Church with family (they sit together — Emma must perform normalcy). Family lunch. Maybe a "quick errand" in the afternoon if `mark_desire >= 40`.
- **Mark movement pattern**: Office → School → Home. His world is a triangle. Every deviation is an alibi he has to construct. The school is the only legitimate overlap with Emma. His office is plausible ("she had an insurance question"). His car at her bar is a bomb waiting to detonate.

---

### Jake's Daily Schedule

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


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 4: STORY EVENTS
# New In Town

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
  → `tom_devotion +2, confidence +1`. He'll replay "I feel safer already" in his head for days.
- **"Stay for coffee? I don't know anyone here yet."** — Extend the encounter. More time.
  → `tom_devotion +3, confidence +1`. He stays for an hour. Can barely make sentences. Spills his coffee once.

**Both set**: `tom_locks_checked`

---

### TOM ACT 1 EVENT 2 — "Classroom Setup" (Day 15-17)

**Canvas ID**: `tom_classroom_setup`
**Trigger**: `tom_locks_checked`, `tom_devotion >= 10`, Day >= 15, 12:00-17:00
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
  → `tom_devotion +2, confidence +1`
- **Brush against him reaching for the same decoration.** — Deliberate contact. Test the response.
  → `tom_devotion +3, confidence +2, corruption +1`

**Both set**: `tom_classroom_setup`

---

### TOM GATE 1 — "The Classroom Catch" (kiss_unlocked) (Day 18-20)

**Canvas ID**: `tom_classroom_catch`
**Trigger**: `tom_classroom_setup`, `tom_devotion >= 20`, `confidence >= 10`, Day >= 18, 12:00-17:00
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
  → `tom_devotion +5, confidence +3, corruption +2`. He touched his lips three times on the drive home. She knows because she watched from the window.
- **Pull away slowly and whisper: "I should go."** — Don't kiss. Make him obsess. The almost-kiss is worse than the kiss for a boy like Tom.
  → `tom_devotion +4, corruption +3`. He won't sleep tonight. He'll replay it. And he'll be back. Hungrier. The kiss comes two days later.

**Both set**: `tom_classroom_catch`, `tom_kiss_unlocked`
**Note**: Both choices unlock the kiss gate. The kiss either happens here or in a follow-up triggered 2 days later. Either way, she's in control.

---

### TOM BRIDGE EVENT — "Tom's Confession" (Day 20-22)

**Canvas ID**: `tom_devotion_confession`
**Trigger**: `tom_kiss_unlocked`, `tom_devotion >= 30`, Day >= 20
**Location**: Diner
**Priority**: 8
**Is Repeatable**: false

---

Non-mechanical character development. No gates unlocked. Exists to deepen Tom as a person.

Coffee at the diner. He's relaxed — the kiss happened, the world didn't end. He tells her about his dad. The old sheriff. The heart attack on duty. How Tom inherited the badge and the town's expectations in the same breath. How he never left Millfield because leaving felt like abandoning his dad's ghost.

"Everyone here thinks I'm brave because I carry a badge. I'm not brave. I just never had anywhere else to go."

She sees it: he's her. He's who she was two weeks ago. Trapped by expectations, defined by other people's image of him, never having seen an alternative.

And she's about to break him out of that cage. The same way Jolene broke her out of hers.

**Stats**: `tom_devotion +2` (he opened up; she listened)
**Sets**: `tom_devotion_confession`

---

### TOM GATE 2 — "Movie Night" (groping_unlocked) (Day 23-25)

**Canvas ID**: `tom_movie_night`
**Trigger**: `tom_kiss_unlocked`, `tom_devotion >= 35`, `corruption >= 20`, Day >= 23, 19:00-01:00
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
  → `tom_devotion +4, corruption +2, confidence +2`. He touches her like she's made of glass. She'll teach him she isn't.
- **"Touch me where you want to."** — Give him freedom. See what he does.
  → `tom_devotion +5, corruption +1, confidence +1`. His hand stays on her thigh. He's too scared to go further. She covers his hand with hers and moves it. "It's okay."

**Both set**: `tom_movie_night`, `tom_groping_unlocked`

---

### TOM GATE 3 — "Good Boy" (oral_unlocked) (Day 26-28)

**Canvas ID**: `tom_good_boy`
**Trigger**: `tom_groping_unlocked`, `tom_devotion >= 55`, `corruption >= 30`, Day >= 26, 22:00-01:00
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
  → `tom_devotion +5, corruption +3, confidence +3`. He'll do anything she says now. Anything.
- **"Come here."** — Pull him close. Soften it. She's not a monster yet.
  → `tom_devotion +4, corruption +2, confidence +2`. Warmth and control. The combo is effective.

**Both set**: `tom_good_boy`, `tom_oral_unlocked`

---

### TOM GATE 4 — "First Time" (sex_unlocked) (Day 29-31)

**Canvas ID**: `tom_first_time`
**Trigger**: `tom_oral_unlocked`, `tom_devotion >= 70`, `corruption >= 35`, Day >= 29, 22:00-01:00
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
  → `tom_devotion +5, corruption +3`. He becomes her tool — covers for her, lies for her, looks the other way when he shouldn't.
  → Sets `tom_asset_activated`
- **"Don't say that."** — She can't hear it. Not yet. She's not ready to face what she's doing.
  → `tom_devotion +4, confidence +2`. A flash of the old Emma. It passes.

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

**Stats**: `ray_interest +3, confidence +2`
**Sets**: `ray_first_sentence`, `ray_plumbing_excuse`, `ray_first_crack`

---

### RAY ACT 2 EVENT — "The Truck Conversation" (Day 28-30)

**Canvas ID**: `ray_truck_conversation`
**Trigger**: `ray_first_crack`, `ray_interest >= 15`, `confidence >= 25`, Day >= 28, 17:00-22:00
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

**Stats**: `ray_interest +4, confidence +3`
**Sets**: `ray_truck_conversation`

---

### RAY GATE 1 — "The Shed" (groping_unlocked) (Day 30-32)

**Canvas ID**: `ray_shed_scene`
**Trigger**: `ray_truck_conversation`, `ray_interest >= 30`, `confidence >= 30`, Day >= 30, 15:00-19:00
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
  → `ray_interest +5, confidence +4, corruption +2`. She turns. Their faces are inches apart. His eyes are dark. His jaw is tight. "This is a bad idea," he says. He doesn't step back.
- **Stay pressed against him and keep "sawing."** — Torture him with plausible deniability.
  → `ray_interest +4, corruption +4, confidence +3`. She resumes the sawing motion. Slowly. He makes a sound in the back of his throat and his hands grip her hips. Neither mentions it after. But he can't unsee her now.

**Both set**: `ray_shed_scene`, `ray_groping_unlocked`
**Note**: Ray's groping gate fires BEFORE the kiss gate — physical precedes emotional. His body admits what his mind won't.

---

### RAY GATE 2 — "The Staircase" (kiss_unlocked) (Day 32-34)

**Canvas ID**: `ray_staircase_kiss`
**Trigger**: `ray_groping_unlocked`, `ray_interest >= 40`, `confidence >= 35`, Day >= 32, 22:00-01:00
**Location**: Bar Floor → Staircase
**Priority**: 10
**Is Repeatable**: false

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

**Stats**: `ray_interest +5, confidence +5, corruption +2`
**Sets**: `ray_staircase_kiss`, `ray_kiss_unlocked`

---

### RAY BRIDGE EVENT — "The Daughter" (Day 34-36)

**Canvas ID**: `ray_daughter_story`
**Trigger**: `ray_kiss_unlocked`, `ray_interest >= 45`, Day >= 34
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

**Stats**: `ray_interest +2`
**Sets**: `ray_daughter_story`

---

### RAY GATE 3 — "The Truck" (oral_unlocked) (Day 36-38)

**Canvas ID**: `ray_truck_oral`
**Trigger**: `ray_kiss_unlocked`, `ray_interest >= 55`, `corruption >= 45`, Day >= 36, 22:00-01:00
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

**Stats**: `ray_interest +5, corruption +3, confidence +4`
**Sets**: `ray_truck_oral`, `ray_oral_unlocked`

---

### RAY TENSION EVENT — "Feelings" (Day 38-40)

**Canvas ID**: `ray_feelings_emerge`
**Trigger**: `ray_oral_unlocked`, `ray_interest >= 60`, Day >= 38
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

**Stats**: `ray_interest -3` (his behavior shift creates temporary distance as he self-regulates)
**Sets**: `ray_feelings_emerge`

---

### RAY GATE 4 — "Upstairs" (sex_unlocked) (Day 38-42)

**Canvas ID**: `ray_upstairs`
**Trigger**: `ray_feelings_emerge`, `ray_interest >= 70`, `corruption >= 50`, Day >= 38, 22:00-01:00
**Location**: Bar Floor → Emma's Room
**Priority**: 10
**Is Repeatable**: false

---

Bar closing. Just them. He's been watching her all night — not the old dismissive watching. Hungry watching. He walks to the staircase. Stops. Looks at her.

"Are you coming up?"

She isn't asking. He follows.

Upstairs. Her room. He pushes her against the door. This isn't Tom — there's nothing tentative. Ray knows what he's doing. His hands, his mouth, the way he lifts her like she weighs nothing.

Sex with Ray is different than Tom. He's experienced. He takes charge. She gasps — actually gasps, unperformative — and for a moment, she's not the one in control.

Afterward, she lies there and realizes: she doesn't like it. Not the sex — the sex was incredible. She doesn't like NOT being in control. She doesn't like gasping. She wants to be the one *making* them gasp.

This is what Ray teaches her. Not by failing — by being too good. By being the man who shows her that competent sex isn't what she wants. She wants power. Pure power. And Ray is too much of an equal for that.

**Stats**: `ray_interest +5, corruption +3, confidence +3`
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

**Stats**: `mark_desire +2, corruption +1`
**Sets**: `mark_first_conference`

---

### MARK ACT 1 EVENT 2 — "The Volunteer" (Day 32-35)

**Canvas ID**: `mark_fundraiser_volunteer`
**Trigger**: `mark_first_conference`, `mark_desire >= 8`, Day >= 32, 15:00-17:00
**Location**: Classroom
**Priority**: 8
**Is Repeatable**: false

---

Mark volunteers for the school fundraiser. He invents the reason. "Karen usually does this but she's been busy." Karen isn't busy. He's manufacturing proximity.

They work late in the classroom. Counting supplies, making posters. He brings coffee from the diner. Conversation gets personal — his marriage, his job, his sense that he's been sleepwalking through a life someone else designed for him.

She creates emotional intimacy Karen doesn't provide. She asks questions no one asks him. She says: "That must be lonely." And the word "lonely" hits him like a brick because no one — not Karen, not his friends, not his therapist he saw twice and quit — has named it.

**Stats**: `mark_desire +3, mark_guilt +2, confidence +1`
**Sets**: `mark_fundraiser_volunteer`

---

### MARK GATE 1 — "The Rain" (kiss_unlocked) (Day 38-40)

**Canvas ID**: `mark_rain_umbrella`
**Trigger**: `mark_fundraiser_volunteer`, `mark_desire >= 25`, `confidence >= 25`, `corruption >= 40`, Day >= 38, 15:00-19:00
**Location**: Classroom → Town Streets (parking area)
**Priority**: 10
**Is Repeatable**: false

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

**Stats**: `mark_desire +5, mark_guilt +3, corruption +2`
**Sets**: `mark_rain_umbrella`, `mark_kiss_unlocked`, `mark_texting_escalation`

---

### MARK GATE 2 — "Under the Desk" (groping_unlocked) (Day 42-44)

**Canvas ID**: `mark_under_desk`
**Trigger**: `mark_kiss_unlocked`, `mark_desire >= 40`, `mark_guilt < 35`, Day >= 42, 15:00-17:00
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

**Stats**: `mark_desire +4, mark_guilt +3, corruption +2, reputation -2`
**Sets**: `mark_under_desk`, `mark_groping_unlocked`

---

### MARK BRIDGE EVENT — "The Phone Call" (Day 45-47)

**Canvas ID**: `mark_call_from_bedroom`
**Trigger**: `mark_groping_unlocked`, `mark_desire >= 45`, `corruption >= 50`, Day >= 45
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

**Stats**: `mark_desire +3, mark_guilt +4, corruption +3`
**Sets**: `mark_call_from_bedroom`

---

### MARK GATE 3 — "The First Visit" (oral_unlocked) (Day 47-49)

**Canvas ID**: `mark_first_visit`
**Trigger**: `mark_groping_unlocked`, `mark_desire >= 55`, `corruption >= 50`, `mark_guilt < 40`, Day >= 47, 19:00-01:00
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

**Stats**: `mark_desire +5, mark_guilt +5, corruption +3, confidence +2`
**Sets**: `mark_first_visit`, `mark_oral_unlocked`

---

### MARK GATE 4 — "No Hesitation" (sex_unlocked) (Day 50-52)

**Canvas ID**: `mark_no_hesitation`
**Trigger**: `mark_oral_unlocked`, `mark_desire >= 70`, `corruption >= 55`, Day >= 50, 19:00-01:00
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
  → `mark_desire +4, mark_guilt +5, corruption +3`. He looks at her like she's the devil and the only thing he's ever truly wanted. He'll come back tomorrow.
- **"We both wanted this."** — Tenderness. Make him feel safe. Reduce guilt.
  → `mark_desire +3, mark_guilt +2, confidence +2`. He calms down. She holds him. He's easier to manage at lower guilt. But the forbidden thrill softens.

**Both set**: `mark_no_hesitation`, `mark_sex_unlocked`

---

### MARK CRISIS — "Karen" (Day 52-55)

**Canvas ID**: `karen_crisis`
**Trigger**: `mark_sex_unlocked`, `mark_guilt >= 20`, Day >= 52
**Location**: Classroom → Town Streets
**Priority**: 10
**Is Repeatable**: false

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

**Stats**: `reputation -5 to -8`, `mark_guilt +8`, `mark_desire -3` (he's terrified)
**Sets**: `karen_finds_text`, `karen_school_confrontation`
**Reputation**: Major hit. The school is buzzing. Principal will follow up.

---

### MARK CRISIS REPAIR — "The Parking Lot" (Day 54-57)

**Canvas ID**: `mark_crisis_repair`
**Trigger**: `karen_school_confrontation`, `days_since_flag(karen_school_confrontation) >= 2`, Day >= 54, 22:00-01:00
**Location**: School Parking Lot
**Priority**: 10

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
  → `mark_guilt -10, mark_desire -5`. He takes the exit. But he comes crawling back in 3-4 days because the hunger doesn't stop. The affair survives on lower heat.
  → Sets `karen_backed_down`
- **"She doesn't know who you are. I do."** — Pull him deeper. Name the truth Karen can't face.
  → `mark_guilt +2, mark_desire +5, corruption +3`. He stares at her. Then he kisses her in the parking lot of his son's school and she tastes tears on his face. The affair intensifies.
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

**Stats**: `jake_power -5` (shifted toward her), `confidence +3, corruption +1`
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

**Stats**: `jake_power -5`, `corruption +2`
**Sets**: `jake_jealousy_game`

---

### JAKE ACT 2 EVENT — "Pour Me One More" (Day 48-52)

**Canvas ID**: `jake_bar_sitting`
**Trigger**: `jake_jealousy_game`, `jake_power <= 75`, `corruption >= 60`, Day >= 48, 22:00-01:00
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

**Stats**: `jake_power -10`, `confidence +4, corruption +3`
**Sets**: `jake_bar_sitting`

---

### JAKE BRIDGE EVENT — "The Ego Crisis" (Day 52-54)

**Canvas ID**: `jake_ego_crisis`
**Trigger**: `jake_bar_sitting`, `jake_power <= 65`, Day >= 52
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

**Stats**: `jake_power -5`
**Sets**: `jake_ego_crisis`

---

### JAKE GATE 1 — "Not Yet" (kiss_unlocked) (Day 52-54)

**Canvas ID**: `jake_not_yet`
**Trigger**: `jake_ego_crisis`, `jake_power <= 65`, `confidence >= 55`, Day >= 52, 22:00-01:00
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

**Stats**: `jake_power -5, confidence +3, corruption +2`
**Sets**: `jake_not_yet`, `jake_kiss_unlocked`

---

### JAKE GATE 2 — "Permission" (groping_unlocked) (Day 54-56)

**Canvas ID**: `jake_permission`
**Trigger**: `jake_kiss_unlocked`, `jake_power <= 50`, `corruption >= 60`, Day >= 54, 22:00-01:00
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

**Stats**: `jake_power -10, corruption +3, confidence +3`
**Sets**: `jake_permission`, `jake_groping_unlocked`

---

### JAKE GATE 3 — "The Stockroom" (oral_unlocked) (Day 58-60)

**Canvas ID**: `jake_stockroom`
**Trigger**: `jake_groping_unlocked`, `jake_power <= 35`, `corruption >= 70`, Day >= 58, 22:00-01:00
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

**Stats**: `jake_power -10, corruption +4, confidence +5`
**Sets**: `jake_stockroom`, `jake_oral_unlocked`
**Risk**: `reputation -3` (Jolene might hear; small chance a customer returns for their jacket)

---

### JAKE GATE 4 — "On Her Terms" (sex_unlocked) (Day 60-63)

**Canvas ID**: `jake_on_her_terms`
**Trigger**: `jake_oral_unlocked`, `jake_power <= 20`, `corruption >= 75`, Day >= 60, 22:00-01:00
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

**Stats**: `jake_power -10, corruption +5, confidence +5`
**Sets**: `jake_on_her_terms`, `jake_sex_unlocked`

---

### JAKE ENDGAME — "The Surrender" (Day 63-65)

**Canvas ID**: `jake_endgame_choice`
**Trigger**: `jake_sex_unlocked`, `jake_power <= 10`, Day >= 63
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
  → `jake_power = 0`. `jake_surrender`. He's a permanent asset. She owns the bar dynamic now.
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
**Trigger**: Day is Friday, 19:00-22:00, `tom_kiss_unlocked` AND `ray_interest >= 20`
**Location**: Bar Floor
**Priority**: 8
**Is Repeatable**: false

Friday night. The bar is full. Tom is here (off duty, out of uniform, uncomfortable). Ray is at his stool. Jake is behind the counter. Mark... is here. Without Karen. Catches her eye across the room.

Four men. One room. All of them aware of her. None of them aware of each other — yet.

She has to choose who to focus on.

**Choices**:
- **Sit with Tom** → `tom_devotion +2, reputation +1` (public, safe, wholesome-looking)
- **Join Ray at the bar** → `ray_interest +2, reputation -1` (older man, drinking, people notice)
- **Flirt with Jake across the counter** → `jake_power -2, reputation -1` (the bartender? really?)
- **Catch Mark's eye and nod toward the door** → `mark_desire +3, reputation -2, mark_guilt +2` (the married man left the building with the teacher)

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
  → `tom_devotion -2` (he doesn't fully believe it), but the relationship survives.
- **"Tom. Look at me. You are the one I think about."** — Redirect. Give him what he needs.
  → `tom_devotion +2, corruption +2`. She's managing him. He believes it because he needs to.
- **"It's complicated."** — Honest-ish. He's hurt but respects her honesty.
  → `tom_devotion -3, reputation -2`. If `tom_devotion >= 60`, he agrees to look the other way: `tom_covers_for_emma`.

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

**Stats**: `ray_interest -2`
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
tom_kiss_unlocked + ray_interest >= 20 → friday_collision
tom_kiss_unlocked + ray_kiss_unlocked → tom_saw_ray → (tom_covers_for_emma?)
ray_kiss_unlocked + mark_kiss_unlocked → ray_sees_mark_text
(tom_saw_ray + ray_sees_mark_text) OR friday_collision → juggling_detected
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GATE TIMELINE SUMMARY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| NPC | Gate | Set By Event | Key Requirements | ~Day |
|-----|------|-------------|-----------------|------|
| **Tom** | kiss_unlocked | "The Classroom Catch" | `tom_devotion >= 20, confidence >= 10` | ~18-20 |
| **Tom** | groping_unlocked | "Movie Night" | `tom_devotion >= 35, corruption >= 20` | ~23-25 |
| **Tom** | oral_unlocked | "Good Boy" | `tom_devotion >= 55, corruption >= 30` | ~26-28 |
| **Tom** | sex_unlocked | "First Time" | `tom_devotion >= 70, corruption >= 35` | ~29-31 |
| **Ray** | groping_unlocked | "The Shed" | `ray_interest >= 30, confidence >= 30` | ~30-32 |
| **Ray** | kiss_unlocked | "The Staircase" | `ray_interest >= 40, confidence >= 35` | ~32-34 |
| **Ray** | oral_unlocked | "The Truck" | `ray_interest >= 55, corruption >= 45` | ~36-38 |
| **Ray** | sex_unlocked | "Upstairs" | `ray_interest >= 70, corruption >= 50` | ~38-42 |
| **Mark** | kiss_unlocked | "The Rain" | `mark_desire >= 25, confidence >= 25, corruption >= 40` | ~38-40 |
| **Mark** | groping_unlocked | "Under the Desk" | `mark_desire >= 40, mark_guilt < 35` | ~42-44 |
| **Mark** | oral_unlocked | "The First Visit" | `mark_desire >= 55, corruption >= 50, mark_guilt < 40` | ~47-49 |
| **Mark** | sex_unlocked | "No Hesitation" | `mark_desire >= 70, corruption >= 55` | ~50-52 |
| **Jake** | kiss_unlocked | "Not Yet" | `jake_power <= 65, confidence >= 55` | ~52-54 |
| **Jake** | groping_unlocked | "Permission" | `jake_power <= 50, corruption >= 60` | ~54-56 |
| **Jake** | oral_unlocked | "The Stockroom" | `jake_power <= 35, corruption >= 70` | ~58-60 |
| **Jake** | sex_unlocked | "On Her Terms" | `jake_power <= 20, corruption >= 75` | ~60-63 |

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


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
- **Energy Cost**: -10

---

### Base Scene (always shown)

**DEFAULT**: The diner. Afternoon. Tom is already there — he showed up fifteen minutes early and has been staring at the door. He's in his off-duty clothes: a clean flannel, jeans that fit like he thought about it. He stands up when she arrives, bumps the table, steadies his coffee mug. "Hey. Hi. You look — how are you?"

He always asks how she is before he tells her anything about himself. He's the only man in Millfield who does that.

**WITHDRAWN variant** (post-tension — e.g., after `tom_saw_ray`): He's at the booth but hasn't ordered for her. He smiles, but it doesn't reach his eyes. He asks about school, not about her. The questions feel like walls.

**WARM variant** (high `tom_devotion`, post-`tom_groping_unlocked`): He's saved the booth in the back corner — their booth now. He ordered her coffee the way she takes it. When she slides in, his knee finds hers under the table immediately. He can't stop looking at her mouth.

**Media**: IMAGE — "Young couple at diner booth, small-town America, afternoon, coffee cups, him nervous and adoring, her confident and amused"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Ask about his day" | always | exit | +1 tom_devotion |
| "Lean close when talking" | tom_devotion >= 22 | warm | +2 tom_devotion, +1 confidence |
| "Touch his thigh under the table" | tom_devotion >= 42 + tom_kiss_unlocked | kiss | +3 tom_devotion, +1 corruption |
| "Guide his hand between your legs" | tom_devotion >= 62 + tom_groping_unlocked | foreplay | +4 tom_devotion, +1 corruption, reputation -1 |

**Caps at foreplay** — this is a public diner. The risk of a public groping incident is the peak of what this location supports. Full escalation happens at Emma's Room.

### Escalation Nodes

**WARM NODE**: She leans across the table. Her hand on his arm. She says something — it doesn't matter what — while her thumb traces circles on the inside of his wrist. His pulse is visible. He loses his train of thought mid-sentence and just looks at her.

The waitress refills their coffee and says, "You two are cute." Tom turns the color of ketchup.

**Media**: IMAGE — "Young couple in diner booth, her leaning close, hand on his arm, intimate conversation, small town"

**Exit**: "Keep talking" → +2 tom_devotion | "Smile and pull away" → +1 tom_devotion, +1 confidence

---

**KISS NODE**: Under the table, her hand finds his thigh. She squeezes once. He freezes. His fork clatters. She doesn't move her hand. Just lets it rest there, warm, possessive, while they talk about nothing. Her fingers creep higher. His voice goes up half an octave.

"Emma, we're in—"

"I know where we are."

**Media**: VIDEO — "Woman's hand under diner table on man's thigh, hidden from other diners, charged tension"

**Exit**: "Pull away and smile" → +3 tom_devotion, +1 corruption | "Whisper 'Later'" → +2 tom_devotion, +2 corruption

---

**FOREPLAY NODE**: She takes his hand under the table. Guides it to her thigh. Higher. His breathing changes. The waitress is across the room. An older couple in the far booth. His fingers touch the hem of her skirt and he makes a sound that he covers with a cough.

She controls his hand — where it goes, how long it stays. She's looking at him the whole time, eating her pie with the other hand like nothing is happening.

"You're doing great, Tom."

He nearly dies.

**Media**: VIDEO — "Couple at diner booth, his hand under her skirt beneath table, her composed face, his red face, public setting, risky"

**Exit**: "That's enough for today" → +4 tom_devotion, reputation -1 | "Let him continue" → +3 tom_devotion, +2 corruption, reputation -2

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
| "Just talk" | always | exit | +1 tom_devotion |
| "Kiss him" | tom_devotion >= 42 + tom_kiss_unlocked | kiss | +2 tom_devotion, +1 corruption |
| "Guide his hands" | tom_devotion >= 62 + tom_groping_unlocked | foreplay | +2 tom_devotion, +2 corruption |
| "Teach him" | tom_devotion >= 82 + tom_oral_unlocked | intimate | +3 tom_devotion, +1 confidence |
| "Take him to bed" | tom_devotion >= 82 + tom_sex_unlocked | intense | +3 tom_devotion, +2 corruption |

### Escalation Nodes

**KISS NODE**: She pulls him in by his collar. He still kisses like he's asking permission — soft, careful, his hands hovering near her waist. She grabs his hands and puts them on her hips. "You can touch me, Tom." He does. Gently. Too gently. She tightens his grip with her hands over his.

**Media**: VIDEO — "Young couple kissing in small bedroom, her guiding his hands, him tentative, her in control"

**Exit**: "Pull back" → +2 tom_devotion | "Keep teaching" → +2 tom_devotion, +1 corruption

---

**FOREPLAY NODE**: She puts him on the bed. Straddles him. Takes his hands and places them — here, then here, then here. He follows instructions. He's getting better at this. When she moans — real, not performed — his face lights up like he's solved something.

"There. Just like that."

**Media**: VIDEO — "Woman straddling man on bed, guiding his hands on her body, him eager and learning, small room"

**Exit**: "That's enough for tonight" → +2 tom_devotion, +2 corruption | "Don't stop" → +3 tom_devotion, +1 confidence

---

**INTIMATE NODE**: She pushes him back on the bed. "Your turn to practice." She's taught him technique over multiple visits and he's improved. He goes down on her with the earnest focus of a student who wants to pass. She directs: "Slower. Right there. Don't stop." When she finishes, she runs her fingers through his hair. "Good boy."

The words hit him like a drug. Every time.

**Media**: VIDEO — "Man performing oral on woman in bed, her hands in his hair, small bedroom, intimate"

**Exit**: "Hold him after" → +3 tom_devotion, +1 confidence | "Tell him what he did right" → +2 tom_devotion, +2 corruption

---

**INTENSE NODE**: She's on top. Always on top with Tom. She controls the pace, controls his hands, controls when he's allowed to finish. He's completely surrendered to her direction. When she pins his wrists, he doesn't resist — he arches into it.

Afterward, he lies there looking at her like she invented oxygen. She traces patterns on his chest and thinks about the next man she needs to see this week.

**Media**: VIDEO — "Couple having sex, woman on top, his hands pinned, small bedroom, she's in control, intense"

**Exit**: "Stay with him" → +3 tom_devotion, +2 corruption | "Send him home" → +2 tom_devotion, +1 confidence

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
- **Energy Cost**: -15
- **Money Cost**: -5 to -8 (drinks)

---

### Base Scene

**DEFAULT**: The bar at evening. Ray is at his usual stool — end of the bar, back against the wall, clear sightline to the door. A beer in front of him, half-finished. He doesn't look up when she walks in. She sits two stools down. Orders whiskey. The silence between them is comfortable in a way conversation with Tom never is.

**WITHDRAWN variant** (post-`ray_feelings_emerge`): He's at his stool but further down the bar. Nursing his beer slower. He nods when she sits. Doesn't initiate. The warmth is there, buried, but something is pulling him back. He's fighting what he feels.

**WARM variant** (high `ray_interest`): He's saved the stool next to him. When she sits, his knee touches hers under the bar. He orders her drink before she asks. "Whiskey. Neat." He knows. The smallest intimacy — knowing how someone takes their drink — means more from Ray than speeches mean from other men.

**Media**: IMAGE — "Man and woman at dive bar counter, evening, him weathered and quiet, her confident, whiskey glasses, amber light"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Sit near him, drink quietly" | always | exit | +1 ray_interest |
| "Ask about his work, touch his forearm" | confidence >= 20 | warm | +2 ray_interest, +1 confidence |
| "Whisper something about last time" | confidence >= 40 + ray_kiss_unlocked | kiss | +3 ray_interest, reputation -1 if overheard |
| "Follow him to his truck in the parking lot" | corruption >= 50 + ray_groping_unlocked | foreplay | +4 ray_interest, reputation -2 |

**Caps at foreplay** — the bar is public. Parking lot is semi-public. Higher escalation happens at Ray's shed/truck or Emma's room (via story events).

### Escalation Nodes

**WARM NODE**: She puts her hand on his forearm. Leaves it there. He looks at her hand. Then at her. His jaw tightens — not rejection. Control. He's controlling the response she can see. But underneath her palm, his pulse is faster than his face lets on.

"Tough day?"

"Every day's a tough day." He covers her hand with his for two seconds. Then removes it. Drinks his beer. But those two seconds — she felt his callouses, his warmth, the grip that held back.

**Media**: IMAGE — "Woman's hand on man's forearm at bar, intimate, him looking at her hand, amber lighting"

**Exit**: "Stay and drink" → +2 ray_interest, +1 confidence | "Leave him wanting" → +1 ray_interest, +2 confidence

---

**KISS NODE**: She leans close. Whispers in his ear — something about the staircase, about his hands, about what she's thinking right now. His grip on his beer tightens. The bartender (Jake) is ten feet away. Other drinkers around them.

"You can't say that here." His voice is low, rough.

"I just did."

**Media**: VIDEO — "Woman whispering in man's ear at bar, intimate, danger of being overheard, bar setting"

**Exit**: "Walk away smiling" → +3 ray_interest, reputation -1 | "Hold his gaze" → +2 ray_interest, +1 corruption

---

**FOREPLAY NODE**: Bar closing. She follows him to the parking lot. His truck is in the dark corner — always parked furthest from the door, old habit. She leans against the hood. He stands in front of her. The parking lot is empty but exposed — headlights from the road, the bar's back door ten yards away.

He puts his hands on the hood, either side of her. Trapping her. His mouth on her neck. Her back arches against the truck. His hand under her jacket, under her shirt, on the warm skin of her stomach.

"We shouldn't—"

"Then stop."

He doesn't stop.

**Media**: VIDEO — "Couple against pickup truck in dark parking lot, him pressing against her, hands under jacket, outdoor, risky"

**Exit**: "Push him away and go inside" → +4 ray_interest, reputation -2 | "Pull him closer" → +3 ray_interest, +2 corruption, reputation -2

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
| "Work alongside him" | always | exit | +1 ray_interest, +1 confidence |
| "Stand closer while he works" | ray_interest >= 22 | warm | +2 ray_interest, +2 confidence |
| "Press against him while he shows you" | ray_interest >= 42 + ray_groping_unlocked | foreplay | +3 ray_interest, +2 corruption |
| "His truck. The cab. Now." | ray_interest >= 62 + ray_oral_unlocked | intimate | +3 ray_interest, +2 confidence |
| "Pull him to the workbench" | ray_interest >= 82 + ray_sex_unlocked | intense | +3 ray_interest, +2 corruption, +1 confidence |

### Escalation Nodes

**WARM NODE**: He's cutting a board. She stands at the end, holding it steady. Their eyes meet over the sawdust. The saw makes a rhythmic sound. Neither speaks. He finishes the cut. Looks at her. The board is cut but neither of them lets go of their end.

"You're a quick learner."

"I had a good teacher."

The compliment lands differently than it would from anyone else. From Emma to Ray, "good teacher" is a weapon.

**Media**: IMAGE — "Man and woman working with saw in shed, eye contact, sawdust in air, intimate labor"

**Exit**: "Keep working" → +2 ray_interest, +2 confidence | "Let the moment stretch" → +2 ray_interest, +1 corruption

---

**FOREPLAY NODE**: He's behind her again. Correcting her grip. But this time she pushes back deliberately — her body against his. His arms tighten around her. The tool clatters to the workbench. His hand spreads across her stomach. His breathing is in her ear.

She reaches back and grabs his belt. "Don't move."

He doesn't move. The man who takes orders from no one stands perfectly still because she told him to.

**Media**: VIDEO — "Man pressed against woman from behind at workbench, shed setting, his hands on her stomach, physical tension"

**Exit**: "Turn around and face him" → +3 ray_interest, +2 corruption | "Stay like this" → +2 ray_interest, +2 confidence

---

**INTIMATE NODE**: His truck. The cab. She leads him there by the hand — a reversal he notices. Inside, she takes control. The bench seat. The dark. Her hands on his belt. She drops down.

Ray is different than Tom — he doesn't freeze, doesn't need directions. But he lets her set the pace. His hand in her hair is firm but not controlling. He's letting her lead. From Ray, that's a revolution.

**Media**: VIDEO — "Woman giving oral in truck cab, dark, cramped, man's hand in her hair, parking lot behind shed"

**Exit**: "Come back up" → +3 ray_interest, +2 confidence | "Finish him" → +3 ray_interest, +2 corruption

---

**INTENSE NODE**: The workbench. She clears the sawdust with her arm and pushes him against it. The shed door is closed but not locked. The bar is fifty yards away. Someone could walk the path at any time.

Sex with Ray is physical — workbench edge digging into her back, his hands on her thighs, the shed smelling like motor oil and sawdust. He's strong enough to lift her. She wraps her legs around him. He buries his face in her neck.

Afterward — the part that complicates things — he doesn't immediately get dressed. He stands there, looking at her. His expression is unguarded for once. Soft. She doesn't want soft from Ray. She wanted the challenge.

"Same time Thursday?"

"Yeah."

**Media**: VIDEO — "Couple having sex on workbench in shed, rustic, physical, her legs around him, tools and sawdust around them"

**Exit**: "Get dressed and leave" → +3 ray_interest, +2 corruption, +1 confidence

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

**WARM variant** (high `mark_desire`, pre-crisis): He closes the door behind him — casually, like the hallway draft. "Drafty corridor." They both know what a closed door means now. He sits closer than the desk requires. Brings her coffee from the diner. The excuse is thin and getting thinner.

**Media**: IMAGE — "Man and woman at teacher's desk, classroom, after hours, professional but charged, door partially open"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Keep it professional, hold eye contact" | always | exit | +1 mark_desire |
| "Brush against him when handing papers" | confidence >= 25 | warm | +2 mark_desire, +1 mark_guilt |
| "Close the door. Stand too close." | corruption >= 40 + mark_kiss_unlocked | kiss | +3 mark_desire, +2 mark_guilt, reputation -2 |
| "Lock the door. Tell him you missed him." | corruption >= 60 + mark_groping_unlocked | foreplay | +4 mark_desire, +3 mark_guilt, reputation -3 |

**Caps at foreplay** — this is a school. The principal's office is down the hall. Other teachers walk by. The forbidden driver thrives on the location — every escalation here is exponentially riskier than anywhere else.

### Escalation Nodes

**WARM NODE**: Handing him the report card. Their fingers touch. She doesn't pull away. Turns the paper so they're both reading it — which requires leaning in. Her shoulder against his. She smells his cologne — he put on cologne for a parent-teacher conference. For her.

"His handwriting is improving."

"Your influence, I'm sure."

The double meaning sits between them like a lit match.

**Media**: IMAGE — "Man and woman leaning over paperwork at desk, shoulders touching, classroom, charged moment"

**Exit**: "Pull away first" → +2 mark_desire, +1 mark_guilt | "Let him pull away" → +2 mark_desire, +1 corruption

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

**Exit**: "Walk him to the door professionally" → +3 mark_desire, +2 mark_guilt, reputation -2

---

**FOREPLAY NODE**: Door locked. She said it was because of the janitor — "he keeps walking in." Mark doesn't question it. He can't question it. He's beyond questions.

She sits on the edge of her desk. He stands between her legs. His hands on her thighs — familiar now, shaking less. She unbuttons the top of her blouse. One button. His eyes drop. She takes his hand and places it on her collarbone, then lower.

"We have fifteen minutes before the janitor's next round."

Fifteen minutes of his hands under her clothes, his mouth on her neck, her hand on his belt, both of them listening for footsteps. The principal's office is thirty feet away. His son sat in this chair this morning.

Nothing about this should work. Everything about it does.

**Media**: VIDEO — "Couple in classroom, her on desk, his hands on her thighs, door locked, intense forbidden encounter"

**Exit**: "Fix yourselves. Leave separately." → +4 mark_desire, +3 mark_guilt, reputation -3

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
- **Energy Cost**: -15
- **Money Cost**: -5 to -8 (drinks)

---

### Base Scene

**DEFAULT**: Jake's behind the bar. He moves like he owns it — spinning bottles, flipping towels, charming tips out of women twice his age. When she sits down, he slides a drink across the bar without asking. "On me." The smile. The lean. The eye contact that lasts one beat too long. Every move is practiced, polished, weaponized.

She doesn't take the bait. She orders her own drink. Pays for it. Doesn't smile back.

**WITHDRAWN variant** (post-`jake_ego_crisis`): He's working but off his game. Drops a glass. Over-pours a pint. He keeps glancing at her and looking away before she catches him — except she always catches him. The bravado is cracked and what's underneath is confused, hungry, and scared.

**WARM variant** (high `jake_power` toward her, post-`jake_kiss_unlocked`): He doesn't try the moves anymore. When she sits, he pours her drink correctly (neat, not the girly pour he used to give her) and sets it down without bravado. "Hey." Just "hey." The simplicity is more intimate than all his lines combined.

**Media**: IMAGE — "Bartender behind bar, tattoos, confident lean, woman sitting at bar with whiskey, challenge in her eyes"

### Choice Progression

| Choice Text | Condition | Node | Effects |
|-------------|-----------|------|---------|
| "Flirt and shut him down" | always | exit | +1 jake_power (toward her) |
| "Flirt with another man while Jake watches" | confidence >= 35 | warm | +2 jake_power, +1 corruption |
| "Lean over the bar, give him the view, walk away" | corruption >= 55 + jake_kiss_unlocked | kiss | +3 jake_power |
| "Tell him to meet you in the stockroom" | corruption >= 70 + jake_oral_unlocked | intimate | +4 jake_power, reputation -3 |

**Note**: Jake's `jake_power` stat is inverted — higher numbers toward her mean she's winning. Gains here shift the power dynamic, not increase affection.

### Escalation Nodes

**WARM NODE**: She's at the bar. A man — nobody, a trucker passing through — sits next to her and tries a line. She laughs. Touches the trucker's arm. Whispers something in his ear that makes him grin.

She doesn't look at Jake once. She doesn't need to. Jake's jaw is tight. His pour is heavy. He slams a glass down harder than necessary.

"Problem, Jake?"

"No problem."

"Good."

She pays the trucker's tab and walks out. Jake watches her go.

**Media**: IMAGE — "Woman flirting with man at bar while bartender watches jealously, dive bar, tension"

**Exit**: "Don't look back" → +2 jake_power, +1 corruption | "Glance at Jake at the door" → +1 jake_power, +2 corruption

---

**KISS NODE**: She leans across the bar to grab a napkin. The angle gives him the full view down her neckline. She takes her time. Straightens up. Catches him looking.

"See something you like?"

"You know I do."

"Hmm." She finishes her drink. Sets the glass down. Turns and walks toward the stairs. His eyes follow every step.

She doesn't go upstairs. She goes to the bathroom. Comes back five minutes later and sits down like nothing happened.

The denial is the weapon. She gives and takes away. Gives and takes away. He's Pavlov's dog and she's ringing the bell without feeding him.

**Media**: VIDEO — "Woman leaning across bar, cleavage visible to bartender, her smirk, his frustrated expression"

**Exit**: "Order another drink like nothing happened" → +3 jake_power

---

**INTIMATE NODE**: Bar closing. She catches his eye. Tilts her head toward the stockroom.

He follows. Through the STAFF ONLY door. Beer cases, one bulb, the door that doesn't lock. Jolene is closing out the register thirty feet away.

"On your knees."

He goes down. The cocky bartender kneels on the concrete floor of the stockroom and puts his mouth between her legs while she leans against the beer cases and listens to Jolene counting the drawer through the wall.

She runs her hand through his hair. Controls the pace. When he tries to speed up, she pulls his hair — gently. "Slower."

He slows.

Someone could walk in. The door doesn't lock. That's the point. The danger is part of the dominance — she's not just making him submit, she's making him submit where anyone could see.

**Media**: VIDEO — "Man on knees giving oral to woman in stockroom, beer cases, dim light, risk of discovery, she's in control"

**Exit**: "Enough. Go close the bar." → +4 jake_power, reputation -3

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
| "Talk" | always | exit | +1 jake_power |
| "Tell him where to sit" | jake_power <= 50 + jake_groping_unlocked | foreplay | +2 jake_power, +2 corruption |
| "Put him on his knees" | jake_power <= 35 + jake_oral_unlocked | intimate | +3 jake_power, +2 corruption |
| "Take him to bed. On her terms." | jake_power <= 20 + jake_sex_unlocked | intense | +3 jake_power, +3 corruption, +1 confidence |

### Escalation Nodes

**FOREPLAY NODE**: She points to the bed. "Sit." He sits. She stands between his legs. Takes his hands. Places them — waist, hips, thighs. Each new placement requires her permission.

"Move them."

He moves his hands up.

"Did I say you could?"

She puts them back. He learns. Every session, the rules clarify. He's being trained the way she trained Tom — except Tom's training was gentle. This is not.

**Media**: VIDEO — "Woman standing over seated man, placing his hands on her body, controlling his touch, bedroom, power dynamic"

**Exit**: "Send him home" → +2 jake_power, +2 corruption | "Keep going" → +3 jake_power, +1 corruption

---

**INTIMATE NODE**: "On your knees." Not the stockroom — her bedroom. Private. No audience, no danger of discovery. Just them. He kneels. She sits on the edge of the bed. His mouth between her legs.

She directs everything. Pace, pressure, position. He responds to her voice the way Tom responds to praise — except Jake doesn't want to be told he's good. He wants to be told what to do. Different mechanism. Same result: she's in absolute control.

"Faster."
"Stop."
"Again."

When she finishes, she lets him stay on the floor for a beat. Just a beat. Then: "Come up here."

**Media**: VIDEO — "Man on knees performing oral on woman sitting on bed edge, she directs him, intense, her control"

**Exit**: "Let him lie next to you" → +3 jake_power, +2 corruption | "Tell him to go home" → +2 jake_power, +3 corruption

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

**Exit**: "Let him stay" → +3 jake_power, +3 corruption | "Send him away" → +2 jake_power, +4 corruption, +2 confidence

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


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHASE 6: STORY ARC
# New In Town

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 0: DRAMATIC SPINE SUMMARY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Central Tension

**"Can a woman discover who she really is by becoming someone her former self would despise — and is the power she gains worth what she loses?"**

### Conflict Types (Per Arc)

| Arc | Primary Conflict | Secondary Conflict |
|-----|-----------------|-------------------|
| Jolene (Phase 1) | INTERNAL (shame vs. desire, upbringing vs. awakening) | EXTERNAL — the town is always watching |
| Tom | INTERNAL + MORAL (guilt over corrupting innocence; his devotion becomes a leash) | POWER — she practices control for the first time |
| Ray | INTERNAL + EXTERNAL (his refusal to see her; his developing real feelings she didn't plan for) | IDENTITY — he forces her to confront that she wants power, not partnership |
| Mark | EXTERNAL + MORAL (Karen's surveillance; reputation destruction; a child between them) | FORBIDDEN — the taboo is the engine, guilt is the lever |
| Jake | INTERNAL + POWER (his ego vs. her dominance; whether she's liberated or addicted to control) | ENDGAME — the question of what she's become |

### Tension Curve Summary (Multi-Arc)

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

### Key Emotional Beats — JOLENE ARC (Phase 1)

| Beat | Event | Emma Feels | Emma Phase |
|------|-------|-----------|-----------|
| Arrival | Opening — Millfield, Jolene, the room | Displacement, culture shock | SHELTERED |
| First Exposure | Thin Walls — hears Jolene with a man | Horror + curiosity she can't name | SHELTERED → edge of CURIOUS |
| Deepening | Wine dinner, cracked door, exposure therapy | Shame fading, desire surfacing | CURIOUS |
| Turning Point | Self-discovery dare | Liberation or frustration | CURIOUS → AWAKENED |
| Phase 1 Close | "There She Is" — noticing men | Hunger she doesn't know what to do with | AWAKENED |

### Key Emotional Beats — TOM ARC

| Beat | Event | Emma Feels | NPC Feels | NPC Quadrant |
|------|-------|-----------|-----------|-------------|
| First Spark | The Excuse — lock check | Curiosity + power discovery | Awestruck / stammering | DEVOTED (instant) |
| Testing | Classroom Setup | Intoxication of control | Overwhelmed / eager to please | DEVOTED |
| Breakthrough | The Classroom Catch (kiss) | "I can make a man do this" | World rebuilt | DEVOTED |
| Deepening | Good Boy (oral) | Power addiction begins | Surrender / "good boy" awakening | SURRENDERED |
| Culmination | First Time (sex — his virginity) | Pure control, first guilt flicker | Absolute devotion | SURRENDERED |

### Key Emotional Beats — RAY ARC

| Beat | Event | Emma Feels | NPC Feels | NPC Quadrant |
|------|-------|-----------|-----------|-------------|
| First Frustration | Invisible Wall | Sting of failure, ego bruised | Indifferent / categorized her | DISTANT |
| First Crack | Plumbing + whiskey | Triumph of being seen | Surprise / reframing | DISTANT → NOTICING |
| Emotional Connection | Truck Conversation | He's real, not just a conquest | Opening up / choosing to see her | WARMING |
| Physical First | The Shed (groping before kiss) | Raw arousal, body before emotion | Body admits what mind won't | WANTING |
| His Surrender | The Staircase (kiss) | Victory + respect earned | Resistance collapsed | WANTING → OPEN |
| Complication | Feelings Emerge | Didn't plan for this | Falling for her, real feelings | OPEN → complicated |
| Culmination | Upstairs (sex) | Revelation — she wants power, not partnership | Fully invested | OPEN |

### Key Emotional Beats — MARK ARC

| Beat | Event | Emma Feels | NPC Feels | NPC Quadrant |
|------|-------|-----------|-----------|-------------|
| The Read | First Conference | Calculated interest, sees the hollow man | Starved for attention | DISTANT (performing) |
| The Build | Fundraiser Volunteer | Patient manipulation | Emotional intimacy he's never had | WARMING |
| The Break | The Rain (almost-kiss + texts) | The taboo is electric | Guilty, desperate, can't stop | CONFLICTED |
| Escalation | Under the Desk | Boldest move yet — at her workplace | Terrified excitement | CONFLICTED → CONSUMING |
| The Bridge | Phone Call from Bedroom | No guilt, none — that's new | Coming apart, wife downstairs | CONSUMING |
| Culmination | No Hesitation (sex) | She owns his guilt | Guilt becomes the engine | SURRENDERED |
| CRISIS | Karen finds text, school confrontation | Ice-cold composure, perfect liar | Terror, three days of silence | CRISIS |
| Repair | Parking Lot | Power or release — her choice | Wrecked, crawling back | CRISIS → recovery |

### Key Emotional Beats — JAKE ARC

| Beat | Event | Emma Feels | NPC Feels | NPC Quadrant |
|------|-------|-----------|-----------|-------------|
| The Laugh | Second Rejection | Delight — she's beyond him | Confusion, first real rejection | EGO INTACT |
| The Campaign | Jealousy Game | Calculated, surgical | Rattled, losing grip | EGO CRACKING |
| The Taunt | Pour Me One More | "You want me so badly it's almost sweet" | Ego shattering | EGO CRACKING → BROKEN |
| The Admission | Ego Crisis — "What do you want from me?" | She's won | Genuine confusion, identity crisis | BROKEN |
| First Kiss | Not Yet (kiss) | She rewards "please" | He said please — first time ever | SUBMITTING |
| The Rules | Permission (groping) | Pure dominance | Discovers he likes being told | SUBMITTING |
| The Risk | Stockroom (oral) | Three months ago she cried after missionary | Worshipping her, 20 feet from Jolene | SURRENDERED |
| Culmination | On Her Terms (sex) | Total power — the transformation is complete | "Please" — the most powerful word | SURRENDERED |
| Endgame | The Surrender — keep or discard | What she's become | Asking for direction in life | SURRENDERED |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: CHAPTERS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| ID | Name | Mood | Description | Order |
|----|------|------|-------------|-------|
| chapter_prologue | Millfield | hopeful | Emma arrives with two suitcases and a Bible. Jolene takes one look at her and grins. The room is small, the walls are thin, and the whole town already knows her name. | 1 |
| chapter_awakening | The Awakening | tense | Jolene doesn't touch her — she exposes her. Thin walls, cracked doors, wine, dares. Twelve days of shame dissolving into curiosity into hunger. Emma stops looking away and starts looking. | 2 |
| chapter_first_hunt | First Blood | romantic | Tom is training wheels. Easy, devoted, pathetically grateful. She learns to lead, to direct, to say "good boy" and watch a man melt. The power is intoxicating and she wants more. | 3 |
| chapter_proving | Proving Ground | passionate | Ray won't see her. Then he can't stop seeing her. Mark is hollow and she fills him with fire. Two arcs running parallel — confidence through seduction, manipulation through the forbidden. | 4 |
| chapter_crisis | What Burns | tense | Karen finds the text. The school buzzes. Reputation bleeds. Ray develops feelings she didn't plan for. The juggling act starts cracking and she has to decide what she's willing to lose. | 5 |
| chapter_endgame | The Endgame | passionate | Jake kneels. The cocky bartender says "please." She controls everything — the bar, the men, the town's perception. The girl with the Bible is gone. The woman in the mirror smiles, and the smile isn't kind. | 6 |
| chapter_mirror | What She Became | neutral | Four mirrors. Four versions of herself. The cardigan, the dress, the underwear, the eyes that calculate before they care. Whatever she is now, she chose it. Every step. | 7 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: STORY NODES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Opening

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| arrival | Arrival in Millfield | chapter_prologue | opening_arrival | game_started | true | "Two suitcases. A backpack with a Bible Mom packed. A town that looks like it fell asleep in 1985. The woman behind the bar took one look at me, grinned, and grabbed my suitcase without asking. 'Room's upstairs. Walls are thin.' I don't know what she means yet." |

### Phase 1: Jolene's Corruption Arc

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| culture_shock | Culture Shock | chapter_awakening | jolene_culture_shock | school_started | true | "She walks around in her underwear like her body isn't something to be embarrassed about. She swears. She touches men's arms when she laughs. She poured me chili and wine and called me 'hon.' I ate the chili and tried not to stare. I failed." |
| thin_walls | Thin Walls | chapter_awakening | jolene_thin_walls | jolene_thin_walls | true | "I should have put in earbuds. I should have prayed. I lay there in the dark and listened to every sound through the wall and I don't have a word for what I felt. Not disgust. Something that scared me more than disgust." |
| wine_dinner | Wine and Honesty | chapter_awakening | jolene_wine_dinner | jolene_wine_dinner | false | "Two glasses of wine and she asked me about sex. I said 'fine.' She looked at me like I'd said the saddest word in the English language. Maybe I did. She talked about desire like it was a natural thing — not a sin. I listened and my glass was empty again and I don't remember drinking it." |
| cracked_door | The Cracked Door | chapter_awakening | jolene_peek_event | jolene_peek_event | true | "She left the door cracked on purpose. I know she did. She saw me standing there and she smiled and she didn't stop. I ran to my room and sat on the bed and my heart was hammering and my hands were shaking and I was horrified. And something else. Something I don't have a name for yet." |
| exposure_therapy | Exposure Therapy | chapter_awakening | jolene_exposure_therapy | jolene_exposure_therapy | false | "The vibrator in the bathroom. The laptop left open. She's not being careless — she's teaching me. Not with words. With evidence that desire exists and the world doesn't end when you see it." |
| shopping_trip | The Shopping Trip | chapter_awakening | jolene_shopping_trip | jolene_shopping_trip | true | "She bought me a dress. Black. Short. I looked in the dressing room mirror and I didn't look like myself. I looked like someone who might be wanted. The thought hit me in the chest. 'You've got legs, girl. Fucking use them.'" |
| self_discovery | Figure It Out | chapter_awakening | jolene_self_discovery | phase_1_complete | true | "She told me to go to my room. Lock the door. Figure it out. And I did. Or I tried. Either way — something opened. Something I was taught to keep shut. Jolene didn't touch me. She didn't have to. She just showed me the door and dared me to walk through it." |
| phase_1_close | There She Is | chapter_awakening | jolene_phase_1_complete | phase_1_complete | true | "I sat at the bar in the dress and ordered wine without hesitating. Ray's arm brushed mine and I didn't flinch. Jake winked and I held his gaze. Tom walked in and his mouth opened. Jolene looked at me and said: 'There she is.' I don't know who 'she' is yet. But I want to find out." |

### Tom Arc

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| tom_excuse | The Excuse | chapter_first_hunt | tom_locks_checked | tom_locks_checked | true | "Jolene said to tell him I don't feel safe alone at night. He was at my door in thirty seconds. Clean shirt. Smelled like he showered. For a lock check. He inspected every window like he was saving me from a fire. And I watched his hands and thought: this is going to be easy." |
| tom_classroom | Classroom Setup | chapter_first_hunt | tom_classroom_setup | tom_classroom_setup | false | "I bent over in front of him to pick up tape. Slowly. His ears turned red. He dropped the banner. He can't form sentences when I stand close. I'm learning — every blush is data, every stammer is proof I have power over this man. The discovery is intoxicating." |
| tom_catch | The Classroom Catch | chapter_first_hunt | tom_classroom_catch | tom_kiss_unlocked | true | "I 'tripped.' He caught me. His hands on my waist. His heartbeat through his shirt. He was frozen — not from fear, from having no framework for what to do when a woman wants him close. So I closed the distance. I kissed him. Or I almost did. Either way — he's mine now." |
| tom_confession | Tom's Confession | chapter_first_hunt | tom_devotion_confession | tom_devotion_confession | false | "He told me about his dad. The heart attack. The badge he inherited. How he never left Millfield because leaving felt like abandoning a ghost. He's me — who I was two weeks ago. Trapped by expectations, never having seen an alternative. I'm about to break him out of that cage. The same way Jolene broke me out of mine." |
| tom_movie | Movie Night | chapter_first_hunt | tom_movie_night | tom_groping_unlocked | true | "Gas station flowers. The most heartbreaking thing I've ever seen. He sat rigid while I put his hand on my thigh. I pushed him against the headboard and kissed him and said: 'You're going to learn. And I'm going to teach you.' His face — wrecked, grateful, terrified. This is what power looks like up close." |
| tom_good_boy | Good Boy | chapter_first_hunt | tom_good_boy | tom_oral_unlocked | true | "I said 'good boy' without thinking. And the moment I said it, I saw his eyes change. Not embarrassment. Something deeper. He liked being directed. He liked being my student. This isn't about sex anymore. This is about control. And I like it more than the physical part." |
| tom_first_time | First Time | chapter_first_hunt | tom_first_time | tom_sex_unlocked | true | "I took his virginity on my terms. On top. His hands pinned. His face — someone rebuilt his entire world. 'I'd do anything for you.' He means it. He's the most honest person in this town and I'm the most dishonest thing that's ever happened to him. Something flickered. Guilt? I pushed it down." |

### Ray Arc

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| ray_wall | The Invisible Wall | chapter_proving | ray_invisible_wall | ray_invisible_wall | true | "Nothing. Zero reaction. He calls me 'Miss' and nods politely and goes back to his beer. I tried everything that worked on Tom — standing close, touching his arm, laughing. Nothing. I'm wallpaper. Jolene said: 'He's decided you're a category he doesn't touch. Break the drawer.'" |
| ray_crack | First Crack | chapter_proving | ray_first_crack | ray_first_crack | true | "I opened the door in a tank top and shorts. No bra. 'Sorry, wasn't expecting you this early.' I was expecting him exactly when he came. He glanced back and caught me looking at his shoulders. Looked away quick. Quicker than a man who felt nothing would need to. First crack." |
| ray_truck | The Truck Conversation | chapter_proving | ray_truck_conversation | ray_truck_conversation | false | "He told me about his daughter. The custody fight. The birthday he missed. His eyes were wet. I put my hand on his arm and left it there. He looked at me like he was seeing me for the first time. 'You're not what I expected, Miss.' 'Emma.' '...Emma.' The way he said my name was worth more than anything Tom ever stammered." |
| ray_shed | The Shed | chapter_proving | ray_shed_scene | ray_groping_unlocked | true | "His chest against my back. His arms alongside mine. The saw forgotten. I pressed back into him and felt him respond and neither of us moved. His body admitted what his mind won't. Ray's physical gate fires before the emotional one — that's who he is. Action before acknowledgment." |
| ray_staircase | The Staircase | chapter_proving | ray_staircase_kiss | ray_kiss_unlocked | true | "He kissed me. Hard. Not tentative like Tom — Ray has been kissing women for twenty years. But this one cost him something. 'This is a bad idea.' 'I know.' My hand reached for his belt. 'Goodnight, Ray.' I walked upstairs. Didn't look back. He stood there a long time." |
| ray_daughter | The Daughter | chapter_proving | ray_daughter_story | ray_daughter_story | false | "A photo in his wallet. A girl missing a front tooth. He talked about driving to the next town every other weekend and pretending two days is enough. His hands shake when he talks about her. This is the complication I didn't plan for — Ray is becoming a real person to me. Not a conquest. A man." |
| ray_truck_oral | The Truck | chapter_proving | ray_truck_oral | ray_oral_unlocked | true | "In the cab of his truck. Dark parking lot. I dropped to my knees between the seat and the dash. 'Jesus, Em—' I didn't let him finish the sentence. For the first time with Ray — he let me lead." |
| ray_feelings | Feelings | chapter_crisis | ray_feelings_emerge | ray_feelings_emerge | true | "He's falling for me. Jolene said it plain: 'If you're playing him, decide now — if you break that man, he doesn't come back. He has a kid.' I didn't plan for feelings. Hers or mine. I said either 'I know what I'm doing' or 'I didn't plan for this.' One is a lie. I'm not sure which." |
| ray_upstairs | Upstairs | chapter_proving | ray_upstairs | ray_sex_unlocked | true | "Ray knows what he's doing. He took charge. I gasped — actually gasped, unperformative — and for a moment I wasn't in control. Afterward I lay there and realized: I didn't like it. Not the sex — the sex was incredible. I didn't like not being in control. Ray taught me what I actually want. Not good sex. Power." |

### Mark Arc

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| mark_conference | First Conference | chapter_proving | mark_first_conference | mark_first_conference | true | "Parent-teacher conference. He came alone — Karen has a 'headache.' He lingered. Asked questions unrelated to his kid. Laughed at things that weren't funny. He's starved. Hollow. A man sleepwalking through a life someone else designed. I touched his hand giving him the report card. 'He must get it from you.' He'll think about that sentence for three days." |
| mark_volunteer | The Volunteer | chapter_proving | mark_fundraiser_volunteer | mark_fundraiser_volunteer | false | "He invented the fundraiser excuse. We work late in the classroom. He brings coffee. The conversation is personal — his marriage, his job, the sleepwalking. I said: 'That must be lonely.' The word 'lonely' hit him like a brick. Nobody names it for him. I did." |
| mark_rain | The Rain | chapter_proving | mark_rain_umbrella | mark_kiss_unlocked | true | "One umbrella. I pressed against him. Shivered. He put his arm around me. We stopped walking. His eyes dropped to my mouth. He almost kissed me. Pulled back. 'I should go.' That night she texted: 'I keep thinking about the rain.' He texted back. The barrier breaks through screens." |
| mark_desk | Under the Desk | chapter_proving | mark_under_desk | mark_groping_unlocked | true | "His hand on my thigh under the desk. His thumb moving against my skin — memorizing the texture of the line he's crossing. Footsteps in the hallway. We separate. Professional smiles. 'Same time Thursday?' Every escalation risks my career. The principal's office is down the hall. The danger is the point." |
| mark_phone | The Phone Call | chapter_proving | mark_call_from_bedroom | mark_call_from_bedroom | false | "I called him at 10pm. 'Karen's downstairs.' I listened to him come apart over the phone while his wife was one floor below. The taboo isn't incidental — it's the engine. The closer Karen is, the hotter it burns. Afterward I hung up and looked at the ceiling. No guilt. None. That's new." |
| mark_visit | The First Visit | chapter_proving | mark_first_visit | mark_oral_unlocked | true | "'Karen thinks I'm at a meeting.' His hands were shaking. I didn't rush it. Made coffee. Let the tension build — I've learned this from Jolene, from Tom, from Ray. Tension is a tool. You shape it. Then I pushed him down and controlled the pace. His guilt makes him harder. I'm learning guilt the way I learned Tom's devotion — as a lever." |
| mark_no_hesitation | No Hesitation | chapter_proving | mark_no_hesitation | mark_sex_unlocked | true | "He came back. No shaking hands. No preamble. He walked in and knew what he was here for. Afterward: 'What did I do. Oh God.' I said either 'You did what you wanted' or 'We both wanted this.' One gives me his guilt. The other gives me his comfort. Both bring him back tomorrow." |
| karen_crisis | Karen | chapter_crisis | karen_crisis | karen_school_confrontation | true | "She showed up at my school. Mid-morning. 'We need to talk. Now.' I played it perfectly. Calm. Professional. Slightly hurt. She searched my face for the crack. She didn't find it. Because I'm not guilty. I'm performing. And I'm better at it than she ever expected. My hands are steady. My heart rate is normal. I just lied to a wife about sleeping with her husband and I feel nothing." |
| mark_repair | The Parking Lot | chapter_crisis | mark_crisis_repair | mark_crisis_repair_complete | true | "11pm. His car. Third row. He looks wrecked. 'She knows. She doesn't have proof, but she knows.' He looked at me like I was either the devil or the only thing keeping him alive. Maybe both. I chose to pull him deeper or let him go. Either way — he comes back. They always come back." |

### Jake Arc

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| jake_rejection | The Second Rejection | chapter_endgame | jake_second_attempt | jake_second_attempt | true | "He tried the lazy smile. The lean. 'So, you finally loosened up.' I laughed. AT him. Nobody laughs at Jake. He stood behind the bar holding a glass he forgot to dry. For the first time in his adult life, he processed rejection that doesn't sting — it confuses." |
| jake_jealousy | The Jealousy Game | chapter_endgame | jake_jealousy_game | jake_jealousy_game | false | "I flirted with other men while he watched. Touched their arms. Whispered close. Glanced at Jake to make sure he saw. The message: you're not the prize. I am. His jaw tightened. His pours got sloppy. Jolene noticed. He lied about it." |
| jake_bar | Pour Me One More | chapter_endgame | jake_bar_sitting | jake_bar_sitting | true | "I sat on the bar. Legs crossed. 'Pour me one more.' He poured. I drank slowly. 'You want me so badly it's almost sweet.' He reached for me. I put one finger on his lips. 'Not yet.' Walked upstairs. I could hear him say to nobody: 'What the fuck.'" |
| jake_ego | The Ego Crisis | chapter_endgame | jake_ego_crisis | jake_ego_crisis | false | "'What the fuck do you want from me?' Not a line. Genuine confusion. His ego — the thing he built his entire identity on — is cracking. He's spent his life being the one who pursues. I've inverted everything. He punched the jukebox and went out the back door." |
| jake_kiss | Not Yet | chapter_endgame | jake_not_yet | jake_kiss_unlocked | true | "'One kiss. Please.' That word — please — is something Jake has never said to a woman in his life. I stepped forward. One kiss. Brief. My terms. My hand controlling the angle. I pulled away first. 'Good.' He stood there touching his lips like they were someone else's." |
| jake_permission | Permission | chapter_endgame | jake_permission | jake_groping_unlocked | true | "'You can touch me. But only where I say.' He reached for my waist. I moved his hands to my hips. He moved them up. I stopped. 'Did I say you could move them?' Something shifted in his eyes. Recognition. He likes being told what to do. The cocky bartender likes surrendering." |
| jake_stockroom | The Stockroom | chapter_endgame | jake_stockroom | jake_oral_unlocked | true | "I put him on his knees in the stockroom. Twenty feet from Jolene. Behind a door that doesn't lock. Three months ago I cried after missionary sex with the lights off. Now I'm standing against beer cases with my hand in a man's hair while he worships me. The girl with the Bible would be horrified." |
| jake_on_her_terms | On Her Terms | chapter_endgame | jake_on_her_terms | jake_sex_unlocked | true | "My room. My terms. I told him when to arrive, what to wear, where to stand. He complied. I pinned his hands. 'Did I say you could touch?' He arched into it. He discovered — and I saw the moment — that the ego was armor, not identity. 'Please.' The most powerful word in the game from someone who's never said it." |
| jake_endgame | The Surrender | chapter_endgame | jake_endgame_choice | jake_endgame_choice | true | "He sat on my bed. Not for sex. 'What do you want me to do?' Not in bed. In life. I built this. I broke him down and rebuilt him. I said 'Stay' or 'I don't need you to do anything. That was the point.' One keeps him. The other proves I never needed him. Both are true." |

### Mirror Scenes

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| mirror_20 | Mirror — Day 20 | chapter_mirror | mirror_day_20 | mirror_day_20 | true | "The dress. Makeup I didn't own two weeks ago. My hair is down. Something is different — not the clothes. The eyes. They're not looking for permission anymore. They're measuring. The Bible is on the nightstand. I haven't opened it in a week." |
| mirror_40 | Mirror — Day 40 | chapter_mirror | mirror_day_40 | mirror_day_40 | true | "I stand in my underwear and I don't flinch. These legs made Ray forget I was 'the schoolteacher.' These lips said 'good boy' to Tom. This body is a weapon I didn't know I carried. I think about three men and feel nothing resembling guilt. The Bible is in the drawer. Face down." |
| mirror_60 | Mirror — Day 60 | chapter_mirror | mirror_day_60 | mirror_day_60 | true | "I barely recognize myself. Not the clothes. Not the body. The eyes. The way my smile has changed from warm to something sharper. The girl who arrived with a cardigan and a Bible would be horrified. Would cry. Would pray. I look at that ghost and smile. The smile isn't kind. The Bible is gone. I threw it away three weeks ago. I don't remember which day." |

### Cross-NPC Events

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| friday_collision | Friday Night Collision | chapter_crisis | friday_collision | friday_collision | false | "Four men. One room. Tom in the corner, off duty. Ray at his stool. Jake behind the counter. And Mark — without Karen — catching my eye across the room. I have to choose who to focus on while the others watch. Three months ago I didn't know how to talk to one man. Now I'm juggling four." |
| tom_saw_ray | Tom Sees Ray | chapter_crisis | tom_saw_ray | tom_saw_ray | true | "Tom saw me touch Ray's arm. The body language. His face changed. He sat in a corner booth with a beer he didn't drink. Later: 'Are you and that handyman... is something happening?' I had to choose — lie, redirect, or be honest-ish. None of the options make me a good person. All of them work." |
| ray_sees_text | Ray Sees the Text | chapter_crisis | ray_sees_mark_text | ray_sees_mark_text | false | "My phone buzzed. A text from Mark. Ray saw the screen. Five minutes of silence. 'Who's Mark?' 'Nobody.' 'Didn't look like nobody.' I touched his arm. Changed the subject. He let it go. But the seed is planted." |
| juggling | Juggling Detected | chapter_crisis | juggling_detected | juggling_detected | false | "Mrs. Hewitt at the general store: 'You've certainly made a lot of friends in town, haven't you, dear?' The tone said everything the words didn't. The schoolteacher has coffee with the deputy, drinks with the handyman, and the insurance agent's car has been near the bar after hours. The town is small. Patterns are noticed." |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: GROUPS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Complete N of M" parallel activity requirements. These define story beats that can be achieved through multiple routes.

| ID | Name | Required Count | Member Nodes | Chapter |
|----|------|----------------|-------------|---------|
| phase1_progression | Breaking Through | 5 | culture_shock, thin_walls, cracked_door, shopping_trip, self_discovery | chapter_awakening |
| first_conquest | First Conquest | 1 | tom_catch, ray_shed | chapter_first_hunt |
| multi_arc_active | Multiple Pursuits | 2 | tom_catch, ray_staircase, mark_rain, jake_kiss | chapter_proving |
| crisis_experienced | Facing Consequences | 1 | karen_crisis, ray_feelings, juggling | chapter_crisis |
| bridge_witnessed | Seeing the Real Person | 1 | tom_confession, ray_daughter, mark_phone, jake_ego | chapter_proving |
| deep_intimacy | Full Corruption | 1 | tom_first_time, ray_upstairs, mark_no_hesitation, jake_on_her_terms | chapter_endgame |
| mirror_progression | The Mirror | 2 | mirror_20, mirror_40, mirror_60 | chapter_mirror |

### Group Purposes

**phase1_progression**: Emma must experience the core Jolene corruption beats before Phase 2 opens. Ensures the awakening is felt as a gradual process, not a switch.

**first_conquest**: At least one first gate (kiss or groping) must fire before the player accesses mid-game content. Ensures she's practiced before harder arcs.

**multi_arc_active**: The player must have kiss gates on 2+ NPCs before cross-NPC events fire. Ensures the juggling mechanic has substance.

**crisis_experienced**: At least one crisis event must fire before Jake's endgame. Ensures the player understands consequences before the power fantasy climax.

**bridge_witnessed**: Bridges can be missed. This tracks whether the player experienced at least one character-deepening moment that shows NPCs as real people.

**deep_intimacy**: The final sex gate on any route opens endgame content. Ensures the player earns the culmination.

**mirror_progression**: At least 2 of 3 mirror scenes seen. The transformation tracker is the game's emotional backbone.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: EMOTION MAPPINGS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Tom — Primary Stat: `tom_devotion`

| Min | Max | Label | Description | NPC Behavior |
|-----|-----|-------|-------------|-------------|
| 0 | 20 | nervous | "He can barely look at me. Stammers my name. Drops things when I'm in the room." | Stammering. Can't hold eye contact for more than a second. Stands too far away. Blushes when she speaks to him. Calls her "Miss." His hands fidget constantly. A golden retriever who's been called over but is too scared to come. |
| 21 | 40 | smitten | "He shows up. Every time. Before I ask. He's started finding reasons to be where I am." | Shows up early. Brings coffee. Rehearses what he'll say (she can tell). Makes eye contact now — for two seconds, then away. Laughs at everything she says. His whole body orients toward her like she's magnetic north. |
| 41 | 60 | devoted | "He'd do anything I said. He doesn't know that yet. But I do." | Follows instructions without question. His face lights up when she enters a room. Physical proximity has become natural — shoulder touches, sitting close. He waits for her. He saves things for her. He is hers and he's starting to realize it. |
| 61 | 80 | addicted | "He called me four times today. Drove past the bar twice. He's not a person anymore — he's a satellite orbiting me." | Constant availability. Texts immediately. Cancels plans for her. His happiness is visibly dependent on her attention. Jealousy appears — mild but noticeable. He covers for her without being asked. He'd lie to God for her. |
| 81 | 100 | surrendered | "'I'd do anything for you.' The scariest part is that I believe him. The scarier part is that I like it." | Complete surrender. No independent will regarding her. He is an extension of her desires — covers for her, lies for her, looks the other way. "Good boy" makes his eyes close. She could destroy him with one sentence. He knows. He doesn't care. |

---

### Ray — Primary Stat: `ray_interest`

| Min | Max | Label | Description | NPC Behavior |
|-----|-----|-------|-------------|-------------|
| 0 | 20 | indifferent | "I'm wallpaper. He calls me 'Miss' and goes back to his beer." | Polite nods. "Ma'am." One-word answers. She could be any barstool. He literally doesn't register her as a sexual being. Category: locked drawer. |
| 21 | 40 | noticing | "He said my name. Not 'Miss.' My name. And the way he said it — slow, like he was testing whether it fit in his mouth." | Surprise at things she does. Longer looks. Real sentences. He starts correcting the category — she's not a kid, she's... something. His eyes do the quick drop-and-snap-back when she wears the dress. |
| 41 | 60 | wanting | "He finds reasons to be where I am. Fixes things that aren't broken. His body admitted what his mind won't." | Seeks proximity. Stands closer. Physical tension — jaw tight when she's near. His hands grip things harder. He's fighting attraction and losing. The strong-silent-type facade develops cracks. |
| 61 | 80 | invested | "He told me about his daughter. His voice broke. This isn't what I planned. He's becoming a real person." | Real conversation. Vulnerability. He waits for her specifically. His arm brushes hers and neither moves. The "bad idea" language has stopped — he's past resistance. Real feelings are surfacing and they scare both of them. |
| 81 | 100 | falling | "He said 'I was thinking about you today.' Ray doesn't say that. That sentence is a symptom of something I might not be able to control." | Emotional availability she didn't ask for. Shows up sober. Saves her stool. Says things a man falling in love says. The complication: she wanted conquest, not connection. His feelings are a variable she can't manage with confidence alone. |

---

### Mark — Primary Stat: `mark_desire`

| Min | Max | Label | Description | NPC Behavior |
|-----|-----|-------|-------------|-------------|
| 0 | 20 | professional | "He shakes my hand. Asks about his son's grades. Goes home to Karen." | Parent mode. Professional warmth. He asks relevant questions, maintains appropriate distance, leaves on time. She's his kid's teacher. Nothing more. |
| 21 | 40 | hungry | "He lingers. Asks questions unrelated to his kid. Laughs at things that aren't funny. He's starved for attention and doesn't know I can see it." | Lingering. Manufactured proximity. His eyes stay on her face when she talks — not looking at her body, but at her *attention*. He's feeding on being seen. The hollow man has found a light source. |
| 41 | 60 | reckless | "He closed the door. Sat too close. His hand on my thigh under the desk — his thumb moving like he was memorizing the line he was crossing." | Bold gestures in dangerous places. Texts at midnight. Creates excuses Karen can't verify. His guilt and his desire are in a death match and desire is winning. Touch is desperate, furtive, charged with the knowledge that a family is ticking like a bomb. |
| 61 | 80 | desperate | "He showed up at my door with shaking hands. 'Karen thinks I'm at a meeting.' He knew what he was here for. He just needed me to not judge him for it." | Night visits. The pretense of meetings. His guilt makes him harder — she knows this, she uses it. He can't stop and he's stopped trying to. Every session gets bolder. He calls from the bedroom while Karen watches TV downstairs. |
| 81 | 100 | owned | "He walked in. No preamble. No 'Karen thinks.' He doesn't mention her anymore. I own the part of him she never knew existed." | Complete enthrallment. He's reorganized his life around access to Emma. The guilt has burned itself out or become the fuel. He doesn't apologize anymore. He doesn't mention Karen unless forced. She is his real life; the house with Karen is the performance. |

### Mark — Secondary Stat: `mark_guilt`

| Min | Max | Label | Description | NPC Behavior |
|-----|-----|-------|-------------|-------------|
| 0 | 15 | suppressed | "He's convinced himself this isn't cheating. 'We just talk. We just text.' The lie is so clean he almost believes it." | Rationalization mode. Compartmentalized. Functions normally at home. The affair exists in a sealed box he opens at her door. |
| 16 | 30 | gnawing | "He panics after every time. 'What did I do.' Then he texts the next day." | Post-encounter panic followed by gravitational return. Guilt spikes after contact, fades between visits. The cycle is accelerating. |
| 31 | 45 | corrosive | "He can't look at his son. He snaps at Karen for no reason. The guilt isn't about Emma — it's about the man he sees in the bathroom mirror." | Behavioral deterioration at home. Short temper. Avoidance of son's eyes. Drinks more. The guilt is spreading from the affair into his entire self-image. |
| 46 | 60 | consuming | "He's stopped sleeping. 'She looks at me like she doesn't recognize me.' The worst part: she's right." | Visible collapse. Weight loss. Work performance drops. Karen asks what's wrong. He says "nothing" and the word tastes like ash. He needs Emma to tell him he's not a monster. |

---

### Jake — Primary Stat: `jake_power` (inverted: 100 = his control, 0 = her control)

| Min | Max | Label | Description | NPC Behavior |
|-----|-----|-------|-------------|-------------|
| 80 | 100 | cocky | "He thinks he runs this bar, this town, every woman who walks through the door. The smile is lazy because he's never had to try." | Full bravado. Reflexive flirting. Eye-fuck on autopilot. He uses the lean, the wink, the 'wanna get out of here.' Every interaction is a performance of control he's never questioned. |
| 60 | 79 | rattled | "Nobody laughs at Jake. She laughed. And now he can't stop watching her talk to other men." | Confusion. Overcorrection — tries harder, fails harder. Watches her with other men and his pours get sloppy. The smile is still there but it's thinner. He's processing an emotion he doesn't have vocabulary for. |
| 40 | 59 | cracking | "'What the fuck do you want from me?' That's not a line. That's genuine confusion. His ego is cracking and he doesn't have a framework for existing without it." | Ego crisis. Behavior changes — shows up sober, stops flirting with others, tries to impress her specifically. He punches the jukebox. He goes out the back door. The armor is coming off and what's underneath scares him. |
| 20 | 39 | submitting | "'One kiss. Please.' He said please. Jake has never said please to a woman in his life." | Submission emerging. He follows her instructions. "Did I say you could move them?" and he learns fast. The discovery that he likes being directed is visible — his eyes change, his breathing changes. The cocky bartender is becoming someone else. |
| 0 | 19 | surrendered | "'What do you want me to do?' Not in bed. In life. The ego is gone. She broke him down and rebuilt him." | Complete surrender. He asks for direction. He waits for permission. The man who flirted with every woman in Millfield sits on her bed asking what to be. She built this. He's either hers completely, or proof that she never needed him at all. |

---

### Player Stat: `corruption`

| Min | Max | Label | Description |
|-----|-----|-------|-------------|
| 0 | 10 | sheltered | "I say 'gosh' unironically. I owned one boyfriend and felt guilty about it. The world has rules and I follow them." |
| 11 | 25 | curious | "I listened through the wall longer than I should have. I looked when I should have looked away. Something is opening and I can't close it." |
| 26 | 45 | experimenting | "I kissed him because I wanted to. I wore the dress because I liked what it did to his face. I'm not following rules anymore — I'm testing them." |
| 46 | 65 | calculating | "I know guilt is a lever. I know devotion is a tool. I know exactly what my body does to men and I use it the way Jolene taught me — deliberately." |
| 66 | 85 | predatory | "I made a man come apart on the phone while his wife was downstairs. I laughed at the cocky bartender until his ego cracked. I feel nothing resembling guilt. That's new. That's power." |
| 86 | 100 | transformed | "The girl with the Bible would be horrified. I threw it away three weeks ago. I don't remember which day. The woman in the mirror smiles, and the smile isn't kind." |

### Player Stat: `confidence`

| Min | Max | Label | Description |
|-----|-----|-------|-------------|
| 0 | 15 | timid | "I can't hold eye contact. I stammer when men look at me. I'm invisible and I feel invisible." |
| 16 | 30 | testing | "I wore the dress. I stood close. I bent over slowly. Every blush, every stammer — that's data. Proof I have power." |
| 31 | 50 | deliberate | "I don't fumble anymore. I choose when to smile, when to touch, when to look away. Every move is intentional." |
| 51 | 70 | commanding | "'You're going to learn. And I'm going to teach you.' I said it and meant it. I direct. I control. I know what I want and I take it." |
| 71 | 100 | absolute | "I sat on the bar with my legs crossed and told a man 'you want me so badly it's almost sweet.' He reached for me. I put one finger on his lips. 'Not yet.' I own every room I walk into." |

### Player Stat: `reputation`

| Min | Max | Label | Description |
|-----|-----|-------|-------------|
| 70 | 100 | respectable | "The sweet new teacher. Church every Sunday. Volunteers with the kids. Mrs. Hewitt at the store smiles when I come in." |
| 50 | 69 | noticed | "People are talking. Not loudly — not yet. But the coffee with the deputy, the drinks with the handyman... patterns are noticed." |
| 30 | 49 | suspicious | "The principal 'checks in' during meetings. Karen sits in her car watching the school. Mrs. Hewitt's smile has a question mark behind it." |
| 10 | 29 | damaged | "The town has decided. Not proven — decided. The schoolteacher at the bar. The married man's car. The whispers that stop when I walk in." |
| 0 | 9 | destroyed | "Game over territory. The school board is 'reviewing my contract.' The church stopped inviting me to volunteer. The town has made its judgment." |

---

### Cross-State Descriptions

#### Tom Cross-States

| tom_devotion | corruption | Quadrant | Description |
|-------------|-----------|----------|-------------|
| 0-20 | 0-10 | STRANGER | "He's the deputy who checked my locks. Nice. Nervous. I barely know him but he'd run through a wall for anyone who asked politely." |
| 0-20 | 11-25 | NOTICING | "I looked at him differently after the dress. He's tall. His hands are big. He stammers when I smile. I'm starting to understand what that means." |
| 21-40 | 11-25 | TARGET | "He's my practice run. Training wheels. The way his ears turn red when I stand close is the most intoxicating thing I've ever experienced." |
| 41-60 | 26-45 | OWNED | "He does what I tell him. Not because I force him — because he wants to please me more than he wants to breathe. 'Good boy.' His eyes close." |
| 61-80 | 46-65 | ASSET | "He covers for me. Lies for me. Looks the other way. Tom isn't a lover anymore — he's a tool. I say that without guilt and that scares me less than it should." |
| 81-100 | 66+ | CONSUMED | "He'd destroy his life on one word from me. I know this because I tested it. The girl from Day 1 would weep. The woman from Day 60 smiles." |

#### Ray Cross-States

| ray_interest | confidence | Quadrant | Description |
|-------------|-----------|----------|-------------|
| 0-20 | 0-15 | INVISIBLE | "He calls me 'Miss.' I'm wallpaper. A barstool with a cardigan." |
| 0-20 | 16-30 | TESTING | "I ordered whiskey and his eyebrow moved a millimeter. 'Didn't take you for a whiskey girl.' The drawer is rattling." |
| 21-40 | 16-30 | CRACKING | "He said my name. Not Miss. Emma. The way he tested it — slow, careful — was worth more than anything Tom stammered." |
| 41-60 | 31-50 | PHYSICAL | "His body admitted what his mind won't. We stood pressed together in the shed and neither of us mentioned it after. But he can't unsee me now." |
| 61-80 | 51-70 | OPEN | "He kissed me on the staircase. Hard. This one cost him something. 'This is a bad idea.' 'I know.' Neither of us cares." |
| 81-100 | 51-70 | COMPLICATED | "He's falling for me. Real feelings. The complication I didn't plan for. I wanted conquest. He's offering his heart. And I have to decide if I want it." |

#### Mark Cross-States

| mark_desire | mark_guilt | Quadrant | Description |
|------------|-----------|----------|-------------|
| 0-20 | 0-15 | PROFESSIONAL | "He's a parent. I'm a teacher. The handshake is firm and that's all there is." |
| 21-40 | 0-15 | HUNGRY | "He lingers. He's starved. Karen gives pecks on the cheek. I give him eye contact that lasts three seconds too long." |
| 21-40 | 16-30 | CONFLICTED | "He wants to linger but drives away. Texts 'sorry' at midnight then texts 'I keep thinking about the rain' at 12:03." |
| 41-60 | 16-30 | BURNING | "Under the desk. Footsteps in the hallway. His thumb on my skin. The danger is the point. Every escalation risks everything and he can't stop." |
| 41-60 | 31-45 | GUILT SPIRAL | "He can't look at his son. Snaps at Karen. The guilt has spread from the affair into his entire self-image. But he still shows up Thursday." |
| 61-80 | 16-30 | CONSUMED | "He stopped mentioning Karen. He walks in and knows what he's here for. I own the part of him she never knew existed." |
| 61-80 | 31-45 | CRISIS | "Karen found the text. He hasn't slept in three days. He looks at me like I'm either the devil or the only thing keeping him alive." |
| 81-100 | 0-15 | OWNED | "The guilt burned itself out. He reorganized his life around access to me. The house with Karen is the performance. I'm his real life." |

#### Jake Cross-States

| jake_power | corruption | Quadrant | Description |
|-----------|-----------|----------|-------------|
| 80-100 | 0-45 | UNTOUCHABLE | "He leans over the bar and uses the smile that works on everyone. I don't exist in his framework yet. I'm another mark he hasn't bothered to close." |
| 80-100 | 46-65 | REJECTED | "He tried his move. I laughed. The confusion on his face was the most satisfying thing I've seen since Day 1." |
| 60-79 | 46-65 | RATTLED | "He watches me flirt with other men and his pours get sloppy. The smile is still there but it's thinner. I'm inside his head." |
| 40-59 | 66-85 | BREAKING | "'What the fuck do you want from me?' He doesn't know. I do. The ego is cracking and I can see what's underneath — a man who wants to be told what to do." |
| 20-39 | 66-85 | SUBMITTING | "He said 'please.' He follows my instructions. When I put his hands where I want them and he doesn't move them without permission — that's the moment the old Jake dies." |
| 0-19 | 86-100 | SURRENDERED | "He sits on my bed and asks what to do with his life. I built this. The cocky bartender is gone. Whatever's left belongs to me — or proves I never needed it." |

---

### Emotional Transition Moments (Per NPC)

#### Tom Transitions

| Transition | The Moment | Sample Line / Beat |
|-----------|-----------|-------------------|
| STRANGER → SMITTEN | First time he changes his routine for her | He's at the diner at noon on a Wednesday. He's never been there at noon. He came because she mentioned she might get coffee. |
| SMITTEN → DEVOTED | First time he does something before she asks | Flowers. Gas station flowers. The most heartbreaking thing she's ever seen. He brought them to a movie night in her room. |
| DEVOTED → ADDICTED | The "Good Boy" moment | "Good boy." She says it and his eyes close. Not embarrassment — recognition. He liked being directed. He liked being hers. Everything after this is gravity. |
| ADDICTED → SURRENDERED | First time he lies for her | Tom sees Ray. Tom chooses to look the other way. Not because she asked — because losing her is the only thing that scares him more than being dishonest. |
| SURRENDERED → (crisis) | Tom sees the truth | "Are you and that handyman... is something happening?" Quiet. Hurt. Not angry — Tom doesn't get angry. Wounded. The golden retriever realizing the hand that feeds him feeds others too. |
| (crisis) → LOYAL AGAIN | He chooses her anyway | "It's complicated." Three words. He looks at his hands. "I know." He stays. He stays because leaving means losing the only person who ever made him feel like he mattered. |

#### Ray Transitions

| Transition | The Moment | Sample Line / Beat |
|-----------|-----------|-------------------|
| INDIFFERENT → NOTICING | First time he uses her name | "...Emma." He says it slow. Testing it. Like he's deciding whether she gets to be a person in his world instead of a category. |
| NOTICING → WANTING | The shed — his body admits it | Pressed together. Saw forgotten. His breathing changes. His hands grip her hips. Neither mentions it after. But the category is shattered. |
| WANTING → OPEN | The staircase kiss | He kisses her. Hard. "This is a bad idea." He doesn't step back. The man who called her "Miss" has his hand on the back of her neck. |
| OPEN → COMPLICATED | "I was thinking about you today" | Ray doesn't say that. That sentence is a symptom. He's developing real feelings and Jolene sees it before Emma does. |
| COMPLICATED → (tension) | Jolene's warning | "If you break that man, he doesn't come back. He has a kid." The first time the game stops being fun. |
| (tension) → DEEP | She stays despite the complication | Whether she admits it or deflects, she keeps seeing him. The feelings are the first thing she can't control, and that terrifies her more than Karen ever did. |

#### Mark Transitions

| Transition | The Moment | Sample Line / Beat |
|-----------|-----------|-------------------|
| PROFESSIONAL → HUNGRY | First time he lingers | "Your son is wonderful. He must get it from you." His eyes — the way they hold her face. He thinks about that sentence for three days. |
| HUNGRY → RECKLESS | The text that changes everything | "I keep thinking about the rain." Typed at midnight. Sent. The barrier breaks through screens. There's no unfinding this. |
| RECKLESS → DESPERATE | First time he lies to Karen | "Karen thinks I'm at a meeting." His hands are shaking. He crosses the doorframe and everything on the other side of it — wife, son, reputation — ceases to exist for the next two hours. |
| DESPERATE → OWNED | No Hesitation | He comes back. No shaking hands. No preamble. He walks in and knows what he's here for. The guilt didn't stop him. Nothing stops him now. |
| OWNED → CRISIS | Karen finds the text | "She knows. She doesn't have proof, but she knows." His face — wrecked. Three days of silence. The bomb he's been building detonates. |
| CRISIS → (recovery) | The parking lot | 11pm. His car. "Parking lot. Please." He can't stay away even when staying away would save his marriage. She either releases him or pulls him deeper. Either way, he comes back. |

#### Jake Transitions

| Transition | The Moment | Sample Line / Beat |
|-----------|-----------|-------------------|
| COCKY → RATTLED | The laugh | She laughs AT him. Not a blush, not a polite decline. She laughs like it's funny that he tried. Nobody laughs at Jake. The glass he forgot to dry is still in his hand. |
| RATTLED → CRACKING | "What the fuck do you want from me?" | Not a line. Genuine confusion. The jukebox gets punched. The back door gets used. His identity is failing and he has no backup system. |
| CRACKING → SUBMITTING | He says "please" | "One kiss. Please." A word Jake has never said to a woman. The moment it leaves his mouth, the power transfer is permanent. He can feel it. So can she. |
| SUBMITTING → SURRENDERED | He discovers he likes it | "Did I say you could move them?" His eyes change. Not anger — recognition. He likes being told. The cocky bartender likes surrendering. The armor was never the man. |
| SURRENDERED → ENDGAME | "What do you want me to do?" | Sitting on her bed. Not for sex. Asking for direction. In life. The question of a man who has been unmade and is waiting to be remade. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: GUIDANCE HINTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### General Progression Hints

| Condition | Hint Text |
|-----------|-----------|
| missing_flag: phase_1_complete | "Jolene has something to show you. She's usually around the bar in the evenings." |
| missing_flag: school_started | "School starts Monday. Get some rest — the kids in Millfield are waiting." |
| missing_flag: chores_explained | "Jolene mentioned something about rent and groceries during your first dinner together..." |
| money < 30 | "Funds are running low. Tutoring pays $30 a session, and Jolene might have bar shifts available." |
| energy < 20 | "You're exhausted. Sleep in your room before doing anything else." |
| reputation < 40 | "People are talking. Church on Sunday and volunteering might help rebuild trust." |
| missing_flag: food_stocked, days_since > 5 | "The fridge is empty. The general store has groceries — $25 but necessary." |

### Phase 1 (Jolene) Hints

| Condition | Hint Text |
|-----------|-----------|
| corruption < 5, days > 3 | "Jolene invited you for dinner upstairs. She might have wine. She definitely has questions." |
| missing_flag: jolene_peek_event, corruption >= 5 | "Jolene's schedule is... unpredictable. Coming home at odd hours might reveal more about your landlady." |
| missing_flag: jolene_self_discovery, corruption >= 12 | "Jolene gave you advice. Uncomfortable advice. But she might be right. Your room. The door locks." |
| corruption >= 10, missing_flag: phase_1_complete | "Something is changing. You're noticing things — people, bodies, desires. Jolene sees it. 'There she is.'" |

### Tom Route Hints

| Condition | Hint Text |
|-----------|-----------|
| missing_flag: tom_locks_checked, phase_1_complete | "Jolene mentioned the deputy. 'That boy's been drooling since you walked into town.' The station is downtown." |
| tom_devotion < 15, days > 16 | "Tom responds to attention. Visits to the diner, walks past the station — he notices every crumb." |
| missing_flag: tom_kiss_unlocked, tom_devotion >= 20 | "You and Tom keep ending up alone. The classroom after school is quiet. You could engineer something." |
| tom_devotion stalled (no gain in 3 days) | "Tom's waiting for you. Coffee at the diner or an invitation upstairs — he just needs a reason." |
| missing_flag: tom_sex_unlocked, tom_devotion >= 60 | "Tom would do anything you asked. Text him. 'Come over. Just you.' He'll be there in minutes." |
| (tom_complete) | "Tom is yours completely. He'd lie for you, cover for you, burn his whole world down on one word. The power is absolute. The question is whether you feel anything about that." |

### Ray Route Hints

| Condition | Hint Text |
|-----------|-----------|
| missing_flag: ray_invisible_wall, phase_1_complete, confidence >= 10 | "Ray drinks at the bar every evening. He hasn't noticed you. That's about to change." |
| ray_interest < 10, days > 22 | "Ray still calls you 'Miss.' Break the frame — show up differently. The dress. The whiskey. Stop being the category he filed you in." |
| missing_flag: ray_kiss_unlocked, ray_interest >= 30 | "Ray's body knows. His mind is catching up. The bar closes late on Fridays. The staircase is private." |
| ray_interest stalled (no gain in 3 days) | "Ray responds to surprise. Do something he doesn't expect. Bring beer to where he's working. Sit on his truck. Let the silence do the work." |
| missing_flag: ray_sex_unlocked, ray_interest >= 60 | "Ray is done pretending. Bar closing. Just the two of you. 'Are you coming up?' isn't a question." |
| (ray_complete) | "Ray taught you something you didn't expect — not how to seduce, but what you actually want. Competent sex isn't the point. Power is. He was too much of an equal." |

### Mark Route Hints

| Condition | Hint Text |
|-----------|-----------|
| missing_flag: mark_first_conference, corruption >= 40 | "Parent-teacher conferences are Tuesday and Thursday. Mark comes alone — Karen has 'headaches.'" |
| mark_desire < 15, days > 33 | "Mark is hungry but cautious. The school fundraiser needs volunteers. He'd jump at an excuse to be near you." |
| missing_flag: mark_kiss_unlocked, mark_desire >= 20 | "Late sessions at the school. Walking to his car. The rain helps — one umbrella, no distance." |
| mark_guilt > 40 | "Mark is spiraling. Keep the next conference professional — lower the temperature. Guilt needs managing, not elimination." |
| missing_flag: mark_sex_unlocked, mark_desire >= 60 | "He'll show up. 'Karen thinks I'm at a meeting.' He just needs permission — not from her, from you." |
| karen_school_confrontation, missing_flag: mark_crisis_repair_complete | "Mark hasn't texted in days. Give it time. He'll reach out. They always reach out." |
| (mark_complete) | "You burned it all down. His marriage, his guilt, his self-image. He comes back because the hunger is stronger than the shame. You feel nothing about that. And that tells you everything about who you've become." |

### Jake Route Hints

| Condition | Hint Text |
|-----------|-----------|
| missing_flag: jake_second_attempt, corruption >= 55 | "Jake's been watching you change. He'll try his move again. This time, you're ready to laugh." |
| jake_power > 70, days > 46 | "Jake's ego is intact. Flirt with other men at the bar while he watches. The message: you're not the prize. She is." |
| missing_flag: jake_kiss_unlocked, jake_power <= 65 | "Jake is confused. That's new for him. The bar closes late. Be the last one there. See what he does when the bravado runs out." |
| jake_power stalled (no change in 3 days) | "Jake responds to denial. Don't give him what he wants. Make him earn the smallest things. 'Not yet' is the most powerful phrase." |
| missing_flag: jake_sex_unlocked, jake_power <= 30 | "He's ready. He's been ready. Tell him when to arrive, what to wear, where to stand. See if he complies. He will." |
| (jake_complete) | "The cocky bartender said 'please.' You own every room you walk into. The question isn't whether you have power — it's what you do with it. Or whether you even need it anymore." |

### Cross-NPC / Reputation Hints

| Condition | Hint Text |
|-----------|-----------|
| tom_kiss_unlocked AND ray_interest >= 20 | "Friday nights at the bar are crowded. If Tom and Ray are both there, be careful who you focus on. People notice patterns." |
| juggling_detected | "Mrs. Hewitt's comment at the store wasn't casual. The town is watching. Church, volunteering, and being seen doing normal things buys time." |
| reputation < 50, 2+ NPCs at kiss+ | "The principal has started 'checking in.' Karen sits in her car outside the school. The net is tightening. Reputation activities are urgent." |
| reputation < 30 | "You're running out of room. Every risky move could be the last one the town forgives. Choose carefully — or decide you don't care." |

### Mirror / Endgame Hints

| Condition | Hint Text |
|-----------|-----------|
| days >= 19, missing_flag: mirror_day_20 | "Take a morning to yourself. Look in the mirror. Really look." |
| days >= 39, missing_flag: mirror_day_40 | "The mirror has been waiting. What you see in it now isn't what you saw on Day 1." |
| days >= 59, missing_flag: mirror_day_60 | "One last look. The cardigan is gone. The Bible is gone. What's left?" |
| (default) | "There are still moments to discover in Millfield..." |
| (all arcs complete) | "Four men. One town. One mirror. Whatever she became, she chose it. Every step. Every 'good boy.' Every 'not yet.' Every closed door and every lie to Karen's face. The girl who arrived with a Bible is gone. She doesn't miss her." |


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# QUALITY CHECKLIST

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Story Quality

- [x] Central tension defined as a single emotional question — "Can a woman discover who she really is by becoming someone her former self would despise — and is the power she gains worth what she loses?" (Phase 4, Dramatic Spine)
- [x] Tom has at least 2 internal contradictions — (1) He wants connection but can't initiate; (2) He wants to please her but doesn't know how. Both drive story events. (Phase 2, Tom section)
- [x] Ray has at least 2 internal contradictions — (1) He wants to feel something but built walls to prevent it; (2) He dismisses her as a "kid" but physically responds to her as a woman. (Phase 2, Ray section)
- [x] Mark has at least 2 internal contradictions — (1) He's a "good man" who craves transgression; (2) He loves his family but feels invisible in his own marriage. (Phase 2, Mark section)
- [x] Jake has at least 2 internal contradictions — (1) He wants to fuck her but she wants to own him; (2) He needs control but control is performance, not reality; (3) He doesn't want to feel anything but she makes him feel everything. (Phase 2, Jake section)
- [x] Tom resistance pattern defined (mild → moderate → severe → recovery) — Phase 2, Tom Resistance Pattern table
- [x] Ray resistance pattern defined (mild → moderate → severe → recovery) — Phase 2, Ray Resistance Pattern table
- [x] Mark resistance pattern defined (mild → moderate → severe → recovery) — Phase 2, Mark Resistance Pattern table
- [x] Jake resistance pattern defined (mild → moderate → severe → recovery) — Phase 2, Jake Resistance Pattern table
- [x] At least 2 tension/crisis events where stats DROP — Ray's "Feelings" event (ray_interest -3), Tom "Saw Ray" event (tom_devotion -2 to -3), Karen crisis (mark_desire -3, reputation -5 to -8), Jake ego crisis (jake_power -5). (Phase 4)
- [x] Major crisis threatens to END the relationship — Karen crisis for Mark (reputation destruction, firing), Tom-sees-Ray (jealousy threatens Tom relationship), Ray-feelings (feelings complication threatens power dynamic), Jake-ego-crisis ("What the fuck do you want from me?" — threatens entire dynamic). (Phase 4)
- [x] Major crisis takes 2-4 in-game days to resolve — Karen crisis spans Day 52-57 (2+ days silence, then parking lot repair). Mark guilt spiral takes 5+ days if guilt > 40. (Phase 4)
- [x] At least 3 story events have TRADE-OFF or SACRIFICE choices — Tom "First Time" (accept devotion vs. push away guilt), Mark "Crisis Repair" (release guilt vs. pull deeper), Jake "Endgame" (keep him vs. walk away), Jolene "Figure It Out" (do it vs. can't). (Phase 4)
- [x] At least 1 choice results in NEGATIVE stat consequences — Ray "Invisible Wall" (confidence -1), Ray "Feelings" choice "I didn't plan for this" (confidence -1), multiple reputation losses from choices. (Phase 4)
- [x] At least 2 bridge events exist purely for character development — Tom's Confession (Day 20-22), Ray's Daughter (Day 34-36), Mark's Phone Call (Day 45-47), Jake's Ego Crisis (Day 52-54). (Phase 4)
- [x] Tension curve alternates: escalation → tension → recovery → escalation — Tension curve diagram shows this pattern per NPC. Tom: easy escalation → devotion lock. Ray: flat → crack → gates → feelings complication. Mark: tension → gates → Karen crisis → recovery. Jake: rejection → humiliation → flip → submission. (Phase 4)
- [x] Each NPC shows fundamentally changed behavior in Act 3 vs Act 1 — Tom: stammering deputy → devoted "good boy." Ray: dismissive "ma'am" → saying her name, saving stools, real feelings. Mark: professional handshake → parking lot at midnight, risking family. Jake: cocky "What can I get you, beautiful?" → "What do you want me to do?" (Phases 2, 4, 6)
- [x] Escalation progression is logical and incremental per-NPC — Each NPC has sequential gate events with increasing stat requirements and day minimums. (Phase 4, Gate Timeline)
- [x] Each gate feels EARNED through preceding drama, not just stat threshold — Gate events are narrative moments: the classroom catch, the staircase kiss, the rain umbrella, the stockroom. Stats are necessary but not sufficient — story context makes them feel earned. (Phase 4)
- [x] Post-crisis intimacy feels deeper than pre-crisis intimacy — Mark post-Karen: the parking lot scene is more emotionally charged than pre-crisis encounters. Ray post-feelings: the "upstairs" sex carries weight of real connection. Jake post-ego-crisis: submission is authentic, not performative. (Phase 4)
- [x] Fantasy is clear and compelling — Female corruption-to-predator arc in small-town setting. Each NPC offers a distinct power fantasy. (Phase 1)
- [x] Each NPC feels like a real person with internal depth — Detailed psychology, contradictions, resistance patterns, emotional quadrant behaviors, speech patterns per NPC. (Phase 2)
- [x] Choices have meaning (different stat outcomes AND narrative consequences) — Every major choice has distinct stat effects AND different narrative text/outcomes. E.g., Tom "First Time": "I know you would" creates an asset; "Don't say that" preserves humanity. (Phase 4)

## Emotional Flow Quality

- [x] NPC emotional quadrant behaviors defined — Phase 2 defines quadrant behaviors for all 4 NPCs (Tom: devotion/confidence, Ray: guard/desire, Mark: desire/guilt, Jake: ego/submission)
- [x] Emotional tells defined for each primary stat range — Phase 2 defines observable behavior tables for tom_devotion (0-100 in 5 ranges), ray_interest (0-100 in 5 ranges), mark_desire (0-100 in 5 ranges), jake_power (100-0 in 5 ranges)
- [x] Emotional tells defined for secondary stats where applicable — mark_guilt has 5 ranges of observable behavior defined in Phase 2
- [x] Cross-state descriptions include relevant stat combinations — Phase 2 quadrant system covers 4 combinations per NPC (e.g., Mark: HIGH DESIRE/LOW GUILT through LOW DESIRE/HIGH GUILT)
- [x] Transition moments defined for each major emotional shift — Phase 6 Section 2 defines act transitions with exact stat thresholds and narrative shift descriptions per NPC
- [x] At least one scene per quadrant exists in the story event chain — Phase 4 story events cover all emotional states per NPC (setup/escalation/crisis/resolution)
- [x] Activity base scenes include emotional state awareness (WITHDRAWN/DEFAULT/WARM variants) — Phase 5 defines DEFAULT, WITHDRAWN, and WARM variants for all 8 NPC activities
- [x] Post-crisis NPC behavior is noticeably different from pre-crisis — Mark post-Karen: withdrawn variant described ("doesn't close the door, doesn't sit, quick, professional"). Jake post-ego-crisis: withdrawn variant described ("off his game, drops glass, keeps glancing"). (Phase 5)
- [x] Crisis period explored for at least 2-3 in-game days — Karen crisis spans Day 52-57 (5 days). Jake ego crisis spans Day 52-54 (2-3 days). Ray feelings span Day 38-42 (4 days). (Phase 4)
- [x] NPC emotional flow follows appropriate arc pattern — Phase 6 Section 2 defines per-NPC arc patterns: Tom (steady ascent), Ray (delayed then rapid), Mark (push-pull with crisis valley), Jake (inverted descent)
- [x] The crisis recovery is a powerful transition point — Mark parking lot scene, Jake "Not Yet" kiss after ego crisis, Ray "Upstairs" after feelings emerge. Each marks a qualitative shift in the relationship. (Phase 4)

## Player Character Quality

- [x] Player has defined want/need/fear/flaw — Phase 2 Section 1: Want (to feel alive), Need (to accept desire without shame), Fear (being seen for who she's becoming), Flaw (she confuses power over others with self-worth)
- [x] Player emotional phases defined — Phase 2 defines Emma's 6-phase transformation: Innocent → Curious → Experimenting → Confident → Predatory → Questioning
- [x] Player phase transitions tied to specific story events — Phase 6 Section 3 maps each phase to specific trigger events and stat thresholds
- [x] Player internal voice changes across phases — Phase 6 Section 3 defines narration tone shifts: "gosh" → clinical observation → confident direction → predatory calculation → self-questioning
- [x] "What player notices" evolves — Phase 6 Section 3 describes perceptual shifts: Phase 1 notices discomfort, Phase 3 notices body language, Phase 5 notices power dynamics
- [x] "How player describes NPC" shifts — Phase 6 Section 3 tracks description evolution per NPC (e.g., Tom: "sweet" → "useful" → "mine")
- [x] Choice text framing reflects player phase — Phase 6 Section 3 shows how identical actions are framed differently at different corruption levels
- [x] Player has a parallel crisis arc (mirror mechanic) — Mirror scenes at Day 1/20/40/60 provide Emma's self-reflection transformation checkpoints. (Phase 4, Mirror Scenes)
- [x] Player crisis stages defined — Phase 6 Section 3 defines Emma's crisis: recognition (Day 40 mirror), confrontation (Day 52-55 Karen crisis), resolution (Day 60 mirror)
- [x] Activity scenes show player internal state — Phase 5 activity narration includes Emma's internal thoughts and evolving perspective
- [x] Player growth is visible in narration — Phase 1 narration uses soft/uncertain language; Phase 2 late narration uses confident/predatory language. Clear progression. (Phase 4, 6)
- [x] Player character feels like a person with her own journey — Emma has detailed background, psychology, want/need/fear/flaw, and a 6-phase transformation arc. She's not just a vehicle — she has her own story. (Phase 2)

## Scene Quality

- [x] Each scene has clear narrative purpose — All 50 story events have defined purpose (setup, gate, bridge, tension, crisis, repair, endgame). (Phase 4, Complete Event Inventory)
- [x] Video/media descriptions are specific where needed — Phase 4 and 5 include specific IMAGE and VIDEO media descriptions for each node and escalation tier
- [ ] Clip UUIDs assigned where available — N/A (Phase 0 not completed, no video files assigned yet)
- [x] Search queries provided for external sources — Phase 3 provides image search queries for all 14 locations
- [x] Progression makes logical emotional sense — Events chain sequentially with flag dependencies and stat requirements ensuring logical emotional progression. (Phase 4, Flag Chain Diagrams)
- [x] No gaps in the experience — 50 story events + 25 activities = 75 canvases covering all 65 days with no narrative gaps. Flag chains show complete coverage. (Phase 4, 5)

## Technical Quality

- [x] All IDs are consistent (loc_, npc_ prefixes) — Phase 3 uses loc_ prefix for all locations. NPC stats use npc_name_ prefix. Canvas IDs use descriptive snake_case. (Phase 2, 3, 4, 5)
- [x] Trigger conditions are logical and achievable — All story events have logical trigger conditions: flag prerequisites, stat thresholds, day minimums, and time windows. (Phase 4)
- [x] Stat thresholds are reachable through normal play — Phase 2 Section 3 provides target progression tables showing stat growth per day range for each NPC, confirming thresholds are reachable. (Phase 2)
- [x] Flag chains form a complete dependency graph — Phase 4 provides complete flag chain diagrams for all 5 arcs (Jolene, Tom, Ray, Mark, Jake) plus cross-NPC dependencies
- [x] Gate flags correctly assigned to story events — 16 gate flags (4 per NPC x 4 NPCs) each set by a specific named story event in Phase 4. Gate Timeline Summary confirms all 16. (Phase 4)

## Activity Quality

- [x] NPC activities cover multiple time slots — Tom: Afternoon + Night. Ray: Evening + Late Afternoon. Mark: Late Afternoon. Jake: Evening + Late Night. Jolene: Late Morning + Afternoon. (Phase 5)
- [x] Utility canvases present (chores, jobs, rest) — 10 utility canvases: groceries, 2 sleep types, rent, church, volunteering, neighborly visits, school events, rest, nap. (Phase 5)
- [x] Economic loop is viable (player can afford rent) — $220 salary - $180 rent = $40 surplus. Food ~$35/week. Teaching + 1 tutoring or bar shift = stable. Detailed economic model in Phase 3. (Phase 3)
- [x] Each NPC activity has base scene + gated choices — All 8 NPC activities have base scenes with DEFAULT/WITHDRAWN/WARM variants and progressive choice tables gated by stats and flags. (Phase 5)
- [x] Choice thresholds use hybrid gating — Choices require both stat thresholds AND gate flags (e.g., "tom_devotion >= 42 + tom_kiss_unlocked"). (Phase 5)
- [x] Not all activities forced to reach sex — Coffee with Tom caps at foreplay (public diner). Evening at Bar (Ray/Jake) caps at foreplay (public bar). Parent Conferences caps at foreplay (school). Jolene Chats has no sexual escalation. (Phase 5)
- [x] Canvas balance: 25 activities + 50 story events = 75 total — Phase 5 confirms 25 activity canvases (8 NPC + 10 utility + 4 money + 3 solo). Phase 4 confirms 50 story events. (Phase 4, 5)

## Video Integration Quality

- [ ] Phase 0 not completed — no video files assigned yet
- [ ] Clip library not yet populated — awaiting Phase 0 video integration
- [x] Search queries and image descriptions provided in Phase 3 — All 14 locations have image search queries. Phase 4 and 5 provide specific media descriptions for story events and activities.

## Gate System Quality

- [x] 4 gates defined per NPC (kiss, groping, oral, sex) — 16 total — Phase 2 Section 4 defines all 16 gates with per-NPC gate chain tables. (Phase 2)
- [x] Each gate set by a specific story event — All 16 gates are set by named story events: Tom (Classroom Catch, Movie Night, Good Boy, First Time), Ray (Shed, Staircase, Truck, Upstairs), Mark (Rain, Under Desk, First Visit, No Hesitation), Jake (Not Yet, Permission, Stockroom, On Her Terms). (Phase 2, 4)
- [x] Hybrid gating model applied to all NPC activities — Activity choice tables in Phase 5 use stat threshold + gate flag requirements for all escalation tiers
- [x] Gates unlock content across ALL activities simultaneously — Gate flags are per-NPC (not per-activity), so tom_kiss_unlocked opens kiss-tier choices in both Coffee With Tom AND Visit Tom. (Phase 2, 5)
- [x] Gate timeline is achievable through normal play — Phase 2 Section 3 target progression tables confirm all gates reachable within the 65-day timeline with normal play patterns. (Phase 2)

## Content Balance

- [x] Activity content distributed across locations and time slots — 8 NPC activities span Diner, Bar, Classroom, Shed, Emma's Room across Afternoon/Late Afternoon/Evening/Night/Late Night. (Phase 5)
- [x] Story events: 50 events (67% of 75 total canvases) — Phase 4 Complete Event Inventory confirms 50 story events. 50/75 = 67%. (Phase 4)
- [x] Economic pressure creates meaningful time trade-offs — $5 weekly surplus from teaching alone forces supplemental income, consuming NPC time slots. Detailed in Phase 3 economic model. (Phase 3)
- [x] Player can reach key stat thresholds by target days — Phase 2 target progression tables show achievable stat growth per day range for all 4 NPCs. (Phase 2)
- [x] days_since_flag pacing prevents narrative compression — Mark crisis repair requires days_since_flag(karen_school_confrontation) >= 2. Mark guilt spiral causes 5+ day contact freeze. Rent timer uses days_since_flag. (Phase 4)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## CHECKLIST SUMMARY

| Category | Passed | N/A | Total |
|----------|--------|-----|-------|
| Story Quality | 17 | 0 | 17 |
| Emotional Flow Quality | 11 | 0 | 11 |
| Player Character Quality | 12 | 0 | 12 |
| Scene Quality | 5 | 1 | 6 |
| Technical Quality | 5 | 0 | 5 |
| Activity Quality | 7 | 0 | 7 |
| Video Integration Quality | 1 | 2 | 3 |
| Gate System Quality | 5 | 0 | 5 |
| Content Balance | 5 | 0 | 5 |
| **TOTAL** | **68** | **3** | **71** |

**Pass Rate**: 68/68 verified items passed (100%). 3 items marked N/A (Phase 0 video integration not yet completed).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# END OF GAME DESIGN BOOK
# New In Town
# Generated: 2026-02-26

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
