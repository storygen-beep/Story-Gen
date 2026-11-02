# [REVIEW] Scene — ryan_08_two_knocks_first_sex

> **Changed 2026-11-02, signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 127) (LO: "it should be like rise from normal, not jump straight to
> fucking", "cant we have more in the sex screens", "B, sheet it"). The step now rises from a normal talk through
> her doubt, a kiss and undressing, one piece at a time, with a no at each rung; the sex has three choices of
> her own (what first, how, and what to do when Laura's light comes on) and three finishes; her feeling after
> gets its own screen before his terms (`the-arc.md:640`, a first time: his want, her doubt, the act, her
> feeling after). Sections changed: the row table (hook, her voice), Branch map (rewritten), The explicit
> screens (which change, which are new), Truth checks. Gate, pay, terms and the repeat's trigger unchanged.

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
| her voice | stage 3 (Bold) at the door, her low line on `doubt`; stage 4 (Hungry) once she says "Stay." |
| the crude-word ceiling | Ryan's whole late column, cunt, fuck, cum ("Fuck me.") · confirmed by LO 2026-11-01 ("Continue") |
| her_line_low · her_line_high (rule 7) | low: "This is Ryan. You should go." · high: "You want him to hear Kayla on the phone while you do this." (worded for this screen with the prose) |
| mixed act? | no: behind his door. Corruption only |

## Branch map — one row per screen (S1)

The order: a normal talk, then her doubt, then the kiss, then clothes, then her pick of what first, then her pick
of how, then Laura's light, then the finish, then how she feels, then his terms. Every rung before the sex has a
no she can come back from (the parked no: "Not tonight." returns the step the next night that isn't Friday).

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `knocks` | two knocks, late; he opens on the first; his phone is face-down on the desk; "Kayla's at her mom's tonight." | no | "Come in." → `talk` · "Not tonight." → the hall (parked) | none |
| `talk` | normal and awkward: they sit on his bed, a foot apart; he tries a joke about the walls; neither says the kiss; he says "I meant it. The girlfriend thing." and doesn't move away | no | "So did I." → `doubt` | none |
| `doubt` | her low line, out loud in her head: *This is Ryan. You should go.* His knee touches hers. He's looking at her mouth (his want, on his body: H7) | no | "Stay." → `kiss` · "Go." → the hall (parked) | none |
| `kiss` | she kisses him; this time he kisses back and doesn't stop; his hand goes under her top, onto her bare back, then round to her tits through her bra; his cock hard against her thigh | yes (low) | "Let him." → `undress` · "Stop. Not tonight." → the hall (parked) | none |
| `undress` | one piece at a time: he pulls her top over her head and looks; she unhooks her bra herself; she pushes his shorts down; he peels her panties off, slow, and stares at her cunt; they're naked on his bed | yes | "Go down on him." → `suck` · "Let him taste you." → `lick` · "Get on him." → `ride` | none |
| `suck` | **new.** On her knees by his bed, his cock in her mouth; he's fighting to stay quiet, one hand in her hair; she stops before he comes | yes | "Ride him." → `ride` · "On your back." → `under` · "Against the wall." → `wall_back` | none |
| `lick` | **new.** On her back, his mouth on her cunt; her hand over her own mouth; she comes first, thighs round his head | yes | "Ride him." → `ride` · "On your back." → `under` · "Against the wall." → `wall_back` | none |
| `ride` | she sinks onto him and rides him; his headboard starts to hit her wall (today's `bed`, its undressing lines moved to `undress`) | yes | "Harder." → `light` | none |
| `under` | **new.** He's on top, slow, looking at her face; it's Ryan, and he says her name | yes | "Harder." → `light` | none |
| `wall_back` | **new.** From behind, her palms flat on the wall she listened through on step 5; she can feel the headboard's dents in the plaster | yes | "Harder." → `light` | none |
| `light` | across the hall, a line of light comes on under Laura's door; he's buried in her; they both see it (today's `wall`, rewritten to fit all three positions) | yes | "Keep going." → `keep` · "Freeze." → `freeze` | none |
| `keep` | **new.** He fucks her harder, his hand over her mouth; the bed or the wall knocks; Laura's light stays on | yes | "Inside me." → `inside` · "On me." → `on` · "In my mouth." → `mouth` | none |
| `freeze` | **new.** They hold still, him deep in her, hearts slamming, listening; the light goes off; he starts again, slow, so slow she's shaking | yes | "Inside me." → `inside` · "On me." → `on` · "In my mouth." → `mouth` | none |
| `inside` | he comes inside her (as written, one line on the knocking fitted to the position) | yes | "Lie there." → `after` | none |
| `on` | he pulls out and comes on her tits and stomach (as written, fitted to the position) | yes | "Lie there." → `after` | none |
| `mouth` | **new.** She gets off him, onto her knees, and he comes in her mouth; she swallows | yes | "Lie there." → `after` | none |
| `after` | **new.** Her feeling, its own beat: her head on her brother's chest, his cum on her or in her, his heart going; she isn't sorry, and that's the part that scares her | no | "Ask him." → `terms` | none |
| `terms` | as signed: "So what is this?"; the Jake line stays | no | as signed: the three terms + "Further. (Next release)" | as signed: Ryan's Want add +5 · `ryan_step` set 8 · the term flag |

**The nos:** "Not tonight." (`knocks`), "Go." (`doubt`), "Stop. Not tonight." (`kiss`). All three parked: the
step comes back the next night that isn't Friday (retry 1 day, as now).

**Her picks, as flags for later** (proposed): none set. The repeat's menu (below) opens by his Lust, not by what she
picked here, so a first pick is never a wrong pick.

**His move:** he kisses back, and he takes the pace on `keep`. **Does it finish:** yes, her pick of three.

**After:** the step-8 repeat opens with its menu (`ryan_hot_repeatables.md`, row 7, changed the same day); step 9
shows "(Next release)".

**Media slots (new, LO harvests):** `sex/ryan_08_kiss_t4`, `sex/ryan_08_undress_t4`, `sex/ryan_08_suck_t5`,
`sex/ryan_08_lick_t5`, `sex/ryan_08_under_t5`, `sex/ryan_08_wall_back_t5`, `sex/ryan_08_keep_t5`,
`sex/ryan_08_freeze_t5`, `sex/ryan_08_mouth_t5`. Kept: `ryan_08_bed_t5` (now `ride`), `ryan_08_wall_t5` (now
`light`), `ryan_08_inside_t5`, `ryan_08_on_t5`.

**Confirmed by LO 2026-11-02** ("Signed"): "In my mouth." as a finish (SP2 signs oral at Bold, `SP2_ladders.md:53`).

**Who writes what, after the sign:** `v2-prose` writes the explicit screens (new: `kiss`, `undress`, `suck`, `lick`,
`under`, `wall_back`, `keep`, `freeze`, `mouth`; rewritten: `ride`, `light`, `inside`, `on`), measured with
`gates.py --beat`. The talk screens (`knocks`, `talk`, `doubt`, `after`) are written in the build.

## The explicit screens, 2026-11-02 (DECISIONS 127)

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-02. Read by the build ahead of the 2026-11-01 screens below
(the first heading wins), which stay as the record. Fixes after: "asleep" cut from `suck` (Laura is awake 22:00–23:00);
`light` no longer has Ryan stop dead (the pause is the player's pick); `kiss` and `undress` name no garment
(gate "her clothes are backed": at night she may be in a sleep shirt, with no bra). Reader pass 2026-11-02: step 7 is
"Kayla can't know" (her hand, his phone), not the cut kiss, so `kiss` and `undress` follow it; Mark is downstairs with the
TV 22:00–02:00, so only Laura is across the hall; `light` has Ryan see the light (she may face the wall); `under`
pulls her up the bed (after `lick` she is already on her back). Every screen after `undress` fits all three
positions or none is named. The `vaginal` rung on some oral or hand screens is the known false reading of "fuck".

**`kiss`** · 119 words · explicit words 7 · median sentence 10

> You lean in and kiss him. You've had your hand on his cock and never once kissed him. He kisses you back, hard, and he doesn't stop. His mouth opens on yours. "@player.nickname," he breathes against your lips, and kisses you again. His hand slides up under your clothes and spreads flat on your bare back. His palm is hot. It drags slowly round your ribs, and then he cups your tits through the cloth. He squeezes. Your nipples go hard under his hand, and his thumb rubs one through it. You squirm closer on his bed. His cock is hard against your thigh through his shorts. *Don't stop. Not this time.* He grinds it into you, slow, and squeezes your tit again.

**`undress`** · 135 words · explicit words 8 · median sentence 11

> He tugs your clothes up over your head and drops them on the floor and looks at you. His eyes go straight to your tits. "Fuck," he whispers. Your bare tits are right there, nipples hard, and he can't stop staring. You hook your fingers in his shorts and push them down. His cock springs out, thick and hard, and slaps up against his stomach. *Not just your hand this time.* He lays you back on his bed. He peels the last of your clothes down your thighs, slow. Then he stares at your cunt. It's already wet, and he can see it. You're both naked on his bed now, his cock hard against your hip.

**`suck`** · 138 words · explicit words 7 · median sentence 8

> You slide off his bed onto your knees. Ryan sits on the edge, legs apart, his cock hard in front of your face. You wrap your fist round the base and lick the tip. He sucks in a breath through his teeth. You take him in your mouth. He's thick, and your lips stretch around him. "Fuck," he hisses, too loud, and bites his own fist. Laura's right across the hall. His other hand goes into your hair. He doesn't push, but he holds on while you bob slow on his cock, deeper each time. *Quiet, Ryan. Quiet.* Spit runs down his shaft into your fist. His thighs shake. His cock swells on your tongue. You pull off him with a wet pop, and his cock jerks, slick and hard, an inch from your lips.

**`lick`** · 129 words · explicit words 10 · median sentence 9

> He pushes you onto your back on his bed and spreads your thighs. Then he kneels between them and puts his mouth on your cunt. His tongue drags up through you, slow and flat. You slap a hand over your own mouth. Laura's right across the hall. He licks you again, then sucks your clit between his lips. Your hips jerk off the mattress. He grabs your ass and holds you down. *Don't make a sound.* His tongue works your clit fast now, and two fingers slide into your wet cunt. You moan into your palm. Your thighs start to shake. Then you come hard, and your thighs clamp tight round his head. He keeps licking your cunt through it while you buck against his mouth.

**`ride`** · 117 words · explicit words 9 · median sentence 11

> You push Ryan flat on his back and climb on. His cock stands up hard between your thighs, thick and hot. "Fuck, @player.nickname," he breathes. You take his cock in your fist and line it up with your cunt. You're so wet it slides right in. You sink down slowly until he's all the way inside you. *Oh God, he's big.* His hands grab your ass and pull you down harder. Your tits bounce as you start to ride him. His headboard knocks the wall. Your wall, the one you listened through when Kayla was here. You lean on his chest and ride his cock faster. The headboard bangs every time your cunt drops onto his cock.

**`under`** · 122 words · explicit words 8 · median sentence 11

> Ryan pulls you up the bed under him and settles between your thighs. The head of his cock presses against your cunt. He pushes in slow, an inch at a time, and watches your face the whole way. You're soaked, and he slides deep. He bottoms out and holds there. "@player.nickname," he says, low. Just your name, with his cock all the way inside you. He pulls almost out and fucks back in, slow and deep. His headboard taps your wall, soft. Tap. Tap. *It's Ryan.* Your tits brush his chest on every stroke. You wrap your legs round his ass and pull him in deeper. He groans into your neck and keeps it slow, grinding into you until your cunt squeezes his cock.

**`wall_back`** · 118 words · explicit words 9 · median sentence 8

> You kneel up on his bed, facing the wall, and put your palms flat on it. Your wall, the one you listened through. The plaster is rough under your hands. You can feel the dents his headboard made. Ryan kneels behind you and grabs your ass. His cock slides between your cheeks, then down to your cunt. He pushes in deep in one stroke. You gasp against the wall. "Fuck," he breathes. He pulls back and slams in again. Your tits sway with every thrust. His headboard knocks the plaster next to your hands. *Kayla was right here.* His fingers dig into your hips. He fucks you deep and slow, then faster, his balls slapping your wet cunt.

**`light`** · 122 words · explicit words 9 · median sentence 8

> "Harder," you gasp, and Ryan gives it to you. He fucks you so hard the bed shakes. The headboard bangs your wall on every stroke, loud. Across the hall, a line of light comes on under Laura's door. Ryan sees it. "Laura," he breathes. Ryan goes still for a second, his cock buried to the root in your cunt. Neither of you breathes. You clap a hand over your own mouth. *She's awake.* His cock throbs inside you. Your tits heave against your arm. Your wet cunt clenches around him on its own, and he swears through his teeth. His fingers dig into your ass. He's so deep you can feel him twitch. You squeeze his cock again, and his hips jerk once, deeper into your cunt.

**`keep`** · 131 words · explicit words 11 · median sentence 8

> Ryan doesn't stop. His hand clamps over your mouth and he fucks you harder. Deep, fast strokes. His cock slams into your cunt so hard you see stars. The wall bangs. It bangs again. Across the hall, the line of light stays on under Laura's door. You moan into his palm and he presses tighter. "Quiet," he hisses. "Fuck. Quiet." You can't be. You're so wet you can hear it, a slick slap of skin on every stroke. His fingers dig into your ass. Your tits shake with every thrust. *She can hear this.* He doesn't slow down. Your cunt tightens on him and his rhythm breaks, ragged and hard. His cock swells and jerks inside you, right at the edge, and he grits his teeth to hold back his cum.

**`freeze`** · 135 words · explicit words 10 · median sentence 5

> You both go still. His cock is buried deep in your cunt and neither of you moves. Your heart slams. You can feel his slamming too. You listen. Nothing across the hall. Just the line of light under Laura's door. Your cunt throbs around him and he grits his teeth. "Don't," he whispers. "Don't move." A minute. Longer. Then the light goes off. Dark under her door. Ryan breathes out. He starts again, slow. He pulls almost all the way out, then sinks back in, inch by inch. It's so slow you're shaking. *Fuck. Fuck, fuck.* You're dripping wet around him. Your tits ache. He does it again, slower, and his cock drags along every inch of you. Your thighs tremble and your cunt clenches on him, desperate, and he still won't fuck you faster.

**`inside`** · 125 words · explicit words 11 · median sentence 9

> He's close. You can feel it in how hard he's fucking you. His hand grips your hip and he takes the pace from you. The wall bangs, fast. "@player.nickname. I'm close." "Inside," you say. "Do it." He slams deep once more and holds there. His cock jerks in your cunt. You feel every pulse. Hot cum floods you, and he keeps grinding into you through it. *That's him. All of it.* Your thighs start to shake. Your cunt clamps around his cock and you come hard, a sound you can't swallow. He fucks you through it in short, hard strokes. Cum leaks out around his cock and runs wet down your thighs. Your tits heave. He stays buried in you until his cock stops twitching.

**`on`** · 121 words · explicit words 11 · median sentence 8

> "Close," Ryan grunts. His fingers dig into your ass. The wall bangs one more time. He pulls out. His cock slides out of your cunt, wet and shining with you. You end up on your back on his sheets, panting. He kneels over you, his fist on his cock. "Fuck. Don't move." You wrap your hand over his and pump with him, root to tip. *Give it to me.* He swears through his teeth. The first rope of cum hits your stomach. The next splashes across your tits. He keeps stroking and keeps spurting until it drips down your chest. Your nipples are slick with it. His cock twitches in your fist. His cum runs down your belly toward your cunt.

**`mouth`** · 129 words · explicit words 12 · median sentence 7

> "I'm close," he grunts. "Fuck, @player.nickname." You pull off his cock. It slips free, wet and shining with your cunt. You get on your knees on the floor by his bed. He stands over you, breathing hard. You take him in your fist and open your mouth. You suck the head of his cock and pump him hard, root to tip. You taste yourself on him. His hand fists in your hair. *Don't you dare stop.* His hips jerk. His cock swells on your tongue and he comes, hot cum flooding your mouth. Another pulse. Another. You keep sucking through every one. You swallow it all, and cum still drips onto your tits. You lick the last of it off the head while his cock twitches against your lips.

## The explicit screens, written (signed 2026-11-01; `bed` and `wall` are rewritten after the 11-02 sign, see the branch map)

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
| "the wall she listened through" on `wall_back` | `ryan_heard_her` (step 5 comes before step 8 on every save) |
| Laura's light on `light`, `keep`, `freeze` | a light coming on under her door claims nothing about what she knows, so it needs no flag; Laura is in her room Sun–Thu from 22:00 on her row. (The older row above, "without it, the line names only her closed door", was never built and is superseded.) |
| "Last time. With Kayla calling." on `talk` | step 7, `ryan_07_kayla_cant_know` (her hand on him while Kayla called), on every save that reaches step 8 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the step, the columns, the terms, her pick | `proposals/RYAN_R1_LADDER.md`, signed by LO 2026-11-01 (DECISIONS 100) |
| first sex in release 1 | LO, 2026-11-01 (DECISIONS 100) |
| the whole late column | proposed in the same file; confirmed by LO 2026-11-01 ("Continue") |
| the parked no, the flag names | proposed here, confirmed by LO 2026-11-01 ("Continue") |
