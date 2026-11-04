# [REVIEW] Scene — hale_thursday_session

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–117). Hale's hot repeatable, from his signed release-1 ladder
> (`sheets/people/npc_hale.md`, "His hot repeatable"). Reworks the built canvas `hale_thursdays` (its sheet `hale_05`
> is cut). Six pool entries written by `v2-prose` and measured; the other lines are mine.

| row | answer |
|---|---|
| system · place | Hale · his office, `hale_office` |
| want | he locks the door; the photo is already face-down |
| next step | "Same time next week." Nothing past this step this release |
| hook | his quest card: "Hale, further. (Next release)" |
| where · when | his office · Thursday, starts 18:30-19:05, once a day |
| gate | his step 4 · Corruption 40 · Exhibitionism 40 · `touch_high` at Corruption 60 |
| two tiers | `touch_low` (Corruption under 60): over her clothes, she says what she feels · `touch_high` (Corruption 60) |
| pays | each session: Psychology grade +2 · Corruption +1 (cap 59, or 79 high) · Exhibitionism +1 (cap 59) |
| the three answers | every session: "Let him." · "This isn't coaching." (`grade_psych` add −1) · Run. (`grade_psych` add −2). Each no costs only grade |
| Claire in the parking lot | "Let him." rolls Claire's Thursday 1-4; on 1 his phone ends it, grade +2 |
| the pools | each tier is a `block_pool`, three entries, `memory = "seen"`, `seen_weight = 0` (the shuffle bag, DECISIONS 112) |
| the crude-word ceiling | Hale's middle column (tits, nipples, cock: his, only hard under his trousers) with plain anatomy beside it (ass, thighs, wet, clit), as Ryan's signed sheets (DECISIONS 114) · no fuck, cum, pussy, cunt (his late column is not used: it goes no further) · the same as his step 4 |
| truth | weekly: no "first time", no "again", no counting, no history |
| her voice | `touch_low` stage 2 · `touch_high` stage 3 (her high line sits in B a) |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`hale_thursdays`** — Dr. Hale's Office · Thu 18:30-19:05 · needs Hale's step = 4 · Corruption 40+ · Exhibitionism 40+ · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | Dr. Hale's office door is unlocked. | no | "Let him." → `roll` | Claire's Thursday rolls 1-4 · costs Energy 10 |
| | | | "This isn't coaching." → `isnt` | Psychology grade -1 |
| | | | "Run." → `run` | Psychology grade -2 |
| `roll` | He looks you over across the desk. | no | "Go on." (Claire's Thursday = 1) → `claire_car` | — |
| | | | "Go on." (Claire's Thursday 2+ · Corruption under 60) → `touch_low` | Hygiene -10 |
| | | | "Go on." (Claire's Thursday 2+ · Corruption 60+) → `touch_high` | Hygiene -10 |
| `touch_low` | Dr. Hale stands behind your chair. | yes | "Same time next week." → `end` | Psychology grade +2 · Corruption +1 (cap 59) · Exhibitionism +1 (cap 59) |
| `touch_high` | Dr. Hale says it like he is reading a page number. | yes | "Same time next week." → `end` | Psychology grade +2 · Corruption +1 (cap 79) · Exhibitionism +1 (cap 59) |
| `claire_car` | His phone buzzes on the desk before he's touched you. | no | "Next Thursday." → Faculty Floor | Psychology grade +2 · `hale_thursday_booked` cleared |
| `end` | He looks at the clock, and straightens his tie, and unlocks the door. | no | "Thursday." → Faculty Floor | `hale_thursday_booked` cleared |
| `isnt` | He turns the photo face-up and doesn't look at you while you go. | no | "Leave him to his photo." → Faculty Floor | `hale_thursday_booked` cleared |
| `run` | You're out of the door before he's out of his chair. | no | "Keep walking." → Faculty Floor | `hale_thursday_booked` cleared |

## The pools, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Shared brief: he leads, touches, nothing of his comes out, no garment of hers named.

In a one-piece the build swaps "your top" for the garment she has on: "your dress" in the blue dress or Zoe's party dress, "your uniform" in either café uniform (pass 4 reader, 2026-11-04: the uniforms sit in the dress slot, so there is no top).

### `touch_low` (Curious and Daring)

**A a** · 131 words · explicit words 5 · median sentence 10 · act rungs: touch, hands

> Dr. Hale stands behind your chair. His hands settle on your shoulders, warm and heavy. "Tell me what you feel, @player." "Your hands," you say. "Be specific." His hands slide down over your top and close on your tits. "You're squeezing my tits," you say, and your voice shakes. His thumbs find your nipples through the cloth and circle them slowly. They go hard under his touch. "My nipples are hard." "Good. Go on." He rolls them between finger and thumb until you gasp. "I feel it between my thighs." "Be specific." "I'm wet." His hands move down your sides to your hips. He pulls you back against the chair and holds you there. Your thighs squeeze together. His thumbs dig into your hips, and your nipples ache against your top.

**A b** · 130 words · explicit words 6 · median sentence 9 · act rungs: none named (over her clothes)

> "Stand there," Dr. Hale says, and he points at the carpet in front of his desk. He stays in his chair. He takes you by the hips and pulls you in between his knees. His hands slide round to your ass. He squeezes it hard, both cheeks, through your clothes. "Tell me what you feel." "Your hands on my ass," you say. "I feel hot. I feel wet." He nods, because that is the right answer. His palms move up your sides, slowly, over your ribs. Then he cups your tits through your top and weighs them. His thumbs find your nipples and press. "And now?" Your breath catches. Your nipples go hard under his thumbs. Your thighs squeeze together. Your hips push forward, so your tits fill his hands.

**A c** · 128 words · explicit words 5 · median sentence 8 · act rungs: touch

> You sit on the corner of his desk. Dr. Hale stands in front of you, close enough that your knees touch his trousers. One hand lies flat on your thigh. The other covers your tit through your top. "Where is the heat, @player?" His voice stays calm, like he is reading you a test. "Between my thighs," you say out loud. His hand slides up your thigh while you say it. It stops an inch short of your clit. His thumb presses your nipple through your clothes. "And here?" "My nipples. They're hard." They are, both of them. You are wet now, and your thighs squeeze his wrist. Your hips push forward, but his hand does not move. It stays flat and warm, one inch from your clit.

### `touch_high` (Bold and Showing)

**B a** · 138 words · explicit words 7 · median sentence 9 · act rungs: touch, hands

> "Top off, @player." Dr. Hale says it like he is reading a page number. You pull your top over your head and drop it on the chair. Your tits are bare in the cold office, and your nipples go hard. His hand cups your left tit. He pinches the nipple until you gasp. You want to know what he'd do next. He sits back instead, with a notepad and a pen. "Touch yourself. Tell me what you feel." You slide your hand inside your clothes. Your fingers find your clit, and you are wet. "It's hot," you say, rubbing. "It's swollen. I want your hand there." He writes it down. His cock is hard under his trousers, and he leaves it alone. You rub your clit faster, your thighs shaking, your hips pushing up into your own fingers.

**B b** · 129 words · explicit words 5 · median sentence 6 · act rungs: hands

> You lie back on his desk with your top off and your tits bare. Dr. Hale stands over you, calm. His hand slides inside your clothes and rests flat on your belly. Then it moves down. Two fingers find your clit. He rubs it slowly, like he is taking a measurement. "Describe it, @player. Precisely." "It's hot," you say. "Small circles. It aches." You stop to breathe, and his hand stops with you. "Keep talking." "My nipples are hard. My thighs are shaking." His fingers move the moment you speak, slow and exact. You are wet on them. He spreads it over your clit. "More detail." "It's swollen," you gasp. "Please don't stop." Your hips lift off the desk into his hand. His wet fingers keep circling your clit.

**B c** · 138 words · explicit words 6 · median sentence 9 · act rungs: hands

> You sit in his chair with your top off and your tits bare. Your knees are wide apart. Dr. Hale stands at the window with his back to the parking lot, taking notes. Your hand is down inside your clothes, two fingers on your clit. You are so wet he can hear it. "Slower," he says. You slow down, and your thighs shake. "Now tell me." "I'm close," you say. "I'm so close it hurts." He writes that down. Then he crosses the room and pinches your nipple once, hard. You gasp and your hips jerk off the seat. His cock is hard under his trousers, right at your shoulder. He goes back to the window and his notes. Your fingers keep circling your clit, slow, the way he said. Your nipple throbs, and your thighs stay open.

Every last sentence is on her body (her nipples, her hips, his hand an inch from her clit, his fingers on her clit, her
thighs open). None of them has her come; the session stops at touching (LO: "things doesn't go beyond").

## The other screens (mine, signed by LO 2026-11-01)

**`door`:** "His office door is unlocked. He locks it behind you without a word. The photo is already face-down." · Dr. Hale: "Twenty minutes, @player."
**`claire_car`:** "His phone buzzes on the desk before he's touched you. He reads it and his face goes flat." · Dr. Hale: "She's early. She's in the parking lot." · "He unlocks the door and holds it open." · Dr. Hale: "Next Thursday." · "From the corridor window you can see a car with its engine running."
**`end`:** "He looks at the clock, and straightens his tie, and unlocks the door." · Dr. Hale: "Thursday." · "Down in the parking lot his wife's car isn't there yet."
**`isnt`:** @player: "This isn't coaching." · Dr. Hale: "Then you'll stay at a C." · "He turns the photo face-up and doesn't look at you while you go."
**`run`:** "You're out of the door before he's out of his chair. Behind you, calm, not raised:" · Dr. Hale: "Next Thursday, @player."

"his wife's car isn't there yet" is true: the session ends by 19:05 and her pickup is half past seven.

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`hale_thursdays` · `touch_low`** — 1167 words · 48 counted: tits, tits, nipple, nipple, nipple, ass, ass, tits, nipple, nipple, tits, tit, clit, nipple, nipple, clit, tits, tits, nipple, nipple, nipple, ass, ass, tits, nipple, nipple, tits, tit, clit, nipple, nipple, clit, tits, tits, nipple, nipple, nipple, ass, ass, tits, nipple, nipple, tits, tit, clit, nipple, nipple, clit · ceiling: Hale's middle column: tits, nipples, cock, with plain anatomy

> Dr. Hale stands behind your chair. His hands settle on your shoulders, warm and heavy.
>
> Tell me what you feel, @player.
>
> Your hands.
>
> You say.
>
> Be specific.
>
> His hands slide down over your top and close on your tits.
>
> You're squeezing my tits.
>
> You say, and your voice shakes. His thumbs find your nipples through the cloth and circle them slowly. They go hard under his touch.
>
> My nipples are hard.
>
> Good. Go on.
>
> He rolls them between finger and thumb until you gasp.
>
> I feel it between my thighs.
>
> Be specific.
>
> I'm wet.
>
> His hands move down your sides to your hips. He pulls you back against the chair and holds you there. Your thighs squeeze together. His thumbs dig into your hips, and your nipples ache against your top.
>
> Stand there.
>
> Dr. Hale says, and he points at the carpet in front of his desk. He stays in his chair. He takes you by the hips and pulls you in between his knees. His hands slide round to your ass. He squeezes it hard, both cheeks, through your clothes.
>
> Tell me what you feel.
>
> Your hands on my ass.
>
> You say.
>
> I feel hot. I feel wet.
>
> He nods, because that is the right answer. His palms move up your sides, slowly, over your ribs. Then he cups your tits through your top and weighs them. His thumbs find your nipples and press.
>
> And now?
>
> Your breath catches. Your nipples go hard under his thumbs. Your thighs squeeze together. Your hips push forward, so your tits fill his hands.
>
> You sit on the corner of his desk. Dr. Hale stands in front of you, close enough that your knees touch his trousers. One hand lies flat on your thigh. The other covers your tit through your top.
>
> Where is the heat, @player?
>
> His voice stays calm, like he is reading you a test.
>
> Between my thighs.
>
> You say out loud. His hand slides up your thigh while you say it. It stops an inch short of your clit. His thumb presses your nipple through your clothes.
>
> And here?
>
> My nipples. They're hard.
>
> They are, both of them. You are wet now, and your thighs squeeze his wrist. Your hips push forward, but his hand does not move. It stays flat and warm, one inch from your clit.
>
> Dr. Hale stands behind your chair. His hands settle on your shoulders, warm and heavy.
>
> Tell me what you feel, @player.
>
> Your hands.
>
> You say.
>
> Be specific.
>
> His hands slide down over your dress and close on your tits.
>
> You're squeezing my tits.
>
> You say, and your voice shakes. His thumbs find your nipples through the cloth and circle them slowly. They go hard under his touch.
>
> My nipples are hard.
>
> Good. Go on.
>
> He rolls them between finger and thumb until you gasp.
>
> I feel it between my thighs.
>
> Be specific.
>
> I'm wet.
>
> His hands move down your sides to your hips. He pulls you back against the chair and holds you there. Your thighs squeeze together. His thumbs dig into your hips, and your nipples ache against your dress.
>
> Stand there.
>
> Dr. Hale says, and he points at the carpet in front of his desk. He stays in his chair. He takes you by the hips and pulls you in between his knees. His hands slide round to your ass. He squeezes it hard, both cheeks, through your clothes.
>
> Tell me what you feel.
>
> Your hands on my ass.
>
> You say.
>
> I feel hot. I feel wet.
>
> He nods, because that is the right answer. His palms move up your sides, slowly, over your ribs. Then he cups your tits through your dress and weighs them. His thumbs find your nipples and press.
>
> And now?
>
> Your breath catches. Your nipples go hard under his thumbs. Your thighs squeeze together. Your hips push forward, so your tits fill his hands.
>
> You sit on the corner of his desk. Dr. Hale stands in front of you, close enough that your knees touch his trousers. One hand lies flat on your thigh. The other covers your tit through your dress.
>
> Where is the heat, @player?
>
> His voice stays calm, like he is reading you a test.
>
> Between my thighs.
>
> You say out loud. His hand slides up your thigh while you say it. It stops an inch short of your clit. His thumb presses your nipple through your clothes.
>
> And here?
>
> My nipples. They're hard.
>
> They are, both of them. You are wet now, and your thighs squeeze his wrist. Your hips push forward, but his hand does not move. It stays flat and warm, one inch from your clit.
>
> Dr. Hale stands behind your chair. His hands settle on your shoulders, warm and heavy.
>
> Tell me what you feel, @player.
>
> Your hands.
>
> You say.
>
> Be specific.
>
> His hands slide down over your dress and close on your tits.
>
> You're squeezing my tits.
>
> You say, and your voice shakes. His thumbs find your nipples through the cloth and circle them slowly. They go hard under his touch.
>
> My nipples are hard.
>
> Good. Go on.
>
> He rolls them between finger and thumb until you gasp.
>
> I feel it between my thighs.
>
> Be specific.
>
> I'm wet.
>
> His hands move down your sides to your hips. He pulls you back against the chair and holds you there. Your thighs squeeze together. His thumbs dig into your hips, and your nipples ache against your dress.
>
> Stand there.
>
> Dr. Hale says, and he points at the carpet in front of his desk. He stays in his chair. He takes you by the hips and pulls you in between his knees. His hands slide round to your ass. He squeezes it hard, both cheeks, through your clothes.
>
> Tell me what you feel.
>
> Your hands on my ass.
>
> You say.
>
> I feel hot. I feel wet.
>
> He nods, because that is the right answer. His palms move up your sides, slowly, over your ribs. Then he cups your tits through your dress and weighs them. His thumbs find your nipples and press.
>
> And now?
>
> Your breath catches. Your nipples go hard under his thumbs. Your thighs squeeze together. Your hips push forward, so your tits fill his hands.
>
> You sit on the corner of his desk. Dr. Hale stands in front of you, close enough that your knees touch his trousers. One hand lies flat on your thigh. The other covers your tit through your dress.
>
> Where is the heat, @player?
>
> His voice stays calm, like he is reading you a test.
>
> Between my thighs.
>
> You say out loud. His hand slides up your thigh while you say it. It stops an inch short of your clit. His thumb presses your nipple through your clothes.
>
> And here?
>
> My nipples. They're hard.
>
> They are, both of them. You are wet now, and your thighs squeeze his wrist. Your hips push forward, but his hand does not move. It stays flat and warm, one inch from your clit.

**`hale_thursdays` · `touch_high`** — 1217 words · 56 counted: tits, nipple, tit, nipple, clit, cock, clit, tits, clit, nipple, clit, clit, tits, clit, nipple, cock, clit, nipple, tits, nipple, tit, nipple, cunt, clit, cock, clit, tits, clit, nipple, clit, clit, tits, clit, nipple, cock, clit, nipple, tits, nipple, tit, nipple, cunt, clit, cock, clit, tits, clit, nipple, clit, clit, tits, clit, nipple, cock, clit, nipple · ceiling: Hale's middle column: tits, nipples, cock, with plain anatomy · **past the ceiling: cunt**

> Top off, @player.
>
> Dr. Hale says it like he is reading a page number. You pull your top over your head and drop it on the chair. Your tits are bare in the cold office, and your nipples go hard. His hand cups your left tit. He pinches the nipple until you gasp. You want to know what he'd do next. He sits back instead, with a notepad and a pen.
>
> Touch yourself. Tell me what you feel.
>
> You slide your hand inside your clothes. Your fingers find your clit, and you are wet.
>
> It's hot.
>
> You say, rubbing.
>
> It's swollen. I want your hand there.
>
> He writes it down. His cock is hard under his trousers, and he leaves it alone. You rub your clit faster, your thighs shaking, your hips pushing up into your own fingers.
>
> You lie back on his desk with your top off and your tits bare. Dr. Hale stands over you, calm. His hand slides inside your clothes and rests flat on your belly. Then it moves down. Two fingers find your clit. He rubs it slowly, like he is taking a measurement.
>
> Describe it, @player. Precisely.
>
> It's hot.
>
> You say.
>
> Small circles. It aches.
>
> You stop to breathe, and his hand stops with you.
>
> Keep talking.
>
> My nipples are hard. My thighs are shaking.
>
> His fingers move the moment you speak, slow and exact. You are wet on them. He spreads it over your clit.
>
> More detail.
>
> It's swollen.
>
> You gasp.
>
> Please don't stop.
>
> Your hips lift off the desk into his hand. His wet fingers keep circling your clit.
>
> You sit in his chair with your top off and your tits bare. Your knees are wide apart. Dr. Hale stands at the window with his back to the parking lot, taking notes. Your hand is down inside your clothes, two fingers on your clit. You are so wet he can hear it.
>
> Slower.
>
> He says. You slow down, and your thighs shake.
>
> Now tell me.
>
> I'm close.
>
> You say.
>
> I'm so close it hurts.
>
> He writes that down. Then he crosses the room and pinches your nipple once, hard. You gasp and your hips jerk off the seat. His cock is hard under his trousers, right at your shoulder. He goes back to the window and his notes. Your fingers keep circling your clit, slow, the way he said. Your nipple throbs, and your thighs stay open.
>
> Top off, @player.
>
> Dr. Hale says it like he is reading a page number. You pull your dress over your head and drop it on the chair. Your tits are bare in the cold office, and your nipples go hard. His hand cups your left tit. He pinches the nipple until you gasp. You want to know what he'd do next. He sits back instead, with a notepad and a pen.
>
> Touch yourself. Tell me what you feel.
>
> You slide your hand down to your cunt. Your fingers find your clit, and you are wet.
>
> It's hot.
>
> You say, rubbing.
>
> It's swollen. I want your hand there.
>
> He writes it down. His cock is hard under his trousers, and he leaves it alone. You rub your clit faster, your thighs shaking, your hips pushing up into your own fingers.
>
> You lie back on his desk with your dress off and your tits bare. Dr. Hale stands over you, calm. His hand slides down your bare belly and rests there, flat. Then it moves down. Two fingers find your clit. He rubs it slowly, like he is taking a measurement.
>
> Describe it, @player. Precisely.
>
> It's hot.
>
> You say.
>
> Small circles. It aches.
>
> You stop to breathe, and his hand stops with you.
>
> Keep talking.
>
> My nipples are hard. My thighs are shaking.
>
> His fingers move the moment you speak, slow and exact. You are wet on them. He spreads it over your clit.
>
> More detail.
>
> It's swollen.
>
> You gasp.
>
> Please don't stop.
>
> Your hips lift off the desk into his hand. His wet fingers keep circling your clit.
>
> You sit in his chair with your dress off and your tits bare. Your knees are wide apart. Dr. Hale stands at the window with his back to the parking lot, taking notes. Your hand is down between your open thighs, two fingers on your clit. You are so wet he can hear it.
>
> Slower.
>
> He says. You slow down, and your thighs shake.
>
> Now tell me.
>
> I'm close.
>
> You say.
>
> I'm so close it hurts.
>
> He writes that down. Then he crosses the room and pinches your nipple once, hard. You gasp and your hips jerk off the seat. His cock is hard under his trousers, right at your shoulder. He goes back to the window and his notes. Your fingers keep circling your clit, slow, the way he said. Your nipple throbs, and your thighs stay open.
>
> Top off, @player.
>
> Dr. Hale says it like he is reading a page number. You pull your dress over your head and drop it on the chair. Your tits are bare in the cold office, and your nipples go hard. His hand cups your left tit. He pinches the nipple until you gasp. You want to know what he'd do next. He sits back instead, with a notepad and a pen.
>
> Touch yourself. Tell me what you feel.
>
> You slide your hand down to your cunt. Your fingers find your clit, and you are wet.
>
> It's hot.
>
> You say, rubbing.
>
> It's swollen. I want your hand there.
>
> He writes it down. His cock is hard under his trousers, and he leaves it alone. You rub your clit faster, your thighs shaking, your hips pushing up into your own fingers.
>
> You lie back on his desk with your dress off and your tits bare. Dr. Hale stands over you, calm. His hand slides down your bare belly and rests there, flat. Then it moves down. Two fingers find your clit. He rubs it slowly, like he is taking a measurement.
>
> Describe it, @player. Precisely.
>
> It's hot.
>
> You say.
>
> Small circles. It aches.
>
> You stop to breathe, and his hand stops with you.
>
> Keep talking.
>
> My nipples are hard. My thighs are shaking.
>
> His fingers move the moment you speak, slow and exact. You are wet on them. He spreads it over your clit.
>
> More detail.
>
> It's swollen.
>
> You gasp.
>
> Please don't stop.
>
> Your hips lift off the desk into his hand. His wet fingers keep circling your clit.
>
> You sit in his chair with your dress off and your tits bare. Your knees are wide apart. Dr. Hale stands at the window with his back to the parking lot, taking notes. Your hand is down between your open thighs, two fingers on your clit. You are so wet he can hear it.
>
> Slower.
>
> He says. You slow down, and your thighs shake.
>
> Now tell me.
>
> I'm close.
>
> You say.
>
> I'm so close it hurts.
>
> He writes that down. Then he crosses the room and pinches your nipple once, hard. You gasp and your hips jerk off the seat. His cock is hard under his trousers, right at your shoulder. He goes back to the window and his notes. Your fingers keep circling your clit, slow, the way he said. Your nipple throbs, and your thighs stay open.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the session, the tiers, the pays, the three answers, Claire one Thursday in four | `proposals/HALE_R1_LADDER.md`, "His hot repeatable" (signed 2026-11-01) |
| the random roll | the build (random effect values, built) |
| the shuffle-bag pools | DECISIONS 112 |
| the window, before Claire | the built canvas |
| what the built canvas loses, the lines | mine, signed by LO 2026-11-01 |
