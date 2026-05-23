# 32 — TLS World Setup (Slice)

> **Status:** E2 deliverable per doc 30 §8 Phase 1. Defines the slice narrative frame: why Maya is at Frank's, what the 10 days look like, how the economic engine drives the player, what each NPC's first-meeting feels like. Future authors read this for "what is the slice TELLING the player."
>
> **Date:** 2026-05-16
> **Inputs:** doc 30 §4.1 (premise + economic engine), §8.2 (NPC contracts), `10_Test_Slice_10Day_Plan.md`, current TOML `7_final_game.toml` intro canvas + rent state.
>
> **Length:** ~3 pages.

---

## §1 Premise — Why Maya is at Frank's

**Setting:** Rural Southern small town. Late summer. The kind of place where Route 9 runs past the property and trucks change gears at the curve. Frank's house sits on a few acres outside town — kitchen garden, back yard running to a treeline, a toolshed, a back porch where you can hear cicadas at dusk.

**Maya's situation:** She's renting Frank's spare room for the summer. 90-day lease. She came from the city to escape something — bad breakup, family drama, a life she walked away from. The slice doesn't dwell on the backstory. She's here. The room is cheap. That's enough for now.

**Who else is in the house:**
- **Frank** — the landlord. Older man. His house, his rules.
- **Diana** — Frank's wife. Maya's mother. Strict. Religious. Holds dinner at 6:30. The reason rent is $60/day cash, not on a card.
- **Jake** — Maya's actual brother. Visiting for the summer too. Stays in the next room. Thin walls.

**Who else Maya meets in town:**
- **Ryan** — works at the gas station on Main Street. Helps Frank with yard work some afternoons. Maya's age. Wholesome.
- **Marge** — owns the diner on Main. Always hiring. Has opinions.
- **Cookie** — the cook at Marge's diner. Maya's age. Quiet, watches.

**The slice (Phase 1) covers Days 1-10** of Maya's 90-day stay. By Day 10 she's met everyone, started building stats, possibly hit the catch capstone with Frank, paid first week's rent. The slice ends. The wider 80-day game (Phase 3+) continues from there.

Cross-reference: doc 30 §4.1.

---

## §2 Economic engine — the player's drive

**Rent mechanics (as wired in current TOML — verified per audit):**

| Field | Value |
|---|---|
| Rate | $60/day (slice tuning — Phase 2 may revise to monthly per doc 30 §4.1) |
| Payment cycle | Weekly — due Sunday morning |
| Week 1 total due | $420 ($60 × 7 days) |
| Eviction gate | Sunday Day 7 — fail to pay = game over |
| Maya starts with | $80 (per existing TOML) |
| Day 1 deficit | Need $340 more by Sunday |

**The player loop:** Maya wakes Monday morning with $80. Rent is $420 due Sunday. She has 6 game-days to find $340. This forces her to:
- Work at the diner (Marge's hiring)
- Help Frank with bookkeeping (he pays cash)
- Help Frank with yard work (Ryan does this paid; Maya can join)
- Eventually — corrupt Frank into "letting her slide" on rent
- Or take other paths (Phase 3+ adds more options)

**Why this matters:** Per doc 30 §3 pattern G ("state compounds"), the rent quest is what FORCES Maya into proximity with the NPCs. Without economic pressure, players treat the game as a pure sandbox and never engage with the corruption arcs. Rent pressure = "you must talk to Frank / Marge / Ryan if you want to survive Day 7."

**Slice success ≠ surviving Day 7.** Phase 1 is exploration scope. Player can hit eviction and replay. Phase 2 onward, eviction is meaningful loss.

---

## §3 Time + day model

**Per doc 30 open Q #2 resolution:** KEEP 24-hour clock for slice (existing system). Phase 2 may migrate to 6-band model.

**Current state (as wired):**
- 24-hour clock, sleep advances day
- Days run Monday → Sunday (week 1) → Monday (start of week 2 if surviving) → ... Day 10 = Wednesday week 2
- Slice = Days 1-10 (10 in-game days, Mon-Wed)
- Sunday Day 7 = first rent check (the slice's only hard gate)

**Day rollover:**
- Maya sleeps → time advances to next day's EM band (~05:00-06:00)
- Day-rollover hook clears `*_today` flags (per audit) — `talked_to_ryan_today`, `walked_past_jakes_today`, etc.
- Lane 2 ambient `max_triggers_per_day` counters reset
- Quests advance state where conditional

**Time bands (informal — engine uses raw hours but author intuition uses bands):**

| Band | Hours | Notes |
|---|---|---|
| Early Morning | 05:00-08:30 | Frank in kitchen morning slot |
| Morning | 08:30-12:00 | Maya can go to town / work |
| Afternoon | 12:00-17:00 | Frank in yard 14:00-17:00 |
| Evening | 17:00-21:00 | Frank kitchen dinner 17-19:30, then living room 19:30-21 |
| Night | 21:00-23:00 | Frank winding down in bedroom 21:00-23:00 |
| Late Night | 23:00-05:00 | Frank asleep; ambient surface for Maya solo activities |

---

## §4 Day 1 opening loop — what player sees first

**Existing intro (in current TOML):** `event_test_slice_intro` — Maya wakes Monday EM in her bedroom. First node "Wake." Body text already RTS-flat per audit. KEEP existing intro; don't rewrite.

**Sidebar visible from Day 1:**
- Stats: Corruption (0) / Arousal / Energy / Money ($80)
- Quests: 3 active per doc 30 §8 E7 deliverable —
  - "Pay rent by Day 7 — $420 due Sunday"
  - "Settle in (meet your housemates: Frank / Diana / Jake)"
  - "First Sunday at church (with Diana)"
- NPC roster: Frank / Diana / Jake / Ryan / Marge / Cookie (with current locations)
- Time/day: Monday Day 1, 06:00

**First decision (after intro auto-advance):** Maya is in her bedroom. Options visible:
- Get dressed (wardrobe — once outfit system surfaces in slice)
- Sketch (existing Maya-solo activity)
- Leave Maya's bedroom → hallway → explore house / town

**First NPC encounter (most likely path):**
- Maya leaves bedroom → hallway → walks to kitchen
- Time is 06:00 EM Monday — Frank scheduled in kitchen morning slot (05:30-09:00) per doc 30 §4.4 + existing schedule
- Diana also scheduled at kitchen mornings (existing TOML — overlap with Frank)
- Random encounter dice rolls on entry (Lane 2 ambient or hub render or Diana scene)

**Tutorial overlays (informal — first-time gameplay hints):**
- "Each action takes time. Sleep advances day. Watch your money."
- "Visit NPCs at their scheduled locations to interact."
- "Rent is due Sunday — don't forget to find work."
- "Your sidebar shows where everyone is right now."

---

## §5 6 NPC first-meet framing

One paragraph per NPC describing the texture of Maya's FIRST meeting in slice. Authors use this for first-encounter scene framing (and walkthrough hint copy in Phase 2+).

### Frank (landlord, 50s)

Maya meets Frank in the kitchen the morning of Day 1 — she comes downstairs, he's at the counter with his coffee, paper folded next to him. He looks up. Says "Coffee's ready." Doesn't introduce himself; assumes she knows. The exchange is 4-5 lines max. Frank asks if she eats breakfast (= "do you want some"). Maya answers. He nods. End of scene. The texture is: **terse, transactional, watchful.** He's noticed her. He's not friendly. He's not unfriendly. He's just *present* and reserved.

### Diana (mother, 40s)

Maya meets Diana in the kitchen too — Diana at the stove, Frank at the counter. Diana doesn't turn around when Maya comes in. Says: "Eggs in the pan. Help yourself." Diana is Maya's actual mother, but the relationship is strained — religious, rule-bound, judgmental. The texture is: **cold-but-functional.** Diana isn't warm but isn't hostile. She's the one who held the dinner schedule for 30 years and isn't changing it for Maya.

### Jake (brother, 20s)

Maya hears Jake before she sees him — his keyboard tick through the wall as she wakes (existing intro line). She meets him later Day 1 in the hallway or his room. He's sketching. Looks up, says hi, looks back at his sketchbook. The texture is: **easy-familiar.** They're siblings who know each other; no introduction needed. He's quieter than her. Lives in his own world. Doesn't make demands on her.

### Ryan (town neighbor / yard worker, Maya's age)

Maya meets Ryan in the yard or at the gas station. He's helping Frank fix the fence. Sees Maya, takes off his cap, says "Hey, you must be Maya. Frank said." Friendly, straightforward, slightly nervous around her. The texture is: **wholesome, awkward, interested.** He's the town boy who notices the new girl. Ryan is the peer arc — Maya's "wholesome path" alternative to the family corruption.

### Marge (diner owner, 50s)

Maya meets Marge if she walks to town Day 1 — Main Street → Diner. Marge is behind the counter, hands flour-dusted. Sizes Maya up immediately: "You the one staying out at Frank's place? Diana's girl?" Half-statement, half-test. If Maya asks about work, Marge nods at the back: "Cookie's been short-handed. Talk to her." The texture is: **knows everyone, holds court, sees through bullshit.** Marge is the matriarch of the diner; getting hired is meeting her standard.

### Cookie (diner cook, Maya's age)

Cookie is back in the diner kitchen — short black hair, apron, tattoos peeking out from sleeves. Looks up when Maya comes in. Doesn't smile. "You here for the job?" Doesn't make small talk. The texture is: **quiet, watchful, slightly closed-off.** Cookie reads as "not from around here either." She sees Maya and recognizes another outsider. The slow-burn lesbian arc starts here, though slice Phase 1 only delivers the first-meet — actual content is Phase 3+.

---

## §6 Slice-end state (Day 10 target)

What the slice should deliver by Day 10:

| State | Target by Day 10 |
|---|---|
| Maya money | Survived Day 7 rent OR evicted (game over) |
| Maya corruption | 5-30 (likely) — depending on play patterns |
| Frank.arousal | 5-15 |
| Frank capstone progress | Catch likely fired (corr 25 + Frank.arousal threshold). Cracked may have fired. First-night possible if player pushed hard. |
| Diana awareness | 0-5 (unless very risky play) |
| Jake — first walk-in | possible (one-time event in his room) |
| Ryan — first conversation | met, possible 1 quest beat |
| Marge / Cookie — diner job | hired possibly, 1-2 work shifts done |
| Quest journal | "Pay rent by Day 7" → completed (or game-over). "Settle in" → completed (met housemates). "First Sunday at church" → completed |

**Slice "complete" doesn't mean "all content seen."** It means: player has experienced one playthrough of the 10 days, met everyone, found the major mechanics, hit at least one capstone with Frank. Replay value is part of the slice — different choices lead to different outcomes by Day 10.

---

## §7 Out of scope for slice (deferred)

Things the slice does NOT deliver (per doc 30 §2 + §8):

- Pregnancy mechanic (Phase 2+)
- Walkthrough panel UI (Phase 2)
- Gallery + achievements (Phase 2+)
- Scandal as global score (Phase 2 — current slice keeps `diana_awareness`)
- Outfit gating beyond basic (Phase 2+)
- AnonStream career arc (Phase 3+)
- Diana confrontation branches 2 + 3 (Phase 2 — slice ships 1 + 4 only)
- Day 11+ content (Phase 3+)
- Image / video media (placeholders OK in Phase 1)

---

## §8 Cross-references

| Doc | Purpose |
|---|---|
| `30_TLS_Test_Redesign_PRD.md` §4.1 | Premise + economic engine spec |
| `30_TLS_Test_Redesign_PRD.md` §8.2 | Per-NPC minimum contract |
| `31_Frank_Arc_Design_Brief.md` | Frank-specific design (this doc deliberately doesn't repeat Frank's depth) |
| `10_Test_Slice_10Day_Plan.md` | Original slice design (kept for context — doc 32 supersedes for narrative frame) |
| `13_Road_to_Success_Reference.md` §10 | RTS stat economy + bootstrap experience reference |
| Current `7_final_game.toml` | Existing intro canvas + rent state + schedule — this doc documents what's there, doesn't redesign |

---

## §9 E2 acceptance criteria (E2R checkpoint)

User reads §1 + §2 + §4 + §5 within 24 hours of E2 ship. Validates:

- [ ] **§1** premise paragraph names the world clearly (rural South + 90-day rental + step-family situation + Maya's vague backstory)
- [ ] **§2** economic engine clear — rent mechanics + Maya's deficit + how rent forces NPC engagement
- [ ] **§4** Day 1 opening loop concrete — what player sees + sidebar quests + first decisions
- [ ] **§5** 6 NPC first-meet paragraphs each capture the TEXTURE of meeting that NPC (not just facts)
- [ ] **§6** slice-end state realistic — Day 10 targets achievable
- [ ] No drift into authoring scene PROSE
- [ ] Length 2-4 pages — verify

**Pass/fail:** all checkboxes pass → E3 starts (Frank Lane 1 rewrite — first TOML editing). Any unchecked → rewrite section, second checkpoint.

**User time estimate:** ~10-15 min for E2R review.

---

**End of TLS World Setup (Slice).** Author handoff to E3 (Frank Lane 1 rewrite) on E2R pass.
