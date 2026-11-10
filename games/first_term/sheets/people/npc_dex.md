# [READY] Person — Dex, the trainer
> Changed 2026-11-10 (DECISIONS 227): his men's-showers variant moves into the shared shower room, after close. Re-signed by LO 2026-11-10 ("Sign them").
> Changed 2026-11-10 (DECISIONS 226): his repeat gets one more variant: the men's locker room when it's empty. Re-signed by LO 2026-11-10 ("Sign them").

> New 2026-11-10 (DECISIONS 225). Signed by LO 2026-11-10 ("Sign them"). Id `npc_dex`.
> LO, 2026-11-10: "Gym trainer too." · on who: "you can decide one" · on this pitch: "Yes, go ahead".

| row | answer |
|---|---|
| age | 34 |
| role | personal trainer at the gym (`gym.md`) |
| look | big and tanned, shaved head, tattooed forearms, a tight black staff tee with TRAINER on the back |
| what she wants from him | at first, to get fit for nothing; then his hands, and to be the girl he picks |
| what he visibly wants, each visit | his hands on her, and to see how far she lets them go |
| what he keeps | step counter `dex_step` (0–5) + `dex_sessions` (hidden, sessions since his last step) + memory flags |
| where he sleeps | offscreen |
| what he calls her | "@player" at step 1 · "@player.nickname" from step 2 |
| met | her first visit to the gym, Mon–Sat 10:00–20:00 (his step 1) |
| his line: track pants and a tee | "You came to work. I like that. Let's see what's under it." |
| his line: leggings | His eyes go to her ass in the mirror and stay. "Those'll show me if your form's right." |
| his line: the sports bra alone | "Now I can see your core. Good." He looks at her tits, not her core. |
| his line: tiny gym shorts | "Those are going to ride up on every squat. Don't fix them." |
| his line: sheer leggings | "You know I can see everything through those." "Yes." "Good. Squats." |

## Crude words, by stage (SP2: "on their sheets")

| column | words |
|---|---|
| early (stages 1–2) | ass, tits |
| middle (stage 3) | ass, tits, cock |
| late (stages 4–5) | cock, cunt, fuck, cum |

Proposed: a ceiling, never a floor. LO confirms.

## Schedule grid

| place | days | from | to | why he is there |
|---|---|---|---|---|
| `gym_floor` | Mon–Sat | 10:00 | 20:00 | his shift: the desk and his clients |
| `gym_sauna` | Mon–Sat | 20:00 | 20:45 | his step 4 only: he finishes his shift in the sauna (`dex_step` eq 3) |
| `gym_locker` | Mon–Sat | 21:00 | 22:00 | after closing, his step 5 and the repeat: he keeps the key (`dex_step` gte 4) |

Sunday he is off. The gym is open; he isn't there.

## Ladder — one guidance card per step

Every step opens from his portrait on the gym floor or in the room he is in (DECISIONS 224), never as its own link.
Stages: Corruption 20 Curious, 40 Bold, 60 Hungry · Exhibitionism 20 Daring, 40 Showing, 60 Watched.

| n | canvas | where | when | gate | raises | the no | her line low · high | guidance card line |
|---|---|---|---|---|---|---|---|---|
| 1 | `dex_01_free_session` | `gym_floor` | Mon–Sat 10:00–20:00 | a pass active · gym clothes · `dex_step` eq 0 | exhibitionism add +1, cap 19 · `dex_step` 1 | "I'm fine on my own." (parked: he asks again next visit) | "He's just doing his job." · "Let him look. That's what he's paid for." | The gym, any day but Sunday, 10 to 8: the trainer at the desk has been watching you in the mirror. |
| 2 | `dex_02_the_mats` | `gym_floor` | Mon–Sat 10:00–20:00 | `dex_step` eq 1 · `dex_sessions` gte 2 · Curious (Corruption 20) | corruption add +1, cap 39 · `dex_step` 2 | "Just the weights today." (parked) | "It's a stretch. People stretch." · "His hand's on your inner thigh and you want it higher." | Book a session with Dex: $15, and his hands on the mats. |
| 3 | `dex_03_another_way` | `gym_locker` | Mon–Sat 10:00–20:00 | `dex_step` eq 2 · `dex_sessions` gte 3 · Bold (Corruption 40) | corruption add +1, cap 59 · `dex_step` 3 · `dex_paid_another_way` | "I'll pay the fifteen." (parked: she pays, he's still waiting) | "Just this once, for fifteen dollars." · "You'd have done it for free." | Dex says keep your money. The locker room, between his clients. |
| 4 | `dex_04_the_sauna` | `gym_sauna` | Mon–Sat 20:00–20:45 | `dex_step` eq 3 · `dex_sessions` gte 3 · Hungry (Corruption 60) | corruption add +1, cap 79 · `dex_step` 4 | "Not here. Someone could come in." (parked) | — (Hungry only) · "The regulars left ten minutes ago. Probably." | The sauna, just before close: Dex ends his shift in there. |
| 5 | `dex_05_after_hours` (top step) | `gym_locker` | Mon–Sat 21:00–22:00 | `dex_step` eq 4 · Hungry (Corruption 60) | corruption add +1, cap 79 · `dex_step` 5 · `dex_first_time` | "Not tonight, Dex." (parked) | — (Hungry only) · "The whole gym dark, and him fucking you on the bench where you change." | After closing, Dex has the key: the locker room, 9 to 10. |
| hot repeatable | `dex_session` (stage 1–2), `dex_after_hours` (stage 3) | `gym_floor` · `gym_locker` | his hours | step 1 · step 5 | `dex_sessions` +1 · exhibitionism or corruption +1 to the step's cap | — | — | "Book a session with Dex ($15)" in his portrait · "Stay after close" in his portrait, from step 5 |

**Paying "another way".** Every session costs $15, or, from step 3, "Keep your money." swaps the $15 for his hand down
her leggings in the locker room (corruption +1, cap 59). She can always pay instead. The swap is his move, not a money
wall: she earns enough at the café that a money gate would almost never fire (`money_pressure.md`).

**Each step, by the seven columns** (`sheets/TASTE_COLUMNS.md`):

| n | the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|---|
| 1 | *hands that happen to her · stage 1* — "Your form's off." His hands on her hips at the squat rack, his crotch an inch from her ass, in front of the mirror wall | the floor | being looked at | she stays in the squat | he pulls her hips back into him | yes | she can book sessions; his "@player.nickname" |
| 2 | *touch she lets go on · stage 2, Curious* — the stretch on the mats: her leg on his shoulder, his hand on her inner thigh, higher every rep | two regulars on the bench | them seeing where his hand is | she doesn't move his hand | his thumb presses the seam of her leggings | yes | "Same time next week?"; sessions count up |
| 3 | *her hand on him for pay · stage 3, Bold* — between clients, the locker room: "Keep your money." His cock out, her hand on it, she gets him off | a member could walk in; the door has no lock | the walk-in | "Okay. Keep it." | he puts her hand on him | **yes** | `dex_paid_another_way`; "another way" on every session |
| 4 | *his mouth and hands in public heat · stage 4, Hungry* — just before close, the sauna: he comes in, the regulars leave, he opens her towel and gets his fingers in her cunt until she comes | the last regular, leaving; the glass door | someone coming back for a bag | she opens her knees | he opens her towel | **yes**, she comes | he gives her a key time: "Nine. Locker room." |
| 5 | *sex · stage 5, Hungry* — after closing, the dark locker room: he bends her over the bench where she changes and fucks her, cum on her ass | nobody, then the cleaner's cart in the hall | the cleaner | she bends over the bench | "Hands on the bench." | **yes** | `dex_first_time`; "Stay after close" becomes his repeat |

### Leak and promise

| n | the leak: his want, shown before | the promise: the line it ends on |
|---|---|---|
| 1 | from the desk, his eyes on her ass in the mirror, every set | "First one's free. After that you pay." |
| 2 | "You're tight here." His hand flat on her inner thigh. | "Fifteen next time. Or we work something out." |
| 3 | "Short this week?" He hasn't looked at her card. | "Keep your money. Every time." |
| 4 | "I finish in the sauna. Most nights it's empty by eight." | "Nine o'clock. I've got the key." |
| 5 | the key on his finger | "Same time Thursday." |

**Final no:** "Get someone else to train me." (ends his path), offered only after this release. In release 1 his nos
are parked.

## Ladder rules — ticked before any step is written

| rule | pass · fail | the one line of evidence |
|---|---|---|
| 1 · every step adds a new witness, risk or kind of yes | pass | the floor → two regulars → a door with no lock → the sauna's glass → the dark gym |
| 2 · the top step is a payoff, finished on the body | pass | step 5, he fucks her over the bench, cum on her ass |
| 3 · one cut-off per ladder | pass | none |
| 4 · he moves at least every other step | pass | he moves on every step (column "his move") |
| 5 · his meter is the lock: 2–10 hot visits between steps | pass | `dex_sessions` gte 2, then 3, then 3: paid sessions between steps |
| 6 · one hot repeatable per stage, written in full | pass | the session (stages 1–2, by her clothes), "another way" (stage 3), after hours (stage 4–5) |
| 7 · a low line and a high line per step | pass | the column above; steps 4–5 are Hungry only, so one line |
| 8 · something still happens after the top step | pass | "Stay after close", his repeat, and the sessions go on |

## Jake and Dex (the rival)

Tue and Thu 15:00–17:00 both are on the floor.

| who sees | when | his line |
|---|---|---|
| Jake | Dex is past step 1, she's in a session | "That trainer's hands are all over you." · from Dex step 3: "Everybody on the team knows what he's like." |
| Dex | Jake's step 2 or later, Jake's team in | "Your boyfriend's watching. Lift." |

## Phone thread

| thread | cause flag | delay | window | booking | loop |
|---|---|---|---|---|---|
| `dex` | `dex_step` 4 (the sauna) | same night | 20:45–21:00 | "Locker room. I'm still here." (the gym floor, 21:00) | after step 5: "Thursday?" every 3 days, 18:00–20:00 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| a trainer, Dex, 34 | LO, 2026-11-10 ("Gym trainer too"; "you can decide one"; "Yes, go ahead") |
| his hours, Mon–Sat 10:00–20:00 | guess (inside the gym's 06:00–21:00, LO 2026-11-10) |
| $15 a session, "another way" from step 3 | guess · `templates/cards/sex_for_pay.md` |
| the steps' meters and caps | `references/the-heat-ladder.md` stages · guess on which meter |
| Jake as his rival | the pitch LO took, 2026-11-10 |
| the crude words | guess, proposed; LO confirms |

## Built 2026-11-10 (DECISIONS 225): where the build differs from this sheet

- **After hours runs from the floor.** A closed room can't be entered, so step 5 opens on the gym floor 20:30–21:00
  ("I'm staying.") and the scene runs on past nine inside one canvas, then lets her out onto the street. His floor row
  runs 10:00–21:00 for it.
- **His repeat is "Go to the locker room with him."** in his portrait, Mon–Sat 10:00–21:00, once a day, from step 5
  (Hungry): between clients the locker-room door has no lock; from 20:30 he locks up. The gate `the loop is open
  enough hours` wants 18 hours a week, and 20:30–21:00 alone was 3.
- **Steps auto-fire** when ready, like every ladder step: step 1 meets him the first time she walks onto the floor
  checked in; step 4 when she's in the sauna 20:00–20:45.
- **A face in the sauna**: `hub_dex_sauna`, his line while his step-4 row has him there.
- **No phone thread yet.** The thread row above is not built this pass; his cards and his own lines say where and when
  ("Half eight. Stay when they lock up.").

## The men's locker room (2026-11-10, DECISIONS 226)

His repeat ("Go to the locker room with him.") gets one more variant, drawn from the same bag: he takes her into the
men's locker room when it's empty, and fucks her in the men's showers. Same gate, cap and once a day.

## The shared showers (2026-11-10, DECISIONS 227)

The men's-showers variant of his repeat moves into the gym's shared shower room: after close, the room empty, he
fucks her under the water. Same gate, cap and once a day.
