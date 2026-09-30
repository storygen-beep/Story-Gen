# [REVIEW] Scene — ethan_01_red_ink

| row | answer |
|---|---|
| person · step | npc_ethan · 1 |
| where · when | landing · Mon–Thu 21:00–23:30, one time · gate `firm_day1_done` |
| want (test 1) | her gone from the firm; and he can't stop looking |
| next step (test 2) | the first time he looks and she lets him |
| hook (test 3) | "Lock it tomorrow." / "It doesn't lock." |
| who notices | Martin at breakfast: "Something wrong with your eggs, Ethan?" |
| clip | steam, a dark landing, a door gap, a woman glancing over her shoulder (explicit on the (c) branch) |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| memo | her memo on her bed in red ink; the note reads her start flag | no | "Take a shower." → shower | — |
| shower | the latch doesn't catch; his door opens across the landing | no | "Wedge it shut with a towel." → parked · "Leave it an inch, back to the door." → inch · "Leave it open and turn round." → seen · "Call through the gap." → callout · "Ask Martin to fix the lock. (ends his path)" → final | — |
| inch | he stands in the gap; she doesn't turn | no | "Finish." → close | `ethan_saw_bathroom` set; nerve add +1 |
| seen | **B2** (explicit beat, below) | **yes** | "Let him look." → close | `ethan_saw_front` set; nerve add +2 |
| callout | "You can stop pretending you came out for water." He goes red, doesn't leave | no | "Let him stay." → close · he may walk off (nerve lt 10) | `ethan_saw_front` set; nerve add +1 |
| close | his door; the hook line | no | "Go to bed." → her_room | `ethan_stage` set 1 |
| parked | he waits; nothing | no | → her_room | returns in 2 days |
| final | Martin fixes the lock next day; Ethan stays cold | no | → her_room | `ethan_final` set |


## Explicit beats (written by v2-prose; measured by `gates.py --beat`, re-run by the author on its own file)

**B2**

> You turn round under the spray and let him look. The door hangs open a hand's width. Ethan stands on the landing with an empty glass. His eyes go straight to your tits. Water runs off your hard nipples and down your stomach. You arch your back so he gets all of it. "Put some clothes on." His voice comes out rough. He stays right where he is. His stare slides lower, over your naked hips, and you turn slowly to give him your wet ass.

*Measured: 86 words · 4 explicit (ass, naked, nipple, tits) · median 9 · last sentence on the body · ceiling: Ethan early (ass, tits).*
