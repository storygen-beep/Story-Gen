# EXTRACTION: Flags, Gates & Chain Diagrams
# Source: Phase 2 (Section 5) + Phase 4 (Flag Chains & Gate Timeline)

## GATE FLAGS (16 total — 4 per NPC)

Format: `{npc}_{tier}_unlocked` — one-way flags, set to `true` only.

### Tom Gates
```
tom_kiss_unlocked
tom_groping_unlocked
tom_oral_unlocked
tom_sex_unlocked
```

### Ray Gates
```
ray_groping_unlocked    # NOTE: Ray's groping fires BEFORE kiss (physical precedes emotional)
ray_kiss_unlocked
ray_oral_unlocked
ray_sex_unlocked
```

### Mark Gates
```
mark_kiss_unlocked
mark_groping_unlocked
mark_oral_unlocked
mark_sex_unlocked
```

### Jake Gates
```
jake_kiss_unlocked
jake_groping_unlocked
jake_oral_unlocked
jake_sex_unlocked
```

---

## GATE REQUIREMENTS TABLE

| NPC | Gate | Set By Event (Canvas ID) | Event Name | Stat Requirements | ~Day |
|-----|------|--------------------------|------------|-------------------|------|
| Tom | kiss_unlocked | `tom_classroom_catch` | The Classroom Catch | `devotion >= 20, confidence >= 10` | ~18-20 |
| Tom | groping_unlocked | `tom_movie_night` | Movie Night | `devotion >= 35, corruption >= 20` | ~23-25 |
| Tom | oral_unlocked | `tom_good_boy` | Good Boy | `devotion >= 55, corruption >= 30` | ~26-28 |
| Tom | sex_unlocked | `tom_first_time` | First Time | `devotion >= 70, corruption >= 35` | ~29-31 |
| Ray | groping_unlocked | `ray_shed_scene` | The Shed | `interest >= 30, confidence >= 30` | ~30-32 |
| Ray | kiss_unlocked | `ray_staircase_kiss` | The Staircase | `interest >= 40, confidence >= 35` | ~32-34 |
| Ray | oral_unlocked | `ray_truck_oral` | The Truck | `interest >= 55, corruption >= 45` | ~36-38 |
| Ray | sex_unlocked | `ray_upstairs` | Upstairs | `interest >= 70, corruption >= 50` | ~38-42 |
| Mark | kiss_unlocked | `mark_rain_umbrella` | The Rain | `desire >= 25, confidence >= 25, corruption >= 40` | ~38-40 |
| Mark | groping_unlocked | `mark_under_desk` | Under the Desk | `desire >= 40, guilt < 35` | ~42-44 |
| Mark | oral_unlocked | `mark_first_visit` | The First Visit | `desire >= 55, corruption >= 50, guilt < 40` | ~47-49 |
| Mark | sex_unlocked | `mark_no_hesitation` | No Hesitation | `desire >= 70, corruption >= 55` | ~50-52 |
| Jake | kiss_unlocked | `jake_not_yet` | Not Yet | `power <= 65, confidence >= 55` | ~52-54 |
| Jake | groping_unlocked | `jake_permission` | Permission | `power <= 50, corruption >= 60` | ~54-56 |
| Jake | oral_unlocked | `jake_stockroom` | The Stockroom | `power <= 35, corruption >= 70` | ~58-60 |
| Jake | sex_unlocked | `jake_on_her_terms` | On Her Terms | `power <= 20, corruption >= 75` | ~60-63 |

---

## PHASE 1 FLAGS — Jolene Corruption (9 flags)

| Flag | Description | Set By Event | ~Day |
|------|-------------|-------------|------|
| `jolene_arrival_complete` | Day 1-2: Settled in, met Jolene | `opening_arrival` | 1 |
| `jolene_thin_walls` | Day 3: Heard Jolene through the wall | `jolene_thin_walls` | 3 |
| `jolene_wine_dinner` | Day 4-5: First wine, first frank sex talk | `jolene_wine_dinner` | 4-5 |
| `jolene_peek_event` | Day 6: Caught Jolene mid-act through cracked door | `jolene_peek_event` | 6 |
| `jolene_exposure_therapy` | Day 7-8: Vibrator in bathroom, laptop "accident" | `jolene_exposure_therapy` | 7-8 |
| `jolene_shopping_trip` | Day 9: City shopping, the dress, confidence unlock | `jolene_shopping_trip` | 9 |
| `jolene_self_discovery` | Day 10: "Figure it out" milestone (player choice — did it) | `jolene_self_discovery` | 10 |
| `jolene_self_discovery_refused` | Day 10: Player refused (alternate path, slower corruption) | `jolene_self_discovery` | 10 |
| `phase_1_complete` | Day 11-12: Phase 2 unlocks, she notices men | `jolene_phase_1_complete` | 11-12 |

---

## TOM STORY PROGRESSION FLAGS (8 flags)

| Flag | Description | Set By Event |
|------|-------------|-------------|
| `tom_locks_checked` | She asks him to check her locks (first excuse) | `tom_locks_checked` |
| `tom_classroom_setup` | She invites him to help with classroom | `tom_classroom_setup` |
| `tom_classroom_catch` | Gate event: the "trip," the catch, the kiss | `tom_classroom_catch` |
| `tom_movie_night` | Gate event: his hands on her body | `tom_movie_night` |
| `tom_good_boy` | Gate event: she teaches him oral | `tom_good_boy` |
| `tom_first_time` | Gate event: she takes his virginity | `tom_first_time` |
| `tom_asset_activated` | Late game: he starts covering for her | `tom_first_time` (optional choice) |
| `tom_devotion_confession` | "I've never felt like this about anyone" (triggers when devotion >= 80) | `tom_devotion_confession` |

---

## RAY STORY PROGRESSION FLAGS (10 flags)

| Flag | Description | Set By Event |
|------|-------------|-------------|
| `ray_invisible_wall` | Unlocks new approach events | `ray_invisible_wall` |
| `ray_first_sentence` | "Didn't take you for a whiskey girl" | `ray_first_crack` |
| `ray_plumbing_excuse` | She gets him to her room to "fix something" | `ray_first_crack` |
| `ray_first_crack` | He looks. She sees him look. He looks away. | `ray_first_crack` |
| `ray_truck_conversation` | Tailgate beers, real conversation, forearm touch | `ray_truck_conversation` |
| `ray_shed_scene` | Gate event: pressed against him in the shed | `ray_shed_scene` |
| `ray_staircase_kiss` | Gate event: he breaks first, kisses her on the stairs | `ray_staircase_kiss` |
| `ray_truck_oral` | Gate event: she drops to her knees in his truck | `ray_truck_oral` |
| `ray_upstairs` | Gate event: raw, urgent sex | `ray_upstairs` |
| `ray_daughter_story` | He opens up about his daughter (emotional complication) | `ray_daughter_story` |
| `ray_feelings_emerge` | Narrative flag: interest > 80, real feelings developing | `ray_feelings_emerge` |

---

## MARK STORY PROGRESSION FLAGS (12 flags)

| Flag | Description | Set By Event |
|------|-------------|-------------|
| `mark_first_conference` | First parent-teacher meeting — she notices his hunger | `mark_first_conference` |
| `mark_fundraiser_volunteer` | He starts inventing reasons to see her | `mark_fundraiser_volunteer` |
| `mark_rain_umbrella` | Gate event: the rain, the almost-kiss, first texts | `mark_rain_umbrella` |
| `mark_texting_escalation` | Texts go from warm to charged to explicit | `mark_rain_umbrella` |
| `mark_under_desk` | Gate event: his hand on her thigh in the classroom | `mark_under_desk` |
| `mark_first_visit` | Gate event: he comes to her door at night | `mark_first_visit` |
| `mark_no_hesitation` | Gate event: he comes back, no guilt preamble | `mark_no_hesitation` |
| `mark_call_from_bedroom` | She makes him call her while Karen is downstairs | `mark_call_from_bedroom` |
| `mark_parking_lot` | She pushes the taboo — his car after hours | `mark_crisis_repair` |
| `karen_finds_text` | Crisis: Karen discovers a suspicious text | `karen_crisis` |
| `karen_school_confrontation` | Crisis: Karen confronts Emma at school | `karen_crisis` |
| `mark_guilt_spiral` | Trigger if guilt (Mark) > 40 | auto (stat threshold) |
| `mark_crisis_repair_complete` | Crisis repair scene completed | `mark_crisis_repair` |

---

## JAKE STORY PROGRESSION FLAGS (11 flags)

| Flag | Description | Set By Event |
|------|-------------|-------------|
| `jake_initial_rejection` | "Old Emma" shot him down (pre-Phase 2) | backstory |
| `jake_second_attempt` | He tries again, she laughs at him | `jake_second_attempt` |
| `jake_jealousy_game` | She flirts with other men while he watches | `jake_jealousy_game` |
| `jake_bar_sitting` | She sits on the bar, "Pour me one more" | `jake_bar_sitting` |
| `jake_not_yet` | Gate event: finger on his lips, "Not yet" | `jake_not_yet` |
| `jake_permission` | Gate event: she controls where his hands go | `jake_permission` |
| `jake_stockroom` | Gate event: on his knees in the stockroom | `jake_stockroom` |
| `jake_on_her_terms` | Gate event: she's on top, hands pinned | `jake_on_her_terms` |
| `jake_ego_crisis` | "What the fuck do you want from me?" | `jake_ego_crisis` |
| `jake_surrender` | He asks: "What do you want me to do?" (choice: Stay) | `jake_endgame_choice` |
| `jake_endgame_choice` | Endgame choice completed | `jake_endgame_choice` |
| `jake_endgame_walked_away` | She breaks it off (choice: "I don't need you") | `jake_endgame_choice` |

---

## MIRROR MECHANIC FLAGS (4 flags)

| Flag | Trigger | Description |
|------|---------|-------------|
| `mirror_day_1` | Opening arrival | Cardigan girl, nervous smile, prayer |
| `mirror_day_20` | Day >= 20, Morning | The dress, sharper eyes, no prayer |
| `mirror_day_40` | Day >= 40, Morning | Underwear, no flinch, power thrum, no guilt |
| `mirror_day_60` | Day >= 60, Morning | Unrecognizable, the smile that isn't kind |

---

## UTILITY & SURVIVAL FLAGS (9 flags)

| Flag | Description | Set By |
|------|-------------|--------|
| `game_started` | Initial game flag | `opening_arrival` |
| `school_started` | First day of teaching | `jolene_culture_shock` |
| `chores_explained` | Jolene explains rent/groceries expectations | `jolene_culture_shock` |
| `bar_shifts_available` | Jolene offers bar work (Day 8+) | `jolene_phase_1_complete` |
| `cafe_job_available` | Diner offers weekend shifts | `jolene_phase_1_complete` |
| `food_stocked` | True when groceries current (5-day duration) | `chore_groceries` activity |
| `church_attended_this_week` | Weekly reset flag | `activity_church` |
| `missed_school_today` | Set when player skips school on a weekday morning | `utility_school_morning` (skip choice) |
| `rent_last_paid` | Timer: days_since_flag for weekly rent ($180) | `expense_rent` activity |
| `groceries_last_bought` | Timer: days_since_flag for food stocking ($25/5 days) | `chore_groceries` activity |
| `salary_last_paid` | Timer: days_since_flag for weekly salary ($220 Friday) | `utility_payday` |

---

## ECONOMIC ESCALATION FLAGS (3 flags)

| Flag | Description | Set When |
|------|-------------|----------|
| `rent_missed_once` | First rent miss — Jolene warns, mild consequence | Ask for time (first) |
| `rent_missed_twice` | Second miss — Jolene demands bar shifts | Ask for time (second) |
| `forced_bar_shifts` | Player must work bar until rent debt cleared | Ask for time (third) |

---

## SCHOOL ENFORCEMENT FLAGS (4 flags)

| Flag | Description | Set When |
|------|-------------|----------|
| `school_enforcement_warned` | Principal has warned about attendance (increases skip penalty from -5 to -8) | `principal_concern_2` |
| `principal_concern_triggered_60` | Reputation < 60: "Just checking in..." conversation fired | `principal_concern_1` |
| `principal_concern_triggered_45` | Reputation < 45: Active monitoring conversation fired | `principal_concern_2` |
| `principal_warning_triggered_30` | Reputation < 30: Formal school board warning fired | `principal_formal_warning` |

---

## REPUTATION & CRISIS FLAGS (10 flags)

| Flag | Description | Set When |
|------|-------------|----------|
| `principal_concern_1` | "Just checking in..." (reputation < 60) | auto (stat threshold) |
| `principal_concern_2` | Active monitoring (reputation < 45) | auto (stat threshold) |
| `principal_formal_warning` | School board meeting (reputation < 30) | auto (stat threshold) |
| `church_gossip_mild` | Ladies mention bar visits | contextual |
| `church_gossip_moderate` | Active whispering about "the teacher" | contextual |
| `karen_suspicious` | Karen is watching (pre-confrontation) | contextual |
| `karen_confrontation_complete` | Karen confronted Emma at school | `karen_crisis` |
| `karen_backed_down` | Karen accepted Emma's explanation | `mark_crisis_repair` (choice 1) |
| `karen_still_watching` | Karen didn't buy it — ongoing threat | `mark_crisis_repair` (choice 2) |
| `reputation_recovery_mode` | Flag to boost rep gains when in danger zone (reputation < 45) | auto (stat threshold) |

---

## CROSS-NPC COMPLICATION FLAGS (5 flags)

| Flag | Description | Trigger |
|------|-------------|---------|
| `tom_saw_ray` | Tom notices Emma with Ray at the bar | `tom_kiss_unlocked` AND `ray_kiss_unlocked`, Day >= 35 |
| `tom_covers_for_emma` | Tom agrees to look the other way (requires devotion >= 60) | `tom_saw_ray` (choice: "It's complicated" + devotion >= 60) |
| `ray_sees_mark_text` | Ray glimpses a text from Mark on her phone | `ray_kiss_unlocked` AND `mark_kiss_unlocked`, Day >= 45 |
| `friday_collision` | All NPCs at the bar on the same night | Day is Friday, 19:00-22:00, `tom_kiss_unlocked` AND `interest >= 20` |
| `juggling_detected` | Any NPC suspects she's seeing others | (`tom_saw_ray` AND `ray_sees_mark_text`) OR `friday_collision`, Day >= 45 |

---

## FLAG CHAIN DIAGRAMS

### Phase 1 (Jolene Corruption)

```
game_started → jolene_arrival_complete → mirror_day_1
  → jolene_thin_walls
    → jolene_wine_dinner
      → jolene_peek_event
        → jolene_exposure_therapy
          → jolene_shopping_trip
            → jolene_self_discovery (OR jolene_self_discovery_refused)
              → phase_1_complete
                → bar_shifts_available
                → cafe_job_available
```

### Tom Arc

```
phase_1_complete → tom_locks_checked
  → tom_classroom_setup
    → tom_classroom_catch → tom_kiss_unlocked (GATE 1)
      → [BRIDGE] tom_devotion_confession
        → tom_movie_night → tom_groping_unlocked (GATE 2)
          → tom_good_boy → tom_oral_unlocked (GATE 3)
            → tom_first_time → tom_sex_unlocked (GATE 4)
              → tom_asset_activated (optional)
```

### Ray Arc

```
phase_1_complete → ray_invisible_wall
  → ray_first_crack (ray_first_sentence + ray_plumbing_excuse)
    → ray_truck_conversation
      → ray_shed_scene → ray_groping_unlocked (GATE 1 — physical first)
        → ray_staircase_kiss → ray_kiss_unlocked (GATE 2)
          → [BRIDGE] ray_daughter_story
            → ray_truck_oral → ray_oral_unlocked (GATE 3)
              → [TENSION] ray_feelings_emerge
                → ray_upstairs → ray_sex_unlocked (GATE 4)
```

### Mark Arc

```
phase_1_complete (+ corruption >= 40) → mark_first_conference
  → mark_fundraiser_volunteer
    → mark_rain_umbrella → mark_kiss_unlocked (GATE 1) + mark_texting_escalation
      → mark_under_desk → mark_groping_unlocked (GATE 2)
        → [BRIDGE] mark_call_from_bedroom
          → mark_first_visit → mark_oral_unlocked (GATE 3)
            → mark_no_hesitation → mark_sex_unlocked (GATE 4)
              → [CRISIS] karen_finds_text → karen_school_confrontation
                → mark_crisis_repair_complete
                  → (karen_backed_down OR karen_still_watching)
```

### Jake Arc

```
phase_1_complete (+ corruption >= 55) → jake_second_attempt
  → jake_jealousy_game
    → jake_bar_sitting
      → [BRIDGE] jake_ego_crisis
        → jake_not_yet → jake_kiss_unlocked (GATE 1)
          → jake_permission → jake_groping_unlocked (GATE 2)
            → jake_stockroom → jake_oral_unlocked (GATE 3)
              → jake_on_her_terms → jake_sex_unlocked (GATE 4)
                → jake_endgame_choice (jake_surrender OR jake_endgame_walked_away)
```

### Cross-NPC Chain

```
tom_kiss_unlocked + interest >= 20 → friday_collision
tom_kiss_unlocked + ray_kiss_unlocked → tom_saw_ray → (tom_covers_for_emma?)
ray_kiss_unlocked + mark_kiss_unlocked → ray_sees_mark_text
(tom_saw_ray + ray_sees_mark_text) OR friday_collision → juggling_detected
```

---

## TOTAL FLAG COUNT

| Category | Count |
|----------|-------|
| Gate flags | 16 |
| Phase 1 (Jolene) | 9 |
| Tom progression | 8 |
| Ray progression | 11 |
| Mark progression | 13 |
| Jake progression | 12 |
| Mirror mechanic | 4 |
| Utility & survival | 11 |
| Economic escalation | 3 |
| School enforcement | 4 |
| Reputation & crisis | 10 |
| Cross-NPC | 5 |
| **TOTAL** | **~106** |
