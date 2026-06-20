# EXTRACTION: NPC Definitions
# Source: Phase 2 (Characters & Stats)

## NPC ID MAPPING

| Book Name | TOML ID |
|-----------|---------|
| Tom | `npc_tom` |
| Ray | `npc_ray` |
| Mark | `npc_mark` |
| Jake | `npc_jake` |
| Jolene | `npc_jolene` |

## NPC STAT MAPPING (Unprefixed on NPC object)

| Book Reference | TOML npcId | TOML trait_key | Starting | Direction | Range |
|----------------|------------|----------------|----------|-----------|-------|
| Tom: devotion | npc_tom | devotion | 0 | 0 -> 100 | 0-100 |
| Ray: interest | npc_ray | interest | 0 | 0 -> 100 | 0-100 |
| Mark: desire | npc_mark | desire | 0 | 0 -> 100 | 0-100 |
| Mark: guilt | npc_mark | guilt | 0 | 0 -> 50 | 0-50 |
| Jake: power | npc_jake | power | 100 | 100 -> 0 | 0-100 |
| Jolene: mentorship | npc_jolene | mentorship | 0 | 0 -> 100 | 0-100 |

---

## NPC 1: JOLENE (npc_jolene)

### Core Config
```toml
[npcs.npc_jolene]
id = "npc_jolene"
name = "Jolene"
role = "Non-romantic corruption catalyst (Phase 1) + mentor (Phase 2)"
age = 42
core_traits = { mentorship = 0 }
```

### Physical Appearance
Full-figured, 5'7", soft curves, sun-freckled shoulders. Auburn hair worn loose and wild. Laugh lines. Rough hands from bar work, nails painted red and chipped.
- Mornings: silk robe over nothing, barefoot, cigarette, coffee
- Bar hours: low-cut top, jeans, boots
- Late night: robe or men's flannel over underwear

### Personality
- Surface: Loud, direct, profane. Says "fuck" like punctuation.
- Hidden: Observant, emotionally intelligent. Knew Emma was sheltered in 10 minutes.

### Psychology
Married at 20, left boring husband at 25. Second husband hit her, left at 31. Single since by choice. Sees Emma and recognizes wound of shame-based sexuality. Corruption method is liberation, not malice. Vulnerability: loneliness she won't admit.

### Speech Patterns
Direct. Short sentences. No qualifiers. Nicknames: hon, sugar, girl.
- Early: "You're wound tighter than a banjo string, sugar."
- During corruption: "That feeling in your stomach right now? That's not guilt. That's want."
- As mentor: "Walk in there like you own the place. Because, honey, you do."

### Note
Jolene is NOT a seduction target. Corruption tracked on player's corruption trait, not on Jolene. Mentorship trait is for narrative gating only.

---

## NPC 2: TOM (npc_tom)

### Core Config
```toml
[npcs.npc_tom]
id = "npc_tom"
name = "Tom"
role = "Deputy"
age = 25
primary_driver = "CORRUPTION"
difficulty = "EASY"
core_traits = { devotion = 0 }
```

### Physical Appearance
6'1", athletic but not bulky. Sandy blond, clean-cut. Blue eyes, strong jaw. Handsome in yearbook-photo way. No tattoos/piercings/scars.
- Uniform: crisp khaki deputy, polished boots, badge centered. Tight across shoulders.
- Off duty: jeans, flannel or plain t-shirt, sneakers. No style instinct.

### Personality
- Surface: Polite, earnest, eager to help. Holds doors, calls women "ma'am," tips 25%.
- Hidden: Deeply insecure about inexperience. Deputy because his dad was sheriff. Never left the county. 25-year-old virgin.

### Psychology
Raised by single father (mother left at 7). Dad was good sheriff, terrible communicator. Crush on Emma from moment she arrives -- immediate, physical, paralyzing. Wants someone to choose him. Would do anything to keep her attention.

### Internal Contradictions
1. Wants Emma but doesn't know what "wanting" means
2. Wants to be protector but she's in control
3. Wants to be good but she's teaching him to want "bad" things

### Resistance Pattern
| Stage | Behavior |
|-------|----------|
| MILD | Freezes, goes still, stammers. "I, uh-- I should probably--" |
| MODERATE | Avoids 1-2 days. Neutral texts hours later. Processing. |
| SEVERE | Does not exist. Cannot push back hard. |
| RECOVERY | Shows up. Just appears wherever she is. Smile = instant recovery. |

### Emotional Tells by Stat Range (devotion)
| Range | Behavior |
|-------|----------|
| 0-20 | Classic crush. "Coincidence" encounters. Straightens uniform. Overreacts. |
| 21-40 | Makes excuses to be around her. Remembers her coffee order. |
| 41-60 | Leans toward her. Breathing changes at touch. Mirrors her body language. |
| 61-80 | Waits for her. Covers for her at church. Small lies without being asked. |
| 81-100 | Complete devotion. Says her name like a prayer. No questions. |

### Speech Patterns
- Early (0-30): Broken, fragmented. Starts words and abandons them.
- Mid (31-60): Short, earnest sentences. "I brought you coffee. Two sugars, right?"
- Late (61-100): Quiet certainty. "Yes." "Okay." "Whatever you want."

### Emotional Quadrants (devotion x awareness)
| Quadrant | Behavior |
|----------|----------|
| LOW DEV / LOW AWARE | Stammers, drops things, can't complete sentences. |
| HIGH DEV / LOW AWARE | Follows like a moon. Brings gifts. "I just happened to be in the area." |
| HIGH DEV / HIGH AWARE | Quiet, intense devotion. "Yes" and "tell me what you want." |
| DEVOTED-ASSET | Total compliance. Lies for her. Covers for her. "Whatever you need." |

---

## NPC 3: RAY (npc_ray)

### Core Config
```toml
[npcs.npc_ray]
id = "npc_ray"
name = "Ray"
role = "Handyman"
age = 44
primary_driver = "SEDUCTION"
difficulty = "MEDIUM"
core_traits = { interest = 0 }
```

### Physical Appearance
5'11", 200lbs, lifts things for a living. Broad shoulders, thick forearms with veins. Weather-darkened skin. Dark brown hair going grey at temples. Brown eyes with crow's feet. Calloused hands, small scar on left knuckle.
- Working: worn jeans, work boots, faded t-shirt or shirtless. Sawdust on forearms.
- Bar: same jeans, clean flannel, boots. No "going out" clothes.

### Personality
- Surface: Quiet, economical with words. Not unfriendly, just efficient.
- Hidden: Lonely. Daughter lives with ex two towns over. Drinks at bar because alternative is empty house.

### Psychology
Married young, had daughter, amicable divorce. Got house, she got kid. Doesn't date -- decided vulnerability isn't worth the risk. Registers Emma as "the new schoolteacher" / "a nice kid" -- she doesn't exist in his sexual awareness. That's the wall she must break.

### Internal Contradictions
1. Doesn't want to want her, but body decides before mind
2. Thinks she's too young, but that's what makes it electrifying
3. Wants to keep it physical, but she makes him feel things

### Resistance Pattern
| Stage | Behavior |
|-------|----------|
| MILD | Doesn't exist traditionally -- she's invisible. Not a wall, just a category she doesn't fit. |
| MODERATE | Pulls back to formality. "Miss." "Ma'am." Finds work somewhere else. |
| SEVERE | Blunt honesty. "This is a bad idea. You know that." Can't stop looking at her mouth. |
| RECOVERY | Shows up. Fixes something near her room. Truck parked where she can see. Exhales when she approaches. |

### Emotional Tells by Stat Range (interest)
| Range | Behavior |
|-------|----------|
| 0-20 | "Evening, Miss." Period. Doesn't look up from drink. |
| 21-40 | He looks. Watches her cross the bar. Holds eye contact one beat before looking away. |
| 41-60 | Speaks first ("Whiskey tonight?"). Remembers her drink. Laughs at her jokes. |
| 61-80 | Stands close enough to smell sawdust/soap. Hand on lower back. Fixes things without being asked. |
| 81-100 | Says "Emma" instead of "Miss." Tells her about daughter, marriage. The stoic man is leaking. |

### Speech Patterns
- Early (0-30): Minimal. "Beer's cold." "Fence needs work." "Evening."
- Mid (31-60): Offers more. "Didn't take you for a whiskey girl." Dry humor.
- Late (61-100): Full sentences. "I was married for twelve years." Voice drops lower when alone.

### Emotional Quadrants (interest x emotional investment)
| Quadrant | Behavior |
|----------|----------|
| LOW INT / LOW INVEST | Polite, functional. "Evening, Miss." She's wallpaper. |
| HIGH INT / LOW INVEST | Rattled. Catches him looking. Grips beer tighter. Leaves early. |
| HIGH INT / HIGH INVEST | Does things unasked. Fixes faucet. Saves barstool. Asks "You eat yet?" |
| FULLY INVESTED | Tells about daughter unprompted. The real version. Cries in truck. |

### Hidden Mechanic
If interest exceeds 80, real feelings develop -- story-triggered complication, not stat-tracked.

---

## NPC 4: MARK (npc_mark)

### Core Config
```toml
[npcs.npc_mark]
id = "npc_mark"
name = "Mark"
role = "Student's Father (Insurance Agent)"
age = ~38
primary_driver = "FORBIDDEN"
secondary_driver = "SEDUCTION"
difficulty = "HARD"
core_traits = { desire = 0, guilt = 0 }
```

### Physical Appearance
5'10", fit from gym routine (duty, not vanity). Dark hair with early grey at temples. Clean-shaven jaw, straight nose, brown eyes. Catalog-handsome, non-threatening.
- School events: pressed khakis, button-down with sleeves rolled once. Department store cologne.
- Casual: polo shirt, well-fitting jeans. About to go to brunch or PTA meeting.

### Personality
- Surface: Responsible, dependable, community-oriented. Coaches little league. Definition of reliable.
- Hidden: Hollow. Marriage died years ago. Karen sleeps in other bedroom. No sex in months. At 2am lies awake wondering if this is all there is.

### Psychology
Married Karen at 26 (she was pretty, mother approved). Son Tyler is only alive thing. Everything else is infrastructure for Tyler's childhood. Noticed Emma at conference -- she looked at HIM, not "Tyler's father." Terror: if discovered, his son finds out.

### Internal Contradictions
1. Wants Emma but wanting her makes him the man he swore he'd never be
2. Wants to leave Karen but can't because of Tyler
3. Wants Emma to understand the risk but also wants her to not care

### Resistance Pattern
| Stage | Behavior |
|-------|----------|
| MILD | Overperforms normalcy. "So, Tyler's grades..." Steers back to son. Checks phone -- "Karen just texted." |
| MODERATE | Cancels. "Something came up with Tyler." Radio silence 2-3 days. At church performing marriage harder. |
| SEVERE | Guilt explosion. "What are we doing? I have a son. He sits in YOUR classroom." Paces. Might cry. |
| RECOVERY | Shows up at her door at night. "Karen thinks I'm at a meeting." No speech. He chose the risk. |

### Emotional Tells by Stat Range (desire)
| Range | Behavior |
|-------|----------|
| 0-20 | Polite parent mode. Appropriate eye contact. Mentions Karen naturally. |
| 21-40 | Lingers. Asks about Emma, not Tyler. Notices what she wears. |
| 41-60 | Creates reasons to be there. Volunteers for everything. Texts warm. Emoji. |
| 61-80 | Reckless. Shows up without reason. Hand on her back. Doesn't delete texts. |
| 81-100 | Lost. "I think about you constantly." "She doesn't make me feel anything." Ready to destroy everything. |

### Guilt Stat Tells (guilt)
| Range | Behavior |
|-------|----------|
| 0-10 | Compartmentalized perfectly. Functional affair state. |
| 11-20 | Small cracks. Flinches when Tyler says "Miss Emma" at dinner. |
| 21-30 | Overcompensates. Flowers for Karen. Park with Tyler. Bittersweet. |
| 31-40 | Starts confessing to Emma. "I feel like a terrible person." Needs absolution. |
| 41-50 | BREAKING POINT. Can't hold both worlds. Might confess to Karen. NUCLEAR. |

### Guilt Economy
| Source | Guilt Change |
|--------|-------------|
| Any physical escalation | +1 to +3 |
| Seeing Tyler after encounter | +2 to +4 |
| Karen suspicion event | +3 to +5 |
| Emma says "you're a good man" | -2 to -3 |
| Emma says "we both wanted this" | -1 to -2 |
| Emma says "you did what you wanted" | +1 to +2 |
| Time passing without contact | -1 per 2 days |

**Sweet spot**: guilt 15-30. Below 15: forbidden thrill dies. Above 30: spiraling, canceling, confessing.

### Speech Patterns
- Early (0-30): Professional. "Tyler's reading scores are excellent." Karen's name as force field.
- Mid (31-60): Force field cracks. Personal questions. Karen mentioned less.
- Late (61-100): Raw. "I shouldn't be here." (He's here.) "We need to stop." (He doesn't.)

### Emotional Quadrants (desire x guilt)
| Quadrant | Behavior |
|----------|----------|
| LOW DESIRE / LOW GUILT | Generic parent. Firm handshake. Leaves when meeting's over. |
| LOW DESIRE / HIGH GUILT | Avoids her. Performs marriage with Karen desperately. |
| HIGH DESIRE / LOW GUILT | Dangerous calm. Accepted it. Texts warm, visits regular. Gets careless. |
| HIGH DESIRE / HIGH GUILT | EXPLOSIVE. Wants her desperately, hates himself. Texts "We need to stop" at midnight and "I miss you" at 12:04. |

---

## NPC 5: JAKE (npc_jake)

### Core Config
```toml
[npcs.npc_jake]
id = "npc_jake"
name = "Jake"
role = "Bartender"
age = ~28
primary_driver = "DOMINANCE"
difficulty = "ENDGAME"
core_traits = { power = 100 }
```

**INVERTED STAT**: power starts at 100 (he's in control), decreases toward 0 as Emma takes over. At 50: balanced/crackling. At 20 or below: fully submissive.

### Physical Appearance
5'11", lean/cut (pull-ups not squats). Visible forearms, tattoo sleeve left arm (abstract, black), ribs tattoo. Dark hair, styled with effort he pretends he didn't make. Sharp jaw, two-day stubble, brown eyes with lazy knowing quality. Half-smile default.
- Bar: fitted black t-shirt (tight, he knows), jeans, boots. Sleeves rolled once.
- Off duty: similar. Leather jacket in winter. Always performing "Jake."

### Personality
- Surface: Cocky, charming, effortlessly sexual. Flirts with every woman. "What can I get you, beautiful?"
- Hidden: Empty. Confidence is shell around nothing. No hobbies, no ambitions, no close friends. Never been challenged, refused, or seen past surface.

### Psychology
Grew up pretty. Never needed depth. Never had relationship longer than 2 months. Never been dumped. Never been in love. When "old Emma" shut him down, filed under "prude." When "new Emma" starts playing him, doesn't recognize what's happening. Existential crisis: she sees through his performance.

### Internal Contradictions
1. Wants to fuck her but she wants to OWN him -- difference is everything
2. Needs to be in control but control is what he's worst at
3. Doesn't want to feel anything but she makes him feel everything

### Resistance Pattern
| Stage | Behavior |
|-------|----------|
| MILD | Doubles down on charm. "Playing hard to get? I like that." Interprets control as foreplay. |
| MODERATE | Cockiness cracks. Lines fail. Asks questions, remembers answers. Shows up early. Irritated he doesn't understand. |
| SEVERE | Ego crisis. "What the fuck do you want from me?" Genuine confusion/fear. Swagger drops. |
| RECOVERY | Submits quietly. Different. "What do you want me to do?" Tentative first, then surrender. Likes not performing. |

### Emotional Tells by Stat Range (power, descending)
| Range | Behavior |
|-------|----------|
| 100-81 | Full Jake. She doesn't exist as challenge. Flirts on autopilot. |
| 80-61 | She's registered as different. Stops flirting with others when she's in room. |
| 60-41 | THE FLIP. Nervous. Drops glass. Asks her opinions. Checks her reaction before his. |
| 40-21 | Surrender in progress. Follows with eyes. "Come here" and he comes. No delay. |
| 20-0 | Complete submission. She makes all decisions. Most peaceful he's ever felt. |

### Speech Patterns
- Early (100-70): Polished, rehearsed. "I've been told I'm an acquired taste." All innuendo.
- Mid (70-40): Lines fail. "You're different. I don't mean that as a line. I mean-- shit."
- Late (40-0): Stripped simple. "I don't know how to do this." "Tell me what you want."

### Emotional Quadrants (ego x submission)
| Quadrant | Behavior |
|----------|----------|
| HIGH EGO / LOW SUB (power 80-100) | Full performance. Lazy smile. Winks at everyone. Insufferable and magnetic. |
| HIGH EGO / HIGH SUB (power 40-60) | Best version. Swagger fraying. Makes cocky comment then checks if she's impressed. |
| LOW EGO / HIGH SUB (power 10-30) | Performance gone. Quiet. Open. Vulnerable. "Tell me what you want. I'll do it." |
| LOW EGO / LOW SUB (rare, crisis) | Empty. Not submissive, not performing. "I don't know what you want from me." |

### Jake Stat Inversion Note
All gains that would be +X for other NPCs are -X for Jake's power stat. Activity win: power -2. Gate event: power -5 to -8. At power 0: fully submissive.

---

## NPC STAT GROWTH RATES

### Per-NPC Activity Gains
| Source | NPC Stat Gain | Frequency |
|--------|--------------|-----------|
| Base activity exit (non-escalating) | +1 | Per visit |
| Suggestive/warm choice | +2 | Per visit |
| Kiss-tier choice | +2 | Per visit |
| Oral-tier choice | +2 to +3 | Per visit |
| Sex-tier choice | +3 | Per visit |
| Minor story event | +1 to +3 | One-time |
| Major story event (gate-setter) | +3 to +8 | One-time |
| NPC-specific story bonus | Variable | One-time |

### Player Stat Sources
| Source | Stat | Gain |
|--------|------|------|
| Jolene Phase 1 events | corruption | +1 to +5 per event (~16 total) |
| Successful seduction move | corruption | +1 per move |
| NPC gate unlock events | corruption | +3 to +5 per gate |
| Successful bold choice | confidence | +1 to +3 |
| Ray scenes (doubled) | confidence | +2 to +6 |
| Jolene mentoring | confidence | +1 per visit |
| Humiliation/rejection | confidence | -2 to -5 |
| Getting caught/near-miss | confidence | -1 to -3 |
| Church attendance | reputation | +3 weekly |
| School events/PTA | reputation | +2 to +4 (1-2x/week) |
| Volunteering | reputation | +4 weekly |
| Neighborly visits | reputation | +2 (2x/week) |
| Risky NPC encounter | reputation | -1 to -5 |
| Gossip circulating | reputation | -1 to -2 passive |
| Bar presence (4+ nights/week) | reputation | -1 weekly |
| Karen confrontation | reputation | -5 to -8 one-time |
