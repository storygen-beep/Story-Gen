# [READY] Scene — martin_02_nobody_knocks

> Signed by LO, 2026-09-30. Written into sheets/ by the author at LO's instruction for this game (NOTES.md).

| row | answer |
|---|---|
| person · step | npc_martin · 2 |
| where · when | study · Fri 19:00–22:00, one time · gate `martin_friday_sat` |
| want (test 1) | her in the chair's arm before he asks |
| next step (test 2) | his hand is on her knee before she answers; it moves up her thigh |
| hook (test 3) | "Same time next Friday. Bring the stub. Leave the jacket downstairs." |
| who notices | nobody: Diane stays upstairs (`diane_blessed_fridays`); office talk read if gte 3 |
| clip | the same study, his hand higher on her thigh (tease) |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| door | "Your chair's free." (If step 1 was sat3: "You didn't move your knee." If martin_power gte 5: "You made me wait a week. Don't do it again.") | no | "Sit." → knee | — |
| knee | his hand, then the question: "What did Callahan say?" | no | "Tell him the truth." → thigh · "Tell him what he wants to hear." (nerve gte 10) → thigh · "Stand up. (not tonight)" → parked | parked: returns next Friday |
| thigh | his hand moves up under her skirt's hem; she lets it | no | "Let him." → close | martin_want add +5; nerve add +1 |
| close | the hook line; the door-choice for step 3 shows locked from here | no | "Go up." → her_room | `martin_stage` set 2 |
