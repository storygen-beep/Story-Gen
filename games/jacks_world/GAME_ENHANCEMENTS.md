# Jack's World — Game Enhancement Proposals

## Current State Summary

The game has strong writing, good video integration, and a clear progression chain. But gameplay is too linear — stats only go up, choices don't matter, Angela has no agency, and the player can't fail. The physical escalation **is** the game, with no underlying drama, risk, or meaningful decision-making.

**Current progression chain:**
```
arrive → bills → job → routine → rent → late_night_talk → towel → massage_offer → bedroom (oral → sex) → date_night → exploring_kink
```

Every link in this chain is guaranteed. The player just needs to show up.

---

## Enhancement Categories

### A. Consequence System (Risk & Setbacks)

#### A1. Peek Risk — Getting Caught
**What**: Bath peek and morning peek have a chance of Angela catching Jack. If caught, trust drops and a cooldown period applies.
**How**: Add a "caught" node to each peek canvas with trust penalty (-3 to -5). Use a `peek_caught_count` trait or flag. After being caught, Angela could reference it in dialogue ("You need to knock, Jack"). Could gate further peeking behind a trust recovery threshold.
**Impact**: Transforms passive observation into risk/reward gameplay. The player must weigh "do I peek and risk trust loss, or skip it?"

#### A2. Missed Rent Consequences
**What**: If the player doesn't pay rent within the weekly window, Angela's trust drops and a confrontation scene triggers.
**How**: Add a repeatable "rent_overdue" canvas that fires when `days_since_flag rent_last_paid >= 10` (3 days grace). Trust -3, plus a dialogue scene where Angela is hurt/disappointed. Multiple missed rents could stack consequences.
**Impact**: Makes the economic system meaningful. Work vs. Angela-time becomes a real trade-off.

#### A3. Pushing Too Fast — Rejection
**What**: If the player picks an escalation choice and love/trust is borderline (within 5 points of threshold), Angela sometimes pulls back instead of accepting.
**How**: This would need engine-level support (random chance or "soft threshold" system). Alternatively, add intermediate "hesitation" nodes where Angela says "not yet" if the player pushes — this could work with existing condition ranges. E.g., a "kiss her" choice at love 42 shows a warm response, but the same choice could have a second version at love 35-41 that shows Angela pulling away.
**Impact**: The player can't just click the highest option every time. Creates a sense that Angela is a person with boundaries.

#### A4. Cooldown After Major Events
**What**: After towel encounter, bedroom encounter, or other milestone events, add a 1-2 day cooldown where Angela is distant or processing. Some activities become temporarily unavailable or have modified text.
**How**: Use `days_since_flag` conditions on activities. E.g., for 2 days after `towel_encounter_complete`, Angela's breakfast dialogue changes to something awkward/distant. Some evening activities could require `days_since_flag towel_encounter_complete >= 2`.
**Impact**: Creates push-pull dynamics. Big moments have emotional aftermath instead of immediate escalation.

---

### B. Angela's Agency (She's a Person, Not a Meter)

#### B1. Angela's Bad Days
**What**: Random or scheduled events where Angela is stressed, upset, or unavailable. She comes home late, has a headache, gets a call that upsets her. The player must respond with care rather than pursuing intimacy.
**How**: Add 3-4 one-time canvases gated by love/trust ranges (not flags). E.g., "Angela's Bad Day" fires at love 25-40, kitchen, evening. She's upset about work/money/loneliness. Player choices: comfort her (trust+3), give her space (trust+1), or try to escalate (trust-2, love-1).
**Impact**: Angela becomes three-dimensional. The player learns that the relationship requires empathy, not just showing up.

#### B2. Angela Pulls Away
**What**: After the bedroom encounter (a huge escalation), Angela has a moment of doubt. She avoids Jack for a day. A one-time canvas where she says "I don't know if this is right" or "What are we doing?"
**How**: One-time canvas triggered by `bedroom_encounter_complete`, fires 2-3 days after. Angela is in the kitchen, avoids eye contact. Player choices matter here: "I care about you" (love+2, trust+2), "We can slow down" (trust+4), "I want more" (love+1, trust-2).
**Impact**: This is the emotional climax the game is missing. The forbidden question finally gets asked. The player's response shapes the relationship going forward.

#### B3. Angela Initiates (Sometimes)
**What**: At high love/trust, Angela occasionally comes to Jack instead of waiting to be found. She knocks on his door, suggests going for a walk, or sends a text asking him to come to the kitchen.
**How**: Add canvases triggered at Jack's bedroom that require Angela-related conditions. E.g., "Angela at Your Door" fires at love≥60 — she shows up with wine and wants to talk. Makes the relationship feel mutual.
**Impact**: The relationship feels two-sided instead of Jack always pursuing.

#### B4. Angela's Social Life
**What**: Angela occasionally has plans. She goes out with a friend, mentions a phone call, has dinner with someone from work. Jack can't always access her.
**How**: Add occasional schedule gaps or "Angela is out" canvases. When the player goes to a location expecting Angela, she's not there. Optional: the player can ask about her evening the next morning (trust builder).
**Impact**: Angela has a life beyond Jack. The player can't take her availability for granted.

---

### C. Meaningful Choices (Decisions That Matter)

#### C1. Branching Story Events
**What**: Key one-time events should have choices that lead to genuinely different outcomes — different flags set, different stat changes, different follow-up events.
**How**: Examples:
- **The Bills**: "Offer rent help" sets a `rent_promised` flag that makes first_rent_day trigger sooner but with higher pressure. "Offer empathy" sets `emotional_support` flag that unlocks a unique conversation later.
- **First Rent**: "Counter" path (distant but respectful) vs "handoff" path (intimate) could gate different mid-game dialogue variants.
- **Late Night Kitchen**: Add a third choice — "Open up about yourself" — that sets a unique flag and unlocks Jack-focused dialogue later.
**Impact**: The player's personality emerges through choices. Different playthroughs feel different.

#### C2. Mutually Exclusive Activities
**What**: Some time slots should force the player to choose between activities that can't both be done. Not just "breakfast OR work" but emotionally different options.
**How**: E.g., on certain evenings, the player can either do movie night with Angela OR go to the cafe to pick up an extra shift. Choosing work means missing a potential Angela scene, but earning money for rent/date. Add a "work late" canvas at the cafe for evenings.
**Impact**: Real opportunity cost. Time becomes a resource to manage.

#### C3. Trust vs. Love Trade-offs
**What**: Some choices should increase one stat while decreasing or not increasing the other. Currently every choice is a win-win.
**How**: Examples:
- Peeking: love+2 but trust-1 (if she had known...)
- Pushing physical: love+2 but trust+0 (she enjoyed it, but something feels rushed)
- Emotional honesty: trust+3 but love+0 (you connected, but the mood wasn't romantic)
- Being bold: love+3 but trust-1 (exciting, but she's not sure she's comfortable)
**Impact**: The player must think about what kind of relationship they're building.

---

### D. Economic Depth (Money Matters)

#### D1. Tighter Economy
**What**: Make money harder to earn and easier to spend. Rent is a real burden.
**How**:
- Reduce cafe pay from $70 to $45-50 per shift
- Add random expenses: "Your phone broke" ($80), "Need new clothes for the cafe" ($60)
- Rent increases over time: $200 week 1, $200 week 2, then Angela mentions it should be $250
- Add optional gifts: flowers ($30, love+2), wine ($25, trust+1), cook dinner ($15, love+1 trust+1)
**Impact**: Money becomes a real constraint. Working more means seeing Angela less. Gifts become meaningful investments.

#### D2. Gift System
**What**: Let the player spend money on Angela for stat boosts. Creates a reason to work beyond rent.
**How**: Add a "shop" canvas at the street or cafe. Items: flowers, wine, book, candle, jewelry. Each gives different love/trust boosts. Some gifts could unlock unique Angela dialogue.
**Impact**: Another dimension of gameplay. Money → gifts → relationship progress.

#### D3. Rent Forgiveness Arc
**What**: At high trust, Angela tells Jack to stop paying rent. But this creates guilt/dependency tension.
**How**: One-time canvas at trust≥35. Angela says "You don't have to keep paying. I'd rather have you here than your money." Player choice: keep paying (trust+2, maintains independence) or accept (saves money, but adds a `rent_forgiven` flag that changes some Angela dialogue to hint at power imbalance).
**Impact**: Adds nuance to the economic relationship. Tests whether the player values independence or comfort.

---

### E. Narrative Depth (Story Beyond the Apartment)

#### E1. The Forbidden Question
**What**: A recurring theme where both characters wrestle with "what is this?" — not just once, but at multiple relationship stages.
**How**: Add 3-4 one-time canvases at different love thresholds:
- **love ~25**: Jack's internal monologue while lying in bed. "She's my step-mom. This isn't..."
- **love ~45**: Angela makes a comment at dinner. "If anyone asked, I'd say you're my tenant." The subtext is heavy.
- **love ~65**: After the bedroom encounter. A morning-after conversation. "We can't tell anyone about this. You know that, right?"
- **love ~85**: Full confrontation. "I love you. I know I shouldn't, and I don't care."
**Impact**: The taboo element becomes a narrative arc instead of invisible set dressing. Creates genuine emotional tension.

#### E2. Maria as a Character
**What**: Expand the cafe owner from a prop to a real character. She notices things. She asks questions. She becomes a confidante or a threat.
**How**:
- Maria comments on Jack looking tired/happy after certain milestones
- Maria asks "How's Angela?" with a knowing look
- At high love levels, Maria says something like "Be careful with her, kid. She's been hurt before."
- Optional: Maria could be a friend of Angela's, creating tension about discovery
**Impact**: The outside world notices. The relationship has witnesses. Stakes feel higher.

#### E3. Jack's Internal Arc
**What**: Jack is currently a blank vessel. Give him moments of self-reflection, doubt, and growth.
**How**: Add canvases in Jack's bedroom that trigger at milestone flags. Pure text, internal monologue:
- After the bills: "She's been doing this alone. I want to help."
- After the towel: "I can't stop thinking about it. About her."
- After the bedroom: "What am I doing? She's... but she looked at me like..."
- After date night: "I'm in love with my step-mom. And it's the most real thing I've ever felt."
**Impact**: The player character has interiority. The story has a protagonist, not just a camera.

#### E4. Day Counter / Endpoint
**What**: The game should have a finite timeline. 30 days, as described in the project description. After day 30, a resolution scene based on relationship state.
**How**: Add a day counter. At day 25, trigger a "5 days left" warning. At day 30, trigger an ending canvas with branches based on love/trust level and flags achieved:
- Low love (<30): Jack moves out. Polite goodbye.
- Medium love (30-60): Bittersweet farewell. "Maybe in another life."
- High love (60-80): They confess feelings but Jack still leaves. Open ending.
- Very high love (80+): Jack stays. They choose each other.
- Plus `date_night_complete` variant: They make plans for the future.
**Impact**: Time pressure creates urgency. Every day matters. The player can't grind forever.

---

### F. Activity Variety (Not All Stats Are Equal)

#### F1. Trust-Only Activities
**What**: Add activities that build trust without love. Currently everything builds both, making them functionally one stat.
**How**:
- Cooking dinner for Angela (kitchen, evening, text-only): trust+2, love+0
- Helping with chores (hallway/kitchen, afternoon): trust+1
- Listening when she's stressed (requires "bad day" events): trust+3
**Impact**: Trust becomes a distinct resource that requires different behavior than love.

#### F2. Negative-Outcome Activities
**What**: Some activities should sometimes go wrong.
**How**:
- Burned breakfast: attempted cooking → "The smoke alarm goes off. Angela laughs." love+1, but no trust.
- Awkward movie choice: player picks something with a sex scene → uncomfortable silence. love+0, trust-1, but also funny follow-up dialogue.
- Bad work day: cafe shift variant where tips are bad ($40 instead of $70).
**Impact**: Not everything is smooth. Failure makes success feel earned.

#### F3. Deep Conversation Expansion
**What**: The single deep conversation canvas is one of the strongest gameplay elements (highest stats, meaningful choices). There should be more.
**How**: Add 4-5 topic-specific conversation canvases that unlock at different points:
- "The Divorce" (trust≥15): Angela talks about Jack's father
- "Her Dreams" (trust≥25): What she wanted before the marriage
- "The Age Thing" (love≥40): She acknowledges the elephant in the room
- "His Future" (trust≥30): Angela asks what Jack wants from life
- "Us" (love≥70): The "define the relationship" talk
Each with 3 choices that have meaningfully different outcomes.
**Impact**: Emotional depth. The relationship is built through words, not just proximity.

---

## Implementation Priority

### High Impact, Lower Effort
1. **E1 — The Forbidden Question** (3-4 text canvases, no videos needed)
2. **E3 — Jack's Internal Arc** (3-4 text canvases in Jack's bedroom)
3. **B2 — Angela Pulls Away** (1 canvas, critical for narrative)
4. **A4 — Cooldown After Major Events** (condition changes only)
5. **F3 — Deep Conversation Expansion** (text canvases, high gameplay value)

### High Impact, Medium Effort
6. **A1 — Peek Risk** (add caught nodes + trust penalties to existing canvases)
7. **A2 — Missed Rent** (1 new canvas + condition logic)
8. **B1 — Angela's Bad Days** (2-3 new canvases)
9. **C3 — Trust vs Love Trade-offs** (rebalance existing stat rewards)
10. **D1 — Tighter Economy** (number adjustments + expense events)

### High Impact, Higher Effort
11. **E4 — Day Counter / Endpoint** (needs engine support for day limit + ending canvases)
12. **C1 — Branching Story Events** (rewrite existing canvases with real branches)
13. **E2 — Maria as Character** (new NPC with canvases at cafe)
14. **D2 — Gift System** (new shop mechanic + canvases)
15. **B3 — Angela Initiates** (new canvases at Jack's bedroom)

### Nice to Have
16. **C2 — Mutually Exclusive Activities** (schedule conflicts)
17. **B4 — Angela's Social Life** (availability gaps)
18. **F1 — Trust-Only Activities** (new canvases)
19. **F2 — Negative-Outcome Activities** (variant nodes)
20. **D3 — Rent Forgiveness Arc** (late-game economic event)
21. **A3 — Pushing Too Fast** (needs engine support or creative workaround)

---

## Notes

- All enhancements can be implemented as TOML canvas changes — no engine code changes needed unless noted
- Items marked "needs engine support" may require changes to `v1.py` generator or SugarCube runtime
- Enhancements are designed to be additive — they layer onto the existing game without removing content
- The first 5 items (text-only canvases) can be implemented immediately with no video sourcing needed
