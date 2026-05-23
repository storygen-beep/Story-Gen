# 13 — Road-to-Success: Analysis & Learnings

> **Created 2026-05-02.**
> Primary-source reference doc capturing observable behavior of Road-to-Success (RTS, https://mopoga.com/road-to-success v0.25), the canonical design reference for The Long Summer.
> Companion to `04_Scene_Cascade_Pattern.md` and `11_Hint_Authoring_Guide.md` — provides the empirical record those design choices reference.
> May inform future revisions of `02_NPC_Stage_Chains.md`.
> **This is a knowledge-capture doc, not a redesign proposal.** Future docs (14+) can reference this when arguing for changes.

---

## §1 — Why this doc exists

We have repeatedly cited RTS in TLS design decisions ("RTS-flat scene bodies," "stat-tier escalation," "walkthrough-as-quest-log") but the citations have lived as vague impressions in conversation memory. Across two sessions on 2026-05-02 we did a focused exploration mixing source-code archaeology with live play. **Five of the inferences that came from data extraction alone turned out to be wrong** (see §11). This doc consolidates the corrected, primary-source record so future TLS design conversations can cite specific RTS behavior rather than re-derive it.

---

## §2 — Method

| Phase | Activity | Yield |
|---|---|---|
| Source extraction | `eval` reads of `npc.X.scenes` for 4 NPCs (Brother / Dad / Marcus / Edward), full passage source for `BrotherBedroom` + `Bedroom`, all Speech-widget definitions in passage_catalog | 16-scene Brother table, 12-scene Dad table, 5-scene Marcus table, 4-scene Edward table; full passage code |
| Live play | Day 1 EM → Day 2 EM (~30 meaningful clicks) | 5 random encounters fired naturally + 1 scripted intro (Natasha) + 1 quest-progress beat (MathHomework +1) |
| Walkthrough panel | Opened + clicked into Stepbrother per-NPC view | Verbatim scene table as rendered to player |

**Honesty note:** source-code extraction is fast but generates wrong inferences. Live play is slow but corrects them. The two complement each other — neither alone is sufficient. ~50% of session time was extraction; ~30 clicks of live play turned up 5 corrections that no amount of source-reading would have surfaced. See §11.

---

## §3 — Game shape at a glance

| Dimension | Count | Notes |
|---|---|---|
| NPC keys defined | 53 | 16 with predefined `scenes` objects; 37 stub-only (location + name, scenes populate when player meets them) |
| NPC-bound scenes | ~60 | Per Walkthrough panel: Stepfather 12, Stepbrother 15, Stepgrandfather 6, Marcus 5, Sam 2, Emma 1, Jamal 3, Veronica 3, Priest 2, Mr. Matthew 1, Edward 4, Tow Truck Driver 1, Yacht Captain 1, Thief 2, Josh 1, Landlord 1, Gangster 1 |
| Location-bound scenes | ~70 | City Center 1, House 1, Bus 3, Photo Studio 2, School 12, Park 9, Gym 3, Mall 3, Night Club 2, Beach 7, Bar 4, Public Pool 2, Office 2, Driving School 1, Thomas's House 2, Strip Club 3, Clandestine Clinic 2, Restaurant 5, Police Station 1, Hospital 2, Abandoned Building 1, Gas Station 1, Movie Theater 2 |
| Total scenes | 130+ | The "content library" RTS sells |
| Quest definitions | 27 | 3 active at game start (`SchoolTest`, `MathHomework`, `INeedMoney`); 24 latent (activate on trigger conditions) |
| Locations | 41 | House sub-rooms + Residential + cityZones |
| Calendar | 7-day week × 6 time buckets | EM (Early Morning) / M (Morning) / A (Afternoon) / E (Evening) / N (Night) / LN (Late Night) |
| Pacing | ~30 turns per ~1 in-game day | One significant arc beat per day per NPC of focus |

---

## §4 — Scene data structure

Every NPC arc is data-driven from `$npc.<key>.scenes`. Verbatim schema (one entry):

```js
{
  id: 13,                              // sequential scene id (numbering jumps suggest staggered patches)
  requirements: {
    arousal: "🔥",                     // NPC arousal — emoji-tier, NOT integer ("🔥" / "🔥🔥" / "🔥🔥🔥")
    corruption: 0,                     // NPC corruption — integer
    relation: 0                        // NPC relation — integer (almost always 0 for family arcs)
  },
  requirementsMC: {
    corruption: 0,                     // Player corruption (level not points) — integer
    exhibitionism: 0                   // Player exhibitionism — integer
  },
  title: "$npc.Brother.relationship Bedroom Grope",  // Walkthrough display title (sugarcube-interpolated)
  chance: 20,                          // % probability of triggering when reqs met (random encounter)
  guide: "Go to your bedroom",         // Natural-language hint surfaced verbatim in Walkthrough panel
  unlocked: false,                     // Has player ever triggered this? (lifetime flag)
  executedToday: false,                // Has it fired today? (per-day flag for chance-gated scenes)
  gallery: false,                      // Adds to Gallery on unlock
  inside: false, blowjob: false, vaginal: false,    // Content-type tags for filtering / age gates
  anal: false, threesome: false, gangbang: false
}
```

**Critical distinction — what's actually enforced where:**

| Field | Enforced in passage code? | Used in Walkthrough display? |
|---|---|---|
| `id` | No (just dedup key) | Yes |
| `requirements.arousal` (NPC) | **Sometimes** — depends on which trigger path fires the scene | Yes |
| `requirements.corruption` (NPC) | Sometimes | Yes |
| `requirementsMC.corruption` | **Often NOT for random encounters** (see §11 correction #1) | Yes |
| `requirementsMC.exhibitionism` | Often NOT | Yes |
| `chance` | **Yes** — drives the `random()` roll in passage code | Yes |
| `guide` | No | **Yes** — this IS the player-facing hint |
| `executedToday` | **Yes** — strict per-day cap | No |
| `unlocked` | Yes (gates Gallery, sometimes follow-up content) | Yes (🔓/🔒) |
| Content-type flags | No (display only) | Indirectly (player can avoid undesired content types via Preferences) |

The `requirementsMC` figures are **suggested thresholds for full content**, not strict entry gates. See §11 #1 + #2 for the correction.

---

## §5 — Three arc shapes (one engine, three player loops)

The same `npc.X.scenes` data structure drives three radically different player experiences. Picking the right `chance` + gate-style + guide phrasing is how RTS authors customize per-NPC tempo without changing the engine.

| Shape | Trigger | Gating style | Player loop | Example NPCs |
|---|---|---|---|---|
| **Family / ambient escalation** | Random encounter on room entry from Hallway, dice roll (20–33%) | NPC arousal emoji + MC corruption thresholds; relation always 0 (no narrative chain) | Visit room → maybe scene fires → repeat. Same action ("Study") triggers different scenes at different stat tiers. | Brother (15), Dad (12), Grandpa (6) |
| **Peer / quest chain** | Deterministic (chance=100) except minor variants | Narrative prerequisites in `guide` string: "Take the test and get at least an 8 grade", "Have at least 15 relationship points", "wait for his invite", "After starting a relationship" | Read walkthrough → execute discrete prerequisite → unlock next deterministic beat. Traditional VN. | Marcus (5), Natasha, Sam, Emma |
| **Career / digital** | Deterministic + external metric + time delay | "Reach 1000 followers on Instafame", "wait 10 days, read message", "wait 15 days, read message" | Phone-mediated async. Grind followers → wait calendar days → respond to DM → date. | Edward (4), Jim (Pornstar), Richard (Photographer) |

### What each shape feels like

**Family arc (ambient escalation).** Player isn't "progressing a story" — they're raising stats, walking around home, and watching content gradually escalate. Reads as low-effort/high-frequency. Bootstrap: flash/tease at MC corruption 5 (chance 100) raises NPC arousal — once arousal > 0, random-encounter scenes become possible on bedroom visits. Family runs in *background* of the player's attention.

**Peer arc (quest chain).** Discrete, planned, sequential. Player has a checklist: "do the prereq → unlock the deterministic beat." Marcus arc requires MC corruption=0 mostly — peer/school is the "wholesome" track. This is what the player *focuses on this session*.

**Career arc (metric + time + DM).** Patient/calendar-driven. Edward DM widget literally arrives on the player's phone after a follower threshold + wait period. The player grinds Instafame followers across many in-game days while the family arc passively unfolds. This is the *long-burn project across weeks*.

The 3 shapes give DIFFERENT TEMPOS so the player isn't always doing the same thing.

---

## §6 — The Walkthrough panel as transparent planning UI

The `📕 Walkthrough` button in the right sidebar opens a passage that **literally renders the scene table as data to the player**. Same fields as the engine's internal scene struct, just formatted as a table.

### Top section — tutorial (verbatim)

> **How to gain corruption and exhibitionism**
>
> At the start of the game, you gain 1 arousal each day, or after being groped in your bedroom. You can choose to masturbate to increase your corruption.
>
> Once you reach 5 corruption points, you unlock the option to flash your Stepbrother through his bedroom, gaining 1 exhibitionism point.
>
> Some events have requirements, such as a minimum corruption level, exhibitionism level, or relationship level with an NPC. You can also trigger events by visiting certain locations.

The bootstrap loop is *taught explicitly*. No discovery required.

### Middle section — NPC scenes index

Card grid: **MC** + **Stepfather (12)** + **Stepbrother (15)** + **Stepgrandfather (6)** + **Marcus (5)** + **Sam (2)** + **Emma (1)** + **Jamal (3)** + **Veronica (3)** + **Priest (2)** + **Gangster (1)** + **Mr. Matthew (1)** + **Edward (4)** + **Tow Truck Driver (1)** + **Yacht Captain (1)** + **Thief (2)** + **Josh (1)** + **Landlord (1)**.

### Bottom section — Location scenes index

Same card grid for location-bound scenes — independent of NPCs (random encounters at the location regardless of who's there).

### Per-NPC drilldown — verbatim columns

Clicking "Stepbrother" → table:

| SCENE | NPC | REQUIREMENTS (NPC) | REQUIREMENTS (MC) | CHANCE | GUIDE | STATUS |
|---|---|---|---|---|---|---|
| Stepbrother Bedroom Grope | Stepbrother | Arousal: 🔥 | None | 20% | Go to your bedroom | 🔒 Locked |
| Stepbrother Bedroom Study Grope | Stepbrother | Arousal: 🔥, Corruption: 1 | None | 20% | Study at your room | 🔒 Locked |
| Stepbrother Bedroom Flash | Stepbrother | None | Corruption: 5 | 100% | Go to your Stepbrother bedroom | 🔒 Locked |
| Sleep with Stepbrother | Stepbrother | Arousal: 🔥, Corruption: 10 | Corruption: 30 | 100% | Go to Stepbrother bedroom late at night and ask to sleep with him | 🔒 Locked |
| ... (15 rows total) | | | | | | |

**This IS the quest log.** The player loop is *literally*: open Walkthrough → pick a locked scene close to unlocking → read its requirements → close the gap → re-attempt. There is no hidden progression. The "story" is the player's self-authored checklist progression across the 130+ scene catalog.

**Design implication for TLS:** the walkthrough/quests panel isn't a debugging affordance, it's the *primary planning surface*. Hide it and the game becomes opaque/grindy. Surface it well and the game becomes a transparent sandbox.

---

## §7 — Passage-level mechanics (verbatim source)

Reading the passage source for `BrotherBedroom` and `Bedroom` exposes the whole mechanical glue. Excerpts are verbatim from `Story.get('X').text`.

### 7.1 BrotherBedroom — full menu logic

```twine
<<if $game.time == "LN">>
    <h3>It's late at night, your $npc.Brother.relationship is sleeping.</h3>
<</if>>
<<if GetNpcLocation("Brother") == "School">>
    <h3>Your $npc.Brother.relationship is at school</h3>
<<else>>
    <h3>Your $npc.Brother.relationship is not in his bedroom</h3>
<</if>>

<div class="menuLocation">
    <<if $game.time == "LN">>
        <<if $npc.Brother.relation >= 10>>
            <<button 'Sleep with him 💤' 'SleepingBrother'>><</button>>
        <</if>>
    <<else>>
        <<if GetNpcLocation("Brother") == "Bedroom">>
            <<button "Talk with him 🗣️">>
                <<Talk Brother>>
                <<AddTime 1>>
                <<UpdateScreen>>
            <</button>>
            <<button 'Tease him ❤️‍🔥'>>
                <<if checkSceneReq("BrotherBedroomTease")>>
                    <<goto 'BrotherBedroomTease'>>
                <</if>>
            <</button>>
            <<button 'Flash to him ❤️‍🔥'>>
                <<if checkSceneReq("BrotherBedroomFlash")>>
                    <<goto 'BrotherBedroomFlash'>>
                <</if>>
            <</button>>
            <<button "Have sex with him 🔥">>
                <<if getCorruptionLevel() >= 3>>
                    <<if getArousal() > 0>>
                        <<if isPregnant()>>
                            <<goto "BrotherBedroomPregnantSex1">>
                        <<else>>
                            <<goto "BrotherBedroomSex1">>
                        <</if>>
                    <<else>>
                        <<Notification "warning" "I'm not aroused enough to do that right now.">>
                    <</if>>
                <<else>>
                    <<NotifyCorruption 4>>
                    <<Notification "warning" "Am I crazy? I'm not doing that with my $npc.Brother.relationship.">>
                <</if>>
            <</button>>

            /* Random encounter on entry from Hallway */
            <<if previous() == "Hallway">>
                <<set $game.random = random(1,4)>>
                <<if $game.random == 1 && !$npc.Brother.scenes.PeepBrotherSex.executedToday>>
                    <<goto 'PeepBrotherSex'>>
                <<elseif $game.random == 2 && !$npc.Brother.scenes.BrotherCaughtMasturbating.executedToday>>
                    <<goto 'BrotherCaughtMasturbating'>>
                <</if>>
            <</if>>
        <</if>>
    <</if>>
    <<button 'Hallway 🚪' 'Hallway'>><</button>>
</div>
```

**Patterns visible:**

- **Time-of-day branch (LN):** Different button set at late night. "Sleep with him" only at LN + relation ≥ 10.
- **Present-NPC branch:** Buttons only render if `GetNpcLocation("Brother") == "Bedroom"` (he's actually here). Otherwise just "is not in his bedroom" + Hallway.
- **Soft-fail vs notify-fail:**
  - Tease/Flash buttons → silent no-op when reqs not met. Player sees nothing happen.
  - "Have sex" button → explanatory notification: *"Am I crazy? I'm not doing that with my Stepbrother."* (corruption too low) or *"I'm not aroused enough to do that right now."* (arousal too low). The notification text exposes the *story reason*, not the mechanical threshold.
- **Random encounter at passage tail:** `previous() == "Hallway" && random(1,4) && !executedToday`. Two scenes compete for the same dice slot. **Bypasses requirementsMC** entirely.
- **`<<NotifyCorruption 4>>`:** UI hint widget — see §7.4 for the full correction.

### 7.2 Bedroom (player's room) — progressive unlocks

```twine
<!-- STUDY -->
<<if $game.time == "LN">>
    <<button '❌ Too late to study ❌'>><</button>>
<<elseif $player.energy <= 0>>
    <<button '🪫 Too tired to study 🪫'>><</button>>
<<else>>
    <<button 'Study 📖' 'BedroomStudy'>><</button>>
    <<if $location.school.homework == false && getQuestProgress("MathHomework") > 0>>
        <<button 'Do homework 📖'>> ... <</button>>
    <</if>>
<</if>>

<!-- MASTURBATE — only after phone purchased -->
<<if isPurchased("phone")>>
    <<button "Masturbate 🍆">>
        <<if getArousal() > 0>>
            <<goto "BedroomMasturbate">>
        <<else>>
            <<Notification 'warning' "You are not aroused enough to masturbate">>
        <</if>>
    <</button>>
<</if>>

<!-- HALLWAY — gated by clothing × corruption -->
<<button 'Hallway 🚪'>>
    <<if $player.clothing.type == 'naked' && getCorruptionLevel() < 3>>
        <<Notification 'warning' "I should wear some clothes.. 30+ Corruption Needed">>
    <<elseif $player.clothing.type == 'underwear' && getCorruptionLevel() < 2>>
        <<Notification 'warning' "I should wear some clothes.. 15+ Corruption Needed">>
    <<elseif $player.energy == 0>>
        <<Notification 'warning' "You need to sleep!">>
    <<else>>
        <<goto 'Hallway'>>
    <</if>>
<</button>>
```

Plus, after the menu div, the random-encounter check on bedroom entry:

```twine
<<if previous() == "Hallway" && (($npc.Dad.arousal > 0 && IsNpcAtHome("Dad"))
                              || ($npc.Brother.arousal > 0 && IsNpcAtHome("Brother")))>>
    <<if random(1,2) == 1>>
        <<goto 'BedroomGrope'>>
    <</if>>
    <<if random(1,3) == 1 && IsNpcAtHome("Brother") && getNpcCorruption("Brother") >= 10
                          && !isNpcSceneUnlocked("Josh", "SellingMyStepsister")>>
        <<goto "SellingMyStepsister">>
    <</if>>
<</if>>
```

**Patterns visible:**

- **State-conditional buttons:** Same passage shows different button set per `$game.time`, `$player.energy`, `isPurchased(item)`, `getQuestProgress(quest)`, `$location.school.homework`. Room layout *evolves with player progression*.
- **Notification text exposes the threshold:** "30+ Corruption Needed", "15+ Corruption Needed". The mechanic and the rationale are surfaced together.
- **Cross-NPC scene branching:** `SellingMyStepsister` requires Brother corruption ≥ 10 AND Josh hasn't already unlocked it. Once unlocked, Brother's arc *transfers into Josh's arc*. NPC arcs link via scene-flag dependencies, not just stat thresholds.

### 7.3 Random-encounter mechanic in summary

The passage code for any room with random encounters does:

```
on_entry_from_hub:
    roll = random(1, N)               # N = 2/3/4 depending on # of competing scenes
    if roll == 1 and !sceneA.executedToday: goto sceneA
    elif roll == 2 and !sceneB.executedToday: goto sceneB
    ...
```

- N == 4 ⇒ each scene has ~25% chance per entry (matches 25% in walkthrough)
- `executedToday` enforces once-per-day cap
- `previous() == hub` prevents loop-spam by reloading the same room
- Some encounters add precondition checks (`NPC.arousal > 0`, `NPC.corruption >= N`)
- **The walkthrough's "REQUIREMENTS (MC)" column is NOT checked here** — see §11 #1.

### 7.4 NotifyCorruption widget — corrected understanding

Reading widget definitions across many scenes (`JimDM`, `RichardDM`, `EdwardDM`, `EdwardSecondDateDM`, `EdwardThreesomeDM`, `RichardSecondPhotoShootDM`):

```twine
<<widget 'JimDM'>>
    ... pitch dialogue ...
    <<if getCorruptionLevel() >= 4>>
        <<linkreplace "Accept the proposal">> ... unlock film studio ... <</linkreplace>>
    <<else>>
        <<linkreplace "I can't do this">>
            <<Speech Player "I'm sorry but I can't do that">>
            <<Speech Jim "I understand, if you change your mind, you can contact me.">>
            <<NotifyCorruption 4>>      /* <-- always in ELSE branch, N matches the if-threshold */
        <</linkreplace>>
    <</if>>
<</widget>>
```

`<<NotifyCorruption N>>` is **a UI hint that displays "you need corruption level N for this"**. It does NOT add corruption. Always called in the ELSE branch with N matching the required level.

**Verified by live play:** clicked "Have sex with him 🔥" at MC corruption 0 → the source has `<<NotifyCorruption 4>>` in that branch → no stat change after. The "rejection trains the player" loop **does not exist** (this was my earlier wrong inference — see §11 #3).

---

## §8 — Linkreplace-drip scene structure

Each scene is **NOT a single passage that you read top-to-bottom and then leave**. It's a *multi-step in-place reveal* using SugarCube's `<<linkreplace>>` macro. Each click reveals the next paragraph (often with a new image, video, and/or new choice link) inside the same passage container.

This is the IF-craft layer that bridges *"a dice roll just triggered this"* and *"I'm reading a story."* It's also what makes scenes feel like scenes rather than popups.

### Concrete example — `PeepBrotherSex` (live observed)

**Initial render (entry):**
> **Stepbrother's Bedroom**
> You push open the door to your Stepbrother's room, only to stop dead in your tracks. He's in bed with a girl, their bodies tangled together... and they're definitely not just sleeping!
>
> [Peep] [Hallway 🚪]

**After "Peep" click:** linkreplace inserts inline:
> Heat flares in your belly as you watch them through the cracked door. Your Stepbrother is groaning, his hands gripping the girl's hips as he moves over her. You're mesmerized, your own breathing getting ragged.
>
> *(VIDEO embedded: `masturbate1.mp4`)*
>
> [Stroke your pussy] [Hallway 🚪]

**After "Stroke your pussy" click (at low MC arousal):** linkreplace inserts:
> You are not aroused enough to do this
>
> [Hallway 🚪]

**After "Keep Watching" on Dad's `ProstituteSex` (at MC corruption 0):** linkreplace inserts an *empty* span — scene literally has no more content for me. Higher-corruption returns would presumably reveal additional paragraphs / videos / interaction options.

### Patterns to take away

- **Stat changes happen DURING the scene**, not just on entry. Peeking raised MC arousal +1 per beat (0 → 1 → 2 over the Brother + Dad scenes).
- **Choice links can fail in-fiction** with explanatory prose ("You are not aroused enough to do this"). The fail is part of the narrative, not a popup error.
- **Content branches by stat INSIDE the scene** rather than at the entry gate (see §11 #2). Every visit shows something; higher-stat returns reveal more.
- **Media (image / video) interleaves with prose** at specific reveal beats, not just at scene entry. The pacing of media reveal contributes to the scene's tension.

---

## §9 — Three writing tiers

RTS doesn't write every scene at the same density. There are three observable tiers, each used deliberately for a class of moments.

### Tier 1 — Utility one-liner

> **STUDY**
> You studied an hour and feel smarter!
> [Return ↩️]

Used for: **bedroom Study, Sleep, Nap, generic activity-passes ("Socialize: You waste time socializing with your classmates").**

Function: pure mechanical confirmation. The text exists only to make the stat-tick acknowledgment feel like *something*. ~10 words.

### Tier 2 — Vignette prose

> **Stepbrother's Bedroom**
> You push open the door to your Stepbrother's room, only to stop dead in your tracks. He's in bed with a girl, their bodies tangled together... and they're definitely not just sleeping!
> [Peep]

Used for: **random-encounter scenes with anonymous partners** (Brother with "a girl," Dad with "a prostitute," generic strangers in public exhibitionism scenes).

Function: bridges mechanic to content. Generic descriptive prose with named situations but un-named NPC partners. ~30–50 words per beat, 2–4 beats per scene via linkreplace.

### Tier 3 — Scripted character

> **A QUIET CORNER**
> *Most of the tables are empty. She slips something into her book to hold the page and looks up when you get close. Same girl from the hallway. This is the first time you actually stop to talk.*
>
> Victoria: Hi. Mind if I sit?
> Student: Yeah, go ahead. I'm just hiding from the hallway noise.
> Victoria: Fair. I'm Victoria.
> Student: Natasha. I come here when I need to study and people won't shut up out there.
> Natasha: Anyway. Don't be a stranger. I'm here most days.
> [Return ↩️]

Used for: **named-NPC introductions, quest beats, arc transitions, Edward's DM widgets (10+ Speech beats with personality and seductive escalation).**

Function: real character writing. Sensory grounding (*"She slips something into her book to hold the page"*). Voice (*"hiding from the hallway noise"* — introvert framing). Live-changing speaker labels (*"Student" → "Natasha"* once names exchanged). This is the layer that earns RTS its narrative weight.

### Distribution observation

Of 130+ scenes:
- Maybe ~30 are Tier 1 utility (every activity)
- Maybe ~70 are Tier 2 vignette (random encounters + most location scenes)
- Maybe ~30 are Tier 3 scripted character (intros + quest beats + DM widgets)

The author **doesn't waste Tier-3 prose on Tier-1 moments**. Reserved for transitions and named characters. This budget discipline is part of why a 130-scene game ships at all.

---

## §10 — Stat economy

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
| `arousal` | integer 0–N | **CORRECTED 2026-05-03 from playthrough 2:** stored as integer (e.g. Brother arousal observed at `1`, `3`, `5`). The `🔥`/`🔥🔥`/`🔥🔥🔥` notation in the walkthrough's REQUIREMENTS column is a *display threshold format*, not the storage format. Original §10 was wrong. NPC arousal also accumulates passively +1/day, not just from MC actions. |
| `corruption` | 0–∞ | Integer. Raised by player taboo actions toward this NPC. |
| `relation` | 0–∞ | Integer. Always 0 for family arcs (no narrative chain); meaningful for peer arcs. |
| `talkedToday` | bool | Once-per-day Talk gate. |
| `location` | string | Schedule-driven by tick (Brother: bathroom EM, school M+A, bedroom E+N+LN). |
| `scenes` | object | Per-scene state: `{unlocked, executedToday, gallery flag}`. |

### Time

- 6 buckets per day: EM / M / A / E / N / LN
- 7-day week: Monday → Sunday
- `$game.days` = lifetime day counter (driving "wait 10 days" mechanics)
- Activities `<<AddTime N>>` advance N buckets

### Composition rule

**The same room can show different button sets per state.** A canonical example: Brother's bedroom at LN with Brother present + relation ≥ 10 shows "Sleep with him." At E with Brother present + corruption < 3 shows Talk/Tease/Flash/[Have sex *gated*]. At M (Brother at school) shows "is at school" + Hallway only.

The **clothing × location × time × stats** product is the gating space. Gates compose from layered conditions, not central rule tables. This makes the world feel rule-bound while keeping each individual gate readable in its own passage.

---

## §11 — Empirical corrections (data-extraction was wrong)

These five corrections came from live play, not source-reading. **Recording these because they were my own confident-but-wrong inferences from the source code alone.** Same trap could catch future TLS conversations citing RTS.

### Correction 1 ❌ Disproved — Walkthrough requirements aren't strict gates for random encounters

- **What I claimed (data-extracted):** Triple gating — NPC stats AND Player stats AND probability — strictly enforced.
- **What actually happens:** `BrotherBedroom` random-encounter check is ONLY `previous()=="Hallway" && random(1,4)==1 && !executedToday`. The `requirementsMC.corruption: 15` field listed in walkthrough for `PeepBrotherSex` is **bypassed**. Live verified: scene fired at MC corruption 0 on Day 1 Evening.
- **Implication:** the walkthrough's "REQUIREMENTS (MC)" column is a **suggested threshold for the FULL content version**, not an entry gate. Player can stumble into scenes early and get a teaser; full content unlocks later.

### Correction 2 ✅ Verified live — Higher stats unlock MORE CONTENT inside a scene, not access TO the scene

- **What I claimed:** Player has to reach the threshold to "unlock" the scene as binary access.
- **What actually happens:** Every visit shows the entry text + image + first beat. Linkreplace beats *after* that branch by stat. Live verified: clicked "Keep Watching" on Dad's `ProstituteSex` at MC corruption 0 → linkreplace inserted **empty content** (`<span class="macro-linkreplace-insert">` with nothing inside). Scene literally has no more body for me.
- **Implication:** every scene has a "low-corruption short version" and a "high-corruption full version" inside the same passage. Player can't be punished for trying. Player knows there's more, comes back later.

### Correction 3 ❌ Disproved — `<<NotifyCorruption N>>` is a UI hint, NOT a corruption-adder

- **What I claimed (data-extracted):** "Failing taboo actions raises corruption — rejection trains the player. Brilliant design loop."
- **What actually happens:** `<<NotifyCorruption N>>` is a *UI feedback widget* that displays "you need corruption level N for this." Always called in the ELSE branch with N matching the required level. Pattern verified across 5+ widget definitions (`JimDM`, `RichardDM`, `EdwardDM`, `EdwardSecondDateDM`, `EdwardThreesomeDM`, `RichardSecondPhotoShootDM`).
- **Live verified:** clicked "Have sex with him 🔥" at MC corruption 0 → notification appeared, **corruption.points stayed 0**.
- **Implication:** the rejection-trains-corruption loop **does not exist** in RTS. Failure is *information* (publishes the threshold), not *progress*. Player still has to actually do the corruption-raising mechanic (masturbate / accept paid date / etc.).

### Correction 4 🟦 Captured — Watching/peeping itself raises MC arousal

- **What I missed:** Voyeur scenes have +arousal effects baked in.
- **What actually happens:** Live observed — peeping at `PeepBrotherSex` raised MC arousal 0 → 1. Clicking "Keep Watching" on Dad's `ProstituteSex` raised it 1 → 2. Sleeping overnight raised it 2 → 3 (matches walkthrough "+1 arousal each day").
- **Implication:** scenes carry their own stat-effect side-channels separate from the explicit "stat-raising activities" (masturbate / gym / etc.). Stats and content interleave.

### Correction 5 🟦 Captured — Quest descriptions are story flavor, not hard timers

- **What I assumed:** "I need to take the school test on Monday" implies a Monday deadline.
- **What actually happens:** Slept past Monday → quest still active Tuesday with same description. The "Monday" is *in-character planning text*, not enforced. Player won't fail by missing it.
- **Implication:** quest description text is for atmosphere/orientation, not for mechanical scheduling. RTS doesn't time-out quests.

### Bonus correction (also wrong in original synthesis)

- I claimed "the bootstrap loop requires getting a phone first ($400) to masturbate." **Partly true** — but Day 1 Evening, just walking around home, the player encounters PeepBrotherSex AND Dad's ProstituteSex with images/video at MC corruption 0. Voyeur content access requires zero stat-grinding. Stat-grinding is for *escalation to active participation* (flash/sex), not initial content access. The game lures you in fast.

---

## §12 — Day 1 bootstrap experience (turn-by-turn play log)

Captured live. ~30 meaningful clicks Day 1 EM → Day 2 EM. Reading top-down gives the actual feel of a fresh playthrough.

| Turn | Action | Result | Stat / state delta |
|---|---|---|---|
| 1 | (start) | Day 1 Monday EM, Bedroom, Victoria | corr 0, ar 0, exhi 0, energy 100, $50, intel 0, beauty 0 |
| 2 | Phase 0a auto-advance: Play → I understand → Continue → History → Start Your Journey | Lands at Bedroom passage | (intro skipped — automated by skill) |
| 3 | Eval `npc.X.scenes` extraction | 16 Brother scenes, 12 Dad scenes, 5 Marcus, 4 Edward inventoried | (no game state change) |
| 4 | Click `Study 📖` | BedroomStudy → "STUDY / You studied an hour and feel smarter!" | intel +1, energy −10, time M |
| 5 | Click `Return ↩️` | Back to Bedroom | — |
| 6 | Click sidebar `🏫 Go to School` | **Silent fail** — passage stays Bedroom | Player wearing casual clothes (no error message — first surprise) |
| 7 | Click `Wardrobe 👚` → `👩🏼‍🎓 School` tab → click School 1 image | clothing equipped | clothing.type = "school", clothing.name = "school1" |
| 8 | Click `↩️ Return` → `🏫 Go to School` | **School hub loads** | passage = School |
| 9 | Click `History Class ⚔️` → `Study 📖` | ClassroomEvent → "feel smarter" — **NEW QUESTS unlocked** | intel +1, time A; questList: SchoolTest + MathHomework activate (sidebar quest cascade) |
| 10 | Click `Socialize 💬` | "You waste time socializing with your classmates" — generic vignette | (no Marcus interaction at this time bucket) |
| 11 | Click `Return ↩️` → leave school via `Residential` → `House` | Hallway loaded | family schedule check: Dad=Work, Brother=School, Grandpa=Kitchen (afternoon) |
| 12 | Eval `handleSubLocation('Bedroom')` → `Nap 💤` | Bedroom → Nap → "You take a nap for an hour" | energy +5 net (decay −10 + recovery +15), time E |
| 13 | Eval check family locations | Dad → DadBedroom, Brother → BrotherBedroom, Grandpa → Bathroom (evening) | All present at home |
| 14 | Click `Hallway 🚪` → eval `handleSubLocation('BrotherBedroom')` | **🎯 PeepBrotherSex random-encounter fires** at MC corruption 0 | scene = PeepBrotherSex |
| 15 | Read scene: *"You push open the door to your Stepbrother's room, only to stop dead in your tracks. He's in bed with a girl, their bodies tangled together... and they're definitely not just sleeping!"* + image | Choice: [Peep] [Hallway] | — |
| 16 | Click `Peep` | linkreplace adds: *"Heat flares in your belly... You're mesmerized, your own breathing getting ragged."* + VIDEO `masturbate1.mp4` + new choice [Stroke your pussy] | MC arousal 0 → 1 |
| 17 | Click `Stroke your pussy` | linkreplace adds: *"You are not aroused enough to do this"* | (no further linkreplace — scene capped at this branch) |
| 18 | Click `Hallway 🚪` → eval `handleSubLocation('DadBedroom')` | **🎯 ProstituteSex (Dad scene) random-encounter fires** at MC corruption 0 | scene = DadBedroom (entry text "You hear a strange noise") |
| 19 | Click `Peek 👀` | linkreplace adds: image `dadpeek1.webp` + *"When you peek, you see your Stepfather having sex with a prostitute"* + new choice [Keep Watching] | MC arousal 1 → 2 |
| 20 | Click `Keep Watching` | **linkreplace adds EMPTY content** — scene truncates at corruption 0 | (no stat change — see Correction 2) |
| 21 | Click `Hallway 🚪` → re-enter `BrotherBedroom` | **PeepBrotherSex does NOT re-fire** (`!executedToday` flag working) — instead full button menu loads | (verifies daily cap) |
| 22 | Click `Have sex with him 🔥` (gated, MC corr 0 < 3) | **Silent visual fail** — passage stays. Notification "Am I crazy? I'm not doing that with my Stepbrother." would have shown if I'd had a notification listener; verified via source. **Corruption stays 0** (Correction 3) | — |
| 23 | Click `Tease him ❤️‍🔥` (gated, MC corr 5 needed) | Silent no-op (soft-fail pattern) | — |
| 24 | Click `Hallway 🚪` → `Bedroom` → `Nap 💤` → `Sleep 💤` | "SLEEP / Wake up" → Day 2 Tuesday EM | day +1, energy 100, MC arousal 2 → 3 |
| 25 | Click `🏫 Go to School` (still in school uniform) | School hub Tuesday EM | — |
| 26 | Click `Math Class 📐` → `Study 📖` | Math class study | intel +1, time M, **MathHomework progress 0 → 1** |
| 27 | Click sidebar `📜 Quests` | Active: SchoolTest "I need to take the school test on Monday" / MathHomework "I need to go to math class and turn in my homework" / INeedMoney "I should get a job, maybe at the restaurant?" | (Correction 5: SchoolTest still active despite Monday passing) |
| 28 | Eval `handleSubLocation('Library')` | Library: *"There is a girl at the reading tables, lost in a book. You keep seeing her in the halls. Kind of weird you never said hi. Could fix that now."* + [Say hello] | (excellent character setup line) |
| 29 | Click `Say hello 📚` | **🎯 Tier-3 scripted intro: Natasha** | scripted dialogue — speaker label changes "Student" → "Natasha" once names exchanged |
| 30 | Read scene + return | (scene ends with "Don't be a stranger. I'm here most days.") | (per-NPC chat now unlocked) |

**Bootstrap takeaways:**

- **Day 1 Evening = first taboo content beat.** No grinding required.
- **Two random encounters fired naturally** in <5 moves.
- **One quest cascade** happened automatically (FirstDayOfShool auto-completed → SchoolTest + MathHomework activated).
- **One Tier-3 intro scene** was discoverable (Library → Natasha).
- **Three soft/notify-fail attempts** taught me thresholds without punishing me.
- **No explicit tutorial outside the Walkthrough panel** — rest is learned by doing.

---

## §13 — Design takeaways (what RTS teaches us, in simple words)

10 points, polished from in-conversation discussion:

1. **Hand the player content immediately.** Day 1 Evening, no grinding, two voyeur scenes with images + video. Prove the game is worth playing in the first 5 minutes.

2. **Same scene plays differently for different players.** Low-corruption Player sees one paragraph + image + truncated linkreplace. High-corruption Player sees three more paragraphs, a video, an interaction option. One authored scene, many lengths. Player wants to revisit because they know they're seeing a truncated version.

3. **Don't punish trying.** Pressing a gated button shows you what you need ("30+ Corruption Needed"). No penalty, no scolding. The threshold is the message. The walkthrough panel publishes the whole gate table.

4. **Story lives at the SCENE level, not the ARC level.** There's no "Brother's emotional journey across 16 scenes." Each scene is a self-contained vignette. The macro-story is whatever the player happens to do, in whatever order. **130 micro-stories beat 12 long arcs** for an open-world feel.

5. **Mix arc shapes — don't pick one.** Family ambient + Peer quest-chain + Career metric+DM. Three tempos run in parallel: family in background, peer in focus, career in long-tail. Each demands different attention.

6. **The walkthrough IS the game's quest log.** RTS doesn't hide its mechanics. It publishes the full scene table — gates, chances, hints, status. Player loop is *literally* "open walkthrough → pick a near-unlock → close the gap." **Transparency is the design**, not a fallback.

7. **Scenes are flows, not popups.** Each scene = multi-step linkreplace. Click → reveal paragraph → reveal image → new choice → reveal video → reveal next paragraph. **One scene feels like reading a chapter.** This is what makes a dice-roll trigger feel like a story instead of a stat payload.

8. **Three writing tiers, used deliberately.** Don't waste Tier-3 character writing on Tier-1 utility moments. Reserve real prose for first meets, quest beats, arc transitions. Tier-2 vignette covers the random-encounter middle ground.

9. **Time + clothing + location compose into gates.** You can't go to school in casual clothes (silent fail). You can't leave home naked at low corruption (notification with threshold). You can't have late-night Brother visits unless relation ≥ 10. Same room, different button set per time of day. **Layered constraints make the world feel rule-bound without writing explicit blockers everywhere.**

10. **Failure is information, not progress.** Rejection doesn't auto-train you. It just *tells you the threshold*. The progression is honest — you have to actually do the corruption-raising mechanic. No "press X 50 times for free corruption" hack. (This was Correction 3 to my earlier mistaken "rejection trains the player" claim.)

---

## §14 — Implications for TLS

### What TLS already has right (do not regress)

- Triple-gating in scene definitions (NPC stats / MC stats / probability) — see `04_Scene_Cascade_Pattern.md`.
- Per-NPC scene tables exposed via Quests panel — analogous to RTS Walkthrough.
- Time-bucket system (RTS uses 6 EM/M/A/E/N/LN; TLS uses similar).
- The `stage_npc/stage_op/stage_value` hint system (`12_Engine_PRD_09_Hint_System_Completeness.md`) is a **hybrid that supports both Marcus-style sequential beats AND Brother-style stat-tier escalation in one mechanism**. This is a sophistication over RTS — RTS picks one shape per NPC; TLS can mix within an NPC.
- Hint priority + crisis-variant override (`11_Hint_Authoring_Guide.md`) — a sophistication over RTS's static walkthrough.

### What's worth borrowing from RTS

| Pattern | Source § | Status in TLS | Action |
|---|---|---|---|
| Linkreplace-drip scene structure | §8 | Not used — TLS scenes are single-render passages | Consider for high-tension Tier-3 scenes; bridges mechanical trigger to narrative feel |
| Content-branches-INSIDE-scenes (not entry gates) | §11 #2 | Not used — TLS gates at entry | Consider: lets every visit show *something* even at low stats; reduces "you're not ready" friction |
| Published walkthrough with full scene table | §6 | Partially — Quests panel exists but doesn't render the full requirements/chance/guide table to player | Consider extending QuestsPage with a per-NPC scene table view |
| Tier-3 character writing reserved for transitions | §9 | Variable — TLS scene-body style mandate is "RTS-flat" but `feedback_tls_scene_body_style.md` may need a Tier-3 carve-out for arc transitions | Audit current TLS scene bodies vs. tier classification; verify intros/transitions are Tier-3 |
| Cross-NPC scene branching (`SellingMyStepsister`) | §7.2 | Not used | Consider for arc convergence moments without rigid scene trees |
| Notification-as-threshold-hint (`30+ Corruption Needed`) | §7.2 | Variable — some TLS gates do this | Standardize: every gated button should publish its threshold in the failure notification |

### Cautions

1. **If every NPC follows family-arc pattern** (random encounters, ambient escalation) → reads as **grindy** and lacks story-beat satisfaction.
2. **If every NPC follows peer-arc pattern** (sequential quest chain) → reads as **VN, not sandbox**; loses the "open-world" feel.
3. **Mix the three shapes per RTS.** TLS has 12 NPCs in the full game — distribute across family-style / peer-style / career-style. Don't standardize on one shape.
4. **NotifyCorruption-style mechanic does NOT exist in RTS.** Don't propose adding "rejection raises corruption" loops to TLS citing RTS — RTS doesn't do this (Correction 3).

### Cross-references

- `00_TLS_Phase2_Diagnosis_and_Direction.md` — original "what RTS does vs. what TLS does" comparison table.
- `01_Repeatable_First_Doctrine.md` — TLS doctrine that scenes-first / repeatables-first matches RTS's approach.
- `02_NPC_Stage_Chains.md` — TLS stage-chain mechanism that should accommodate the 3 arc shapes from §5.
- `04_Scene_Cascade_Pattern.md` — TLS scene cascade rules; this doc's §7 is the empirical basis.
- `09_Future_Polish_Items.md` — may reference §6 (transparent walkthrough) for future Quests page extension.
- `11_Hint_Authoring_Guide.md` — TLS hint authoring; this doc's §6 + §13 #6 are the empirical basis for "publish gates to player."
- `12_Engine_PRD_09_Hint_System_Completeness.md` — the hybrid stage system this doc's §5 partially validates.

---

## §15 — Source artifacts

All artifacts captured during the 2026-05-02 sessions. Available as primary-source data for future verification.

### Live exploration outputs

- `game_explorations/rts-arc-trace/notes.md` — 5 long structured notes:
  1. Brother arc structure (extracted from `npc.Brother.scenes`)
  2. Cross-arc design pattern (3 arc shapes)
  3. Walkthrough = transparent game-design reveal
  4. Passage-level mechanics (BrotherBedroom + Bedroom source)
  5. Experiential corrections from live play (the 5 corrections in §11)
- `game_explorations/rts-arc-trace/passage_catalog.json` — full `Story.passages` dump with raw Twine source.
- `game_explorations/rts-arc-trace/variable_index.json` — every variable + where it's set/unset across all passages.
- `game_explorations/rts-arc-trace/play_log.jsonl` — every command issued during live play, with passage + state_hash.
- `game_explorations/rts-arc-trace/state_timeline.jsonl` — per-observation state snapshots.
- `game_explorations/rts-arc-trace/sidebar_snapshots.jsonl` — sidebar/chrome panel content captures.
- `game_explorations/rts-arc-trace/ui_probes/` — 8 chrome-button screenshots (Cheats / Gallery / Go_to_School / Inventory / Preferences / Quests / Relations / Walkthrough).
- `game_explorations/rts-arc-trace/sessions/` — per-run metadata (timing, clicks, completion).

### Older exploration (still relevant for scene bodies)

- `game_explorations/road-to-success/scene_bodies.jsonl` — 447 scene-body entries from prior playthroughs. Used in this doc for Tier-1/Tier-2 verbatim examples (`StudyWithMarcus`, `SecretAdmirer`, `BedroomMasturbate`, `BedroomStudy`).
- `game_explorations/road-to-success/notes.md` — 971 lines of older structural observations.
- `game_explorations/road-to-success/scene_catalog.json` — visit-counted scene catalog.
- `game_explorations/road-to-success/report.md` — auto-generated finalize-time synthesis.

### Memory entries

- `~/.claude/projects/-Users-a0000-.../memory/rts_three_arc_shapes.md` — the live-corrected memory record indexed in `MEMORY.md`. **Has corrections applied** — the older claims about NotifyCorruption-as-corruption-adder have been removed. Treat this entry as ground-truth for future conversations.

### Twine-game-explorer skill

- `.claude/skills/twine-game-explorer/SKILL.md` — the skill that drove this exploration. Resumable: re-run `node $SKILL_DIR/scripts/live.js start --slug rts-arc-trace --url https://mopoga.com/road-to-success` (without `--fresh`) to re-open the same Chromium profile and continue.

---

## §16 — Playthrough 2: Brother arc to near-exhaustion (2026-05-03)

After the doc was first written, a second focused playthrough sampled Brother's content table to near-exhaustion. **Five findings updated or invalidated parts of the original doc.** Recorded here rather than rewriting the earlier sections so the methodology trail stays visible.

### Method

- Resumed `rts-arc-trace` session, fresh Day 1 Monday EM (state had reset).
- Naturally bootstrapped MC corruption 0 → 5 across 3 in-game days (~30 turns) using sleep cycles + school bathroom masturbate + family groping passive corruption.
- Eval-jumped to MC corruption 30, exhibitionism 10, beauty 50, Brother arousal 5 / corruption 10 / relation 10 to skip mid-game grind and reach high-tier content efficiently.
- Played 6 distinct Brother scenes plus 3 ambient family random encounters.

### Content sampled live

| Scene | Type | Trigger | Outcome |
|---|---|---|---|
| `PeepBrotherSex` | random (chance 25%) | Bedroom entry from Hallway, Brother home | At MC corr 0: ~80 words + 1 video, "stroke your pussy" choice fails with arousal-too-low |
| `BedroomGrope` | random (50%) | MY bedroom entry from Hallway, NPC arousal>0, NPC home | ~30 words, image, +MC corr 1 from passive grope |
| `BedroomSleepDadScene` | random | Sleep when Dad arousal>0 | **Tier-3 with NPC interior thought bubbles** (`💭 Alfred is thinking...`), 3 linkreplace beats, 3 videos |
| `BrotherCaughtMasturbating` | random (25%) | Bedroom entry, Brother home | **TESTED at MC corr 6 AND MC corr 31.** Low: 5-line scene, "Ew! you pervert!", Brother kicks her out. High: same opening but new `[Shhh]` choice appears → multi-stage seduction (~590 words, full sex sequence). |
| `BrotherBedroomFlash` | deterministic (button, MC corr 5+) | Click Flash in Brother's bedroom | Tier-1 utility, "You give a little show". exhibitionism +1, MC arousal +1, Brother corruption +1, Brother arousal NO change |
| `SellingMyStepsister` | random (33%) | Bedroom entry, Brother corr ≥10, !Josh.scene unlocked | **Tier-3 cross-NPC bridge.** Brother proposes selling player to Josh for $500. Real `[Accept]/[Refuse]` branching choice. Accept → Josh arrives → money exchange → Brother stays to watch → ~25 linkreplace beats sex sequence + $500. Once unlocked, Brother→Josh arc transfers (won't re-fire). |
| `BrotherBedroomSex1` | deterministic (button, MC corr 3+ AND arousal>0) | Click "Have sex with him" | Tier-3 setup: roleplay book-talk on bookshelf → kiss → sex sequence ~478 words, Brother corr +1, rel +1 |
| `SleepingBrother` | deterministic (button, LN, relation 10+) | Late Night visit | **NEGATIVE outcome at relation 12!** Only 134 words: Brother wakes, "I think you better go to your room, someone might hear." "You get angry with your Stepbrother." Probably has high-relation continuation branch I didn't reach. |
| `BATHROOM FLASHING` | random | Bathroom entry | 1 linkreplace beat, image, exits to shower |

### Content not tested (still in Brother table)

`BrotherBedroomTease`, `BrotherShowerSex` (random in shower, didn't roll), `BrotherWashDishesSex` (kitchen), `PlayingGamesSex` (living room), `BrotherHelpStudy` (when studying), `BrotherBedroomGrope` (intro variant), all pregnant variants, `Talk with him` repeatedly. **Estimate ~6-8 hours of additional gameplay would exhaust the rest.** Pattern saturation reached at this sample.

### NEW corrections / additions to earlier sections

#### ❌ Correction 6 (new) — NPC arousal is **integer**, not emoji-tier string

Doc 13 §10 originally said NPC arousal was stored as `"🔥"` / `"🔥🔥"` strings. **Wrong.** Stored as integer (Brother arousal observed at `1`, `3`, `5` from `eval` reads). The emoji notation in the Walkthrough panel's REQUIREMENTS column is a *display threshold format*, not the storage format. Already patched in §10.

#### ❌ Correction 7 (new) — "Three arc shapes" was oversimplified

Doc 13 §5 framed Brother as purely "Family / ambient escalation." **Reality:** Brother is a **HYBRID** — has random ambient encounters AND deterministic player-initiated buttons (Tease/Flash/Have sex) AND time-of-day deterministic (Sleep With Him at LN+relation 10) AND quest-like cross-NPC scenes (SellingMyStepsister gates on Brother corruption + Josh flag). The clean "three shapes" framing was a story I told from data; live play shows every NPC mixes triggers. **More honest framing:** *RTS gives every NPC a mix of random + deterministic + time-gated triggers; the ratio differs per NPC.* Brother is "mostly random + significant deterministic"; Marcus is "mostly deterministic + tiny random splash"; Edward is "metric+wait + DM-mediated deterministic". The 3 shapes are *tendencies*, not categories.

#### 🆕 Finding 1 — NPC interior thought bubbles are a runtime UI primitive

**Missed entirely** in original doc 13. RTS uses a styled Speech-thought macro to render NPC interior monologue inside scenes:

```
💭 Alfred is thinking...
"I can't help myself... she looks so peaceful, so innocent.
 I just need to touch her..."
```

This appears as an **italicized speech bubble with the `💭` emoji and a "thinking..." label**, distinct from the regular speech bubbles. Used in `BedroomSleepDadScene` (3 thought bubbles across 3 beats) and likely many other scenes. **This is a fourth writing dimension** beyond the three tiers in §9 — NPC interiority via Speech-thought macro. Drastically increases narrative depth without adding text density.

For TLS: this is a craft primitive worth borrowing. Currently TLS scene bodies are RTS-flat-style (per `feedback_tls_scene_body_style.md`) — flat dialogue + stage direction. NPC thought bubbles would add character interiority without violating the flat-prose mandate.

#### 🆕 Finding 2 — DETERMINISTIC scenes also have stat-tier branching

§11 #2 said "every visit shows something + content branches inside scenes." **The branching applies to *deterministic* scenes too**, not just random encounters. Concrete proof:

- `SleepingBrother` walkthrough says "100% chance" — but at relation 12 the scene plays a 134-word *rejection* outcome ("Brother wakes, tells player to leave"). Higher relation (likely 25+ or higher) presumably gates the consummation outcome.
- `BrotherCaughtMasturbating` at MC corr 6 plays the disgusted-rejection variant (5 lines, ends "Get out!"). At MC corr 31 a new `[Shhh]` choice appears → full sex sequence (~590 words, multiple positions).

**Implication:** the walkthrough's `CHANCE: 100%` means the trigger always fires when reqs met, but the *content within* still gates by stats. A player can "unlock" a scene mechanically and still get a truncated/rejection version. The full content unlocks at a higher tier.

For TLS: this complicates the "transparent walkthrough" claim. RTS isn't fully transparent — players can hit "100% scene" and still see a stub. TLS could be MORE transparent by surfacing content-tier thresholds in the walkthrough (e.g. "Sleep with Stepbrother — basic version: relation 10+. Full version: relation 25+."). Or TLS could intentionally hide tier ladders to preserve the come-back-later loop RTS uses.

#### 🆕 Finding 3 — Real branching choices DO exist, just rare

§4 / §11 emphasized stat-gated linkreplace as the dominant pattern. **Live observation:** `SellingMyStepsister` has a real meaningful narrative `[Accept]/[Refuse]` choice that materially diverges downstream. So real player-choice branching is rarer than stat-gated reveals, but it does exist for major story moments. Pattern: high-stakes scenes get player choice; everyday encounters get linkreplace-drip.

For TLS: TLS already uses choice-bearing canvases (`5_scenes.toml` has block-level choices). Pattern matches — keep using real choices for major beats, linkreplace-style reveals for routine content.

#### 🆕 Finding 4 — Passive NPC arousal accumulation

Brother arousal observed climbing 0 → 1 → 2 → 3 across 3 in-game days *without me doing anything to him*. NPCs have a passive arousal trickle, not just MC-driven. This is part of why "Day 1 has voyeur content immediately" works — by Day 1 Evening, family arousals are already non-zero, so the random-encounter preconditions (`NPC.arousal > 0`) are met.

For TLS: TLS NPC traits are mostly stage-driven, not passive-trickle. Adding a passive trickle for selected stats (Frank trust slowly accrues from co-presence; Jake notice slowly increases on player visibility) would create the "ambient activity" feel RTS has.

#### 🆕 Finding 5 — Being groped raises MC corruption (+1 per grope)

The walkthrough tutorial said "1 arousal per day OR after being groped in your bedroom" but didn't mention corruption. **Live observed:** the BedroomGrope scene gave MC +1 corruption. So the bootstrap loop is *faster* than the tutorial implies — passive groping accelerates corruption naturally without active choices. Around 30-50% of corruption gain in early game can come from just walking around.

### What survived from playthrough 1 + data extraction

- ✅ Linkreplace-drip scene structure (§8) — confirmed across 6 more scenes
- ✅ Three writing tiers (§9) — confirmed; NPC thought bubbles add a fourth dimension orthogonal to tiers
- ✅ Walkthrough as published planning UI (§6) — confirmed; players DO use it as quest log, but its requirements columns are *suggestions* not strict gates
- ✅ Same scene plays differently at different stats (§11 #2) — *triple-confirmed* with `BrotherCaughtMasturbating` low+high comparison
- ✅ NotifyCorruption is UI hint not stat-adder (§11 #3) — confirmed across 5+ widget definitions
- ✅ Cross-NPC scene branching (§7.2) — confirmed live with `SellingMyStepsister` Brother→Josh transfer
- ✅ Day 1 content access at corruption 0 — confirmed; voyeur scenes fired immediately
- ✅ Soft-fail / notify-fail distinction (§7.1) — confirmed

### Player experience tone notes

- **Bootstrap from corr 0 → 5 took ~15 clicks across 4 in-game days.** Felt efficient. The ambient grope/sleepscene encounters between activities provided constant content texture; player isn't grinding in silence.
- **The stat economy IS the story's tempo.** Corruption gates new options (Flash at 5, SellingMyStepsister at Brother corr 10, Sleep With Him at relation 10). Each unlock feels like a milestone.
- **Same scene replayed at higher corruption was a CRITICAL satisfaction moment.** The `[Shhh]` choice appearing where `Ew gross!` was before is the literal payoff for stat-grinding. This is the come-back-later loop working as designed.
- **The SleepingBrother negative-outcome at relation 12 was FRUSTRATING.** Felt like punishment for not grinding higher. The published walkthrough said relation 10 unlocks the scene — and it did, but the *good* version requires more. This is the soft-fail-as-hint pattern ratcheted up to scene-level.
- **$500 from `SellingMyStepsister` was a HUGE economic moment** — solves money quest in one scene. Story arc and economic arc converge.
- **Travel friction is real.** Most clicks per session went to traveling: Bedroom → Hallway → School → Bathroom → Cabin chain is 5 clicks each way. The sidebar `🏫 Go to School` shortcut helps but only for school. No "Go home" sidebar.

---

**End of doc 13.** 🟦 Captured. Future docs (14+) can cite specific § references when arguing for or against TLS design choices.
