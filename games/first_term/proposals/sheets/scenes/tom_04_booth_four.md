# [REVIEW] Scene — tom_04_booth_four

> A draft for LO to place. Written 2026-10-08. **Tom's voice sample, in full:** every screen written by
> `v2-prose` from a spec, measured with `gates.py --beat`, pasted here. LO picked this step. It is the first
> time on the café's paid route.

| row | answer |
|---|---|
| person · step | `npc_tom` · 4 (Tom B 4) · with Gary (52) |
| where · when | the café, booth four · weekdays 14:30–18:00, Gary's hours |
| gate | `cafe_job` · Corruption 40 · Exhibitionism 20 · his Want 30 |
| want (test 1) | Tom: "Gary asks about you." · Gary lowered his paper at step 2 |
| next step (test 2) | she is paid for her company: Gary's hand on her thigh |
| hook (test 3) | Tom's open palm: whose price is it? (step 5) |
| what she wears here (test 8) | her café uniform: the café's dress rule backs it |
| the price on the button | "$20 — Tom takes half" · money add +10 |
| her climb (paid) | introduced: step 2 (Gary) · first time: here · then the repeat |
| the crude-word ceiling | Tom's middle column: tits, cock · early: ass, tits (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `counter` | Tom sells her time: twenty, half his | no | "Sit with him. ($20 — Tom takes half)" → `booth` · "Not today." → `no` | none |
| `booth` | beside Gary; her rule: "Hands where I can see them." | no | "Ten minutes." → `ten` | none |
| `ten` | his hand on her thigh, his eyes on her tits | yes (3 words) | "Time." → `after` | corruption add +3 · Tom's Want add +10 |
| `after` | the twenty; Tom's palm; she gives him ten | no | "Back to work." → the shift | money add +10 · `tom_step` set 4 · `gary_ten_minutes_open` set |
| `no` | "Not today, Tom." Booth four goes to the other server | no | "Back to work." → the shift | this shift's tips: normal rate only · the step returns next shift |

"Stop" is on `ten` as a choice too: "That's enough, Gary." It ends the ten minutes early for ten, not twenty
(money add +5, guess), and still counts the step.

## The screens, written

**`counter`** · 110 words · explicit words 1 (tits) · median sentence 8

> Tom leans on the counter beside you and keeps his voice low. "Gary wants company. Ten minutes. Sit." He tips his head at booth four. Gary is already watching you, a folded twenty on his saucer. "Twenty for ten minutes. Half is mine." Tom says the price slowly, because he likes saying it. His eyes drop down your uniform. "He just wants a look at your tits up close, @player. Easy money." Your face goes hot. You want the ten, but you don't want Gary's eyes on you for ten minutes. *You could just say no. So why haven't you?* Gary taps the bill, and both men wait for you.

**`booth`** · 104 words · explicit words 1 (tits) · median sentence 7

> You slide into booth four. Not across from Gary, but beside him. The twenty sits folded on his saucer. Gary doesn't pretend to look anywhere else. His eyes drop to your tits, then climb back to your mouth. "Ten minutes, sweetheart." His voice has gone thick. Your face burns, because you know exactly what that twenty buys. You hesitate, then you say it out loud. "Ten minutes. Hands where I can see them." At the counter, Tom is drying a glass that is already dry. He hasn't looked away once. Under the table, Gary's warm palm settles on your bare knee. The clock starts.

One change after `v2-prose`: "two tens" became "the twenty", to match the first screen.

**`ten`** · 139 words · explicit words 3 (cock, nipple, tits) · median sentence 12 · no act: his hand stays on her thigh · Tom's middle column: tits, cock · early: ass, tits · no cunt, cum, fuck

> Gary's hand finds your bare knee under the table, warm and heavy. Then it slides up your thigh, slow, and his thumb starts to stroke. His eyes are on your tits. He tries to look at your face, but they drop back every time. "You've no idea what you do to me, sweetheart," he says, low. He shifts in the booth so you see it. His cock is hard in his slacks, a thick ridge pressing the cloth. Your nipples tighten under your uniform, and he sees it. His other hand stays flat on the table, where you told him to keep it. Behind him, Tom watches from the counter. You let the hand stay. You're shaky, and more turned on than you expected. Gary checks his watch with his breath short and his hand still squeezing your thigh.

*The last sentence:* `--beat` flags it, because thigh and breath are not on its list. It is his hand and his breath, on
the body, not a meaning: the same reading you kept for Mark A 5. Your call.

**`after`** · 90 words · explicit words 0 · median sentence 10 · her feeling after, its own beat

> Gary leaves the twenty on the saucer, and a wink. You fold the note small before anyone sees it. At the counter, Tom holds out his hand. He doesn't say a word. You give him ten. He pockets it and grins like he did the work. "Nice, @player. Easy money." *Ten for letting a man touch your thigh. And you'd do it again.* *But Tom taking half already feels wrong. He never sat in that booth.* His palm stays open on the counter, like it will be there every time.

**`no`** · 64 words · explicit words 0 · median sentence 7 · the written no, priced

> "Not today, Tom." He shrugs. "Your call, @player. Offer stands." Then he gives booth four to the other server, and that is the price. You're angry, but you knew it would cost something. You watch her laugh at Gary's jokes. You watch the big tip go into her hand instead of yours. Gary never looks at her. His eyes follow you across the room.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, her rule, her no | the arc ideas, Tom B 4 (heat 10-06) |
| $20, half to Tom | LO, 2026-10-07 (SP4) |
| her climb: introduced, first time, repeat | `the-arc.md` A15 · the job sheet |
| this step as the voice sample | LO, 2026-10-08 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| "That's enough" pays half | guess |
