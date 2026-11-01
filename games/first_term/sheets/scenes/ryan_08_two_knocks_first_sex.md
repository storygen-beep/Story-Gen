# [REVIEW]] Scene — ryan_08_two_knocks_first_sex

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **New 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113). From Ryan's signed release-1 ladder
> (`sheets/people/npc_ryan.md`, step 8, the top step). Replaces `ryan_08_two_knocks` (cut): the talk's terms move here,
> after the sex. The explicit screens are written by `v2-prose` and measured: below.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 8 (new, top step) |
| where · when | his room, `home_ryan_room` · any night but Friday, 22:00–00:00, after two knocks |
| gate | Corruption 60 (was 40: DECISIONS 124) · his Want 70 · `ryan_step` eq 7 · not Friday · the boost off |
| want (test 1) | his phone face-down when she knocks (step 7's after) |
| next step (test 2) | first sex, on a night that isn't Kayla's; his headboard hits the wall she listened through |
| hook (test 3) | the terms; the step-8 repeat; step 9 shown locked, "Further. (Needs Corruption 60)" |
| who notices | Laura, across the hall: her light on (`laura_knows_ryan`, from "Laura opens the door") |
| what she risks | Laura hearing the headboard |
| what she wears here (test 8) | not named; undressed on screen |
| her voice | stage 3 (Bold) |
| the crude-word ceiling | Ryan's whole late column, cunt, fuck, cum ("Fuck me.") · confirmed by LO 2026-11-01 ("Continue") |
| her_line_low · her_line_high (rule 7) | low: "This is Ryan. You should go." · high: "You want him to hear Kayla on the phone while you do this." (worded for this screen with the prose) |
| mixed act? | no: behind his door. Corruption only |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `knocks` | two knocks, late; his phone is face-down on the desk | no | "Fuck me." → `bed` · "Not tonight." → the hall (parked) | none |
| `bed` | he pulls her onto him; his headboard starts to hit the wall, her wall | yes | "Ride him." → `wall` | none |
| `wall` | the headboard against the wall; across the hall Laura's light comes on under her door; they don't stop | yes | "Inside me." → `inside` · "On me." → `on` | none |
| `inside` | he comes inside her | yes | "Lie there." → `terms` | none |
| `on` | he pulls out and comes on her | yes | "Lie there." → `terms` | none |
| `terms` | after: what this is. The Jake line stays: "And Jake? The guy who walks you to the door?" | no | "Keep Kayla. I'm the secret." → the hall · "Mom finds out when I want." → the hall · "You're my brother, that's all. (ends his path)" → the hall | Ryan's Want add +5 · `ryan_step` set 8 · the term picked sets `ryan_terms_secret` / `ryan_terms_mine` / `ryan_path_closed`  |

**The parked no** (confirmed by LO 2026-11-01 ("Continue")): "Not tonight." The step comes back the next night that isn't Friday.

**His move:** he pulls her onto him. **Does it finish:** yes, inside her or on her, her pick.

**After:** the step-8 repeat opens (`ryan_hot_repeatables.md`, the last row); step 9 shows locked on his card.

## The explicit screens, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Fixes after: Ryan's name for her is `@player.nickname`, not "Ella". The tool lists `vaginal` where his spoken "fuck" or a "thrust" matches its regex; no vaginal act is on these screens (a known false reading of `gates.py`'s rung check).

**`bed`** · 137 words · explicit words 7 · median sentence 10 · act rungs: vaginal · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> He grabs your wrist and pulls you down onto him. His bed creaks under both of you. You drag his shirt up over his head. He shoves your clothes off you and drops them on the floor. His cock lies hard against your belly, thick and hot. "Fuck, @player.nickname," he breathes. You lift up, take his cock in your fist and line it up with your cunt. You're so wet it slides right in. You sink down slowly until he's all the way inside you. *Oh God, he's big.* His hands grip your ass and pull you down harder. Your tits bounce as you start to ride him. His headboard knocks the wall. It's the wall you listened through when Kayla was here. You ride his cock faster, and the headboard bangs in time with every stroke.

*The last sentence:* riding him, the headboard in time. On the body.

**`wall`** · 118 words · explicit words 9 · median sentence 12 · act rungs: hands, vaginal · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> You ride him harder, and his headboard bangs your wall every time you drop onto his cock. Across the hall, a line of light comes on under Laura's door. You both see it. You freeze on him, his cock buried to the root in your cunt. Ryan grabs your hips and fucks up into you hard. You clap a hand over your own mouth. *She's awake. Don't you dare stop.* Your tits bounce with every thrust, and the headboard keeps hitting. "Fuck," he breathes against your fingers when you cover his mouth too. He drags you down onto him, deep. Your wet cunt clenches around his cock on every stroke, and you feel him swell inside you, close.

*The last sentence:* her cunt clenching, him swelling, close. On the body; the finish is her pick.

**`inside`** · 130 words · explicit words 10 · median sentence 12 · act rungs: hands, vaginal, finish · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> His headboard bangs your wall every time you drop. His hands lock on your hips and he takes the pace from you. He pulls you down hard onto his cock and holds you there. "@player.nickname. I'm close." "Inside," you say. "Do it." He drives up once more and his cock jerks deep in your cunt. You feel every pulse. Hot cum floods you, and he keeps grinding you down onto it. *That's him. All of it.* Your thighs start to shake. Your cunt clamps around him and you come loud, nails in his chest. He fucks you through it in short, hard strokes. Cum slides out around his cock and runs wet down your thighs. Your tits heave. He holds your hips down until his cock stops twitching inside you.

*The last sentence:* his cock twitching inside her. On the body; the talk is the next screen.

**`on`** · 119 words · explicit words 9 · median sentence 6 · act rungs: hands, vaginal, finish · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> "Close," Ryan grunts. His hands dig into your ass. The headboard bangs your wall one more time. You lift off him. His cock slides out of your cunt, wet and shining, and slaps down on his stomach. You wrap your hand around it. It's slick with you and hot. "Fuck. Don't stop." You pump him fast, root to tip, and his hips jerk off the mattress. *Give it to me.* He swears through his teeth. The first rope of cum hits your stomach. The next splashes across your tits. You keep stroking and he keeps spurting until it drips down your chest. You're panting. His cock twitches in your fist. His cum runs down your belly toward your cunt.

*The last sentence:* his cum running down her belly. On the body; the talk is the next screen.

## Truth checks

| line | what backs it |
|---|---|
| "the wall she listened through" | `ryan_heard_her` (step 5) |
| Laura's light on | `laura_knows_ryan` (the event after step 4); without it, the line names only her closed door |
| "And Jake?" | shown only when `jake_met` |
| not Friday | Kayla's night; the gate's weekday |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the step, the columns, the terms, her pick | `proposals/RYAN_R1_LADDER.md`, signed by LO 2026-11-01 (DECISIONS 100) |
| first sex in release 1 | LO, 2026-11-01 (DECISIONS 100) |
| the whole late column | proposed in the same file; confirmed by LO 2026-11-01 ("Continue") |
| the parked no, the flag names | proposed here, confirmed by LO 2026-11-01 ("Continue") |
