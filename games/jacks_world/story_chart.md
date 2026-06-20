# Jack's World - Story Structure

> Game Design v0.4.8 — Love Path, Clip-First Design
>
> **Design philosophy:** Built FROM clips upward. Every described clip is assigned to exactly one game activity. NSFW clips from different video files are never combined in one activity. Couple/narrative clips play in their original sequence order within each activity. Solo peekable activities (Bath, Morning) organize clips by content intensity — these clips are independent vignettes, not continuous narrative.

## Core Concept

Jack moves into his step-mom Angela's apartment. Over time, a romantic bond develops. The **love stat** drives everything — as love increases, daily activities reveal more intimate content. There is one path (love), and the player's choices determine how deep the connection grows.

- **Low love:** Domestic routine, getting to know each other, SFW interactions
- **Medium love:** Flirting, suggestive glimpses, kissing, emotional vulnerability
- **High love:** Full romantic/sexual intimacy, special date activities, deep connection

## Stats System

| Stat | Start | Range | Notes |
|------|-------|-------|-------|
| **Love** | 0 | 0–50 | Primary stat. Drives all escalation and unlocks. |
| **Trust** | 15 | 0–50 | Pacing control. Angela won't escalate if she doesn't feel safe. |
| **Money** | 50 | 0+ | Resource. Cafe shifts pay $70. Rent ($200/week) and special activity costs create budget tension — every dollar spent on Angela is a shift worked away from her. |

> **Trust = 0 → Game Over** (Angela kicks Jack out)
> **Love drops** whenever trust drops sharply (trust -3 or worse in one event → love -1)
> Trust gates exist to prevent rushing — high love + low trust = she wants to but can't

## Love Brackets

| Bracket | Range | Label | Content Tier |
|---------|-------|-------|-------------|
| 1 | 0–10 | Strangers | SFW only. Domestic routine, getting to know each other |
| 2 | 11–20 | Warming Up | Suggestive. Flirting, accidental glimpses, light touching |
| 3 | 21–30 | Attraction | Kissing, embracing, foreplay begins |
| 4 | 31–40 | Intimate | Oral, manual stimulation, undressing together |
| 5 | 41–50 | Lovers | Full sex, all positions, deep romantic connection |

> **Note:** Brackets define the *general* content ceiling at each love level. Individual activities escalate based on their available clip content — some reach full sex earlier (Movie Night), others peak at oral (Breakfast). Clip-first design means activities use what's available, not what the bracket ideally prescribes.

---

## Video Source Map

| Short Name | Full Folder Name | Total Clips |
|---|---|---|
| angela_white_4 | `angela_white_4/` | 28 |
| 480p.h264 | `480p.h264/` | 16 |
| 480p.h264 (1) | `480p.h264 (1)/` | 20 |
| 480p.h264 (2) | `480p.h264 (2)/` | 20 |
| Step Bro | `[PornhubFans 480p] ANGELA WHITE - Busty Slut Fuck Her Step Bro/` | 17 |
| Mofos | `[PornhubFans 480p] Mofos - Big tit thicc Angela White sucks and fucks one lucky cock pov/` | 12 |
| ADULT TIME | `[PornhubFans 480p] ADULT TIME - Naturally Stacked Angela White Has Romantic Sex With Her Husband At The Hotel/` | 25 |
| NewSensations | `[PornhubFans 480p] NewSensations - Angela White XXX BIg Tits Rubdown/` | 20 |
| Busty Babe Leash | `[PornhubFans 480p] ANGELA WHITE - Busty Babe is All Yours While She Gets Fucked on a Leash/` | 14 |
| POV Blowjob Bath | `[PornhubFans 480p] ANGELA WHITE - POV Blowjob and Fucking in the Bath/` | 10 |

**Total described clips: 176. Step Bro clips 1–3 dropped (replaced by NewSensations 1–3 for Jack Arrives). 3 unassigned.**

---

## Activity Master List

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

---

## Activity Unlock Schedule

| Activity | Available From | Love Required | Trust Required | Type |
|---|---|---|---|---|
| Jack Arrives | Day 1 | 0 | — | Story (auto) |
| Breakfast/Kitchen | Day 2+ | 0 | — | Daily |
| Angela's Bath | Day 2+ | 0 (peek) | — | Daily |
| Angela's Morning | Day 2+ | 0 (peek) | — | Daily |
| Movie Night | Day 3+ | 0 (text) / 21 (video) | — | Daily |
| Towel Encounter | — | 10 | 18 | Story (auto) |
| Deep Conversation | — | 10 | 20 | Daily (unlock) |
| Couch Play | — | 20 | — | Daily (unlock) |
| Bedroom Encounter | — | 25 | 22 | Story (auto) |
| Bedroom Moment | — | 30 | 25 | Story (auto) |
| Morning Together | — | 30 | 25 | Daily (unlock) |
| Bedroom Play | — | 30 | 25 | Daily (unlock) |
| Spa/Massage | — | 35 | 28 | Special |
| Bath Together | — | 35 | 28 | Special |
| Date Night Hotel | — | 40 | 30 | Special |
| Exploring Kink | — | 45 | 30 | Special |

---

## Story Event Sequence

```mermaid
flowchart TD
    jack_arrives["Jack Arrives<br/>📍 Apartment<br/>🏷️ Day 1<br/>📊 love=0, trust=15"]
    daily_loop["Daily Loop Begins<br/>Breakfast + Bath peek + Morning peek + Movie Night text"]
    towel["Towel Encounter<br/>📍 Bathroom<br/>⚡ love >= 10, trust >= 18<br/>📊 love +3, trust +2"]
    couch_play["Couch Play unlocks<br/>⚡ love >= 20<br/>🎬 Mofos clips"]
    bedroom_enc["Bedroom Encounter<br/>📍 Bedroom<br/>⚡ love >= 25, trust >= 22<br/>📊 love +5, trust +3"]
    bedroom_mom["Bedroom Moment<br/>📍 Bedroom<br/>⚡ love >= 30, trust >= 25<br/>📊 love +3, trust +2<br/>🔓 Unlocks: Morning Together, Bedroom Play"]
    high_love["High Love Zone<br/>love 35–50<br/>🔓 Spa, Bath Together, Date Night, Kink"]
    endings["Endings<br/>Based on final love + trust"]

    jack_arrives --> daily_loop
    daily_loop --> |"love >= 10"| towel
    towel --> |"love >= 20"| couch_play
    couch_play --> |"love >= 25"| bedroom_enc
    bedroom_enc --> |"love >= 30"| bedroom_mom
    bedroom_mom --> |"love >= 35"| high_love
    high_love --> endings
```

> **Note:** Arrows show progression order (stat thresholds are reached in this sequence), not flag dependencies. Each activity/event is independently gated by its own love/trust requirements — no prerequisite flags between them.

---

## Story Events — Detail

### 7. Jack Arrives (Day 1)
**Video:** NewSensations clips 1–3 (all SFW)
- Clip 1: Angela opens the door in a robe — Jack steps inside carrying his suitcase
- Clip 2: Angela at the door, smiling warmly, turning the handle — welcoming him in
- Clip 3: Jack setting up in the room — unpacking, getting settled into her space

**Gameplay:** Jack moves in. Tutorial. Angela shows him around. Establishes the living situation.
**Stat change:** love +3

### 8. Towel Encounter (love >= 10, trust >= 18)
**Video:** Step Bro clips 4–6
- Clip 4: Angela nude near bathtub, adjusting faucet (Jack walks in)
- Clip 5: Angela wrapping in towel, smiling (not upset — intrigued)
- Clip 6: Angela in towel, talking animatedly (they laugh it off, but the spark is lit)

**Gameplay:** Jack accidentally walks in on Angela near the tub. She's not angry — she wraps up, they have an awkward-but-charged conversation. Both feel something shift.
**Stat change:** love +3, trust +2

### 9. Bedroom Encounter (love >= 25, trust >= 22)
**Video:** Step Bro clips 7–17
- Clip 7: Angela in black lingerie, lying in bed (Jack finds her)
- Clip 8: He masturbates at the sight of her — she watches, intrigued
- Clip 11: Oral — she takes him, unhurried, deliberate
- Clip 12: Oral continues — confident, in control
- Clip 10: Missionary — she pulls him in, bodies pressed together
- Clip 9: Penetration deepens — rhythm building
- Clip 13: Thrusting — hip movement, breast touch, passionate
- Clip 14: Doggy style — intense, she grips the sheets
- Clip 15: Doggy continues — deeper, both losing themselves
- Clip 16: Missionary — back to face-to-face, intimate and raw
- Clip 17: She performs oral — intimate finale

**Gameplay:** Major milestone. Angela and Jack's first intimate night. She's in lingerie, the tension breaks. Love stat determines how many clips play (love 25–29 = clips 7–8 + 11, love 30+ = full sequence clips 7–17).
**Stat change:** love +5, trust +3.

> **Design note:** This is a one-time event — it cannot be replayed. If triggered at love 25–29, clips 10–17 are never seen. Patient players who delay visiting the bedroom until love 30+ are rewarded with the full 11-clip sequence. This is intentional: the event fires based on the player's love at trigger time, and there's no second chance.

### 10. Bedroom Moment (love >= 30, trust >= 25)
**Video:** angela_white_4 clips 15–16
- Clip 15: Kissing on bed — tender, slow, intimate
- Clip 16: Anal sex — intense, deliberate, raw connection

**Gameplay:** Brief but intense. Their relationship has deepened beyond the first encounter. This is the "first time in her bedroom on her terms" moment.
**Stat change:** love +3, trust +2. Unlocks Morning Together, Bedroom Play.

---

## Daily Activities — Clip Escalation Tables

### 1. Breakfast/Kitchen
**Video:** angela_white_4 (clips 1–12) | **Location:** Kitchen

| Love | Clips | What Player Sees |
|---|---|---|
| 0–10 | 1–5 | Angela enters kitchen, opens fridge, grabs fruit plate, places food, eats playfully. Domestic SFW. |
| 11–20 | 6 | Man arrives shirtless, embraces her from behind. She laughs. Tender. |
| 21–30 | 7–8 | Passionate kissing in kitchen, neck kisses, caressing. Shirts partially off. |
| 31–40 | 9–10 | Shorts removed, kissing her lower body over counter. Foreplay in kitchen. |
| 41–50 | 11–12 | Oral sex in kitchen. Full intimacy during breakfast routine. |

**Player choices:**
- Eat together (+1 love) — always available
- Help cook (+2 love) — requires love >= 5
- Compliment her food (+1 love) — always available
- Cook for her (+1 trust) — requires love >= 5. Trust-only action: no love gain, but she appreciates the effort.
- Passionate morning routine (+2 love) — requires love >= 31. Physical intimacy replaces the meal.

### 2. Movie Night
**Video:** angela_white_4 (clips 13–14, 17–28) | **Location:** Living room

| Love | Clips | What Player Sees |
|---|---|---|
| 0–20 | (none) | Text-only: sit on couch, watch movie. She sits close, your legs touch, she laughs at the same parts you do. Tension builds but nothing happens. |
| 21–30 | 13–14 | First physical contact during movie — handjob + passionate kiss. She initiates. Sofa foreplay, thigh kissing. |
| 31–40 | 17–20 | Sex on couch — reclining penetration, oral stimulation of her, straddling/grinding (clip 19 = no visible penetration), cowgirl. The movie is forgotten. |
| 41–50 | 21–28 | Intense — multiple positions on couch. Cowgirl riding, doggy style, anal penetration (clips 22, 25–26), oral (clip 27 includes anal-to-oral), climax. Full sequence. |

### 3. Couch Play (unlocks at love 20)
**Video:** Mofos (clips 6, 8–10) | **Location:** Living room

| Love | Clips | What Player Sees |
|---|---|---|
| 20–30 | — | Text-only. She teases, stretches, watches you watching her. Playful tension. |
| 31–40 | 6, 8 | Couple foreplay and sex on couch — touching, penetration. |
| 41–50 | 9–10 | Afterglow — solo self-touch, then he stimulates her manually. Intimate wind-down. |

> Note: Mofos clips 1, 2, 7 dropped (phone visible in clips 1-2 breaks POV; clip 7 content mismatch).

**Player choices per visit:**
- Be gentle and attentive (+1 love, +1 trust)
- Be passionate (+2 love, +0 trust)

### 4. Angela's Bath (peekable)
**Video:** 480p.h264 (clips 1–16) | **Location:** Bathroom

| Love | Clips | What Player Sees |
|---|---|---|
| 0–10 | 1–2, 15–16 | Entering tub, exiting tub. Brief glimpse — she's just bathing. (Incidental nudity: peek activity, not interactive. Player catches a fleeting moment.) |
| 11–20 | 4–6, 8–10, 14 | Full bathing routine: sitting up, washing with loofah, soaping, scrubbing, relaxing. |
| 21–30 | 3, 12–13 | Breast touching in water, caressing body, intimate self-soothing. |
| 31–40 | 7 | Self-touching lower body with loofah/object. Deliberate self-care becomes self-pleasure. |
| 41–50 | 11 | Genital self-stimulation in tub. Full private moment. |

### 5. Angela's Morning (peekable)
**Video:** 480p.h264 (1) (clips 1–20) | **Location:** Angela's bedroom

| Love | Clips | What Player Sees |
|---|---|---|
| 0–10 | 1–5 | Resting in bed in underwear, walking, grabbing coffee mug, sitting at window. SFW morning. |
| 11–20 | 6, 11 | Removing robe in underwear. Crawling on bed. Suggestive but not explicit. |
| 21–30 | 7–8, 12, 16–20 | Unbuttoning shirt, breasts exposed. Removing shirt. Nude posing — crawling on bed, adjusting pillows, sitting nude, lying prone. She's comfortable in her own skin. |
| 31–40 | 9–10, 14 | Pulling underwear aside, touching groin area. Self-exploration. |
| 41–50 | 13, 15 | Full masturbation — deliberate genital self-stimulation, rhythmic touching. Intense private moment. |

### 6. Morning Together (unlocks at love >= 30, trust >= 25)
**Video:** 480p.h264 (2) (clips 1–20) | **Location:** Bedroom

| Love | Clips | What Player Sees |
|---|---|---|
| 30–35 | 1–3 | Sleeping together, waking, gentle shoulder touch, tender kissing. |
| 36–40 | 4–8, 14, 19–20 | Foreplay — thigh kissing, breast stimulation, oral, mutual touching, straddling, manual stimulation, grinding. |
| 41–45 | 9–13 | Sex — cowgirl, grinding, missionary, multiple positions. Active intimacy. |
| 46–50 | 15–18 | Intense sex — doggy style, anal (clip 17), passionate missionary, deep connection. |

**Player choices per visit:**
- Cuddle and talk (+1 love, +1 trust)
- Initiate intimacy (+2 love, +0 trust)

### 15. Bedroom Play (unlocks at love >= 30, trust >= 25)
**Video:** Mofos (clips 3–5, 11, 12) | **Location:** Bedroom floor

| Love | Clips | What Player Sees |
|---|---|---|
| 30–35 | 3, 12 | Nude posing on rug, talking to camera — playful, confident. She knows he's watching. |
| 36–40 | 4–5 | Oral sex — she kneels on rug and performs blowjob. Direct eye contact with camera. |
| 41–50 | 11 | Solo masturbation on all fours — she's no longer performing for him, this is purely for herself. Most intimate reveal. |

**Player choices per visit:**
- Watch and appreciate (+1 love, +1 trust)
- Encourage and participate (+2 love, +0 trust)

### 16. Deep Conversation (unlocks at love >= 10, trust >= 20)
**Video:** None (text-only) | **Location:** Living room (Evening)

Text-based activity. No video clips. Angela and Jack talk about life, family, dreams, fears. These conversations build both love AND trust — the only activity that does both significantly.

**Player choices per conversation:**
- Listen and ask questions (+3 love, +1 trust)
- Share something personal (+2 love, +2 trust)
- Deflect with humor (+1 love, +0 trust)

> **Design note:** Deep Conversation is the primary trust-building activity beyond rent. It's also where Angela drops hints about gifts she wants (used for the Special Gift mechanic). Hints also appear randomly at Breakfast (love >= 15). One hint per week maximum, across all sources.

---

## Special Activities — Full Arcs

### 11. Date Night Hotel (unlocks at love 40, trust >= 30)
**Video:** ADULT TIME (clips 1–25) | **Location:** Hotel bedroom

The romantic culmination. Angela suggests "somewhere nobody knows us." Full 25-clip arc plays in sequence:
**Cost:** $300. Angela suggests it, Jack pays. The most expensive activity — requires deliberate saving.
- **Arrival** (clips 1–3): Lingerie, anticipation, first kiss at the hotel. Straddling, passionate kissing. No penetration.
- **Undressing** (clips 4–7): Slow removal, tender touches, kissing abdomen and hips, grinding. Building intimacy.
- **First wave** (clips 8–12): Intensity builds — riding/grinding (clip 8), more foreplay (9–10), then oral sex (11–12). First peak of passion.
- **Intimate pause** (clips 13–14): They stop and just look at each other. Lying together, eye contact, quiet tenderness. No sexual activity — just being present.
- **Second wave** (clips 15–20): Oral sex (15), handjob + kissing (16), manual stimulation (17), penetrative sex (18), gentle caressing (19–20). Passion and tenderness interleave.
- **Afterglow & final peak** (clips 21–23): Hand-holding and gentle massage (21–22) give way to one last passionate encounter — full penetrative sex (23). The night's final crescendo.
- **Departure** (clips 24–25): She gazes at him lovingly, then leaves the room. He lies in bed, thinking. Something has changed between them.

**Stat change:** love +8, trust +5

### 12. Spa/Massage (unlocks at love 35, trust >= 28)
**Video:** NewSensations (clips 4–20) | **Location:** Bedroom

Angela sets up a massage session at home — oils, candles, towels on the bed. 17-clip arc:
- **Preparation** (clip 4): Angela fixes her hair at the bathroom mirror
- **Getting ready** (clip 5): She brushes her hair, sets the mood — candles lit
- **Massage** (clips 6–10): Professional-style massage. Oil, rubbing, relaxation.
- **Sensual turn** (clips 11–14): Massage becomes intimate — oil on breasts, genital stimulation, sensual chest touching, shoulder massage. Arousal builds unevenly.
- **Sexual** (clips 15–18): Oral sex, handjob, cowgirl riding, penetration. Full sexual encounter emerges from the massage.
- **Aftercare** (clips 19–20): She massages his back with oil (tender role reversal), then oral sex. The session winds down intimately.

**Stat change:** love +6, trust +4

### 13. Bath Together (unlocks at love 35, trust >= 28)
**Video:** POV Blowjob Bath (clips 1–10) | **Location:** Bathtub

Angela invites Jack to join her bath. Full 10-clip arc:
- **Self-care** (clips 1–2, 4): Angela bathing alone — washing breasts, scrubbing back, applying bath oil. Relaxed, unguarded.
- **Self-pleasure** (clips 3, 5–6): Self-stimulation — breast/clitoral touching, anal self-play with fingers. She's aware he's watching. (Note: clip 3 AI description is erroneous — "lick own erect penis" for female performer; actual content is self-pleasure in tub.)
- **Display** (clips 7–8): She stands near the window — nude posing, back and buttocks on display. Deliberate showing off.
- **Together** (clips 9–10): Oral sex (blowjob) in the bathtub. She takes the lead.

**Stat change:** love +5, trust +3

### 14. Exploring Kink (unlocks at love 45, trust >= 30)
**Video:** Busty Babe Leash (clips 1–14) | **Location:** Floor/mirror → bed

Late-game content. Angela suggests trying something new — BDSM-lite. Full 14-clip arc:
- **Floor/Mirror** (clips 1–4): Pink lingerie, kneeling, leash, oral, crawling near mirror
- **Bed** (clips 5–14): Restrained positions, various sexual acts, collar/leash play, multiple positions

**Stat change:** love +4, trust +2

### Replayability Rules

> **Story events** (7–10): One-time only. Cannot be replayed.
> **Special activities** (11–14): Replayable after first completion.
> - First play: full love/trust gains
> - Replay: 50% love gain, 0 trust gain
> - Same diminishing returns as daily activities apply
> **Daily activities** (1–6, 15, 16): Always available (subject to unlock and diminishing returns)

---

## Story Progression — Full Flow

```mermaid
flowchart TD
    subgraph Act1["Act 1: The New Normal (love 0–10)"]
        A1_arrive["Day 1: Jack Arrives<br/>📍 Apartment<br/>🎬 NewSensations clips 1–3"]
        A1_daily["Daily: Breakfast (SFW clips 1–5)<br/>Bath peek (entering/exiting tub)<br/>Morning peek (resting, coffee)<br/>Movie Night (text only)"]
        A1_towel["Towel Encounter<br/>📍 Bathroom<br/>⚡ love >= 10<br/>🎬 Step Bro clips 4–6"]
    end

    subgraph Act2["Act 2: Growing Closer (love 11–30)"]
        A2_daily["Daily activities escalate:<br/>Breakfast → embracing, kissing<br/>Bath peek → washing routine visible<br/>Morning peek → undressing visible<br/>Movie Night → text until love 21, then sofa foreplay clips"]
        A2_couch["Couch Play unlocks (love 20)<br/>🎬 Mofos clips 6,8–10 (text-only at T1)"]
        A2_bedroom["Bedroom Encounter<br/>📍 Bedroom<br/>⚡ love >= 25<br/>🎬 Step Bro clips 7–17"]
        A2_moment["Bedroom Moment<br/>📍 Bedroom<br/>⚡ love >= 30<br/>🎬 AW4 clips 15–16"]
    end

    subgraph Act3["Act 3: Deep Connection (love 31–50)"]
        A3_morning["Morning Together unlocks (love 30)<br/>🎬 480p.h264(2) clips 1–20"]
        A3_bedplay["Bedroom Play unlocks (love 30)<br/>🎬 Mofos clips 3–5,11,12"]
        A3_spa["Spa/Massage unlocks (love 35)<br/>🎬 NewSensations clips 1–20"]
        A3_bath["Bath Together unlocks (love 35)<br/>🎬 POV Blowjob Bath clips 1–10"]
        A3_hotel["Date Night Hotel unlocks (love 40)<br/>🎬 ADULT TIME clips 1–25"]
        A3_kink["Exploring Kink unlocks (love 45)<br/>🎬 Busty Babe Leash clips 1–14"]
    end

    A1_arrive --> A1_daily
    A1_daily --> A1_towel
    A1_towel --> A2_daily
    A2_daily --> A2_couch
    A2_daily --> A2_bedroom
    A2_bedroom --> A2_moment
    A2_moment --> A3_morning
    A2_moment --> A3_bedplay
    A3_morning --> A3_spa
    A3_morning --> A3_bath
    A3_spa --> A3_hotel
    A3_bath --> A3_hotel
    A3_hotel --> A3_kink
```

> **Note:** Arrows show progression order (stat thresholds are reached in this sequence), not flag dependencies. Each activity/event is independently gated by its own love/trust requirements.

---

## Daily Schedule

| Time Slot | Activity Options |
|---|---|
| **Morning** | Breakfast/Kitchen, Angela's Morning (peek), Cafe (morning shift) |
| **Afternoon** | Cafe (afternoon shift), Couch Play, Bedroom Play, Spa/Massage |
| **Evening** | Movie Night, Angela's Bath (peek), Deep Conversation, Date Night Hotel |
| **Night** | Morning Together, Bath Together, Exploring Kink |

> **Morning:** Player picks Breakfast (interact) OR Morning peek (observe). Can't do both.
> **Night:** "Morning Together" stays here — they go to bed together and wake up together, so the activity spans night-to-morning.
> **Evening:** Bath peek moves here — she bathes in the evening. Deep Conversation becomes available at love >= 10, trust >= 20. Replaces Movie Night for that slot (can't do both in one evening).
> **Cafe shifts:** Morning shift ($70) means skipping breakfast with Angela — a direct trade-off between money and love. Afternoon shift ($70) replaces what was previously just "Work." Double shift (morning + afternoon) pays $140 but sacrifices two Angela time slots. Maximum 2 shifts per day.
> **Afternoon slot:** Before love 20, only Cafe is available. The player can skip the slot (free time, no stat change) or work. After Couch Play unlocks, the afternoon becomes a meaningful choice.
> **Night slot:** Empty before love 30 (no unlocked activities). The player effectively has 3 actions/day until Morning Together unlocks. This is intentional — nighttime intimacy must be earned.
> **Skipping:** Any time slot can be skipped (free time, no stat change). This is the default for slots with no unlocked activities.

## Player Actions Per Day

> Player gets **4 actions per day** (one per time slot: morning, afternoon, evening, night).
> Cafe shift: $70. Rent: $200/week.
> Rent due every 7 days (Day 7, 14, 21, 28). First rent due Day 7. Paid on time: trust +2. Paid early (before Day 6): bonus trust +1. Missed: trust -3.
> 3 shifts/week barely covers rent ($210). 4 shifts = $80 savings. Leaves 24–25 of 28 weekly slots for Angela.
> Special activities cost money: Date Night Hotel $300. Spa/Massage, Bath Together, and Exploring Kink are free (at home).
> Saving for Date Night Hotel at love 40 means ~4 extra shifts — that's 4 mornings or afternoons NOT spent with Angela.

### Game Length

> The game runs for **30 days**. Endings are evaluated at the end of Day 30 based on final love and trust values.
> - 4 rent cycles (Day 7, 14, 21, 28)
> - True Love is achievable by ~Day 30 with optimal play
> - The game can also end early if trust hits 0 (Kicked Out)

### The Cafe

Jack works at a neighborhood cafe. Text-only — no video clips. The cafe exists to create economic pressure, not as a location with its own content.

| Detail | Value |
|---|---|
| **Pay** | $70 per shift |
| **Available slots** | Morning, Afternoon (max 2 shifts/day) |
| **Morning trade-off** | Skips Breakfast/Kitchen — loses love-gain opportunity |
| **Afternoon trade-off** | Skips Couch Play, Bedroom Play, or Spa |
| **Tips** | None. Flat rate. Predictable income for planning. |

> **Economy feel:** At 3 shifts/week (rent minimum), Jack has $10 left over. Every flower ($30), gift ($150), or special date ($300) requires extra shifts — each one a missed Angela interaction. The player must budget time against money against love.

### Money Talk Events

Text-only events triggered by economic conditions. No video clips.

| Event | Trigger | What Happens | Stat Effect |
|---|---|---|---|
| **"You've been working a lot"** | 5+ shifts in one week | Angela: "I appreciate how hard you work... but I miss having you around." She makes him dinner. | trust +2 |
| **"I want to take you somewhere"** | Player-initiated (requires $100+ saved beyond rent) | Jack tells Angela he's saving for something special. She's intrigued. Must spend $100+ on her within 2 weeks (flowers, gifts, or Date Night Hotel all count). | love +1 now. If fulfilled: love +2 bonus. If broken: love -2 |
| **"About the rent..."** | Rent day (weekly) | If player does Breakfast: Angela brings up rent. Tone depends on payment history. If player skips Breakfast (cafe shift): rent is still due — Angela leaves a note on the counter. | (covered by existing rent trust rules) |

### Love Gain Sources

| Action | Love Gain | Notes |
|---|---|---|
| Eat breakfast together | +1 | Always available |
| Help cook breakfast | +2 | Requires love >= 5 |
| Compliment her food | +1 | Always available |
| Passionate morning routine | +2 | Requires love >= 31. Breakfast physical intimacy. |
| Peek at her (Bath/Morning) | +1 | Available daily. Risk of being caught. |
| Bring her flowers | +2 | Costs $30 |
| Deep conversation | +1 to +3 | Requires trust >= 20. Gain depends on player choice. |
| Special gift (thing she mentioned) | +5 | Costs $150. She mentions wants during Deep Conversation (trust >= 20) or randomly at Breakfast (love >= 15). One hint per week. |
| Story events | +3 to +5 | Auto-triggered at love thresholds |
| Movie Night (watch together) | +1 | Text-only phase (love 0–20). Sit close, share popcorn. |
| Movie Night (suggest her favorite) | +1 | Text-only phase. She's surprised you remembered. |
| Movie Night (video tiers) | +2 | Love 21+. Physical intimacy during movie. |
| Couch Play | +2 | Love 20+. Playful intimacy on the couch. |
| Morning Together | +2 | Love 30+. Waking up together. |
| Bedroom Play | +2 | Love 30+. Intimate bedroom moments. |
| Special activities | +4 to +8 | Date Night gives highest |
| "I want to take you somewhere" | +1 (now) / +2 (fulfilled) | Player-initiated. Must spend $100+ on her within 2 weeks. Broken promise: love -2. |

### Trust Gain Sources

| Action | Trust Gain | Notes |
|---|---|---|
| Pay rent on time | +2 | Weekly. Due every 7 days |
| Pay rent early (before day 6) | +1 | Bonus on top of the +2 for paying on time |
| Cook for her (Breakfast) | +1 | Requires love >= 5. Trust-only — no love gain. |
| Honest when caught peeking | +2 | Random event if caught during Bath/Morning peek |
| Respect her "not tonight" | +2 | When she declines intimacy, accept gracefully |
| Deep conversation | +1 to +2 | Gain depends on player choice. Listen: +1, Share personal: +2, Deflect: +0. |
| Help with chores | +1 | Available daily |
| Morning Together | +1 | Sleeping together builds trust naturally |
| Couch Play (gentle and attentive) | +1 | Being attentive during intimacy |
| Bedroom Play (watch and appreciate) | +1 | Being respectful during her intimate moments |
| "You've been working a lot" | +2 | 5+ shifts in one week (Money Talk event) |
| Story events | +2 to +3 | Auto from milestones |
| Date Night Hotel | +5 | Special activity (love 40+) |
| Spa/Massage | +4 | Special activity (love 35+) |
| Bath Together | +3 | Special activity (love 35+) |
| Exploring Kink | +2 | Special activity (love 45+) |

### Trust Loss Sources

| Action | Trust Loss | Notes |
|---|---|---|
| Miss rent | -3 | Weekly check |
| Caught peeking (deny it) | -3 | Random event |
| Push when she says no | -4 | If player insists after "not tonight" |
| Aggressive dialogue choice | -2 | Various story moments |

> **Peek detection:** 15% chance of being caught each time you peek (Bath or Morning). If caught, player chooses: admit honestly (+2 trust) or deny (-3 trust). Detection chance drops to 5% at love >= 20 (she's more comfortable with your presence). Maximum once per week — after being caught, she's alert and you can't peek for 3 days.

> **"Not tonight" events:** When starting a couple activity (Couch Play, Morning Together, Bedroom Play) there's a chance Angela declines based on trust gap. If trust < (love ÷ 2), she says "not tonight." Player choice: respect it (+2 trust) or push (-4 trust). At trust >= 30, she never declines.

### Diminishing Returns

> **Same action repeated:** 100% → 75% → 50% → 0% stat effect
> Resets after 2 days of NOT doing that action.
> Forces the player to vary their approach.
>
> **Rounding:** Gains always round up (ceiling). A +1 action at 75% yields 1, at 50% yields 1, at 0% yields 0. A +2 action at 75% yields 2, at 50% yields 1, at 0% yields 0. This ensures low-gain actions remain worthwhile until fully exhausted.
>
> **Different choices within the same activity count as separate actions.** Within Breakfast: "Eat together" (+1), "Help cook" (+2), and "Compliment food" (+1) each have independent diminishing return timers. The player exhausts a specific choice, not the entire activity.
>
> At love 0–10, available unique choices across all activities:
> - Breakfast: 3 choices (eat, cook, compliment)
> - Bath peek: 1 choice (peek)
> - Morning peek: 1 choice (peek)
> - Movie Night: 2 choices (watch together, suggest movie)
> - Bring flowers: 1 choice (costs $30)
> Total: 8 unique love-gaining actions. Enough for 2–3 full days before needing to rotate.
>
> **Flowers, gifts, and chores** are choices within existing activities, not separate time-slot actions:
> - **Bring flowers** ($30): Choice available during Breakfast or when returning home. "I picked these up on the way back."
> - **Special gift** ($150): Choice available during Deep Conversation after Angela hints at something she wants. One hint per week.
> - **Help with chores**: Choice available during Breakfast/Kitchen. "Let me clean up" instead of eating together.
> These don't consume an extra time slot — they replace a choice within an activity you're already doing.

---

## Endings

> Endings are evaluated in priority order — first match wins.

| Priority | Ending | Condition | Description |
|---|---|---|---|
| 1 | **Kicked Out** | trust = 0 | Trust hit zero. Angela asks Jack to leave. Game over. |
| 2 | **True Love** | love >= 50, trust >= 38 | Angela and Jack become a real couple. Date Night Hotel is the culminating scene. Open, honest, committed. |
| 3 | **Close Bond** | love >= 35, trust >= 25 | Deep connection but not fully committed. They care deeply but haven't taken the final step. |
| 4 | **Bittersweet** | love >= 35, trust < 25 | Physical intimacy without emotional safety. Angela enjoys being with Jack but can't fully let her guard down — too many missed rents, broken promises, or pushed boundaries. They part with mixed feelings about what could have been. |
| 5 | **Friendly** | love >= 15 | Friendly housemates with unresolved tension. Some good memories but nothing lasting. |
| 6 | **Distant** | (default) | Jack never connected with Angela. He moves out. |

### Ending Reachability

- **True Love:** Requires consistent daily engagement across all activities. Player must reach Date Night Hotel (love 40) and continue building to 50. Achievable by ~Day 30 with optimal play.
- **Close Bond:** Natural outcome for players who engage regularly but don't maximize every interaction. ~Day 20-25.
- **Friendly:** Player who works too much, skips breakfasts, or doesn't pursue deeper activities.
- **Distant:** Player who actively avoids Angela or fails to engage.
- **Bittersweet:** Player who built physical intimacy (love 35+) but neglected trust — missed rent, denied peeking, or pushed boundaries. At very low trust (below love ÷ 2), the "not tonight" mechanic adds friction. At trust 20–24, activities still proceed but the relationship lacks emotional depth.
- **Kicked Out:** Player who repeatedly violates trust (missed rent, aggressive actions, snooping caught).

---

## Validation Checklist

| # | Check | Status | Notes |
|---|---|---|---|
| 1 | **Every clip assigned** | ✅ | 176 clips across 16 activities (Deep Conversation is text-only). Step Bro clips 1–3 dropped (3 unassigned). |
| 2 | **NSFW isolation** | ✅ | Each activity's NSFW content comes from exactly 1 video file. |
| 3 | **Sequence preserved** | ✅ | Couple/narrative clips play in original order. Solo peekable activities (Bath, Morning) organize by content intensity — independent vignettes, not continuous narrative. |
| 4 | **SFW at low love** | ✅ | All daily activities have SFW content at love 0–10 (Movie Night uses text-only). |
| 5 | **Unlock progression** | ✅ | Activities unlock gradually: love 0 → 10 → 20 → 25 → 30 → 35 → 40 → 45. |
| 6 | **All endings reachable** | ✅ | 6 endings, priority-ordered. True Love requires ~Day 30. Bittersweet from high love + low trust. Distant is default. Kicked Out from trust=0. All (love, trust) combinations covered. |
| 7 | **No dead zones** | ✅ | Every love bracket has content. Player always has something to do. |
| 8 | **Angela has agency** | ✅ | Story events are milestones SHE participates in. Bath/Morning are HER private moments player observes. She initiates intimacy at key moments. |

---

## Clip Count Verification

| # | Activity | Video Source | Clips | Count |
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

> angela_white_4 total: 12 + 14 + 2 = 28 ✅
> Step Bro total: 3 + 11 = 14 ✅ (clips 1–3 dropped, now used by NewSensations for Jack Arrives)
> NewSensations total: 3 (Jack Arrives) + 17 (Spa/Massage) = 20 ✅
> Mofos total: 4 + 5 = 9 ✅ (clips 1, 2, 7 dropped — phone/content mismatch)
> All other videos: single activity each ✅
