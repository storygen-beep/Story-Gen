# [READY] Scene — jake_03_my_boyfriend

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. **Jake's voice sample, in full:** every screen written by
> `v2-prose` from a spec, measured with `gates.py --beat`, pasted here. LO picked this step.

| row | answer |
|---|---|
| person · step | `npc_jake` · 3 (Jake B 3) |
| where · when | the front door · Saturday 23:00–00:00, after a booked date |
| gate | Corruption 20 · Exhibitionism 20 · `jake_date_booked` · the boost off |
| want (test 1) | "Saturday. Pick me up at the door." (B 2); "Is anyone up?" |
| next step (test 2) | she names him to the house: Ryan |
| hook (test 3) | Ryan's light goes out; "Next Saturday?" (his thread) |
| what she wears here (test 8) | not named |
| explicit? | no: a kiss on the porch rail (stage 2) |
| the crude-word ceiling | Jake's early column: ass · Ryan's early: ass, tits (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `porch` | Jake under the porch light: "Is anyone up?" | no | "Kiss him." → `rail` · "Goodnight, Jake." → `no` | none |
| `rail` | on the porch rail, her legs round him; the lock turns behind her | no | "Don't stop." → `ryan` | none |
| `ryan` | Ryan opens the front door from inside: "Ryan, this is Jake. My boyfriend." | no | "Goodnight, Jake." → `after` | Ryan's Warmth add −10 (guess) · Ryan's Want add +5 (guess) |
| `after` | Ryan's door, his light; "Next Saturday?" | no | "Go to bed." → her room | `jake_step` set 3 · `jake_date_booked` set false |
| `no` | a kiss on the cheek; "Next Saturday, then?" | no | "Go in." → the hall | `jake_date_booked` set false · the step returns next date |

## The screens, written

**`porch`** · 102 words · explicit words 1 · median sentence 10

> Jake walks you up to the porch and stops under the light. The downstairs is dark. He looks past you at the windows, then up at the second floor. "Is anyone up?" He sounds like he hopes so. "Nobody," you say. "Not yet." Upstairs, Ryan's window is lit, right above the porch. He's home. You want him to look. "Shame," Jake says. "I want them to see you're mine, @player." His hand slides down your back and settles on your ass. You should move it, but you like being shown off. He leans in, and his mouth stops an inch from yours.

**`rail`** · 90 words · explicit words 2 · median sentence 9

> You kiss him first, right there under the porch light. Jake makes a low sound and lifts you onto the rail like you weigh nothing. Your legs lock round his waist. His hands sit on your hips, then slide down to grab your ass. "God, @player," he breathes into your mouth. It gets hungry and loud, all teeth and breath. The rail creaks every time he pulls you closer. Anyone inside could hear it, but you don't care. You want more of his mouth. Then, behind you, the lock turns.

**`ryan`** · 104 words · explicit words 2 · median sentence 7

> The front door opens behind you. Ryan stands in the doorway and stops dead. You're on the porch rail with your legs locked round Jake's waist, kissing him. Jake's hands are full of your ass. You don't climb down. You look straight at Ryan over Jake's shoulder and hold it. "Ryan, this is Jake. My boyfriend." Ryan's jaw goes tight. His eyes drop to Jake's hands on you, then come back to your face. "Great." Jake grins over his shoulder, not getting it. "Your brother hates me." *Good. Look all you want, Ryan.* Ryan steps back inside without another word. The door slams hard.

**`after`** · 89 words · explicit words 0 · median sentence 7 · the meaning beat

> Jake goes off down the path, whistling. You let yourself in and climb the stairs. Ryan's door is shut, and his light is on under it. You stand outside it a second. You don't knock, but you don't move either. You wanted him to see. You said Jake's name to his face on purpose, and you're not sorry. Not even a little. Jake will want a next Saturday. You already know it. Your phone buzzes in your hand. It's Jake: "Next Saturday?" Under Ryan's door, the light goes out.

**`no`** · 63 words · explicit words 1 · median sentence 10 · the written no

> You kiss his cheek, quick, and step back before he can turn it into more. Jake wanted the porch rail. It's all over his face, but he lets it go. "Okay, @player. Next Saturday, then?" He's disappointed, and somehow he's grinning harder than before. "Next Saturday," you say, and your stomach flips. Jake walks backwards down the path, still grinning at your door.

Changed after `v2-prose` (LO, 2026-10-08): Ryan is home, in his room from 22:00 (his schedule), so he opens the front
door from inside. Screens 1–3 re-measured.

## Truth checks

| line | what backs it |
|---|---|
| Ryan's window lit; he opens the door | his night row: his room from 22:00 every night |
| "Next Saturday?" | his thread books the next date (the Saturday date repeat) |
| no garment of hers is named | nothing needs backing |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Jake B 3 (fixed 10-06) |
| Ryan's Warmth drops: choosing Jake | SP2 (Ryan, lowered by) |
| this step as the voice sample | LO, 2026-10-08 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| the Warmth −10 and Want +5 | guess |
