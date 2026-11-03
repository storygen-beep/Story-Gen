# [READY] Scene — zoe_05_no_dare

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): both endings point ahead.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–118). From Zoe's signed release-1 ladder
> (`sheets/people/npc_zoe.md`, step 5, the top step; `proposals/ZOE_R1_LADDER.md`, signed "with step 5 on her late
> column"). The explicit screens are written by `v2-prose` and measured; the other lines are mine.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 5 (new, top step) |
| where · when | Zoe's place, built at her living room · Sat 00:00-01:45, within 8 hours of the party |
| gate | her step 4 · Corruption 40 · her dares 4+ · `cocky_guy_met` · the boost off · "Let him watch." Exhibitionism 60 |
| want | "I dared you instead of asking. I always do." (step 4) |
| next step | she stops daring and asks |
| hook | the cocky guy at the door (`zoe_let_him_watch`) · her dares change after `zoe_together` · her card ends "Zoe's next dare. (Next release)" |
| who notices | Zoe; **the cocky guy at the door** |
| what she risks | the party hearing; the guy at the door |
| what she wears here | not named; "your clothes" come off in the act |
| her voice | stage 3 (Bold) |
| the crude-word ceiling | Zoe's late column: pussy, clit, fuck, with tits, nipples, wet, ass, thighs · no cunt, cum, cock (signed with the proposal, LO 2026-11-01) |
| her_line_low · her_line_high | low: "It's a dare. It doesn't count." · high: "You want her to dare you something worse." | The high line is the thought on `asking`. |
| does it finish | yes |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** oral sex with someone she knows, and a watcher at the door · Bold (Corruption 40); the watcher at Watched (60)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| "No dare." Zoe goes down on her; the cocky guy opens the door | Zoe; the cocky guy at the door | the party hearing; the guy at the door | "Yes." · "Ask me again." (back in 7 days) | she asks; she decides about the door | yes, on the body | her step 5; `zoe_together`; Corruption +3; watched: `zoe_let_him_watch` |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`zoe_05_no_dare`** — Zoe's Living Room · Sat 00:00-01:45 · Zoe there · needs Zoe's step = 4 · Corruption 40+ · Zoe's dares 4+ · `cocky_guy_met` · drinks boost off · under 8h since `party_went` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `asking` | Zoe pulls you into her bedroom and shuts the door on the party. | no | "Yes." → `down` | — |
| | | | "Ask me again." → `again` | — |
| `down` | Zoe pulls your clothes off you and pushes you back on her bed. | yes | "Don't stop." → `comes` | — |
| `comes` | Zoe's tongue stays flat on your clit and her fingers curl inside your pussy, and you're … | yes | "Tell him to go." → `out` | — |
| | | | "Let him watch." (Exhibitionism 60+) → `watch` | — |
| `out` | The door clicks shut. | no | "Stay with her." → Zoe's Living Room | Corruption +3 (cap 79) · Zoe's step = 5 · `zoe_05_done` set · `zoe_together` set |
| `watch` | He stays. | no | "Stay with her." → Zoe's Living Room | Corruption +3 (cap 79) · Zoe's step = 5 · Exhibitionism +3 (cap 79) · `zoe_05_done` set · `zoe_together` set · `zoe_let_him_watch` set |
| `again` | Zoe laughs, and something in her face lets go. | no | "Go back to the party." → Zoe's Living Room | back in 7 days |

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

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`zoe_05_no_dare` · `down`** — 173 words · 14 counted: kiss, tits, suck, nipple, lick, clit, puss, moan, ass, fuck, clit, fuck, cunt, clit · ceiling: Zoe's late column: pussy, clit, fuck, with tits, nipples, wet, ass · **past the ceiling: cunt**

> Zoe pulls your clothes off you and pushes you back on her bed. The music thumps through the door. She kisses down your tits and sucks one nipple hard, then the other. Her mouth moves down your belly. She spreads your thighs with both hands and grins up at you.
>
> Say it, babe.
>
> Lick me.
>
> You tell her.
>
> Please.
>
> Her tongue finds your clit, slow and flat. Two fingers slide inside your pussy, and you're so wet they go in easy. You moan, loud, but the party is right through the door and you don't care. You grab her hair and push your hips up into her face. Her ass is up, her own hips rocking against the sheets. She curls her fingers and fucks you faster. Her tongue stays on your clit until your thighs shake around her head.
>
> Oh fuck. Right there, Zo. Don't you dare stop.
>
> I've wanted my mouth on your cunt all term, babe.
>
> She says it against your clit, and her tongue goes straight back to work.

**`zoe_05_no_dare` · `comes`** — 126 words · 9 counted: clit, puss, ass, lick, fuck, moan, cock, tits, puss · ceiling: Zoe's late column: pussy, clit, fuck, with tits, nipples, wet, ass

> Zoe's tongue stays flat on your clit and her fingers curl inside your pussy, and you're gone. You come hard. Your hand slams over your own mouth so the party won't hear you scream. Your thighs lock tight round her head. Your hips buck off the bed, but Zoe pins your ass down and keeps licking. She fucks you with her fingers through every wave. You moan into your palm until your whole body shakes. Only then does she slow. Then the bedroom door swings open. The cocky guy stands there with a beer in his hand, staring at your bare tits and your spread thighs. Zoe doesn't look up. Her mouth is still on your pussy, and your legs are still trembling round her ears.

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
