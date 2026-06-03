# Reference 01 — Road to Success (RTS) Overview

**Source:** Doc 13 (`28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md`, 2026-05-02 + §16 update 2026-05-03); `game_explorations/rts-arc-trace/notes.md`; live extraction across multiple sessions May 2026.
**Authority:** Reference. The sole reference game per LO §6.3.
**Purpose:** Name what RTS IS — the game shape, the size, the player loop, the chrome surfaces, the bootstrap experience. Doctrine files cite this for the "what does the reference game DO" question.

This file is the broad overview. Per-NPC scene catalogs in `reference/02_rts_scene_catalog.md`. Walkthrough doctrine in `reference/03_rts_walkthrough_panel.md`. HUD doctrine in `reference/04_rts_hud_world_model.md`.

---

## §1 — What RTS is

**Road to Success (RTS)** — adult interactive fiction, SugarCube/Twine-based. Source: `https://mopoga.com/road-to-success` v0.25. Captured locally in `game_explorations/rts-arc-trace/` across multiple exploration sessions.

The game RTS-shape sandboxes are modeled on. Every principle in `doctrine/01_rts_principles.md` (P1–P10) was extracted live from this game. Every mechanism in `doctrine/02_three_lanes_plus_capstone.md` was verified against this game's passage source. Every anti-pattern in `doctrine/07_anti_patterns.md` was tested against this game's behavior.

**LO decision §6.3:** RTS is THE reference. Not Jack's World. Not New In Town. Not Two Weeks. When a doctrine question arises and the answer isn't already specified, the question is: *"What does RTS do here?"*

---

## §2 — Game shape at a glance

Doc 13 §3 — verified counts via `eval(Story.passages)` + walkthrough panel + per-NPC `scenes` extraction:

| Dimension | Count | Notes |
|---|---|---|
| **NPC keys defined** | 53 | 16 with predefined `scenes` objects; 37 stub-only (location + name, scenes populate when player meets them) |
| **NPC-bound scenes** | ~60 | Per Walkthrough panel: Stepfather 12, Stepbrother 15, Stepgrandfather 6, Marcus 5, Sam 2, Emma 1, Jamal 3, Veronica 3, Priest 2, Mr. Matthew 1, Edward 4, Tow Truck Driver 1, Yacht Captain 1, Thief 2, Josh 1, Landlord 1, Gangster 1 |
| **Location-bound scenes** | ~70 | City Center 1, House 1, Bus 3, Photo Studio 2, School 12, Park 9, Gym 3, Mall 3, Night Club 2, Beach 7, Bar 4, Public Pool 2, Office 2, Driving School 1, Thomas's House 2, Strip Club 3, Clandestine Clinic 2, Restaurant 5, Police Station 1, Hospital 2, Abandoned Building 1, Gas Station 1, Movie Theater 2 |
| **Total scenes** | 130+ | The "content library" RTS sells |
| **Quest definitions** | 27 | 3 active at game start (`SchoolTest`, `MathHomework`, `INeedMoney`); 24 latent (activate on trigger conditions) |
| **Locations** | 41 | House sub-rooms + Residential + cityZones |
| **Calendar** | 7-day week × 6 time buckets | EM (Early Morning) / M (Morning) / A (Afternoon) / E (Evening) / N (Night) / LN (Late Night) |
| **Pacing** | ~30 turns per ~1 in-game day | One significant arc beat per day per NPC of focus |

**Key takeaways for RTS-shape sandbox authoring:**

- **130+ scenes is the content library**. RTS-shape games aren't 12 long arcs; they're many short scenes with overlapping mechanics.
- **53 NPCs with 16 active arcs** — the rest are NPCs the player meets later (e.g., Natasha unlocks via Library encounter). For TLS-shape slice scope: 4–6 fully-authored NPCs, with stubs prepared for "meet later" NPCs.
- **70 location-bound scenes vs 60 NPC-bound** — locations themselves have content (Beach 7, School 12). For TLS: solo-Maya activities at locations count as content surfaces (Lane 3 dispatcher mechanism).
- **6 time buckets × 7 day** — RTS uses a smaller time-buckets-per-day count than TLS's 24-hour clock. For TLS-shape games: time grain is implementation choice; RTS-style 6-band model is simpler for player planning.

---

## §3 — The 3 arc shapes (tendencies, not categories)

Doc 13 §5 originally framed 3 arc shapes; Doc 13 §16 Correction 7 refined to "tendencies, not categories" — every RTS NPC mixes random + deterministic + time-gated triggers; the RATIO differs.

The 3 tendencies:

| Shape | Trigger | Gating style | Player loop | Example NPCs |
|---|---|---|---|---|
| **Family / ambient escalation** | Random encounter on room entry, dice roll (20–33%) | NPC arousal emoji + MC corruption thresholds; relation always 0 (no narrative chain) | Visit room → maybe scene fires → repeat. Same action ("Study") triggers different scenes at different stat tiers. | Brother (15 scenes), Dad (12), Grandpa (6) |
| **Peer / quest chain** | Deterministic (chance=100) except minor variants | Narrative prerequisites in `guide` string: "Take the test and get at least an 8 grade", "Have at least 15 relationship points", "wait for his invite" | Read walkthrough → execute discrete prerequisite → unlock next deterministic beat. Traditional VN. | Marcus (5 scenes), Natasha, Sam, Emma |
| **Career / digital** | Deterministic + external metric + time delay | "Reach 1000 followers on Instafame", "wait 10 days, read message", "wait 15 days, read message" | Phone-mediated async. Grind followers → wait calendar days → respond to DM → date. | Edward (4 scenes), Jim (Pornstar), Richard (Photographer) |

### What each shape feels like

**Family arc (ambient escalation).** Player isn't "progressing a story" — they're raising stats, walking around home, and watching content gradually escalate. Reads as low-effort/high-frequency. Bootstrap: flash/tease at MC corruption 5 (chance 100) raises NPC arousal — once arousal > 0, random-encounter scenes become possible on bedroom visits. Family runs in *background* of the player's attention.

**Peer arc (quest chain).** Discrete, planned, sequential. Player has a checklist: "do the prereq → unlock the deterministic beat." Marcus arc requires MC corruption=0 mostly — peer/school is the "wholesome" track. This is what the player *focuses on this session*.

**Career arc (metric + time + DM).** Patient/calendar-driven. Edward DM widget literally arrives on the player's phone after a follower threshold + wait period. The player grinds Instafame followers across many in-game days while the family arc passively unfolds. This is the *long-burn project across weeks*.

**The 3 shapes give DIFFERENT TEMPOS so the player isn't always doing the same thing.**

### Refinement (Doc 13 §16 Correction 7)

The clean "three shapes" framing was a story extracted from data; live play shows every NPC mixes triggers. More honest framing:

> RTS gives every NPC a mix of random + deterministic + time-gated triggers; the ratio differs per NPC.

- **Brother** = "mostly random + significant deterministic" (15 scenes: 7 Lane 3 substitution / 5 Lane 1 hub / 3 Lane 2 random)
- **Marcus** = "mostly deterministic + tiny random splash" (5 scenes: 5 deterministic / 0 substitution / 0 random)
- **Edward** = "metric+wait + DM-mediated deterministic" (4 scenes: all deterministic via DM widget gate)

The 3 shapes are **tendencies**, not categories. TLS-shape sandbox NPC arc shapes (`doctrine/03_arc_shapes.md` 5 shapes) refine the RTS tendencies into more specific mechanical rhythms (family/ambient + slow-burn family + peer/dating + service + antagonist/witness).

---

## §4 — Bootstrap experience (Doc 13 §12 — turn-by-turn play log)

Captured live 2026-05-02. ~30 meaningful clicks Day 1 EM → Day 2 EM. Reading top-down gives the actual feel of a fresh playthrough.

### Day 1 — bootstrap timeline

| Turn | Action | Result | Stat / state delta |
|---|---|---|---|
| 1 | (start) | Day 1 Monday EM, Bedroom, Victoria | corr 0, ar 0, exhi 0, energy 100, $50, intel 0, beauty 0 |
| 2 | Auto-advance through intro | Lands at Bedroom passage | — |
| 4 | Click `Study 📖` | "STUDY / You studied an hour and feel smarter!" | intel +1, energy −10, time M |
| 6 | Click sidebar `🏫 Go to School` | **Silent fail** — passage stays Bedroom | Player wearing casual clothes (no error message — first surprise) |
| 7 | Wardrobe → School 1 image | clothing equipped | clothing.type = "school" |
| 8 | `Go to School` | School hub loads | — |
| 9 | Click `History Class ⚔️` → `Study 📖` | "feel smarter" — **NEW QUESTS unlocked** | intel +1, time A; SchoolTest + MathHomework activate |
| 11 | Leave school → House → Hallway | — | family schedule check: Dad=Work, Brother=School, Grandpa=Kitchen |
| 14 | `Hallway 🚪` → `Bedroom` (Brother's bedroom) | **🎯 PeepBrotherSex random-encounter fires** at MC corruption 0 | scene = PeepBrotherSex |
| 15 | Read scene + image + [Peep] [Hallway] | — | — |
| 16 | Click `Peep` | linkreplace adds: paragraph + VIDEO `masturbate1.mp4` + new choice [Stroke your pussy] | MC arousal 0 → 1 |
| 17 | Click `Stroke your pussy` | linkreplace adds: "You are not aroused enough to do this" | (no further reveal at corr 0) |
| 18 | Hallway → DadBedroom | **🎯 ProstituteSex (Dad scene) random fires** at MC corruption 0 | — |
| 19 | Click `Peek 👀` | image + "Stepfather having sex with a prostitute" + [Keep Watching] | MC arousal 1 → 2 |
| 20 | Click `Keep Watching` | **linkreplace adds EMPTY content** — scene truncates at corruption 0 | (Doc 13 §11 Correction 2: every visit shows opening; high-corruption returns reveal more) |
| 21 | Re-enter BrotherBedroom | PeepBrotherSex does NOT re-fire (`!executedToday` flag) | (verifies daily cap) |
| 22 | Click `Have sex with him 🔥` (gated, MC corr 0 < 3) | **Silent visual fail**. Source has `<<NotifyCorruption 4>>` for threshold publish. Corruption stays 0 (Doc 13 §11 Correction 3) | — |
| 24 | Sleep → Day 2 EM | — | day +1, energy 100, MC arousal 2 → 3 |
| 28 | Library | "There is a girl at the reading tables..." + [Say hello] | (excellent character setup line) |
| 29 | Click `Say hello 📚` | **🎯 Tier-3 scripted intro: Natasha** | speaker label changes "Student" → "Natasha" once names exchanged |

### Bootstrap takeaways

- **Day 1 Evening = first taboo content beat.** No grinding required.
- **Two random encounters fired naturally** in <5 moves.
- **One quest cascade** happened automatically (FirstDayOfShool auto-completed → SchoolTest + MathHomework activated).
- **One Tier-3 intro scene** was discoverable (Library → Natasha).
- **Three soft/notify-fail attempts** taught the thresholds without punishing.
- **No explicit tutorial outside the Walkthrough panel** — rest is learned by doing.

### Implications for RTS-shape sandbox authoring

- **Hand the player content immediately.** Day 1 Evening should have at least 1–2 taboo content beats. Don't gate the first 30 minutes behind grinding.
- **First 30 minutes should fire at least 2 random encounters.** Lane 2 ambient mechanism via dice on entry (per `doctrine/02_three_lanes_plus_capstone.md` §3).
- **First 30 minutes should include 1 Tier-3 scripted intro.** Named NPC introduction (e.g., Natasha at Library) — sets the literary quality bar players will see again at Lane 4 capstones.
- **No tutorial outside the walkthrough.** Discoverability lives in the Walkthrough panel (P2 transparent gating) + the sidebar (P10 HUD = world model).

---

## §5 — The economic + time engine (Doc 13 §10)

### Player stats

| Stat | Range | Mutation cadence | Notes |
|---|---|---|---|
| `corruption.points` | 0–∞ | Per masturbation / accept-taboo-action | Accumulates |
| `corruption.level` | 0–5+ | Derived from points (tiered: Pure / Lewd / Slutty / Whore...) | Used in gates as `getCorruptionLevel() >= N` |
| `exhibitionism` | 0–∞ | Per flash / public-nudity action | Independent axis from corruption |
| `beauty` | 0–∞ | Per gym, makeup, salon | Visible in left sidebar |
| `intelligence` | 0–∞ | Per Study / class | Used for school grade gates |
| `energy` | 0–100 | -10 per tick of activity, +N on rest | Hard cap forces sleep cycle |
| `arousal` | 0–10 | +1/day passive, +1 per peep beat, set by scenes | Required > 0 for masturbation, sex |
| `money` | 0–∞ | Earned via jobs, lost on rent / shopping | Drives apartment / car / phone unlock chain |
| `hunger` / `hygiene` | 0–100 | Decay over time | Force eating / showering loops |
| `clothing.type` / `clothing.name` | enum | Wardrobe equip | Gates location entry (school requires `school1`, naked requires corruption ≥ 3 to leave bedroom) |

### NPC stats (per `$npc.<key>`)

| Stat | Range | Notes |
|---|---|---|
| `arousal` | integer 0–N | Stored as integer (Brother arousal observed at `1`, `3`, `5`). The 🔥/🔥🔥/🔥🔥🔥 in Walkthrough display is threshold format, not storage format. Passive +1/day for in-scope family NPCs. |
| `corruption` | 0–∞ | Integer. Raised by player taboo actions toward this NPC. |
| `relation` | 0–∞ | Integer. Always 0 for family arcs (no narrative chain); meaningful for peer arcs. |
| `talkedToday` | bool | Once-per-day Talk gate. |
| `location` | string | Schedule-driven by tick (Brother: bathroom EM, school M+A, bedroom E+N+LN). |
| `scenes` | object | Per-scene state: `{unlocked, executedToday, gallery flag}`. |

### Time + economy

- **6 buckets per day:** EM / M / A / E / N / LN
- **7-day week:** Monday → Sunday
- **`$game.days`** = lifetime day counter (driving "wait 10 days" mechanics)
- **Activities `<<AddTime N>>`** advance N buckets
- **Money drives engagement:** rent on apartment, $400 for phone, etc. Force player to engage with peer/career arcs (jobs).

### Composition rule

> The same room can show different button sets per state.

A canonical example: Brother's bedroom at LN with Brother present + relation ≥ 10 shows "Sleep with him." At E with Brother present + corruption < 3 shows Talk/Tease/Flash/[Have sex *gated*]. At M (Brother at school) shows "is at school" + Hallway only.

The **clothing × location × time × stats** product is the gating space. Gates compose from layered conditions, not central rule tables. This makes the world feel rule-bound while keeping each individual gate readable in its own passage.

---

## §6 — The 4 RTS player surfaces

RTS presents content through 4 distinct UI surfaces. Each has its own doctrine for what belongs there.

### §6.1 — The location passage (the actual game world)

Where Maya is right now. Renders:
- Image of the location
- Time-of-day + day + weather (small banner)
- Menu of available activities (clothing-gated, time-gated, energy-gated, purchase-gated)
- Random-encounter override block (Lane 2 — see `doctrine/02_three_lanes_plus_capstone.md` §3)

This is what the player spends most of their time looking at.

### §6.2 — The Walkthrough panel (the published catalog)

The `📕 Walkthrough` button in the right sidebar opens a passage that **literally renders the scene table as data to the player**. Same fields as the engine's internal scene struct, just formatted as a table. (Detailed in `reference/03_rts_walkthrough_panel.md`.)

The player loop is literally: *open Walkthrough → pick a locked scene close to unlocking → read its requirements → close the gap → re-attempt.*

### §6.3 — The right sidebar (the HUD = world model)

Continuously surfaces:
- Time (Early Morning, Monday, Clear weather)
- Quest pin
- Per-NPC rows: Stepfather: Kitchen / Arousal / Corruption / Stepbrother: Bathroom / Arousal / Corruption / Stepgrandfather: Bedroom / Arousal / Corruption

Updates every tick. No menu click required to check NPC state. (Detailed in `reference/04_rts_hud_world_model.md`.)

### §6.4 — The phone app (career/digital surface)

Phone is a purchased item ($400 + first NPC's allowance unlocks it). Once acquired, the phone has multiple "apps":
- Messages (chat threads with NPCs)
- Instafame (social_feed + DM-driven career arc)
- Photo gallery
- Quests journal
- Custom apps

Phone is async-mediated content (Edward DM arrives after follower threshold + wait). Phone is NOT load-bearing for family/ambient arcs — those run via location passages + walkthrough.

### §6.5 — City map + location locking (live-verified 2026-06-03)

Live-play of `road_to_success` (introspected the `CityMap` macro handler + `$location` state; notes in `game_explorations/road_to_success/notes.md`). RTS locks **venues** (never districts — center/residential/elite/ghetto are always reachable via the Bus Stop) on **two orthogonal axes**:

| Axis | Field | Player experience |
|---|---|---|
| **Discovery** | `unlocked` (bool) | `CityMap` renders **nothing** when `unlocked === false` → the venue is **absent** from the map. The player can't see a place they haven't discovered. Verified: at game start the Residential map omits Marcus's/Emma's houses; the Elite map shows only Casino + Bus Stop (all three mansions hidden). |
| **Time** | `open` (bool, derived from `openPeriods` vs `$game.time`) + `opensAt` label | When `unlocked` but `open === false`, the tile **is** shown — darkened with a 🔒 + a "CLOSED / Opens at \<opensAt\>" badge; clicking it is a **no-op** (you stay on the map). Verified at early-morning Center: Night Club "Opens at Night," Bar "Opens at Evening," Movie Theater "Opens at Morning." |

**Discovery unlock = meeting the person tied to the place.** `<<UnlockLocation X>>` (→ `LocationService.unlockLocation`) fires at the in-fiction *meet / invite / "address sent"* beat — the lock literally means "you don't know them / where they live yet":

| Unlock | Trigger beat | Story |
|---|---|---|
| jamalHouse | `JamalMeet` | meet Jamal at the Club; "I'll see you again, right?" |
| veronicaHouse | `VeronicaMeet` | a sexual encounter with Veronica |
| marcusHouse | `SchoolTest` | the school test starts the "Study with Marcus" quest |
| emmaHouse | `EmmaInvite` | Emma: "I'll wait for you at my house in evening" |
| clandestineClinic | `HospitalBirth` | the doctor refers you to a friend's artificial-womb clinic |
| vipers (gang HQ) | `DrugDealer` | the drug-dealer questline opens the hideout |
| photoStudio / filmStudio / hotel | phone DMs (`InstafameMessages`) | Richard/Jim/Edward each "send you the address" + a `NotifyPhone "X is now unlocked on the city map"` signal |

**How our engine adapts it.** We have only a flag lock: `[[locations]]` `entry_conditions` + `blocked_message` — **visible-but-blocked** (the door shows and tells you why), not RTS-style hide; and **no native time-of-day location lock** (time/exposure lives on the hub, D72-R7). The coordination rule (a locked location that hosts an NPC schedule — Cases A/B/C, the unlock contract, the schedule-page leak if we ever adopt discovery-hiding) is `doctrine/10` §5.4.

---

## §7 — Three writing tiers (Doc 13 §9)

RTS doesn't write every scene at the same density. There are three observable tiers, each used deliberately for a class of moments.

### Tier 1 — Utility one-liner (~30 of 130 scenes, ~23%)

> **STUDY**
> You studied an hour and feel smarter!
> [Return ↩️]

Used for: bedroom Study, Sleep, Nap, generic activity-passes ("Socialize: You waste time socializing with your classmates").

Function: pure mechanical confirmation. The text exists only to make the stat-tick acknowledgment feel like *something*. ~10 words.

### Tier 2 — Vignette prose (~70 of 130 scenes, ~54%)

> **Stepbrother's Bedroom**
> You push open the door to your Stepbrother's room, only to stop dead in your tracks. He's in bed with a girl, their bodies tangled together... and they're definitely not just sleeping!
> [Peep]

Used for: random-encounter scenes with anonymous partners (Brother with "a girl," Dad with "a prostitute," generic strangers in public exhibitionism scenes).

Function: bridges mechanic to content. Generic descriptive prose with named situations but un-named NPC partners. ~30–50 words per beat, 2–4 beats per scene via linkreplace.

### Tier 3 — Scripted character (~30 of 130 scenes, ~23%)

> **A QUIET CORNER**
> *Most of the tables are empty. She slips something into her book to hold the page and looks up when you get close. Same girl from the hallway. This is the first time you actually stop to talk.*
>
> Victoria: Hi. Mind if I sit?
> Student: Yeah, go ahead. I'm just hiding from the hallway noise.
> Victoria: Fair. I'm Victoria.
> Student: Natasha. I come here when I need to study and people won't shut up out there.
> Natasha: Anyway. Don't be a stranger. I'm here most days.
> [Return ↩️]

Used for: named-NPC introductions, quest beats, arc transitions, Edward's DM widgets (10+ Speech beats with personality and seductive escalation).

Function: real character writing. Sensory grounding (*"She slips something into her book to hold the page"*). Voice (*"hiding from the hallway noise"* — introvert framing). Live-changing speaker labels (*"Student" → "Natasha"* once names exchanged). This is the layer that earns RTS its narrative weight.

### Distribution discipline

**The author doesn't waste Tier-3 prose on Tier-1 moments.** Reserved for transitions and named characters. This budget discipline is part of why a 130-scene game ships at all.

For TLS-shape sandboxes: Lane 1/2/3 = Tier 1 + Tier 2 default. Lane 4 capstones = Tier 3 earned. See `doctrine/05_rts_flat_prose.md` for the dual-register doctrine.

---

## §8 — Empirical corrections (data-extraction was wrong)

Doc 13 §11 captures 5 corrections from live play that disproved source-only inferences. Methodologically important: source-code extraction is fast but generates wrong inferences. Live play is slow but corrects them.

### Correction 1: Walkthrough requirements aren't strict gates for random encounters

**What was claimed (data-extracted):** Triple gating — NPC stats AND Player stats AND probability — strictly enforced.

**What actually happens:** `BrotherBedroom` random-encounter check is ONLY `previous()=="Hallway" && random(1,4)==1 && !executedToday`. The `requirementsMC.corruption: 15` field listed in walkthrough for `PeepBrotherSex` is **bypassed**. Live verified: scene fired at MC corruption 0 on Day 1 Evening.

**Implication:** the walkthrough's "REQUIREMENTS (MC)" column is a **suggested threshold for the FULL content version**, not an entry gate. Player can stumble into scenes early and get a teaser; full content unlocks later.

### Correction 2: Higher stats unlock MORE CONTENT inside a scene, not access TO the scene

**What actually happens:** Every visit shows the entry text + image + first beat. Linkreplace beats *after* that branch by stat. Live verified: clicked "Keep Watching" on Dad's `ProstituteSex` at MC corruption 0 → linkreplace inserted **empty content**. Scene literally has no more body for the player.

**Implication:** every scene has a "low-corruption short version" and a "high-corruption full version" inside the same passage. Player can't be punished for trying. Player knows there's more, comes back later.

### Correction 3: `<<NotifyCorruption N>>` is a UI hint, NOT a corruption-adder

**What was claimed:** "Failing taboo actions raises corruption — rejection trains the player. Brilliant design loop."

**What actually happens:** `<<NotifyCorruption N>>` is a *UI feedback widget* that displays "you need corruption level N for this." Always called in the ELSE branch with N matching the required level. Pattern verified across 5+ widget definitions.

**Live verified:** clicked "Have sex with him 🔥" at MC corruption 0 → notification appeared, **corruption.points stayed 0**.

**Implication:** the rejection-trains-corruption loop **does not exist** in RTS. Failure is *information* (publishes the threshold), not *progress*. P7 in `doctrine/01_rts_principles.md`.

### Correction 4: Watching/peeping itself raises MC arousal

**What was missed:** Voyeur scenes have +arousal effects baked in.

**What actually happens:** Live observed — peeping at `PeepBrotherSex` raised MC arousal 0 → 1. Clicking "Keep Watching" on Dad's `ProstituteSex` raised it 1 → 2. Sleeping overnight raised it 2 → 3 (matches walkthrough "+1 arousal each day").

**Implication:** scenes carry their own stat-effect side-channels separate from the explicit "stat-raising activities" (masturbate / gym / etc.). Stats and content interleave. P6 in `doctrine/01_rts_principles.md`.

### Correction 5: Quest descriptions are story flavor, not hard timers

**What was assumed:** "I need to take the school test on Monday" implies a Monday deadline.

**What actually happens:** Slept past Monday → quest still active Tuesday with same description.

**Implication:** quest description text is for atmosphere/orientation, not for mechanical scheduling. RTS doesn't time-out quests.

### Methodological note

**Source-code extraction generates wrong inferences ~30% of the time.** Live play is the only way to verify. For prompts_v2/ work: never claim "RTS does X" without source + live verification. The 5 corrections above were confident-but-wrong from data alone.

---

## §9 — Playthrough 2 additional findings (Doc 13 §16, 2026-05-03)

A second focused playthrough sampled Brother's content to near-exhaustion. Key additional findings:

### NPC interior thought bubbles are a runtime UI primitive (Finding 1)

RTS uses a styled Speech-thought macro to render NPC interior monologue:

> 💭 Alfred is thinking...
> *"I can't help myself... she looks so peaceful, so innocent. I just need to touch her..."*

This is a 4th-dimension writing primitive beyond the three tiers. Used in `BedroomSleepDadScene` (3 thought bubbles across 3 beats). Distinctly styled (italic + 💭 + "thinking..." attribution row).

For TLS-shape sandboxes: TLS has `thought_bubble` block type (shipped 2026-05-06). See `doctrine/05_rts_flat_prose.md` §7.

### Deterministic scenes also have stat-tier branching (Finding 2)

Doc 13 §11 #2 said "every visit shows something + content branches inside scenes." The branching applies to *deterministic* scenes too, not just random encounters:

- `SleepingBrother` walkthrough says "100% chance" — but at relation 12 the scene plays a 134-word *rejection* outcome ("Brother wakes, tells player to leave"). Higher relation (likely 25+) gates the consummation outcome.
- `BrotherCaughtMasturbating` at MC corr 6 plays the disgusted-rejection variant (5 lines). At MC corr 31 a new `[Shhh]` choice appears → full sex sequence (~590 words).

**Implication:** the walkthrough's `CHANCE: 100%` means the trigger always fires when reqs met, but the *content within* still gates by stats. P3 in `doctrine/01_rts_principles.md`.

### Real branching choices DO exist, just rare (Finding 3)

`SellingMyStepsister` has a real meaningful narrative `[Accept]/[Refuse]` choice that materially diverges downstream. Real player-choice branching is rarer than stat-gated reveals, but it does exist for major story moments.

**Pattern:** high-stakes scenes get player choice (Pattern F per Doc 57); everyday encounters get linkreplace-drip (Patterns A/B/C/D/E per `reference/02_rts_scene_catalog.md`).

### Passive NPC arousal accumulation (Finding 4)

Brother arousal observed climbing 0 → 1 → 2 → 3 across 3 in-game days *without anything done to him*. NPCs have a passive arousal trickle, not just MC-driven.

**Implication:** Doc 40 doctrine — both player + NPC arousal are always-climbing meters; passive +1/day for in-scope family NPCs.

### Being groped raises MC corruption (Finding 5)

Tutorial says "1 arousal per day OR after being groped." Live observed: BedroomGrope scene gave MC +1 corruption.

**Implication:** passive groping accelerates corruption naturally without active choices. The bootstrap loop is faster than tutorial implies — around 30-50% of corruption gain in early game can come from just walking around.

---

## §10 — Cross-references

### Sibling reference files

- `reference/02_rts_scene_catalog.md` — per-NPC scene tables (Brother / Father / Marcus / Edward with lane classifications + GUIDE strings + cumulative stat ladders)
- `reference/03_rts_walkthrough_panel.md` — Walkthrough panel doctrine (P2 transparent gating)
- `reference/04_rts_hud_world_model.md` — sidebar doctrine (P10 HUD = world model)

### Source

- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` — primary source
- `game_explorations/rts-arc-trace/notes.md` — 8 timestamped observation blocks
- `game_explorations/rts-arc-trace/passage_catalog.json` — 361 passages (engine source code)
- `game_explorations/rts-arc-trace/scene_bodies.jsonl` — 274 scene bodies (P1 length distribution evidence)
- `game_explorations/rts-arc-trace/ui_map.json` — HUD chrome catalog (P10 evidence)

### Sibling doctrine files (this reference informs)

- `doctrine/01_rts_principles.md` — P1–P10 derived from RTS extraction
- `doctrine/03_arc_shapes.md` — 5 TLS arc shapes refine RTS's 3 tendencies

---

**End of file.** Next: `reference/02_rts_scene_catalog.md` for the per-NPC scene catalogs.
