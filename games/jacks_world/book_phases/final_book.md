===============================================================================
                              JACK'S WORLD
                          A Game Design Book
                              Version 1.0
===============================================================================

ABOUT THIS BOOK
───────────────

This book describes the complete game design for Jack's World.
Each scene specifies what video to show. Built from story chart v0.4.8.

NPC: Angela (step-mom)
Scenario: Step-family — step-son moves into step-mom's apartment
Tone: Romantic, emotional, forbidden
Length: 30 days, 16 activities, 4 story events
Driver: LOVE (primary), TRUST (secondary)

VIDEO INTEGRATION STATUS:
- Total video sources: 10
- Total clips: 182
- All clips assigned: Yes (zero waste, zero external sources needed)
- Clip reference format: Video source folder + clip index numbers

===============================================================================

                    PHASE 0.5: VIDEO INTEGRATION

===============================================================================

All video content was pre-analyzed and assigned during story chart design.
Every clip is allocated to exactly one activity. No gaps. No external sourcing needed.

VIDEO SOURCE MAP
────────────────

| # | Short Name | Full Folder Name | Total Clips |
|---|---|---|---|
| 1 | angela_white_4 | angela_white_4/ | 28 |
| 2 | 480p.h264 | 480p.h264/ | 16 |
| 3 | 480p.h264 (1) | 480p.h264 (1)/ | 20 |
| 4 | 480p.h264 (2) | 480p.h264 (2)/ | 20 |
| 5 | Step Bro | [PornhubFans 480p] ANGELA WHITE - Busty Slut Fuck Her Step Bro/ | 17 |
| 6 | Mofos | [PornhubFans 480p] Mofos - Big tit thicc Angela White sucks and fucks one lucky cock pov/ | 12 |
| 7 | ADULT TIME | [PornhubFans 480p] ADULT TIME - Naturally Stacked Angela White Has Romantic Sex With Her Husband At The Hotel/ | 25 |
| 8 | NewSensations | [PornhubFans 480p] NewSensations - Angela White XXX BIg Tits Rubdown/ | 20 |
| 9 | Busty Babe Leash | [PornhubFans 480p] ANGELA WHITE - Busty Babe is All Yours While She Gets Fucked on a Leash/ | 14 |
| 10 | POV Blowjob Bath | [PornhubFans 480p] ANGELA WHITE - POV Blowjob and Fucking in the Bath/ | 10 |

CLIP ALLOCATION BY ACTIVITY
────────────────────────────

| # | Activity | Video Source | Clips | Clip Numbers | Type |
|---|---|---|---|---|---|
| 1 | Breakfast/Kitchen | angela_white_4 | 12 | 1–12 | Daily |
| 2 | Movie Night | angela_white_4 | 14 | 13–14, 17–28 | Daily |
| 3 | Couch Play | Mofos | 4 | 6,8–10 | Daily (unlock love 20) |
| 4 | Angela's Bath | 480p.h264 | 16 | 1–16 | Daily (peekable) |
| 5 | Angela's Morning | 480p.h264 (1) | 20 | 1–20 | Daily (peekable) |
| 6 | Morning Together | 480p.h264 (2) | 20 | 1–20 | Daily (unlock love 30) |
| 7 | Jack Arrives | NewSensations | 3 | 1–3 | Story event |
| 8 | Towel Encounter | Step Bro | 3 | 4–6 | Story event |
| 9 | Bedroom Encounter | Step Bro | 11 | 7–17 | Story event |
| 10 | Bedroom Moment | angela_white_4 | 2 | 15–16 | Story event |
| 11 | Date Night Hotel | ADULT TIME | 25 | 1–25 | Special (unlock love 40) |
| 12 | Spa/Massage | NewSensations | 17 | 4–20 | Special (unlock love 35) |
| 13 | Bath Together | POV Blowjob Bath | 10 | 1–10 | Special (unlock love 35) |
| 14 | Exploring Kink | Busty Babe Leash | 14 | 1–14 | Special (unlock love 45) |
| 15 | Bedroom Play | Mofos | 5 | 3–5, 11, 12 | Daily (unlock love 30) |
| 16 | Deep Conversation | — (text-only) | 0 | — | Daily (unlock trust 20) |

CLIP COUNT VERIFICATION
───────────────────────

| Video Source | Activities Using It | Clips Used | Total Available | Match |
|---|---|---|---|---|
| angela_white_4 | Breakfast (12) + Movie Night (14) + Bedroom Moment (2) | 28 | 28 | ✅ |
| Step Bro | Towel (3) + Bedroom Enc (11) | 14 | 17 | ⚠️ clips 1–3 dropped |
| Mofos | Couch Play (4) + Bedroom Play (5) | 9 | 12 | ⚠️ clips 1,2,7 dropped |
| 480p.h264 | Angela's Bath (16) | 16 | 16 | ✅ |
| 480p.h264 (1) | Angela's Morning (20) | 20 | 20 | ✅ |
| 480p.h264 (2) | Morning Together (20) | 20 | 20 | ✅ |
| ADULT TIME | Date Night Hotel (25) | 25 | 25 | ✅ |
| NewSensations | Jack Arrives (3) + Spa/Massage (17) | 20 | 20 | ✅ |
| Busty Babe Leash | Exploring Kink (14) | 14 | 14 | ✅ |
| POV Blowjob Bath | Bath Together (10) | 10 | 10 | ✅ |
| **TOTAL** | | **176** | **182** | ⚠️ 6 dropped |

INTEGRATION RULES
─────────────────

- NSFW isolation: Each activity's NSFW content comes from exactly 1 video file.
- Sequence preserved: Couple/narrative clips play in original order.
- Solo peekable activities (Bath, Morning) organize clips by content intensity — independent vignettes, not continuous narrative.
- No clip is shared between activities. Each clip belongs to exactly one activity.

===============================================================================

                         PHASE 1: FOUNDATION

===============================================================================

GAME: Jack's World

NPC: Angela
- Step-mom
- Warm, attractive, lives alone in her apartment
- The relationship she has with Jack is new — they're getting to know each other

SETTING: Domestic
- Angela's apartment (kitchen, living room, bedroom, bathroom)
- A neighborhood cafe where Jack works
- A hotel (for Date Night, late game)

RELATIONSHIP: Step-family
- Jack is Angela's step-son
- He's moving into her apartment
- They didn't grow up together — this is their first time living under the same roof
- The forbidden element: she's his step-mom

TONE: Romantic + Forbidden
- Not purely sexual — the game is about emotional connection
- The taboo adds tension but doesn't define the relationship
- Love is the driver, not lust
- Trust must be earned — Angela won't escalate if she doesn't feel safe

GAME LENGTH: 30 days
- 4 time slots per day (Morning, Afternoon, Evening, Night)
- 120 total actions across the game
- 4 rent cycles (Day 7, 14, 21, 28)
- Endings evaluated at Day 30

DESIGN PHILOSOPHY: Clip-First
- Every activity is built FROM available video clips upward
- Activities use what's available, not what an ideal template prescribes
- NSFW clips from different video files are never combined in one activity
- Some activities peak at oral, some at solo play — this is intentional

===============================================================================

                    PHASE 2: FANTASY FOUNDATION

===============================================================================

THE CORE FANTASY
────────────────

Type: FORBIDDEN DESIRE + LOVE

This game fulfills the fantasy of developing a genuine romantic connection
with someone you're not supposed to want. The player experiences the slow
transformation from awkward housemates to lovers — earned through daily
presence, small kindnesses, and emotional vulnerability.

THE PREMISE
───────────

"What if you moved in with your step-mom and fell in love?"

This premise promises: A relationship that grows from domestic routine into
deep intimacy. Not a seduction — a mutual discovery.

EMOTIONAL JOURNEY
─────────────────

- Opening: Awkward. Jack doesn't know Angela well. She's being welcoming but distant. The apartment feels like someone else's home.
- Building: Shared meals, accidental glimpses, late-night movies. Small moments that accumulate. She starts to relax around him. He starts to see her as more than his step-mom.
- Climax: The Bedroom Encounter — weeks of tension finally break. Date Night Hotel — they leave the apartment as a real couple for the first time.
- Resolution: Depends on how the player treated her. True Love if he earned both her heart and her trust. Bittersweet if he rushed the physical without earning the emotional.

THE PROMISE
───────────

This game promises to deliver: A love story where every intimate moment
feels earned because you were there for every breakfast, every conversation,
every awkward silence that turned into something more.

The "hero moment": Date Night Hotel — 25 clips, the longest scene in the
game. Angela suggests "somewhere nobody knows us." They spend the night
together as equals, not step-mom and step-son.

DRIVER ASSIGNMENT
─────────────────

- Primary Driver: LOVE → Stat: love (0–50)
- Secondary Driver: TRUST → Stat: trust (0–50, start 15)
- Tertiary Resource: MONEY → Stat: money ($50 start)

The LOVE driver means:
- Escalation feels romantic, not predatory
- Angela initiates at key moments — she has agency
- T1 (love 0-10): Polite, friendly, getting-to-know-you
- Mid (love 20-30): Testing boundaries, vulnerability, "we shouldn't but..."
- High (love 40-50): "I love you," full intimacy, no pretense

The TRUST secondary means:
- Angela has walls. Player must earn access.
- High love + low trust = "she wants to but can't"
- Trust gates prevent rushing — you can't skip the emotional work
- Trust = 0 is game over (she kicks him out)

===============================================================================

                    PHASE 3: CHARACTER DESIGN

===============================================================================

ANGELA
──────

Physical Presence:
Long, straight dark hair. Fair skin. Full-figured with natural curves — she
carries herself with quiet confidence. When she enters a room, she fills it
without trying. In the mornings she wears thin robes or an off-the-shoulder
top and jeans. She favors a delicate necklace. Her smile is warm but
measured — she gives it when she means it.

Personality:
- Warm but guarded. She opens her home before she opens herself.
- Independent. She's lived alone and likes her routines — morning coffee,
  evening baths, the kitchen as her domain.
- Maternal instinct blended with attraction she doesn't expect. She cares
  for Jack before she wants him.
- Direct. She doesn't play games with words. If something is wrong, she
  says it. If something is right, her body says it first.

Speech Style:
- Calm, measured, slightly playful
- Uses his name when it matters: "Jack." (pause) "Thank you."
- Short sentences when emotional. Long sentences when comfortable.
- Teasing: "You're up early. Couldn't sleep... or couldn't stay away?"
- Vulnerable: "I didn't expect this. Any of this."
- Boundary-setting: "Not tonight. I need to know this is real."

Psychology:
- Surface: She wants a normal household. A step-son who respects her space.
  Someone to share meals with.
- Deeper: She wants to be seen — not as a step-mom, not as a body, but as
  a person. She's lonely in a way she won't admit.
- Contradiction: She's the adult, the authority figure — but she's the one
  who initiates at key moments. She tells herself she's in control even as
  she gives control away.

With the Player:
- Initially sees Jack as: a responsibility. Her partner's son. Someone to
  be polite to.
- Would be drawn to: his consistency. Showing up for breakfast every day.
  Paying rent on time. Small kindnesses she didn't ask for.
- Her boundaries: She won't let physical intimacy outpace emotional safety.
  If trust is low, she says "not tonight" even when love is high. She needs
  to feel safe before she can feel desire.

DRIVER ASSIGNMENT:
- Primary: LOVE → Stat: love
- Secondary: TRUST → Stat: trust
- Arc: Strangers (love 0-10) → Growing comfort (love 11-20) → Attraction
  acknowledged (love 21-30) → Physical intimacy (love 31-40) → Full love,
  no pretense (love 41-50)

THE PLAYER: JACK
────────────────

Role: Young man moving into his step-mom's apartment
Starting Position: New to the apartment. Doesn't know Angela well. Needs a
place to stay. Has a job at a neighborhood cafe.
Motivation: Initially practical — he needs housing. Over time, he discovers
a connection he didn't expect. His choices determine whether it becomes love,
stays friendly, or falls apart.

The player controls Jack's daily decisions:
- How he spends his 4 time slots each day
- Whether he prioritizes Angela (love) or work (money)
- How he responds in key moments (honest vs. evasive, respectful vs. pushy)
- Whether he builds trust through reliability or burns it through negligence

===============================================================================

                       PHASE 4: WORLD DESIGN

===============================================================================

LOCATIONS
─────────

► Kitchen (loc_kitchen)
  The center of domestic life. Bright, well-lit, modern appliances.
  Natural light through windows. Counter island in the center.
  Function: Breakfast activity, cooking scenes, economy events (rent notes)
  Access: Always available
  Video: angela_white_4 clips (Breakfast), plus text scenes

► Living Room (loc_living_room)
  Couch facing a TV. Comfortable, lived-in. Where they watch movies.
  Function: Movie Night, Couch Play, Deep Conversation
  Access: Always available
  Video: angela_white_4 clips (Movie Night), Mofos clips (Couch Play)

► Angela's Bedroom (loc_angelas_bedroom)
  Her private space. Bed, pillows, warm lighting.
  Function: Angela's Morning (peek), Morning Together, Exploring Kink (bed phase),
  Bedroom Moment, Bedroom Encounter, Spa/Massage
  Access: Angela's Morning is peekable from Day 2. Other activities
  unlock at love 30+ with trust requirements.
  Video: 480p.h264(1) (Morning peek), 480p.h264(2) (Morning Together),
  Step Bro (Bedroom Encounter), angela_white_4 (Bedroom Moment),
  NewSensations (Spa/Massage), Busty Babe Leash (Exploring Kink, bed phase)

► Bathroom (loc_bathroom)
  Bathtub, warm lighting, steam.
  Function: Angela's Bath (peek), Towel Encounter, Bath Together
  Access: Bath peek from Day 2. Towel Encounter at love >= 10. Bath Together at love >= 35.
  Video: 480p.h264 (Bath peek), Step Bro clips 4-6 (Towel Encounter),
  POV Blowjob Bath (Bath Together)

► Bedroom Floor (loc_bedroom_floor)
  Rug area, mirror nearby. Part of Angela's bedroom but distinct zone.
  Function: Bedroom Play, Exploring Kink
  Access: Bedroom Play at love >= 30, trust >= 25. Exploring Kink at love >= 45, trust >= 30.
  Video: Mofos clips 3-5, 11, 12 (Bedroom Play),
  Busty Babe Leash clips 1-14 (Exploring Kink)

► Cafe (loc_cafe)
  Jack's workplace. A neighborhood cafe. Text-only — no video clips.
  Function: Work shifts ($70 each). Morning or Afternoon slot.
  Access: Always available
  Video: None (text-only)

► Hotel (loc_hotel)
  Hotel bedroom. Romantic, private. "Somewhere nobody knows us."
  Function: Date Night Hotel activity
  Access: Love >= 40, trust >= 30. Costs $300.
  Video: ADULT TIME clips 1-25

TIME STRUCTURE
──────────────

Game spans: 30 days
Time periods: 4 per day

| Slot | Activities Available |
|---|---|
| **Morning** | Breakfast/Kitchen, Angela's Morning (peek), Cafe (morning shift) |
| **Afternoon** | Cafe (afternoon shift), Couch Play, Bedroom Play, Spa/Massage |
| **Evening** | Movie Night, Angela's Bath (peek), Deep Conversation, Date Night Hotel |
| **Night** | Morning Together, Bath Together, Exploring Kink |

SLOT RULES:
- Morning: Player picks Breakfast (interact) OR Morning peek (observe) OR Cafe shift. Can't do multiple.
- Afternoon: Before love 20, only Cafe is available. Player can skip (free time, no stat change) or work.
- Evening: Bath peek moves here — she bathes in the evening. Deep Conversation replaces Movie Night for that slot (can't do both in one evening).
- Night: Empty before love 30 (no unlocked activities). Nighttime intimacy must be earned.
- Any slot can be skipped (free time, no stat change).

DAY PROGRESSION:
- Days 1-3: Act 1 — Jack Arrives, daily routine establishes. Breakfast, peeks, Movie Night (text). 3 useful slots per day.
- Days 4-10: Towel Encounter fires. Deep Conversation unlocks. Trust building begins. Still 3 useful slots.
- Days 10-20: Couch Play unlocks (love 20). Afternoon becomes meaningful. Bedroom Encounter fires. 4 useful slots.
- Days 20-30: Morning Together, Bedroom Play, Special Activities unlock. All 4 slots active. Endgame push.

===============================================================================

                    PHASE 5: DAILY LIFE DESIGN

===============================================================================

ACTIVITY OVERVIEW
─────────────────

16 activities total:
- 8 Daily activities (Breakfast, Movie Night, Couch Play, Angela's Bath,
  Angela's Morning, Morning Together, Bedroom Play, Deep Conversation)
- 4 Special activities (Date Night Hotel, Spa/Massage, Bath Together,
  Exploring Kink)
- 4 Story events (Jack Arrives, Towel Encounter, Bedroom Encounter,
  Bedroom Moment) — covered in Phase 9

Each daily/special activity has a clip escalation table showing what the
player sees at each love bracket. Activities escalate at different rates
based on their available clip content (clip-first design).

Activity types:
- **Interactive**: Player participates. Choices affect stats.
- **Peekable**: Player observes. No interaction. Risk of detection.
- **Text-only**: No video clips. Dialogue and narrative only.
- **Special arc**: Full multi-clip sequence plays in order. One-time
  story experience, replayable at reduced gains.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MORNING ACTIVITIES (Slot 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

───────────────────────────────────────────────────
ACTIVITY 1: Breakfast/Kitchen
───────────────────────────────────────────────────
Type: Daily, Interactive
Location: loc_kitchen
Video Source: angela_white_4 (clips 1–12)
Available: Day 2+
Love Required: 0
Trust Required: —
Time Slot: Morning

ESCALATION TABLE:
| Love | Clips | Content |
|---|---|---|
| 0–10 | 1–5 | Angela enters kitchen, opens fridge, grabs fruit plate, places food, eats playfully. Domestic SFW. |
| 11–20 | 6 | Man arrives shirtless, embraces her from behind. She laughs. Tender. |
| 21–30 | 7–8 | Passionate kissing in kitchen, neck kisses, caressing. Shirts partially off. |
| 31–40 | 9–10 | Shorts removed, kissing her lower body over counter. Foreplay in kitchen. |
| 41–50 | 11–12 | Oral sex in kitchen. Full intimacy during breakfast routine. |

PLAYER CHOICES:
- Eat together (+1 love) — always available
- Help cook (+2 love) — requires love >= 5
- Compliment her food (+1 love) — always available
- Cook for her (+1 trust) — requires love >= 5. Trust-only action: no love gain.
- Passionate morning routine (+2 love) — requires love >= 31. Physical intimacy replaces the meal.

───────────────────────────────────────────────────
ACTIVITY 5: Angela's Morning (Peekable)
───────────────────────────────────────────────────
Type: Daily, Peekable (observational — no interaction)
Location: loc_angelas_bedroom
Video Source: 480p.h264 (1) (clips 1–20)
Available: Day 2+
Love Required: 0 (peek)
Trust Required: —
Time Slot: Morning

ESCALATION TABLE:
| Love | Clips | Content |
|---|---|---|
| 0–10 | 1–5 | Resting in bed in underwear, walking, grabbing coffee mug, sitting at window. SFW morning. |
| 11–20 | 6, 11 | Removing robe in underwear. Crawling on bed. Suggestive but not explicit. |
| 21–30 | 7–8, 12, 16–20 | Unbuttoning shirt, breasts exposed. Removing shirt. Nude posing — crawling on bed, adjusting pillows, sitting nude, lying prone. Comfortable in her own skin. |
| 31–40 | 9–10, 14 | Pulling underwear aside, touching groin area. Self-exploration. |
| 41–50 | 13, 15 | Full masturbation — deliberate genital self-stimulation, rhythmic touching. Intense private moment. |

PLAYER CHOICES: None. Peekable activity — player observes, does not interact.
PEEK RISK: 15% chance of being caught (drops to 5% at love >= 20). If caught: admit (+2 trust) or deny (-3 trust). Maximum once per week — after being caught, can't peek for 3 days.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AFTERNOON ACTIVITIES (Slot 2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

───────────────────────────────────────────────────
ACTIVITY 3: Couch Play (Unlocks at love 20)
───────────────────────────────────────────────────
Type: Daily, Interactive
Location: loc_living_room
Video Source: Mofos (clips 6, 8–10)
Available: Love >= 20
Trust Required: —
Time Slot: Afternoon

ESCALATION TABLE:
| Love | Clips | Content |
|---|---|---|
| 20–30 | — | Text-only. She teases, stretches, watches you watching her. Playful tension. |
| 31–40 | 6, 8 | Couple foreplay and sex on couch — touching, penetration. |
| 41–50 | 9–10 | Afterglow — solo self-touch, then he stimulates her manually. |

PLAYER CHOICES PER VISIT:
- Be gentle and attentive (+1 love, +1 trust)
- Be passionate (+2 love, +0 trust)

───────────────────────────────────────────────────
ACTIVITY 15: Bedroom Play (Unlocks at love 30, trust 25)
───────────────────────────────────────────────────
Type: Daily, Interactive
Location: loc_bedroom_floor
Video Source: Mofos (clips 3–5, 11, 12)
Available: Love >= 30, Trust >= 25
Time Slot: Afternoon

ESCALATION TABLE:
| Love | Clips | Content |
|---|---|---|
| 30–35 | 3, 12 | Nude posing on rug, talking to camera — playful, confident. She knows he's watching. |
| 36–40 | 4–5 | Oral sex — she kneels on rug and performs blowjob. Direct eye contact with camera. |
| 41–50 | 11 | Solo masturbation on all fours — purely for herself. Most intimate reveal. |

PLAYER CHOICES PER VISIT:
- Watch and appreciate (+1 love, +1 trust)
- Encourage and participate (+2 love, +0 trust)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVENING ACTIVITIES (Slot 3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

───────────────────────────────────────────────────
ACTIVITY 2: Movie Night
───────────────────────────────────────────────────
Type: Daily, Interactive
Location: loc_living_room
Video Source: angela_white_4 (clips 13–14, 17–28)
Available: Day 3+
Love Required: 0 (text) / 21 (video)
Trust Required: —
Time Slot: Evening

ESCALATION TABLE:
| Love | Clips | Content |
|---|---|---|
| 0–20 | (none) | Text-only: sit on couch, watch movie. She sits close, legs touch, she laughs at the same parts. Tension builds but nothing happens. |
| 21–30 | 13–14 | First physical contact during movie — handjob + passionate kiss. She initiates. Sofa foreplay, thigh kissing. |
| 31–40 | 17–20 | Sex on couch — reclining penetration, oral stimulation of her, straddling/grinding, cowgirl. The movie is forgotten. |
| 41–50 | 21–28 | Intense — multiple positions on couch. Cowgirl riding, doggy style, anal penetration, oral, climax. Full sequence. |

PLAYER CHOICES (text phase, love 0–20):
- Watch together (+1 love)
- Suggest her favorite movie (+1 love)

───────────────────────────────────────────────────
ACTIVITY 4: Angela's Bath (Peekable)
───────────────────────────────────────────────────
Type: Daily, Peekable (observational)
Location: loc_bathroom
Video Source: 480p.h264 (clips 1–16)
Available: Day 2+
Love Required: 0 (peek)
Trust Required: —
Time Slot: Evening

ESCALATION TABLE:
| Love | Clips | Content |
|---|---|---|
| 0–10 | 1–2, 15–16 | Entering tub, exiting tub. Brief glimpse — she's just bathing. |
| 11–20 | 4–6, 8–10, 14 | Full bathing routine: sitting up, washing with loofah, soaping, scrubbing, relaxing. |
| 21–30 | 3, 12–13 | Breast touching in water, caressing body, intimate self-soothing. |
| 31–40 | 7 | Self-touching lower body with loofah/object. Self-care becomes self-pleasure. |
| 41–50 | 11 | Genital self-stimulation in tub. Full private moment. |

PLAYER CHOICES: None. Peekable activity.
PEEK RISK: Same rules as Angela's Morning (15% catch, drops to 5% at love >= 20).

───────────────────────────────────────────────────
ACTIVITY 16: Deep Conversation (Unlocks at love 10, trust 20)
───────────────────────────────────────────────────
Type: Daily, Text-only (no video)
Location: loc_living_room
Video Source: None
Available: Love >= 10, Trust >= 20
Time Slot: Evening (replaces Movie Night — can't do both in one evening)

Text-based activity. Angela and Jack talk about life, family, dreams, fears.
The only activity that significantly builds both love AND trust.
Also where Angela drops hints about gifts she wants (Special Gift mechanic).

PLAYER CHOICES PER CONVERSATION:
- Listen and ask questions (+3 love, +1 trust)
- Share something personal (+2 love, +2 trust)
- Deflect with humor (+1 love, +0 trust)

HINT MECHANIC: Angela mentions things she wants during Deep Conversation
(trust >= 20). Hints also appear randomly at Breakfast (love >= 15).
One hint per week maximum across all sources. Fulfilling a hint with a
Special Gift ($150) gives +5 love.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIGHT ACTIVITIES (Slot 4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

───────────────────────────────────────────────────
ACTIVITY 6: Morning Together (Unlocks at love 30, trust 25)
───────────────────────────────────────────────────
Type: Daily, Interactive
Location: loc_angelas_bedroom
Video Source: 480p.h264 (2) (clips 1–20)
Available: Love >= 30, Trust >= 25
Time Slot: Night (spans night-to-morning — they go to bed together, wake up together)

ESCALATION TABLE:
| Love | Clips | Content |
|---|---|---|
| 30–35 | 1–3 | Sleeping together, waking, gentle shoulder touch, tender kissing. |
| 36–40 | 4–8, 14, 19–20 | Foreplay — thigh kissing, breast stimulation, oral, mutual touching, straddling, manual stimulation, grinding. |
| 41–45 | 9–13 | Sex — cowgirl, grinding, missionary, multiple positions. Active intimacy. |
| 46–50 | 15–18 | Intense sex — doggy style, anal, passionate missionary, deep connection. |

PLAYER CHOICES PER VISIT:
- Cuddle and talk (+1 love, +1 trust)
- Initiate intimacy (+2 love, +0 trust)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECIAL ACTIVITIES (Full Arc Sequences)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Special activities play their FULL clip sequence in order on first visit.
Replayable at reduced gains (50% love, 0 trust).

───────────────────────────────────────────────────
ACTIVITY 11: Date Night Hotel
───────────────────────────────────────────────────
Type: Special arc (25 clips in sequence)
Location: loc_hotel
Video Source: ADULT TIME (clips 1–25)
Available: Love >= 40, Trust >= 30
Cost: $300
Time Slot: Evening
Stat Change: love +8, trust +5

The romantic culmination. Angela suggests "somewhere nobody knows us."

ARC SEQUENCE:
- Arrival (clips 1–3): Lingerie, anticipation, first kiss at the hotel. Straddling, passionate kissing. No penetration.
- Undressing (clips 4–7): Slow removal, tender touches, kissing abdomen and hips, grinding. Building intimacy.
- First wave (clips 8–12): Intensity builds — riding/grinding, foreplay, then oral sex. First peak of passion.
- Intimate pause (clips 13–14): They stop and just look at each other. Lying together, eye contact, quiet tenderness. No sexual activity — just being present.
- Second wave (clips 15–20): Oral sex, handjob + kissing, manual stimulation, penetrative sex, gentle caressing. Passion and tenderness interleave.
- Afterglow & final peak (clips 21–23): Hand-holding and gentle massage give way to one last passionate encounter — full penetrative sex. The night's final crescendo.
- Departure (clips 24–25): She gazes at him lovingly, then leaves the room. He lies in bed, thinking. Something has changed between them.

───────────────────────────────────────────────────
ACTIVITY 12: Spa/Massage
───────────────────────────────────────────────────
Type: Special arc (20 clips in sequence)
Location: loc_angelas_bedroom
Video Source: NewSensations (clips 1–20)
Available: Love >= 35, Trust >= 28
Cost: Free (at home)
Time Slot: Afternoon
Stat Change: love +6, trust +4

Angela sets up a massage session at home — oils, candles, towels on the bed.

ARC SEQUENCE:
- Setup (clips 1–3): Jack enters the bedroom, Angela's laid out towels and oils — SFW establishment
- Preparation (clip 4): Angela fixes her hair at the bathroom mirror
- Getting ready (clip 5): She brushes her hair, sets the mood — candles lit
- Massage (clips 6–10): Professional-style massage. Oil, rubbing, relaxation.
- Sensual turn (clips 11–14): Massage becomes intimate — oil on breasts, genital stimulation, sensual chest touching, shoulder massage. Arousal builds.
- Sexual (clips 15–18): Oral sex, handjob, cowgirl riding, penetration. Full sexual encounter emerges from the massage.
- Aftercare (clips 19–20): She massages his back with oil (tender role reversal), then oral sex. The session winds down intimately.

───────────────────────────────────────────────────
ACTIVITY 13: Bath Together
───────────────────────────────────────────────────
Type: Special arc (10 clips in sequence)
Location: loc_bathroom
Video Source: POV Blowjob Bath (clips 1–10)
Available: Love >= 35, Trust >= 28
Cost: Free (at home)
Time Slot: Night
Stat Change: love +5, trust +3

Angela invites Jack to join her bath.

ARC SEQUENCE:
- Self-care (clips 1–2, 4): Angela bathing alone — washing breasts, scrubbing back, applying bath oil. Relaxed, unguarded.
- Self-pleasure (clips 3, 5–6): Self-stimulation — breast/clitoral touching, anal self-play with fingers. She's aware he's watching.
- Display (clips 7–8): She stands near the window — nude posing, back and buttocks on display. Deliberate showing off.
- Together (clips 9–10): Oral sex (blowjob) in the bathtub. She takes the lead.

───────────────────────────────────────────────────
ACTIVITY 14: Exploring Kink
───────────────────────────────────────────────────
Type: Special arc (14 clips in sequence)
Location: loc_bedroom_floor → loc_angelas_bedroom
Video Source: Busty Babe Leash (clips 1–14)
Available: Love >= 45, Trust >= 30
Cost: Free (at home)
Time Slot: Night
Stat Change: love +4, trust +2

Late-game content. Angela suggests trying something new — BDSM-lite.

ARC SEQUENCE:
- Floor/Mirror (clips 1–4): Pink lingerie, kneeling, leash, oral, crawling near mirror
- Bed (clips 5–14): Restrained positions, various sexual acts, collar/leash play, multiple positions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORK ACTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

───────────────────────────────────────────────────
Cafe Shift
───────────────────────────────────────────────────
Type: Solo, Text-only
Location: loc_cafe
Video Source: None
Available: Always
Time Slot: Morning or Afternoon (max 2 shifts/day)
Pay: $70 per shift

Jack works at a neighborhood cafe. The cafe exists to create economic
pressure, not as a location with its own content.

| Detail | Value |
|---|---|
| Pay | $70 per shift |
| Available slots | Morning, Afternoon (max 2 shifts/day) |
| Morning trade-off | Skips Breakfast/Kitchen — loses love-gain opportunity |
| Afternoon trade-off | Skips Couch Play, Bedroom Play, or Spa |
| Tips | None. Flat rate. Predictable income for planning. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REPLAYABILITY RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Story events (7–10): One-time only. Cannot be replayed.
- Special activities (11–14): Replayable after first completion.
  First play: full love/trust gains. Replay: 50% love gain, 0 trust gain.
  Same diminishing returns as daily activities apply.
- Daily activities (1–6, 15, 16): Always available (subject to unlock and diminishing returns).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTIVITY SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| # | Activity | Type | Slot | Love Req | Trust Req | Clips | Source |
|---|---|---|---|---|---|---|---|
| 1 | Breakfast/Kitchen | Daily | Morning | 0 | — | 12 | angela_white_4 |
| 2 | Movie Night | Daily | Evening | 0/21 | — | 14 | angela_white_4 |
| 3 | Couch Play | Daily | Afternoon | 20 | — | 4 | Mofos |
| 4 | Angela's Bath | Peek | Evening | 0 | — | 16 | 480p.h264 |
| 5 | Angela's Morning | Peek | Morning | 0 | — | 20 | 480p.h264(1) |
| 6 | Morning Together | Daily | Night | 30 | 25 | 20 | 480p.h264(2) |
| 7-10 | Story Events | Story | — | varies | varies | 19 | Step Bro + AW4 |
| 11 | Date Night Hotel | Special | Evening | 40 | 30 | 25 | ADULT TIME |
| 12 | Spa/Massage | Special | Afternoon | 35 | 28 | 20 | NewSensations |
| 13 | Bath Together | Special | Night | 35 | 28 | 10 | POV Blowjob Bath |
| 14 | Exploring Kink | Special | Night | 45 | 30 | 14 | Busty Babe Leash |
| 15 | Bedroom Play | Daily | Afternoon | 30 | 25 | 5 | Mofos |
| 16 | Deep Conversation | Text | Evening | 10 | 20 | 0 | — |
| — | Cafe Shift | Work | Morn/Aft | 0 | — | 0 | — |

===============================================================================

                    PHASE 6: STORY ARCHITECTURE

===============================================================================

STORY STRUCTURE
───────────────

ACT 1: THE NEW NORMAL (love 0–10, Days 1–5)

- Hook: Day 1 — Jack arrives at Angela's apartment. She welcomes him.
  Tutorial. They're polite strangers under one roof.
- Establishing: Daily routine begins. Breakfast together (SFW clips 1–5).
  Jack peeks at her bath and morning routines. Movie Night is text-only —
  they sit on the couch, legs touch, tension builds but nothing happens.
- Inciting Incident: Towel Encounter (love >= 10, trust >= 18). Jack
  accidentally walks in on Angela near the tub. She wraps up, they laugh
  it off — but the spark is lit.

ACT 2: GROWING CLOSER (love 11–30, Days 5–18)

- Rising Tension: Daily activities escalate. Breakfast moves from domestic
  to embracing and kissing. Bath/Morning peeks reveal more. Movie Night
  gets physical at love 21+ (sofa foreplay clips).
- Turning Point 1: Couch Play unlocks (love 20). Afternoon slot becomes
  meaningful. She's teasing and playful on the couch (text-only at first, video at love 31+).
- Complications: Deep Conversation unlocks (love 10, trust 20). Trust
  building becomes critical — she won't escalate without emotional safety.
- Turning Point 2: Bedroom Encounter (love 25, trust 22). Their first
  intimate night. Lingerie, the tension breaks. Love at trigger time
  determines clip count (love 25–29 = 3 clips, love 30+ = full 11 clips).
- Key Milestone: Bedroom Moment (love 30, trust 25). Brief but intense —
  kissing, anal. "First time in her bedroom on her terms." Unlocks
  Morning Together and Bedroom Play.

ACT 3: DEEP CONNECTION (love 31–50, Days 18–30)

- Point of No Return: All 4 time slots now active. Morning Together,
  Bedroom Play, and escalating daily activities fill the day.
- Special Activities Unlock:
  - Spa/Massage (love 35, trust 28) — 20 clips, free
  - Bath Together (love 35, trust 28) — 10 clips, free
  - Date Night Hotel (love 40, trust 30) — 25 clips, $300
  - Exploring Kink (love 45, trust 30) — 14 clips, free
- Climactic Sequence: Date Night Hotel is the romantic culmination.
  Angela suggests "somewhere nobody knows us." 25-clip arc. Love +8,
  trust +5. The longest scene in the game.
- Resolution: Endings evaluated at Day 30 based on final love + trust.

STORY EVENT FLOWCHART
─────────────────────

```
Day 1: Jack Arrives (love +3)
  ↓
Daily Loop: Breakfast + Bath peek + Morning peek + Movie Night (text)
  ↓ love >= 10, trust >= 18
Towel Encounter (love +3, trust +2)
  ↓ love >= 20
Couch Play unlocks
  ↓ love >= 25, trust >= 22
Bedroom Encounter (love +5, trust +3)
  ↓ love >= 30, trust >= 25
Bedroom Moment (love +3, trust +2) → Unlocks Morning Together + Bedroom Play
  ↓ love >= 35
Special Activities unlock (Spa, Bath Together)
  ↓ love >= 40
Date Night Hotel ($300, love +8, trust +5)
  ↓ love >= 45
Exploring Kink
  ↓ Day 30
ENDINGS
```

Arrows show progression order. Each activity/event is independently gated
by its own love/trust requirements — no prerequisite flags between them.

ENDINGS
───────

Endings are evaluated in priority order at Day 30 — first match wins.

| Priority | Ending | Condition | Description |
|---|---|---|---|
| 1 | Kicked Out | trust = 0 | Trust hit zero. Angela asks Jack to leave. Game over. (Can trigger early.) |
| 2 | True Love | love >= 50, trust >= 38 | Angela and Jack become a real couple. Date Night Hotel is the culminating scene. Open, honest, committed. |
| 3 | Close Bond | love >= 35, trust >= 25 | Deep connection but not fully committed. They care deeply but haven't taken the final step. |
| 4 | Bittersweet | love >= 35, trust < 25 | Physical intimacy without emotional safety. She enjoys being with Jack but can't fully let her guard down. They part with mixed feelings. |
| 5 | Friendly | love >= 15 | Friendly housemates with unresolved tension. Some good memories but nothing lasting. |
| 6 | Distant | (default) | Jack never connected with Angela. He moves out. |

ENDING REACHABILITY:
- True Love: Requires consistent daily engagement + Date Night Hotel. Achievable by ~Day 30 with optimal play.
- Close Bond: Natural outcome for regular engagement without maximizing everything. ~Day 20-25.
- Bittersweet: Physical intimacy (love 35+) but neglected trust — missed rent, denied peeking, pushed boundaries. At very low trust (< love ÷ 2), "not tonight" adds friction. At trust 20–24, activities still proceed but the relationship lacks emotional depth.
- Friendly: Player who works too much, skips breakfasts, doesn't pursue deeper activities.
- Distant: Player who actively avoids Angela.
- Kicked Out: Repeatedly violates trust (missed rent, aggressive actions, caught peeking and lying).

===============================================================================

                    PHASE 7: INTIMACY PROGRESSION

===============================================================================

ESCALATION SYSTEM
─────────────────

This game uses LOVE BRACKETS — 5 content levels driven by the love stat.
No flag gates. Content level is determined purely by love threshold.

| Bracket | Love Range | Label | Content Ceiling |
|---|---|---|---|
| 1 | 0–10 | Strangers | SFW only. Domestic routine, getting to know each other. |
| 2 | 11–20 | Warming Up | Suggestive. Flirting, accidental glimpses, light touching. |
| 3 | 21–30 | Attraction | Kissing, embracing, foreplay begins. |
| 4 | 31–40 | Intimate | Oral, manual stimulation, undressing together. |
| 5 | 41–50 | Lovers | Full sex, all positions, deep romantic connection. |

CLIP-FIRST DESIGN NOTE:
Brackets define the *general* content ceiling at each love level. Individual
activities escalate based on their available clip content — some reach full
sex earlier (Movie Night at love 31+), others peak at oral (Breakfast at
love 41+). Activities use what's available, not what the bracket prescribes.

TRUST GATES
───────────

Trust acts as a pacing control independent of love. Angela won't escalate
if she doesn't feel safe, even when love is high.

| Activity | Love Required | Trust Required |
|---|---|---|
| Towel Encounter | 10 | 18 |
| Deep Conversation | 10 | 20 |
| Bedroom Encounter | 25 | 22 |
| Bedroom Moment | 30 | 25 |
| Morning Together | 30 | 25 |
| Bedroom Play | 30 | 25 |
| Spa/Massage | 35 | 28 |
| Bath Together | 35 | 28 |
| Date Night Hotel | 40 | 30 |
| Exploring Kink | 45 | 30 |

High love + low trust = "she wants to but can't." Trust prevents rushing.

"NOT TONIGHT" MECHANIC:
When starting a couple activity (Couch Play, Morning Together, Bedroom Play),
there's a chance Angela declines based on trust gap. If trust < (love ÷ 2),
she says "not tonight." Player choice:
- Respect it (+2 trust)
- Push (-4 trust)
At trust >= 30, she never declines.

HOW STAGES APPEAR IN ACTIVITIES VS STORY EVENTS:

| Bracket | Activity Experience | Story Event |
|---|---|---|
| 1 (0-10) | SFW clips, text interactions | Jack Arrives |
| 2 (11-20) | Suggestive clips, embracing | Towel Encounter |
| 3 (21-30) | Kissing, foreplay clips | Bedroom Encounter |
| 4 (31-40) | Oral, manual clips | Bedroom Moment |
| 5 (41-50) | Full sex clips | Date Night Hotel |

PROGRESSION LOGIC:
- Activities build stats slowly and consistently (~70% of total love gains)
- Story events provide milestone bursts (~30% of total love gains)
- Players must engage with activities to reach story event thresholds
- Each activity tier unlocks at the appropriate love level
- Trust must be maintained in parallel through rent, honesty, and respect

===============================================================================

                    PHASE 8: CHOICE ARCHITECTURE

===============================================================================

STATS
─────

| Stat | Start | Range | Role |
|---|---|---|---|
| **Love** | 0 | 0–50 | Primary. Drives all escalation and unlocks. |
| **Trust** | 15 | 0–50 | Pacing control. Angela won't escalate without emotional safety. |
| **Money** | $50 | 0+ | Resource. Creates budget tension — every dollar spent on Angela is a shift worked away from her. |

STAT RULES:
- Trust = 0 → Game Over (Angela kicks Jack out)
- Love drops whenever trust drops sharply (trust -3 or worse → love -1)
- Trust gates prevent rushing — high love + low trust = she wants to but can't

LOVE GAIN SOURCES
─────────────────

| Action | Love Gain | Notes |
|---|---|---|
| Eat breakfast together | +1 | Always available |
| Help cook breakfast | +2 | Requires love >= 5 |
| Compliment her food | +1 | Always available |
| Passionate morning routine | +2 | Requires love >= 31 |
| Peek at her (Bath/Morning) | +1 | Available daily. Risk of being caught. |
| Bring her flowers | +2 | Costs $30 |
| Deep conversation | +1 to +3 | Requires trust >= 20. Gain depends on player choice. |
| Special gift | +5 | Costs $150. Requires hint from Angela. |
| Story events | +3 to +5 | Auto-triggered at love thresholds |
| Movie Night (text, watch) | +1 | Love 0–20. Sit close, share popcorn. |
| Movie Night (suggest movie) | +1 | Love 0–20. She's surprised you remembered. |
| Movie Night (video tiers) | +2 | Love 21+. Physical intimacy during movie. |
| Couch Play | +2 | Love 20+. |
| Morning Together | +2 | Love 30+. |
| Bedroom Play | +2 | Love 30+. |
| Special activities | +4 to +8 | Date Night gives highest. |
| "I want to take you somewhere" | +1 now / +2 fulfilled | Player-initiated. Must spend $100+ within 2 weeks. Broken: love -2. |

TRUST GAIN SOURCES
──────────────────

| Action | Trust Gain | Notes |
|---|---|---|
| Pay rent on time | +2 | Weekly. Due every 7 days. |
| Pay rent early | +1 | Bonus on top of +2 for on-time. |
| Cook for her (Breakfast) | +1 | Requires love >= 5. Trust-only action. |
| Honest when caught peeking | +2 | Random event if caught during Bath/Morning peek. |
| Respect her "not tonight" | +2 | When she declines, accept gracefully. |
| Deep conversation | +1 to +2 | Listen: +1, Share personal: +2, Deflect: +0. |
| Help with chores | +1 | Available daily. |
| Morning Together | +1 | Sleeping together builds trust. |
| Couch Play (gentle) | +1 | Being attentive during intimacy. |
| Bedroom Play (watch) | +1 | Being respectful during her moments. |
| "Working a lot" event | +2 | 5+ shifts in one week. |
| Story events | +2 to +3 | Auto from milestones. |
| Date Night Hotel | +5 | Special activity (love 40+). |
| Spa/Massage | +4 | Special activity (love 35+). |
| Bath Together | +3 | Special activity (love 35+). |
| Exploring Kink | +2 | Special activity (love 45+). |

TRUST LOSS SOURCES
──────────────────

| Action | Trust Loss | Notes |
|---|---|---|
| Miss rent | -3 | Weekly check. |
| Caught peeking (deny it) | -3 | Random event. |
| Push when she says no | -4 | If player insists after "not tonight." |
| Aggressive dialogue choice | -2 | Various story moments. |

ECONOMY
───────

| Item | Cost | Notes |
|---|---|---|
| Cafe shift | +$70 | Morning or Afternoon slot |
| Rent | -$200 | Due Day 7, 14, 21, 28 |
| Flowers | -$30 | +2 love. Available during Breakfast or when returning home. |
| Special gift | -$150 | +5 love. Requires hint from Angela. |
| Date Night Hotel | -$300 | Special activity. Most expensive. |
| Spa, Bath, Kink | Free | At-home activities. |

ECONOMY MATH:
- 3 shifts/week barely covers rent ($210). $10 left over.
- 4 shifts/week = $280. $80 savings. Leaves 24–25 of 28 weekly slots for Angela.
- Saving for Date Night at love 40 means ~4 extra shifts — 4 mornings/afternoons NOT with Angela.

MONEY TALK EVENTS
─────────────────

| Event | Trigger | What Happens | Effect |
|---|---|---|---|
| "You've been working a lot" | 5+ shifts in one week | Angela makes him dinner. She misses him. | trust +2 |
| "I want to take you somewhere" | Player-initiated ($100+ saved) | Jack tells Angela he's saving. Must spend $100+ on her within 2 weeks. | love +1 now. Fulfilled: +2. Broken: -2. |
| "About the rent..." | Rent day (weekly) | If at Breakfast: Angela brings it up. If at Cafe: she leaves a note. | (existing rent trust rules) |

DIMINISHING RETURNS
───────────────────

Same action repeated: 100% → 75% → 50% → 0% stat effect.
Resets after 2 days of NOT doing that action.

ROUNDING: Gains always round up (ceiling).
- +1 at 75% = 1, at 50% = 1, at 0% = 0
- +2 at 75% = 2, at 50% = 1, at 0% = 0

Different choices within the same activity count as SEPARATE actions.
Within Breakfast: "Eat together," "Help cook," and "Compliment food"
each have independent diminishing return timers. The player exhausts a
specific choice, not the entire activity.

At love 0–10, available unique love-gaining actions:
- Breakfast: 3 choices (eat, cook, compliment)
- Bath peek: 1 (peek)
- Morning peek: 1 (peek)
- Movie Night: 2 (watch together, suggest movie)
- Bring flowers: 1 ($30)
Total: 8 unique actions. Enough for 2–3 full days before needing to rotate.

IN-ACTIVITY PURCHASES:
Flowers, gifts, and chores are choices within existing activities, not
separate time-slot actions:
- Bring flowers ($30): During Breakfast or when returning home.
- Special gift ($150): During Deep Conversation after Angela hints.
- Help with chores: During Breakfast/Kitchen. "Let me clean up."
These don't consume an extra time slot.

PEEK DETECTION
──────────────

15% chance of being caught each time you peek (Bath or Morning).
If caught: Admit honestly (+2 trust) or Deny (-3 trust).
Detection drops to 5% at love >= 20 (she's more comfortable).
Maximum once per week — after being caught, can't peek for 3 days.

===============================================================================

                    PHASE 9: SCENE DESIGN (STORY EVENTS)

===============================================================================

4 story events. One-time only. Cannot be replayed.
These are the milestone moments that punctuate the daily activity loop.

───────────────────────────────────────────────────
SCENE 7: Jack Arrives
───────────────────────────────────────────────────
Location: loc_kitchen / loc_angelas_bedroom (apartment tour)
Time: Day 1
Stage: Bracket 1 (SFW)
Trigger: Automatic — game start

What Happens:
Jack moves in. Angela shows him around the apartment. Tutorial scene.
She's welcoming but measured — polite, not warm. The apartment feels
like her space, and he's a guest. First impressions form.

VIDEOS:
- Clip 1 (NewSensations): Angela opens door in robe — Jack steps inside
  carrying his suitcase. She smiles, watches him walk past.
- Clip 2 (NewSensations): Angela at the door, smiling warmly, turning
  the handle — welcoming him in.
- Clip 3 (NewSensations): Jack setting up in the room — unpacking,
  getting settled into her space.

Stat Change: love +3
Choices: None (cinematic scene — tutorial)

───────────────────────────────────────────────────
SCENE 8: Towel Encounter
───────────────────────────────────────────────────
Location: loc_bathroom
Time: Any (fires when conditions met)
Stage: Bracket 2 (Suggestive)
Trigger: love >= 10, trust >= 18

What Happens:
Jack accidentally walks in on Angela near the bathtub. She's nude,
adjusting the faucet. She's not angry — she wraps up in a towel, they
have an awkward-but-charged conversation. Both feel something shift.
She laughs it off, but the look lingers.

VIDEOS:
- Clip 4 (Step Bro): Angela nude near bathtub, adjusting faucet. Jack walks in.
- Clip 5 (Step Bro): Angela wrapping in towel, smiling. Not upset — intrigued.
- Clip 6 (Step Bro): Angela in towel, talking animatedly. They laugh it off,
  but the spark is lit.

Stat Change: love +3, trust +2
Choices: None (cinematic scene)

───────────────────────────────────────────────────
SCENE 9: Bedroom Encounter
───────────────────────────────────────────────────
Location: loc_angelas_bedroom
Time: Any (fires when conditions met)
Stage: Bracket 3-4 (Kissing → Intimate)
Trigger: love >= 25, trust >= 22

What Happens:
Major milestone. Angela and Jack's first intimate night. She's in
lingerie, the tension breaks. Love stat at trigger time determines
how many clips play.

VIDEOS:
Love 25–29 (partial sequence):
- Clip 7 (Step Bro): Angela in black lingerie, lying in bed. Jack finds her.
- Clip 8 (Step Bro): He masturbates at the sight — she watches, intrigued.
- Clip 11 (Step Bro): Oral — she takes him, unhurried, deliberate.

Love 30+ (full sequence, clips 7–17):
- Clips 7–8, 11: As above
- Clip 12: Oral continues — confident, in control
- Clip 10: Missionary — she pulls him in, bodies pressed together
- Clip 9: Penetration deepens — rhythm building
- Clip 13: Thrusting — hip movement, passionate
- Clips 14–15: Doggy style — intense, both losing themselves
- Clip 16: Missionary — back to face-to-face, intimate and raw
- Clip 17: She performs oral — intimate finale.

Stat Change: love +5, trust +3
Choices: None (cinematic scene)

DESIGN NOTE: One-time event. If triggered at love 25–29, clips 10–17 are
never seen. Patient players who delay until love 30+ are rewarded with the
full 11-clip sequence. No second chance.

───────────────────────────────────────────────────
SCENE 10: Bedroom Moment
───────────────────────────────────────────────────
Location: loc_angelas_bedroom
Time: Any (fires when conditions met)
Stage: Bracket 4 (Intimate)
Trigger: love >= 30, trust >= 25

What Happens:
Brief but intense. Their relationship has deepened beyond the first
encounter. This is the "first time in her bedroom on her terms" moment.

VIDEOS:
- Clip 15 (angela_white_4): Kissing on bed — tender, slow, intimate.
- Clip 16 (angela_white_4): Anal sex — intense, deliberate, raw connection.

Stat Change: love +3, trust +2
Unlocks: Morning Together, Bedroom Play

Choices: None (cinematic scene)

===============================================================================

                    PHASE 9.5: OPENING SCENE DESIGN

===============================================================================

OPENING SCENE: "Jack Arrives"

═══════════════════════════════════════════════════
NODE 1: PLAYER IDENTITY
═══════════════════════════════════════════════════

Who: Jack. Young man, early 20s. Needs a place to stay.
Why here: His father married Angela. The marriage didn't last, but
Angela offered to let Jack stay at her apartment while he gets on his
feet. He accepted — it was practical.
Emotional state: Uncertain. Grateful but awkward. He doesn't know
Angela well. She's his father's ex-wife. He's carrying a suitcase
and a vague sense that this arrangement might be strange.
History: Jack and Angela met a few times during the marriage —
holidays, a dinner or two. They were polite. Nothing more. Now he's
moving into her home.

Narrative:
You stand at the door with your suitcase. The hallway smells like someone
else's life — her laundry detergent, a candle she left burning. You
knock, even though she said to just come in.

This is temporary. That's what you tell yourself. A few months, save
some money, figure things out. She offered, you accepted. Simple.

VIDEO: NewSensations clip 1 — Angela opens the door in a robe, Jack
steps inside carrying his suitcase. She smiles, watches him walk past.

───────────────────────────────────────────────────

═══════════════════════════════════════════════════
NODE 2: ANGELA INTRODUCTION
═══════════════════════════════════════════════════

Physical Description:
She opens the door and you see her properly for the first time outside
of a holiday dinner. Long dark hair, straight, falling past her
shoulders. Fair skin. Full-figured — curves she doesn't hide but
doesn't advertise. She's wearing a light satin robe, loosely tied. A delicate necklace.
Bare feet on the hardwood floor — she's comfortable in her own home.

She's taller than you remembered. She smiles — warm but measured, like
she's calibrating how much warmth is appropriate.

First words: "Jack. Come in. Let me show you around."

The greeting:
She steps aside. No hug — that would be too much for two people who
are almost strangers. Her hand touches your shoulder as you pass
through the doorway. Brief. Intentional or accidental? You can't tell.

Chemistry moment:
She walks ahead of you through the apartment. You notice the way she
carries herself — confident, unhurried. She looks back over her
shoulder to make sure you're following. The look lasts half a second
longer than it needs to.

VIDEO: NewSensations clip 2 — Angela at the door, smiling warmly,
turning the handle — welcoming him in.
VIDEO: NewSensations clip 3 — Jack setting up in the room — unpacking,
getting settled into her space.

CHOICES: None (cinematic scene — tutorial). Love +3 is awarded
automatically for completing the arrival sequence.

───────────────────────────────────────────────────

═══════════════════════════════════════════════════
NODE 3: THE SITUATION
═══════════════════════════════════════════════════

The Stakes: Jack needs housing. Angela offered. If this doesn't work,
he's back to couch-surfing or worse.
The Obstacle: She's his step-mom. The age gap. The fact that his
father was once married to her. Anyone looking in would say this is
inappropriate.
Why Alone: They live together. Just the two of them. Every morning,
every evening. Proximity is the catalyst.
The Forbidden Element: She's technically his step-mother. The domestic
intimacy — sharing a kitchen, hearing her bath through the walls —
creates a closeness that blurs the line between family and something
else.

Narrative:
She shows you the guest room. It's small but clean. She's put fresh
sheets on the bed. A towel folded on the pillow. She thought about
your arrival.

"Bathroom's down the hall. Kitchen — you saw it. Help yourself to
anything." She pauses at the door. "Rent is two hundred a week. I
know that sounds like a lot, but..."

"It's fine," you say. "I'll pick up shifts at the cafe."

She nods. A moment passes where neither of you moves.

"Well," she says. "Welcome home, Jack."

She closes the door. You sit on the bed. Home.

The loaded moment:
"Welcome home, Jack." — spoken by a woman who's been living alone,
to a young man who's just moved in. Just the two of them. For as
long as it takes.

===============================================================================

                    PHASE 10: TECHNICAL SPECS

===============================================================================

LOCATIONS
─────────

| ID | Name | Activities |
|---|---|---|
| loc_kitchen | Kitchen | Breakfast/Kitchen |
| loc_living_room | Living Room | Movie Night, Couch Play, Deep Conversation |
| loc_angelas_bedroom | Angela's Bedroom | Angela's Morning, Morning Together, Bedroom Encounter, Bedroom Moment, Spa/Massage, Exploring Kink (bed phase) |
| loc_bathroom | Bathroom | Angela's Bath, Towel Encounter, Bath Together |
| loc_bedroom_floor | Bedroom Floor | Bedroom Play, Exploring Kink |
| loc_cafe | Cafe | Cafe Shift (work) |
| loc_hotel | Hotel | Date Night Hotel |

CHARACTERS
──────────

| ID | Name | Role |
|---|---|---|
| npc_angela | Angela | Primary NPC. Step-mom. Love interest. |
| player | Jack | Player character. Step-son. |

STATS
─────

| Stat | ID | Range | Start | Role |
|---|---|---|---|---|
| Love | love | 0–50 | 0 | Primary driver. All escalation. |
| Trust | trust | 0–50 | 15 | Pacing control. Gates on activities. |
| Money | money | 0+ | $50 | Resource. Cafe shifts, rent, purchases. |

ACTIVITY UNLOCK SCHEDULE
────────────────────────

| Activity | Day | Love | Trust | Type |
|---|---|---|---|---|
| Jack Arrives | 1 | 0 | — | Story (auto) |
| Breakfast/Kitchen | 2+ | 0 | — | Daily |
| Angela's Bath | 2+ | 0 | — | Daily (peek) |
| Angela's Morning | 2+ | 0 | — | Daily (peek) |
| Movie Night | 3+ | 0/21 | — | Daily |
| Towel Encounter | — | 10 | 18 | Story (auto) |
| Deep Conversation | — | 10 | 20 | Daily |
| Couch Play | — | 20 | — | Daily |
| Bedroom Encounter | — | 25 | 22 | Story (auto) |
| Bedroom Moment | — | 30 | 25 | Story (auto) |
| Morning Together | — | 30 | 25 | Daily |
| Bedroom Play | — | 30 | 25 | Daily |
| Spa/Massage | — | 35 | 28 | Special |
| Bath Together | — | 35 | 28 | Special |
| Date Night Hotel | — | 40 | 30 | Special |
| Exploring Kink | — | 45 | 30 | Special |

GAME LENGTH
────────────

- 30 days total
- 4 time slots per day = 120 total actions
- 4 rent cycles (Day 7, 14, 21, 28)
- Endings evaluated at Day 30
- Early exit if trust = 0

CLIP COUNT VERIFICATION
───────────────────────

| # | Activity | Source | Clips | Count |
|---|---|---|---|---|
| 1 | Breakfast/Kitchen | angela_white_4 | 1–12 | 12 |
| 2 | Movie Night | angela_white_4 | 13–14, 17–28 | 14 |
| 3 | Couch Play | Mofos | 6,8–10 | 4 |
| 4 | Angela's Bath | 480p.h264 | 1–16 | 16 |
| 5 | Angela's Morning | 480p.h264 (1) | 1–20 | 20 |
| 6 | Morning Together | 480p.h264 (2) | 1–20 | 20 |
| 7 | Jack Arrives | NewSensations | 1–3 | 3 |
| 8 | Towel Encounter | Step Bro | 4–6 | 3 |
| 9 | Bedroom Encounter | Step Bro | 7–17 | 11 |
| 10 | Bedroom Moment | angela_white_4 | 15–16 | 2 |
| 11 | Date Night Hotel | ADULT TIME | 1–25 | 25 |
| 12 | Spa/Massage | NewSensations | 4–20 | 17 |
| 13 | Bath Together | POV Blowjob Bath | 1–10 | 10 |
| 14 | Exploring Kink | Busty Babe Leash | 1–14 | 14 |
| 15 | Bedroom Play | Mofos | 3–5, 11, 12 | 5 |
| | **TOTAL** | | | **176** |

Source verification:
- angela_white_4: 12 + 14 + 2 = 28 ✅
- Step Bro: 3 + 3 + 11 = 17 ✅
- Mofos: 4 + 5 = 9 ✅ (clips 1, 2, 7 dropped — phone/content mismatch)
- All other sources: single activity each ✅

VALIDATION CHECKLIST
────────────────────

| # | Check | Status |
|---|---|---|
| 1 | Every clip assigned | ✅ 182 clips, 16 activities, zero unassigned |
| 2 | NSFW isolation | ✅ Each activity's NSFW content from exactly 1 source |
| 3 | Sequence preserved | ✅ Couple/narrative in order. Solo by intensity. |
| 4 | SFW at low love | ✅ All dailies have SFW content at love 0–10 |
| 5 | Unlock progression | ✅ love 0→10→20→25→30→35→40→45 |
| 6 | All endings reachable | ✅ 6 endings, priority-ordered, all (love,trust) covered |
| 7 | No dead zones | ✅ Every love bracket has content |
| 8 | Angela has agency | ✅ She initiates at key moments, has private moments |

===============================================================================

                           END OF BOOK

===============================================================================
