# PHASE 5: ACTIVITIES
# The Long Summer

*Per-activity spec. Every activity has canvas metadata + Base Scene Variants (DEFAULT / WITHDRAWN / WARM) + choice progression + consequence variants (per Rule 16) + block pools on repeatables (per Rule 17).*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION A: SOLO ACTIVITIES

### A1 — Sleep (`activity_sleep`)

- **Location**: `loc_mayas_bedroom`
- **Schedule**: `overnight` (or `late` if Maya slept through)
- **Energy cost**: advances day; restores to 100
- **is_repeatable**: true (daily)

**Base scene variants (repeatable block pool)**:
- DEFAULT: *The fan pushing air. Jake's keyboard through the wall. Maya's last thought before sleep is about tomorrow's shift.*
- WITHDRAWN (low energy, high hygiene decay): *She's asleep before the fan finishes its first rotation.*
- WARM (post-arc tier, positive-valence route): *She's still in Jake's shirt / the truck keys on her desk / Frank's light still under the door.*

**Variants per route (post-Keep)**:
- Frank-Romantic: *The porch light is off. He turned it out when she came home.*
- Ryan-Yes: *The truck is in the driveway. He's sleeping in her room now most nights.*
- Jake-Owned: *His shirt in her drawer. She sleeps on top of it.*

---

### A2 — Shower (`activity_shower`)

- **Location**: `loc_bathroom`
- **Schedule**: any (except Frank's 6:15am window)
- **Energy cost**: -5 / **Hygiene**: +40
- **is_repeatable**: true

**Block pool (4 variants)**:
- Regular hygiene restore.
- Ambient bathroom-share encounter (Jake peeks variant if `jake_peek_draw_open`; adds to peek-scene inventory).
- Steam-through-the-thin-window variant (Ryan in the yard glimpsing the window is an ambient ryan.arousal modifier_effect).
- Late-night shower variant: after a T2 or T3 shift; Maya rinses longer.

**Consequence variant (post-Frank-Restrict)**: Frank has tightened the bathroom-use window. She showers on his schedule now. Prose reads the constraint.

---

### A3 — Sketch in room (`activity_sketch_bedroom`)

- **Location**: `loc_mayas_bedroom`
- **Schedule**: any
- **Energy**: -10 / **corruption**: 0 (art is private-honest)
- **is_repeatable**: true

**Choice progression**:
- *Sketch something from memory.* — Maya sketches a hand. Whose hand varies per highest `.arousal` NPC in her last 48 hours.
- *Sketch something from the window.* — yard, Ryan, nothing, depending on time.
- *Work on something she won't finish.* — long scene, high calm.

**Consequence echo**: the hand-sketch block pool rotates per arc state:
  - No arc active: a generic hand from life-drawing reference.
  - Jake Noticed+: Jake's hand (she won't tell him).
  - Ryan Partner+: Ryan's hand on the gearshift.
  - Frank Restrict+: Frank's hand flat on the table.

---

### A4 — Sketch at creek (`activity_sketch_creek`)

- **Location**: `loc_creek`
- **Schedule**: `mid_morning`, `afternoon` (daylight)
- **Energy**: -15 / fitness: +1
- **is_repeatable**: true (max 2/week without `fitness` bump)

**Base scene (DEFAULT)**: *Water over stones. Dragonflies. Maya's page fills with nothing she'll keep but something that keeps her.*

**WARM variant (post-midpoint_crack)**: *She sketches a self-portrait and doesn't throw the page out.*

---

### A6 — Walk to town (`activity_walk_to_town`)

- **Location**: `loc_driveway` → `loc_main_street`
- **Schedule**: `morning`, `mid_morning`, `afternoon`
- **Energy**: -15 / hygiene -5 / **possible ambient encounter fires**
- **is_repeatable**: yes

**Ambient encounter roll**: 40% chance one of the 8 ambient encounters (Phase 3 §5) fires per walk.

---

### A7 — Read (`activity_read`)

- **Location**: any room
- **Schedule**: any
- **Energy**: -5

Low-cost downtime. Block pool rotates based on what book — paperback from Diana's shelf / the college brochure re-read / nothing she chose.

---

### A8 — Cook for herself (`activity_cook_solo`)

- **Location**: `loc_kitchen`
- **Schedule**: any Diana-absent window (lunch, late)
- **Energy**: -10 / money -$3 / hygiene -5
- **is_repeatable**: yes

**Consequence variant (post-Restrict)**: Frank walks through the kitchen. Variant fires if Frank home + `frank_tease_under_compliance_open`.

---

### A9 — Eat from fridge (`activity_eat_fridge`)

- **Location**: `loc_kitchen`
- **Schedule**: any
- **Energy**: +5 / money -$1
- **is_repeatable**: yes

Fast. No scene weight.

---

### A10 — Mirror look (`activity_mirror_look`)

- **Location**: `loc_bathroom`
- **Schedule**: any
- **Energy**: 0
- **is_repeatable**: true

**Corruption-band variants (the main axis)**:
- Closed: *She can't hold her own eye for five seconds.*
- Opening: *She holds it. Catalogs what she sees.*
- Operating: *She tilts her chin. Tests the angle. She knows what it does.*
- Saturated: *She doesn't need the mirror to know.*

---

### A11 — Look at brochure / journal (`activity_brochure_journal`)

- **Location**: `loc_mayas_bedroom`
- **Schedule**: any
- **Energy**: -5

**Choice progression**:
- *Re-read the brochure.* — updates money target in Maya's head.
- *Journal.* — private sincerity; no corruption effect; mood +1.

---

### A12 — Solo masturbation (`activity_solo_mast`)

- **Location**: `loc_mayas_bedroom` (default) OR `loc_living_room` (the gate variant)
- **Schedule**: `late`, `overnight`
- **Energy**: -5
- **is_repeatable**: yes

**Bedroom variant (default)**: *Under the sheet. Quiet. Jake's wall on one side.*

**Living-room variant (gate-triggering)**:
- Gate: `corruption >= 45` and Frank expected home within 20 minutes
- Scene: Maya on the couch. The TV low. She chose the room.
- **If Frank arrives during the scene → triggers B21 `frank_catch_living_room`.** This is the Frank arc's Phase-B opening.

---

## SECTION B: FRANK ACTIVITIES

### F1 — Breakfast with Frank (`activity_breakfast_frank`)

- **Location**: `loc_kitchen`
- **Schedule**: Mon–Fri 06:30–07:30
- **NPC**: Frank (+ ambient Diana)
- **Energy**: -5 / food auto-handled
- **is_repeatable**: yes

**Base variants**:
- DEFAULT: *Paper, coffee, small exchanges about the day. Frank nods at her when she sits.*
- WITHDRAWN (post-Restrict no tease tier): *Frank doesn't look up. Diana talks for both of them.*
- WARM (frank.trust ≥ 60, pre-Crack): *He saves the good cushion chair for her. Refills her coffee without asking.*

**Consequence variant (post-Crack)**: *The breakfast doesn't work anymore. Nobody names it. Diana fills the silence.*

---

### F2 — Cook dinner with Frank (`activity_cook_dinner_frank`)

- **Location**: `loc_kitchen`
- **Schedule**: Mon–Fri 17:30–18:30
- **NPC**: Frank
- **Energy**: -10
- **is_repeatable**: yes

**Base variants**:
- DEFAULT: *Cutting onions side by side. He hands her the knife handle-first.*
- WARM: *He shows her the right way to break down the chicken. His hand overlaps hers for one beat when he takes the cleaver back.*
- CONSEQUENCE (post-Restrict, tease-under-compliance): *She cuts slowly. He watches her wrists. Nobody narrates the watching.*

---

### F3 — Help with bookkeeping (`activity_bookkeeping`)

- **Location**: `loc_franks_office`
- **Schedule**: Mon–Fri 20:00–21:00 (when Frank offers)
- **NPC**: Frank
- **Energy**: -15 / money +$20 per session
- **is_repeatable**: yes (max 3/week)

**Base variants**:
- DEFAULT: *Ledger, pencil, small columns. He catches a mistake he didn't make to let her correct it.*
- WARM: *He leans over to point at a column. His shoulder on hers.*
- CONSEQUENCE (post-Cracked): *Neither of them pretends it's about the ledger.*

**Choice progression (post-tease tier)**:
- *Stay focused on the work.* — paid, steady, low charge.
- *Lean in when he reaches past you.* — frank.arousal modifier +15 (duration 2h).
- *Let your hand rest under his on the page.* — advances toward Cracked threshold.

---

### F4 — Porch evening with Frank (`activity_porch_frank`)

- **Location**: `loc_front_porch`
- **Schedule**: 21:00–22:30
- **NPC**: Frank (+ whiskey)
- **Energy**: -5
- **is_repeatable**: yes

**Base variants (block pool, 4)**:
- Whiskey and silence.
- Whiskey and a question he asks about her day without looking at her.
- Whiskey and Diana on the phone in the kitchen behind them.
- Whiskey and the porch light going off early.

---

### F5 — Saturday hardware run (`activity_hardware_run`)

- **Location**: `loc_main_street` (general store + gas station)
- **Schedule**: Saturday morning
- **NPC**: Frank (truck)
- **Energy**: -20 / money passive ($5 gas split)
- **is_repeatable**: yes (weekly)

Truck cab scene. Two-person confined. Conversation evolves per `frank.trust` band.

---

### F6 — Weekend repairs with Frank (`activity_weekend_repairs`)

- **Location**: `loc_property` (yard, house, ambient)
- **Schedule**: Saturday / Sunday afternoon
- **Energy**: -25 / fitness +1
- **is_repeatable**: yes

Shared labor. Post-Restrict variant introduces specific chore assignments (the Phase B texture).

---

### F7 — Post-Restrict chore supervision (`activity_chore_supervision`)

- **Location**: varies per assigned chore
- **Schedule**: when Frank assigns
- **NPC**: Frank (watching)
- **Energy**: -20 / frank.arousal modifier accumulates
- **is_repeatable**: yes (task-based)

**The chore-supervision scene** is the Phase B recurring activity. Tease-under-compliance lives here.

**Choice progression per scene**:
- *Do it clean.* — pay/progress, low charge.
- *Do it with him watching the way he's watching.* — heavy charge, advances Cracked conditions.
- *Mess up on purpose to keep him there longer.* — calculation +1, arousal build.

---

## SECTION C: RYAN ACTIVITIES

### R1 — Help Ryan in yard (`activity_yard_help`)

- **Location**: `loc_yard`
- **Schedule**: Mon–Fri 08:00–15:00 windows
- **NPC**: Ryan
- **Energy**: -20 / fitness +1 per session
- **is_repeatable**: yes

**Base variants**:
- DEFAULT: *Hand him the ratchet. Wait. Hand him the crescent. The yard at 2pm is louder than the house.*
- WARM: *He hands something back. Their hands in the same space.*
- CONSEQUENCE (post-big-deal, pre-Beach): *He barely talks. Works harder than he needs to.*

---

### R2 — Help Ryan with truck (`activity_truck_help`)

- **Location**: `loc_driveway`
- **Schedule**: Saturday afternoon
- **NPC**: Ryan
- **Energy**: -25 / money +$30 (paid)
- **is_repeatable**: weekly

---

### R3 — Watch Ryan working (`activity_watch_ryan`)

- **Location**: `loc_yard`
- **Schedule**: daytime
- **Energy**: -5
- **is_repeatable**: yes

Ambient. No direct stats. Passive ryan.arousal bump if Maya sits in sightline for a full scene.

---

### R4 — Bring water to Ryan (`activity_bring_water`)

- **Location**: `loc_yard`
- **Schedule**: hot afternoons
- **Energy**: -5 / ryan.trust +1
- **is_repeatable**: yes (max 1/day)

---

### R5 — Ride shotgun on pickup (`activity_ride_shotgun`)

- **Location**: truck → auction / pickup destination
- **Schedule**: Saturdays / some weekdays
- **NPC**: Ryan
- **Energy**: -30 / money +$10 small pay
- **is_repeatable**: yes (weekly)

Introduces outside-the-property locations ambient. Long drives; quiet Ryan.

---

### R6 — Work the shop / small-ticket close (`activity_shop_small`)

- **Location**: `loc_shop_customer_area`
- **Schedule**: weekday afternoons
- **NPC**: Ryan + walk-in customer
- **Energy**: -15 / money +$10–25
- **is_repeatable**: yes

**Base variants per customer type** (block pool, 3):
- Pete the mechanic — easy.
- Random walk-in — transactional.
- The repeat buyer who mentions Ryan's uncle — texture.

---

### R7 — Close a walk-in / mid-ticket (`activity_shop_mid`)

- **Location**: `loc_shop_customer_area`
- **Schedule**: weekday afternoons post-Partner
- **NPC**: Ryan + customer
- **Energy**: -20 / money +$25–60
- **is_repeatable**: yes

Maya runs the close. Ryan stays off-screen.

**Choice progression (corruption-tier gated)**:
- *Close at asking.* — small pay, no cost.
- *Hold his eye and take him twenty over.* — medium pay, corruption +1.
- *Let him look.* — higher pay, corruption +2, rep_road +1.

---

### R8 — Close big-ticket deal (`activity_shop_big`)

*The Crack-trigger activity. Maps to Beat B18.*

- **Location**: `loc_shop_customer_area` → `loc_shop_back_office`
- **Schedule**: Saturday afternoon when customer flag set
- **NPC**: Big customer (one of three archetypes)
- **Energy**: -30 / money +$80–300
- **is_repeatable**: no (by design — one big-deal in Phase 1 by design)

---

### R9 — Help fix something (non-commerce) (`activity_help_fix`)

- **Location**: `loc_ryans_shop` work bay
- **Schedule**: weekend afternoons, rainy weekdays
- **NPC**: Ryan
- **Energy**: -15 / ryan.trust +2
- **is_repeatable**: yes

Trust-building, no pay. The hands-on-the-same-engine scenes.

---

## SECTION D: JAKE ACTIVITIES

### J1 — Sketch with Jake (`activity_sketch_jake`)

- **Location**: `loc_jakes_room` OR `loc_yard` (outdoor sketching)
- **Schedule**: when Jake's receptive
- **NPC**: Jake
- **Energy**: -10 / art track
- **is_repeatable**: yes (post-Noticed)

**Base variants**:
- DEFAULT: *Paper, pencils. He doesn't show her his page. She doesn't show him hers.*
- WARM (post-Hand): *She leans over to see. He lets her.*
- CONSEQUENCE (Jake withdrawn route): *He says he's busy every time.*

---

### J2 — Watch Jake sketch (`activity_watch_jake`)

- **Location**: wherever he is
- **Schedule**: variable
- **Energy**: -5
- **is_repeatable**: yes

Ambient. Passive jake.arousal bump when corruption mid-band.

---

### J3 — Knock on Jake's door (`activity_knock_jake`)

- **Location**: `loc_hallway` (threshold)
- **Schedule**: when he's home
- **Energy**: -5

**Choice progression**:
- *Knock and wait.* — no answer at hostile; cracked door at Noticed; *"Yeah?"* at Tease.
- *Knock and walk in.* (corruption mid-band) — Tease-scene fires.

---

### J4 — Post-Tease linger (`activity_jake_linger`)

- **Location**: `loc_hallway` at Jake's door, `loc_bathroom` when Jake in hallway
- **Schedule**: evenings
- **Energy**: -5 / jake.arousal modifier +20 (8h)
- **is_repeatable**: yes (max 2/day)

**Base variant**: *She passes his door a second time. Doesn't look in. He knows.*

---

### J5 — Post-Caught visits (`activity_post_caught_jake`)

*Post-Hand milestone. The power-inverted register.*

- **Location**: `loc_jakes_room`
- **Schedule**: late evenings, she chooses
- **NPC**: Jake
- **Energy**: -10

**Variants per Keep route** (4):
- Owned: *She sits on his bed. Says what she wants him to do.*
- Lovers: *They draw together until one of them stops.*
- Withdrawn: *He doesn't let her in. The door isn't cracked anymore.*
- She-uses-him: *She asks about the community college. He tells her. The scene is a negotiation dressed as a hangout.*

---

### J6 — Help with college stuff (post-enrollment) (`activity_jake_college`)

- **Location**: `loc_jakes_room` or `loc_college_campus`
- **Schedule**: when Maya has enrolled
- **NPC**: Jake
- Phase 2+ surface mostly.

---

## SECTION E: GROUP ACTIVITIES

### G1 — Family dinner (`activity_family_dinner`)

- **Location**: `loc_kitchen`
- **Schedule**: daily 18:30–19:30
- **NPCs**: Diana (leads), Frank, Ryan, Jake
- **Energy**: -5 / social scene
- **is_repeatable**: yes (daily)

**Base variants (block pool, 6 — Diana-awareness bands × arc-state)**:
- Low-awareness, pre-arc: *Plates passed; Diana tells a story about okra.*
- Low-awareness, one-arc-live: *Frank's jaw ticks once; Diana doesn't notice; the plates keep moving.*
- Mid-awareness, two-arcs-live: *Diana looks at Maya across the table during the salad. Says nothing.*
- High-awareness, brothers-discover: *Three men quiet at the same dinner for the first time. Diana's spoon on the serving plate is the loudest thing in the room.*
- Post-Crack (Frank or Ryan): *The arc's NPC does not meet Maya's eye. Diana reads the table better than anyone.*
- Keep-locked (Phase-1 close dinner): the B28 variant.

---

### G2 — TV with whoever's home (`activity_tv_living_room`)

- **Location**: `loc_living_room`
- **Schedule**: evenings
- **NPCs**: whoever
- **Energy**: -5
- **is_repeatable**: yes

Block pool of configurations: Frank alone / Frank + Ryan / Frank + Jake / everyone / nobody.

---

### G3 — Saturday outdoor dinner (`activity_outdoor_dinner`)

- **Location**: `loc_back_porch`
- **Schedule**: Saturday 18:00–19:30
- **NPCs**: all + Diana
- **Energy**: -10
- **is_repeatable**: weekly

Longer-form group scene. The brothers-discover beat can fire in this canvas (Saturday variant).

---

## SECTION F: DINER ACTIVITIES

### D1 — T0 Distance shift (`activity_diner_t0`)

- **Location**: `loc_diner_front`
- **Schedule**: 17:00–22:00 Mon–Sat
- **NPCs**: Marge, Cookie, ambient regulars
- **Energy**: -40 / hygiene -15 / money +$45 / rep_road +1
- **is_repeatable**: yes (daily)

**Block pool (5 variants)**:
- Monday slow / Tuesday steady / Wednesday pickup / Thursday trucker-heavy / Friday the full floor / Saturday church overflow at lunch (not Maya's shift but ambient referenced).

---

### D2 — T1 Play-along shift (`activity_diner_t1`)

- **Location**: `loc_diner_front`
- **Schedule**: same as T0
- **Gate**: `corruption ≥ 25` + `rep_road ≥ 15` + `beauty ≥ 45`
- **Energy**: -40 / hygiene -15 / money +$53–65 / rep_road +2

**Base variants**:
- DEFAULT: *Laugh at the joke. Linger at the counter when Pete takes too long with the coffee.*
- WARM: *A $5 bill left under the plate without comment.*
- CONSEQUENCE (rep_church -1 accumulates over shifts): *The church couple switches booths.*

---

### D3 — T2 Work-the-floor shift (`activity_diner_t2`)

- **Location**: `loc_diner_front`
- **Schedule**: same
- **Gate**: `corruption ≥ 50` + `beauty ≥ 55`
- **Energy**: -50 / hygiene -20 / money +$70–105 / rep_road +3 / rep_church -1 per shift

**Base variants**:
- DEFAULT: *Lean on the counter. Hold the look. Pick the moment.*
- WARM (midpoint_crack triggered on a T2 shift): the B19 variant.
- CONSEQUENCE (post-Ryan-Beach): *The trucker crowd asks about Ryan. Maya picks what to say.*

---

### D4 — T3 Back-booth after-close (`activity_diner_t3`)

- **Location**: `loc_diner_back_booth`
- **Schedule**: Thursdays 22:00+ only (the key scene)
- **Gate**: `corruption ≥ 75` + `first_ambient_tilt = true` + specific customer flag
- **Energy**: -25 additional / money +$50–200 / rep_road +2 / rep_church -2

**Per-scene (not a mode toggle — each T3 scene is a separate choice Maya makes)**:
- Variant per customer archetype (trucker, mid-age regular, out-of-town): 3 customer templates.
- Each scene: block-gated decision to accept, negotiate price, or refuse.

---

### D5 — Drop by diner off-shift (`activity_diner_off_shift`)

- **Location**: `loc_diner_front`
- **Schedule**: open hours
- **Energy**: -5
- **is_repeatable**: yes

Ambient. Cookie chat on the back step. Marge's nod.

---

### D6 — Groceries from diner (`activity_diner_groceries`)

- **Location**: `loc_diner_front`
- **Schedule**: before Maya's shift, or Saturdays
- **Energy**: -5 / money -$8 for a bag of the family-style leftovers Marge bundles
- **is_repeatable**: yes

---

## SECTION G: TOWN ACTIVITIES

### T1 — Browse general store (`activity_general_store`)

- **Location**: `loc_general_store`
- **Schedule**: open hours
- **Energy**: -5 / money varies

**Block pool**: essentials / a new shirt / art supplies / nothing.

---

### T2 — Visit college admin office (`activity_college_admin`)

- **Location**: `loc_college_admin`
- **Schedule**: Mon–Fri 09:00–16:00
- **is_repeatable**: no (single visit, sets `college_brochure_taken`)

Single visit. Single scene. Brochure + information.

---

### T3 — Gas station / post office errands (`activity_errands`)

- **Location**: `loc_gas_station` OR `loc_post_office`
- **Schedule**: open hours
- **Energy**: -5
- **is_repeatable**: yes

Ambient. Minor rep ticks.

---

### T4 — Attend church front (`activity_church_attend`)

- **Location**: `loc_church_front`
- **Schedule**: Sunday 10:00
- **Energy**: -10 / rep_church +3
- **is_repeatable**: weekly

Not interior. The lawn-to-front-steps walk. Diana present.

---

## SECTION H: SOLO INCOME / EXTRAS

### H1 — Side work with Ryan (Saturday paid block)

Already R2.

### H2 — Sell sketches (Phase 2+, stubbed)

Art track unlock. Not active Phase 1.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## VALIDATION

- **Each deep NPC activity has DEFAULT + WITHDRAWN + WARM variants** (or per-route equivalents for Jake's post-Hand routes). ✅ Frank F1–F7, Ryan R1–R9, Jake J1–J5.
- **Consequence variants exist for all branching story events**: ✅ post-Restrict (F1, F2, F3, A8), post-Catch / post-Crack (F1, F3, G1), post-big-deal (R1, D3), post-Beach (R1, G1), post-Caught (J1, J5).
- **No flat tier ladder** — all choices visible, tiered gating strict (corruption/beauty/rep thresholds enforce which variant appears). ✅
- **Escalation logical** — for this register: peek → tease → caught → hand for Jake; help → partner → big → beach for Ryan; rules → tease → crack → call-out for Frank. ✅
- **Every Phase 2B income channel has an activity canvas**: ✅ T0=D1, T1=D2, T2=D3, T3=D4, Ryan small=R6, Ryan mid=R7, Ryan big=R8. Frank chores post-Restrict=F7.
- **Block pools on repeatables** (per Rule 17, 3–5 text variants): ✅ A1 sleep (3+), A2 shower (4), A3 sketch-in-room (4), F4 porch (4), R6 shop-small (3), G1 family dinner (6), D1 T0 (5).
- **Rule 16 consequence echoes** documented on activities that shift after story beats: ✅ A1 (post-Keep), A3 (per-arc hand sketch), A8 cook-solo (post-Restrict), F1 breakfast (post-Crack), F3 bookkeeping (post-Crack), D3 T2 (post-Beach).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End of Phase 5 — Activities. Proceed to Phase 6: Story Arc.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
