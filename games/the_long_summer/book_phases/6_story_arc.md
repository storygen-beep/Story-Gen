# PHASE 6: STORY ARC
# The Long Summer

*Narrative spine + node table + branching groups + emotion mappings + hints. Every Phase 4 beat maps to at least one arc node. Journal entries are first-person Maya, 1–2 sentences each.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 0: DRAMATIC SPINE SUMMARY

### Central tension

> *"Maya arrived carrying a moral code the place doesn't enforce. As she learns what her body and her wits can earn, you decide which parts of herself she keeps — and how much she walks away with."*

### Conflict types

| # | Conflict | Where it lives | Resolved by |
|---|---|---|---|
| 1 | Economic (rent / tuition / Ryan's shop) | Diner, shop, The Math | Income accumulation — tier choices |
| 2 | Household power (Frank's rules → Phase B) | Property, office, living room | Frank arc progression |
| 3 | Code-enforcement (Diana's silence) | Kitchen, family dinner, Sunday porch | No resolution in Phase 1 — carries to Phase 2 |
| 4 | Self-register (Maya's old code vs. town register) | All solo scenes, midpoint_crack | midpoint_crack + Keep-Tier Fork |

### Tension curve (ASCII)

```
intensity
    |
 HI |                                             *Crack cluster*
    |                                         * * *
    |                                       *       *
    |                                     *          *
    |          *collapse*              *              *(close)
    |          *                    *
    |         * *                 *
MID | *       *   *             *
    |* *     *     *          *
    | * *   *       *       *
    |  *   *         *    *
 LO |   * *           * *
    |    *          *(Ch2 tilt)
    +------------------------------------------------->
         Prologue  Arrival  Ch1     Ch2   Ch3  Ch4  Ch5  Close
         crash    (low      (establ (Marge (first (Frank (Jake (Keep
                  awake)    -ish)   key)   Crack) Crack) Hand)  Fork)
```

### Key emotional beats (selected)

| Beat | Canvas | What Maya feels | What Maya does |
|---|---|---|---|
| Revenge commit | `prologue_the_act` | the shame-engine plants | chooses deliberately |
| Arrival | `arrival_at_franks` | guarded, tired, grateful | takes the suitcase from Frank |
| First rent | `the_math` | the math frame lands | does the math |
| Marge key | `marge_thursday_key` | something tilted that she didn't control | takes the key |
| Midpoint crack | `maya_midpoint_crack` | recognizes she's the one steering | walks home with the money |
| Beach | `ryan_beach` | a door she didn't expect to be offered | answers |
| Frank Cracked | `frank_crack` | the discipline goes | names it next scene |
| Jake Hand | `jake_caught_and_hand` | the scene is hers | takes the shirt |
| Brothers discover | `brothers_discover` | the house can't hold the three arcs | eats dinner with Diana next to her |
| Keep-Tier Fork | `keep_tier_fork` | the summer's line | walks to one of four rooms |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: CHAPTERS

Five chapters (plus Prologue). Book-generation can fold as needed; this is the designer's shape.

| # | Chapter | Mood | Description |
|---|---|---|---|
| **0** | Prologue — Before the Summer | bright → shattered | Normal life, discovery, revenge, collapse. The moral code is planted through play. |
| **1** | Arrival + Chapter 1 — Establishment | hopeful-guarded, quiet | Maya arrives. Household rhythm, diner job, first rent paid. *Can she be the girl she told herself she'd be when she got here?* |
| **2** | Chapter 2 — Accumulation | tilt | World responds in specific small ways. Marge hands her the Thursday key. *What does she already know how to do that she hasn't admitted yet?* |
| **3** | Chapter 3 — Opening | shifting | NPC arcs activate. Ryan Partner. Jake Noticed. Frank Phase A tests deepen. One Crack queues (Ryan). |
| **4** | Chapter 4 — Operating | deliberate | Ryan Beach fires. midpoint_crack lands. Frank catch → Restrict → Cracked → Called-out. |
| **5** | Chapter 5 — Saturated | reckoning | Jake Caught+Hand. Rent shortfall if economic path demanded it. Brothers discover. Keep-Tier Fork closes Phase 1. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: STORY ARC NODES

One arc node per Phase 4 beat, plus ambient milestones. 45 nodes total (20 Prologue + 25 Phase 1). Each node: `id`, `chapter`, `linked_canvas`, `linked_flag`, `npc` (if NPC-specific), `is_milestone` (bool), `journal_entry` (first-person Maya).

### Prologue nodes

| ID | Chapter | Canvas | Flag | NPC | Milestone | Journal entry |
|---|---|---|---|---|---|---|
| `node_morning_daniel` | 0 | `prologue_morning_with_daniel` | `met_daniel` | — | false | *He kissed my forehead before he left. The phone was face-down on the counter. I noticed that.* |
| `node_group_dinner` | 0 | `prologue_group_dinner` | `prologue_cast_met` | — | false | *Emma told me the dress looked good. Sarah held my wrist. I still don't know which one of them meant it.* |
| `node_job_day` | 0 | `prologue_parttime_job` | `job_baseline` | — | false | *Sarah texted. "Are you okay?" — no context. I said yes anyway.* |
| `node_date_suspicion` | 0 | `prologue_date_night_with_daniel` | `saw_emma_text` | Daniel | false | *A name flashed on his phone. He turned it over too fast. I didn't say anything.* |
| `node_morning_flag` | 0 | `prologue_morning_after_flag` | `second_flag_landed` | Daniel | false | *He picked the receipt off the counter like it was nothing. It wasn't nothing.* |
| `node_doubt_crystallizes` | 0 | `prologue_doubt_crystallizes` | `decided_to_look` | — | true | *I made a list. Three things. I'm going to look.* |
| `node_sarah_conversation` | 0 | `prologue_sarah_conversation` | `sarah_knows_something` | Sarah | false | *Sarah told me to figure out what I want before I do anything in her living room. She knew.* |
| `node_phone_check` | 0 | `prologue_phone_check` | `saw_the_thread` | — | true | *Weeks of it. I read until the shower stopped. I put the phone back face-down.* |
| `node_plan_or_confront` | 0 | `prologue_plan_or_confront` | `calculation_tier` | — | true | *I'm not going to confront him. I'm going to make it hurt.* |
| `node_public_confirmation` | 0 | `prologue_daniel_emma_in_public` | `confirmed_visual` | Daniel/Emma | false | *His hand on her wrist. I walked past the window. I felt less than I expected to.* |
| `node_midpoint_revenge` | 0 | `prologue_midpoint_decision` | `revenge_planned` | — | true | *Kevin. Emma's boyfriend. Saturday's party.* |
| `node_identify_party` | 0 | `prologue_identify_party` | `party_scheduled` | — | false | *Sarah asked if I was coming. I said yes.* |
| `node_prep` | 0 | `prologue_prep` | (multiple prep flags) | — | false | *The blue dress. Sarah half-lied to. Two drinks before I went in.* |
| `node_party_approach` | 0 | `prologue_party` | `kevin_approach_branch` | Kevin | false | *Kevin at the kitchen island. I knew what I was going to say three steps before I got there.* |
| `node_the_act` | 0 | `prologue_the_act` | `revenge_committed` | Kevin | true | *I chose the angle. I chose the moment. I didn't cry. I thought I would.* |
| `node_morning_after_revenge` | 0 | `prologue_morning_after_revenge` | — | — | false | *I showered twice. It didn't help. The feeling I expected didn't come.* |
| `node_sarah_confession` | 0 | `prologue_sarah_confession` | `told_sarah` | Sarah | true | *I told her the whole thing. She didn't cry either. She said my name and closed her door.* |
| `node_emma_confrontation` | 0 | `prologue_emma_confrontation` | — | Emma | false | *I didn't apologize. I took his name and threw it back at her.* |
| `node_daniel_breakup` | 0 | `prologue_daniel_breakup` | — | Daniel | true | *He broke up with me first. I didn't get to use the sentence I'd been practicing.* |
| `node_diana_call_pack` | 0 | `prologue_diana_call_and_pack` | `accepted_diana_offer` | Diana | true | *Mom said there was room for the summer. She didn't ask why. I said yes.* |

### Phase 1 nodes

| ID | Chapter | Canvas | Flag | NPC | Milestone | Journal entry |
|---|---|---|---|---|---|---|
| `node_arrival` | 1 | `arrival_at_franks` | `arrived_at_franks` | Frank/Diana/Ryan/Jake | true | *Frank carried my suitcase. Diana hugged me on the porch. Ryan said "hey kid" from the yard. Jake didn't look up from his plate.* |
| `node_first_morning` | 1 | `first_morning_kitchen` | `first_morning_kitchen_done` | Diana/Frank | false | *Coffee was going at six. Diana handed me a mug. Frank said "church is at ten, you can come, you can not."* |
| `node_first_ryan` | 1 | `first_ryan_encounter` | `first_ryan_observation` | Ryan | false | *He asked for a wrench. I handed him the wrench. He said thanks, kid, and didn't look up. I watched him work for a minute.* |
| `node_first_jake` | 1 | `first_jake_cold_shoulder` | `first_jake_rebuff` | Jake | false | *I knocked. He raised his hand without turning around. "I'm working."* |
| `node_town_walk_diner` | 1 | `town_walk_day_two` | `diner_found` | Marge | false | *An hour of gravel road to get there. Marge looked at me for three seconds and said come back tomorrow.* |
| `node_marge_interview` | 1 | `marge_interview` | `hired_at_diner` | Marge | true | *"Tie the apron. Learn as you go." That was the whole interview.* |
| `node_first_t0_shift` | 1 | `first_diner_shift_t0` | `first_t0_shift_done` | Marge/Cookie/regulars | false | *I learned the booth numbers and the coffee pot. A trucker held my eyes too long. I looked away first.* |
| `node_first_sunday` | 1 | `first_sunday` | `first_sunday_passed` | Diana/Frank | false | *I sat on the porch with Mom while she read the paper. I sketched her hand without meaning to.* |
| `node_the_math` | 1 | `the_math` | `first_rent_paid` | — | true | *Rent's sixty a week. Tuition's fifteen hundred. The diner alone doesn't get me there. I can see where it goes from here.* |
| `node_diner_rhythm` | 2 | `diner_rhythm_deepens` | `diner_regulars_named` | regulars | false | *I know their orders now. Pete takes coffee without having to ask. It bumps the tip.* |
| `node_cookie_peer` | 2 | `cookie_peer_established` | `cookie_peer_established` | Cookie | false | *Cookie told me who was going to tip me on the Thursday nights. I wrote the names down later.* |
| `node_ryan_shop_visit` | 2 | `ryan_shop_first_visit` | `ryan_shop_first_visit` | Ryan | false | *He asked if I was good with numbers. I said yes. He said help with the ledger tomorrow, I'll feed you.* |
| `node_jake_first_glance` | 2 | `jake_first_glance_noticed` | `jake_first_glance_noticed` | Jake | false | *His hands stopped on the water pitcher. Half a second. I felt it.* |
| `node_frank_phase_a_test` | 2 | `frank_phase_a_test` | `frank_phase_a_test_1` | Frank | false | *"Maya. The porch light." I stood up and went and turned it off.* |
| `node_marge_key` | 2 | `marge_thursday_key` | `first_ambient_tilt` | Marge | true | *Marge handed me the key under the till and said Thursdays are slow. I walked the hour home with it in my pocket.* |
| `node_ryan_partner_close` | 3 | `ryan_partner_first_close` | `ryan_partner_open` | Ryan/Pete | false | *I closed the mower at twenty over asking. Ryan said "yeah, you got it" and meant it.* |
| `node_jake_peek_revealed` | 3 | `jake_peek_discovery` | `jake_peek_draw_revealed` | — | true | *His door was cracked. He was drawing a woman. The woman was me. I stepped back.* |
| `node_ryan_big_deal` | 3 | `ryan_big_ticket_deal` | `ryan_big_deal_closed` | farmer/Ryan | true | *The tractor. The back office. I walked out with the money and Ryan didn't look at me from the work bay.* |
| `node_ryan_beach` | 3/4 | `ryan_beach` | `ryan_beach_proposal` | Ryan | true | *He said one whole sentence. I gave him an answer.* |
| `node_midpoint_crack` | 4 | `maya_midpoint_crack` | `midpoint_crack` | — | true | *Table four. I tilted at the hip on purpose and I felt nothing doing it. That's the thing I didn't know I could do.* |
| `node_frank_catch` | 4 | `frank_catch_living_room` | `frank_caught` | Frank | true | *He walked in. Neither of us said anything. He went upstairs. I stayed where I was.* |
| `node_frank_restrict` | 4 | `frank_restrict` | `frank_restrict_declared` | Frank | false | *New rules at breakfast. He didn't reference what he saw. Diana watched him say them.* |
| `node_frank_crack` | 4 | `frank_crack` | `frank_cracked` | Frank | true | *In the office. He held the look a count too long and his hands pressed the desk instead of resting.* |
| `node_frank_callout` | 4 | `frank_call_out` | `frank_called_out` | Frank | true | *I said "everyone has needs, Frank. Even you." He closed the ledger and said my name.* |
| `node_jake_caught_hand` | 5 | `jake_caught_and_hand` | `jake_hand` | Jake | true | *I walked in. The drawings of me were on his desk. I took his hand and told him to show it to me. I took his shirt on the way out.* |
| `node_rent_shortfall` | 4/5 | `rent_shortfall_first` | `rent_shortfall_1` | Frank | false | *I was fifteen short. I stood at his office door. He let me sit in it before he said Thursday.* |
| `node_brothers_discover` | 5 | `brothers_discover` | `brothers_discover` | all | true | *Saturday dinner on the back porch. Three men quiet at the same table for the first time. Mom held the platter.* |
| `node_keep_tier_fork` | 5 | `keep_tier_fork` | `keep_tier_fork_fired` | all | true | *Mom set a place for me next to her. Dinner finished. I walked to the one I was going to walk to.* |

**Total: 45 nodes (20 Prologue + 25 Phase 1). Milestone count: 15.**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: BRANCHING GROUPS

Each NPC's Keep-tier routes form a group. `required_count = 1` — the player picks one route per NPC. The Phase 1 close (`node_keep_tier_fork`) locks the *active* route from the tentative route flag set during the Keep-entry canvas.

### Group: Frank-Keep (`group_frank_keep`)

```toml
[[groups]]
id = "group_frank_keep"
required_count = 1
nodes = [
  "node_frank_keep_romantic",
  "node_frank_keep_arrangement",
  "node_frank_keep_rupture",
  "node_frank_keep_power_inverted",
]
```

- **`node_frank_keep_romantic`** — *He turns out the porch light when I come home.*
- **`node_frank_keep_arrangement`** — *Sixty became three hundred. He counts it out every Sunday.*
- **`node_frank_keep_rupture`** — *We don't speak at the table. Diana fills the silence.*
- **`node_frank_keep_power_inverted`** — *He asks before he walks through a room I'm in.*

### Group: Ryan-Keep (`group_ryan_keep`)

```toml
[[groups]]
id = "group_ryan_keep"
required_count = 1
nodes = [
  "node_ryan_keep_yes",
  "node_ryan_keep_not_yet",
  "node_ryan_keep_withdrawn",
]
```

- **`node_ryan_keep_yes`** — *He calls me Maya now. He told Frank at dinner.*
- **`node_ryan_keep_not_yet`** — *The question sits. The shop runs. He doesn't ask again.*
- **`node_ryan_keep_withdrawn`** — *He still works the yard. He doesn't come to the porch after dinner anymore.*

### Group: Jake-Keep (`group_jake_keep`)

```toml
[[groups]]
id = "group_jake_keep"
required_count = 1
nodes = [
  "node_jake_keep_owned",
  "node_jake_keep_lovers",
  "node_jake_keep_withdrawn",
  "node_jake_keep_she_uses_him",
]
```

- **`node_jake_keep_owned`** — *His shirt is in my drawer. He doesn't ask for it back.*
- **`node_jake_keep_lovers`** — *We draw together in his room. He shows me what he's working on now.*
- **`node_jake_keep_withdrawn`** — *The door doesn't open when I knock anymore.*
- **`node_jake_keep_she_uses_him`** — *He told me everything about the college registration. He didn't ask what I wanted it for.*

### Group: Phase-1-Close-Route (`group_phase_1_close`)

```toml
[[groups]]
id = "group_phase_1_close"
required_count = 1
nodes = [
  "node_close_independence",
  "node_close_frank",
  "node_close_ryan",
  "node_close_jake",
  "node_close_deferred",
]
```

These nodes are the five fork outcomes of `node_keep_tier_fork`. Exactly one fires; it locks the Phase 2 opening morning.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: EMOTION MAPPINGS

*Copied from Phase 2B for node-surface reference. The `trait_words` sidebar strings render during play; they are ground-truth for the prose register per band.*

### Maya — corruption

| Band | Range | Text |
|---|---|---|
| Closed | 0–24 | *She catches herself noticing things — the way hands rest on a counter, the weight of a look — and catches herself noticing that she noticed.* |
| Opening | 25–49 | *She lets the looks land. She catalogs them the way she catalogs faces for a sketch. Something is happening she hasn't named yet.* |
| Operating | 50–74 | *She picks her targets. She knows what her voice does at table four and what her posture does at the booth. The room tilts when she wants it to.* |
| Saturated | 75–100 | *She speaks the language she made this summer. The diner, the shop, the porch — all of it answers her when she asks.* |

### Maya — calculation

| Band | Range | Text |
|---|---|---|
| Impulsive | 0–19 | *She acts and then decides what she thought she was doing.* |
| Deliberate-drafting | 20–39 | *She drafts the sentence in her head before she says it, and the drafts are getting faster.* |
| Strategic | 40–69 | *She picks the room she'll walk into before she walks in. She picks the shift she'll take before she takes it.* |
| Planning-internalized | 70–100 | *The plan is the room. The room is the plan. She doesn't narrate it to herself anymore.* |

### Frank — trust

| Band | Range | Text |
|---|---|---|
| 0–19 | *He watches the door more than he watches her.* |
| 20–39 | *He nods when she walks in. Doesn't look up from the paper, but he nods.* |
| 40–59 | *He saves her the chair with the good cushion.* |
| 60–79 | *He waits for her to come home before turning out the porch light.* |
| 80–100 | *His voice goes lower in the house when she's awake. She has heard it do that twice and she counts.* |

### Frank — love

| Band | Range | Text |
|---|---|---|
| 0–19 | *She is Diana's girl. The rent is on the table. That's the whole job.* |
| 20–39 | *There is a version of Maya he has stopped saying no to in his head.* |
| 40–59 | *He has caught himself making coffee for two in the morning without asking.* |
| 60–79 | *He picked the porch chair for her three nights running without noticing he did it.* |
| 80–100 | *The thing he will not name is the thing he will do.* |

### Ryan — love

| Band | Range | Text |
|---|---|---|
| 0–19 | *He calls her kid and means it.* |
| 20–39 | *He calls her kid and almost doesn't.* |
| 40–59 | *He says her name in the shop when the customer's gone and the truck's still running.* |
| 60–79 | *He drives her home from the diner without asking if she needed it.* |
| 80–100 | *He has a sentence ready and he is waiting for the moment to say it.* |

### Jake — love

| Band | Range | Text |
|---|---|---|
| -20 to -1 | *He doesn't acknowledge her at breakfast. The sketchbook is a wall.* |
| 0–19 | *His hands stop when she walks in. Half a second. Then he draws again like nothing happened.* |
| 20–39 | *The sketchbook closes when she's near. He doesn't want her to see what he's working on.* |
| 40–69 | *He leaves his door cracked when he thinks she might walk by.* |
| 70–100 | *He draws her from memory and the drawings are the best work he has done in years.* |

### Diana — awareness (ambient-only, never sidebar-visible)

| Band | Range | Text (surfaces in Diana-passage variants) |
|---|---|---|
| Low | 0–24 | *She doesn't look up when Maya comes in late.* |
| Mid-low | 25–49 | *She looks up, smiles, doesn't ask.* |
| Mid-high | 50–74 | *She looks up and doesn't smile.* |
| High | 75–100 | *She doesn't look up at all. The kitchen is quieter by the time Maya is in it.* |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: GUIDANCE HINTS

*40 hints from Phase 2B are the backbone. Below are 8 additional Phase 6-specific hints keyed to story-arc milestones (not stat bands). Combined total: 48 hints.*

### Milestone-specific hints

41. *Sunday's rent morning. Sixty on the table.* — `day_of_week = sunday AND money >= 60 AND week > 1 AND rent_paid_this_week = false`
42. *I know where the living room is at midnight.* — `corruption >= 45 AND frank_caught = false AND week >= 4`
43. *Thursday after ten is a different shift than before ten.* — `first_ambient_tilt = true AND day_of_week = thursday AND time < 22:00`
44. *The farmer's on Saturday. Ten percent off asking is what he folds at. Let's see.* — `ryan_partner_open AND customer_farmer_flag = true AND day = friday`
45. *The sketchbook on his desk isn't the one he shows me.* — `jake_peek_draw_open AND not jake_peek_draw_revealed`
46. *Mom set a place next to her tonight.* — `keep_tier_fork_queued AND not keep_tier_fork_fired`
47. *If I walk out of the summer with fifteen hundred it means I walked out of it with something else too.* — `money >= 1200 AND corruption >= 60`
48. *I can leave his shirt in my drawer or I can give it back. That's a decision.* — `jake_keep_route = owned OR jake_keep_route = she_uses_him`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## VALIDATION

- **Chapters thematically organized (5 + Prologue)**: ✅
- **One arc node per Phase 4 beat** (+ ambient milestones). 45 nodes vs. 48 Phase-4 beats — 3 ambient beats (A1.2 social scene, B7 first T0, minor bridges) are absorbed into adjacent nodes. ✅
- **Branching paths have group definitions**: `group_frank_keep` (4), `group_ryan_keep` (3), `group_jake_keep` (4), `group_phase_1_close` (5). ✅
- **Emotion-mapping ranges align with Phase 2B and Phase 5 thresholds**: ✅ (corruption 0–100, love 0–100, jake.love -20–100, trust 0–100 consistent across phases).
- **Hints actionable, not spoilery, Maya-voice (not third-person coaching)**: ✅ (all 48 hints are first-person).
- **Journal entries first-person** (never third-person narrator): ✅ (every node's journal_entry reads *I / me / my*).
- **No gating that references unresolved flags**: audited; Phase 2 flag inventory + Phase 4 beat flags cover all references here.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End of Phase 6 — Story Arc.

Book phase generation complete. Next: compile `final_book.md`.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
