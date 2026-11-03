# [READY] Scene — zoe_05_no_dare

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): both endings point ahead.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–118). From Zoe's signed release-1 ladder
> (`sheets/people/npc_zoe.md`, step 5, the top step; `proposals/ZOE_R1_LADDER.md`, signed "with step 5 on her late
> column"). The explicit screens are written by `v2-prose` and measured; the other lines are mine.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 5 (new, top step) |
| where · when | Zoe's bedroom, `zoe_bedroom` · Sat 00:00–02:00, after a Friday party (`AT_PARTY` was set tonight), the music still through the door |
| gate | `zoe_step` eq 4 · Corruption 40 · "Let him watch." needs Exhibitionism 60 (DECISIONS 124) · player counter `zoe_dares_done` gte 4 (+1 on every yes in `zoe_dares`; name mine) · the boost off |
| want | "I dared you instead of asking. I always do." (step 4) |
| next step | she stops daring and asks |
| hook | the cocky guy at the door; `zoe_let_him_watch` for the locked threesome · the dares change (`zoe_dares.md`) · locked: "Zoe's next dare. (Needs Corruption 60.)" |
| who notices | Zoe; **the cocky guy at the door** |
| what she risks | the party hearing; the guy at the door |
| what she wears here | not named; "your clothes" come off in the act |
| her voice | stage 3 (Bold) |
| the crude-word ceiling | Zoe's late column: pussy, clit, fuck, with tits, nipples, wet, ass, thighs · no cunt, cum, cock (signed with the proposal, LO 2026-11-01) |
| her_line_low · her_line_high | low: "It's a dare. It doesn't count." · high: "You want her to dare you something worse." | The high line is the thought on `asking`. |
| does it finish | yes |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `asking` | Zoe shuts the bedroom door on the party: "No dare. I'm asking." | no | "Yes." → `down` · "Ask me again." → the apartment (parked) | none |
| `down` | she undresses her and goes down on her, the party through the door | yes | → `comes` | none |
| `comes` | she comes with her hand over her mouth; the door opens: the cocky guy, a beer in his hand | yes | "Tell him to go." → `out` · "Let him watch." → `watch` | none |
| `out` | Zoe, without looking up: "Out." The door shuts | no | → the apartment | the step's pay |
| `watch` | Zoe, without looking up: "Stay. Watch." He stays in the doorway | no | → the apartment | the step's pay · `zoe_let_him_watch` set · exhibitionism add +3 (seen) |

**The step's pay:** corruption add +3 (a big first, unseen until the door) · `zoe_step` set 5 · `zoe_05_done` set ·
`zoe_together` set. The proposal names no meter pay; these follow `meters.md` rule 3 (sex behind a door: Corruption;
seen: both). Mine; confirmed by LO 2026-11-01 ("Continue").
**The parked no** ("Ask me again."): Zoe grins, "Next Friday, then." The step waits a week.

## The explicit screens, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Where the tool lists `cock` on a beat with "the cocky guy", it is matching "cocky" (a false reading, like its `vaginal` rung); the counts below leave it out.

**`down`** · 140 words · explicit words 11 · median sentence 12 · act rungs: touch, hands, oral, vaginal

> Zoe pulls your clothes off you and pushes you back on her bed. The music thumps through the door. She kisses down your tits and sucks one nipple hard, then the other. Her mouth moves down your belly. She spreads your thighs with both hands and grins up at you. "Say it, babe." "Lick me," you tell her. "Please." Her tongue finds your clit, slow and flat. Two fingers slide inside your pussy, and you're so wet they go in easy. You moan, loud, but the party is right through the door and you don't care. You grab her hair and push your hips up into her face. Her ass is up, her own hips rocking against the sheets. She curls her fingers and fucks you faster. Her tongue stays on your clit until your thighs shake around her head.

*The last sentence:* her tongue on her clit, her thighs shaking. On the body; she comes on the next screen.

**`comes`** · 126 words · explicit words 8 (9 listed, one is "cocky") · median sentence 10 · act rungs: hands, oral, vaginal

> Zoe's tongue stays flat on your clit and her fingers curl inside your pussy, and you're gone. You come hard. Your hand slams over your own mouth so the party won't hear you scream. Your thighs lock tight round her head. Your hips buck off the bed, but Zoe pins your ass down and keeps licking. She fucks you with her fingers through every wave. You moan into your palm until your whole body shakes. Only then does she slow. Then the bedroom door swings open. The cocky guy stands there with a beer in his hand, staring at your bare tits and your spread thighs. Zoe doesn't look up. Her mouth is still on your pussy, and your legs are still trembling round her ears.

*The last sentence:* Zoe's mouth on her, her legs trembling. On the body; Zoe's answer to him is the player's pick.

## The other screens (mine, signed by LO 2026-11-01)

**`asking`:** "Zoe pulls you into her bedroom and shuts the door on the party. The music thumps through it. She leans back against the door and, for once, she isn't grinning." · Zoe: "No dare. I'm asking." · *(thought, high)* "You want her to dare you something worse. She isn't going to."
**`out`:** Zoe, without lifting her head: "Out." · "The door clicks shut. The music goes muffled again. Zoe crawls up the bed and kisses you, and you taste yourself on her."
**`watch`:** Zoe, without lifting her head: "Stay. Watch." · "He stays. He leans in the doorway with his beer and doesn't say a word. Zoe crawls up the bed and kisses you slowly, so he can see all of it."
**The parked no:** @player: "Ask me again." · "Zoe laughs, and something in her face lets go." · Zoe: "Next Friday, then. I'll ask nicer."

## Why — the source of each key choice

| key choice | source |
|---|---|
| the step, the door, the two buttons, the late column | `proposals/ZOE_R1_LADDER.md`, step 5 (signed 2026-11-01) |
| four dares done | the same, the gate |
| the pay | `meters.md` rule 3 · mine, confirmed by LO 2026-11-01 ("Continue") |
| the counter name | mine, confirmed by LO 2026-11-01 ("Continue") |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

A hook line, proposed (LO asked whether a line solves it). Each line names a thing that is in the game and comes next, so it is true; a line that points at nothing would break the truth rule instead.

| node | the closing line (mine, signed) | what it points at |
|---|---|---|
| `out`, `watch` | Zoe: "Friday, babe. I'm in the dare with you now." | the dares' third tier (Zoe joins) |
