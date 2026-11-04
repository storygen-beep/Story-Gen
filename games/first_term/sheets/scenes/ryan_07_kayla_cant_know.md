# [REVIEW] Scene — ryan_07_kayla_cant_know

> Changed 2026-11-04 to match the build; waits for LO's re-sign. "Go to your room." lands in her room.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the door's two buttons as built; the pay sits on `after7`; the step row. the explicit beats as built, measured.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): `comes` ends on what comes next.

> **New 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113). From Ryan's signed release-1 ladder
> (`sheets/people/npc_ryan.md`, step 7; `proposals/RYAN_R1_LADDER.md`). Replaces `ryan_07_first_kiss` (cut).
> The explicit screens are written by `v2-prose` and measured: below.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 7 (new) |
| where · when | his room, `home_ryan_room` · Mon, Tue, Thu, Sun 19:00–22:00, after two knocks |
| gate | Corruption 60 (was 40: DECISIONS 124) · his Want 60 · `ryan_step` eq 6 · the boost off |
| want | his door left open a hand's width since the shower (step 6) |
| next step | her hand on him, to the end, while Kayla's photo lights up his phone |
| hook | his phone face-down every time she knocks after this; step 8, two knocks late at night |
| who notices | Kayla, on the screen: she calls while he's in Ella's hand |
| what she risks | Kayla calling while he's in her hand |
| what she wears here | not named |
| her voice | stage 3 (Bold) |
| the crude-word ceiling | Ryan's late column for "cum" (cunt, fuck, cum) · confirmed by LO 2026-11-01 ("Continue") |
| her_line_low · her_line_high | low: "This is Ryan. You should go." · high: "You want him to hear Kayla on the phone while you do this." (worded for this screen with the prose) |
| mixed act? | no: behind his door, unseen. Corruption only (`meters.md` rule 3) |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** her hand on him: the taboo act at home (Hungry · Watched 60).

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| her hand on his cock to the end while Kayla's photo lights up his phone | Kayla, on his screen, calling | Kayla, calling while he's in her hand | "Knock twice." · "Don't answer it." | he reaches for her, then for the phone | yes: he comes in her hand | his phone face-down when she knocks; step 8; the blanket repeatable |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `knocks` | his door is already open a hand's width | no | "Knock twice." → `hand` · "Leave him to it." → the hall (parked) | none |
| `hand` | she pushes him onto the bed and takes his cock in her hand; his phone lights up on the bed: Kayla's photo | yes | "Don't answer it." → `phone` | none |
| `phone` | he reaches for her first, then for the phone; she pushes his hand away and keeps stroking | yes | "Make him come." → `comes` | none |
| `comes` | he comes in her hand while the phone buzzes out; it goes to voicemail | yes | "Wipe your hand on his shirt." → `after7` | none |
| `after7` | from now on his phone is face-down every time she knocks | no | "Go to your room." → her room | Ryan's Want add +5 · corruption add +3, cap 79 · `ryan_step` set 7 |

**The parked no** (as built): "Leave him to it." The signed wording was "Just checking you're decent." The step waits a week (`retry_after_days = 7`,
as his other steps).

**His move:** he reaches for her first, then for the phone. **Does it finish:** yes, he comes.

## The explicit screens, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Fixes after: Ryan's name for her is `@player.nickname`, not "Ella". The tool lists `vaginal` where his spoken "fuck" or a "thrust" matches its regex; no vaginal act is on these screens (a known false reading of `gates.py`'s rung check).

**`hand`** · 126 words · explicit words 4 · median sentence 6 · act rungs: hands · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> You knock twice and push his door open without waiting. Ryan looks up from the bed. "@player.nickname. What are you doing?" You put both hands on his chest and shove him flat on the mattress. You yank his shorts down. His cock is already half hard. You wrap your hand around it and squeeze. "Jesus," he breathes. You stroke his cock slowly, base to tip, until it swells thick and hot in your fist. His balls pull tight. *Let her call. Let her call right now.* His phone buzzes on the bed beside him. Kayla's photo lights up the screen. CALLING. You keep pumping his cock, your knuckles an inch from his hip and her smile.

*The last sentence:* her fist on his cock, an inch from the lit phone. On the body; whether he answers is the next screen.

**`phone`** · 110 words · explicit words 5 · median sentence 9 · act rungs: hands, vaginal · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> Kayla's face fills the screen. The phone buzzes against the mattress beside his hip. Ryan's hand closes on your wrist first. Then his other hand goes for the phone. You knock it away. "Don't you dare." You keep stroking his cock, faster now, your fist tight and wet from him. *Let her ring.* "Fuck. @player.nickname. She'll keep calling." "Then let her." The phone buzzes again by his hip. His ass lifts off the bed. His cock throbs in your fist, swollen and hot, the head leaking over your knuckles. You twist your grip over the tip and pump him harder. His cock jerks up into your fist with every stroke.

*The last sentence:* his cock jerking into her fist. On the body; he hasn't come.

**`comes`** · 122 words · explicit words 6 · median sentence 10 · act rungs: hands, vaginal, finish · Ryan's late column: ass, tits, cock, wet, cunt, fuck, cum

> You don't slow down. Your fist works his cock from the root to the swollen head, tight and wet, and the phone buzzes against your knee. His hips come off the mattress. "@player.nickname, fuck, she's calling," he breathes, and you squeeze harder. *Let her ring.* His thighs lock. His cock jerks in your grip, thick and hot, and the first rope of cum hits his stomach. You keep pumping. The next pulses spill over your knuckles, warm and heavy, running down between your fingers. The buzzing stops. The phone lights up once with voicemail and goes dark. He shudders under you, still twitching in your fist. You hold him there until his cock softens, your hand slick and dripping with his cum.

*The last sentence:* her hand slick with his cum. On the body; not a pivot.

## Truth checks

| line | what backs it |
|---|---|
| his door open a hand's width | step 6 sets it as his after-line; gate `ryan_step` eq 6 |
| Kayla's photo on his phone | `knows_about_kayla` (step 2) |
| "two knocks" | `ryan_knock_code` (step 3) |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the step, the columns, the pay | `proposals/RYAN_R1_LADDER.md`, signed by LO 2026-11-01 (DECISIONS 100) |
| the late column for "cum" | proposed in the same file; confirmed by LO 2026-11-01 ("Continue") |
| the parked no's wording | proposed here, confirmed by LO 2026-11-01 ("Continue") |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

A hook line, proposed (LO asked whether a line solves it). Each line names a thing that is in the game and comes next, so it is true; a line that points at nothing would break the truth rule instead.

| node | the closing line (mine, signed) | what it points at |
|---|---|---|
| `comes` | "From now on his phone is face-down every time you knock." | step 8 opens on it |

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `hand` | 128 | 4: cock ×3, balls | Ryan's middle column | on this sheet above |
| `phone` | 129 | 7: cock ×3, fuck ×3, ass | Ryan's late column | on this sheet above |
| `comes` | 122 | 6: cock ×3, cum ×2, fuck | Ryan's late column | on this sheet above |
