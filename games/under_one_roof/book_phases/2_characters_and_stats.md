# PHASE 2: CHARACTERS & STAT ECONOMY
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: PLAYER DEFINITION

### Lily Chen — The Player Character

**Name**: Lily Chen
**Age**: 19
**Portrait Reference**: Dark-haired East Asian young woman, slim build, average height. Messy bun or ponytail. Youthful face — looks younger than 19. The kind of face you'd trust immediately.

**Background**: Art student, second year at the local state college. Parents divorced when she was 14. Mom (Diana) remarried Frank Harmon 8 months ago. Lily attended the wedding, made small talk with Frank's sons, went home. She doesn't know these people.

Diana takes a 10-week overseas nursing contract in Dubai — the money is too good to refuse. Lily was supposed to stay in her college dorm, but mid-semester flooding makes it uninhabitable. Insurance won't cover alternative housing. Diana arranges for Lily to stay at Frank's rural property with his two adult sons.

Lily arrives with one suitcase to a house she's been to exactly once.

**Sexual History**: Limited. A boyfriend in high school that lasted 4 months. She's not innocent — she's inexperienced. She knows what sex is. She's just never had it be complicated.

### Starting Stats

```
corruption  = 0      # Primary progression driver. Gates choices across all NPC arcs.
confidence  = 10     # How she carries herself. Gates assertiveness and self-initiated escalation.
money       = 400    # Economic pressure engine. Depletes through expenses.
energy      = 100    # Daily activity budget. Resets on sleep.
fitness     = 20     # Body condition. Built through exercise. Decays without maintenance.
beauty      = 30     # Presentation. Built through grooming, makeup, skincare. Decays without maintenance.
```

| Stat | Start | Range | Clamp | Purpose |
|------|-------|-------|-------|---------|
| **corruption** | 0 | 0-250 | false | Gates which activity choices appear. Grows from activities (+2-5), random encounters (+2-3), story events (+3-8). The player's internal transformation — tracks how far Lily has moved from who she was on day one. |
| **confidence** | 10 | 0-100 | true | Gates assertiveness choices (negotiating pay, refusing demands, standing up for herself, self-initiating physical encounters). Grows from exercise, confrontations, art achievements, wearing bold clothes. Does NOT decay — represents permanent growth. |
| **money** | 400 | unclamped | false | Depletes through monthly expenses (~$385/month). Replenished through household work and jobs. The impossible math forces escalation. |
| **energy** | 100 | 0-100 | true (dynamic max: 100 base, 110 at fitness 61+) | Daily budget forcing prioritization. 4-5 activities/day without rest, 6-7 with naps/meals. Resets to max on full sleep. |
| **fitness** | 20 | 0-100 | true | How her body looks and performs. Built through gym, swimming, jogging, hiking, job site labor. Affects NPC reactions to her body, unlocks stamina-related choices, increases energy max at 61+. Decays -1 per 3 days without exercise. |
| **beauty** | 30 | 0-100 | true | How her face/hair/presentation looks. Built through grooming routines, makeup, skincare, hairstyles. Affects diner tips, NPC compliments, love gain bonuses. Decays -1 per 2 days without grooming. |

### Player Psychology (REQUIRED)

| Field | Value |
|-------|-------|
| **Want** | Independence — finish her degree, get her own place, stop depending on anyone |
| **Need** | Connection — she's been isolated since the divorce, builds walls, keeps people at distance |
| **Fear** | Being trapped — dependency on people she can't trust or control |
| **Flaw** | Pride — she'd rather suffer quietly than ask for help. She'll find her own solutions, even if those solutions push her boundaries |

**How the flaw drives the game**: Lily's pride is the economic engine. She won't ask Frank for money. She won't admit she's struggling. She won't call her mom crying. This pride is what the economic pressure exploits — she'll find her *own* solutions, and each solution pulls her deeper. The game never tells her to take her clothes off. The math does, and her pride closes every exit that doesn't involve going deeper.

### Player Emotional Phases (REQUIRED)

| Phase | Triggered By | Player Mindset | How It Shows in Narration |
|-------|-------------|----------------|--------------------------|
| **OUTSIDER** | Arrival (Day 1) | "I don't belong here. This is temporary. I'll be out in ten weeks." | Short sentences. Notices house layout, awkward silences, the smell of sawdust. Counts days. Refers to NPCs by role: "my step-dad," "the older one," "the quiet one." |
| **SETTLING** | First week complete / first chore accepted | "These are just people. I can make this work." | Starts noticing NPC routines — Frank's 5 AM coffee, Jake's humming while he draws, Ryan's boots by the door. Refers to NPCs by name. Internal voice relaxes. |
| **AWARE** | First physical awareness / `exposure_unlock` fires | "Something is changing. In them. In me. I don't hate it." | Notices bodies, proximity, charged moments. Starts caring about what she wears. Narration gets physically specific — collarbone, forearms, the way a shirt sits. Longer internal passages. |
| **WANTING** | First kiss / `kiss_unlock` fires | "I want this. I shouldn't, but I want this." | Stops pretending encounters are accidental. Seeks out specific NPCs. Internal voice admits desire without qualifying it. Narration becomes anticipatory — what she hopes will happen, not just what does. |
| **TORN** | Crisis events (Frank discovers drawings / brothers clash) | "This is falling apart. What have I done?" | Guilt, fear, desperation. Contradictory internal voice — "I need to stop" followed by "I can't stop." Questions every decision. Notices what she'd lose. Longest internal passages. |
| **COMMITTED** | Crisis resolved / `crisis_resolved` flag | "This is who I am now. I choose this." | Confident, deliberate. Initiates instead of reacting. Manages relationships consciously. Internal voice is direct, unapologetic. Shorter sentences — certainty needs fewer words. |
| **ENDGAME** | Mom's return announced / `mom_returning` flag | "She's coming home. Time's up. What am I?" | Urgency in every interaction. Every moment weighted. Final choices carry existential weight. Narration oscillates between desperate intensity and quiet reflection. |

### Player Internal Voice (REQUIRED)

**What Lily notices (evolves over time):**

| Phase | What She Notices | Example |
|-------|-----------------|---------|
| OUTSIDER | Environment, layout, rules, exits | "The hallway is narrow. His room is right next to mine. The walls are thin." |
| SETTLING | NPC habits, routines, patterns | "Frank makes coffee at 5 AM. I can hear the grinder through the floor. Jake draws until his light clicks off at midnight." |
| AWARE | Bodies, proximity, tension | "Ryan came back from the job site shirtless. Sweat on his collarbone. I looked for three seconds too long." |
| WANTING | Anticipation, desire, plans | "Jake's door is cracked open. I could knock. I want to knock." |
| TORN | Stakes, consequences, what she'd lose | "If Frank finds out about Jake, he'll call Mom. If Ryan finds out about Frank, I don't know what happens." |
| COMMITTED | The relationships themselves, shared history | "Jake's hand shakes when he draws me now. It didn't used to. I know exactly when it started." |
| ENDGAME | Time, finality, identity | "Three more days. She'll walk through that door and see... what? Who am I now?" |

**How Lily describes each NPC (evolves over time):**

| Phase | @frank | @ryan | @jake |
|-------|--------|-------|-------|
| OUTSIDER | "My step-dad. Broad. Quiet. Smells like sawdust." | "The older one. Loud. Thinks he's funny." | "The quiet one. Draws a lot. Won't make eye contact." |
| SETTLING | "Frank. Runs things. Fair, actually." | "Ryan. Relentless, but not mean." | "Jake. Sweet. We have stuff in common." |
| AWARE | "His hands. The way he fills a doorway." | "Those arms. The way his jeans sit." | "His eyes behind the glasses. The focus." |
| WANTING | "He looked at me like he was deciding something." | "He leaned in and I didn't pull away." | "He touched my wrist while positioning my hand. Neither of us moved." |
| TORN | "He trusted me. I'm in his house." | "He's going to figure it out." | "I'm going to hurt him." |
| COMMITTED | "He knows what I am and he wants me anyway." | "We understand each other." | "He draws me like I'm the only thing worth looking at." |

**Choice text framing (evolves over time):**

| Phase | Tone | Example Choices |
|-------|------|-----------------|
| OUTSIDER | Cautious, polite | "Offer to help with dishes" / "Go to your room" |
| SETTLING | Friendly, practical | "Ask Jake about his drawings" / "Do your own homework" |
| AWARE | Physically charged, risk-aware | "Hold the pose a little longer" / "Cover up" |
| WANTING | Direct, desire-forward | "Kiss him back" / "Pull away" |
| TORN | High-stakes, emotional | "Tell him the truth" / "Lie" |
| COMMITTED | Confident, initiating | "Go to his room tonight" / "Sleep alone" |
| ENDGAME | Urgent, defining | "One last night together" / "Start saying goodbye" |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: NPC DEFINITIONS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### NPC 1: FRANK HARMON — The Step-Father

#### Physical Appearance
Broad shoulders, calloused hands from decades of construction work. Salt-and-pepper stubble, always slightly unshaven. Crow's feet around steady dark eyes — the kind that don't blink when they look at you. Smells like sawdust and black coffee. Wears flannels with rolled sleeves, work boots, jeans that fit right. At 45, he hasn't gone soft — the job site keeps him solid. Mornings: flannel, coffee mug. Evenings: same flannel, sleeves down, whiskey instead of coffee. Late nights: undershirt, barefoot, the controlled version of himself coming loose at the seams.

#### Personality Traits
**Surface (what people see):** Responsible. Steady. A man who says what he means and doesn't say much. Good father. Fair employer. Pays his debts.
**Hidden (what emerges):** Lonely. Hungry. Controlled to the point of compression. The control isn't strength — it's a dam holding back everything he won't let himself feel since his first wife left and Diana is always overseas.

#### Psychology
Frank wants to be the man Diana married — responsible, paternal, trustworthy. He's terrified of being the man he actually is — a 45-year-old who's been alone too long, whose new wife is on another continent, and whose step-daughter is walking around his house in increasingly less clothing.

His internal conflict is between duty and desire. He set the house rules. He maintains distance. He calls Lily by her name, never a nickname. Every structural decision he makes — separate bathrooms, dinner schedule, giving her a job in his office — is designed to keep things appropriate. And every one of those decisions brings her closer.

He responds to intimacy with withdrawal — then overcorrection. If his hand touches hers reaching for the salt, he leaves the room. The withdrawal is disproportionate, which is how Lily knows he felt it too. When he finally stops withdrawing, it's not a gradual opening — it's a break. The dam doesn't leak. It cracks.

#### Internal Contradictions (REQUIRED)

1. **He promised Diana he'd take care of Lily** — BUT he is the biggest threat to her under this roof. Every protective action (driving her to campus, giving her work, setting house rules) puts her deeper in his orbit. The protector IS the danger.

2. **He uses his authority to maintain boundaries** — BUT the authority itself is the turn-on. "Put something on before your brothers see you" is a command. He's telling her what to wear. Every boundary he sets reinforces the power dynamic that eventually breaks him.

3. **He prides himself on self-control** — BUT the control is brittle, not flexible. He doesn't bend — he holds, holds, holds, then shatters. His resistance makes the eventual break devastating because there's no gradual slide. He goes from iron discipline to "lock the door" in the space of a single scene.

#### Resistance Pattern (REQUIRED)

| Stage | Frank's Resistance Behavior | What Triggers It |
|-------|---------------------------|-----------------|
| **MILD** | Leaves the room. Pours more coffee. Doesn't make eye contact for an hour. Says "I need to get back to the workshop." Over-formal — calls her "Lily" instead of relaxing into conversation. | Any charged moment: her hand on his, eye contact held too long, her wearing Cute+ clothing near him. |
| **MODERATE** | Cancels the bookkeeping session. "I can handle it myself this week." Creates physical barriers — sits behind the desk instead of beside her. Adds new house rules. Avoids being alone with her for 2-3 days. | After a physical milestone fires between them. After he catches himself looking. After discovering drawings or other evidence. |
| **SEVERE** | Direct confrontation. "This stops. Whatever this is." Voice is tight, not loud. Hands flat on the desk. He doesn't threaten — he states. Avoids all non-essential interaction for 3-5 days. Eats dinner in the workshop. | After a line is explicitly crossed: a kiss, a touch that can't be misread, the brothers discovering something. |
| **RECOVERY** | Stays in the kitchen past midnight. Doesn't speak first but doesn't leave when she enters. Pours her coffee without being asked. The silence is different — loaded, not cold. Eventually: "Sit down." Two words. An opening. | After Lily demonstrates patience. After she handles the household well in his absence. After a vulnerability moment — he needs something fixed and she's the one who helps. |

#### Emotional Quadrant Behaviors (REQUIRED)

| Quadrant | Frank's Specific Behaviors |
|----------|---------------------------|
| **DISTANT** (low love / low trust) | Functional and clipped. "Dinner's at six." Doesn't sit when she's in the room — stays standing, keeps exit access. Reads the paper at breakfast instead of talking. Leaves his office door open when she's doing bookkeeping (witness insurance). Refers to her as "Diana's daughter" when talking to Ryan. |
| **SAFE** (low love / high trust) | Relaxed but unromantic. Asks about her classes, remembers her answers. Leaves money on the counter for art supplies without being asked. Closes the office door during bookkeeping because he trusts her now — but the trust is professional, not charged. Tells stories about building the house. Laughs sometimes — low, surprised, like he forgot he could. |
| **CONFLICTED** (high love / low trust) | The most common Frank state. He wants her and is fighting it. Stays in rooms longer than he should but stands at maximum distance. Stares at the spot where she was sitting after she leaves. Makes rules that create proximity ("You should eat breakfast with us" — an order wrapped in concern). Pours whiskey earlier in the evening. Grip on the coffee mug tightens when she walks through in sleepwear. Sentences start and stop: "You should—" (pause) "Never mind." |
| **OPEN** (high love / high trust) | Rare and devastating. The controlled man uncontrolled. Holds eye contact without looking away first. Sits next to her instead of across. Voice gets lower — not louder, lower. Calls her "Lil" for the first time (then catches himself, then does it again). Touches the small of her back guiding her through a doorway and doesn't pull away. Leaves his bedroom door unlocked. Says what he actually means: "Stay." |

#### Emotional Tells by Stat Range (REQUIRED)

**Love Tells (Frank):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-5 | "He nods when you enter the kitchen. Pours his own coffee. Reads the paper. You're a guest he's tolerating." |
| 6-12 | "He pours your coffee too. Black — he doesn't know how you take it yet. 'Classes going alright?' He's being polite. You think." |
| 13-20 | "He remembered you take cream. It's already in the mug. He watches you sit down, then looks away — but slower than before." |
| 21-28 | "He's already at the kitchen table when you arrive. Like he was waiting. The paper is open but he hasn't read it. His eyes track you across the room." |
| 29-35 | "He pushes the mug toward you as you sit. Their fingers almost touch. He doesn't pull his hand back. 'You look...' He stops. Drinks his coffee. Whatever he was going to say stays behind his teeth." |

**Trust Tells (Frank):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-8 | "His office door stays open when you're doing the books. He checks your work. Counts the cash drawer after you leave." |
| 9-15 | "Door stays open but he stops checking your work. Leaves receipts for you to file without supervision. 'You're doing fine.'" |
| 16-22 | "Door closes — he trusts the privacy. Tells you about a client who's late on payment. Business talk. You're inside the circle." |
| 23-28 | "Leaves you alone in the office with the books and the checkbook. Tells you about the business debt — the real numbers, not the ones he shows the boys. 'Don't tell Diana.'" |
| 29-35 | "Asks your opinion on a bid. Listens to the answer. Falls asleep in the office chair while you're working — the most vulnerable thing Frank Harmon has ever done in front of another human being." |

#### Speech Patterns

**Structure**: Short, declarative. Statements, not questions. Subject-verb-done. "Dinner's at six." "Clean up when you're finished." "I'll drive you."

**What he says vs what he means**: Almost everything Frank says has a subtext layer. "Put something on" means "I can see too much and I can't stop looking." "I'll drive you" means "I want to be the one who takes you." "That's enough for tonight" means "If we stay in this room one more minute I'm going to do something I can't take back."

**Evolution**: Early Frank speaks in commands and logistics. Mid-game Frank starts trailing off — unfinished sentences, longer pauses, the arrival of "..." in his dialogue. Late-game Frank uses fewer words but each one costs more. When he finally says something honest, it's devastating because you've been waiting 40 days to hear him mean something out loud.

**Signature phrases:**
- "That's enough." (boundaries)
- "I said I'll handle it." (control)
- "Sit down." (the moment he opens a door)
- "Diana trusts me." (the guilt he carries)

#### Starting Stats

```toml
[npcs.npc_frank]
name = "Frank"
core_traits = { love = 0, trust = 5, corruption = 0 }
# Trust starts at 5 — basic decency, not warmth. She's his wife's daughter.
```

#### Arc Concept Summary

- **Act 1 (corruption 0-100):** Professional, fatherly, maintains distance. Functional interactions — rides, dinner, bookkeeping. Micro-moments: hand on her back, watching her leave.
- **Act 2 (corruption 100-180):** Walls crack. Late-night kitchen encounters get longer. Bookkeeping sessions get quieter. He starts making excuses to be where she is.
- **Act 3 (corruption 180-240):** Control breaks. Forbidden fully embraced. Dominance emerges — stops asking, starts telling. Authority inverts from protective to possessive.

**Branch Point (Level 3, mid-game ~corruption 110):** Lily discovers Frank's financial secret — the business is in debt.
- **Path A: Confront him** → `chose_confront_frank` — adversarial-to-intimate. Anger, vulnerability, gratitude. Trust-to-love pipeline.
- **Path B: Keep his secret** → `chose_protect_frank` — conspiratorial. Private meetings shift from bookkeeping to real talk. Forbidden-intimacy pipeline.
- Both set `frank_secret_complete`. Tone changes, not direction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### NPC 2: RYAN HARMON — The Older Step-Brother

#### Physical Appearance
Athletic, tanned from outdoor work. Strong jaw, cocky grin that he knows is effective. Thick arms from hauling lumber and drywall — the kind of arms that fill a tank top. Wears tank tops, work boots, jeans slung low. Has a faded scar on his forearm from a job site accident he tells a different story about every time. At 23, he's in his physical prime and knows it. Mornings: shirtless if he thinks she's watching, tank top if he's being subtle (he's never being subtle). Job site: sweaty, dusty, rolled bandana on his forehead. Evenings: cleaned up just enough — cologne over sawdust, the grin reloaded.

#### Personality Traits
**Surface (what people see):** Confident. Teasing. Physical. The kind of guy who tests every boundary once to see what happens. Laughs easily. Makes everything feel like a dare.
**Hidden (what emerges):** Protective in ways he won't admit. Competitive with Jake, dismissive of Jake's "art kid" interests — but covers for him with Frank when Jake misses work. Genuinely lonely under the bravado — his confidence is an armor built from being the only one in the house who doesn't have someone.

#### Psychology
Ryan wants to be seen as the one who doesn't need anyone — the guy who takes what he wants and doesn't look back. He's afraid of wanting something he can't have — specifically, he's afraid of wanting Lily for more than just the physical, because wanting more means risking rejection on terms he can't joke away.

His internal conflict is between pursuit and vulnerability. He flirts because it's safe — flirting is a game, and games have defined winners and losers. But as Lily's corruption grows and she starts flirting BACK, the game changes. She's not resisting anymore. And Ryan doesn't know what to do with someone who says "yes" — because now it's real, and real means he could actually lose something.

He responds to intimacy with deflection — a joke, a change of subject, a physical escalation that replaces the emotional moment. "You're getting soft on me?" when what he means is "Am I getting soft on you?" When Lily breaks through that deflection, it's the first time Ryan is genuinely vulnerable in the game.

#### Internal Contradictions (REQUIRED)

1. **He treats Lily as a conquest** — BUT he starts developing real protective feelings. When a guy at the diner hits on her, Ryan doesn't laugh — he gets quiet. He wants her for himself, but "for himself" is shifting from "I got there first" to "nobody touches her."

2. **He pushes every boundary** — BUT he's scared of crossing a line that actually matters. Physical escalation is easy — he's done it a hundred times. Saying "I actually care about you" is the line he's terrified of, because it can't be taken back with a grin.

3. **He uses "you're not really my sister" as a license** — BUT he knows exactly what the taboo is. The technicality is an excuse. Underneath the excuse, he knows Diana is his step-mom, Lily is Diana's daughter, and Frank is his father. The "not really family" framing lets him do what he wants without examining what it means.

#### Resistance Pattern (REQUIRED)

| Stage | Ryan's Resistance Behavior | What Triggers It |
|-------|--------------------------|-----------------|
| **MILD** | Turns it into a joke. "Relax, I'm just messing with you." Physical withdrawal disguised as casualness — puts his hands behind his head, leans back, increases distance without looking like he's retreating. Sends a text instead of saying it out loud. | After an emotional moment lands too close to real. After Lily says something honest about him that he can't deflect. |
| **MODERATE** | Goes out without saying where. Comes home late. Avoids being alone with her for 1-2 days. Louder and more obnoxious at dinner — performing normalcy. Teases Jake harder than usual (displacement). | After he catches feelings and realizes it. After discovering Lily's involvement with Jake or Frank. After she rejects a physical advance he thought was guaranteed. |
| **SEVERE** | Confrontational but controlled. "You think this is a game? Because I don't." Not angry — hurt, which is worse coming from Ryan. Takes his truck and disappears for a day. Won't make eye contact for 2-3 days. | After Lily lies to him directly. After a major trust breach. After the brothers-discover-each-other crisis. |
| **RECOVERY** | Shows up with something — gas station coffee, a bag of art supplies he'd never buy himself. Doesn't apologize in words. Instead: "Heading to town, you coming or what?" The offer IS the apology. | After Lily gives him space without chasing him. After she does something that proves she's not just using him (covers for him with Frank, defends him). |

#### Emotional Quadrant Behaviors (REQUIRED)

| Quadrant | Ryan's Specific Behaviors |
|----------|--------------------------|
| **DISTANT** (low love / low trust) | Maximum performance mode. Loud at breakfast. Makes comments about Lily's appearance that are technically jokes. Offers rides that feel like traps — helpful with strings attached. Doesn't ask personal questions. Everything is a test. "You own gym clothes or...?" |
| **SAFE** (low love / high trust) | Calms down. Less performing, more genuine. Drives her to campus without commentary. Tells actual stories instead of bits — the scar on his forearm, why he dropped out of community college. Sits on the couch at a comfortable distance. Still teases, but the edge is gone. "You're alright, you know that?" |
| **CONFLICTED** (high love / low trust) | Jealous and visible about it. Watches Jake's door when Lily goes in. Truck rides get quieter — charged silence instead of banter. Makes possessive comments he tries to pass off as jokes: "Jake's real busy drawing lately." Gets competitive about activities: "Why don't you come to the gym instead of sitting in his room?" When he's near her, his body gravitates closer even as his words push away. |
| **OPEN** (high love / high trust) | The bravado drops. Quieter. More physical but less aggressive — a hand on the small of her back instead of a slap on the arm. Actually listens when she talks. Drives slower when she's in the truck, like he's stretching the time. "I don't want to go home yet" is the most vulnerable thing Ryan has ever said. Protects her without making it a joke. |

#### Emotional Tells by Stat Range (REQUIRED)

**Love Tells (Ryan):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-5 | "He looks at you like you're a new piece of furniture in the house. Interesting, temporary." |
| 6-12 | "He holds the truck door open. Still a test — watching if you'll say thank you. But he's paying attention now." |
| 13-18 | "He's cleaned the passenger seat. The empty cans are gone. The cab smells like pine air freshener. He doesn't mention it." |
| 19-25 | "He waits. That's the tell. Ryan doesn't wait for anyone. But he's in the truck, engine running, even though you said 'give me five minutes' ten minutes ago." |
| 26-35 | "He reaches across and tucks your hair behind your ear while you're talking. Then freezes. His hand hangs there for a second before he pulls it back. 'What were you saying?' Quieter than you've ever heard him." |

**Trust Tells (Ryan):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-5 | "He watches you from across the room like he's keeping score. Every smile counted, every move cataloged." |
| 6-12 | "He tells you the real story about the scar — not the funny version, the one where he was scared." |
| 13-18 | "He covers for you with Frank when you come home late. Doesn't ask where you were. Just: 'She was with me.'" |
| 19-25 | "He admits he didn't finish community college because he couldn't read fast enough. No joke after. Just silence, and the window down, and the road." |
| 26-35 | "He falls asleep in the truck with you after parking by the creek. He doesn't do that. Ryan doesn't fall asleep around people." |

#### Speech Patterns

**Structure**: Short, punchy, teasing. Uses questions as weapons: "You gonna wear that?" Turns statements into dares: "Bet you won't." Sprinkles in nicknames — "college girl," "roomie," eventually just "Lil" (different from Frank's "Lil" — Ryan's version is possessive, Frank's is tender).

**What he says vs what he means**: Ryan deflects everything real with humor. "Whatever" means "I care more than I'm going to show you." "You coming or what?" means "Please come." "I'm just messing with you" means "I meant every word but I'm scared you know that."

**Evolution**: Early Ryan is all surface — fast, loud, one-liners. Mid-game Ryan starts leaving silences where jokes used to go. Late-game Ryan says less but means everything. The biggest shift: when he stops asking questions (tests) and starts making statements (truths). "You coming?" becomes "I want you there."

**Signature phrases:**
- "You coming or what?" (invitations disguised as challenges)
- "Relax." (said when he's the one who needs to relax)
- "Whatever." (his armor word)
- "Not really my sister." (the license he uses, and eventually questions)

#### Starting Stats

```toml
[npcs.npc_ryan]
name = "Ryan"
core_traits = { love = 0, trust = 0, corruption = 10 }
# Corruption starts at 10 — he's already looking at her on day one. No pretense.
```

#### Arc Concept Summary

- **Act 1 (corruption 0-60):** Loudest presence. Teasing, offering rides, finding excuses to be shirtless. Testing Lily's boundaries.
- **Act 2 (corruption 60-150):** Truck rides get longer. Job site has private corners. Shows real protectiveness — covers for her, defends her. The lust gets a foundation of trust.
- **Act 3 (corruption 150-240):** Full physical escalation. Hungry, direct. Gym encounters, shower "accidents," truck parked remote. If he discovers Jake/Frank involvement: competitive, determined to win.

**Branch Point (Level 2, early-mid ~corruption 60):** In the truck, Ryan makes a physical move.
- **Slap his hand** → `ryan_resisted` — shifts to verbal seduction. More careful, testing with words. Seduction-flavored.
- **Let it happen** → `ryan_allowed` — gets bolder, more direct. Lust-flavored.
- Both set `truck_incident_complete`. Same journal entry, different tone going forward.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### NPC 3: JAKE HARMON — The Younger Step-Brother

#### Physical Appearance
Lean, not scrawny — just hasn't filled out yet. Shaggy brown hair that falls in his eyes. Wears glasses when he's drawing or reading, takes them off otherwise. Soft hands compared to his brother and father — artist's hands, graphite-stained fingertips. Usually in a faded band t-shirt and jeans. At 20, he's caught between boy and man — lanky frame still settling into its adult shape. Mornings: rumpled, squinting without glasses, t-shirt he slept in. Art sessions: focused, glasses on, sleeves pushed up, streak of charcoal on his forearm. Late nights: barefoot, old sweatpants, the sketchbook always within arm's reach.

#### Personality Traits
**Surface (what people see):** Shy. Quiet. The one who doesn't fit in the Harmon household of loud men. Draws constantly. Avoids eye contact with strangers. Polite in a way that makes him invisible at family dinners.
**Hidden (what emerges):** Observant in ways no one expects — he sees what Frank is hiding, how Ryan performs, what Lily needs before she says it. Passionate about art with an intensity that surprises people who mistake quiet for empty. Possessive in a way that surprises even him — once he decides someone is his to draw, to know, to love, he doesn't share easily.

#### Psychology
Jake wants to be seen — truly seen, not the version of himself his family acknowledges (the quiet kid, the art student, the one who's "different"). He's afraid of being ordinary — of his art being a hobby instead of a calling, of Lily seeing him the way Ryan sees him (small, unimportant).

His internal conflict is between tenderness and obsession. His feelings for Lily start genuine — affection, artistic fascination, the relief of finding someone who gets him. But genuine feelings in close proximity become consuming. He draws her face from memory. He listens through the wall. He notices when she comes back from Ryan's truck and catalogs what's different about her. The sweet boy is also the one who's been drawing her without permission, and the line between devotion and fixation is one he can't see clearly.

He responds to intimacy with openness that's almost painful — he has no defenses. No jokes (like Ryan), no control (like Frank). When Lily is kind to him, he leans into it completely. This makes his corruption arc devastating: every escalation is consensual, mutual, and tender, which is exactly why it hits differently.

#### Internal Contradictions (REQUIRED)

1. **He wants to protect Lily from the other men in the house** — BUT he's crossing the same lines they are. He judges Ryan for being aggressive and Frank for being inappropriate, while secretly drawing Lily nude from memory and listening through the wall at night. The moral high ground is a comfortable lie.

2. **He wants the relationship to stay tender and pure** — BUT his desire is getting more intense. Early Jake draws her collarbone with reverence. Late Jake draws her body with hunger. He wants to be the good one, the different one — and every day the gap between who he thinks he is and what he actually wants gets wider.

3. **He sees Lily as a real person, not a conquest** — BUT art IS possession. Drawing someone is claiming them visually. His sketchbook is full of her — her hands, her jaw, the way light falls on her shoulder. He tells himself it's art. Lily tells herself it's flattering. Neither of them is entirely wrong, and neither is entirely honest.

#### Resistance Pattern (REQUIRED)

| Stage | Jake's Resistance Behavior | What Triggers It |
|-------|--------------------------|-----------------|
| **MILD** | Blushes and drops something. Changes the subject to art. Adjusts his glasses (nervous tell). Moves his sketchbook so she can't see what he was drawing. "It's nothing." Finds an excuse to leave: "I should probably work on my portfolio." | Any moment of physical tension he wasn't prepared for. Accidental touches. Lily changing the dynamic from friendly to charged. |
| **MODERATE** | Goes quiet — not cold, just internal. Draws with more intensity, like he's processing through the pencil. Doesn't knock on the wall at night. Avoids being alone with her for 1-2 days — not because he doesn't want to, but because he can't trust himself to be appropriate. | After a physical milestone. After seeing Lily come back from Ryan's truck or Frank's office. After realizing his drawings have crossed a line. |
| **SEVERE** | Emotionally raw, not confrontational. "I can't do this if it doesn't mean something." Eyes wet. Hands shaking. The sketchbook stays closed. He won't draw her until it's resolved. This is the only leverage Jake has — withdrawing the one thing she values from him. | After the secret sketches discovery. After learning about Lily's involvement with Ryan or Frank. After a direct emotional betrayal. |
| **RECOVERY** | Leaves a drawing under her door. Not a nude, not a pose — something small. Her coffee mug. Her shoes by the door. A detail only someone who watches her constantly would notice. The drawing IS the apology. Eventually: "I drew something for you. Do you want to see it?" | After Lily comes to him. After she chooses him in a visible way (sits next to him at dinner, asks to see his sketchbook). After she's honest about what she wants. |

#### Emotional Quadrant Behaviors (REQUIRED)

| Quadrant | Jake's Specific Behaviors |
|----------|--------------------------|
| **DISTANT** (low love / low trust) | Barely exists in her awareness. Eats fast, clears his plate, retreats to his room. Acknowledges her with a nod, nothing more. Draws landscapes, not people. Door closed. Headphones on. The wall between their rooms might as well be concrete. |
| **SAFE** (low love / high trust) | Warm but undirected. Shares his art willingly — landscapes, the creek, the house. Recommends books. Saves her a seat at the breakfast table. Talks about his classes, asks about hers. Comfortable silence when they're both in the kitchen studying. Friendship energy — present, easy, no charge. |
| **CONFLICTED** (high love / low trust) | The most painful version of Jake. He's in love with her and doesn't trust the situation — either because she's involved with Ryan/Frank, or because the crisis shattered something. Draws her compulsively but won't show her. Sits near her at dinner but can't eat. Starts sentences with her name and can't finish them. Knocks on the wall at night — just once — then nothing. His door is cracked open, the light is on, the invitation is there. But he won't say it out loud. |
| **OPEN** (high love / high trust) | Art becomes their language. He draws her while she talks and she doesn't have to hold still. Leaves his door open when he knows she's passing. Makes eye contact and holds it — for Jake, this is the equivalent of Ryan's grand gestures. His hand finds hers under the table at dinner. His sketchbook is open on the bed, her face on every page, and he's not embarrassed anymore. "I drew you again. I always draw you." |

#### Emotional Tells by Stat Range (REQUIRED)

**Love Tells (Jake):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-8 | "He glances up from his sketchbook when you enter. Small nod. Back to drawing. You're scenery." |
| 9-15 | "He's drawing and you realize the angle of his page means he can see you in his peripheral. The pencil moves differently when you're in the room." |
| 16-22 | "He shows you a drawing and his hand is shaking. Not the drawing itself — the act of showing. He's never shown anyone before you." |
| 23-30 | "He's drawn your hands. Just your hands. From three different angles. When you see them, he says 'I couldn't get the light right' — but the light is perfect. He just wanted to keep drawing." |
| 31-40 | "He stops drawing when you walk in. Not because he's hiding it. Because looking at you is better than any picture he could make. The sketchbook closes. His eyes don't." |

**Trust Tells (Jake):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-8 | "He keeps the sketchbook angled away. If you lean in, he turns the page. Whatever's on it isn't for you." |
| 9-15 | "He shows you the landscape he's working on. Professional distance — the work, not him. 'What do you think of the composition?'" |
| 16-22 | "He tells you about his professor who says he has talent. Then, quieter: 'Ryan thinks it's a waste of time.' He's trusting you with something that hurts." |
| 23-30 | "He draws with his door open when he knows you're in your room. An invitation. If you come in, he doesn't stop drawing — he pulls over a chair. You belong in his space now." |
| 31-40 | "He falls asleep drawing. The sketchbook is open on his chest — her face, her hands, a partial nude he hasn't finished. He didn't close it because he forgot you might see. He forgot because forgetting is trust." |

#### Speech Patterns

**Structure**: Incomplete sentences that trail into silence. Questions he already knows the answer to. Starts strong, loses confidence mid-thought. "I was thinking maybe we could—" (pause) "—if you're not busy." Frequent use of "I mean" and "it's not—" as hedges before saying something real.

**What he says vs what he means**: Jake is more transparent than the others, which makes his subtext subtler. "I drew you" means exactly what it says — but also means "I've been looking at you for hours and this is the result." "Do you want to see?" means "Please see me seeing you." "We shouldn't" means "I know we will and I want to."

**Evolution**: Early Jake stammers and trails off. Mid-game Jake becomes more articulate when they're alone — full sentences, direct questions, the stammer only returning when she surprises him. Late-game Jake says things simply and completely: "I love you." No hedging. No trailing off. The boy who couldn't finish a sentence found his ending.

**Signature phrases:**
- "I was just—" (caught doing something he can't explain)
- "Can I draw you?" (the invitation that means everything)
- "We shouldn't." (the protest that never holds)
- "I drew you again." (the truth he can't stop telling)

#### Starting Stats

```toml
[npcs.npc_jake]
name = "Jake"
core_traits = { love = 5, trust = 5, corruption = 0 }
# Love and trust start at 5 — genuine warmth from being similar ages,
# sharing the "outsider" feeling. Zero corruption — he hasn't considered
# her sexually yet.
```

#### Arc Concept Summary

- **Act 1 (corruption 0-50):** Bonding over art. Drawing sessions, studying together. She notices his sketchbook has her in it. First physical awareness through posing: "Hold still, I need to get the light on your collarbone."
- **Act 2 (corruption 50-130):** Art becomes the excuse. Poses get revealing. Shared wall at night becomes charged. Creek swim. First kiss — tender, guilty, mutual. "We shouldn't." "I know."
- **Act 3 (corruption 130-220):** Full emotional + physical escalation. Tenderness remains. He draws her nude. The sketchbook is their shared secret. If Frank or Ryan discovers the drawings → major crisis catalyst.

**Branch Point (Level 3, mid-game ~corruption 90):** Lily discovers Jake's SECRET intimate sketches — poses she didn't know he saw. Different from Beat 11 (where he shows her innocent art willingly).
- **"They're beautiful"** → `chose_tender_jake` — arc stays sweet. He draws her with consent. Art as shared language. Corruption + Love.
- **"You've been watching me?"** → `chose_possessive_jake` — arc turns darker. Shyness was hiding obsession. Sorry, then defiant, then desperate. Sweetness has teeth. Corruption + Dominance undertone.
- Both set `jake_sketches_discovered`. Emotional texture shifts dramatically.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### SECTION 2.5: NPC CUSTOMIZATION

All three NPCs are customizable at game start. The player can rename them and choose a relationship label.

```toml
[[npcs]]
id = "npc_frank"
name = "Frank"
customizable = true
relationship = "step-dad"
relationship_options = ["step-dad", "mom's boyfriend", "landlord"]
description = "45, broad shoulders, calloused hands, salt-and-pepper stubble..."
portrait = "frank.jpg"
core_traits = { love = 0, trust = 5, corruption = 0 }
flag_keys = []

[[npcs]]
id = "npc_ryan"
name = "Ryan"
customizable = true
relationship = "step-brother"
relationship_options = ["step-brother", "housemate", "roommate"]
description = "23, athletic, tanned, strong jaw, cocky grin..."
portrait = "ryan.jpg"
core_traits = { love = 0, trust = 0, corruption = 10 }
flag_keys = []

[[npcs]]
id = "npc_jake"
name = "Jake"
customizable = true
relationship = "step-brother"
relationship_options = ["step-brother", "housemate", "roommate"]
description = "20, lean, shaggy hair, glasses when drawing..."
portrait = "jake.jpg"
core_traits = { love = 5, trust = 5, corruption = 0 }
flag_keys = []
```

**Content Writing Rule**: ALL narrative content uses `@frank`, `@ryan`, `@jake` for names and `@frank.rel`, `@ryan.rel`, `@jake.rel` for relationship labels. All relationship options share the same cohabitation context.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: STAT ECONOMY DESIGN

### Player Corruption Growth

| Source | Gain | Frequency | Notes |
|--------|------|-----------|-------|
| Neutral activity choice (emotional/safe) | +1-2 | Per visit | Small ambient corruption from proximity |
| Escalating activity choice (physical) | +2-5 | Per visit | Higher tiers give more corruption |
| Random encounters (passive witnessing) | +2-3 | Per trigger (1/day max) | ~0.5-1 triggers/day average |
| Story events (minor) | +3-5 | One-time | Bus problem, creek swim, etc. |
| Story events (major) | +5-8 | One-time | First kiss, first handjob, crisis points |
| Wearing Bold+ clothing in town | +1-2 | Daily | Passive — NPCs stare, catcalls |
| Wearing Daring sleepwear around house at night | +1 | Nightly | Passive — walking to kitchen in lingerie |
| Bold makeup kit (when applied) | +1 | Daily | Self-corruption through presentation |

**Target corruption progression:**

| Day Range | Corruption Range | What's Happening |
|-----------|-----------------|------------------|
| Days 1-7 | 0-40 | Arrival, settling, personal discovery. Reaching 40 requires some escalation. |
| Days 8-15 | 40-70 | Bookkeeping unlocks. Jake arc deepens. Ryan pushes. |
| Days 16-25 | 70-100 | Kiss likely fired. Frank arc begins to stir. |
| Days 26-35 | 100-140 | Frank arc active. All three in play. Physical escalation. |
| Days 36-45 | 140-180 | Deep escalation. Oral tiers. Cross-NPC awareness. |
| Days 46-56 | 180-240 | Endgame. Sex tiers. Mom's return. Convergence. |

### Player Confidence Growth

| Source | Gain | Notes |
|--------|------|-------|
| Gym workout | +1 | +2 with proper athletic wear |
| Jogging (any) | +1 | Solo exercise builds self-reliance |
| Wearing Cute+ clothing (first time per tier) | +2 one-time | The mirror moment |
| Wearing Bold+ clothing (daily) | +1/day | She knows people are looking |
| Successful confrontation (story event) | +3-5 | Standing up to Ryan, negotiating with Frank |
| Art achievement / modeling | +2 | Per milestone |
| Diner waitressing shift | +1 | Per shift |
| Assertive dialogue choice | +1-2 | When she picks bold over safe |
| Fitness 21+ bonus | +1 extra on clothing confidence | Clothes fit better |
| Beauty 61+ bonus | +1 extra on social confidence | Compliments land harder |

**Key confidence thresholds:**
- 30: Required for diner job
- 60+: Required for Independent ending

### Per-NPC Stat Growth (Love / Trust / Corruption)

**How different activities build different NPC stats:**

| Activity Type | Love | Trust | Corruption | Example |
|---------------|------|-------|------------|---------|
| Meals together (T1 — eat) | +1 | +1 | — | Breakfast, dinner |
| Meals together (T2 — talk/flirt) | +2 | — | +1 | Deep conversation at dinner |
| Working together | — | +2 | — | Job site with Ryan, bookkeeping with Frank |
| Drawing sessions (Jake) | +2 | +1 | +1-2 | Higher corruption as poses escalate |
| Truck rides (Ryan) | +1 | +1 | +1-2 | Confined space, his comments |
| Bookkeeping (Frank) | +1 | +2 | +1-2 | Closed door, proximity |
| Deep emotional conversation | +2 | +2 | — | Late-night talks, vulnerability |
| Covering for NPC / keeping secrets | — | +3 | — | Frank's debt, Ryan's school, Jake's drawings |
| Physical encounter (escalating choice) | +1 | — | +2-3 | Each tier builds the NPC's corruption toward Lily |
| Story gift/sacrifice | +3 | +1 | — | NPC clothing gifts, acts of protection |
| Cooking together | +2 | +1 | — | Kitchen, evening |
| Creek swimming | +1 | — | +2-3 | Bodies + water + isolation |
| Gym together (Ryan) | — | +1 | +2 | Physical proximity, bodies |
| Hiking (group) | +1 | +1 | +1 | Whoever she walks with |

**Activities NEVER build all three stats equally.** This forces Lily to diversify — she can't grind one activity to max everything for one NPC. The player must balance emotional time (love/trust) with escalation activities (corruption) to unlock gate-setting story events.

### NPC Stat Growth Targets (Jake-first default path)

**Jake:**

| Day Range | Love | Trust | Corruption | Key Moments |
|-----------|------|-------|------------|-------------|
| Days 1-7 | 5→12 | 5→10 | 0→5 | Bonding, drawing sessions begin |
| Days 8-14 | 12→18 | 10→16 | 5→15 | Exposure, modeling begins |
| Days 15-25 | 18→25 | 16→22 | 15→30 | Kiss, deeper intimacy |
| Days 26-40 | 25→32 | 22→28 | 30→40 | Handjob/oral tiers |
| Days 41-56 | 32→40 | 28→35 | 40→50 | Sex tier, endgame |

**Ryan:**

| Day Range | Love | Trust | Corruption | Key Moments |
|-----------|------|-------|------------|-------------|
| Days 1-7 | 0→3 | 0→2 | 10→13 | Testing boundaries, truck rides begin |
| Days 8-14 | 3→8 | 2→8 | 13→18 | Job site work, gym trips |
| Days 15-25 | 8→15 | 8→14 | 18→28 | Truck incident, first real connection |
| Days 26-40 | 15→22 | 14→20 | 28→38 | Physical escalation, protectiveness |
| Days 41-56 | 22→30 | 20→25 | 38→45 | Full arc, competitive with Jake |

**Frank:**

| Day Range | Love | Trust | Corruption | Key Moments |
|-----------|------|-------|------------|-------------|
| Days 1-7 | 0→3 | 5→8 | 0→2 | Professional distance, house rules |
| Days 8-14 | 3→8 | 8→12 | 2→5 | Bookkeeping begins, building trust |
| Days 15-25 | 8→14 | 12→18 | 5→10 | Office proximity, first cracks |
| Days 26-40 | 14→22 | 18→24 | 10→18 | Late-night kitchen, control eroding |
| Days 41-56 | 22→32 | 24→30 | 18→28 | Full arc, dominance emerges |

### Player Resource Flows

**Income:**

| Source | Pay/Session | Energy | Time Slot | Corruption Gate | Notes |
|--------|-----------|--------|-----------|-----------------|-------|
| House cleaning | $20 | 25 | Late Morning | None | Available from week 1 |
| Bookkeeping (Frank) | $25 | 20 | Afternoon | corruption >= 40 | Unlocks ~week 3-4 |
| Job site labor (Ryan) | $40 | 25 | Late Morning | corruption >= 40 | Physical proximity |
| Art modeling — clothed (Jake) | $30 | 15 | Afternoon | corruption >= 50 | Poses escalate |
| Diner waitressing | $45 | 20 | Evening | confidence >= 30 | Misses dinner + night |
| "Overtime" bookkeeping (Frank) | $60 | 20 | Evening | corruption >= 100 | Alone, door closed, his terms |
| Art modeling — nude (Jake) | $80 | 15 | Afternoon | corruption >= 130 | Full exposure |
| Ryan's "favors" | $100 | 20 | Night | corruption >= 150 | Whatever Ryan asks |
| Frank's "arrangement" | $150 | 20 | Late Night | corruption >= 180 | Authority takes control |

**Recurring expenses:**

| Expense | Amount | Frequency | If Unpaid |
|---------|--------|-----------|-----------|
| Bus pass | $80 | Monthly | No bus travel. Must use Ryan's truck (increases dependency). |
| Art supplies | $60 | Monthly | Can't complete assignments. Loses campus events after 2 weeks. |
| Phone bill | $45 | Monthly | Phone cut off after 1 month. Mom can't call — misses story beats. |
| Food contribution | $50 | Weekly | frank_trust -3. "Pull your weight." Triggers once, then weekly. |
| **Total monthly** | **~$385** | | |

**Other income:**
- Mom sends $200/month (often late — Diana is overwhelmed, transfers bounce or arrive a week late)
- Starting money: $400

**Two-phase economic model:**

| Phase | Weekly Income | Weekly Expenses | Surplus | Pressure |
|-------|-------------|-----------------|---------|----------|
| **Weeks 1-3** (cleaning only) | $100 (5 cleans) | $96 (food $50 + bus+art+phone prorate $46) | **$4/week** | CRITICAL |
| **Weeks 4+** (bookkeeping unlocks) | $225 (clean + bookkeep daily) | $96 | **$129/week** | Comfortable — but corruption >= 40 already |

### Fitness Stat Economy

| Activity | Fitness Gain | Energy Cost | Location | Notes |
|----------|-------------|-------------|----------|-------|
| Gym workout | +3 | 30 | loc_gym (town) | Best source. Requires transport. |
| Jogging (park) | +2 | 20 | loc_park (town) | Afternoon. Better gains than property. |
| Jogging (property) | +1 | 15 | loc_yard | Anytime incl. mornings. No transport. |
| Creek swimming | +2 | 30 | loc_creek | Also builds corruption (bodies + water). |
| Hiking | +2 | 30 | loc_trail (weekends) | Also builds NPC stats with hiking partner. |
| Job site labor | +1 | 25 | loc_workshop | Side benefit of earning money. |
| Yoga in room | +1 | 10 | loc_lily_room | Solo, always available. Low energy, low reward. |

**Decay**: -1 fitness per 3 days without exercise.

**Level effects:**

| Fitness | Label | Mechanical Effect |
|---------|-------|-------------------|
| 0-20 | Average | No bonuses, no penalties |
| 21-40 | Toning up | +1 confidence from Cute+ clothing |
| 41-60 | Noticeable | NPC body dialogue upgrades. Swimwear scene upgrades. |
| 61-80 | Athletic | Energy max → 110. Stamina physical tier choices unlock. |
| 81-100 | Peak | +1 to ALL NPC corruption gains per interaction |

### Beauty Stat Economy

| Activity | Beauty Effect | Cost | Location | Notes |
|----------|-------------|------|----------|-------|
| Morning grooming | Prevents decay | Free | loc_bathroom | Minimum daily maintenance |
| Apply makeup (basic kit) | +1 daily buff | $20 kit | loc_lily_room | Buff until sleep |
| Apply makeup (cute kit) | +2 daily buff | $35 kit upgrade | loc_lily_room | Requires corruption >= 45 |
| Apply makeup (bold kit) | +2 buff + 1 corruption | $45 kit upgrade | loc_lily_room | Requires corruption >= 85 |
| Skincare routine | +1 permanent | $15 set | loc_bathroom | Once per day |
| Premium skincare | +2 permanent | $30 upgrade | loc_bathroom | Requires corruption >= 45 |
| New hairstyle #1 | +3 one-time | $30 | loc_clothing_store | NPCs comment 2-3 days |
| New hairstyle #2 | +3 one-time | $30 | loc_clothing_store | Bolder. Corruption >= 45. |
| New hairstyle #3 | +3 one-time | $30 | loc_clothing_store | Statement. Corruption >= 85. |
| Spa/self-care day | +2 permanent | 15 energy | loc_lily_room | Requires skincare products |
| Perfume | Narrative only | $25 | loc_clothing_store | Scent descriptions in ALL close NPC scenes |

**Decay**: -1 beauty per 2 days without grooming.

**Total beauty investment**: ~$260 across the full game.

**Level effects:**

| Beauty | Label | Mechanical Effect |
|--------|-------|-------------------|
| 0-20 | Neglected | Negative NPC comments. "You look tired." |
| 21-40 | Natural | Default. No bonuses, no penalties. |
| 41-60 | Pretty | Diner tips +15%. Casual compliments. |
| 61-80 | Beautiful | Diner tips +30%. +1 confidence from social activities. |
| 81-100 | Stunning | +1 to ALL NPC love gains per interaction |

### The "Polished" Daily State

**Polished = showered today + makeup applied + clothing tier Cute or above**

Effect: +1 to ALL NPC stat gains (love, trust, corruption) for that day.

Morning routine trade-off:
- Shower only: +10 energy, prevents beauty decay. No polished.
- Shower + grooming: +5 energy, prevents decay, enables "groomed." No polished without makeup + Cute outfit.
- Shower + grooming + makeup: +5 energy, prevents decay, +1-2 beauty buff, polished if Cute+ outfit.
- Skip everything: No energy restore from shower. Beauty decays. Looks rough.

The 5-energy difference between shower-only (+10) and grooming (+5) is the daily investment: 5 energy now vs. polished bonus (+1 all NPC gains) across 3-4 interactions all day.

### Energy Budget Summary

| Tier | Cost | Activities |
|------|------|-----------|
| Free | 0 | Sleep, shower, phone scroll, getting dressed, napping |
| Minimal | 5 | Check phone, journal, wander property |
| Light | 10 | Breakfast, lunch, quick conversation, stargazing |
| Moderate-light | 15 | Dinner, TV, drawing session, park bench |
| Moderate | 20 | Cooking together, bookkeeping, studying, diner shift, Ryan's errands |
| Heavy | 25 | Job site work, house cleaning, yard chores |
| Very heavy | 30 | Creek swimming, gym workout, hiking trail |

**Restoration:**

| Source | Restore |
|--------|---------|
| Full sleep (Late Night → Early Morning) | Set to max (100, or 110 at fitness 61+) |
| Afternoon nap | +20 |
| Shower | +10 |
| Breakfast T1 | +5 |
| Lunch T1 | +5 |
| Dinner T1 | +10 |

**Rules:**
- Story events (is_repeatable = false) NEVER have energy costs
- Random encounters NEVER have energy costs
- Restorative activities are FREE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: GATE FLAG DESIGN

### Gate Architecture

7 shared skill unlock flags, earnable through ANY NPC. Flags represent Lily's internal shift — she's crossed that mental barrier — not a milestone with a specific person. Whichever NPC she reaches that threshold with first sets the shared flag.

### Unlock Threshold Table (Per NPC)

| Flag | What It Unlocks | Jake Conditions | Ryan Conditions | Frank Conditions |
|------|----------------|-----------------|-----------------|------------------|
| `exposure_unlock` | Being seen / showing body choices | corruption >= 25, jake_love >= 10 | corruption >= 40, ryan_corruption >= 10 | corruption >= 60, frank_trust >= 10 |
| `flirt_unlock` | Flirting choices with all NPCs | corruption >= 40, jake_love >= 12 | corruption >= 50, ryan_love >= 8 | corruption >= 75, frank_trust >= 15 |
| `tease_unlock` | Teasing / showing off choices | corruption >= 55, jake_love >= 15, jake_trust >= 10 | corruption >= 70, ryan_corruption >= 15 | corruption >= 90, frank_love >= 15, frank_trust >= 15 |
| `kiss_unlock` | Kissing choices with all NPCs | corruption >= 70, jake_love >= 15, jake_trust >= 15 | corruption >= 85, ryan_love >= 12, ryan_trust >= 10, ryan_corruption >= 15 | corruption >= 120, frank_love >= 20, frank_trust >= 20 |
| `handjob_unlock` | Manual/groping tier choices | corruption >= 100, jake_love >= 20, jake_trust >= 18, jake_corruption >= 15 | corruption >= 110, ryan_love >= 15, ryan_trust >= 12, ryan_corruption >= 25 | corruption >= 140, frank_love >= 25, frank_trust >= 22 |
| `blowjob_unlock` | Oral tier choices | corruption >= 140, jake_love >= 25, jake_trust >= 20, jake_corruption >= 25 | corruption >= 150, ryan_love >= 18, ryan_trust >= 15, ryan_corruption >= 30 | corruption >= 180, frank_love >= 28, frank_trust >= 25 |
| `sex_unlock` | Full sex choices | corruption >= 180, jake_love >= 30, jake_trust >= 25, jake_corruption >= 30 | corruption >= 190, ryan_love >= 22, ryan_trust >= 18, ryan_corruption >= 35 | corruption >= 210, frank_love >= 30, frank_trust >= 28 |

### Gate-Setting Story Events (Default Jake-First Path)

| Gate | Most Likely Story Event | Approx Day | Corruption | Unlocks In Activities |
|------|------------------------|------------|------------|----------------------|
| `exposure_unlock` | Jake drawing session — she lowers a strap for the pose (Beat 7) | Day ~8 | ~25-30 | "Stand closer" physical sub-menu option in ALL NPC activities |
| `flirt_unlock` | Art modeling gets charged — she teases Jake while posing (Beat 13) | Day ~12 | ~40-50 | "Flirt with him" option (corruption >= 40 + flag) |
| `tease_unlock` | She poses provocatively on purpose for Jake (organic progression) | Day ~16 | ~55-65 | "Tease him" option (corruption >= 55 + flag) |
| `kiss_unlock` | Over the sketchbook — tender, mutual, guilty (Beat 14) | Day ~18 | ~70-80 | "Kiss him" option (corruption >= 70 + flag) |
| `handjob_unlock` | Drawing session turns physical — her hand on him (Beat 20) | Day ~28 | ~100-110 | "Touch him" option (corruption >= 100 + flag) |
| `blowjob_unlock` | Jake's room at night — tender, she wants to (organic) | Day ~38 | ~140-150 | "Use your mouth" option (corruption >= 140 + flag) |
| `sex_unlock` | His bed, eye contact, whispered names (organic) | Day ~46 | ~180-190 | "Go further" option (corruption >= 180 + flag) |

**Note:** These are the EXPECTED path. A Ryan-first or Frank-first player hits these milestones through different scenes at different corruption levels. The gate flag is the same regardless of source NPC.

### Narrative Flavor Per NPC (How Each Milestone FEELS)

| Flag | Jake (CORRUPTION + LOVE) | Ryan (LUST + SEDUCTION) | Frank (FORBIDDEN + DOMINANCE) |
|------|--------------------------|-------------------------|-------------------------------|
| `exposure_unlock` | Drawing session — she lowers a strap for the pose. His pencil stops. | Creek swim — bikini comes untied. He doesn't look away. | She walks out of the shower, he's in the hallway. Both freeze. |
| `flirt_unlock` | She teases him while posing, watches him blush. Tender. | She flirts back in the truck for the first time. Playful. | She makes a comment during bookkeeping that isn't about numbers. Charged. |
| `tease_unlock` | She poses provocatively on purpose, watching his reaction. | She wears the bikini he bought, knows he's watching. | She bends over the desk reaching for a file, takes her time. |
| `kiss_unlock` | Over the sketchbook. Tender, mutual, guilty. "We shouldn't." "I know." | In the truck, parked on a dirt road. He pulls her in. She lets him. | Kitchen at 2 AM. Coffee going cold. "This can't happen." Then he does it. |
| `handjob_unlock` | Drawing session turns physical. Her hand on him. Both shaking. | Truck parked somewhere remote. "You owe me." Direct. | Office, door locked. She reaches under the desk. Power. |
| `blowjob_unlock` | His room at night. Tender. She wants to. He can't believe it. | Gym shower or truck. Raw, direct. He tells her what he wants. | Office. He stands. She kneels. Dominance fully realized. |
| `sex_unlock` | His bed. Eye contact. Whispered names. Love. | Against a wall, truck bed, wherever the moment takes them. Need. | His bedroom. His rules. Door locked. Forbidden fully embraced. |

### First-Time vs Repeat Awareness (Group Block Variant)

Each NPC's milestone scene acknowledges whether this is Lily's FIRST time or she's done it before with another NPC:

**If flag NOT yet set (first time):**
> "She's never done this before. Her hands are shaking. The world narrows to just this moment — his breath, her heartbeat, the line she's about to cross."

**If flag already set (learned from another NPC):**
> "She's done this before. But not like this. Not with him. Everything she thought she knew about this act gets rewritten in the space between their bodies."

One extra group block per milestone scene per NPC. Low content cost, high emotional payoff.

### Cross-NPC Transfer Logic

Once a flag is set by ANY NPC's story scene → that tier of choices appears in ALL NPC activities.

The flag = "permission slip" (Lily is psychologically ready).
Each NPC's individual stat thresholds = "relationship earned it."

Both are always required. Never flag alone. Never stats alone.

### Physical Sub-Menu Thresholds (In Activities)

```
Physical choice → sub-menu:
  "Stand closer"        (always, after exposure_unlock)
  "Flirt with him"      (after flirt_unlock + corruption >= 40)
  "Tease him"           (after tease_unlock + corruption >= 55)
  "Kiss him"            (after kiss_unlock + corruption >= 70)
  "Touch him"           (after handjob_unlock + corruption >= 100)
  "Use your mouth"      (after blowjob_unlock + corruption >= 140)
  "Go further"          (after sex_unlock + corruption >= 180)
```

These corruption thresholds match the LOWEST flag-setting threshold (Jake's). Each choice ALSO requires NPC-specific stat thresholds.

### Minimum Narrative Distance Between Gates

| Transition | Minimum Gap |
|-----------|-------------|
| exposure → flirt | 1 tension event + 2 in-game days |
| flirt → tease | 1 bridge event + 2 in-game days |
| tease → kiss | 1 crisis moment + 3 in-game days |
| kiss → handjob | Major crisis + resolution |
| handjob → blowjob | 1 sacrifice choice + 3 in-game days |
| blowjob → sex | Turning point + 3 in-game days |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: COMPLETE FLAG INVENTORY

### Progression Flags (Story Event Completion)

| Flag | Set By | When |
|------|--------|------|
| `game_started` | Opening scene — Lily arrives | Day 1 |
| `first_morning` | Shared bathroom incident, breakfast dynamics | Day 2 |
| `bus_problem_discovered` | Lily discovers terrible bus schedule | Day 2-3 |
| `mom_called` | Diana calls — money transfer late | Day 3-4 |
| `money_crisis_realized` | Lily counts her money, internal monologue | Day 4-5 |
| `first_week_complete` | Week 1 milestone — routines established | Day 7 |
| `chores_started` | Lily offers to clean for cash | Day 6-7 |
| `drawing_started` | Jake asks if she'll model (clothed) | Day ~8 |
| `truck_incident_complete` | Ryan's first push in the truck | Day ~10 |
| `bookkeeping_started` | Frank offers bookkeeping work | Day ~12 |
| `first_swim` | First creek swim — physical exposure | Day ~10-12 |
| `saw_jakes_sketches` | Jake shows his sketchbook willingly (innocent art) | Day ~12-14 |
| `ryan_caught_her` | Ryan walks in on Lily changing | Day ~14 |
| `modeling_started` | Art modeling gets charged (Jake) | Day ~14 |
| `frank_kitchen_moment` | Late-night kitchen — his hand on hers | Day ~28 |
| `ryan_leverage` | Ryan knows about modeling/activities, wants arrangement | Day ~30 |
| `power_outage` | One night, no electricity — candles, proximity | Day ~32 |
| `frank_found_drawings` | Frank finds Jake's intimate sketches | Day ~35 |
| `financial_crisis` | Mom's transfer bounces, art supplies overdue | Day ~34 |
| `brothers_know` | Ryan finds out about Jake (or vice versa) | Day ~42 |
| `frank_offer` | "I'll cover everything. Here's what I want." | Day ~45 |
| `crisis_resolved` | Lily handles the brothers' discovery | Day ~44 |
| `mom_returning` | Diana announces early return | Day ~48 |
| `endgame_active` | Final week begins | Day ~50 |
| `game_complete` | Mom arrives. Resolution. | Day ~56 |

### Gate Flags (Shared Skill Unlocks)

| Flag | What It Enables | Approximate Day (Jake-first) |
|------|----------------|------------------------------|
| `exposure_unlock` | "Stand closer" in physical sub-menus | Day ~8 |
| `flirt_unlock` | "Flirt with him" choices | Day ~12 |
| `tease_unlock` | "Tease him" choices | Day ~16 |
| `kiss_unlock` | "Kiss him" choices | Day ~18 |
| `handjob_unlock` | "Touch him" choices | Day ~28 |
| `blowjob_unlock` | "Use your mouth" choices | Day ~38 |
| `sex_unlock` | "Go further" choices | Day ~46 |

### Branch Flags (Player Choices)

| Flag | Set By | Effect |
|------|--------|--------|
| `chose_tender_jake` | Jake branch — "They're beautiful" | Jake arc stays sweet. Corruption + Love. |
| `chose_possessive_jake` | Jake branch — "You've been watching me?" | Jake arc darkens. Corruption + Dominance undertone. |
| `jake_sketches_discovered` | Either Jake branch choice | Marks Jake branch complete. |
| `ryan_resisted` | Ryan branch — slap his hand | Ryan shifts to verbal seduction. |
| `ryan_allowed` | Ryan branch — let it happen | Ryan gets bolder, more direct. |
| `truck_incident_complete` | Either Ryan branch choice | Marks Ryan branch complete. |
| `chose_confront_frank` | Frank branch — confront about debt | Adversarial-to-intimate pipeline. |
| `chose_protect_frank` | Frank branch — keep his secret | Conspiratorial intimacy pipeline. |
| `frank_secret_complete` | Either Frank branch choice | Marks Frank branch complete. |
| `chose_independent` | Global crisis — "It's none of your business" | Lily asserts dominance. |
| `chose_peacemaker` | Global crisis — "Please don't fight" | Guilt + tenderness tone. |
| `chose_avoidant` | Global crisis — walk away silently | Short-term regression, Frank accelerates. |

### Utility Flags (System/Mechanic)

| Flag | Set By | Purpose |
|------|--------|---------|
| `town_access` | First ride with Ryan | Unlocks clothing store, gym, park, diner |
| `comfortable_braless` | Jake drawing session (removes bra for pose) | Bra no longer required in wardrobe |
| `discovered_teasing` | Ryan encounter where underwear becomes a factor | Underwear no longer required in wardrobe |
| `polished` | Daily state: shower + makeup + Cute+ outfit | +1 all NPC stat gains (recalculated each morning) |

### Ending Condition Flags

| Ending | Conditions |
|--------|-----------|
| **Jake's Girl** | Jake highest combined stats (love+trust+corruption), corruption < 160 |
| **Ryan's Conquest** | Ryan highest combined stats, corruption > 150 |
| **Frank's Arrangement** | Frank highest combined stats, corruption > 180 |
| **All Three** | No NPC more than 25 combined points ahead of others |
| **Independent** | confidence > 60, money > 500, diner job active |
| **Escape** | corruption < 100, low NPC stats across the board |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue to Phase 3: World Design,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
