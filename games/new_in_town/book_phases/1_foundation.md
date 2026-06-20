# PHASE 1: FOUNDATION
# New In Town

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GAME IDENTITY

**Title**: New In Town
**Protagonist**: Emma (female, player-controlled), 23 years old
**Genre**: Adult interactive fiction with video integration
**Perspective**: Female protagonist — player IS the woman
**Theme**: Female corruption → female predator. Innocence lost, power gained.

### Engine Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| **Starting Canvas** | `opening_arrival` | The arrival scene — no trigger (fires on game start) |
| **Schema Version** | `"0.2"` | TOML v2 schema |

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

**Primary Driver**: CORRUPTION (stat: `devotion` on npc_tom)
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

**Primary Driver**: SEDUCTION (stat: `interest` on npc_ray)
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

**Primary Driver**: FORBIDDEN (stat: `desire` on npc_mark)
- The taboo is the engine. Teacher-parent. The professional boundary, the marriage, the child between them, the PTA wife who's always watching.
- His resistance is real — he has genuine reasons to say no. Family, reputation, morality. She has to make the risk feel worth the cost.
- Secondary driver: SEDUCTION — he's not seeking an affair, she's engineering one. She must actively pursue while maintaining plausible deniability.

**Driver fit**: FORBIDDEN because the transgression itself is the escalation mechanic. Every step forward is a line crossed that can't be uncrossed. The stat isn't measuring attraction (he's attracted from the start) — it's measuring how much of his life he's willing to burn. The secondary SEDUCTION layer captures the deliberate manipulation: she creates situations, engineers proximity, and controls the pace through texting.

**Difficulty**: HARD — highest external stakes. First NPC where getting caught has consequences beyond the relationship. Karen is a persistent threat. Reputation damage is severe. Requires manipulation skills built from Tom and Ray.

**Unique Complication**: `guilt` stat (on npc_mark). She must manage his guilt like a throttle — too much and he confesses to Karen or stops coming; too little and the forbidden thrill dies. The sweet spot is: guilty enough to be desperate, not so guilty he self-destructs.

---

### NPC 4: Jake — The Bartender

**Vibe**: Cocky, tattooed, effortlessly attractive. The guy who leans on the bar and says "What can I get you, beautiful?" to every woman who walks in. Lazy smile, lean build, zero depth. Think "the man who's never had to try — and has no idea what happens when a woman stops letting him win."

**What makes him appealing**: He's the final boss — not because he's hard to sleep with (he'd fuck her tonight if she said yes), but because the game isn't sex. The game is *submission*. He's spent his life being the confident one, the pursuer, the one in control. The fantasy is making him kneel. Making the cocky guy beg. Stripping away the persona and finding the man underneath who *wants* to be told what to do.

**Relationship**: Bartender at Jolene's bar. He tried his moves on "old Emma" and got shut down. He's filed her under "prude." He has no idea what she's become.

**Primary Driver**: DOMINANCE (stat: `power` on npc_jake)
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

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue to Phase 2: Characters & Stat Economy,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
