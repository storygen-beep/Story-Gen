# [REVIEW] Scene — jade_01_first_night

| row | answer |
|---|---|
| person · step | npc_jade · 1 (companion) |
| where · when | club · Mon 21:00–23:59, one time (night one) |
| want (test 1) | Jade wants her sister out of that house for one night; the man at the bar wants her |
| next step (test 2) | the game's first hot moment, from a stranger |
| hook (test 3) | Jade: "Come Saturday. I'll get you on the stage." |
| who notices | Jade sees her come back from the corridor and grins |
| clip | a dim club corridor, a man pressing a woman to the wall (explicit) |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| bar | Jade finds her: "Em! You came." Jade goes on | no | "Watch her dance." → watch | — |
| watch | Jade on stage; a man buys Emma a drink: "Stay." | no | "Let him buy you another." → corridor · "Go home." → close | — |
| corridor | **B1** (explicit beat, below) | **yes** | "Pull away and go back to the bar." → close | nerve add +2 |
| close | Jade's hook line | no | "Take the bus home." → downtown | `jade_stage` set 1; energy add −20 |

## Explicit beats (written by v2-prose; measured by `gates.py --beat`, re-run by the author on its own file)

**B1**

> He kisses you hard against the corridor wall. His tongue fills your mouth and tastes like the whiskey he bought you. His hand shoves up under your work skirt, up your thigh, higher. You moan into the kiss. You want more, right now. You grab the front of his trousers. His cock is right there, thick under your palm. He grunts against your lips. "Harder." You squeeze his cock through the wool while his fingers rub over your panties and your hips rock into his hand.

*Measured: 86 words · 5 explicit (cock, kiss, moan) · median sentence 8 · last sentence on the body · ceiling: role:the man at the bar.*
