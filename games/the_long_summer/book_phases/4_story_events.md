# PHASE 4: STORY EVENTS
# The Long Summer

*The heavy phase. Prologue (~20 beats) + Phase 1 (~25 beats) = ~45 beats total. Each beat specified with canvas metadata, node structure, flag/stat effects, and branching choices. Per-beat prose is kept tight (~150–300 words) so the TOML translator can extract structure without inventing content.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## DRAMATIC STRUCTURE

### Central tension

Maya arrived carrying a moral code the town doesn't enforce. Diana still enforces it in the kitchen at 6:30. The game is which code wins each time the two registers touch. The Prologue plays the first register's collapse. Phase 1 plays the second register's construction.

### Primary conflicts

| Conflict | Driver | Where it plays |
|---|---|---|
| **Economic** | Rent + groceries + tuition math | Diner, Ryan's shop, The Math canvas |
| **Household power** | Frank's rules (Phase A), then his wanting (Phase B) | Property scenes, office, living room, Crack + Call-out |
| **Shared economic** | Ryan's failing shop | Yard, shop, big-deal canvas, beach |
| **Social / register** | Jake's hostility + noticing + shame | Jake's room, hallway, bathroom, yard, Caught scene |
| **Silent trust** | Diana's watching without saying | Kitchen, dinner table, Sunday porch, `diana_awareness` accumulator |

### Tension curve

```
Prologue: Normal → Discovery → Revenge → Collapse  (high→low→high→crash)

Phase 1:  Arrival (low but awake)
        → Ch1 Establishment (small rises)
        → Ch2 Accumulation (visible tilt — Marge key)
        → Ch3+ escalation (first Crack fires)
        → midpoint crack (Maya's internal beat)
        → brothers_discover
        → Phase 1 close (Keep-Tier Fork dinner)
```

**At most one Crack per chapter.** First Crack by design is Ryan's Beach (Ch 3–4 window); Frank's Crack and Jake's Caught+Hand alternate across Ch 4–5. `midpoint_crack` (Maya's) sits between Ryan Beach and Frank Crack.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PART A: PROLOGUE (PHASE 0) — ~20 BEATS

All Prologue canvases have `priority = 10`, `is_repeatable = false`, `phase = "prologue"`. Cast: Daniel, Emma, Kevin, Sarah, Diana (phone only).

---

### ACT 1 — THE NORMAL LIFE (6 beats)

#### Beat P1.1 — `prologue_morning_with_daniel`

- **Canvas**: `prologue_morning_with_daniel`
- **Location**: `loc_prologue_daniels_apartment`
- **NPC**: Daniel
- **Schedule**: morning, Day -28 (four weeks before arrival at Frank's)
- **Trigger**: game start
- **Priority**: 10 / **is_repeatable**: false

**Nodes**:
1. **Wake**: Maya wakes in Daniel's bed. Light through cheap blinds. His arm over her stomach. She lies still a minute. The narrator is warm, trusting; no corruption register yet.
2. **Coffee scene**: Kitchen. Two mugs. Daniel's phone lights face-down on the counter — the first flag. Maya notices, doesn't name it.
3. **Kiss at the door**: He's leaving for class. She's working tonight. *"Tonight?"* *"Tonight."* Warm, normal.

**Choices**: none (establishment beat).
**Effects**: sets `met_daniel`. Sets starting `daniel_trust = 100` internal marker for the Prologue's collapse curve.
**Consequence echo**: the kitchen in Phase 1 Day 1 is deliberately written to rhyme with this one — same morning-kitchen register, different people.

---

#### Beat P1.2 — `prologue_social_scene`

- **Canvas**: `prologue_group_dinner`
- **Location**: `loc_prologue_restaurant`
- **NPCs**: Daniel, Emma, Kevin, Sarah
- **Schedule**: evening, Day -25
- **Trigger**: after P1.1

**Nodes**:
1. **Arrival**: the group at a corner booth. Maya meets the whole cast in one beat. Sarah's hand on Maya's wrist when she sits — a best-friend tell Maya won't notice until it's gone.
2. **Small talk**: Daniel across from Emma. Kevin next to Sarah. Three-way conversation where Maya can *hear* the right arrangement.
3. **Bathroom beat**: Maya in the mirror washing her hands. Emma comes in, stands next to her, says *"That dress looks really good on you."* Flat. Sincere or not — ambiguous. Seeds.

**Choices**:
- *Say thank you* → `emma_read = neutral`
- *Say "thanks, I needed it tonight"* → `emma_read = tested` (seeds Maya's later suspicion)

**Effects**: sets `prologue_cast_met`. `emma_read` shapes Act 2.

---

#### Beat P1.3 — `prologue_job_day`

- **Canvas**: `prologue_parttime_job`
- **Location**: `loc_prologue_workplace` (coffee shop, bookstore — TBD content pass but consistent per playthrough)
- **NPC**: none primary
- **Schedule**: afternoon, Day -22
- **Trigger**: after P1.2

**Nodes**:
1. **Shift**: Maya competent, ordinary. No calculation yet.
2. **End-of-shift flag**: Sarah texts. *Are you okay?* No context.

**Choices**:
- *Tell her I'm fine.*
- *Ask what she means.* → `sarah_suspicion_surfaced = true`

**Effects**: money +$45 (the Prologue's only income). Sets `job_baseline`.

---

#### Beat P1.4 — `prologue_date_night_suspicion`

- **Canvas**: `prologue_date_night_with_daniel`
- **Location**: `loc_prologue_daniels_apartment`
- **NPC**: Daniel
- **Schedule**: evening, Day -19
- **Trigger**: after P1.3

**Nodes**:
1. **Dinner in**: Daniel cooks. It's good. Maya almost forgets the phone-face-down thing.
2. **The detail**: Daniel's phone lights. He turns it over too quickly. A name flashes. Maya sees *Emma*. He doesn't explain.
3. **The bedroom**: Maya goes through the motions. Her narrator's voice has pulled back by an inch. Calculation +1.

**Choices**:
- *Say something now.* → early confrontation fork (shorter Prologue, different end-state)
- *Say nothing.* → continues to P1.5

**Effects**: calculation +2. Sets `saw_emma_text`.

---

#### Beat P1.5 — `prologue_morning_after_flag`

- **Canvas**: `prologue_morning_after_flag`
- **Location**: `loc_prologue_daniels_apartment`
- **NPC**: Daniel
- **Schedule**: morning, Day -18
- **Trigger**: after P1.4 (if Maya chose *say nothing*)

**Nodes**:
1. **Kitchen**: coffee. Daniel cheerful. Maya's narrator sharper than her voice. The kitchen from P1.1 reads different now.
2. **Second flag**: Daniel's wallet open on the counter. A receipt from a place Maya doesn't know about. He picks it up fast.

**Effects**: calculation +1, sets `second_flag_landed`.

---

#### Beat P1.6 — `prologue_doubt_crystallizes`

- **Canvas**: `prologue_doubt_crystallizes`
- **Location**: `loc_prologue_mayas_apartment`
- **NPC**: (solo)
- **Schedule**: late, Day -17
- **Trigger**: after P1.5

**Nodes**:
1. **Alone**: Maya on her bed. Lists in her head everything she's noticed. Three items.
2. **Decision**: she decides to *look*. Stands up. Closes her door. Act 2 opens.

**Effects**: sets `decided_to_look`. calculation +2.

---

### ACT 2 — DISCOVERY (5 beats)

#### Beat P2.1 — `prologue_conversation_with_sarah`

- **Canvas**: `prologue_sarah_conversation`
- **NPC**: Sarah
- **Schedule**: afternoon, Day -15
- **Trigger**: after P1.6

**Nodes**:
1. **Sarah's couch**: Maya says the word *Emma*. Sarah goes quiet. She says *Maya.* That's all. Sarah knows something.
2. **The ask**: Maya asks. Sarah says, *"Don't do it in my living room. Figure out what you want first."*

**Choices**:
- *Drop it.* → `sarah_declined` (diverges later)
- *Press on.* → `sarah_soft_confirmed`

**Effects**: sets `sarah_knows_something`.

---

#### Beat P2.2 — `prologue_phone_check_fork`

- **Canvas**: `prologue_phone_check`
- **NPC**: Daniel (off-screen)
- **Schedule**: evening, Day -13

**Nodes**:
1. **Opportunity**: Daniel's in the shower. Phone on the nightstand.
2. **Maya's hand**: the screen. The thread. *Emma.* Weeks of it.

**Choices**:
- *Look.* → sets `saw_the_thread`, calculation +3
- *Don't look.* → forks to a different Act 2 (confront without evidence branch; shorter Prologue)

**Effects**: sets `saw_the_thread` on look.

---

#### Beat P2.3 — `prologue_plan_or_confront`

- **Canvas**: `prologue_plan_or_confront`
- **NPC**: (solo)
- **Schedule**: late, Day -13

**Nodes**:
1. **Maya alone**: reads the thread again in her head. Two paths.

**Choices (midpoint decision — sets `calculation_tier`)**:
- *Confront him tonight.* → `calculation_tier = impulsive`; Prologue's short branch
- *Wait. Plan.* → `calculation_tier = moderate`; continues
- *Wait. Make it hurt.* → `calculation_tier = deliberate`; the longest, most weighted Prologue

**Effects**: sets `calculation_tier` (the central Prologue output). calculation stat adjusts accordingly.

---

#### Beat P2.4 — `prologue_public_confirmation`

- **Canvas**: `prologue_daniel_emma_in_public`
- **NPCs**: Daniel + Emma (Maya observing)
- **Schedule**: afternoon, Day -11
- **Trigger**: after P2.3 (only on *Wait. Plan* or *Make it hurt*)

**Nodes**:
1. **Coffee shop window**: Maya sees them. His hand on Emma's wrist. Daniel laughs. Emma laughs.
2. **Maya walks on by**: Calculation +3. She feels nothing she didn't feel before, which is the worst part.

**Effects**: sets `confirmed_visual`. calculation +3.

---

#### Beat P2.5 — `prologue_midpoint_revenge_decision`

- **Canvas**: `prologue_midpoint_decision`
- **NPC**: (solo, Maya's room)
- **Schedule**: late, Day -11

**Nodes**:
1. **Maya on the edge of her bed**: the decision isn't *confront him* or *leave him*. The decision is *what does she do?*
2. **The plan forms**: Kevin. Emma's boyfriend. The party Saturday.

**Choices**:
- *Do it.* → sets `revenge_planned`
- *Don't.* → `backed_out_early` (different Act 3)

**Effects**: sets `revenge_planned` on Do it.

---

### ACT 3 — THE REVENGE (4 beats)

#### Beat P3.1 — `prologue_identify_party`

- **Canvas**: `prologue_identify_party`
- **NPC**: Sarah, ambient
- **Schedule**: evening, Day -10

**Nodes**:
1. **Sarah texts**: *Mutual friend's thing Saturday. You coming?*
2. **Maya replies**: *Yes.*

**Effects**: sets `party_scheduled`.

---

#### Beat P3.2 — `prologue_prep_scene`

- **Canvas**: `prologue_prep`
- **NPC**: Maya solo at mirror + bathroom
- **Schedule**: evening, Day -8

**Nodes**:
1. **What to wear**: three choices, each moves `calculation` and `beauty` differently.
2. **What to tell Sarah**: lie / half-truth / nothing.
3. **Drink or not**: tracks into Phase 1 as `drinks_at_party`.

**Choices**:
- wardrobe: *the safe thing / the blue thing / the black thing* (each +beauty differently, seeds later Phase 1 color-reference prose)
- Sarah-lie tier: *nothing / some of it / everything* (interacts later with `told_sarah`)
- drink: *sober / buzzed / drunk* (sets `drinks_at_party`)

**Effects**: beauty minor adjustment; calculation +2; multiple flags set.

---

#### Beat P3.3 — `prologue_party_approach`

- **Canvas**: `prologue_party`
- **NPCs**: Kevin + ambient party
- **Schedule**: late, Day -7

**Nodes**:
1. **Arrival**: mutual friend's place. Music, crowd. Daniel isn't there; Emma isn't there.
2. **Maya scans**: Kevin at the kitchen island. Alone with a beer.
3. **Approach**: Maya crosses. Four feet. Three. Two.
4. **First line**: Maya picks the opening from three options.

**Choices (opening line)**:
- *"Where's Emma?"* → sets `kevin_knows` false; he doesn't know about Daniel
- *"I saw your girlfriend today at the coffee shop. You should ask her about that."* → sets `told_kevin` true; heavier collapse
- *"I need someone to not be Daniel tonight."* → the direct line; calculation -1 (honest), shame +1 later

**Effects**: sets opening-line branch; locks `kevin_approach_branch`.

---

#### Beat P3.4 — `prologue_the_act`

- **Canvas**: `prologue_the_act`
- **NPC**: Kevin
- **Schedule**: late, Day -7 into Day -6

**Nodes**:
1. **Upstairs**: the bedroom the host said no one should be in. Kevin already complicit.
2. **The moment she could back out**: three separate beats offer an out. Each back-out forks to `backed_out_of_revenge = true`.
3. **The act**: narrated cleanly — not pornographic, not coy. Her agency is the content. Prose reads *deliberate*. Sets `revenge_committed`.

**Choices (agency-preserving beats, each an off-ramp)**:
- At the bedroom door: *leave / stay*
- At the first undressing: *leave / stay*
- At the bed: *leave / stay*

**Effects**: on full commit → `revenge_committed = true`, corruption +18, calculation +5 (if `deliberate`) or +2 (if `impulsive`). `backed_out_of_revenge = true` on any off-ramp; corruption +5 only, calculation flat. Shame engine established either way (she *considered* doing it — that counts).

---

### ACT 4 — THE COLLAPSE (5 beats)

#### Beat P4.1 — `prologue_morning_after_revenge`

- **Canvas**: `prologue_morning_after_revenge`
- **NPC**: (solo)
- **Schedule**: morning, Day -6

**Nodes**:
1. **Maya's room**: the hoodie from the party on the floor. She showers twice. Doesn't feel anything she expected.
2. **Sarah calls**: *"I need to see you."*

**Effects**: hygiene restored; corruption sits; shame engine live.

---

#### Beat P4.2 — `prologue_sarah_confession_fork`

- **Canvas**: `prologue_sarah_confession`
- **NPC**: Sarah
- **Schedule**: afternoon, Day -5

**Nodes**:
1. **Sarah's living room**: she already knows. Kevin told Emma; Emma told Sarah.
2. **Sarah's question**: *"Tell me yourself."*

**Choices (sets `told_sarah`)**:
- *Tell her everything.* → `told_sarah = true`; Sarah closes off, friendship cracks, respects the honesty but doesn't forgive
- *Deflect.* → `told_sarah = false`; Sarah hears it confirmed by silence, friendship ends colder

**Effects**: `told_sarah` set. Sarah-relationship ends (she's Prologue-only, no carry forward).

---

#### Beat P4.3 — `prologue_emma_confrontation`

- **Canvas**: `prologue_emma_confrontation`
- **NPC**: Emma
- **Schedule**: evening, Day -4

**Nodes**:
1. **Public**: parking lot after Maya's shift. Emma waiting at the curb.
2. **The beat**: slap / scream / silence — player picks.
3. **Aftermath**: the ring of people who watched.

**Choices**:
- *Apologize.* → rep_church-analog hit (not tracked, but shame +1)
- *Defend.* → *"He cheated on me with you. Take it up with him."* — calculation +2
- *Walk away silent.* → the longest silence. calculation +3, shame internalized harder.

**Effects**: public record of Maya's act established in the Prologue town. This doesn't carry forward (different town in Phase 1) but shapes the flashback texture.

---

#### Beat P4.4 — `prologue_daniel_breakup`

- **Canvas**: `prologue_daniel_breakup`
- **NPC**: Daniel
- **Schedule**: late, Day -3

**Nodes**:
1. **He comes to her door**: he already knows. He breaks up with her first. She doesn't get first-move satisfaction.
2. **Maya's reply**: throws Emma back at him. Moral high ground burns for everyone.

**Effects**: relationship over. The Prologue's weight lands.

---

#### Beat P4.5 — `prologue_diana_call_and_pack`

- **Canvas**: `prologue_diana_call_and_pack`
- **NPC**: Diana (phone only — first time player hears her)
- **Schedule**: evening, Day -2 → morning, Day 0

**Nodes**:
1. **Phone rings**: Diana. *"Maya, honey. You sound tired."* She senses something, doesn't pry. *"Come stay with me and Frank for the summer. There's room. You don't have to say why."*
2. **Pause**: Maya closes her eyes.
3. **Maya says yes**.
4. **Pack scene**: she folds the funeral dress last. Puts it in the suitcase. Closes it.
5. **The drive**: transition montage. Phase 1 opens on her pulling into the driveway at 5:00 p.m. Saturday.

**Effects**: sets `accepted_diana_offer = true`. Prologue ends. Phase 1 opening canvas queued.

---

**Prologue beat count: 20.** (Act 1: 6 / Act 2: 5 / Act 3: 4 / Act 4: 5.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PART B: PHASE 1 — ~25 BEATS

### ARRIVAL (1 beat)

#### Beat B1 — `arrival_at_franks`

- **Canvas**: `arrival_at_franks`
- **Location**: `loc_front_porch`
- **NPCs**: Frank, Diana; Ryan and Jake emerge later in the scene
- **Schedule**: Saturday, Week 1, 17:00
- **Trigger**: Prologue complete (`accepted_diana_offer = true`)
- **Priority**: 10 / **is_repeatable**: false

**Nodes**:
1. **Driveway**: Maya's car on the gravel. Heat through the windshield. The screen door opens before she turns off the engine.
2. **Diana on the porch**: *"Maya, honey."* Hug. Diana smells like laundry soap and basil from the side garden.
3. **Frank in the doorway**: *"Maya."* The name as a full sentence. Offers to carry the suitcase. She lets him.
4. **Hallway**: shows her the room. *"Bathroom's across the hall. Dinner's at six-thirty."*
5. **Ryan from the yard**: calls *"Hey kid"* without coming in.
6. **Jake at dinner**: headphones around his neck. Doesn't look up from his plate. Diana says his name once. He nods. That's it.

**Choices**: none (establishment).
**Effects**: sets `arrived_at_franks`, `met_diana_day_1`, `met_frank_day_1`, `met_ryan_day_1`, `met_jake_day_1`. All three NPC arcs enter Meet tier. Frank.trust = 10 baseline; Jake.love = -5; Ryan.trust = 5.
**Consequence echo**: the kitchen at the first dinner will be rewritten at `diana_awareness` bands later — same dinner, different silences.

---

### CHAPTER 1 — ESTABLISHMENT (9 beats, closes on `first_rent_paid`)

#### Beat B2 — `first_morning_kitchen`

- **Canvas**: `first_morning_kitchen`
- **Location**: `loc_kitchen`
- **NPCs**: Diana, Frank
- **Schedule**: Sunday, Week 1, 07:00
- **Trigger**: `arrived_at_franks`

**Nodes**:
1. **Coffee already going**: Diana at the counter. Frank at the table with the paper. Nobody talks for the first minute.
2. **Diana hands Maya a mug**: *"Sit."*
3. **Frank's line**: *"Church is at ten. You can come. You can not."*

**Choices**:
- *I'll come.* → rep_church +2, `attended_church_week_1`
- *I'll stay.* → Diana nods once.

**Effects**: sets `first_morning_kitchen_done`. energy +10 from coffee, rest from travel.

---

#### Beat B3 — `first_ryan_encounter`

- **Canvas**: `first_ryan_encounter`
- **Location**: `loc_yard`
- **NPC**: Ryan
- **Schedule**: Sunday, Week 1, afternoon
- **Trigger**: after B2

**Nodes**:
1. **Yard**: Ryan under the hood of his truck. Grease on his forearm. Doesn't look up when Maya walks out.
2. **The exchange**: *"Wrench'd help."* She hands it. *"Thanks kid."*
3. **Observation**: Maya watches him work for a minute without being asked. He notices but doesn't acknowledge.

**Choices**:
- *Stay and watch.* → ryan.trust +2
- *Go back inside.* → neutral

**Effects**: Ryan Meet tier progressing. Sets `first_ryan_observation`.

---

#### Beat B4 — `first_jake_cold_shoulder`

- **Canvas**: `first_jake_cold_shoulder`
- **Location**: `loc_hallway`
- **NPC**: Jake
- **Schedule**: Sunday, Week 1, evening
- **Trigger**: after B3

**Nodes**:
1. **Hallway**: Maya passes Jake's door. Open a crack. He's at the desk, headphones on.
2. **Maya knocks**: *"Hey, I just wanted to say—"* He doesn't turn. Raises one hand. *"I'm working."*
3. **Maya retreats**: jake.love -2 confirmed hostile.

**Effects**: Jake Meet-hostile tier confirmed. Sets `first_jake_rebuff`.

---

#### Beat B5 — `town_walk_diner_discovery`

- **Canvas**: `town_walk_day_two`
- **Location**: `loc_driveway` → `loc_main_street` → `loc_diner`
- **NPC**: Marge (introduced in the diner)
- **Schedule**: Monday, Week 1, mid-morning
- **Trigger**: after B2 (next day)

**Nodes**:
1. **The walk**: hour of gravel and county road. First ambient encounter fires (pickup truck slows).
2. **Main Street**: Maya walks the three blocks. Registers the diner sign.
3. **Diner interior**: Marge behind the counter. *"Help you?"*
4. **Maya's ask**: *"Are you hiring?"* Marge's look: a full three-second appraisal. *"Come back tomorrow. Five p.m. Can you stay till ten?"* *"Yes."* *"See you then."*

**Choices**: none.
**Effects**: sets `diner_found`, `interview_scheduled`. money -$0 (she walked).

---

#### Beat B6 — `marge_interview_and_hire`

- **Canvas**: `marge_interview`
- **Location**: `loc_diner_front`
- **NPC**: Marge
- **Schedule**: Tuesday, Week 1, 17:00
- **Trigger**: after B5

**Nodes**:
1. **Arrival**: apron on the counter. *"Tie it. Learn as you go."*
2. **Shift**: first two hours of Maya shadowing Cookie + watching tables.
3. **End**: *"Tomorrow 5 to 10. $9 an hour. Tips are yours."* Sets the base wage.

**Effects**: sets `hired_at_diner`. First small paycheck queued.

---

#### Beat B7 — `first_t0_shift`

- **Canvas**: `first_diner_shift_t0`
- **Location**: `loc_diner_front`
- **NPCs**: Marge, Cookie, ambient regulars
- **Schedule**: Wednesday, Week 1, 17:00–22:00
- **Trigger**: after B6
- **is_repeatable**: false (first-shift variant); later shifts use a repeatable canvas with block pool variants (see Phase 5)

**Nodes**:
1. **The floor**: Maya learns the booth numbers, the checks, the coffee pot.
2. **Trucker regular's first look**: he holds eye contact a beat too long. Maya breaks first.
3. **End of shift**: Marge pays cash. $45. Maya walks the hour home in the dark.

**Choices**:
- At the trucker's look: *hold the look / look down / smile and look away* (each nudges corruption + rep_road differently, but T0 caps low)

**Effects**: sets `first_t0_shift_done`. money +$45. hygiene -15 (long shift).

---

#### Beat B8 — `first_sunday`

- **Canvas**: `first_sunday`
- **Location**: `loc_front_porch` / `loc_church_front` / `loc_kitchen`
- **NPCs**: Diana, Frank, Ryan
- **Schedule**: Sunday, Week 2
- **Trigger**: week advances past first diner shift

**Nodes**:
1. **Rent on the table**: Diana's note. *Leave sixty for Frank before church.* Maya pays (money -$60). First time she writes that line into her mental ledger.
2. **Church choice**: attend / stay.
3. **Sunday afternoon porch**: Diana with the paper. Maya sketches Diana's hand without meaning to.

**Choices**:
- Church: attend → rep_church +3
- Church: stay → Diana reads; Maya sketches.

**Effects**: advances `first_sunday_passed`. Opens **The Math** next.

---

#### Beat B9 — `the_math` (CH 1 CLOSE — milestone)

- **Canvas**: `the_math`
- **Location**: `loc_mayas_bedroom`
- **NPC**: (solo)
- **Schedule**: Sunday, Week 2, late
- **Trigger**: `first_sunday_passed` and rent paid once

**Nodes**:
1. **Maya at the desk with a calculator app**: money in pocket, rent for the next week already owed, the college brochure on the nightstand.
2. **The math**: $60 rent × weeks × summer + $15 groceries × weeks + tuition target $1,500 − what she'll earn at T0. It doesn't work.
3. **The internal line**: *"There's more tier available if I want it. I can see where it goes from here."*
4. **Sets the chapter-close**: `first_rent_paid = true` if she paid on B8 (she did). **Closes Ch 1.**

**Effects**: sets `first_rent_paid` (**milestone**). Opens `group_settled_in`. Ch 2 beats now reachable.
**Consequence echo**: the brochure line will resurface in the Ch2 hints and in the Operating-band sidebar text.

---

**Chapter 1 = 9 beats: Arrival (B1) + 8 Ch1 beats.** No NPC-arc escalations. No Frank catch. No Jake peek. No Ryan big-ticket. College brochure only (via Sunday porch reference, not yet a visit).

---

### CHAPTER 2 — ACCUMULATION (6 beats, closes on `first_ambient_tilt`)

#### Beat B10 — `diner_rhythm_deepens`

- **Canvas**: `diner_rhythm_deepens`
- **Location**: `loc_diner_front`
- **NPCs**: Marge, Cookie, named regulars
- **Schedule**: Tuesday, Week 3 (specific shift)
- **Trigger**: `first_rent_paid` and N completed shifts

**Nodes**:
1. **Maya knows the regulars now**: names the older mechanic (Pete) without asking. *"Coffee."* Delivered without the question.
2. **Variant shift**: same shift canvas as B7 but prose-inventory has shifted per Chekhov detail — the things she notices have tilted.
3. **Tip bump**: small. $7 on top of base. First real tip night.

**Effects**: sets `diner_regulars_named`. money +$52. Opens T1 gate check.

---

#### Beat B11 — `cookie_peer_established`

- **Canvas**: `cookie_peer_established`
- **Location**: `loc_diner_kitchen` (back step)
- **NPC**: Cookie
- **Schedule**: Thursday, Week 3, 20:00 smoke break
- **Trigger**: after B10

**Nodes**:
1. **Back step**: Cookie on her cigarette. *"You gonna make it, new girl?"* Maya: *"I'm gonna."* Cookie: *"Yeah you are. Hang a second, I'll tell you who's gonna tip you."*
2. **Information**: Cookie runs down the Thursday-night regulars. Trucker shift peak. Pete on Tuesdays. The church couple Saturdays.

**Effects**: sets `cookie_peer_established`. Primes T1-to-T2 awareness.

---

#### Beat B12 — `ryan_shop_first_visit`

- **Canvas**: `ryan_shop_first_visit`
- **Location**: `loc_shop_customer_area`
- **NPC**: Ryan
- **Schedule**: Saturday, Week 3, afternoon
- **Trigger**: `group_settled_in` and Maya walks to shop

**Nodes**:
1. **The shop**: Ryan rebuilding a carb at the counter. Doesn't look up when she comes in. *"You lost?"*
2. **Maya watches**: a walk-in customer. Maya sees how Ryan talks to him — the fragments, the ten-percent dance.
3. **After the customer**: *"You any good with numbers?"* *"Yeah."* *"Help me with the ledger tomorrow. I'll feed you."*

**Effects**: sets `ryan_shop_first_visit`, `ryan_help_tier_open`. Ryan Help tier live.

---

#### Beat B13 — `jake_first_glance_noticed`

- **Canvas**: `jake_first_glance_noticed`
- **Location**: `loc_kitchen`
- **NPCs**: Jake, Diana (ambient)
- **Schedule**: Thursday, Week 4, 17:15
- **Trigger**: `beauty >= 45` (after ~3 weeks of maintenance)

**Nodes**:
1. **Kitchen**: Maya at the counter cutting okra for Diana. Jake walks in for the cold water pitcher.
2. **The beat**: his hands stop on the pitcher. Half a second. He drinks, closes the fridge, leaves.
3. **Maya's narrator catches it**: she doesn't name it. But she notices.

**Effects**: sets `jake_first_glance_noticed`, `jake_noticed_open`. Jake Noticed tier live.
**Consequence echo**: every kitchen scene after this reads slightly differently — Jake-absent scenes include the small fact of him not being there.

---

#### Beat B14 — `frank_phase_a_test_1`

- **Canvas**: `frank_phase_a_test`
- **Location**: `loc_front_porch`
- **NPC**: Frank
- **Schedule**: Sunday, Week 4, evening
- **Trigger**: after B8 (a week later, Maya left the porch light on past midnight on Saturday)

**Nodes**:
1. **Porch**: Maya sits down beside him. Frank doesn't turn.
2. **The rule**: *"Maya. The porch light."* The whole correction. One sentence.
3. **Maya's choice**:

**Choices**:
- *"I forgot. Sorry, Frank."* → frank.trust +1
- *"I'll get it."* (she stands and goes) → frank.trust +3, a specific variant of *she took the correction without defending it*
- *"It was on a timer I didn't know about."* (deflects) → frank.trust -1

**Effects**: sets `frank_phase_a_test_1`. Ch 3 readiness +1.

---

#### Beat B15 — `marge_hands_key` (CH 2 CLOSE — milestone)

- **Canvas**: `marge_thursday_key`
- **Location**: `loc_diner_office`
- **NPC**: Marge
- **Schedule**: Thursday, Week 5, 22:00 (shift close)
- **Trigger**: `diner_regulars_named` and N Thursday shifts worked

**Nodes**:
1. **End of shift**: Maya at the till. Marge walks by with the key on the hook. Picks it up.
2. **The line**: *"You're steady. Thursdays are slow. Key's under the till."*
3. **Pause**: Maya takes the key. Marge goes back to the kitchen without another word.
4. **Maya walks home**: the key in her pocket. The hour of county road. The narrator is quieter than it used to be.

**Effects**: sets `first_ambient_tilt = true` (**milestone, closes Ch 2**). Opens T3 gate conditions. `diana_awareness` +5 silent (she sees Maya come in with the key Thursday nights).

---

**Chapter 2 = 6 beats: B10–B15.** No NPC-arc Touch/Crack. No Frank catch. No Jake peek. No Ryan big-ticket.

---

### CHAPTER 3+ — ESCALATION (10 beats)

Approximate ordering (one Crack per chapter rule honored). The design places Ryan's Beach (Ch 3–4), then midpoint_crack (between), then Frank's Crack (Ch 4), then Jake's Caught+Hand (Ch 5). `brothers_discover` fires late. Phase 1 closes on the Keep-Tier Fork dinner.

#### Beat B16 — `ryan_partner_first_close`

- **Canvas**: `ryan_partner_first_close`
- **Location**: `loc_shop_customer_area`
- **NPC**: Ryan + Pete (the older mechanic — his small-ticket baseline)
- **Schedule**: Tuesday, Week 6, afternoon
- **Trigger**: N Help scenes completed + corruption ≥ 25

**Nodes**:
1. **Pete walks in**: wants the riding mower. Ryan stands back.
2. **Maya closes**: twenty dollars above asking. Pete pays without comment. Ryan doesn't say anything till Pete's gone.
3. **Ryan's line**: *"Yeah. You got it. Big one's coming Saturday."*

**Effects**: sets `ryan_partner_open`. money +$35. rep_road +3.

---

#### Beat B17 — `jake_peek_draw_revealed`

- **Canvas**: `jake_peek_discovery`
- **Location**: `loc_hallway` → `loc_jakes_room` threshold
- **NPC**: Jake (off-screen for most of canvas)
- **Schedule**: late, Week 6
- **Trigger**: `jake_peek_draw_open = true` (fires automatically after Noticed) AND Maya's ambient solo-masturbation canvas was played in bedroom with Jake home

**Nodes**:
1. **Maya on the way to the bathroom at 1 a.m.**: Jake's door is cracked. A pencil line scratches.
2. **She looks, one second**: he's drawing. The page shows a woman. The woman is her.
3. **Maya steps back from the doorway**: doesn't make a sound. Walks to the bathroom. Doesn't look at herself in the mirror.

**Choices**:
- *Pretend she didn't see.* → Tease tier queues
- *Confront him now.* → early Caught fork (less typical; corruption ≥ 70 required)

**Effects**: sets `jake_peek_draw_revealed`. `jake_tease_open` if `corruption ≥ 50`. Sets `one_crack_this_chapter = true` only if early-Caught path chosen.
**Consequence echo**: Maya's next sketch in her own journal is of his hand.

---

#### Beat B18 — `ryan_big_ticket_deal`

- **Canvas**: `ryan_big_ticket_deal`
- **Location**: `loc_shop_customer_area` → back office (Ryan's small office in the shop)
- **NPCs**: Ryan + Big Customer
- **Schedule**: Saturday, Week 7, afternoon
- **Trigger**: `ryan_partner_open` + N mid-ticket closes + corruption ≥ 75 + customer-flag set (one of three archetypes — retired farmer / out-of-town scrapper / recently-divorced middle-ager)

**Nodes**:
1. **Customer arrives**: type is one of the three locked archetypes. First playthrough: the retired farmer (wants his wife's dead brother's tractor gone cheap — the most textured variant).
2. **Price dance**: negotiation. He digs in. Ryan disappears into the work bay on a pretext.
3. **The back office**: Maya and the customer. The close requires what it requires.
4. **After**: money in an envelope. Ryan in the work bay not looking up when Maya walks back through.

**Choices**:
- At the back-office threshold: *do it / walk away* (walk away → arc caps at Partner; `ryan_big_deal_walked` set; different Phase 1 close)

**Effects**: on close → `ryan_big_deal_closed = true`, money +$250 (retired farmer variant), corruption +8, rep_road -2 (word circulates in the wrong way). Sets `one_crack_this_chapter` true.
**Consequence echo**: the diner T3 gate now reads differently (Maya knows what T3 is an extension of, not a new register).

---

#### Beat B19 — `midpoint_crack` (MAYA'S midpoint — placed between Ryan Beach and Frank Crack)

*Design note: midpoint_crack sits AFTER Ryan Beach and BEFORE Frank Crack in the intended ordering. Placed here in the beat list before Beach only for clarity; sequencing handled by flag-chain.*

- **Canvas**: `maya_midpoint_crack`
- **Location**: `loc_diner_front` (T2 shift)
- **NPC**: (solo POV, ambient)
- **Schedule**: Thursday, Week 8, 19:30
- **Trigger**: `ryan_beach_proposal = true` and Maya has worked ≥ 3 T2 shifts since

**Nodes**:
1. **The floor**: Thursday shift. Maya walks past table four with two plates. She tilts at the hip. Three men at the table clock the tilt in a way that pays. She felt the tilt happen from the inside.
2. **Internal beat**: the narrator names it. *She did it on purpose. She felt nothing doing it.*
3. **End of shift**: she walks home with the tips. The feeling she expected doesn't come.

**Effects**: sets `midpoint_crack = true`. calculation +3. Unlocks Saturated-band prose variants across all subsequent activities.
**Consequence echo**: this beat is the hinge. Every subsequent scene reads with the knowledge that *she knows what she's doing* in her own voice now.

---

#### Beat B20 — `ryan_beach_proposal`

- **Canvas**: `ryan_beach`
- **Location**: `loc_beach` (new room, created for this scene; a freshwater lake an hour's drive east — "beach" in the local vernacular)
- **NPC**: Ryan
- **Schedule**: Sunday, Week 7, all day
- **Trigger**: `ryan_big_deal_closed`

**Nodes**:
1. **Truck ride out**: quiet. Ryan has one hand on the wheel, the other on the gearshift.
2. **The lake**: small sandy stretch. No one else there. They swim.
3. **The sand**: they cross the line they've been crossing in increments. Kiss + more, how far TBD by player track.
4. **The proposal**: Ryan says one complete sentence. The designer picks from three options in the content pass; provisional: *"Stay with me."*
5. **Maya's answer**:

**Choices (sets `ryan_keep_route`)**:
- *Yes.* → `ryan_keep_route = yes_engaged`
- *Not yet.* → `ryan_keep_route = not_yet`
- *No.* → `ryan_keep_route = no_withdrawn`

**Effects**: sets `ryan_beach_proposal`, `ryan_keep_route`. `one_crack_this_chapter = true` (this chapter's Crack spent on Ryan). `diana_awareness` +8 (Diana noticed Maya wasn't home Sunday).
**Consequence echo**: the yard scenes after this read differently per route.

---

#### Beat B21 — `frank_catch_trigger`

- **Canvas**: `frank_catch_living_room`
- **Location**: `loc_living_room`
- **NPCs**: Frank, Maya
- **Schedule**: Wednesday, Week 8 or 9, 23:30
- **Trigger**: `corruption >= 50` AND Maya's living-room-solo-masturbation canvas played AND Frank expected home within 15 minutes

**Nodes**:
1. **Living room**: Maya on the couch. The TV low. She knows he's coming home from porch-whiskey with a neighbor. She picked the room.
2. **Frank in the doorway**: one second. He doesn't speak. She doesn't speak.
3. **He walks to the kitchen**: pours a glass of water. Walks past the living room without looking again. Goes upstairs.
4. **Maya on the couch**: eyes open. The narrator is still.

**Effects**: sets `frank_caught = true`. No immediate stat changes — the weight is latent. The Restrict canvas queues for 1–2 days later.

---

#### Beat B22 — `frank_restrict_declared`

- **Canvas**: `frank_restrict`
- **Location**: `loc_kitchen` (morning)
- **NPC**: Frank
- **Schedule**: Friday, Week 8/9, 06:45
- **Trigger**: `frank_caught = true` + 1–2 days

**Nodes**:
1. **Breakfast**: Frank at the table. The paper down. *"Maya."* (the opener).
2. **The new rules**: (1) common areas locked after midnight. (2) extra chore rotation — one item per week, his to assign. (3) a line about "shared spaces" delivered without naming what she did.
3. **Maya's reply**: short.

**Choices**:
- *"Fine."* → compliance register
- *"Okay."* + eye contact held → tease-under-compliance register queues earlier
- *"Whatever you need, Frank."* → the Call-out-bait line; sets a sub-flag for *she lined it up*

**Effects**: sets `frank_restrict_declared = true`, `frank_tease_under_compliance_open = true` after Restrict beat closes (1 day). diana_awareness +3 (she watched the exchange).

---

#### Beat B23 — `frank_cracked`

- **Canvas**: `frank_crack`
- **Location**: `loc_franks_office` (most likely) OR `loc_kitchen` late night (alternate)
- **NPC**: Frank
- **Schedule**: Week 10, 22:45
- **Trigger**: N chore-supervision scenes + `frank.arousal >= X` + `midpoint_crack = true`

**Nodes**:
1. **Office**: bookkeeping session. Maya leans over the ledger. Frank is close enough.
2. **The beat**: he holds eye contact a count longer than he can afford. Hands press the desk instead of resting. One incomplete sentence. Silence.
3. **Maya notices it fully**: the Call-out is now available.

**Effects**: sets `frank_cracked = true`. `one_crack_this_chapter = true` (chapter's Crack spent on Frank — this chapter will not carry Jake Caught).

---

#### Beat B24 — `frank_called_out`

- **Canvas**: `frank_call_out`
- **Location**: `loc_franks_office`
- **NPC**: Frank
- **Schedule**: Week 10 or 11, evening
- **Trigger**: `frank_cracked`

**Nodes**:
1. **Bookkeeping**: another session. Frank quieter than before.
2. **Maya's line (the Call-out)**: *"This is normal. Everyone has needs. Even you."*
3. **Frank's response**: no words. He closes the ledger. Puts his hand flat on the desk. Looks at her. *"Maya."*
4. **The moment opens to Keep routes**.

**Choices (shapes `frank_keep_route` preview — final route lock at Keep-Tier Fork)**:
- *Touch his hand.* → primes Romantic
- *Name the number.* → primes Arrangement
- *Walk out.* → primes Rupture
- *"You work for me from now on."* → primes Power-Inverted

**Effects**: sets `frank_called_out = true`. `frank_keep_route` tentative tag set (confirmed at fork).

---

#### Beat B25 — `jake_caught_and_hand`

- **Canvas**: `jake_caught_and_hand`
- **Location**: `loc_jakes_room`
- **NPC**: Jake
- **Schedule**: Week 11, late
- **Trigger**: `jake_tease_open` + Maya walks in (her action)

**Nodes**:
1. **She knocks once and doesn't wait**: he's at the desk. Drawings of her in front of him, loose. He freezes.
2. **Silence**: whole scene.
3. **Maya picks a drawing up**: looks at it. Sets it back on the desk.
4. **She sits on his bed**: *"Show me your hand."*
5. **The hand beat**: her hand on his. She leads. He does not speak. Afterward she wipes her hand on his t-shirt. Takes the shirt with her.

**Choices (shapes `jake_keep_route`)**:
- *Take the shirt.* + routine return visits → `jake_keep_route = owned`
- *Lie down with him.* → `jake_keep_route = lovers`
- *Leave without taking anything.* → `jake_keep_route = withdrawn` (he avoids her after)
- *"Tell me what you know about the community college."* mid-scene → `jake_keep_route = she_uses_him`

**Effects**: sets `jake_caught`, `jake_hand`, `jake_keep_route` tentative. `brothers_discover_readiness` += (one step closer).

---

#### Beat B26 — `rent_shortfall_forced_event`

- **Canvas**: `rent_shortfall_first`
- **Location**: `loc_franks_office`
- **NPC**: Frank
- **Schedule**: A Sunday in Weeks 9–11 when money < $60 at 7 a.m.
- **Trigger**: `money < 60 AND day_of_week = sunday AND week >= 9`

**Nodes**:
1. **Sunday morning**: Maya knocks on the office door. Frank knows before she says it.
2. **The scene**: she says how much short she is. Frank lets the silence sit.
3. **Frank's options (player chooses Maya's stance)**:

**Choices (sets `rent_shortfall_1` resolution flavor)**:
- *I'll make it up Thursday.* → `rent_resolution = defer` (Frank: *"Thursday."*)
- *Can I work it off?* (if `frank_tease_under_compliance_open`) → `rent_resolution = chore_barter` (opens a heavier Frank-scene next chore window)
- *I'll take the extras-tier Thursday.* (if `first_ambient_tilt = true`) → `rent_resolution = diner_extras` (queues a T3 Thursday scene)
- *I can't yet.* → eviction mode flag_set triggers (per F4): Frank gives her until end of week; no physical eviction in Phase 1

**Effects**: sets `rent_shortfall_1` + resolution flavor. Maya's next week reshapes around the resolution.
**Consequence echo**: each resolution branches the Week-N dinner-table atmosphere.

---

#### Beat B27 — `brothers_discover` (milestone, late Phase 1)

- **Canvas**: `brothers_discover`
- **Location**: `loc_kitchen` (Saturday outdoor dinner) OR `loc_back_porch`
- **NPCs**: Frank + Ryan + Jake + Diana
- **Schedule**: Week 12, Saturday dinner
- **Trigger**: ≥2 NPC arcs past Crack-equivalent OR 1 arc at Keep + specific ambient tells accumulated

**Nodes**:
1. **Saturday dinner on the back porch**: Diana at the head. Frank at the foot. Ryan and Jake on one side. Maya on the other.
2. **The beat varies by which arcs fired**:
   - **Two or three arcs live**: reckoning tone. Ryan's hand goes still on his fork. Jake's sketchbook isn't out. Frank says *"Pass the salt"* in a voice that isn't about salt. Diana serves, silent.
   - **One arc only**: softer. The brothers register what they hadn't named to themselves. Jake looks at Maya differently for the first time if Frank is her arc; Frank's jaw tightens if Ryan is hers; Ryan laughs too hard at something Jake said if Jake is hers.
   - **No arc committed** (edge case): Diana's silence becomes the whole scene. She stands up to clear the plates and doesn't ask anyone to help.

**Choices**: Maya's response per sub-variant. Each response nudges `keep_tier_fork` configuration.

**Effects**: sets `brothers_discover = true`. `diana_awareness` +10.
**Consequence echo**: Phase 1 close is now queued.

---

#### Beat B28 — `phase_1_close_keep_tier_fork` (PHASE 1 CLOSE — milestone)

- **Canvas**: `keep_tier_fork`
- **Location**: `loc_kitchen` (family dinner, Diana-attended)
- **NPCs**: All: Frank, Ryan, Jake, Diana
- **Schedule**: Week 14 or end-of-summer Sunday dinner
- **Trigger**: `brothers_discover = true` + any NPC Keep-route tentatively set

**Nodes**:
1. **The table**: Diana has made something Maya remembers from childhood — the exact dish Maya's biological father used to request. The table is set with the good plates.
2. **Diana's one line (pre-dinner)**: *"Maya, honey. Set a place for yourself next to me."* Not at her usual spot.
3. **Dinner plays out**: brief, quiet, the food good. Maya eats next to Diana.
4. **After the table**: Diana gets up for coffee. Turns in the kitchen doorway. Looks at Maya. Doesn't say anything. Goes to get the coffee.
5. **Maya signals intent** (the fork):

**Choices (locks Phase 1 end-state + `keep_tier_fork_fired = true`)**:
- *Stand and follow Diana into the kitchen.* → **Independence** path. Diana's Phase 2 arc opens immediately post-close. NPC Keep routes cap at their current tier without locking.
- *Stay at the table and meet Frank's eye across it.* → **Frank Keep** locked to the `frank_keep_route` primed value.
- *Go out to the yard where Ryan is.* → **Ryan Keep** locked.
- *Walk down the hall to Jake's room.* → **Jake Keep** locked.
- *Go up to her own room.* → **Deferred** — Phase 2 opens with no Keep locked; all arcs hang at post-Call-out/Caught tier without resolution.

**Effects**: sets `keep_tier_fork_fired = true`, locks `phase_1_final_route`. Phase 1 ends.
**Consequence echo**: Phase 2 opens on a specific morning depending on the fork — the prose register of Day 1 Phase 2 is locked by this beat.

---

**Phase 1 beat count: 28 total (Arrival + Ch1 × 9 + Ch2 × 6 + Ch3+ × 12).** Combined with the Prologue's 20 beats = **48 beats**. Slightly over the 40–45 target; the overage is on the Ch3+ escalation block, which benefits from one beat per arc-milestone.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## VALIDATION

- **≥3 events where stats drop (danger real)**: ✅ rent shortfall (B26, money), diner hygiene decay (B7), big-deal rep_road cost (B18), Frank restrict cost (B22 chore-time).
- **Crisis takes 2–4 in-game days to resolve**: ✅ rent shortfall (Sunday → Thursday), Frank Crack → Call-out (several days), brothers_discover → Phase 1 close (multiple days per sub-variant).
- **Minimum narrative distance between gates**: ✅ first_rent_paid (Wk 2) → first_ambient_tilt (Wk 5) → first Crack (Wk 7 Ryan) → midpoint_crack (Wk 8) → Frank Crack (Wk 10) → Jake Caught+Hand (Wk 11) → brothers_discover (Wk 12) → Phase 1 close (Wk 14).
- **Every Keep branch has ≥1 bridge event**: ✅ each arc has bridging beats between Crack and Keep (Frank Call-out, Ryan Beach, Jake Hand); Phase 1 close locks the route.
- **All flag dependencies form complete graph (no orphans / no circular)**: audited in Phase 2 flag inventory. ✅
- **At most one Crack per chapter**: ✅ Ryan Beach (Ch3), Frank Cracked (Ch4), Jake Caught+Hand (Ch5), separated by `one_crack_this_chapter`.
- **Frank catch-trigger correctly placed**: Ch3+ only; gated on `corruption ≥ 50` AND player-chosen living-room canvas; Maya picks the room. ✅
- **Diana does not confront in Phase 1**: ✅ `diana_awareness` accumulates silently; Diana's only "spoken" moment at close is to set a place at the table without explanation.
- **Placeholders resolved in-phase**: ✅
  - Midpoint crack: locked in B19 (T2 diner tilt, feels nothing).
  - Phase 1 closing event: locked in B28 (Keep-Tier Fork).
  - Ryan's three customer archetypes: locked (retired farmer / out-of-town scrapper / recently-divorced middle-ager).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End of Phase 4 — Story Events. Proceed to Phase 5: Activities.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
