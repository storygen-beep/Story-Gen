# [READY] Scene — jake_04_sneak_him_in

> **Changed 2026-11-02** (reader fails a3, signed by LO 2026-11-02, DECISIONS 131): row 22, `after` now points ahead: Jake mumbles "Next Saturday. Same room." before he falls asleep (`jake.py`).

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): the no gets his reply.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–119). From Jake's signed release-1 ladder
> (`sheets/people/npc_jake.md`, step 4, the top step; `proposals/JAKE_R1_LADDER.md`, signed "with step 4 on his late
> column"). The explicit screens are written by `v2-prose` and measured; the other lines are mine.

| row | answer |
|---|---|
| person · step | `npc_jake` · 4 (new, top step) |
| where · when | the front door after a date, Sat 22:00–00:00 (it takes the date-end slot that night, higher priority), then up to her room, `home_ella_room`; the clock goes past midnight |
| gate | `jake_step` eq 3 · Corruption 40 · `jake_date_went` (tonight) · the boost off |
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

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `door` | the porch; she takes his hand: "Come up." On the stairs, in the dark: "Your room. Now." | no | "Quiet." → `bed` · "Goodnight, Jake." → the date end's goodnight (parked) | none |
| `bed` | her door shut; her clothes off, her wrists pinned; he pushes into her; the headboard knocks once | yes | → `wall` | none |
| `wall` | harder; the headboard hits Ryan's wall, again and again; she makes it louder | yes | → `landing` if `her_door_unlocked` · else → `comes` | none |
| `landing` | a footstep on the landing; her door has no key; Jake's hand over her mouth; the footstep goes on; they don't stop | no | → `comes` | none |
| `comes` | she comes first, his hand over her mouth; he comes inside her; still | yes | → `after` | corruption add +3 (cap 59) · `jake_step` set 4 · `jake_04_done` · `jake_first_time` set |
| `after` | Jake asleep; through the wall, if Ryan is past his step 5: "…@player.nickname?" | no | "Sleep." → her room | Ryan's Lust add +5 (as the built Jake 3 pays, jealousy) |

**Across the landing, the same hour:** Sunday 00:00–01:00 is Mark and Laura's own hour (`master_door_saturday_night`, `npc_mark.md` schedule), so the house is awake across the landing while she sneaks Jake in. The `landing` line and the near-catches in the repeat are true to it.

**The parked no** ("Goodnight, Jake."): the date ends as usual; the step waits for the next date.

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
