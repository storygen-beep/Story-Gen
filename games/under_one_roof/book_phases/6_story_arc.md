# PHASE 6: STORY ARC
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 0: DRAMATIC SPINE SUMMARY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Central Tension

"Can a girl who swore she'd never depend on anyone survive a house where every form of help comes with a price — and still recognize herself when it's over?"

### Conflict Types

1. BOUNDARY BREAK — Ryan pushes too far (Act 2)
2. REVELATION — Frank finds Jake's intimate drawings (Act 3)
3. COMPETING PULL — Brothers discover each other's involvement (Act 4)
4. EXTERNAL THREAT — Mom announces early return (Act 4)

### Tension Curve Summary

```
ARRIVAL → ROUTINE → BATHROOM INCIDENT → BUS DEPENDENCY → MOM'S CALL (bridge) →
  THE MATH → FIRST CHORE → FIRST AWARENESS (exposure_unlock) →
    RYAN'S PUSH ↓↓ (tension — trust breaks) →
      REPAIR → BOOKKEEPING (Frank orbit) → CREEK SWIM → JAKE'S CONFESSION →
        RYAN CATCHES LILY → FIRST FLIRTATION (flirt_unlock) →
          FIRST KISS (kiss_unlock) ↑↑↑↑ →
            FRANK'S LATE NIGHT → RYAN'S ULTIMATUM ↓ →
              POWER OUTAGE (bridge) →
                FRANK FINDS DRAWINGS ↓↓↓ (MAJOR CRISIS) →
                  REPAIR (Frank + Jake separate) → FINANCIAL CRISIS →
                    PHYSICAL ESCALATION (handjob_unlock) ↑↑↑ →
                      BROTHERS DISCOVER ↓↓ (crisis) → FRANK'S OFFER →
                        GLOBAL BRANCH → MOM'S RETURN ↓ →
                          FINAL WEEK → RESOLUTION
```

### Key Emotional Beats (Multi-NPC Adaptation)

| Beat | Event | Lily Feels | Lily Phase | NPCs Feel | NPC Quadrants |
|------|-------|-----------|------------|-----------|---------------|
| Arrival | Opening scene | Displacement, pride, isolation | OUTSIDER | Frank: dutiful. Ryan: interested. Jake: curious. | All DISTANT |
| First Chore | The Math / first clean | Humiliation + determination | OUTSIDER→SETTLING | Frank: respectful. Ryan: teasing. Jake: sympathetic. | Frank SAFE, others DISTANT |
| First Spark | Physical awareness | Excitement + confusion | SETTLING→AWARE | Whoever triggered: first awareness. Others: unchanged. | Triggering NPC: DISTANT→edge |
| Ryan's Push | Truck incident | Fear + anger OR arousal | AWARE | Ryan: testing/hurt. Others: unaware. | Ryan: CONFLICTED briefly |
| First Kiss | Kiss milestone | Desire + guilt + wanting more | AWARE→WANTING | Kissing NPC: terrified + hopeful. Others: sensing shifts. | Kissing NPC: OPEN |
| Frank Finds Drawings | Major crisis | Panic, shame, desperation | WANTING→TORN | Frank: betrayed. Jake: scared. Ryan: sensing opportunity. | Frank: deep CONFLICTED. Jake: CONFLICTED. |
| Recovery | Repair events | Determination + vulnerability | TORN | Frank: testing. Jake: hoping. | Both: CONFLICTED softening |
| Physical Escalation | Handjob milestone | "I chose this" | TORN→COMMITTED | Chosen NPC: amazed/grateful. | OPEN (rebuilt deeper) |
| Brothers Discover | Global crisis | "What have I done?" | COMMITTED (crisis) | Both brothers: hurt/competitive. Frank: calculating. | Brothers: CONFLICTED |
| Mom's Return | Announcement | Terror + urgency + "who am I?" | COMMITTED→ENDGAME | All NPCs: fear response. | All: momentary CONFLICTED |
| Resolution | Mom arrives | Depends on ending | ENDGAME | Depends on ending | Depends on ending |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: CHAPTERS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| ID | Name | Mood | Description | Order |
|----|------|------|-------------|-------|
| `chapter_arrival` | One Suitcase | neutral | Lily arrives at a house she's been to exactly once. Three men she barely knows. Ten weeks. | 1 |
| `chapter_settling` | The New Normal | hopeful | Routines form. The bathroom schedule. The breakfast table. The bus problem. She starts to see them as people. | 2 |
| `chapter_awakening` | Something Shifts | tense | Bodies noticed. Boundaries tested. The math forces choices. She starts making excuses to be where they are. | 3 |
| `chapter_deepening` | Lines in the Sand | romantic | Kisses that shouldn't happen. Offices with locked doors. Sketchbooks full of her. Every line drawn is a line crossed. | 4 |
| `chapter_crisis` | Under the Same Roof | tense | The house fractures. Drawings discovered. Brothers at war. The question isn't who she wants — it's what she's willing to lose. | 5 |
| `chapter_convergence` | The Countdown | passionate | Mom's coming home. Seven days. Maximum intensity. Every touch is both first and last. | 6 |
| `chapter_resolution` | When She Walks Through the Door | peaceful | Diana returns. Lily is... who? The answer depends on sixty days of accumulated choices. | 7 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: STORY NODES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

One node per story event from Phase 4, linked to its canvas and flag.

### Act 1 Nodes

| ID | Name | Chapter | Canvas | Flag | Milestone | Journal Entry |
|----|------|---------|--------|------|-----------|---------------|
| `node_arrival` | Arrival | `chapter_arrival` | `opening_arrival` | `game_started` | true | "One suitcase. One room. Three men I don't know. The house smells like sawdust and coffee. The walls are thin. I can hear the creek from my window. Ten weeks." |
| `node_first_morning` | First Morning | `chapter_arrival` | `story_first_morning` | `first_morning` | false | "@jake walked in on me in the bathroom. Toothbrush in hand, face on fire. He backed out so fast he hit the doorframe. At breakfast he couldn't look at me. His ears were red for an hour." |
| `node_bus_problem` | The Bus Problem | `chapter_settling` | `story_bus_problem` | `bus_problem_discovered` | false | "The bus is forty minutes and two dollars each way. @ryan offered to drive. Fifteen minutes, free. Free. That word sounds different when someone's looking at you like that." |
| `node_moms_call` | Mom's Call | `chapter_settling` | `story_moms_call` | `mom_called` | false | "Mom called. She's fine. The money's late. 'Can you manage?' I told her I'm fine. I'm not fine. $398 in my account and $385 in expenses this month. I'll manage. I always manage." |
| `node_the_math` | The Math | `chapter_settling` | `story_the_math` | `money_crisis_realized` | true | "I asked @frank if I could clean the house for money. Twenty dollars. He looked at me like he understood exactly what it cost me to ask. I hope he doesn't." |
| `node_first_chore` | First Week | `chapter_settling` | `story_the_math` | `first_week_complete` | false | "One week. I know the bathroom schedule. I know how @frank takes his coffee. I know @ryan sleeps past nine. I know @jake draws until midnight because I can hear his pencil through the wall." |

### Act 2 Nodes

| ID | Name | Chapter | Canvas | Flag | Milestone | Journal Entry |
|----|------|---------|--------|------|-----------|---------------|
| `node_first_awareness` | Something Shifts | `chapter_awakening` | `story_first_awareness` | `exposure_unlock` | true | *(Jake variant)*: "He asked me to lower my collar for the light. I did. His pencil stopped. For three seconds he wasn't drawing — he was seeing. I felt it on my skin like a sunburn." *(Ryan variant)*: "Creek water and a sports bra. He didn't look away. For the first time, I didn't want him to." *(Frank variant)*: "I walked out of the shower and he was in the hallway. Two seconds. His eyes on my shoulders. Then gone. But I felt those two seconds all day." |
| `node_ryans_push` | The Truck | `chapter_awakening` | `story_ryans_push` | `truck_incident_complete` | true | *(ryan_resisted)*: "I slapped his hand. He looked surprised. Not angry — surprised. Like nobody's told him no before. Good." *(ryan_allowed)*: "His hand on my knee in the truck. I didn't move it. The road was empty. The silence was loud. When we got home I went straight to my room and sat on the bed with my heart hammering." |
| `node_bookkeeping` | The Office | `chapter_awakening` | `story_bookkeeping_offer` | `bookkeeping_started` | false | "@frank's office smells like leather and old paper. The door closes. It's just us and numbers. Twenty-five dollars a session. The money is good. The proximity is... something else." |
| `node_creek_swim` | The Creek | `chapter_awakening` | `story_creek_swim` | `first_swim` | false | "Cold water, warm skin, no real swimsuit. @jake tried not to stare. @ryan didn't try at all. I crossed my arms over my chest and then stopped. I'm not sure why I stopped." |
| `node_jakes_sketches` | The Sketchbook | `chapter_awakening` | `story_jakes_confession` | `saw_jakes_sketches` | true | "He showed me the pages. My face. My hands. My neck in afternoon light. Page after page. All beautiful. 'I've been drawing you since the second day.' His hands were shaking. Not from fear. From showing me." |
| `node_ryan_catches` | The Door | `chapter_awakening` | `story_ryan_catches_lily` | `ryan_caught_her` | false | "@ryan in the doorway. Me in my underwear. The mirror showed both of us. He grinned. He didn't leave. I could have screamed. I didn't. I finished putting on my shirt while he watched. I don't know why I did that." |
| `node_first_flirtation` | The First Flirt | `chapter_deepening` | `story_first_flirtation` | `flirt_unlock` | true | "I flirted. On purpose. Not accidentally, not ambiguously — deliberately. I watched his face change and I liked it. Something has shifted inside me and I can't shift it back." |
| `node_first_kiss` | The First Kiss | `chapter_deepening` | `story_first_kiss` | `kiss_unlock` | true | *(Jake)*: "Over the sketchbook. Pencils on the floor. 'We shouldn't.' 'I know.' Neither of us stopped." *(Ryan)*: "Truck. Dead-end road. He pulled me in. I let him. His mouth was sure." *(Frank)*: "Kitchen. 2 AM. Coffee going cold. 'This can't happen,' he said. Then he kissed me like a man taking apart his own rules." |

### Act 3 Nodes

| ID | Name | Chapter | Canvas | Flag | Milestone | Journal Entry |
|----|------|---------|--------|------|-----------|---------------|
| `node_franks_late_night` | 2 AM | `chapter_deepening` | `story_franks_late_night` | `frank_kitchen_moment` | false | "Kitchen at 2 AM. Whiskey and silence. He talked about building the house, about his first wife leaving. His hand was four inches from mine on the table. Neither of us closed the gap. Neither of us needed to." |
| `node_ryans_ultimatum` | The Ultimatum | `chapter_crisis` | `story_ryans_ultimatum` | `ryan_leverage` | true | "@ryan knows. About the drawing sessions. About the time I spend in @jake's room. He wants his own arrangement. The worst part: it's not a threat. It's a negotiation." |
| `node_power_outage` | Candlelight | `chapter_deepening` | `story_power_outage` | `power_outage` | false | "Storm killed the power. Candles on the coffee table. For the first time, all four of us in one room without the TV as a shield. @frank told stories. @ryan was quiet. @jake drew by candlelight. I looked at them and saw people. Just people. In a house that's too small and too close and somehow, impossibly, starting to feel like mine." |
| `node_frank_finds` | The Discovery | `chapter_crisis` | `story_frank_finds_drawings` | `frank_found_drawings` | true | "@frank found the drawings. Not the ones @jake showed me — the others. Me in a towel. Me sleeping. His face was stone. 'My son. In my house. Drawing my wife's daughter.' He didn't yell. That was worse." |
| `node_frank_repair` | Workshop Morning | `chapter_crisis` | `story_frank_repair` | `frank_repair_complete` | false | "Found him in the workshop sanding something that didn't need sanding. I didn't make excuses. He didn't turn around. 'I shouldn't have gone through his things.' From @frank, that's an apology. From me, standing there in sawdust at 6 AM — that's one too." |
| `node_jake_repair` | The Door Opens | `chapter_crisis` | `story_jake_repair` | `jake_repair_complete` | false | "Knocked on @jake's door. Red-eyed. 'He saw them.' 'I know.' I sat with him. He cried. I held him. No escalation. No agenda. Just two people scared of what's happening and choosing to be scared together." |
| `node_financial_crisis` | The Bounce | `chapter_crisis` | `story_financial_crisis` | `financial_crisis` | false | "Mom's transfer bounced again. Art supplies overdue. Bus pass expired. Phone bill late. I stared at my bank app and did the math I've been avoiding. The numbers don't care about my pride." |
| `node_escalation` | Crossing the Line | `chapter_deepening` | `story_physical_escalation` | `handjob_unlock` | true | "My hand on him. His breath catching. The sound — raw, surprised, like something breaking open that was always meant to break. I've never held someone like this. I've never wanted to." |

### Act 4 Nodes

| ID | Name | Chapter | Canvas | Flag | Milestone | Journal Entry |
|----|------|---------|--------|------|-----------|---------------|
| `node_brothers_discover` | They Know | `chapter_crisis` | `story_brothers_discover` | `brothers_know` | true | "The hallway. @ryan's face when he saw me leave @jake's room. Not the grin. Something underneath. Hurt. Then @jake in the doorway. Both of them looking at me. At each other. The house held its breath." |
| `node_crisis_choice` | The Choice | `chapter_crisis` | `story_brothers_discover` | `crisis_resolved` | true | *(chose_independent)*: "'It's none of your business.' I said it and meant it. My life. My body. My choices. They both looked at me like they were seeing someone new." *(chose_peacemaker)*: "'Please don't fight. I care about both of you.' It's true. It's also not enough. But it's all I have." *(chose_avoidant)*: "I walked away. Couldn't speak. Couldn't choose. The silence behind me was worse than any argument." |
| `node_franks_offer` | The Arrangement | `chapter_convergence` | `story_franks_offer` | `frank_offer` | true | "@frank's office. Late. No invoices on the desk. 'I know what's been happening. I'm not asking for details. I'll cover everything — bus, art supplies, phone. In exchange, you stay here. With me. Late nights.' He's not my father. He stopped pretending a long time ago." |
| `node_jake_branch` | The Secret Sketches | `chapter_crisis` | `story_jake_secret_sketches` | `jake_sketches_discovered` | true | *(chose_tender_jake)*: "'They're beautiful.' And they are. Every line is devotion. He sees me in ways I don't see myself. I'm not angry. I'm seen." *(chose_possessive_jake)*: "'You've been watching me.' His face crumbles. Then rebuilds into something harder. 'I can't stop.' The sweet boy has teeth I didn't know about." |
| `node_frank_branch` | The Ledger | `chapter_crisis` | `story_franks_secret` | `frank_secret_complete` | true | *(chose_confront_frank)*: "I told him I could help. He fought it — then broke. Let me see everything. The real numbers. Two people against a problem. When he looked at me, it wasn't as Diana's daughter anymore." *(chose_protect_frank)*: "'I didn't see anything.' His eyes. Relief and something else — the weight of sharing a secret you've carried alone. We're conspirators now." |
| `node_moms_return` | The Call | `chapter_convergence` | `story_moms_return` | `mom_returning` | true | "'I'm coming home early!' Mom sounded happy. I felt the floor tilt. Seven days. All of this — the routines, the drawing sessions, the late nights, the truck rides, the arrangement — has an expiration date. When she walks through that door, I become her daughter again. They become her family. And whatever this was... stops." |
| `node_final_week` | Last Days | `chapter_convergence` | `story_final_week` | `endgame_active` | false | "The last week. Everything is louder. @frank's hand on my mug. @jake drawing like he's running out of time. @ryan: 'We should do a hike. All of us. Before she gets here.' The first generous thing he's said about shared time." |
| `node_resolution` | When She Walks Through the Door | `chapter_resolution` | `story_resolution` | `game_complete` | true | *(Ending-dependent — see Section 2.5)* |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2.5: BRANCHING PATHS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Branch Points

| Branch Canvas | Choice A | Flag A | Choice B | Flag B | Shared Flag |
|--------------|----------|--------|----------|--------|-------------|
| `story_ryans_push` | "Slap his hand" | `ryan_resisted` | "Let it stay" | `ryan_allowed` | `truck_incident_complete` |
| `story_jake_secret_sketches` | "They're beautiful" | `chose_tender_jake` | "You've been watching me?" | `chose_possessive_jake` | `jake_sketches_discovered` |
| `story_franks_secret` | "I can help" | `chose_confront_frank` | "I didn't see anything" | `chose_protect_frank` | `frank_secret_complete` |
| `story_brothers_discover` | "None of your business" | `chose_independent` | "Please don't fight" | `chose_peacemaker` | `crisis_resolved` |
| `story_brothers_discover` | *(also)* "(Walk away)" | `chose_avoidant` | | | `crisis_resolved` |

### Ending-Specific Resolution Nodes

| ID | Name | Chapter | Condition | Journal Entry |
|----|------|---------|-----------|---------------|
| `node_ending_jake` | Jake's Girl | `chapter_resolution` | Jake highest stats, corruption < 160 | "Mom hugged me at the door. Over her shoulder, @jake's eyes found mine. His hand reached for mine behind our backs. The sketchbook under his bed is full. This isn't over. This is just the part nobody else gets to see." |
| `node_ending_ryan` | Ryan's Conquest | `chapter_resolution` | Ryan highest, corruption > 150 | "Mom unpacked in the kitchen. @ryan caught my eye across the room. Jingled the truck keys. Mouthed: 'Later.' It's not love. We both know that. But it's honest. And he'll drive me wherever I want." |
| `node_ending_frank` | Frank's Arrangement | `chapter_resolution` | Frank highest, corruption > 180 | "@frank and I don't look at each other when Mom walks in. We don't need to. The arrangement is already in place. Diana will travel again. @frank will be here. So will I. Nothing is said. Everything is understood." |
| `node_ending_all` | All Three | `chapter_resolution` | No NPC >25 ahead | "Five chairs at the dinner table now. I look at each of them. Each looks back. The house is mine in a way Mom will never understand. She came home to a daughter she doesn't quite recognize. She's right not to." |
| `node_ending_independent` | Independence | `chapter_resolution` | confidence > 60, money > 500 | "I hugged Mom. 'I got a job at the diner. I'm going to look for my own place.' She looked surprised. Proud, maybe. I don't need anyone's truck or office or arrangement. I can leave. I might stay — but on my terms." |
| `node_ending_escape` | Escape | `chapter_resolution` | corruption < 100 | "I hugged Mom. Went to my room. Started packing. The dorm repairs are done. I'll be back at campus by next week. Nothing happened here. Almost. I think about @jake's drawing of my hands and wonder if 'almost' counts." |

### Reconvergence

The global crisis branch (chose_independent / chose_peacemaker / chose_avoidant) reconverges at `node_franks_offer`:
- **Reconvergence group**: `group_crisis_resolution` with `required_count = 1`, containing `node_crisis_independent`, `node_crisis_peacemaker`, `node_crisis_avoidant`
- **Shared continuation**: `node_franks_offer` with `requires_group = "group_crisis_resolution"`

The ending branches do NOT reconverge — they are terminal nodes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: GROUPS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Complete N of M" parallel requirements for story progression:

| ID | Name | Required | Members | Purpose |
|----|------|----------|---------|---------|
| `group_settling_in` | Settling In | 3 of 5 | `node_first_morning`, `node_bus_problem`, `node_moms_call`, `node_the_math`, `node_first_chore` | Player must experience at least 3 settling events before Act 2 opens |
| `group_first_awareness` | First Awareness | 1 of 3 | `node_awareness_jake`, `node_awareness_ryan`, `node_awareness_frank` | Any NPC can trigger exposure_unlock |
| `group_first_kiss` | First Kiss | 1 of 3 | `node_kiss_jake`, `node_kiss_ryan`, `node_kiss_frank` | Any NPC can trigger kiss_unlock |
| `group_npc_branches` | NPC Discoveries | 2 of 3 | `node_jake_branch`, `node_frank_branch`, `node_ryans_push` | At least 2 NPC branches must fire before endgame |
| `group_crisis_resolution` | Crisis Resolved | 1 of 3 | `node_crisis_independent`, `node_crisis_peacemaker`, `node_crisis_avoidant` | Global crisis must resolve before Frank's offer |
| `group_ending` | Resolution | 1 of 6 | All ending nodes | One ending fires based on accumulated stats |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: EMOTION MAPPINGS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Player Corruption

| Min | Max | Label | Description |
|-----|-----|-------|-------------|
| 0 | 30 | innocent | "She's the girl who arrived with one suitcase. Uncomfortable with proximity. Notices things and feels guilty for noticing." |
| 31 | 60 | curious | "She's starting to look on purpose. The guilt is fading into something else — curiosity, then anticipation. She picks her outfit with someone in mind." |
| 61 | 100 | awakened | "She wants things she didn't want three weeks ago. She seeks out the encounters she used to stumble into. The morning routine includes makeup now." |
| 101 | 150 | embracing | "She's past pretending. She flirts deliberately, escalates consciously, manages three dynamics with growing skill. The hoodie hasn't left the closet in weeks." |
| 151 | 200 | transformed | "She initiates. She chooses who gets her evening. The girl who arrived with one suitcase would not recognize the woman choosing lingerie at the clothing store." |
| 201 | 250 | consumed | "The house is hers. Three men, one roof, and she's the center of gravity. When Mom walks through that door, the person she meets will be a stranger wearing her daughter's face." |

### Per-NPC Emotion Mappings

#### @jake — Love

| Min | Max | Label | Description | Jake's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 8 | strangers | "She's the new girl in the house. Pretty. Quiet." | Nods at meals. Draws landscapes. Door closed. |
| 9 | 15 | noticing | "Something about her face in the afternoon light." | Draws her without realizing. Saves her a seat. Stutters when she's close. |
| 16 | 22 | drawn | "He can't stop looking. The sketchbook is full of her." | Shows her his art. Pencil shakes. Finds excuses to be where she is. |
| 23 | 30 | devoted | "She's the only thing worth drawing." | Says her name differently. Leaves drawings under her door. Can't eat when she's at the table. |
| 31 | 40 | in love | "He's hers. He knows it. He doesn't want to be anything else." | "I love you." No stutter. No trailing off. Complete. |

#### @jake — Trust

| Min | Max | Label | Description | Jake's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 8 | guarded | "Polite distance. She's a guest." | Sketchbook angled away. Headphones on. Door closed. |
| 9 | 15 | opening | "She likes art. She's kind." | Shows landscapes. Mentions his professor. Leaves door cracked. |
| 16 | 22 | trusting | "She gets it. She gets him." | Tells her about Ryan mocking his art. Draws with door open. Vulnerable. |
| 23 | 30 | safe | "He'd tell her anything." | Falls asleep while she's in the room. Shows the private sketches. Cries in front of her. |
| 31 | 40 | complete | "She's the only person who sees him." | Leaves the sketchbook open. Doesn't flinch when she touches him. "I've never shown anyone." |

#### @ryan — Love

| Min | Max | Label | Description | Ryan's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 5 | testing | "New girl. Interesting. Let's see what happens." | Teases. Offers rides with strings. Looks her over like inventory. |
| 6 | 12 | pursuing | "She's not what he expected." | Cleans the truck cab. Drives slower. Tells real stories instead of jokes. |
| 13 | 18 | invested | "He's thinking about her when she's not around." | Waits for her. Covers for her. Gets quiet when she's close. |
| 19 | 25 | falling | "He's scared of how much he wants this." | Drops the nicknames. Tucks hair behind her ear. Falls asleep near her. |
| 26 | 35 | his | "She's the only thing he's ever wanted that he can't joke about." | "I don't want to go home yet." Protects without performing. Vulnerable. |

#### @ryan — Trust

| Min | Max | Label | Description | Ryan's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 5 | performing | "Everything is a bit. A test." | Watches her like he's keeping score. Jokes deflect everything. |
| 6 | 12 | real | "She saw past the act." | Tells the real scar story. Admits he didn't finish school. |
| 13 | 18 | loyal | "He'd cover for her." | Lies to Frank on her behalf. "She was with me." No questions. |
| 19 | 25 | exposed | "She knows him. The real one." | Admits he's scared. Doesn't put up the front when they're alone. |
| 26 | 35 | hers | "She could destroy him with what she knows." | Falls asleep in the truck with her. Trusts her with his actual feelings. |

#### @frank — Love

| Min | Max | Label | Description | Frank's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 5 | dutiful | "Diana's daughter. A responsibility." | Nods. Pours coffee. Reads the paper. She's a guest he's tolerating. |
| 6 | 12 | aware | "Something about her he can't name." | Remembers how she takes her coffee. Watches her leave a room. |
| 13 | 20 | fighting | "He knows exactly what he's feeling and he's horrified." | Eyes track her. Leaves the room when she enters. Pours whiskey earlier. |
| 21 | 28 | breaking | "The dam is cracking." | Holds eye contact. Says her name softer. Hand on the small of her back. |
| 29 | 35 | his | "He's done fighting. She's his." | "Stay." One word. "Lil." The door locks. He stops pretending. |

#### @frank — Trust

| Min | Max | Label | Description | Frank's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 8 | professional | "She works for him. That's the relationship." | Office door open. Checks her work. Counts the drawer. |
| 9 | 15 | respect | "She's reliable." | Stops checking work. Tells her about late-paying clients. |
| 16 | 22 | inner circle | "She's inside the walls." | Door closes. Shares real numbers. Business talk. "Don't tell Diana." |
| 23 | 28 | partner | "He needs her." | Asks her opinion on bids. Leaves her alone with the checkbook. |
| 29 | 35 | absolute | "She could destroy him and he's given her every tool." | Falls asleep in the office while she works. The most vulnerable thing Frank has ever done. |

### Cross-State Descriptions (Per NPC)

#### @jake Cross-States

| Love | Trust | Quadrant | Description |
|------|-------|----------|-------------|
| 0-8 | 0-8 | DISTANT | "He's the quiet one at meals. You share a wall and nothing else." |
| 0-8 | 9-15 | SAFE | "He's a friend. He shares his art. No charge in the air." |
| 9-22 | 0-8 | CONFLICTED | "He watches you when you're not looking. The sketchbook is full of you. But the door stays closed." |
| 9-22 | 9-15 | WARMING | "Drawing sessions get longer. His hand lingers positioning your chin. Something is building." |
| 16-30 | 8-15 | CRISIS | "He loves you. You can see it in every line he draws. But something broke — the drawings, the discovery, what you did — and he won't let you close until it heals." |
| 16-30 | 16-30 | OPEN | "Art is foreplay. Every pose is charged. He draws you like a prayer." |
| 23-40 | 23-40 | DEEP OPEN | "He's yours. The sketchbook is open. His door is open. His heart is open. 'I drew you again. I always draw you.'" |

#### @ryan Cross-States

| Love | Trust | Quadrant | Description |
|------|-------|----------|-------------|
| 0-5 | 0-5 | DISTANT | "He's the loud one. Tests every boundary. You're entertainment." |
| 0-5 | 6-12 | SAFE | "He's calmed down. Tells real stories. Drives you without commentary." |
| 6-18 | 0-5 | CONFLICTED | "He wants you and he's angry about it. Jealous. Competitive. The grin is gone." |
| 6-18 | 6-12 | WARMING | "Truck rides get longer. He cleaned the seat for you. Something's shifting." |
| 13-25 | 6-12 | CRISIS | "He found out. About Jake. About Frank. The hurt is underneath the anger. 'Both of us? Really?'" |
| 13-25 | 13-25 | OPEN | "The bravado drops. He's quiet. His hand finds the small of your back. 'I don't want to go home yet.'" |
| 19-35 | 19-35 | DEEP OPEN | "He's done performing. Protects you without making it a joke. Falls asleep in the truck. Trusts you with everything he pretends not to feel." |

#### @frank Cross-States

| Love | Trust | Quadrant | Description |
|------|-------|----------|-------------|
| 0-5 | 0-8 | DISTANT | "He's the authority. Professional. 'Dinner's at six.'" |
| 0-5 | 9-15 | SAFE | "He trusts your work. Business talk. No charge." |
| 6-20 | 0-8 | CONFLICTED | "He wants you and he's fighting it with everything he has. Leaves the room. Pours whiskey. 'Diana trusts me.'" |
| 6-20 | 9-15 | WARMING | "The office door closes. His hand on the back of your chair. He smells like sawdust and restraint." |
| 13-28 | 8-15 | CRISIS | "He found the drawings. He knows what's happening under his roof. The control is brittle. 'This stops. Whatever this is.'" |
| 13-28 | 16-28 | OPEN | "2 AM kitchen. Whiskey. His hand four inches from yours. He stops fighting. 'Stay.'" |
| 21-35 | 22-35 | DEEP OPEN | "'Lil.' The dam broke. His voice is low. His door is unlocked. He's done being appropriate." |

### Emotional Transition Moments (Per NPC)

#### @jake Transitions

| Transition | The Moment | Sample Line |
|-----------|-----------|-------------|
| DISTANT → SAFE | First time he shares his art with her | "What do you think of the composition?" (He's never asked anyone.) |
| SAFE → WARMING | First charged look during a drawing session | He stops drawing. Just looks. His pencil hangs in the air. |
| WARMING → OPEN | First time he says what he's feeling | "I keep drawing you. I can't draw anything else." |
| OPEN → CONFLICTED | After Frank finds the sketches / after discovering she's with Ryan | "You knew. About the other drawings. You knew and you let me keep—" Silence. Door closes. |
| CONFLICTED → OPEN | After repair — she comes to his room | He slides a drawing under her door. Her coffee mug. A detail only someone who watches her would notice. "I drew something for you." |

#### @ryan Transitions

| Transition | The Moment | Sample Line |
|-----------|-----------|-------------|
| DISTANT → SAFE | First time the teasing stops and something real shows | "The scar? I was eighteen and scared. Dad drove me to the ER without a word." |
| SAFE → WARMING | First time he cleans the truck for her | She notices the seat is wiped down. He doesn't mention it. |
| WARMING → OPEN | First time he admits he's invested | "I don't want to go home yet." (Said quietly. No grin.) |
| OPEN → CONFLICTED | Brothers discover each other | "Both of us? Really?" The hurt is under the anger. |
| CONFLICTED → OPEN | He shows up with something — gas station coffee, art supplies | "Heading to town. You coming or what?" The offer IS the apology. |

#### @frank Transitions

| Transition | The Moment | Sample Line |
|-----------|-----------|-------------|
| DISTANT → SAFE | First time he asks about her life | "Classes going alright?" (He's never asked. This is new.) |
| SAFE → WARMING | First time the control slips — an unfinished sentence | "You should—" (pause) "Never mind." His coffee mug tightens. |
| WARMING → OPEN | 2 AM kitchen. He doesn't leave when she enters. | "Sit down." Two words. An opening. |
| OPEN → CONFLICTED | He finds the drawings / discovers the arrangement with his sons | "This stops." Voice tight. Hands flat on the desk. Not anger. Discipline. |
| CONFLICTED → OPEN | She finds him in the workshop. Doesn't make excuses. | "I shouldn't have gone through his things." From Frank, that's vulnerability. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: GUIDANCE HINTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hints are phrased as Lily's internal observations — never game-mechanical language.

### General Progression Hints

| Condition | Hint Text |
|-----------|-----------|
| corruption < 25, days > 5 | "I've been keeping my head down. Maybe I should pay more attention to what's happening around this house." |
| `chores_started` not set, days > 4 | "I'm running out of money. Maybe I should offer to help around the house." |
| `town_access` not set, days > 3 | "I need to get to town. @ryan has that truck..." |
| `exposure_unlock` not set, corruption >= 20 | "Something's different about how they look at me. Or maybe it's how I look at them." |
| `bookkeeping_started` not set, corruption >= 40 | "@frank mentioned needing help with the books. The pay is better than cleaning..." |
| `drawing_started` not set, jake_love >= 8 | "@jake asked if I'd sit for him. Something about the light." |

### Per-NPC Hints

| Condition | Hint Text |
|-----------|-----------|
| jake_love < 10, days > 10 | "@jake draws all day in his room. I bet he'd show me if I asked." |
| jake_love >= 15, `kiss_unlock` not set | "The way @jake looks at me when we're alone... I wonder what happens if I stop pulling away." |
| ryan_love < 5, days > 7 | "@ryan offered to drive me again. The truck rides are awkward. Maybe they don't have to be." |
| ryan_corruption >= 15, `flirt_unlock` not set | "@ryan's been different since the truck. More careful. I could push that... or not." |
| frank_trust < 8, days > 10 | "@frank is always in his office. Maybe helping with the books would bring us closer." |
| frank_love >= 15, `kiss_unlock` not set | "The kitchen at 2 AM. @frank's whiskey. The silence between us. I keep going back." |

### Economic Hints

| Condition | Hint Text |
|-----------|-----------|
| money < 50 | "I'm almost broke. I need to find more work — or find someone willing to pay more for... different services." |
| money < 0 | "I can't afford the bus. I can't afford art supplies. Something has to give." |
| `bus_pass` expired | "No bus pass. I'm stuck at the property unless @ryan drives me. That's a lot of leverage to hand someone." |

### Endgame Hints

| Condition | Hint Text |
|-----------|-----------|
| `mom_returning` set | "Seven days. Everything I've built here has an expiration date. What do I want the last week to look like?" |
| `endgame_active`, confidence > 60, money > 400 | "I have my own money. My own job. I could leave when Mom gets here. The question is whether I want to." |
| `endgame_active`, corruption > 200 | "When Mom walks through that door, she's going to see someone new. The question isn't whether I've changed. It's whether I like who I've become." |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 6 complete. All 6 book phases are now written.
Type "proceed" to compile the final book, or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━