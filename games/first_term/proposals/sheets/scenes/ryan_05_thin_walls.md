# [REVIEW] Scene — ryan_05_thin_walls

> A draft for LO to place. Written 2026-10-08. **The batch 5 voice sample, in full:** every screen written by
> `v2-prose` from a spec, measured with `gates.py --beat`, pasted here. LO picked this step.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 5 (Ryan A 6) |
| where · when | her bed, `home_ella_room` · Friday 22:00–00:00, seen from his room |
| gate | Corruption 20 · Exhibitionism 40 · his Want 40 · the boost off |
| want (test 1) | his hand on her ankle while he lied to Kayla (step 4) |
| next step (test 2) | her first explicit act at home, and he hears it |
| hook (test 3) | Kayla in the hall at dawn; one bathroom (step 6) |
| what she wears here (test 8) | not named: the sheet only |
| her voice | stage 2, "warming up": shocked, honest, then she does it |
| the crude-word ceiling | Ryan's middle column: ass, tits, cock, wet (LO, 2026-10-08: middle = stage 3) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `wall` | the headboard through the wall; Kayla; she can't stop listening | no | "Listen." → `listen` · "Put your headphones in." → parked | none |
| `listen` | she listens on purpose; her body answers | yes (3 words) | "Touch yourself." → `act` · "Roll over. Sleep." → parked | none |
| `act` | her fingers, his rhythm; she comes; his headboard stops dead | yes (9 words) | "Lie still." → `after` | corruption add +1 · Ryan's Want add +10 |
| `after` | silence; "...@player.nickname?" through the wall; she doesn't answer | no | "Sleep." → `hall` · "Knock back twice." locked: "Needs Bold" | `ryan_heard_her` set · `ryan_step` set 5 |
| `hall` | Saturday dawn: Kayla in his T-shirt: "You must be @player.nickname." | no | "Take the shower." → the bathroom, Sat 08:00 | energy set 100 (a night's sleep, guess) |

**The parked nos** ("Put your headphones in.", "Roll over. Sleep."): the step comes back next Friday
(`retry_after_days = 7`, guess). Nothing else moves.

## The screens, written

**`wall`** · 97 words · explicit words 1 (moan) · median sentence 7 · not explicit

> Thump. Thump. Thump. Ryan's headboard hits the wall a foot from your pillow. Kayla moans through the plaster, high and breathless. Then Ryan's voice, low: "Quiet. They'll hear." She doesn't get quiet. The knocking gets faster. You knew Kayla sneaks in on Fridays. You read her text on his phone. Knowing it and hearing it are not the same thing. Your face is hot. You pull the sheet up to your chin, but you don't cover your ears. *Turn over. Go to sleep.* Kayla gasps his name. You lie still and listen to every second of it.

**`listen`** · 105 words · explicit words 3 (clit, moan, nipple) · median sentence 6 · registers as explicit · Ryan's middle column (SP2 crude table): ass, tits, cock, wet · not cunt, fuck, cum, pussy

> The headboard thuds against the wall. Thud. Thud. Faster. You lie still and listen on purpose. Kayla moans, high and broken. "Harder. Don't stop. Right there, Ryan, right there." Ryan groans her name, low and rough. That's your brother's voice. Your nipples go tight against the sheet. Your breath comes short. Heat pools between your thighs until you're wet. *That's Ryan. You should be grossed out.* You aren't, but that scares you less than how badly you want to hear more. The headboard speeds up. Kayla cries out. Your hand slides down your stomach and stops an inch above your clit, aching to keep going.

**`act`** · 133 words · explicit words 9 (ass, clit, cock, moan, nipple, thrust, tits) · median sentence 8 · act rungs: hands, vaginal · Ryan's middle column (SP2 crude table): ass, tits, cock, wet · not cunt, fuck, cum, pussy

> Your hand slides down under the sheet. Your fingers find your clit, and you're already wet. On the other side of the wall, Ryan's headboard knocks, slow and hard. You rub in time with it. Kayla moans his name. You picture his cock sinking into her, his hands full of her ass, her tits bouncing with every thrust. Your other hand finds a nipple and pinches. Your hips lift off the mattress. The headboard speeds up, so you speed up. Your thighs start to shake. Then Ryan groans through the wall, low and rough, and that does it. You come hard, biting the pillow, but a moan still gets out of you. The headboard stops dead, while your thighs clamp tight around your hand and your clit is still throbbing under your fingers.

*The last sentence:* the stopped headboard, her thighs, her clit. On the body; not a pivot. "He heard" is shown,
not said, and the meaning goes to the next screen.

**`after`** · 76 words · explicit words 0 · median sentence 6 · the meaning beat

> The headboard doesn't start again. Through the wall, Kayla mumbles, "What? ... Nothing?" "Nothing," Ryan says. "Go to sleep." The bed creaks. Then, low, right against the wall by your head: "...@player.nickname?" You don't answer. You lie still, your heart slamming, the pillow damp where you bit it. *He heard all of it. Every second. And you're not sorry.* Kayla is still here in the morning. There's one bathroom, and all three of you need it.

**`hall`** · 97 words · explicit words 1 (ass) · median sentence 9 · not explicit

> Ryan's door clicks open and a girl slips out barefoot. Kayla. She's in one of his T-shirts, and it barely covers her ass. She's sneaking for the bathroom before Mom is up. She sees you and stops. She looks a beat too long, and she's smiling. "You must be @player.nickname." *She heard you. Or he told her.* "I am," you say. "Thin walls." Kayla laughs, low, like she just won something. "Shower's free. Go on. I'm not going anywhere." Behind her, Ryan stands frozen in his doorway, red to the ears, and he can't look at you.

One line changed after `v2-prose`: her thought was first person; it is now *"She heard you. Or he told her."*
Re-measured: 97 words.

## Truth checks

| line | what backs it |
|---|---|
| "You read her text on his phone." | step 2 sets `knows_about_kayla`; the counter needs it |
| "Kayla sneaks in on Fridays" | the step fires Friday only |
| "I heard you last night" (step 6) | `ryan_heard_her`, set here |
| no garment of hers is named | nothing needs backing |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene: the wall, her hand, Kayla in the hall | the arc ideas, Ryan A 6 (heat 10-06) |
| touching herself from Curious | LO, 2026-10-08 (question 13) |
| this step as the voice sample | LO, 2026-10-08 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| the middle column for stage 3 | LO, 2026-10-08 (question 28) |
| retry in 7 days, energy on waking | guess |
