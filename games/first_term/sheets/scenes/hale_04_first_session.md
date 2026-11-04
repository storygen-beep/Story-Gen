# [REVIEW] Scene — hale_04_first_session
> Changed 2026-11-04, writing pass: lines brought to the build (fresh text per room, her voice by level, the reader's fixes); waits for LO's re-sign.

> Changed 2026-11-04 to match the build; waits for LO's re-sign. His card's end line as built (DECISIONS 132); "Wait." also takes Energy 10 and Hygiene 10.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–117). From Hale's signed release-1 ladder
> (`sheets/people/npc_hale.md`, step 4, the top step; `proposals/HALE_R1_LADDER.md`). Reworks the built canvas
> `hale_04_claire_knocks` (the id stays; that sheet is marked reworked). The explicit screens are written by `v2-prose`
> and measured; the other lines are mine.

| row | answer |
|---|---|
| person · step | `npc_hale` · 4 of 4, top step · Claire (38), his wife, met here |
| where · when | his office · Thursday, starts 18:30-19:15 |
| gate | his step 3 · Corruption 40 · Exhibitionism 40 · the boost off · "Let him." pays +3 each, cap 79 |
| want | he locks the door; "Tell me what you feel." |
| next step | his hand on her tits, then higher, until Claire knocks |
| hook | Claire at the door; the Thursday sessions open |
| who notices | Hale; **Claire**, through the door |
| what she risks | his wife; her grade; how far he'll go |
| what she wears here | not named (the beats say "your top", "your clothes" only) |
| her voice | stage 2 (Curious and Daring) |
| the crude-word ceiling | Hale's middle column (tits, nipples, cock: his, only hard under his trousers) with plain anatomy beside it (ass, thighs, wet, clit), as Ryan's signed sheets (DECISIONS 114) · no fuck, cum, pussy, cunt (his late column is not used: it goes no further) · **at stage 2 this is a column above her stage, as Ryan's step 4 (C20, middle column); confirmed by LO 2026-11-01 ("Continue")** |
| her_line_low · her_line_high | low: "He's your professor. He's married." (in `feel`) · high: "You want to know what he'd do next." (on `knock`) |
| mixed act? | **yes** (`meters.md` rule 4): it shows her and it's sexual, so the gate needs both 20s and "Let him." pays both |
| his move | his hand, his questions |
| does it finish | **cut off** (Claire): the ladder's one cut-off |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** private sexual touch with someone she knows · Bold · Showing (40)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| locked office: she says what she feels while his hand moves on her; Claire knocks | Hale; Claire, at the door | his wife; her grade | "Let him." | locks the door; his hand and his questions | cut off: Claire's knock, the ladder's one cut-off | his step 4; `hale_touched`, `claire_met`; grade +5; Thursdays open |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`hale_04_claire_knocks`** — Dr. Hale's Office · Thu 18:30-19:15 · Dr. Hale there · needs Hale's step = 3 · Corruption 40+ · Exhibitionism 40+ · drinks boost off · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `feel` | Dr. Hale locks the door and sits back in his chair. | yes | "Let him." → `higher` | — |
| | | | "This isn't coaching." → `isnt` | — |
| | | | "Run." → `run` | — |
| `higher` | His hand leaves your tit, your nipple still stiff from his thumb. | yes | "Wait." → `knock` | Psychology grade +5 · Corruption +3 (cap 79) · Exhibitionism +3 (cap 79) · Energy -10 · Hygiene -10 |
| `knock` | The knock is two raps, light. | no | "Pick up your bag." → `corridor` | `claire_met` set |
| `corridor` | You pull your clothes straight and pick up your bag. | no | "Go home." → Hall | Hale's step = 4 · `hale_04_done` set · `hale_touched` set |
| `isnt` | You pull everything back down over your tits. | no | "Leave him with your grade." → Faculty Floor | back in 7 days |
| `run` | You pull everything back down over your tits, grab your bag and turn the lock yourself. | no | "Keep walking." → Campus | Psychology grade -2 · `claire_met` set · back in 7 days |

## The explicit screens, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Shared brief: he leads, touches, nothing of his comes out, no garment of hers named.

**`feel`** · 117 words · explicit words 7 · median sentence 6 · act rungs: hands · one line changed after (", but you pull your top up anyway" became two sentences), re-measured

> Dr. Hale locks the door and sits back in his chair. "Tell me what you feel, @player. Bare your tits first." You're scared. You're turned on too. You pull everything up anyway. He takes your tit in his hand. His thumb finds your nipple and circles it, slow. You go quiet. "Out loud," he says. "Your thumb. My nipple's going hard." *He's your professor. He's married.* His thumb doesn't stop. "Again." "It's hot. The heat goes all the way down." He listens like it's a lecture. Your other nipple is hard too, and you're wet. He rolls the nipple between finger and thumb. "Say it." "I'm wet. Your hand on my tit is making me wet."

*The last sentence:* her own words, his hand on her tit. On the body.

**`higher`** · 125 words · explicit words 4 · median sentence 10 · act rungs: hands

> His hand leaves your tit, your nipple still stiff from his thumb. "Keep talking." His hand slides down over your ribs, slow. "Your hand is on my ribs," you say. Your voice shakes. It moves to your hip, then flat onto your thigh. "My thigh." His fingers turn in, onto the soft inside of it. "The inside. Higher." He goes higher, an inch at a time, and you say every inch out loud. Your knees fall open. His fingertips reach the heat between your thighs and press there, once, through your clothes. You're wet, and his fingers find it. "Right there," you whisper. His cock is hard under his trousers, right by your knee. His fingers stay pressed on your clit, and your breath catches.

*The last sentence:* his fingers on her clit, her breath. On the body; the knock is the next screen.

## The other screens (mine, signed by LO 2026-11-01)

**`knock`:** "The knock is two raps, light. A woman's voice through the door, bright." · Claire, outside: "You ready, love?" · "Dr. Hale takes his hand away, not fast. He doesn't look at the door. He looks at you." · Dr. Hale: "My wife. Same time next week, @player." · *(thought)* "You want to know what he'd do next."
**`corridor`:** "You pull your clothes straight and pick up your bag. He unlocks the door for you." · "His wife is in the corridor in a neat coat, car keys in her hand. Her smile stops halfway when she sees you. Her eyes go to your face, and then past you, to the face-down photo on his desk." · Dr. Hale, behind you: "Claire. This is one of my students." · "You walk the whole corridor without looking back. Your legs are shaking."
**`isnt`:** "You pull everything back down over your tits." · @player: "This isn't coaching." · "He sits back in his chair." · Dr. Hale: "Then you'll stay at a C." · "He doesn't unlock the door until you're at it."
**`run`:** "You pull everything back down over your tits, grab your bag and turn the lock yourself. You're out of the door before he can stand up. In the corridor a woman with short dark hair is coming the other way with car keys in her hand. The woman in the photo." · "She smiles at you, polite, the way you smile at a student." · *(thought)* "His wife. She has no idea."

## After it
- **The weekly session** opens (`hale_thursday_session.md`).
- **His card** ends on: "Hale, further. (Next release)" No locked button (DECISIONS 132).
- **His office hub:** the built line at step 4 ("He can't look at you for long. He checks the corridor before he speaks.") is
 against "the jerk"; it becomes "He looks at the clock, and then at you, like you're both on his schedule." Mine; confirmed by LO 2026-11-01 ("Continue").

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`hale_04_claire_knocks` · `feel`** — 116 words · 7 counted: tits, tit, nipple, nipple, nipple, nipple, tit · ceiling: Hale's middle column: tits, nipples, cock, with plain anatomy

> Dr. Hale locks the door and sits back in his chair.
>
> Tell me what you feel, @player. Bare your tits first.
>
> You're scared. You're turned on too. You pull everything up anyway. He takes your tit in his hand. His thumb finds your nipple and circles it, slow. You go quiet.
>
> Out loud.
>
> He says.
>
> Your thumb. My nipple's going hard.
>
> He's your professor. He's married.
>
> His thumb doesn't stop.
>
> Again.
>
> It's hot. The heat goes all the way down.
>
> He listens like it's a lecture. Your other nipple is hard too, and you're wet. He rolls the nipple between finger and thumb.
>
> Say it.
>
> I'm wet. Your hand on my tit is making me wet.

**`hale_04_claire_knocks` · `higher`** — 125 words · 4 counted: tit, nipple, cock, clit · ceiling: Hale's middle column: tits, nipples, cock, with plain anatomy

> His hand leaves your tit, your nipple still stiff from his thumb.
>
> Keep talking.
>
> His hand slides down over your ribs, slow.
>
> Your hand is on my ribs.
>
> You say. Your voice shakes. It moves to your hip, then flat onto your thigh.
>
> My thigh.
>
> His fingers turn in, onto the soft inside of it.
>
> The inside. Higher.
>
> He goes higher, an inch at a time, and you say every inch out loud. Your knees fall open. His fingertips reach the heat between your thighs and press there, once, through your clothes. You're wet, and his fingers find it.
>
> Right there.
>
> You whisper. His cock is hard under his trousers, right by your knee. His fingers stay pressed on your clit, and your breath catches.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the session, the three answers, Claire's knock, the pays | `proposals/HALE_R1_LADDER.md`, step 4 (signed 2026-11-01) |
| the mixed act, both meters | `meters.md`, rules 3–4 (signed) |
| Claire's look at the photo, her coat and keys | the built `knock` (kept in spirit) |
| the nos park, the hub line, the column | mine, confirmed by LO 2026-11-01 ("Continue") |
