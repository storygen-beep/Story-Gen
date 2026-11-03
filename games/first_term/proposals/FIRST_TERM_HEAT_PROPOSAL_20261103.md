> Copied into the game on 2026-11-03 (third alignment pass) from `~/Documents/Great_Games_Study_20260926/FIRST_TERM_HEAT_PROPOSAL_20261103.md`, unchanged below this note. Signed by LO 2026-11-03 (DECISIONS 147: A1-A7 and A10-A13 yes, A8 and A9 no, B1-B20 yes, C1-C6 yes, C2, C4 and C6 as adjusted). Built in DECISIONS 148-152.

# First Term: the heat proposal (2026-11-03)

One page to sign. Three parts: **A** the places with no sex scene, **B** walk-ins, **C** the small rungs.
Nothing here is built. No beat is written here; every line is a one-line description.

**What I read.** `the-heat-ladder.md` (H1 stages, H2 accident first at home, H5 what pays, line 119; "a release
that writes only some stages", line 49), `the-surfaces.md` (R3 walk-ins, line 228; the payoff canvas must declare a
`location`, line 270; three to five outcomes per host, line 307; no "Nothing happens" events, line 867),
`the-board.md`, `register.md`, `engine.md` §31 and §46, `DECISIONS.md` rows 1–144, the person and place sheets,
`v2_state.json`, `7_final_game.toml` (read only), `SMALL_RUNGS_STUDY_20261103.md`, and `v2.py:6803-6880`
(`checkAndSubstituteCanvas`).

**Today's numbers** (`gates.py first_term`, run 2026-11-03 on the current build):

| gate | now | floor | needed |
|---|---|---|---|
| traversal heat | 17/31 destinations (55%) | 60% | 19 (two more) |
| explicit pools by place | 15/38 locations (39%) | 60% | 23 (eight more) |
| the walk-in floor | 0/24 rooms | every room | all 24 (the gate is red until no room is missing) |

**The rules every item keeps.** Release 1 writes stages 1–4 and every pay caps at 79. Her own button to go further
pays +1, capped at the top of the stage it opens at (19, 39, 59, 79). An accident pays HIS meter and sets a flag; it
pays her nothing. His Want goes on the moment the act happens, never on her answer; a no adds 0 to him and to her
(H5, DECISIONS 143, 135). No sex for money; Tom is strict and never sells her; no sex with Mark or Tom this release
(DECISIONS 102, 107, 108). Nothing at stage 5. Each act names its meter; a mixed act needs both meters at its stage
(DECISIONS 103). Stages: Corruption Good Girl 0 · Curious 20 · Bold 40 · Hungry 60; Exhibitionism Covered 0 ·
Daring 20 · Showing 40 · Watched 60. One person seeing her is stage 2 or 3; a group is stage 4.

---

## A · A sex scene in the cold places

The gate counts a place as hot when one of its screens has 3+ explicit words, or `_t4`/`_t5` media. The pools gate
counts a place when a repeatable there carries a `pool_dir` with `_t4`/`_t5` in its name. Every new surface below is
a repeatable with its own pool, so each one lifts **both** numbers.

### A1–A9 · new repeatable surfaces

| id | place | who | stage (meter) | the act, one line | trigger | pays | the written no |
|---|---|---|---|---|---|---|---|
| **A1** | `campus_gym` | Jake | Bold 40 · Hungry 60 (Corruption) | Bold: the empty locker room after training, door shut, her hand and then her mouth on his cock. Hungry: the team's showers running ten feet away, and he fucks her against the lockers. | Tue, Thu 16:30–17:00, Jake there; after `jake_first_time` (his step 4). A choice in his gym hub. | her Corruption +1, cap 59 (Bold) · +1, cap 79 (Hungry). Jake has no Lust meter, so nothing of his moves. | "Not here, Jake." · Jake: "Saturday, then." Pays 0. |
| **A2** | `canteen` | Zoe | Hungry 60 (Corruption; the table could see) | At lunch, Zoe's fingers under her skirt and into her pussy while Nadia talks across the table. | Mon–Fri 11:45–13:00, Zoe there; after `zoe_together` (her step 5). A choice in Zoe's canteen hub. | her Corruption +1, cap 79. Zoe has no meter. | "Not here, Zo." · Zoe: "Later, babe." Pays 0. |
| **A3** | `quad` | Jake and his team | Watched 60 (Exhibitionism); the doing yes is mixed, both at 60 | In his lap on the grass he shows her off: his hand up her skirt where the team can see. Doing yes: she lets his fingers in. | Mon, Wed, Fri 08:30–11:45, Jake there; after `jake_first_time`. A choice in his quad hub. | showing yes: Exhibitionism +1, cap 79 · doing yes: both +1, cap 79. | "Not in front of them." · Jake: "Saturday, then." Pays 0. |
| **A4** | `clothes_shop` | her alone (the assistant's voice outside the curtain) | Curious 20 (Corruption) | In the changing room she touches herself in the mirror, fingers on her clit, the assistant asking if the size is right. | Mon–Sat 10:00–18:00. A button on the existing `shop_try_on` screen. | her Corruption +1, cap 39 (the same as `touch_toilet`, `touch_shower`, `touch_bed`). | "Not here." She dresses. Pays 0. |
| **A5** | `zoe_bedroom` | Zoe | Bold 40 (Corruption); a Hungry band adds her pick of the act | "Stay over." In Zoe's bed, Zoe's mouth on her tits and her fingers in her, Zoe's middle crude column at Bold, the late one at Hungry. | Mon–Thu 22:00–00:00, Zoe there (her bedroom row); after `zoe_together`. A choice in Zoe's bedroom hub. | her Corruption +1, cap 59 · Hungry band +1, cap 79. | "Not tonight, Zo." · Zoe: "Ask me again." Pays 0. |
| **A6** | `zoe_kitchen` | the keg guy (a party regular, no row) | Hungry 60 (Corruption; the party can walk in) | By the keg, the guy she flashed bends her over the counter and fucks her while the party is through the door. | Fri 22:00–00:00 and Sat 00:00–02:00 (party night); after `keg_guy_dared`. A solo canvas in the kitchen, no `npc` field (he has no schedule). | her Corruption +1, cap 79. He has no meter. | "Not tonight." · him: "You know where the keg is." Pays 0. |
| **A7** | `zoe_bathroom` | Jake | Bold 40 (Corruption); Hungry band: the door left unlocked | At Zoe's Friday party he pulls her into the bathroom and fucks her against the sink while the queue knocks. | Fri 19:00–00:00, Jake at `zoe_apartment`; after `jake_first_time`. A solo canvas in the bathroom whose condition reads Jake in the living room (`requires_npc` would fail: he is scheduled next door). | her Corruption +1, cap 59 · Hungry band +1, cap 79. | "Not at Zoe's." · Jake: "Saturday, then." Pays 0. |
| **A8** (optional) | `art_office` | the art lecturer | Showing 40 (Exhibitionism: naked by choice for one person) | She poses nude on the office stool while the lecturer draws her: a pose, not sex. It counts as hot by the gate's word count. | Mon, Tue, Thu, Fri 14:30–18:00, lecturer there; after `art_lecturer_met`. A choice in her office hub. | her Exhibitionism +1, cap 59. She has no meter. | "Not today." · her: "The offer stands." Pays 0. |
| **A9** (optional) | `vance_house` | Vance | Daring 20 (Exhibitionism: a flash for one person she knows) | On his porch step she lifts her top for him, and no money or rent moves. | every day 18:00–22:00, Vance there; from his Lust 30. A choice in his porch hub. | his Lust +2 on the flash itself, her Exhibitionism +1, cap 39. | "Goodnight, Mr. Vance." (already built, pays 0). |

**A8 and A9 clash with a signed page, so they are optional.** A8: her sheet says her rungs wait for the next release
(`npc_art_lecturer.md`, SP5), and posing is what she "wants later". A9: Vance's sheet says "his arc is later", and a
flash for the landlord sits close to "no sex for money" even with no money on the page. **My call: A8 yes if you want her
started; A9 no.**

### A10–A13 · a pool on a screen that is already explicit (media only, no new prose)

These four places already have a repeatable screen with 3+ explicit words by the build's own count. A pool there is
honest. Tag them `_t4` (nudity), never `_t5`: these are exposure scenes, not sex.

| id | place | the screen | what it adds |
|---|---|---|---|
| **A10** | `home_garden` | `garden_sun` (8 explicit words: topless to Ryan's window or Mark's garage door) | a `_t4` pool on the show-off screens |
| **A11** | `street` | `street_seen_nobra`, `street_seen_nopanties` (5 and 4) | a `_t4` pool on the witness screens |
| **A12** | `home_hall` | `wardrobe_event_stairs` (3: Mark at the foot of the stairs) | a `_t4` pool on the no-panties screen. Or B5's walk-in carries the pool instead |
| **A13** | `party_house` | `party_house_soak` (Watched 60) | a `_t4` pool on "Leave it.", plus one more body word on that screen so it reaches 3 (it measures 2 now) |

### Skip, and why

| place | why |
|---|---|
| `college_mens_toilet` | LO: built empty, nothing to do (DECISIONS 76) |
| `corner_shop` | LO: the grocery run only, plain, no heat (DECISIONS 50; its sheet: no heat in stages 1–3) |
| `business_office` | he can't be bought, no route (his sheet) |
| `dean_office` | his ladder is a later release; Zoe's dean rung is later (`RELEASE1_SCOPE.md`, his sheet) |
| `ta_office` | her rungs wait for the next release (SP5); nothing private fits without starting her ladder |
| the containers `home`, `campus`, `town`, `zoe_flat` | the engine shows no scene in a container; they stay in the pools denominator and can never count |
| `faculty_floor` | a corridor of office doors; nothing sexual belongs there |

### Cost

| id | cost |
|---|---|
| A1, A5, A7 | one loop canvas each with 2 bands, 3–4 screens, 3–4 explicit beats by `v2-prose`, measured with `gates.py --beat`; one pool each; the person sheet and the place sheet re-signed |
| A2, A3 | 2–3 screens each, 2 explicit beats, one pool, two sheets re-signed |
| A4 | 2 screens, 1 explicit beat, one pool; adds a fourth place to DECISIONS 13 ("her bed, the shower, the college toilet") |
| A6 | 2–3 screens, 2 beats in the strangers' words of DECISIONS 41 (no fuck, cum, pussy), one pool |
| A8 | 2 screens, 1 beat, one pool; moves her out of "later" (SP5 changes) |
| A9 | 2 screens, 1 beat, one pool; starts Vance's arc this release |
| A10–A12 | media only: one pool folder each |
| A13 | one pool folder and one line edited and re-measured |
| all pools | need a media harvest, which only LO starts. Until it runs, each pool folder renders its fallback |

### What A reaches

| if LO signs | traversal heat | explicit pools by place |
|---|---|---|
| A1–A7 and A10–A13 (my rec) | **24/31 (77%)** | **26/38 (68%)** |
| plus A8 | 25/31 (81%) | 27/38 (71%) |
| plus A8 and A9 | 26/31 (84%) | 28/38 (74%) |
| the least that passes both | any 2 of A1–A9 | A10–A13 plus any 4 of A1–A7 |

---

## B · Walk-ins

**How the engine does it** (`the-surfaces.md` R3, `v2.py:6803-6880`). The solo activity she clicks carries
`trigger.substitutions`. On entry the engine rolls; on a hit it shows the walk-in canvas instead. The walk-in canvas
has `substitution_only = true` and its own `trigger.location`, or it silently never fires. The walker is in another
room when the roll happens, so the rule's condition reads **where he is now and the time his next row brings him
here** (for example Mark in the garage at 21:30–22:00, whose living-room row starts at 22:00). The target must not
carry `requires_npc`: `_tryRule` would refuse it, because he is not in her room yet.

**The pay rule, the same for every walk-in.**
- Screen 1 is the moment ("The door opens."). Its only exit carries his raise: **his Lust +2, once a day per person**,
  the size the towel hubs use (DECISIONS 98). This puts his Want on what happened, never on her answer (H5, DECISIONS 143).
- Screen 2 is her answer, banded on the meter the act uses. The first button is always the cover or the way out, and
  it pays 0. One bolder button per band pays her +1, capped at that band's top.
- People with no meter (Kayla, Gary, Jake, Zoe, Nadia, the lecturers, the TA, the dean) gain nothing. A flag records
  the walk-in, and their next hub line reads it.
- Odds: 1 in 4 (0.25), as DECISIONS 59 set for home events. One rule per walker, each walker's window separate in
  time, so Pattern A rolls give the odds that are written. Once a day per walker, through a `*_walkin_today` flag added
  to `[engine.daily_tick]` (DECISIONS 77).
- At home the walk-in is the accident that comes first (H2). Its flag can open that person's chosen act later.
- There are no empty outcomes. A miss shows her activity as it is today.

### Home first (H2: an accident before her chosen act)

| id | room · the activity she's doing alone | who walks in, when (his row) | what he does · her answers by band | the flag |
|---|---|---|---|---|
| **B1** | `home_bathroom` · `bathroom_shower` (and `touch_shower`) | **Ryan**, awake in his room (Sun–Thu 19:00–00:00, weekends 07:30–14:00); **Kayla**, Fri 18:00–22:00 (Ryan's Friday row); **Mark**, Sat 09:00–17:00 from the garage, for the sink | Ryan comes in for his toothbrush and stops; Kayla comes in to pee and looks her over; Mark comes in with grease to his elbows and doesn't look away. Hers (Exhibitionism): Covered: "Grab the towel." (0) · "Don't grab it straight away." (+1, cap 19) · Daring: "Keep washing." (+1, cap 39) · Showing: "Turn round." (+1, cap 59). After Ryan's step 6, a "Let him stay." button leads into his built bathroom hub. | `ryan_walked_in_shower`, `kayla_saw_her` (Ryan's hub: "Kayla says you've got nice tits."), `mark_walked_in_shower` |
| **B2** | `home_kitchen` · `kitchen_breakfast`, `kitchen_coffee` (kitchen empty) | **Ryan**, Sat and Sun 07:30–10:00, down from his room in his boxers; **Mark**, Sat 08:30–09:00 on his way to the garage | Ryan reaches over her for a mug, morning wood against her ass, and turns it away (H7 leak); Mark's hand on her hip to get past. Hers (Corruption, a brush): "Step aside." (0) · "Don't move." (+1, cap 19) · Curious: "Push back into him." (+1, cap 39) | `ryan_brushed_kitchen`, `mark_brushed_kitchen` |
| **B3** | `home_living_room` · `living_tv` (channel 5), `living_film` | **Mark**, Sun–Fri 21:30–22:00 (his late TV row starts at 22:00); **Ryan**, Sat and Sun 13:30–14:00 (his TV row); **Laura**, Sat 21:30–22:00 (she waits up from 22:00) | Mark finds channel 5 on; Ryan the same; Laura the cover branch: she sees the screen, says one line, no heat. Hers (Corruption): "Turn it off." (0) · Good Girl: "Don't reach for the remote yet." (+1, cap 19) · Curious: "Leave it on." (+1, cap 39; with one person she knows it is a chosen act, so stage 2). Laura's branch has only the off button and her line. | `mark_caught_ch5` (his hub: "Channel five, was it?"), `ryan_caught_ch5`, `laura_saw_ch5` |
| **B4** | `home_garage` · `garage_laundry` | **Mark**, Mon, Tue, Thu, Fri 18:45–19:00 and Sat 08:45–09:00 (his garage rows start); only after `mark_saw_her`, so the dryer accident stays first | He comes in while she's bent at the drum. The answers route into the built laundry tease ladder (DECISIONS 128): the basket (Curious), "Bend for the bottom drum." (Curious and Daring), "Wash what you're wearing." (Bold and Showing), with their built pays. | `mark_walked_in_laundry` |
| **B5** | `home_hall` · `hall_mirror` | **Ryan**, his door opening behind her (any hour he's in his room awake); **Mark**, 01:30–02:00 coming up to bed | He sees her in the mirror in what she has on; the mirror's built lines by what she wears are reused. Hers (Exhibitionism): "Go to your room." (0) · "Stay at the mirror." (+1, capped at her stage's top: 19, 39 or 59). This shares the daily brake with the hall's two random events, so it is one hall accident a day. | `ryan_saw_mirror`, `mark_saw_mirror` |
| **B6** | `home_master_bedroom` · `master_wardrobe` | **Laura**, Sat 16:45–17:00 (she dresses from 17:00); **Mark**, Sat 21:45–22:00 (he goes up at 22:00) | Laura catches her in her dress: good mom, a line by Laura's Love, no heat, no pay. Mark catches her in Laura's lingerie and stares (taboo accident, no touch). Hers with Mark (Exhibitionism): "Cover up." (0) · "Let him look." (+1, cap 19 at Covered, 39 at Daring) | `laura_saw_wardrobe`, `mark_saw_lingerie` |
| **B7** | `home_ryan_room` · `ryan_things` (Ryan out) | **Ryan**, Sun, Mon, Tue, Thu 18:45–19:00 (up from dinner); **Kayla**, Fri 17:45–18:00 (she arrives with him) | Ryan catches her holding what she found; his line by his Lust band. Kayla: "Snooping?" and a hook line, nothing about Ryan's secret. Hers (Corruption) with Ryan: "Put it back." (0) · "Hold it up. 'Explain this.'" (+1, cap 19) | `ryan_caught_snooping`, `kayla_caught_her` |
| **B8** | `home_front_door` · `front_step` | **Vance**, every day 18:00–22:00 from his porch; **Jake**, 18:45–19:00 on a booked Wednesday or Saturday (early for the pickup) | Vance stops at the gate and looks at her legs (his porch lines by Lust); Jake early, a kiss on the step. Hers with Vance (Exhibitionism): "Pull your skirt down." (0) · "Leave it." (+1, cap 19) · Daring: "Stretch your legs out." (+1, cap 39) | `vance_saw_step`, `jake_early` |

### Out of the house

| id | room · the activity she's doing alone | who walks in, when | what they do · her answers | the flag |
|---|---|---|---|---|
| **B9** | `cafe` · `cafe_coffee` (off shift) | **Gary**, Mon–Fri 14:30–18:00, Fri 20:00–22:00 | He sits down at her table; his knee finds hers. "Move your knee." (0) · "Leave it." (Corruption +1, cap 19) · Curious: "Let his hand rest on your thigh." (+1, cap 39). **No tip, no money:** she is off shift. | `gary_sat_with_her` (his booth line reads it) |
| **B10** | `campus_gym` · `gym_workout` | **Jake's team** at 14:45–15:00 Tue and Thu (unnamed before `jake_number`, DECISIONS 144); **Jake** after it | They come in while she's on the bench in her sports bra. "Cover up and go." (0) · Daring: "Finish your set." (Exhibitionism +1, cap 39). After A1, Jake's line points at the locker room. | `team_saw_gym` |
| **B11** | `canteen` · `canteen_eat`, `canteen_listen` | **Zoe**, **Jake**, **Nadia**, Mon–Fri 11:30–11:45 (lunch starts 11:45) | Zoe slides in and puts a hand on her knee (F/F tease); Jake: "Guys. Look at her." if her skirt is short; Nadia: a line about Hale, no heat. With Zoe (Corruption): "Move her hand." (0) · Curious: "Let it stay." (+1, cap 39) | `zoe_canteen_knee` |
| **B12** | `library` · `library_study` (not the stacks, so C1 is untouched) | **Nadia**, Mon, Tue, Wed, Fri 14:15–14:30 | She sits down beside her. After a new flag `library_stacks_seen` (set on the stacks' stay exit): "You saw them too? Everyone goes back there." Overhearing as a hook; no pay. | `nadia_knows_stacks` |
| **B13** | `park` · `park_run`, `park_rest` | **Zoe**, Sat and Sun 07:45–08:00 (her run starts 08:00) | She catches up and slaps her ass ("Race you."), or flops down with her head in her lap. The answers route into the built `zoe_park_dare` and her park hub. | `zoe_caught_up` |
| **B14** | `party_house` · `party_house_soak` (Watched 60) | **Zoe**, Sat 23:30–00:00 | She gets in beside her; after `zoe_together` her hand goes under the water while the deck can see. "Not here, Zo." (0) · Hungry: "Let her." (Corruption +1, cap 79; needs Corruption 60 too, a mixed act) | `zoe_in_the_tub` |
| **B15** | `quad` · `quad_grass` | **Jake** and the team, Mon, Wed, Fri 08:15–08:30; **Zoe**, Tue, Thu, Fri 14:15–14:30 | Her skirt has ridden up on the grass and the team sees (a group look that happens to her, stage 1); Zoe lies down with her head in her lap. With the team (Exhibitionism): "Fix your skirt." (0) · "Leave it." (+1, cap 19) | `team_saw_grass`, `zoe_lap_quad` |
| **B16** | `lecture_hall` · `lecture_timetable` | **Hale**, Mon, Wed, Fri 08:15–08:30, setting up early; only after `hale_01_done` | He finds her alone in the hall and looks at her legs, pen in his hand (his leak). "Take a seat." (0) · Daring: "Sit on the front desk while he sets up." (Exhibitionism +1, cap 39) | `hale_early_look` |
| **B17** | `zoe_apartment` · `zoe_couch_alone` | **Zoe**, Mon–Thu 22:00–00:00, out of her bedroom in her sleep shirt and no bra | Her leak. "Say goodnight." (0) · Curious: "Pull her down onto the couch." (Corruption +1, cap 39). After `zoe_together`, a link to A5. | `zoe_couch_night` |
| **B18** | `zoe_bedroom` · `zoe_bedroom_look` | **Zoe**, Mon–Thu 21:45–22:00, coming in to change for bed | She strips in front of her ("Nope. Eyes stay."). "Look away." (0) · "Watch her change." (Corruption +1, cap 19: a look that happens to her, she stays) | `zoe_changed_in_front` |
| **B19** | `vance_house` · `vance_house_look` | **Vance**, 18:00–18:15 (he comes out onto his porch) | He sits down and looks at her legs; his built porch lines by Lust. "Walk on." (0) · Daring: "Stay where he can see your legs." (Exhibitionism +1, cap 39) | `vance_porch_look` |
| **B20** | the five office doors · `door_grade_*`, `door_dean_notice` | the person in each office, inside their own office hours (they are already inside, so they open the door) | The art lecturer looks at her as if measuring her for a pose; the TA looks and catches herself (H7); the dean: "Is that what you wore to class?"; Hale on Thursday 16:45–17:00, by his step; the Business lecturer looks at the grade, not at her. One screen each, line only, no pay. | `<person>_door_seen`, read by their hub |

### Cost

| id | cost |
|---|---|
| each home walk-in (B1–B8) | `substitutions` on the host (one rule per walker), one target canvas (`substitution_only`, its own `location`), 2 screens per walker, one or two short paragraphs per band, a media pool where the screen is explicit, the place and person sheets re-signed, flags added to the overnight list |
| each out walk-in (B9–B19) | the same, 1–2 walkers, thinner |
| B20 | five rules, five one-screen canvases, about 5 lines in all, no pools |
| engine | none: the importer reads `substitutions` already (`template_import.py:2461-2481`) |
| about | 20 router rules on hosts, 20 target canvases, about 60 short screens, about 25 explicit beats where the band is on the body |

### What B reaches

| if LO signs | the walk-in floor |
|---|---|
| B1–B20 | **24/24, green** |
| home only, B1–B8 | 8/24: still red, because the gate fails while any room is missing |

The walk-ins can also heat cold rooms: B10, B11, B15 and B18 sit in four of A's cold places. Written on the body
with 3+ explicit words, they count for traversal heat even if their A item is a no.

---

## C · The small rungs (option B, as shown to LO), checked

Each rung is one bolder button inside a scene she already gets. It pays +1, capped at 19, and it shows greyed as
"(Needs Corruption N)" until she has the number. The quest card gets a goal line per rung.

| id | meter, rung | where | the button | against the build, A and B | verdict |
|---|---|---|---|---|---|
| **C1** | Corruption 5 | library back stacks (`library_back_stacks`, node `stay`) | "Move one aisle closer." | The build has "Stay behind the shelf." (pays +1 cap 19 on its exit). Closer is still hidden, inside the accident, so it stays stage 1 ("a look that happens to her, even when she stays", H1). B12 sits on `library_study`, not here. | **keep.** She stays unseen; if the couple sees her, it becomes a stage 2 catch. |
| **C2** | Corruption 10 | living-room TV | was: "Leave it on when the film gets hot." | **Clash.** Channel 5 (porn) already pays +1 cap 19 from Corruption 0 (DECISIONS 86), so a hot scene in an ordinary film at 10 is tamer than what is open at 0. | **adjust:** on channel 5, "Turn the sound up." at Corruption 10, +1 cap 19. It ends the session (DECISIONS 91). While it's up, B3's walk-in odds go from 0.25 to 0.5 (the house hears). The risk is a sentence on the screen. |
| **C3** | Corruption 15 | Ryan's door ajar (`ryan_door_ajar`, nodes `watch` and `watch_low`) | "Stay until his light goes off." | The built exits pay +1 cap 19. The new button pays its own +1 and leads to one more screen whose exit pays the +1, so it is +2 a night, cap 19. B7 sits on `ryan_things` (Ryan out), and the hall's door event needs `ryan_step` 7, so nothing clashes. | **keep.** |
| **C4** | Exhibitionism 5 | home shower (`bathroom_shower`) | "Leave the door unlocked." | **It depends on B1.** Without a walk-in nobody can ever come through the unlocked door, so the line would be false (the truth rule). The roll happens on entry, so a flag cleared at midnight would never matter. | **adjust:** `shower_unlocked` stays set until she picks "Lock it again." on a later shower. While it's set, B1's odds go from 0.25 to 0.5. +1 cap 19 once a day. **Sign it together with B1.** |
| **C5** | Exhibitionism 10 | clothes-shop changing room (`shop_try_on`) | "Leave the curtain where it is." | The screen has one exit today ("Hang them back up."). The watcher is one stranger in the queue, a look that happens to her, and she leaves it (stage 1). A4 goes on the same screen at Corruption 20. | **keep.** |
| **C6** | Exhibitionism 15 | the rack | the sheer blouse | It already exists: `thin_top`, "Sheer blouse", $20, buyable today at Exhibitionism 0 (only the garage hold locks it). Two scenes read it worn. | **adjust:** add `exhibitionism gte 15` to its conditions, AND with the garage-hold flag. The rack shows "(Needs Exhibitionism 15)". A save that already owns it keeps it. Worn with a bra it is still "covered", so no state's readers change. |

**Cost:** 5 buttons (C1–C5), each with one short screen by `v2-prose`; one garment condition (C6); 6 quest-card goal lines;
the library, living-room, Ryan's-room, bathroom and clothes-shop sheets and the wardrobe card re-signed. No engine work.
C moves neither floor: the four home and library places are already hot and pooled, and the shop gets its heat from A4.

---

## Found while reading (not part of the sign)

- `zoe_05_no_dare` is built at `zoe_apartment`; her sheet puts step 5 in `zoe_bedroom`. Moving it does not fix the
  bedroom: Zoe has no bedroom row on Saturday 00:00–02:00, and it is not a repeatable, so A5 is still needed.
- `mark_00_the_dryer` pays Mark's +5 on both endings, including the one after "Take the towel." That is the same value
  on every way out, and the gate `a no never raises his Want` passes it. The walk-ins above put his raise on screen 1
  instead, the way DECISIONS 143 moved Ryan's +10 onto "Open the door."
- The walk-in gate counts the offices as rooms where she is alone, although each office is open only in its person's
  hours. That is why B20 is "he opens his door", which is true at every hour the room is open.

---

## Sign sheet

Answer on one line, for example:

```
A1 yes, A2 yes, A3 yes, A4 yes, A5 yes, A6 yes, A7 yes, A8 no, A9 no, A10 yes, A11 yes, A12 yes, A13 yes,
B1 yes, B2 yes, B3 yes, B4 yes, B5 yes, B6 yes, B7 yes, B8 yes, B9 yes, B10 yes, B11 yes, B12 yes, B13 yes,
B14 yes, B15 yes, B16 yes, B17 yes, B18 yes, B19 yes, B20 yes,
C1 yes, C2 adjusted yes, C3 yes, C4 adjusted yes, C5 yes, C6 adjusted yes
```

C2, C4 and C6 can also take "as shown" to keep the version LO saw first.
