# PHASE 2B: SYSTEMS BUDGET
# The Long Summer

*Phase 2B is The Long Summer's fastest book phase — the redesign doc did the systems work up-front. Most of this file is transcription and formalization of decisions already made in `Game_Redesign.md` §1.6, §2.8, §2.11, §2.12, §3.7–3.8, §7.1–7.8, §8. Generative content is in the hint menu and gate-justification sections.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: WHITEBOARD GOALS

Goals are the in-fiction targets the game quietly asks the player to pursue. They replace a formal "endings" table — the game ends on the Keep-Tier Fork, and the goals are what Maya can look back on and say *I did that.* Every goal is surface-able on the Guide Page as a hint when the trigger conditions are close.

| # | Goal | Completion trigger | Hint surfaces when |
|---|---|---|---|
| **1** | **First rent paid.** Maya hands Frank sixty dollars on a Sunday morning for the first time. | `first_rent_paid = true` | Day 5 and money < $60 |
| **2** | **First ambient tilt — the Thursday key.** Marge trusts Maya enough to close Thursday alone. | `first_ambient_tilt = true` | Week 3 with `hired_at_diner = true` and `rep_road` rising |
| **3** | **One NPC arc to Keep tier.** At least one of Frank/Ryan/Jake reaches its Keep-tier milestone. | Any of `frank_keep_route`, `ryan_keep_route`, `jake_keep_route` set | When the corresponding Crack has fired |
| **4** | **Brothers discover.** The three men in the house (plus Diana as silent witness) register each other's awareness of Maya. | `brothers_discover = true` | Late Phase 1 with ≥2 NPC arcs at or past mid-tier |
| **5** | **College savings threshold approached** (stretch). Maya's tracked savings hit $1,500. | `money >= 1500` and `college_brochure_taken = true` | Any point savings cross $800 |

No goal is *required* for Phase 1 to close. Phase 1 closes on the **Keep-Tier Fork** (summer-end Diana-attended family dinner). The goals are the legible Guide-Page content during the run.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: ARCHETYPE ROSTER

Roster-as-functions. Each entry maps an archetypal role to the NPC(s) filling it. Some slots are multi-NPC (authority: Frank *and* Diana).

| Archetype | Filled by | Function |
|---|---|---|
| **Authority** | Frank (landlord, rule-enforcer) + Diana (household line-holder) | Enforces the house register; enforces the code Maya can violate without being caught |
| **Romance candidates** | Frank / Ryan / Jake | Three parallel arcs, each with its own trigger and Keep-tier routes |
| **Mentor (lite)** | Marge | Employer; reads Maya's steadiness; hands her the Thursday key |
| **Peer** | Cookie (diner) + ambient regulars | Provides a second female voice in the diner scenes; social-peer texture |
| **Safe harbor** | Diana | The kitchen at 6 a.m. is always Diana's. Her silence is the pressure, but her kitchen is the refuge. |
| **Clock** | Economic pressure (rent + groceries + college target) | The motor that tilts corruption upward unless actively resisted |
| **Threat (reserved)** | *none in Phase 1* | The Prologue ex does not return; the shadow layer does not activate; a Phase-1 external threat is deliberately absent |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: THREE-STAGE QUEST ARCS (PER DEEP NPC)

The 5-tier arc structures from §7.3–7.5 collapse cleanly to a 3-stage Introduction / Escalation / Climax shape for the 2B format. The full 5-tier structures live in Phase 6 (Story Arc).

### Frank — 3-stage

| Stage | Tiers collapsed | Opening gate | Closing milestone |
|---|---|---|---|
| **Introduction** | Meet (Phase A) + Rules established + Abide | Day 1 | First Frank rules-test beat passed |
| **Escalation** | Trigger (masturbation in living room) + Restrict + Tease under compliance | `corruption >= 50` + Maya-picks-living-room | Chore-supervision scenes live with `frank.arousal` ramping |
| **Climax** | Crack + Call-out + Keep | N chore-supervision scenes + `frank.arousal >= X` | `frank_keep_route` set (one of: romantic / arrangement / rupture / power_inverted) |

### Ryan — 3-stage

| Stage | Tiers collapsed | Opening gate | Closing milestone |
|---|---|---|---|
| **Introduction** | Meet + Help | `group_settled_in` + `first_ambient_tilt` | First small-ticket close witnessed |
| **Escalation** | Partner | N Help scenes + `corruption >= 25` | Mid-ticket close with charm |
| **Climax** | Big deal + Guilt + Beach + Keep | N Partner closes + `corruption >= 75` + customer flag | `ryan_keep_route` set (one of: yes_engaged / not_yet / no_withdrawn) |

### Jake — 3-stage

| Stage | Tiers collapsed | Opening gate | Closing milestone |
|---|---|---|---|
| **Introduction** | Meet (hostile) + Noticed | Day 1 + `beauty` crosses threshold | First glance noticed (hands-stop-mid-line beat) |
| **Escalation** | Peeking + drawing + Tease | Automatic after Noticed + `corruption` mid-band for Tease | Caught-beat becomes triggerable |
| **Climax** | Caught + Hand + Keep | Caught scene + Maya's deliberate offer | `jake_keep_route` set (one of: owned / lovers / withdrawn / she_uses_him) |

### Arc-clock cross-gating (per §7.6)

- **One Crack per chapter.** `one_crack_this_chapter` blocks a second Crack beat in the same chapter window.
- **Frank trigger is Maya-initiated.** Gates on *she picked the living room*, not on ambient timing.
- **Ryan clock is economic.** Gates on business tier + corruption.
- **Jake clock is physical.** Gates on beauty rising + corruption.
- **Diana accumulator runs in the background** through the whole game. Does not gate Phase 1 content. Seeds Phase 2.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: INCOME CHANNELS

Phase 1 runs on six channels. Base diner wage is mathematically tight. Tier 2 and a Ryan Partner cut are what make the college target plausible. The channels are deliberately uneven: the corruption-gated channels pay more, and the math is designed so that the $1,500 college target is *out of reach* without at least one corruption-tier unlock.

| # | Channel | Pay range | Gate | Energy cost |
|---|---|---|---|---|
| **1** | Diner base wage (T0 Distance shift) | $45 / shift (5 hours) | Always available from `hired_at_diner` | 40 energy |
| **2** | Diner tips (T1 Play along) | $8–20 / shift on top of base | `corruption` 25+ + `rep_road` ≥ 15 + `beauty` ≥ 45 | Same 40 energy; higher hygiene decay |
| **3** | Diner tips elevated (T2 Work the floor) | $25–60 / shift on top of base | `corruption` 50+ + `beauty` ≥ 55 | 50 energy (more active) |
| **4** | Diner extras (T3 Back booth after close) | $50–200 / scene (scene-by-scene agency) | `corruption` 75+ + specific customer flags + `first_ambient_tilt = true` | 25 additional energy |
| **5** | Ryan shop small-ticket cut | $10–25 / close | `ryan_help_tier_open` | 15 energy per close |
| **6** | Ryan shop big-ticket cut | $80–300 / close | `ryan_partner_open` + customer-mid/big flags + corruption gates per tier | 30 energy per close; may consume the whole afternoon |

### Weekly math (illustrative — tuned in Phase 3)

| Strategy | Weekly net (approx) | Time to $1,500 |
|---|---|---|
| **Pure T0 diner (no corruption)** | $45 × 5 shifts − $75 rent/groceries = $150 net | ~10 weeks — close to impossible before summer's end |
| **T1 + occasional Ryan Help** | ~$230 net | ~6.5 weeks |
| **T2 + Ryan Partner** | ~$380 net | ~4 weeks |
| **T2 sustained + Ryan Partner + one big-ticket** | $500+ net | 3 weeks for the bulk + stretch |
| **T3 scene + full stack** | Variable; can land $1500 in 2–3 weeks but costs rep_church + sets up arc-specific beats | — |

### Optional channels

- **Frank chores (post-trigger Phase B Restrict tier).** Small payments, $5–20 per task. Mechanic: Frank uses chores to keep Maya visible. The money is real, the purpose is supervision.
- **Sell sketches (deferred to Phase 2+).** Art track unlock; not an income channel in Phase 1.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: EMOTION MAPPINGS — `trait_words` BAND STRINGS

Emotion mappings are the `trait_words` sidebar strings (Engine F1). Each item mixes two match modes, evaluated **top-to-bottom, first match wins**:

1. **Flag-driven bands** (`{ flag = "...", text = "..." }`) fire on narrative milestones. Author top-down with the latest milestone first, so the most recent state shows through.
2. **Trait-value bands** (`{ min, max, text }`) are the continuous fallback when no flag row matches.

Strings are **4–8 words, third-person**. A band is either flag-mode OR value-mode, never both in the same entry.

Items can declare a `show_when = { version = "1.0", items = [...] }` gate (same dict shape as `entry_conditions`) to stagger NPC reveal. Target: **≤4 sidebar items visible at once.**

### Player — `corruption` (always on)

```toml
[[sidebar_items]]
type = "trait_words"
trait_owner = "player"
trait = "corruption"
bands = [
  # Flag-driven (latest milestone first)
  { flag = "keep_tier_fork_fired",  text = "Chose who to keep." },
  { flag = "brothers_discover",     text = "Three men know." },
  { flag = "frank_called_out",      text = "Said it out loud." },
  { flag = "midpoint_crack",        text = "Not performing now." },
  { flag = "first_ambient_tilt",    text = "Thursday key, Thursday weight." },
  { flag = "first_rent_paid",       text = "Rent on the table." },
  { flag = "arrived_at_franks",     text = "Different house. Same body." },
  { flag = "prologue_complete",     text = "Driving south." },
  { flag = "prologue_crossed_line", text = "Did the thing." },
  { flag = "prologue_saw_them",     text = "Saw what Sarah was." },
  { flag = "prologue_at_bed",       text = "Daniel's Sunday bed." },
  # Trait-value fallback
  { min = 0,  max = 24,  text = "Catching herself noticing." },
  { min = 25, max = 49,  text = "Letting the looks land." },
  { min = 50, max = 74,  text = "Picking the room." },
  { min = 75, max = 100, text = "Speaks the language she made." },
]
```

### Player — `calculation` (hides after Ryan opens, to keep ≤4 visible)

```toml
[[sidebar_items]]
type = "trait_words"
trait_owner = "player"
trait = "calculation"
show_when = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "ryan_help_tier_open", operator = "is_false" },
] }
bands = [
  { flag = "calc_tier_deliberate", text = "Drafts before she speaks." },
  { flag = "calc_tier_moderate",   text = "A beat, then the move." },
  { flag = "calc_tier_impulsive",  text = "Acts, then decides." },
  { min = 0,  max = 19,  text = "Acts. Decides after." },
  { min = 20, max = 39,  text = "Drafts the sentence first." },
  { min = 40, max = 69,  text = "Picks the room first." },
  { min = 70, max = 100, text = "The plan is the room." },
]
```

### NPC — `npc_frank.love` (reveals after first kitchen)

*`npc_frank.trust` is no longer a sidebar item — `love` carries the same emotional texture more legibly in one line.*

```toml
[[sidebar_items]]
type = "trait_words"
trait_owner = "npc"
npc_id = "npc_frank"
trait = "love"
show_when = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "first_morning_kitchen_done", operator = "is_true" },
] }
bands = [
  { flag = "frank_called_out",        text = "Admitted it aloud." },
  { flag = "frank_cracked",           text = "He's not pretending." },
  { flag = "frank_restrict_declared", text = "Rules, sharper now." },
  { flag = "frank_caught",            text = "He saw. He left." },
  { min = 0,  max = 19,  text = "Diana's girl. Rent due." },
  { min = 20, max = 39,  text = "Version he doesn't refuse." },
  { min = 40, max = 59,  text = "Coffee for two, unasked." },
  { min = 60, max = 79,  text = "Saves her the porch chair." },
  { min = 80, max = 100, text = "The thing he won't name." },
]
```

### NPC — `npc_ryan.love` (reveals when Ryan partnership opens)

```toml
[[sidebar_items]]
type = "trait_words"
trait_owner = "npc"
npc_id = "npc_ryan"
trait = "love"
show_when = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "ryan_help_tier_open", operator = "is_true" },
] }
bands = [
  { flag = "ryan_beach_proposal",  text = "He asked. She answered." },
  { flag = "ryan_big_deal_closed", text = "Big ticket closed." },
  { flag = "ryan_partner_open",    text = "Partner in the shop." },
  { flag = "ryan_help_tier_open",  text = "Watching him work." },
  { min = 0,  max = 19,  text = "Calls her kid. Means it." },
  { min = 20, max = 39,  text = "Calls her kid. Almost doesn't." },
  { min = 40, max = 59,  text = "Says her name in the shop." },
  { min = 60, max = 79,  text = "Drives her home, unasked." },
  { min = 80, max = 100, text = "Sentence ready. Waiting." },
]
```

### NPC — `npc_jake.love` (reveals after Jake's first glance)

```toml
[[sidebar_items]]
type = "trait_words"
trait_owner = "npc"
npc_id = "npc_jake"
trait = "love"
show_when = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "jake_first_glance_noticed", operator = "is_true" },
] }
bands = [
  { flag = "jake_hand",               text = "Took his shirt home." },
  { flag = "jake_caught",             text = "Found the drawings." },
  { flag = "jake_tease_open",         text = "Door cracked for her." },
  { flag = "jake_peek_draw_revealed", text = "He's been drawing her." },
  { flag = "jake_noticed_open",       text = "Hands stop, briefly." },
  { min = -20, max = -1,  text = "Sketchbook is a wall." },
  { min = 0,   max = 19,  text = "Hands pause when she walks in." },
  { min = 20,  max = 39,  text = "Sketchbook closes near her." },
  { min = 40,  max = 69,  text = "Leaves his door cracked." },
  { min = 70,  max = 100, text = "Draws her from memory." },
]
```

### Stagger math (≤4 visible at once)

| Phase | Flags set | Visible items | Count |
|---|---|---|---|
| Prologue start | — | corruption + calculation | 2 |
| Prologue mid | prologue_saw_them / prologue_crossed_line | corruption + calculation | 2 |
| Ch1 after first kitchen | first_morning_kitchen_done | corruption + calculation + Frank | 3 |
| Ch1 after Jake notice | jake_first_glance_noticed | corruption + calculation + Frank + Jake | 4 |
| Ch2 after Ryan help tier | ryan_help_tier_open | corruption + Frank + Jake + Ryan (calc hides) | 4 |
| Ch5 close | keep_tier_fork_fired | corruption + Frank + Jake + Ryan | 4 |

### Per-node flags added to the Prologue canvas

Three additive flagEffects were added to `prologue_morning_with_daniel` exit_blocks so the corruption sidebar can shift within the single-canvas Prologue. No existing behavior changed.

| Node | Flag set on exit | Sidebar text |
|---|---|---|
| N1 (wake → bed) | `prologue_at_bed` | "Daniel's Sunday bed." |
| N3 (classroom → home) | `prologue_saw_them` | "Saw what Sarah was." |
| N7 (upstairs → after) | `prologue_crossed_line` | "Did the thing." |

The existing `prologue_complete` flag (set at N10) continues to mark the Prologue close, rendering "Driving south." until `arrived_at_franks` fires.

### NPC — `diana_awareness` (4 bands — surface only through ambient Diana-prose, never as a visible sidebar stat)

```toml
# NOT a sidebar item. Used only by passage-level variant selection in Diana ambient scenes.
# Logical bands:
#   0-24  "She doesn't look up when Maya comes in late."
#   25-49 "She looks up, smiles, doesn't ask."
#   50-74 "She looks up and doesn't smile."
#   75-100 "She doesn't look up at all. The kitchen is quieter by the time Maya is in it."
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 6: HINT MENU

All hints are **Maya-voice**, not coach-voice. They surface on the Guide Page when their gate condition is true and the referenced target beat has not yet fired. Target: 40 hints across backbone + deep NPCs + corruption bands. Below is the Phase 2B inventory; Phase 6 expands with node-specific hints.

### Backbone hints (rent, college, Diana, routine — 8 hints)

1. *Rent's Sunday morning. The sixty bucks has to be on the table before Frank comes in from the porch.* — `money < 60 and day_of_week = sunday`
2. *The college brochure is on my nightstand. Tuition sits at fifteen hundred. The diner alone doesn't get me there.* — `college_brochure_taken and money < 1500`
3. *Mom cooks at five-thirty. I can help or I can not, but I shouldn't make her notice I chose not to.* — `day_time = late_afternoon and in_location = property`
4. *Sunday's church. I can go or stay. Staying means Mom reads on the porch alone until lunch.* — `day_of_week = sunday and not attended_church_this_week`
5. *My hygiene's slipping. The tips drop when the regulars notice.* — `hygiene < 60`
6. *I'm tired. Everything costs more when I'm tired.* — `energy < 40`
7. *The math is the math. Either I work Thursday alone or I don't hit the number.* — `money < 500 and week >= 3`
8. *I keep thinking about what Mom would say if she ever said it.* — `diana_awareness >= 50`

### Frank hints (Phase A + trigger + Phase B — 10 hints)

9. *Frank's porch at nine. He doesn't talk much but he notices when I sit down.* — `day_time = late_evening and frank.trust < 40`
10. *The office door is closed. He's working. I know when he's working and when he's pretending.* — `day_time = evening and in_location = hallway`
11. *The bookkeeping pays. It's an hour. I can sit through an hour.* — `corruption < 50 and money < 200`
12. *He asked me not to leave the living room light on after midnight. I didn't do it. He still asked.* — `frank_phase_a_test_1 and not frank_caught`
13. *I could do it in the living room. I could do it where he'd come home. I could.* — `corruption >= 45 and not frank_caught`
14. *He didn't say anything the next morning. That's worse than if he'd said something.* — `frank_caught and not frank_restrict_declared`
15. *The new rules aren't about the rules.* — `frank_restrict_declared`
16. *Every time he corrects me the correction is longer than it needs to be.* — `frank_tease_under_compliance_open`
17. *I could name it.* — `frank_cracked and not frank_called_out`
18. *He's been on the porch every night since.* — `frank_called_out`

### Ryan hints (Help → Partner → Big deal → Beach — 10 hints)

19. *Ryan's in the yard with the belt sander. He could use a water.* — `day_time = afternoon and ryan.trust < 30`
20. *He said the farmer's coming Saturday. The farmer folds ten percent. Let's see what he folds at if I'm standing in the yard.* — `ryan_partner_open and customer_farmer_flag`
21. *There's a guy coming in tomorrow who buys things he doesn't need when a pretty woman is there. Ryan said it like a joke.* — `ryan_partner_open and corruption >= 50`
22. *I could close the big one. I know what it would take. I know.* — `ryan_partner_open and corruption >= 75 and not ryan_big_deal_closed`
23. *The money's in my pocket and I can't look at it yet.* — `ryan_big_deal_closed and not ryan_beach_proposal`
24. *He hasn't said anything. He doesn't need to. He's getting the truck keys.* — `ryan_big_deal_closed and day_since_big_deal = 1`
25. *He wants an answer.* — `ryan_beach_proposal and not ryan_keep_route`
26. *The shop's been quiet since I said yes.* — `ryan_keep_route = yes_engaged`
27. *The shop's been quiet since I said not yet.* — `ryan_keep_route = not_yet`
28. *The shop's been quiet since I said no.* — `ryan_keep_route = no_withdrawn`

### Jake hints (Noticed → Peek → Tease → Caught → Hand — 8 hints)

29. *Jake hates me. It's fine. He can hate me.* — `jake.love < 0`
30. *His hands stopped when I walked in. Not for long, but they stopped.* — `jake_noticed_open and not jake_peek_draw_open`
31. *I heard him in the hallway when I was in the bathroom. I know I heard him.* — `jake_peek_draw_open and not jake_tease_open`
32. *I could lean on the doorframe. I could stay longer.* — `jake_tease_open and not jake_caught`
33. *There's a drawing on the floor by his bed. It's me.* — `jake_tease_open and corruption >= 60`
34. *He didn't hear me come in.* — `jake_caught_imminent`
35. *I decide what happens next.* — `jake_caught and not jake_hand`
36. *He hasn't come out of his room today.* — `jake_keep_route = withdrawn`

### Corruption-band preoccupations (4 hints)

37. *I keep drafting sentences in my head I haven't said yet.* — `corruption band = Closed (0-24)`
38. *I keep thinking about Frank's office drawer.* — `corruption band = Opening (25-49)`
39. *I know what the tip will be before the table sits down.* — `corruption band = Operating (50-74)`
40. *Millhaven has a rhythm and I'm in it.* — `corruption band = Saturated (75-100)`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 7: GATE JUSTIFICATIONS (IN-FICTION)

The five Phase-1-gated locations each have a *narrative* reason for being unreachable, not a mechanical lockout screen. These are the in-fiction reasons:

| Location | Gate | In-fiction justification |
|---|---|---|
| **Truck stop bar** | Phase 2+ | Maya hasn't had a reason to go. The diner does everything the bar does, legally and with Marge watching. The bar opens when she's chasing something the diner can't give her — or when a regular she knows from T2/T3 tells her *come by Friday*. |
| **Fairground** | Phase 2+ | Seasonal. The fair isn't on. Announcements in the newspaper reference the August week. (Deferred to Phase 2+ expansion.) |
| **High school stadium** | Phase 2+ | Friday night football hasn't started. First game is after Phase 1 closes. |
| **Church interior** | Phase 2+ | Maya attends the *front* of the church (parking lot, lawn, front steps) for `rep_church` gains without entering. Interior entry requires a sustained attendance pattern that doesn't land in Phase 1's runtime. |
| **Full community college campus** | Tuition-gated | Maya has the brochure. She hasn't paid the admission fee. The admin office lets her in for one brochure visit and then sends her back to Main Street. The campus itself is visible through the gate but she has no student ID. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 8: PHASE 2+ UNLOCK STUBS

*Listed as deferred content. No Phase 1 authoring happens in these areas.*

- **Diana's arc.** Opens in Phase 2. `diana_awareness` value carried forward. Three design seeds: (a) the first husband's death as backstory reveal, (b) Frank–Diana strain as Frank's Phase-1 Keep route bleeds into the marriage, (c) Diana finally speaking the sentence she has refused to speak in Phase 1. All reserved.
- **Shadow layer.** Criminal/drug undercurrent reserved. Ryan's sketchy buyer could open the surface if Phase 2 needs it. In Phase 1, Ryan's big-ticket buyers are all *legitimate* customers; the edge is their treatment of Maya, not the legality of the transaction.
- **Truck stop bar + fairground + stadium + full college.** Content stubs for Phase 2 expansion.
- **Friday football / Saturday market / fair.** Calendar beats deferred.
- **Peer NPC slot.** Cookie fills the Phase 1 peer need. If Phase 2 wants a deeper peer arc (college friend, waitress bond), the slot is open.
- **Owner/appraisal sexual dynamic for Marge.** Reserved. Phase 1 Marge stays clean.
- **Midpoint crack structure.** Locked placement between Ryan Beach and Frank Crack. Not a content stub — it is authored in Phase 4. Noted here because it depends on both prior arcs having fired.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## VALIDATION

- **Whiteboard goals:** 5 (≥5 required). ✅
- **Income channels:** 6 (≥4 required). ✅
- **Hints:** 40 (target 30–50). ✅
- **Emotion-mapping bands:** corruption 4 / calculation 4 / frank.trust 5 / frank.love 5 / ryan.love 5 / jake.love 5 / diana_awareness 4. ✅
- **Orphan flags:** none (Phase 2 flag inventory confirmed; Phase 2B introduces no new flags).
- **Phase 2+ content stubbed, not written.** ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End of Phase 2B — Systems Budget. Proceed to Phase 3: World Design.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
