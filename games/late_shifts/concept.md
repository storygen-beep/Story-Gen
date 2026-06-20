# Late Shifts — Design Book

**Scope mode:** full_game
**Author:** ENI (Stage 1 authoring)
**Authority:** Designed per `prompts_v2/` doctrine (Doc 66 corpus, complete).
**Status:** Stage 1 output — consumed by `stages/02_toml_generation_prompt.md` for TOML emission.
**Game slug:** `late_shifts`
**Cast:** 5 NPCs — family/ambient + slow-burn family + peer/dating + service + antagonist/witness
**Phase 2+ inclusions:** pregnancy=include, scandal=include (5th NPC: Pam Dockery, apartment neighbor), gallery=include, tracker=include

---

## §1 World Setup

### Premise

Maya is 22 and back in the hometown she left four years ago for grad school, trailing the wreckage of a failed PhD application and a worse breakup. She's in her older brother Ben's apartment because she has nowhere else to go. Ben works construction. He's quiet about it — he didn't ask questions when she called, just said he'd move the boxes out of the second bedroom.

The economic logic is immediate: she needs rent money. The diner two blocks away is hiring nights. The owner — Hank — interviews her across the counter in five minutes and tells her to come back Thursday. She gets home at 7am. Ben is leaving for work. They pass in the kitchen like two people in a place they're both still figuring out.

The diner is called Mel's (after Hank's late wife). It's been there since 1987. Hank built it with Mel. He runs it the way some men run a house — like it belongs to him in some molecular sense, and everyone inside it answers to that fact. Night shift is quiet. The cook, Cole, barely speaks. The head waitress, Rosa, has worked evening/night overlap for eleven years and knows where everything is. Maya gets trained in two days and thrown in by Day 3.

The play loop: work shifts to make rent, escalate each NPC's arc through Lane 1 interactions on location, watch the ambient world around her (Lane 2/3) carry the escalation forward in ways she didn't initiate.

### Player character

- **Name:** Maya
- **Age:** 22
- **Background:** Dropped out of a linguistics PhD program. Home is temporary, or so she tells herself.
- **Agency:** Player drives the corruption ladder via Lane 1 choices + shift attendance. Lane 2/3 + capstones gate on stat thresholds + flags.

### Economic engine

- **Rent:** $500/month, paid as $125/week, due Fridays, 1 grace period
- **Starting money:** $60
- **First income source:** Mel's Diner — $40/shift + tips (~$20–30/shift in tips); ~4 shifts/week = ~$240–280/week. Rent is makeable with full attendance.
- **Income dependency:** Maya must be hired (Hank's hire capstone, Day 1–2) before first Friday. Hank provides the job and therefore the economic lever.

### Phase 2+ inclusions (resolved at §0.5.2 Q&A)

| Decision | Call | Engine entry point / scope impact |
|---|---|---|
| Pregnancy | Include | Hank and Ben sex-eligible canvases ship bareback from first explicit beat; pregnancy stat on Maya; Tier-5 breeding-talk vocabulary at Hank Stage 4+ and Ben Stage 4+; parallel pregnant-variant canvases at sex-loop level for both NPCs. All sex scenes ship bareback regardless (Doc 30 §7.3.1). |
| Scandal arc | Include — 5th NPC: Pam Dockery (apartment neighbor) | Pam accumulates awareness 0–100 from Ben arc beats (thin walls, building encounters, late-night crossovers); confrontation capstone Type B Pattern F at awareness ≥ 75; branches: Maya-manages-Pam vs Pam-escalates-to-Ben. |
| Gallery | Include | 5 NPCs at full_game depth → 15 once-only capstones estimated; gallery tab ships; each once-only capstone gets thumbnail ID + scene title + replay button. |
| Tracker | Include | `guide` field on every canvas per Doc 62 PRD; WalkthroughV2 panel shows per-NPC progress; Stage 2 authors `guide` strings during TOML emission. |

### Time model

24h clock. Mel's is a 24-hour diner. Shifts are clock-specific (Maya's night shift 22:00–07:00). Ben's construction schedule is fixed (06:00–17:30 weekdays). Clock model makes scheduling constraints legible.

---

## §2 NPC Roster (5 NPCs)

| NPC | Arc shape | Full-arc depth | Fantasy (1 line) | Vocab ceiling |
|---|---|---|---|---|
| Hank (58) | Family/ambient | 25–32 canvases (L1 4 hubs + L2 6–8 ambients + L3 5–7 subs + 5 capstones) | The diner owner who took her in takes everything else | FULL EMPLOYER-AUTHORITY + AGE-GAP + BAREBACK + BREEDING TALK (Phase 2+ Tier 5) |
| Ben (28) | Slow-burn family | 10–14 canvases (L1 2–3 + L2 2 + L3 2–3 + 3–4 capstones) | Her protective older brother crosses the line he spent 4 years holding | FULL INCEST CALLOUTS at all tiers post-Stage 2 |
| Cole (27) | Peer/dating | 8–11 canvases (L1 2–3 + L2 1–2 + L3=0 + 4 capstones) | The night-shift cook who barely talks takes Maya home in the gray hours | FULL EXPLICIT SEX at Stage 3+; MAXIMUM CRUDE DETAIL anatomical |
| Rosa (43) | Service | 6–9 canvases (L1 hub + 4 locked-visible Phase 3+ stubs + L2=0 + L3=0 + 2 capstones) | The married head waitress who trained her | FULL ADULTERY FRAMING (Phase 3+ deferred — ceiling declared, content held) |
| Pam Dockery (56) | Antagonist/witness | 4–7 standalone + cross-appearances in Ben's lanes | The apartment neighbor who has been listening through the wall | Witness only — no sexual kink ceiling; confrontation IS the event |

**Shape mix:** family/ambient + slow-burn family + peer/dating + service + antagonist/witness. All 5 shapes covered. Per P4 — no repeated tempo rhythms.

**Total estimated canvas count:** ~53–73 across cast (Hank 25–32 dominant; Ben 10–14; Cole 8–11; Rosa 6–9; Pam 4–7).

---

## §3 Locations

### Home hub (Maya + Ben's apartment building)

- `loc_apartment_hallway` (container — parent of apartment locations)
- `loc_mayas_room`
- `loc_bens_room`
- `loc_shared_kitchen`
- `loc_living_room`
- `loc_bathroom`
- `loc_laundry_room` (building laundry, down the hall — Pam's primary territory)
- `loc_building_front` (front steps + building entrance)

### Town hub

- `loc_main_street` (container)
- `loc_diner_front` (Mel's dining floor — Hank's and Rosa's primary territory)
- `loc_diner_back` (kitchen — Cole's territory)
- `loc_diner_office` (Hank's back office — unlocks post-`hank_first_contact`)
- `loc_town_park` (outdoor town; Cole dating-chain)
- `loc_cole_apartment` (Cole's place — unlocks post-`cole_date_done`)
- `loc_convenience_store` (errands)

### Per-NPC schedules

**Hank:**

| Days | Time | Location | Activity |
|---|---|---|---|
| 0–6 | 06:00–09:00 | loc_diner_front | Morning setup |
| 0–6 | 09:00–17:00 | loc_diner_front / loc_diner_office | Day management |
| 0–6 | 17:00–22:00 | loc_diner_front | Evening peak |
| 0–4 (weekdays) | 22:00–01:30 | loc_diner_front | Stays late; keeps floor during Maya's shift |
| 5–6 (weekend) | 22:00–00:00 | loc_diner_front | Shorter stay |
| 0–4 | 01:30–06:00 | loc_diner_office | Dozing / paperwork |

*(Hank is present during Maya's entire 22:00–07:00 shift on weekdays. The 22:00–01:30 window is the Lane 1/2/3 surface.)*

**Ben:**

| Days | Time | Location | Activity |
|---|---|---|---|
| 0–4 (weekdays) | 05:30–06:30 | loc_shared_kitchen | Morning prep |
| 0–4 | 06:30–17:30 | off-location (construction site) | Work |
| 0–4 | 17:30–23:00 | loc_bens_room or loc_living_room | Home |
| 0–4 | 23:00–05:30 | loc_bens_room | Asleep |
| 5–6 (weekend) | 09:00–20:00 | loc_living_room or loc_building_front | Free time |
| 5–6 | 20:00–06:00 | loc_bens_room | Asleep |

*(Ben home evenings; Maya works 22:00–07:00. Key crossover: 05:30–06:30 when Ben wakes and Maya arrives home from shift. Weekend overlap: Ben free when Maya awake by early afternoon after sleep.)*

**Cole:**

| Days | Time | Location | Activity |
|---|---|---|---|
| 0–6 | 07:00–14:00 | off-location (sleeping) | Sleep |
| 0–6 | 14:00–21:00 | off-location / loc_town_park | Personal time |
| 0–6 | 21:00–22:00 | loc_diner_back | Pre-shift prep |
| 0–6 | 22:00–07:00 | loc_diner_back | On shift (same as Maya) |

**Rosa:**

| Days | Time | Location | Activity |
|---|---|---|---|
| 0–4 (weekdays) | 17:00–01:00 | loc_diner_front | Evening + early-night shift |
| 5–6 (weekend) | 10:00–18:00 | loc_diner_front | Day shift |
| Other hours | off-location | — | Home (school runs, family) |

*(Rosa's shift overlaps Maya's 22:00–07:00 start; she trains Maya during the 22:00–01:00 window, then leaves. She is NOT present during the 01:00–07:00 deep-night hours — that window is Hank + Cole only.)*

**Pam Dockery:**

| Days | Time | Location | Activity |
|---|---|---|---|
| 0–6 | 06:00–09:00 | loc_laundry_room or loc_building_front | Morning routine |
| 0–6 | 09:00–17:00 | loc_pam_apartment (off-location, home) | Home (thin walls) |
| 0–6 | 17:00–21:00 | loc_building_front or loc_apartment_hallway | Evening errands |
| 0–6 | 21:00–06:00 | loc_pam_apartment (off-location) | Home |

---

## §4 Per-NPC Design Briefs

---

### §4.1 — Hank brief (Family/Ambient)

**Scope mode:** full_game

#### §4.1.1 End-state fantasy

**Hank claims Maya as his — in his diner, in his back office, in his settled understanding that this is what the building has been moving toward since Mel died.**

Hank is 58, widowed six years, and runs Mel's like a monument to what he had. Maya walks in and he hires her in five minutes because she has her chin up and doesn't look sorry about anything — the way Mel used to look. He doesn't say that. He barely says anything. But he notices. The diner is his house; inside it, Maya answers to him. The arc moves from authority-coded proximity → first late-night disclosure → first physical contact in the kitchen → declared possession in the back office → routine intimate ownership.

**Specific signature scenes:**

- Hank at the counter at 2am in an empty diner, coffee going cold, telling Maya one thing about Mel he's never told anyone
- First time he puts his hand on Maya's waist in the kitchen — not a stumble, the way someone does something they've already decided
- After-close in the back office: Hank locks the front door and tells Maya to stay
- Hank takes Maya from behind over the prep counter; quiet; employer-to-employee authority register throughout
- Bareback routine established; breeding-talk vocabulary (Phase 2+): Hank makes no move to stop; "I'm going to put a baby in you" unlocked at Tier 5

#### §4.1.2 Hank voice spec

**Background:** Built Mel's in 1987 with his wife. Mel died of cancer in 2020. He stayed because the diner is what's left. Functions as boss, older man, and de facto institution. Not warm. Notices things.

**Speech patterns:**

| Pattern | Rule | Example |
|---|---|---|
| Sentence length | 3–6 words; complete thought, no padding | "Took the order out?" / "Counter's wet." |
| No warmth-bombs | Validation is presence, not praise | wrong: "You're doing great" / right: "You'll be fine." |
| Authority-coded observations | Observes and states; doesn't ask permission | "You missed Table 4." / "Leave the back hall light on." |
| Rarely names Maya | Address by role or implication | "You." / "Go." / "Tell him it's forty." |
| Short directives > long explanations | One instruction; if you don't follow, he notices | "Don't let the ice machine cycle after midnight." |
| Emotion via displacement | Addresses the physical, not the thing itself | (wants her to stay) → "Coffee's been sitting too long." |
| No apology in words | Correction is the apology | — |

**Voice samples per stage:**

| Stage | Sample line | Tone |
|---|---|---|
| Stage 0 (authority-baseline) | "Get the rag. Counter needs it." | Boss-neutral; evaluation mode |
| Stage 1 (noticing) | "Mel used to know the regular's order by their coat." | First disclosure; flat delivery |
| Stage 2 (first contact) | "I know." (after Maya realizes he's watching her) | Acknowledgment that removes the pretense |
| Stage 3 (explicit) | "Good girl. Stay." | Authority register bleeds into sex |
| Stage 4 (ownership) | "You work here. You stay here. That's how it goes." | Possessive declaration |
| Stage 5 (routine) | "Come in through the back from now on." | The arrangement is infrastructure |

**Hank-specific framing rules:**

- **Employer-authority register** is in place from Stage 0. He owns the space Maya works in; his authority is the kink from Day 1. The frame is NOT "daddy" (no biological family coding); it's "the man who decides what happens in this room."
- At **Stage 3+**, authority register merges with physical possession: "good girl" / "stay" / "take it" — imperative, employer-coded, minimal excess.
- At **Stage 4+**, bareback framing is baseline; no contraception language. Phase 2+ Tier 5: "breed me" / "I'm going to put a baby in you" / "you want it inside."
- **Mel references** are Tier-3 capstone moments — once per capstone maximum. Lane 1/2 canvases do NOT use Mel as recurring ambient texture.
- Pre-Stage 3: NO sexual register. Restraint IS the charge.

**Banned dialogue patterns:**

❌ "Sweetheart" / "honey" / any pet name in Lane 1/2 canvases
❌ Warmth-bombs ("You're great at this") — authority-coded validation only
❌ Backstory volunteered unprompted — one disclosure per capstone maximum
❌ Questions that apologize for themselves
❌ Third-person narration of his feelings
❌ "Daddy" framing — Hank is employer-authority, not biological-family-coded
❌ Hank laughing or making jokes — dry observations only
❌ Rushing the physical — pre-Stage 2 is purely restrained
❌ Any contraception language at any stage
❌ Warmth-register during sex ("I love you," "you're so beautiful")

#### §4.1.3 Stat ladder + tier mapping

| Tier | Maya corr | Capstone gate | Content type | Pretext shape | Authority register | Pam awareness |
|---|---|---|---|---|---|---|
| 0 | 0+ | none | Proximity / observation | Passing in diner; corrections | None | 0 |
| 1 | 5+ | none | Self-display / visual | Maya in uniform; Hank watching | Implicit | 0 |
| 2 | 15+ | none | Charged contact (clothed) | Hand on waist; kitchen positioning | "I know." moment | 0 |
| 3 | 25+ | `hank_first_contact` | Explicit oral / partial sex | Back office after close; empty diner | "Good girl. Stay." | 0 (diner-private) |
| 4 | 35+ | `hank_after_close_done` | Full sex / established act | Prep counter; office; after-close surfaces | "Good girl" baseline + bareback | 0 |
| 5 | 50+ | `hank_cracked` | Routine intimate / possessive | Maya arrives through back; breeding talk Phase 2+ | Breeding language active | 0 |

*(Pam does NOT accumulate awareness from Hank arc beats — diner is 2 blocks away; Pam's accumulator is home-based.)*

**Tier transitions:**
- 0→1: corr 5
- 1→2: corr 15
- 2→3: corr 25 + `hank_first_contact`
- 3→4: corr 35 + `hank_after_close_done`
- 4→5: corr 50 + `hank_office_first_done`
- 5→terminal: `hank_cracked` + routine established

#### §4.1.4 Per-rung pretext shapes

**Tier 0 (corr 0+, proximity/observation):**
1. Maya restocking shelves; Hank emerges from the back, watches without comment, returns
2. Counter wipe-down; Hank standing behind her with a single-sentence correction
3. Hank giving an instruction; Maya's hands moving; his eyes on them
4. A regular asks for something off-menu; Hank tells Maya the answer before she can fumble it
5. Maya drops something; Hank picks it up; holds it a beat too long before handing it back

**Tier 1 (corr 5+, self-display/visual):**
1. Maya in her uniform, bending to load the glass rack; Hank at the counter, coffee cooling
2. Maya stretching to reach the top shelf of the supply closet; Hank passes through; his pace slows
3. End-of-shift stretch, apron off; Hank noticing something different in the way she moves
4. Maya catching Hank's eye in the back-kitchen window; neither breaks first
5. Maya bringing coffee to Hank's table during lull; setting it down too close

**Tier 2 (corr 15+, charged contact/clothed):**
1. Hank steadies Maya when she misjudges the reach in the walk-in cooler — hand on hip, released at once
2. Passing behind the counter, his hand on her lower back — positioning, not lingering; he keeps going
3. Hank close behind Maya explaining the coffee machine, not touching but close
4. Maya on break at the counter; Hank across; quiet; both aware the diner is empty
5. He corrects her grip on a tray; fingers briefly around hers; instruction-framed
6. First explicit observation: "You work well when you're not thinking about it." — the compliment too close

**Tier 3 (corr 25+, post-hank_first_contact, explicit/partial):**
1. Maya staying after close to recount the register; Hank coming from the office; door locked
2. Empty diner at 3am; Hank sits next to Maya; hand on her knee; no explanation given
3. Walk-in cooler; door closes; Hank doesn't step back
4. Back office; Hank at the desk; Maya delivering something; the turn; what happens
5. Maya kneeling for something dropped under the counter; Hank behind her; the moment

**Tier 4 (corr 35+, post-hank_after_close_done, full sex/established):**
1. Prep counter at 4am: Hank bends Maya over it; "good girl"; bareback; employer-possessive throughout
2. Office sex routine — Maya after her last table, Hank waiting; established now
3. Hank guiding Maya through an explicit act during empty-diner hours; instructions, not conversation
4. Counter sex in full uniform: apron still on; Hank from behind; "stay still"
5. Maya initiates for the first time: Hank's reaction — waiting rather than moving; she earns it

**Tier 5 (corr 50+, post-hank_cracked, routine + Phase 2+ breeding):**
1. Maya arrives through the back; Hank's already started the coffee; the arrangement is infrastructure
2. Hank fucks Maya at close without preamble; "You want it inside." (breeding baseline Phase 2+)
3. Routine: Maya on shift, office after, bareback, consistent
4. (Phase 2+) Pregnancy discovered: Hank's reaction — "That's what I figured."

#### §4.1.5 Lane-by-lane content map

**loc_diner_front (Hank present 22:00–01:30 weekdays):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | `hank_diner_front_hub` | Locked-visible ladder from Day 1: Talk + Tease (locked corr 5) + Flash (locked corr 15) + Come to office (locked corr 25 + `hank_first_contact`) + Back door routine (locked corr 50) |
| Lane 2 ambient | `ambient_hank_counter_alone` | T1+; Hank at counter during lull; Maya approaching; dice 25% |
| Lane 2 ambient | `ambient_hank_diner_observation` | T0; Hank making an observation about Maya's work; dice 20% |
| Lane 2 ambient | `ambient_hank_mel_reference` | T1+; one oblique Mel reference; low-repeat; dice 15% |
| Lane 3 sub | `scene_hank_passes_during_restock` | T0+; Maya doing solo restock; Hank passes through; sub on `activity_diner_restock` |
| Lane 3 sub | `scene_hank_kitchen_doorway` | T1+; Maya in kitchen prep; Hank in doorway watching; sub on `activity_diner_kitchen_prep` |
| Lane 3 sub | `scene_hank_walkin_encounter` | T2+; Maya in walk-in cooler; Hank appears; sub on `activity_diner_walkin_stock` |
| Capstones | `scene_hank_slow_night_talk`, `scene_hank_first_contact_kitchen` | Per §6 |

**loc_diner_back:**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 2 ambient | `ambient_hank_kitchen_check` | T0; Hank doing kitchen walkthrough; dice 15% |
| Lane 3 sub | `scene_hank_storage_room` | T3+; Maya in diner storage; sub on `activity_diner_storage_stock` |

**loc_diner_office (T3+ unlocked, post-`hank_first_contact`):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | `hank_office_hub` | Post-`hank_first_contact`; explicit items at T3+ |
| Capstones | `scene_hank_after_close`, `scene_hank_office_first`, `scene_hank_declaration` | Per §6 |

#### §4.1.6 Capstones

| # | Capstone | Type | Trigger | Brief shape | Flag writes |
|---|---|---|---|---|---|
| 1 | `canvas_hank_hire` | A | Day 1; loc_diner_front; first visit | Hank interviews Maya in five minutes across the counter. She gets the job. Not elaborate — he sees something and decides. | `hired_at_diner = true` |
| 2 | `scene_hank_slow_night_talk` | A | corr 5 + `hired_at_diner` + 22:00–02:00 + diner empty | 2am; empty diner; Hank tells Maya one specific thing about Mel. Not sexual — first honest moment between them. | `hank_opened_up = true` |
| 3 | `scene_hank_first_contact_kitchen` | A | corr 15 + `hank_opened_up` + loc_diner_back + Hank present | Kitchen. Hank steadies Maya; his hand on her waist, briefly. He removes it. Both register it happened. | `hank_first_contact = true` |
| 4 | `scene_hank_after_close` | B (Pattern F) | corr 25 + `hank_first_contact` + 01:00–07:00 + loc_diner_front | Hank locks the front door while Maya finishes side-work. Tells her to stay. Branch A (accept): first explicit back-office beat → `hank_after_close_done`. Branch B (leave): re-fires next eligible night. | `hank_after_close_done = true` (accept) |
| 5 | `scene_hank_office_first` | A | corr 35 + `hank_after_close_done` + loc_diner_office | Full sex in the office after close. Bareback. "Good girl." Employer-authority register throughout; not elaborate. | `hank_office_first_done = true` |
| 6 | `scene_hank_declaration` | A | corr 50 + `hank_office_first_done` + loc_diner_office | Hank tells Maya she belongs in the diner. Possession-framed, not romance-framed. "You work here. You stay here." Routine intimate established. | `hank_cracked = true` |

#### §4.1.7 Anti-patterns

❌ **Hank volunteering emotional backstory unprompted** — one disclosure per capstone max; Lane 1/2 is sparse
❌ **Warmth-bombs ("great job," "well done")** — wrong register entirely
❌ **Any contraception language** — bareback from first explicit beat; no exceptions
❌ **Mel references as recurring ambient device** — once per capstone; never in Lane 1/2 texture
❌ **"Daddy" framing** — Hank is employer-authority, NOT biological-family-coded
❌ **Hank being warm, joking, or casual** — observational, not funny; dry, not warm
❌ **Hank initiating before Stage 2 stat threshold** — restraint is load-bearing; he does not move early
❌ **Lane 3 substitutions on non-work activities** — Hank fires only on diner-work Maya activities
❌ **Pam accumulating awareness from Hank scenes** — diner is 2 blocks away; invisible to Pam's accumulator
❌ **Explicit sex at Tier 0–2** — the wait is the kink
❌ **Hank apologizing or showing regret** — correction is not apology
❌ **Long Lane 2 ambients** — restraint governs even ambient length (~100–150 words max)

#### §4.1.8 Cross-arc state writes / reads

**Writes:**

| State | Trigger | Effect |
|---|---|---|
| `hired_at_diner` | `canvas_hank_hire` | Activates diner income; enables Rosa + Cole canvases |
| `hank.arousal +1` | Per Tier 1+ Lane 1 beat | Standard |
| `player.corruption +1` | Per Tier 1+ Lane 1 beat | Standard |
| `hank.relation +1` | Talk interactions | Standard |
| `hank_opened_up` | Capstone 2 | Stage 1 canvases unlock |
| `hank_first_contact` | Capstone 3 | Tier 3 content + office hub unlock |
| `hank_after_close_done` | Capstone 4 accept | Tier 3+ explicit unlocked |
| `hank_office_first_done` | Capstone 5 | Tier 4 established |
| `hank_cracked` | Capstone 6 | Tier 5 routine |

**Reads:**

| State | Source | Effect on Hank scenes |
|---|---|---|
| `hired_at_diner` | Hank hire capstone | Required gate for all Hank arc canvases |
| `outfit_id` | Wardrobe system | Certain Lane 2 ambients fire differently in uniform vs off-duty clothes |
| `player.pregnancy` | Pregnancy system | Tier 5 scenes branch to pregnant-variant canvases |

#### §4.1.9 Cross-references

| Doc | Purpose |
|---|---|
| `doctrine/03_arc_shapes.md` §3 | Family/ambient distribution |
| `doctrine/08_kink_vocab_ceilings.md` | Authority + breeding ceiling |
| `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` | Family/ambient gold standard |

#### §4.1.10 Acceptance criteria

- [ ] §1 names arc-complete state with 5 specific signature scenes
- [ ] §2: 7 speech patterns + 6 stage samples + 10 banned patterns
- [ ] §3: 6-tier ladder; all columns populated; Pam=0 documented
- [ ] §4: 5+ pretext shapes per tier (Tier 0–5 = 30 shapes)
- [ ] §5: diner_front + diner_back + diner_office per Hank schedule
- [ ] §6: 6 capstones (hire + 5-capstone chain), all typed + triggered + flag-writes named
- [ ] §7: 12 anti-patterns; "daddy" explicitly banned
- [ ] §8: cross-arc writes + reads; pregnancy retrofit noted; Pam=0 explicit
- [ ] No contraception language anywhere in brief

---

### §4.2 — Ben brief (Slow-Burn Family)

**Scope mode:** full_game

#### §4.2.1 End-state fantasy

**Ben sleeps with his little sister, and neither of them pretends it happened by accident.**

Ben is 28 and has spent four years deciding things for himself at a distance from Maya. He moved her boxes when she called because that's what you do. In the apartment he's careful with her — gives space, doesn't ask questions, reads on the couch when she's home, leaves before she wakes up from her night-shift sleep. The slow-burn: the closeness they built as kids (he read to her; she still knows where he sets his coffee cup) layered over a gap that's done something complicated to the register between them. Arc: coexistence → Ben noticing Maya differently → quiet charged moments → first physical admission → consummation.

**Specific signature scenes:**

- 5:45am kitchen: Ben in his work clothes, Maya in the front door from her night shift — apartment half-lit, both between states
- Ben on the couch with his book, Maya watching TV; he closes the book and watches her instead; nothing said
- First touch: one of them takes the other's hand; held five seconds too long; released; nothing said
- Ben's room on a weekend night: Maya knocks and goes in; the specific quiet of two people who know what they're not saying
- First sex: incest callouts throughout; "little sister" said first; the taboo IS the moment

#### §4.2.2 Ben voice spec

**Background:** 28, construction foreman. Grew up as Maya's older protective presence. Hasn't lived with her since she left for school at 18. He reads literary fiction at night — the same habit from reading her to sleep as kids. Economical with words; careful with people he cares about.

**Speech patterns:**

| Pattern | Rule | Example |
|---|---|---|
| Sentence length | Short; questions aren't interrogations | "You eat anything?" / "Work go okay?" |
| Careful address | Uses Maya's name when it matters | "Maya." (specific weight when used) |
| Observation over confrontation | Notices, doesn't announce | (she didn't sleep) → "Coffee's on." |
| Physical restraint | Talks about the neutral thing; real thing stays in body language | — |
| No big-feelings vocabulary | Doesn't say "I miss you" / "I want you" — not his register | — |
| Marks the line flatly | "That's not what that was." / "Yeah." | — |
| Incest register (Stage 3+) | "Little sister" / taboo named during sex | "You're my little sister." / "This is wrong." |

**Voice samples per stage:**

| Stage | Sample line | Tone |
|---|---|---|
| Stage 0 (coexistence) | "You working tonight?" | Practical; schedule-checking |
| Stage 1 (noticing) | "You look — " [doesn't finish] | Interrupted observation |
| Stage 2 (charged moments) | "You know I see you, right." | Not a question; acknowledgment |
| Stage 3 (first admission) | "This isn't something we should do." (doing it anyway) | Taboo named at the moment |
| Stage 4 (explicit) | "God, you're my little sister." | Full incest callout during sex |
| Stage 5 (routine) | "Come here." | No more pretense needed |

**Ben-specific framing rules:**

- **Incest framing IS the kink.** At Stage 3+: "little sister" / "Maya" as callout during sex; explicit taboo acknowledgment throughout ("this is so fucking wrong" / "I shouldn't want you like this" / "my own sister"). Named and dwelt on, not mentioned once and moved past.
- Pre-Stage 2: NO sexual register. Ben is careful. The charge lives in restraint.
- The **5:45am crossover** (Ben leaving/Maya arriving) is the most load-bearing ambient surface.
- Ben's **reading** is a personality anchor — book on the couch, what he's reading, is voice-consistent detail across all stages.
- At Stage 3+, the taboo IS explicit — not softened.

**Banned dialogue patterns:**

❌ "Big brother protective-mode" during sex — protectiveness is pre-Stage 2 only; it breaks INTO incest, not around it
❌ Generic romantic dialogue ("I love you so much," "you're so beautiful") — incest callouts are the language
❌ Ben initiating before Stage 3 without player-driven crossover
❌ Sexual content where the sibling relationship is not acknowledged
❌ Ben volunteering backstory about his life / feelings about their past — not his register
❌ "I've been wanting this for years" — Ben's desire is immediate to proximity, not stored longing
❌ Contraception language at any stage (bareback throughout; pregnancy included)
❌ Scene-body prose creeping into pretext shapes — templates, not prose

#### §4.2.3 Stat ladder + tier mapping (4-stage slow-burn model)

| Stage | Threshold | Gate flag | Content type | Incest callout? | Pam awareness write |
|---|---|---|---|---|---|
| 0 | 0+ | none | Proximity / schedule overlap; no charge | None | 0 |
| 1 | corr 5 + relation 5 | `ben_stage1` (dual-path) | Ben notices differently; charged but unmarked | Implicit framing | 0 |
| 2 | corr 15 + relation 10 | none | Charged moments; hands held too long | None explicit | +1 per charged-moment beat through wall |
| 3 | corr 25 + relation 15 | `ben_first_move_done` | First physical admission; first contact | Emerges: "This is wrong" | +2 (audible through wall) |
| 4 | corr 35 | `ben_consummation_done` | Full sex; incest callouts throughout | Full: "little sister" / "my own sister" | +3 (unmistakable) |

**Stage transitions:**
- 0→1: dual-path (via_beauty: outfit + glance; via_glance: Ben caught watching)
- 1→2: stat-driven (corr 15 + relation 10); ambient-carried, no capstone gate
- 2→3: corr 25 + relation 15 + `scene_ben_stage2_charged_moment` capstone
- 3→4: `ben_first_move_done` + corr 35 + `scene_ben_consummation`

#### §4.2.4 Per-rung pretext shapes

**Stage 0 (coexistence/proximity):**
1. Morning kitchen crossover — Ben leaving, Maya just home; coffee on for himself, pours one for her
2. Both on the couch; Ben has his book; neither watching the show they have on
3. Maya hears Ben come in from work through her bedroom door; sounds she recognizes
4. Ben takes the long way through the living room to get water; Maya's there; no need to
5. Late: Maya awake, light under Ben's door; she considers knocking; doesn't

**Stage 1 (noticing):**
1. Maya in the kitchen in what she wore home from shift; Ben's mid-thought and then isn't
2. Ben watching Maya cross the living room; registers the watch; doesn't correct it
3. Maya stretched on the couch reading; Ben sits; the silence is different from before
4. Morning: Maya not quite awake at the kitchen table; Ben across; he doesn't leave when he could
5. Ben comes home; Maya's in the bathroom; he stops at the door without knocking; turns back

**Stage 2 (charged moments):**
1. Couch: Maya asleep; Ben reading; he puts the book down and watches her for too long
2. Maya home from shift exhausted; Ben awake; kitchen table; hands near each other
3. Bathroom timing: both reaching the bathroom at the same time; the close hall
4. Maya in distress (bad shift); Ben sits next to her; hand on her back; stays longer than comfort
5. Ben hands Maya something; their fingers together a moment; neither moves first

**Stage 3 (first admission):**
1. Late Friday — Ben puts the book down; Maya is close; the line; someone crosses
2. Ben's room: Maya knocks, goes in; sits on his bed for no reason; the quiet becomes specific
3. Kitchen at 5am: Maya home, Ben awake; first contact — hand, cheek, small and irreversible
4. Couch: TV off; the decision in the room; "This is wrong"; doing it anyway
5. Taboo stated into the act: "I know. I know what this is." — named, not avoided

**Stage 4 (consummation, full incest register):**
1. Ben's room: full sex; "little sister" said first; the callout sustained throughout
2. Maya initiates; Ben's restraint breaks: "You're my sister, Maya."; goes there anyway
3. Couch: quick and urgent; "my own sister" during it; both named in it
4. Kitchen morning crossover becomes something else; incest framing throughout
5. (Phase 2+) Post-pregnancy-revealed: Ben's reaction — incest callouts mixed with breeding weight

#### §4.2.5 Lane-by-lane content map

**loc_shared_kitchen (Ben 05:30–06:30 daily + evenings):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | `ben_kitchen_hub` | Stage 1+: Talk + [locked: Stay up with me (Stage 2) + Touch his hand (Stage 2) + Come to his room (Stage 3)] |
| Lane 2 ambient | `ambient_ben_morning_crossover` | Stage 0+; 5:45am crossover; dice 30% in morning window |
| Lane 2 ambient | `ambient_ben_kitchen_late` | Stage 1+; both awake at odd hours; dice 20% |
| Lane 3 sub | `scene_ben_walks_in_kitchen` | Stage 2+; Maya making tea/coffee solo; Ben appears; sub on `activity_make_tea` / `activity_make_coffee_solo` |

**loc_living_room (Ben evenings + weekends):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | `ben_living_room_hub` | Stage 1+: Talk + [locked: Sit with him + Touch him + Come to his room] |
| Lane 2 ambient | `ambient_ben_couch_reading` | Stage 0+; Ben reading, Maya in the room; dice 25% |
| Lane 3 sub | `scene_ben_couch_reveal` | Stage 1+; Maya watching TV solo; Ben appears; sub on `activity_watch_tv` |

**loc_bens_room (Stage 3+ unlocked):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | `ben_room_hub` | Stage 3+; charged hub: Come in + Talk + Touch + [explicit items Stage 4+] |
| Lane 3 sub | `scene_ben_walks_in_change` | Stage 1+; Maya changing; Ben in doorway (door ajar); sub on `activity_change_clothes` |

#### §4.2.6 Capstones

| # | Capstone | Type | Trigger | Brief shape | Flag writes |
|---|---|---|---|---|---|
| 1a | `scene_ben_stage1_via_beauty` | A | corr 0 + `outfit_corrupted_tier1` + Ben schedule present + loc_living_room | Ben sees Maya in a specific outfit; the look that crosses his face; he corrects it too late. Stage 0→1. | `ben_noticed_via_beauty = true`; `ben_stage1 = true` |
| 1b | `scene_ben_stage1_via_glance` | A | corr 5 + `ben_stage1 = false` + Ben present + loc_living_room | Maya catches Ben watching her during an ordinary moment; eye contact held too long; neither addresses it. Stage 0→1. | `ben_noticed_via_glance = true`; `ben_stage1 = true` |
| 2 | `scene_ben_stage2_charged_moment` | B (Pattern F) | corr 25 + relation 15 + `ben_stage1` + Ben home evening | Charged late-night moment. Branch A (accept): first contact — hand held, cheek, small and irreversible → `ben_first_move_done`; `pam.awareness += 2`. Branch B (decline): Ben pulls back; re-fires next eligible evening. | `ben_first_move_done = true` (accept); `pam.awareness += 2` (accept) |
| 3 | `scene_ben_consummation` | A | corr 35 + `ben_first_move_done` + loc_bens_room + Ben present | First full sex in Ben's room. Incest callouts at every beat. Taboo named and held. Tier-3 prose. Pam awareness +3. | `ben_consummation_done = true`; `pam.awareness += 3` |
| 4 | `scene_ben_pregnancy_revelation` | A (Phase 2+) | `player.pregnancy = true` + `ben_consummation_done` | Maya tells Ben. Ben's response — incest and breeding weight combined. | `ben_knows_pregnancy = true` |

#### §4.2.7 Anti-patterns

❌ **Ben initiating before Stage 3** — restraint is the arc; no moves before `ben_first_move_done`
❌ **Incest framing absent from Stage 3+ sexual content** — "brother/sister" callouts THROUGHOUT; no generic dialogue
❌ **"I've wanted you for years" backstory** — desire is immediate to proximity, not stored
❌ **Family/ambient saturation** — Ben is NOT Frank-shaped; no Lane 2 ambients before Stage 1; no padding
❌ **Long Lane 2 Ben ambients** — slow-burn = concentrated beats; Lane 2 scenes ~80–120 words
❌ **Ben protective-mode during sex** — protectiveness is pre-Stage 2 only
❌ **Contraception language** — bareback throughout; pregnancy included
❌ **Generic romantic declarations** — incest register ("little sister," "we shouldn't") not ("I love you")
❌ **Ben and Cole overlap** — separate locations; arcs do not bleed
❌ **Pam accumulating from Stage 0–1 Ben scenes** — accumulation starts Stage 2+ only
❌ **More than 3 Lane 2 Ben ambients total** — slow-burn budget: sparse
❌ **Pretext shapes written as scene prose** — shape descriptors only

#### §4.2.8 Cross-arc state writes / reads

**Writes:**

| State | Trigger | Effect |
|---|---|---|
| `pam.awareness +1` | Stage 2 ambient charged-moment through wall | Pam accumulator begins |
| `pam.awareness +2` | `scene_ben_stage2_charged_moment` accept branch | Audible through wall |
| `pam.awareness +3` | `scene_ben_consummation` | Unmistakable |
| `ben_stage1` | Dual-path capstone 1a or 1b | Stage 1 canvases unlock |
| `ben_first_move_done` | Capstone 2 accept | Stage 3+ unlock |
| `ben_consummation_done` | Capstone 3 | Stage 4 established |
| `player.corruption +1` | Per Lane 1 charged interaction | Standard |
| `ben.relation +1` | Talk interactions | Standard |

**Reads:**

| State | Source | Effect |
|---|---|---|
| `outfit_corrupted_tier1` | Wardrobe system | Triggers `scene_ben_stage1_via_beauty` path |
| `player.pregnancy` | Pregnancy system | Unlocks `scene_ben_pregnancy_revelation` |

#### §4.2.9 Cross-references

| Doc | Purpose |
|---|---|
| `doctrine/03_arc_shapes.md` §4 | Slow-burn family distribution |
| `doctrine/08_kink_vocab_ceilings.md` | Incest callout ceiling |
| `28th_april_TLS_Phase2_Redesign/59_Jake_Design_Brief.md` | Jake slow-burn gold standard |

#### §4.2.10 Acceptance criteria

- [ ] §1: 5 specific signature scenes named
- [ ] §2: incest register locked; 6 stage samples; 12 banned patterns
- [ ] §3: 4-stage ladder (not 6-tier); all columns populated; Pam write values declared
- [ ] §4: 5+ pretext shapes per stage (Stage 0–4 = 20+ total)
- [ ] §5: kitchen + living room + Ben's room + Lane 3 subs covered
- [ ] §6: dual-path capstone + charged-moment + consummation + Phase 2+ pregnancy capstone
- [ ] §7: 12 anti-patterns; "stored longing" explicitly banned
- [ ] §8: Pam awareness write-values per stage-threshold tabulated

---

### §4.3 — Cole brief (Peer/Dating)

**Scope mode:** full_game

#### §4.3.1 End-state fantasy

**Cole and Maya sleep together in the gray morning after a shift, in his apartment two blocks from the diner, in the particular exhaustion of people who work the night.**

Cole is 27, dropped out of art school (tattoo illustration track) and found the grill. He doesn't talk much on shift but he watches. His timing is calibrated — he lets the food speak. The dating chain: coworkers → first real break conversation → post-shift predawn walk → first date in daylight → first night at his place. The arc is relation-driven; Cole doesn't push; the escalation happens at Maya's pace.

**Specific signature scenes:**

- Break in the diner alley at 2am — Cole leaning against the wall, Maya on the step, talking about something that isn't work for the first time
- Post-shift walk: 6:45am, the town empty, both still in their work smell, light going blue-gray
- First date: afternoon coffee; both slightly sleep-deprived and strange from being in daylight; the weirdness of seeing him outside the diner
- Cole's apartment, first time: drawings on the walls; him showing her one
- First sex: Cole's bedroom; crude anatomical register per ceiling; his sparse diction throughout

#### §4.3.2 Cole voice spec

**Background:** 27, from two towns over. Art school for a year, then left. Been cooking for four years. Tattoo drafts everywhere on paper at his apartment. Speaks sparingly on shift; slightly more off it. Not shy — selectively present.

**Speech patterns:**

| Pattern | Rule | Example |
|---|---|---|
| Minimal sentence count | Fewer sentences per exchange than the scene invites | Three where another character would give ten |
| No urgency | Doesn't rush explanations or reactions | "Yeah." [pause] "I figured." |
| Direct without harsh | States things plainly; unadorned | "You're better at the counter than Rosa was at first." |
| Physical anchors over feelings-talk | What he did, not what he felt | "I walked home the long way." |
| Patience-coded | If you're not ready to talk, he's not going anywhere | — |
| Stage 3+ sex diction: crude and spare | Maximum crude anatomical; minimum extra words | "Turn over." / "Open." / "Your cunt's so tight." |

**Voice samples per stage:**

| Stage | Sample line | Tone |
|---|---|---|
| Stage 0 (coworkers) | "Order's up." | Functional |
| Stage 1 (noticed) | "You want coffee? I made extra." | Attention, plainly stated |
| Stage 2 (dating) | "You're weird in daylight." (not unkind) | Observation-affection |
| Stage 3 (intimate) | "Come over." | Minimal; definite |
| Stage 4 (explicit) | "Your cunt's so tight." / "Turn over." | Maximum crude; directive |

**Cole-specific framing rules:**

- Stage 3+ sex register: MAXIMUM CRUDE ANATOMICAL. "Cock" / "cunt" / "ass" / cum descriptions — crude and direct. The sparseness of his speech carries into sex: short directives, anatomical specificity, no sentimentality.
- The diner drawings / art details are voice-consistent anchors for Lane 2 and capstone texture.
- Cole during sex is even more spare than Cole normally — imperative sentences, no endearments.

**Banned dialogue patterns:**

❌ Cole being verbose or explanation-heavy at any point
❌ Romantic-Hollywood declarations ("I think I'm falling for you")
❌ Cole apologizing in advance
❌ Euphemistic anatomical references in Tier 3+ scenes
❌ Cole making small talk with Hank or Rosa on-screen in ways that pad canvases
❌ Lane 3 substitutions — Cole is peer/dating; Lane 3 = 0
❌ Cole knowing about Ben or Maya's home situation before she tells him

#### §4.3.3 Stat ladder + tier mapping (relation-driven stages)

| Stage | Relation threshold | Gate flag | Content type |
|---|---|---|---|
| 0 | 0+ | none | Work-neutral co-presence |
| 1 | relation 5+ | `cole_noticed` | First real break conversation; mutual awareness |
| 2 | relation 15+ | `cole_walk_done` | Post-shift walks; first date; outside-work identity |
| 3 | relation 25+ | `cole_date_done` | First sex; Cole's apartment |
| 4 | relation 35+ | `cole_first_night_done` | Established sexual relationship; explicit routine |

#### §4.3.4 Per-rung pretext shapes

**Stage 0 (coworkers):**
1. Cole slides an order; Maya picks it up; three words max exchanged
2. Maya asks where something is in the kitchen; Cole shows her without comment
3. Cole eating on his break; Maya sits nearby; no conversation; both okay with that
4. Shift-end: Cole wiping the grill; Maya doing side-work; parallel tasks quiet
5. Rosa references Cole during training: "Cole doesn't talk much but he'll tell you if something's wrong"

**Stage 1 (noticed — post-`cole_noticed`):**
1. Alley break: Maya asks something that isn't about work; Cole answers it
2. Cole making extra coffee; handing it to Maya across the counter
3. End-of-shift walk to the parking lot; Cole goes the same direction for two blocks
4. Cole mentions the drawings without Maya asking — first voluntary disclosure
5. 4am lull: Cole visible through the kitchen window; Maya catches herself watching

**Stage 2 (dating — post-`cole_walk_done`):**
1. Cole and Maya walk to the edge of town at 6:30am, coffee in paper cups
2. First date in daylight: coffee shop; both slightly unreal; the weirdness of being there
3. Cole in the park; specific detail of what they talked about (something from the drawings)
4. Post-shift: Cole waits for Maya's side-work to finish; unstated offer
5. Cole shows Maya a drawing at his apartment door; first time she's there; stopped at the threshold

**Stage 3 (intimate — post-`cole_date_done`):**
1. Post-date; Cole's apartment; Maya goes in; first explicit moment
2. Late-shift end: both tired; couch; the move that's been coming
3. Afternoon: Maya comes by outside of work; both know why; Cole's bedroom
4. First sex: explicit throughout; crude anatomical register; Cole's sparse diction in it too

**Stage 4 (ongoing — post-`cole_first_night_done`):**
1. Maya knocks on Cole's door mid-afternoon; established now; no pretense
2. After-shift sex: Cole's bedroom; directives throughout; maximum crude anatomical
3. Position-specific explicit scenes; cum descriptions; the established physical vocabulary
4. (Phase 2+) Pregnant-variant scenes: same register; pregnancy acknowledged in diction

#### §4.3.5 Lane-by-lane content map

**loc_diner_back (Cole's territory 21:00–07:00):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | `cole_diner_back_hub` | Stage 0+: Talk + [locked: Ask him to walk (Stage 1) + Ask him out (Stage 2) + Come to his place (Stage 3+)] |
| Lane 2 ambient | `ambient_cole_kitchen_window` | Stage 1+; Maya at diner_front sees Cole through kitchen window; dice 20% |
| Lane 2 ambient | `ambient_cole_break_alley` | Stage 1+; break overlap in alley; dice 25% |

**loc_town_park / loc_main_street (post-shift window 06:30–09:00):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 2 ambient | `ambient_cole_post_shift_parallel` | Stage 2+; both leaving shift same direction; dice 30% |

**loc_cole_apartment (Stage 3+ unlocked, post-`cole_date_done`):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | `cole_apartment_hub` | Stage 3+; dating-chain hub; explicit items at Stage 3+ |

#### §4.3.6 Capstones

| # | Capstone | Type | Trigger | Brief shape | Flag writes |
|---|---|---|---|---|---|
| 1 | `scene_cole_first_break_talk` | A | relation 5 + loc_diner_back + 23:00–05:00 break window | Alley break: Maya asks Cole something real; he answers. First mutual acknowledgment they're people with lives outside the grill. | `cole_noticed = true` |
| 2 | `scene_cole_post_shift_walk` | A | relation 10 + `cole_noticed` + shift-end window 06:00–08:00 | Post-shift predawn walk. 6:45am light. Both in their work smell. He talks about the drawings. The town is empty. | `cole_walk_done = true` |
| 3 | `scene_cole_first_date` | A | relation 15 + `cole_walk_done` + afternoon off-shift window | Daytime coffee; both sleep-deprived; the strangeness of daylight. Cole shows her a drawing. First time outside the diner context. | `cole_date_done = true` |
| 4 | `scene_cole_first_night` | B (Pattern F) | relation 25 + `cole_date_done` + loc_cole_apartment | Cole's apartment. Branch A (stay): first sex; crude anatomical register throughout; `cole_first_night_done`. Branch B (leave): Maya leaves; re-fires next eligible visit. | `cole_first_night_done = true` (accept) |

#### §4.3.7 Anti-patterns

❌ **Lane 3 substitutions** — peer/dating, Lane 3 = 0; no exceptions
❌ **Verbose or emotionally articulate Cole** — three sentences where ten would fit
❌ **Soft sex diction at Stage 3+** — maximum crude anatomical; no euphemisms
❌ **Cole initiating before relation 15** — he notices and offers; doesn't push before threshold
❌ **Cole and Hank overlap** — diner_back is Cole's; Hank appears there rarely and differently
❌ **Romantic declarations** — wrong register; Cole says things plainly or doesn't
❌ **Backstory volunteered without prompt** — sparse; disclosure is rare
❌ **Dating chain skipping steps** — capstones gate sequentially; no shortcuts
❌ **Lane 2 Cole ambients before `cole_noticed`** — Stage 0 is neutral co-presence only
❌ **Cole knowing about Ben** — separate arcs; no bleed unless Maya explicitly tells him

#### §4.3.8 Cross-arc state writes / reads

**Writes:**

| State | Trigger | Effect |
|---|---|---|
| `cole_noticed` | Capstone 1 | Stage 1 unlock |
| `cole_walk_done` | Capstone 2 | Stage 2 unlock |
| `cole_date_done` | Capstone 3 | Stage 3 / apartment unlock |
| `cole_first_night_done` | Capstone 4 accept | Stage 4 established |
| `cole.relation +1` | Talk + capstone progression | Standard |

**Reads:**

| State | Source | Effect |
|---|---|---|
| `hired_at_diner` | Hank hire capstone | Required gate for all Cole canvases |
| `player.pregnancy` | Pregnancy system | Stage 4 scenes branch to pregnant-state variants |

#### §4.3.9 Cross-references

| Doc | Purpose |
|---|---|
| `doctrine/03_arc_shapes.md` §5 | Peer/dating distribution |
| `28th_april_TLS_Phase2_Redesign/58_Ryan_Design_Brief.md` | Ryan peer/dating gold standard |

#### §4.3.10 Acceptance criteria

- [ ] §1: 5 signature scenes named
- [ ] §2: sparse diction locked; 6 stage samples; 10+ banned patterns
- [ ] §3: 4-stage relation ladder
- [ ] §4: 5+ pretext shapes per stage (20+ total)
- [ ] §5: diner_back + post-shift town + cole_apartment covered; Lane 3=0 committed
- [ ] §6: 4 capstones in sequence, each gating the next
- [ ] §7: 10 anti-patterns; Lane 3=0 explicitly listed
- [ ] §8: hired_at_diner gate documented; pregnancy retrofit noted

---

### §4.4 — Rosa brief (Service)

**Scope mode:** full_game

#### §4.4.1 End-state fantasy

**Rosa trains Maya on the floor. In Phase 3+, the head waitress who has held her marriage intact for eleven years of night shifts stops holding it.**

Rosa is 43, married 15 years, two kids in middle school. She's been head waitress at Mel's for eleven years. She trains Maya efficiently and with warmth that isn't performative — she just knows how this place works. The service arc is bounded in full_game scope by the service register: Rosa's content is training + workplace texture + relationship build. Phase 3+ is adultery / lesbian-initiation territory. Her marriage is the kink when that moment arrives — she knows exactly what she's doing when she crosses that line.

**Specific signature scenes:**

- Rosa showing Maya the floor in 40 words — efficient; warm; the woman who has run this shift for 11 years
- Rosa covering for Maya on a hard night without making a thing of it
- Rosa and Maya side-by-side at end of shift; a conversation that isn't training anymore
- (Phase 3+) Rosa after close with Maya; something changed in how she's standing; "You don't have to go yet"
- (Phase 3+) Rosa's marriage named explicitly during the explicit act — adultery IS the kink; she knows it

#### §4.4.2 Rosa voice spec

**Background:** 43, from this town. Married to a decent man. Two daughters, 11 and 13. Works nights because the money is better and the work is real. Warm without being saccharine — the warmth of someone calibrated, not performing.

**Speech patterns:**

| Pattern | Rule | Example |
|---|---|---|
| Efficiency | Delivers information; no pad | "Table 4 is the big tipper. Table 9 never tips. Don't argue with 9." |
| "Hon" register | Used sparingly; not sycophantically | "Hon, the ice machine is temperamental after midnight." |
| Warm-direct split | Warm in tone; direct in content | Neither cold nor over-warm |
| Doesn't volunteer personal life | Kids, husband mentioned only if contextually needed | — |
| Competence-coded | Knows everything about the floor; authority from that | — |
| Phase 3+ register shift | Something changes late at night when the diner's empty | "You're doing good." (said differently) |

**Voice samples per stage:**

| Stage | Sample line | Tone |
|---|---|---|
| T0 (training) | "Coffee before water for Table 7 — they always ask." | Efficient competence |
| T1 (colleague) | "You'll be fine. Don't let Hank see you do the napkin thing." | Warm, conspiratorial |
| Phase 3+ | "You know you don't have to go yet." | Different weight; she knows what she means |

**Banned dialogue patterns:**

❌ Rosa volunteering intimate personal details in slice
❌ Lane 2 or Lane 3 content in any scope (service shape; empty cells are honest)
❌ Rosa making moves in this game's current scope
❌ "Rosa drama" from home life in canvases
❌ Phase 3+ content authored before Phase 3+ is scoped by LO

#### §4.4.3 Stat ladder (Service — 2 tiers)

| Tier | Gate | Content type | Register |
|---|---|---|---|
| T0 | `hired_at_diner` | Training + shift work + talk | Efficient-warm workplace |
| T1 | rosa.relation 15+ | Trusted colleague; Rosa covers for Maya | Warm-direct; conspiratorial-colleague |
| Phase 3+ (deferred) | TBD Phase 3+ | Adultery / lesbian initiation | FULL ADULTERY FRAMING (ceiling declared, content held) |

#### §4.4.4 Per-rung pretext shapes (Service — minimal)

**T0 (training):**
1. Rosa showing Maya the table layout — specific about which tables need what
2. Rosa demonstrating the coffee cadence; three instruction sentences
3. Rosa handling a difficult regular while Maya watches
4. Rosa explaining a Mel's rule that isn't in any manual
5. Rosa covering for Maya's mistake without flagging it to Hank

**T1 (trusted colleague):**
1. Side-by-side doing side-work at end of shift; conversation that isn't training
2. Rosa covers for Maya on a hard table; later: "Next time do it the other way."
3. Rosa shows Maya something about the diner that isn't in the training — institutional memory

**Phase 3+ (ceiling declared, content deferred):**
*FULL ADULTERY FRAMING — Rosa's marriage is named during the explicit act; she knows she's crossing a line that holds her together; lesbian initiation or Rosa-initiates direction TBD Phase 3+ authoring session.*

#### §4.4.5 Lane-by-lane content map

**loc_diner_front (Rosa 17:00–01:00 weekdays):**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | `rosa_diner_front_hub` | 4 unlocked: Talk + Ask about a regular + Ask Hank about hours + Watch her work; 4 locked-visible Phase 3+ stubs (Tease / Flirt / Invite to close / Let her close with you); 1 Leave |
| Lane 2 | **Empty** | Phase 3+ |
| Lane 3 | **Empty** | Service shape; 0 own Lane 3 |
| Capstones | `canvas_rosa_onboarding` | Per §6 |

#### §4.4.6 Capstones

| # | Capstone | Type | Trigger | Brief shape | Flag writes |
|---|---|---|---|---|---|
| 1 | `canvas_hank_hire` | A | Day 1; loc_diner_front; first visit | Hank hires Maya across the counter in five minutes. The interview is five sentences. He sees something and decides. (This fires as Hank's capstone but sets the shared flag.) | `hired_at_diner = true` |
| 2 | `canvas_rosa_onboarding` | A | `hired_at_diner` + Rosa schedule present + first 3 days | Rosa shows Maya the floor in two hours. The training is the capstone. Efficient. Warm. The relationship starts here. | `rosa_trained_maya = true` |

*(Phase 3+ escalation capstone TBD Phase 3+ authoring.)*

#### §4.4.7 Anti-patterns

❌ **Lane 2 or Lane 3 content for Rosa** — service shape; empty cells are honest
❌ **Rosa making moves before Phase 3+** — training/colleague register only
❌ **Hub padded with work-task items** ("Help clear Table 4" is NOT a hub item)
❌ **Rosa backstory volunteered in prose** — compact, efficient; personal details only if contextual
❌ **Treating Rosa as Marge** — Rosa is peer-colleague, not employer; different power dynamic
❌ **Phase 3+ content authored before scoped** — ceiling declared, content held
❌ **More than 2 capstones in this game's authoring scope** — Phase 3+ escalation capstone is the Phase 3+ add

#### §4.4.8 Cross-arc state writes / reads

**Writes:**

| State | Trigger | Effect |
|---|---|---|
| `hired_at_diner` | Hank hire capstone | Activates income; enables diner NPC canvases |
| `rosa_trained_maya` | Rosa onboarding capstone | T1 Rosa canvases unlock |
| `rosa.relation +1` | Talk interactions | Standard |

**Reads:**

| State | Source | Effect |
|---|---|---|
| `hired_at_diner` | Hank hire capstone | Required gate for all Rosa canvases |

#### §4.4.10 Acceptance criteria

- [ ] §1: Phase 3+ end-state named even though deferred
- [ ] §2: efficient-warm register locked; Phase 3+ shift noted
- [ ] §3: 2-tier service ladder; Phase 3+ row declared + deferred
- [ ] §5: diner_front hub with locked-visible Phase 3+ stubs; Lane 2/3 empty committed
- [ ] §6: 2 capstones (hire + onboarding)
- [ ] §7: 8+ anti-patterns
- [ ] Empty Lane 2/3 cells committed, not papered over

---

### §4.5 — Pam Dockery brief (Antagonist/Witness)

**Scope mode:** full_game

#### §4.5.1 End-state fantasy

**Pam Dockery names what she's heard through the apartment walls. The confrontation determines whether she becomes a threat or goes quiet.**

Pam is 56, retired bookkeeper, has lived in the building for 12 years. She was friendly with Ben before Maya moved in — she knows him as the quiet guy on the second floor who nods at her in the parking lot. When Maya arrives, Pam notices the change in the apartment's sounds. She doesn't say anything immediately. The awareness accumulates slowly, then past a threshold, she acts.

**Specific signature scenes:**

- Pam in the laundry room when Maya comes home from shift — the over-polite exchange that's really surveillance
- Pam at the building front when Ben comes home; watching; nothing said
- Pam in the hallway; she stops Maya; says the thing she's been not saying
- Branch A: Maya manages Pam — Pam implies she'll stay quiet if things stay quiet; Maya gives her something to hold
- Branch B: Pam escalates to Ben — she goes to his door; Ben has to have the conversation with Maya

#### §4.5.2 Pam voice spec

**Background:** 56, retired bookkeeper. Seen a lot from this building in 12 years. Not mean — observant. Keeps her opinions until she can't.

**Speech patterns:**

| Pattern | Rule | Example |
|---|---|---|
| Polite + knowing | Every sentence has a second sentence underneath | "Busy night? I heard you come in." |
| Implies rather than states | Doesn't accuse; suggests | "This building has thin walls. Always has." |
| Uses Ben as anchor | References Ben as known quantity | "Ben seemed tired this morning." |
| Confrontation: direct | When she finally names it, she names it | "I know what's happening up there." |

**Banned dialogue patterns:**

❌ Pam acting sexually or with any kink register
❌ Pam threatening in operatic/villain mode
❌ Pam knowing about Hank or Cole (home-based; diner invisible to her)
❌ Pam appearing in Hank or Cole canvases

#### §4.5.3 Awareness accumulator

| Band | Awareness | State | Effect |
|---|---|---|---|
| Cold | 0–24 | Baseline | Neutral building encounters |
| Suspicious | 25–49 | Pam noticing | Interactions become loaded |
| Knowing | 50–74 | Confrontation primed | Capstone eligible |
| Shut-out | 75–100 | Confrontation imminent | Capstone fires |

**Accumulator writes (from Ben arc only):**
- Ben Stage 2 ambient charged-moment (through wall): `pam.awareness +1`
- `scene_ben_stage2_charged_moment` accept: `pam.awareness +2`
- `scene_ben_consummation`: `pam.awareness +3`
- Building-encounter canvases at Suspicious band: `pam.awareness +1` per eligible beat

**Sidebar:** awareness NOT surfaced. Dramatic surprise depends on hiding.

#### §4.5.4 Lane-by-lane content map

**loc_laundry_room + loc_building_front + loc_apartment_hallway:**

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 2 ambient | `ambient_pam_building_neutral` | Cold band (0–24); neutral encounter; dice 20% on building entry |
| Lane 2 ambient | `ambient_pam_building_loaded` | Suspicious band (25–49); observations pointed without naming anything |
| Lane 2 ambient | `ambient_pam_building_precursor` | Knowing band (50–74); Pam makes clear she knows; confrontation eligible |
| Capstone | `scene_pam_confrontation` | Awareness ≥ 75; Type B Pattern F |

#### §4.5.5 Capstones

| # | Capstone | Type | Trigger | Brief shape | Flag writes |
|---|---|---|---|---|---|
| 1 | `scene_pam_confrontation` | B (Pattern F) | `pam.awareness >= 75` + Pam schedule + building location | Hallway or laundry room. Pam says what she knows. Branch A (managed): Maya implies discretion; Pam stays quiet → `pam_managed`. Branch B (escalated): Pam goes to Ben; Ben confronts Maya → `pam_escalated_to_ben`. | `pam_managed = true` OR `pam_escalated_to_ben = true` |

#### §4.5.6 Anti-patterns

❌ **Pam accumulating from Hank or Cole scenes** — diner is 2 blocks away; home-based only
❌ **Pam's confrontation with sexual kink register** — witness, not participant
❌ **Pam in Lane 1 or Lane 3** — antagonist shape; no own Lane 3; no hub
❌ **Awareness surfaced to player sidebar** — hidden; dramatic surprise depends on it
❌ **Accumulation from Stages 0–1 Ben beats** — Stage 2+ only
❌ **More than 1 confrontation capstone** — Pam's arc ends at confrontation
❌ **Voyeur-participation "brought-in" branch** — not authoring this; confrontation is non-sexual

#### §4.5.7 Cross-arc state writes / reads

**Writes:**

| State | Trigger | Effect |
|---|---|---|
| `pam_managed` | Confrontation Branch A | Pam silent; no further arc |
| `pam_escalated_to_ben` | Confrontation Branch B | Ben confrontation scene unlocked |

**Reads:**

| State | Source | Effect |
|---|---|---|
| `pam.awareness` | Ben arc write events | Gates confrontation capstone + band-based ambients |
| `ben_stage1` | Ben arc | Awareness accumulation can begin at Stage 2+ |

#### §4.5.8 Cross-references

| Doc | Purpose |
|---|---|
| `doctrine/03_arc_shapes.md` §7 | Antagonist/witness distribution |
| `28th_april_TLS_Phase2_Redesign/60_Diana_Design_Brief.md` | Diana antagonist gold standard |

#### §4.5.10 Acceptance criteria

- [ ] §1: both confrontation branches named explicitly
- [ ] §3: awareness bands + accumulator write-values tabulated
- [ ] §5: laundry room + building front + hallway ambient structure; Lane 3=0 committed
- [ ] §6: 1 confrontation capstone (Type B Pattern F)
- [ ] §7: 8+ anti-patterns; "Pam knows Hank/Cole" explicitly banned
- [ ] §8: accumulator writes from Ben arc cross-referenced
- [ ] Awareness hidden from sidebar committed

---

## §5 Cross-arc World State

### Shared flags

| Flag | Writer | Reader | Effect |
|---|---|---|---|
| `hired_at_diner` | `canvas_hank_hire` | Rosa onboarding; Cole hub; all diner canvases; income system | Diner income active; NPC arcs at diner unlock |
| `rosa_trained_maya` | `canvas_rosa_onboarding` | Rosa T1 canvases | Training complete; colleague register begins |
| `hank_opened_up` | `scene_hank_slow_night_talk` | Hank Stage 1+ | Stage 1 canvases unlock |
| `hank_first_contact` | `scene_hank_first_contact_kitchen` | Hank Stage 2+ | Office hub + Tier 3+ unlocked |
| `hank_after_close_done` | `scene_hank_after_close` accept | Hank Stage 3+ | Tier 3+ explicit canvases |
| `hank_office_first_done` | `scene_hank_office_first` | Hank Stage 4+ | Tier 4 established |
| `hank_cracked` | `scene_hank_declaration` | Hank Stage 5 | Routine intimate |
| `ben_stage1` | Ben dual-path capstone | Ben Stage 1+ | Stage 1 canvases unlock |
| `ben_first_move_done` | `scene_ben_stage2_charged_moment` | Ben Stage 3+ | Stage 3+ unlock |
| `ben_consummation_done` | `scene_ben_consummation` | Ben Stage 4+; Pam awareness +3 | Consummation established |
| `cole_noticed` | `scene_cole_first_break_talk` | Cole Stage 1+ | Stage 1 unlock |
| `cole_walk_done` | `scene_cole_post_shift_walk` | Cole Stage 2+ | Dating chain |
| `cole_date_done` | `scene_cole_first_date` | Cole Stage 3+ | Apartment unlock |
| `cole_first_night_done` | `scene_cole_first_night` | Cole Stage 4 | Explicit routine |
| `pam_managed` | `scene_pam_confrontation` Branch A | — | Pam silent; arc closed |
| `pam_escalated_to_ben` | `scene_pam_confrontation` Branch B | Ben confrontation scene | Ben learns Pam knows |

### Pregnancy system (Phase 2+ included)

- `player.pregnancy` bool (initially false)
- **Bareback commitment:** all sex scenes for Hank, Ben, Cole ship bareback from first explicit beat. No contraception language at any tier. Per Doc 30 §7.3.1.
- **Pregnancy trigger:** cumulative climax events at Stage 4+ with any bareback NPC (simplified flag or on-cycle day model — engine decision at Stage 2)
- **Tier-5 breeding talk (Hank):** unlocked when `player.pregnancy = true` — "I'm going to put a baby in you" / "You want it inside" / "That's mine."
- **Ben breeding-talk range:** unlocked at Stage 4 when `player.pregnancy = true` — incest framing + breeding weight combined
- **Cole Stage 4 pregnancy variants:** separate canvas nodes for pregnant state
- **Ben pregnancy-revelation capstone:** `scene_ben_pregnancy_revelation` fires when `player.pregnancy = true` + `ben_consummation_done`

### Pam awareness system

- `pam.awareness` trait: silent accumulator 0–100; **NOT surfaced to sidebar** (dramatic surprise requires hiding)
- Writer: exclusively Ben arc beats (Stage 2+ threshold; earlier beats = inaudible through wall)
- Reader: Pam band-based ambient canvases (Cold/Suspicious/Knowing); confrontation capstone gate (≥75)
- No daily decay; one-way climb

### Gallery (Phase 2+ included)

Once-only capstones eligible for gallery items (thumbnail + title + replay):

| NPC | Capstones |
|---|---|
| Hank | `canvas_hank_hire`, `scene_hank_slow_night_talk`, `scene_hank_first_contact_kitchen`, `scene_hank_after_close`, `scene_hank_office_first`, `scene_hank_declaration` — **6** |
| Ben | `scene_ben_stage1_via_beauty` OR `scene_ben_stage1_via_glance`, `scene_ben_stage2_charged_moment`, `scene_ben_consummation` — **3** |
| Cole | `scene_cole_first_break_talk`, `scene_cole_post_shift_walk`, `scene_cole_first_date`, `scene_cole_first_night` — **4** |
| Rosa | `canvas_hank_hire` (shared), `canvas_rosa_onboarding` — **1 unique** |
| Pam | `scene_pam_confrontation` — **1** |

**Total once-only capstones: 15.** Gallery threshold (9+) met. Gallery tab ships.

### Pregnancy retrofit compatibility

Per Doc 30 §7.3.1: all sex scenes ship bareback with zero contraception language. This is mandatory regardless of pregnancy inclusion status and enables the Phase 2+ pregnancy mechanic to add parallel pregnant-variant canvases without requiring scene rewrites.

---

## §6 Capstone Chain Map

### Hank chain (Type C, 6 capstones)

```
canvas_hank_hire                          (Type A) → hired_at_diner
  → scene_hank_slow_night_talk            (Type A) → hank_opened_up
    → scene_hank_first_contact_kitchen    (Type A) → hank_first_contact
      → scene_hank_after_close            (Type B Pattern F)
            Accept → hank_after_close_done
            Decline → re-fires next eligible night
        → scene_hank_office_first         (Type A) → hank_office_first_done
          → scene_hank_declaration        (Type A) → hank_cracked → Stage 5 routine
```

### Ben chain (Type C, 3–4 capstones)

```
scene_ben_stage1_via_beauty               (Type A) → ben_stage1  [OR]
scene_ben_stage1_via_glance               (Type A) → ben_stage1
  → scene_ben_stage2_charged_moment       (Type B Pattern F)
          Accept → ben_first_move_done; pam.awareness +2
          Decline → re-fires next eligible evening
    → scene_ben_consummation              (Type A) → ben_consummation_done; pam.awareness +3
      → scene_ben_pregnancy_revelation    (Type A, Phase 2+) → ben_knows_pregnancy
```

### Cole chain (Type C, 4 capstones)

```
scene_cole_first_break_talk               (Type A) → cole_noticed
  → scene_cole_post_shift_walk            (Type A) → cole_walk_done
    → scene_cole_first_date               (Type A) → cole_date_done
      → scene_cole_first_night            (Type B Pattern F)
              Accept → cole_first_night_done
              Decline → re-fires next eligible visit
```

### Rosa chain (2 slice capstones)

```
canvas_hank_hire                          (Type A) → hired_at_diner  [shared with Hank chain]
  → canvas_rosa_onboarding                (Type A) → rosa_trained_maya
    [Phase 3+: Rosa escalation capstone TBD]
```

### Pam chain (1 capstone)

```
[Ben arc awareness accumulation: pam.awareness 0 → 75]
  → scene_pam_confrontation               (Type B Pattern F)
          Branch A → pam_managed (Pam silent; arc closed)
          Branch B → pam_escalated_to_ben
            → [Ben apartment confrontation scene: Ben learns Pam knows; cross-arc NPC dialogue]
```

### Cross-NPC bridges

| Bridge | Trigger | What it does |
|---|---|---|
| Hank hire → Rosa onboarding | `hired_at_diner` | Hank's capstone enables Rosa arc start |
| Hank hire → Cole hub | `hired_at_diner` | All diner NPC canvases require this gate |
| Ben consummation → Pam confrontation approach | `pam.awareness >= 75` | Ben arc drives Pam chain toward close |
| Pam escalated → Ben apartment confrontation | `pam_escalated_to_ben` | Ben and Maya must account for what Pam knows |
| Pregnancy → Hank/Ben/Cole variant scenes | `player.pregnancy = true` | Phase 2+ retrofit activates variant canvases for all three NPCs |

---

## §7 Full-Game Build Plan

### Day 1 (Monday, first shift) — Bootstrap

- Maya walks to loc_diner_front. `canvas_hank_hire` fires on first visit. `hired_at_diner = true`.
- `canvas_rosa_onboarding` fires same visit or Day 2 — Rosa shows Maya the floor.
- Cole at loc_diner_back — Stage 0 co-presence; no arc content yet.
- Ben at home. Kitchen crossover ambient eligible 05:30–06:30 (dice 30%).
- Pam.awareness = 0. First building encounter: `ambient_pam_building_neutral`.
- Day 1 income: $40 + tips ~$20 = ~$60. Starting money $60 → ~$120 after Day 1 shift.

### Day 2–3

- Maya works shifts. Lane 1 Hank hub active at diner_front during 22:00–01:30.
- Cole Stage 0 — Talk available via `cole_diner_back_hub`.
- Ben morning crossover ambients accumulating.
- Rosa T0 relationship builds via Talk interactions.
- Rent Day 1 income tracking: $60 × 4 shifts/week = $240 + tips ~$80 = ~$320 week 1.

### Day 4–6 — First corruption accumulation

- Maya's corruption climbs via Hank Lane 1 (Tease unlocks at corr 5).
- `scene_hank_slow_night_talk` eligible when corr 5 + `hired_at_diner` + 22:00–02:00 empty window.
- Ben Stage 0 ambients: couch reading + kitchen crossover firing regularly.
- Cole break interaction opens when relation 5 threshold approaching.

### Day 7 (Friday) — First rent due

- $125 rent due. With 4 shifts ($240) + tips ($80) = $320 starting money $60 = available ~$380. After rent: ~$255. Comfortable.
- Missed shifts: 2+ missed shifts = $200 income → tight at $135 after rent.

### Day 8–14 — Stage transitions begin

- `scene_hank_first_contact_kitchen` eligible at corr 15 + `hank_opened_up`.
- Ben Stage 1: `scene_ben_stage1_via_beauty` fires if `outfit_corrupted_tier1` equipped; `scene_ben_stage1_via_glance` fires at corr 5 + Ben schedule present.
- `scene_cole_first_break_talk` fires at relation 5+ — Cole Stage 1 begins.
- Pam.awareness 0; accumulation hasn't started (Ben Stage 2 not yet).

### Day 15–21 — Mid-arc progression

- Hank: `scene_hank_after_close` eligible at corr 25 + `hank_first_contact`.
- Ben: charged moments ambient in living_room. `scene_ben_stage2_charged_moment` eligible at corr 25 + relation 15. **Pam.awareness write begins here.**
- Cole: `scene_cole_post_shift_walk` → `scene_cole_first_date` in sequence.
- Rosa T1 at relation 15 — trusted colleague register.

### Day 22–30 — Deep escalation

- `scene_hank_office_first` eligible at corr 35 + `hank_after_close_done`.
- Ben consummation eligible at corr 35 + `ben_first_move_done`. **Pam.awareness +3 write.**
- Cole `scene_cole_first_night` eligible at relation 25 + `cole_date_done`.
- Pam.awareness likely in Suspicious band (25–49) by Day 25–28.

### Day 31–45 — Arc completion milestones

- `scene_hank_declaration` (corr 50 + `hank_office_first_done`) → Hank Stage 5.
- Pam confrontation eligible when awareness ≥ 75 (typically Day 35–40 if Ben chain completed).
- Cole Stage 4 established.
- Phase 2+: `player.pregnancy_eligible = true` in Hank/Ben Stage 4 sex loops.

### Stage-transition milestone schedule

| Milestone | Typical day | Gate condition |
|---|---|---|
| Maya hired | Day 1 | `hired_at_diner` |
| Hank Stage 1 (opened up) | Day 4–7 | corr 5 + `hired_at_diner` |
| Ben Stage 1 (noticing) | Day 6–12 | dual-path via beauty or glance |
| Cole Stage 1 (noticed) | Day 6–10 | relation 5 + `hired_at_diner` |
| Hank Stage 2 (first contact) | Day 10–14 | corr 15 + `hank_opened_up` |
| Ben Stage 2 (charged moments) | Day 12–18 | corr 15 + relation 10 |
| Hank Stage 3 (after close) | Day 14–20 | corr 25 + `hank_first_contact` |
| Cole Stage 2 (dating) | Day 12–18 | relation 10 + `cole_noticed` |
| Ben Stage 3 (first move) | Day 18–25 | corr 25 + relation 15 |
| Hank Stage 4 (office) | Day 20–28 | corr 35 + `hank_after_close_done` |
| Cole Stage 3 (first night) | Day 18–26 | relation 25 + `cole_date_done` |
| Ben Stage 4 (consummation) | Day 22–30 | corr 35 + `ben_first_move_done` |
| Pam confrontation | Day 28–42 | `pam.awareness >= 75` |
| Hank Stage 5 (declared) | Day 30–40 | corr 50 + `hank_office_first_done` |
| Pregnancy onset (Phase 2+) | Day 30–50 | cumulative climax events at Stage 4+ |

### Phase 2+ enable points

| System | Enable condition |
|---|---|
| Breeding talk — Hank Tier 5 | `player.pregnancy = true` + `hank_cracked` |
| Breeding talk — Ben Stage 4 | `player.pregnancy = true` + `ben_consummation_done` |
| Ben pregnancy-revelation capstone | `player.pregnancy = true` + `ben_consummation_done` |
| Cole pregnant-state variants | `player.pregnancy = true` + `cole_first_night_done` |
| Rosa Phase 3+ escalation capstone | TBD Phase 3+ scope (LO triggers this authoring pass) |
| Gallery tab | Populates as capstones complete (threshold 9+ met by ~Day 20) |

### Endgame state (completed game per Doc 65)

A completed playthrough has:
- **Hank Stage 5:** diner is home in a different sense; "come in through the back" is established routine; bareback possession complete; breeding talk active (Phase 2+)
- **Ben Stage 4:** consummation acknowledged by both; incest callouts held through the act; Pam confrontation resolved (managed or escalated); pregnancy revelation if applicable
- **Cole Stage 4:** the night-shift cook who barely talks took Maya home in the gray hours; explicit routine established
- **Rosa T1:** trusted colleague; Phase 3+ adultery seduction deferred pending LO scope
- **Pam:** confrontation resolved — managed (pam_managed) or escalated (Ben knows Pam knows)
- **15 gallery items unlocked** across all capstone chains
- **(Phase 2+)** At least one NPC's breeding-talk vocabulary active; pregnancy-revelation scene completed

---

**End of Stage 1 design book.** Next: `stages/02_toml_generation_prompt.md` for TOML emission across 7 phased files into `games/late_shifts/toml_phases/`.
