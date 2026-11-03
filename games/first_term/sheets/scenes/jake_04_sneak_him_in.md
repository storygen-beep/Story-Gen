# [READY] Scene — jake_04_sneak_him_in

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> **Changed 2026-11-02** (reader fails a3, signed by LO 2026-11-02, DECISIONS 131): row 22, `after` now points ahead: Jake mumbles "Next Saturday. Same room." before he falls asleep (`jake.py`).

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): the no gets his reply.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–119). From Jake's signed release-1 ladder
> (`sheets/people/npc_jake.md`, step 4, the top step; `proposals/JAKE_R1_LADDER.md`, signed "with step 4 on his late
> column"). The explicit screens are written by `v2-prose` and measured; the other lines are mine.

| row | answer |
|---|---|
| person · step | `npc_jake` · 4 (new, top step) |
| where · when | the front door after a date, Sat 22:00-00:00, then her room |
| gate | his step 3 · Corruption 40 · a date tonight · the boost off |
| want | the car after his dates (the date end, Bold): he wants more than the car |
| next step | she sneaks him in: Kayla's move, reversed |
| hook | Ryan's next-morning line; Monday, the team knows; the sneak-in repeat opens |
| who notices | **Ryan, through the wall** (from his step 5) · a footstep on the landing when her door has no key |
| what she risks | Laura and Mark across the landing; the door that won't lock |
| what she wears here | not named; "your clothes" come off in the act |
| her voice | stage 3 (Bold) |
| the crude-word ceiling | Jake's late column: cock, fuck, cum (signed with the proposal, LO 2026-11-01), with ass, tits and plain anatomy (nipples, clit, wet, thighs) · no pussy, cunt |
| her_line_low · her_line_high | low: "He's normal. This is normal." · high: "You want Ryan to hear every second of it." | The high line is her thought in `bed` and `wall`. |
| mixed act? | no: behind her door. Corruption only (`meters.md` rule 3) |
| does it finish | yes |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** sex with someone she knows, her brother through the wall · Bold (Corruption 40)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| she sneaks him up; they fuck on her bed against Ryan's wall | Ryan, through the wall; a footstep if her door is unlocked | Laura and Mark across the landing | "Come up." then "Harder." | "Your room. Now." He pins her wrists | yes, on the body | his step 4; `jake_first_time`; Corruption +3; Ryan's Want +5 |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`jake_04_sneak_him_in`** — Front Door · Sat 22:00-00:00 · Jake there · needs Jake's step = 3 · Corruption 40+ · under 6h since `jake_date_went` · drinks boost off · under 6h since `jake_date_went` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | Jake walks you up to the porch and stops under the light. | no | "Quiet." → `bed` | — |
| | | | "Goodnight, Jake." → `next_sat` | — |
| `next_sat` | He grins and walks backwards down the path, all the way to the car. | no | "Go in." → Hall | `jake_date_booked` cleared · `late_date` set · `came_home_late` set · back in 7 days |
| `bed` | Your door clicks shut behind you both, and Jake is all hands. | yes | "Harder." → `wall` | — |
| `wall` | Jake pins your wrists above your head and fucks you harder. | yes | "Don't stop." (`her_door_unlocked`) → `landing` | — |
| | | | "Don't stop." (not `her_door_unlocked`) → `comes` | — |
| `landing` | A footstep in the hall. | no | "Don't stop." → `comes` | — |
| `comes` | You come first. | yes | "Lie there." → `after` | — |
| `after` | Jake pulls you in against his chest and mumbles it into your hair, already half asleep. | no | "Sleep (6h)." → Your Room | Corruption +3 (cap 79) · Jake's step = 4 · Ryan's Want +5 · `jake_04_done` set · `jake_first_time` set · `jake_date_booked` cleared · `late_date` set · `came_home_late` set |

## The explicit screens, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Fixes after: "cums" / "cum" as a verb became "comes" / "come" (as Ryan's batch); her high line in `bed` came back as speech and is now her thought; both re-measured.

**`bed`** · 135 words · explicit words 8 · median sentence 9 · act rungs: touch, oral (his mouth on her nipples), vaginal

> Your door clicks shut behind you both, and Jake is all hands. He pulls your clothes off and pushes you back onto your bed. One big hand pins your wrists above your head. "Look at you, gorgeous," he whispers, grinning. His jeans come open. His cock springs out, hard and thick. He kisses down to your tits and sucks your nipples until you gasp. His free hand slides up between your thighs. You're soaking wet, so he feels it straight away. "Fuck me," you whisper. *You want Ryan to hear every second of it.* He laughs low and lines his cock up against you. He pushes into you slowly, then all the way. You arch off the mattress. His cock drives deeper as he starts to move, and your headboard knocks once against the wall.

**`wall`** · 135 words · explicit words 9 · median sentence 10 · act rungs: oral (the same), vaginal

> Jake pins your wrists above your head and fucks you harder. The headboard hits the wall. Again. Again. That wall is Ryan's, the thin one, and every thrust bangs it. You don't tell Jake to slow down. You push your hips up into him and make it louder. You want Ryan to hear every second of it. "Fuck, gorgeous," Jake grunts into your neck. His mouth drops to your tits, sucking one nipple hard, then the other. Your legs lock round his back. His cock drives deep, all the way in, and your thighs shake around him. You're so wet that every stroke is loud too. Your clit grinds against him each time he slams in. You're close, right at the edge. The headboard slams the wall, and his cock slams into you with it.

**`comes`** · 129 words · explicit words 5 · median sentence 7 · act rungs: hands, vaginal, finish

> You come first. Your whole body locks up and you clench hard around his cock. You cry out, so Jake clamps his hand over your mouth. "Shh, gorgeous. The whole house will hear." You moan into his palm anyway. Your thighs shake against his hips. He fucks you through it, deep and fast, until he loses it. He groans into your neck. His hips jerk once, twice, three times. You feel him come inside you, hot and thick. The headboard hits the wall one last time. Then he stops. He sinks down on you, heavy, his chest crushing your tits. You both breathe hard. His sweat cools on your stomach. Your thighs stay wrapped around his hips. His cock is still buried inside you, and neither of you moves.

Every last sentence is on the bodies (the headboard and his cock; still inside her).

## The other screens (mine, signed by LO 2026-11-01)

**`door`:** "Jake walks you up to the porch and stops under the light. You don't let go of his hand. You open the front door and pull him in after you." · @player, a whisper: "Come up." · "On the dark stairs he catches your hip and his breath is hot on your ear." · Jake: "Your room. Now."
**`landing`:** "A footstep on the landing. You both freeze. Your door has no key, not since Sunday." · "Jake's hand goes over your mouth. The footstep stops, and then goes on, and a door closes." · "He doesn't pull out. He starts again, slower."
**`after`:** "Jake pulls you in against his chest and mumbles it into your hair, already half asleep." · Jake: "Next Saturday. Same room." · "He's asleep in under a minute, one arm heavy across you, taking up most of the bed." · if `ryan_step` gte 5: "Through the wall, very low, so low you might have dreamed it:" · Ryan: "…@player.nickname?" · *(thought)* "He heard. Every second."

## After it
- **Ryan, next morning** (his bathroom-door hub, the first morning after `jake_first_time`, once): "Thin walls, @player.nickname. Remember?" Mine.
- **Monday on the quad** (Jake's quad hub, `jake_step` eq 4): "One of the team whistles when you walk up. Jake doesn't tell him to stop." Mine.
- **The sneak-in repeat** opens (`jake_date_end.md`).

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`jake_04_sneak_him_in` · `bed`** — 153 words · 8 counted: cock, kiss, tits, suck, nipple, fuck, cock, cock · ceiling: Jake's late column: cock, fuck, cum, with ass, tits, plain anatomy

> Your door clicks shut behind you both, and Jake is all hands. He pulls your clothes off and pushes you back onto your bed. One big hand pins your wrists above your head.
>
> Look at you, gorgeous.
>
> He whispers, grinning. His jeans come open. His cock springs out, hard and thick. He kisses down to your tits and sucks your nipples until you gasp. His free hand slides up between your thighs. You're soaking wet, so he feels it straight away.
>
> Fuck me.
>
> You whisper.
>
> You want Ryan to hear every second of it.
>
> He laughs low and lines his cock up against you. He pushes into you slowly, then all the way. You arch off the mattress. His cock drives deeper as he starts to move, and your headboard knocks once against the wall.
>
> God, you're tight. Is this okay? Tell me this is okay.
>
> It's okay. Don't you dare be gentle.

**`jake_04_sneak_him_in` · `wall`** — 149 words · 9 counted: fuck, thrust, fuck, tits, suck, nipple, cock, clit, cock · ceiling: Jake's late column: cock, fuck, cum, with ass, tits, plain anatomy

> Jake pins your wrists above your head and fucks you harder. The headboard hits the wall. Again. Again. That wall is Ryan's, the thin one, and every thrust bangs it. You don't tell Jake to slow down. You push your hips up into him and make it louder. You want Ryan to hear every second of it.
>
> Fuck, gorgeous.
>
> Jake grunts into your neck. His mouth drops to your tits, sucking one nipple hard, then the other. Your legs lock round his back. His cock drives deep, all the way in, and your thighs shake around him. You're so wet that every stroke is loud too. Your clit grinds against him each time he slams in. You're close, right at the edge. The headboard slams the wall, and his cock slams into you with it.
>
> Your bed's hitting the wall. Who's on the other side?
>
> My brother. Don't stop.

**`jake_04_sneak_him_in` · `comes`** — 141 words · 7 counted: cock, moan, fuck, tits, cock, fuck, fuck · ceiling: Jake's late column: cock, fuck, cum, with ass, tits, plain anatomy

> You come first. Your whole body locks up and you clench hard around his cock. You cry out, so Jake clamps his hand over your mouth.
>
> Shh, gorgeous. The whole house will hear.
>
> You moan into his palm anyway. Your thighs shake against his hips. He fucks you through it, deep and fast, until he loses it. He groans into your neck. His hips jerk once, twice, three times. You feel him come inside you, hot and thick. The headboard hits the wall one last time. Then he stops. He sinks down on you, heavy, his chest crushing your tits. You both breathe hard. His sweat cools on your stomach. Your thighs stay wrapped around his hips. His cock is still buried inside you, and neither of you moves.
>
> Fuck. Fuck, @player. I'm still inside you.
>
> Stay there. Don't move yet.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the step, Ryan's wall, the unlocked door, the late column | `proposals/JAKE_R1_LADDER.md`, step 4 (signed 2026-11-01) |
| the unlocked door | `money_pressure.md`: Mark takes her key after the first short Sunday (`her_door_unlocked`) |
| Ryan's Lust +5 | the same, "Ryan hears" |
| the pay (Corruption +3) | `meters.md` rule 3; mine, confirmed by LO 2026-11-01 ("Continue") |
| the lines, Ryan's and the team's | mine, confirmed by LO 2026-11-01 ("Continue") |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

| node | the no | the reply (mine, signed by LO 2026-11-01) |
|---|---|---|
| `door` | "Goodnight, Jake." | Jake: "Next Saturday, then. Your room." · "He grins and walks backwards down the path, all the way to the car." The step waits for the next date, as before. |
