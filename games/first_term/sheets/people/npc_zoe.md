# [READY] Person — Zoe

> **Changed 2026-11-01, re-signed by LO 2026-11-01** ("Signed", DECISIONS 113; design DECISIONS 99–112): the release-1 ladder, from `proposals/ZOE_R1_LADDER.md` (signed 2026-11-01). Changed: Ladder, the seven columns, Leak and promise, the dares, step 5, the party regulars. Everything else as signed.

> **Changed 2026-10-29, re-signed by LO 2026-10-29** (DECISIONS 87–88): her run text books the run; a no-show sets `zoe_bailed`, read by her next park line. Her party text: "obviously" is a promise to come short.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08). Re-signed 2026-10-29 ("sign all", in chat).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the place sheets. Id `npc_zoe`.

| row | answer |
|---|---|
| age | 19 |
| role | her friend |
| what she wants from her | someone to follow into fun |
| what she visibly wants, each visit | a partner in trouble; she wants @player, and dares instead of asking |
| what she keeps | step counter + memory flags |
| where she sleeps | `zoe_bedroom` |
| what she calls her | "babe" |
| met | the quad, week 1: `zoe_00_quad_meeting` sets `zoe_met` |
| her line: short skirt | "Now we're talking. Turn around." |
| her line: no bra | "Oh, you're ready for Friday." |
| her line: her party dress | She bites her lip at the bra strap. "Nope. Eyes stay." |

## Crude words, by stage (SP2: "on their sheets")

| column | words |
|---|---|
| early (stages 1–2) | tits, ass |
| middle (stage 3) | tits, nipples, wet |
| late (stages 4–5) | pussy, clit, fuck |

A ceiling, never a floor. LO took these, 2026-10-08.

## Schedule grid (S5)

| place | days | from | to | why she is there |
|---|---|---|---|---|
| `quad` | Tue, Thu, Fri | 14:30 | 18:00 | between classes |
| `party_house` | Sat | 20:00 | 00:00 | the party house, the hot tub (Zoe A 3); above her living-room row |
| `zoe_apartment` (her living room) | Mon–Thu | 18:00 | 22:00 | home evenings |
| `zoe_apartment` (her living room) | Fri, Sat | 18:00 | 00:00 | Friday party · Saturday evening |
| `zoe_apartment` (her living room) | Sat | 00:00 | 02:00 | the Friday party after midnight |
| `zoe_bedroom` | Mon–Thu | 22:00 | 00:00 | going to bed: she lends the dress |
| `canteen` | Mon–Fri | 11:45 | 13:00 | lunch |
| `park` | Sat, Sun | 08:00 | 10:00 | her weekend run |

## Everyday: make-up before the party (LO's pick 12, 2026-10-08)

A choice in Zoe's hub in her living room, Friday 18:00–19:00, before the party: "Lips. Open." Zoe does
@player's face; `made_up` set true (10 hours). Curious: she does it sitting in @player's lap. Lines guess.

## Ladder — one guidance card per step (S10)

> **Changed 2026-11-01, re-signed by LO 2026-11-01:** six steps, one per first. Paced by party nights and Ella's own
> meters (a step counter): a declared exception to taste rule 5. The dares are her hot repeatable, and where both of
> Ella's meters grow fastest.

| n | canvas | where | when | gate | raises | the no | guidance card line |
|---|---|---|---|---|---|---|---|
| 0 | `zoe_00_quad_meeting` | `quad` | her hours | none | `zoe_met` set · her number | (as built) | The quad, between classes: a girl who's looking at you. |
| 1 | `zoe_01_first_party` (= Jake 1) | `zoe_apartment` | Fri 19:00–23:00 | step 0 (built: jake_step eq 0, the shared step) | exhibitionism add +3 | "Not tonight, Zo." (parked; costs nothing) | Friday evening: Zoe's party at her apartment, and she has a dress for you. |
| 2 | `zoe_02_bra_through_the_sleeve` | `zoe_apartment` | Fri 21:00–00:00 | Corruption 20 **or** Exhibitionism 20 (was and) | exhibitionism add +3 | "Not tonight, Zo." (parked) | A Friday party at Zoe's, out on the balcony: Zoe has a dare. |
| 3 | `zoe_03_hot_tub` | `party_house` | Sat 20:00–00:00 | Corruption 20 · Exhibitionism 20 (was 40 · 40) | exhibitionism add +3 · corruption add +3 | "Not tonight, Zo." (parked) | Saturday night: the hot tub at the party house. Zoe's friends head inside first. |
| 4 | `zoe_04_i_pick_the_dares` | `zoe_apartment` | Mon–Thu 18:00–22:00 · Sat 18:00–20:00 | step 3 (was Corruption 40) | `picks_the_dares` set: **the dares open** | Zoe's: "Not that one, babe." (parked) | An evening at Zoe's, on her couch, after the hot tub. |
| 5 | `zoe_05_no_dare` (new, top step) | `zoe_bedroom` | after a Friday party, Sat 00:00–02:00 | step 4 · Corruption 40 · four dares done | `zoe_together` set · `zoe_let_him_watch` (her pick) | "Ask me again." | After Friday's party: Zoe's bedroom, the music still through the door. |
| — | locked | her card | — | Corruption 60 | — | — | "Zoe's next dare. (Needs Corruption 60.)" (threesome, foursome, gloryhole, the dean, the porn video, gangbang: later) |

Every step's gate also says the drinks boost is off. Stage numbers: 20 is Curious or Daring, 40 Bold or Showing.

## Card goals (LO's play note, 2026-10-08)

Each guidance card's goals are the step's real requirements: the meters, flags, place and hour in its
row above. Never the step counter (no "1 / 2"). A requirement on another person's ladder is named as
the event, e.g. "after Ryan's feet-in-his-lap night".

## Each step, by the seven columns (`sheets/TASTE_COLUMNS.md`)

| n | the moment | who sees or knows | what she risks | how she says yes | Zoe's move | does it finish | what changes after |
|---|---|---|---|---|---|---|---|
| 0 | Zoe on the quad: "You're new. Party Friday. Wear something short." | Zoe | — | she takes Zoe's number | the invite | yes | `zoe_met`, her number |
| 1 | Zoe's dress on her, her first dare, and a guy who picks her out: Jake | Zoe, the party, Jake | the party's eyes | she takes the dare | the dress and the dare | yes | Jake met; party nights |
| 2 | a dress dare on the balcony, the room behind the glass watching: her bra comes off through her sleeve | the room behind the glass | strangers seeing | "Watch me." (showing) · "Dare me something else." (doing) | the dare, and her eyes on Ella | yes | the party house invite |
| 3 | the hot tub: her friends go in first; topless for Zoe alone, and Zoe kisses her | Zoe; the friends in the water | being seen topless; a girl's mouth on hers | the top comes off · she kisses back | the kiss | yes | home at three; Ryan at his door sees her come in (Ryan's Lust +5, built) |
| 4 | Zoe's couch: "I dared you instead of asking. I always do." | Zoe's secret is hers | — | "Then keep daring me." | the admission | yes | `picks_the_dares`: party nights are Zoe's to dare; the dares open |
| 5 | after the party, Zoe's bedroom: "No dare. I'm asking." Ella says yes, and Zoe goes down on her, and Ella comes with her hand over her mouth. The door opens: the cocky guy, a beer in his hand. Zoe, without looking up: "Out." Or: "Stay. Watch." | Zoe; **the cocky guy at the door** | the party hearing; the guy at the door | "Yes." (out loud) · "Ask me again." | she asks; she decides about the door | **yes** | `zoe_together`; the dares change; the door line is the hook for the locked threesome |

**Her voice (rule 7):** low line, "It's a dare. It doesn't count." · high line, "You want her to dare you something
worse." Both on each step sheet.

### Leak and promise (S5)

| n | the leak: her want, shown before | the promise: the line it ends on |
|---|---|---|
| 0 | none: step 0 | "Party Friday. Wear something short." |
| 1 | her head in @player's lap on the quad: "Let them." | "Kiss someone. Or don't, and I'll keep asking." |
| 2 | she keeps her eyes on the bra strap | "Nope. Mine now." |
| 3 | "There's a hot tub Saturday. Just us." | "Took you long enough." |
| 4 | "You didn't need me last night." | "From now on, I pick the dares." |
| 5 | she picks the dares that keep Ella close to her | "No dare. I'm asking." |

**Final no:** none. Every dare has "Not tonight, Zo" (parked, costs nothing).

**What the release ends on:** the dares by stage, the door hook (`zoe_let_him_watch`) and the locked line.

## The dares (her hot repeatable, rule 6)

- **When:** party nights, after step 4: Friday at Zoe's apartment, Saturday at the party house. **One dare a night.**
  Zoe picks it; her line names the dare.
- **Every dare:** a showing yes, a doing yes and the no (`sheets/systems/meters.md`).

| stage | showing yes (Exhibitionism) | doing yes (Corruption) | pays |
|---|---|---|---|
| Curious · Daring | "Flash the guy at the keg." | "Kiss the cocky guy. Properly." | that meter +1 (both when seen) |
| Bold · Showing | "Topless in the kitchen till the song ends." | "Sit in his lap until he's hard. Make him beg." (mixed: Corruption 40 and Exhibitionism 20) | +1 each, mixed pays both |
| after step 5 | Zoe joins the dare: "Kiss me where they can see." | "Let her watch you with him." | both +1 |
| Corruption 60 | — | — | locked: "Zoe's next dare. (Needs Corruption 60.)" |

- **The no:** "Not tonight." Zoe pouts and picks something tamer next week. Never a cost but the meter.
- **Who sees:** the room, every time; the regular in the dare remembers it next party ("You again.").
- **Jake:** if Jake is her boyfriend (Jake step 3), each dare with a man carries one line of risk: someone at the party
  knows Jake. Jake finding out is a later release.

**The party regulars, not faceless strangers** (`HEAT_STUDY.md` turn-off 4): the cocky guy (already in the game), the
guy at the keg, the hot-tub girl. Each has one detail and a memory of what she did last time.

## Step 5, "No dare"

- **The door:** the player's pick on a button: "Tell him to go." / "Let him watch." Both finish the act. "Let him
  watch" sets `zoe_let_him_watch`, which the locked threesome reads later.
- **Crude words:** step 5 is Bold (stage 3, the middle column), which can't write this act on the body.
  **Proposed:** step 5 uses the late column ("pussy, clit, fuck"). **LO confirms on the scene sheet.**

## Not cut, but changed

- Step 3 (the hot tub) and step 4 (I pick the dares) gates come down to Curious and Daring, so the dares open before
  Bold. No built step is cut.

## Phone thread

| thread | cause flag (a scene sets it) | delay | window | booking (place + time, reminder) | loop |
|---|---|---|---|---|---|
| `zoe` | `zoe_met` | 1 day | Thursday 18:00–22:00 | "Party Friday. Wear something short." her apartment, Fri 19:00 · reminder: quest card | every 7 days, Thursday |
| the run | `zoe_met` | 2 days | Friday 18:00–22:00 | "Run tomorrow? 8. The park." · reminder: quest card | every 7 days |

### Messages, per reply (LO's note, 2026-10-08)

Each follow-up waits for her reply (`after_round`), and a different answer follows each reply where it matters (`after_choice`). Texts are lowercase, 3–7 words. Lines are samples (guess).

**`zoe` — the party.** Thursday 18:00–22:00.

| round | Zoe | her reply | after that reply |
|---|---|---|---|
| 1 | "party tmrw. wear something short" | "obviously" | "that's my girl 😈" |
| | | "what counts as short" | "come by tonight. i'll lend you one" (Zoe is home till midnight) |
| | | "can't. my mom" | "sneak out. kidding. kinda" |

**The run.** Friday 18:00–22:00. "8, the park" is a meeting time, a rule of the world.

| round | Zoe | her reply | after that reply |
|---|---|---|---|
| 1 | "run tmrw? 8. the park" | "i'm in" | "wear the sports bra 😏" · sets `zoe_run_booked` |
| | | "too early" | "lazy. next week then" |

**Bookings and no-shows (changed 2026-10-29, DECISIONS 87–88, re-signed by LO 2026-10-29).** A yes books it; showing up pays or plays its line and clears the booking; a yes with no show brings a short text that costs, whether she answers it or ignores it for a day. Ignoring the first text costs a little. Amounts are guesses for LO.

| text | the yes books | showing up | ignored a day | the no-show text (when) | it costs |
|---|---|---|---|---|---|
| "run tmrw? 8. the park" | "i'm in": `zoe_run_booked` | at the park: "You actually came! Okay. I owe you a coffee." (Zoe has no number, so nothing more) | nothing | "you bailed on me 🙄" · "i ran alone like a loser" (16 hours after the yes, 10:00–20:00) | sets `zoe_bailed`: her next park line is "Oh, look who remembered mornings exist." |
| "party tmrw. wear something short" | "obviously": `zoe_party_promised` (read for 30 hours) | at her door in something short: "Told you. Short. Good girl." · not short: "\"Obviously\", she said. That's not short, babe." | nothing | none | none |

## Rows a gate needs

| row | gate |
|---|---|
| the step counter read by every gate | ladders move forward |
| the four-dares counter read by step 5 | a meter is read |
| her park row has a hub | standing surface |

## Why — the source of each key choice

| key choice | source |
|---|---|
| steps, lines and nos | SP2 · the arc ideas (Zoe A) |
| the release-1 ladder, six steps, the dares by stage, the regulars, "No dare" | `proposals/ZOE_R1_LADDER.md`, signed by LO 2026-11-01 (DECISIONS 99–111) |
| the park on weekend mornings | LO, 2026-10-08 |
| Zoe A 3: only Zoe sees her | LO, 2026-10-08 |
| the threads | guess |
| her rows split by room in her flat | LO, 2026-10-08 (questions 47, 48, narrowed by 52) |
| Zoe at the party house Sat 20:00–00:00 | LO, 2026-10-08 (sweep A4-08) |
| messages per reply | LO's play note, 2026-10-08 (chats wait for her reply) · lines guess |
| fix from the false-line sweep | sweep A4-09 (2026-10-08) |
| card goals are the step's real requirements | LO's play note, 2026-10-08 · sweep K8 and its 38 more cards |
