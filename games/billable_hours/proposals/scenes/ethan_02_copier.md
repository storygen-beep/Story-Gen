# [REVIEW] Scene — ethan_02_copier

| row | answer |
|---|---|
| person · step | npc_ethan · 2 |
| where · when | firm · Thu 18:00–21:00, one time |
| want (test 1) | to win the argument about her job, and to be near her with nobody watching |
| next step (test 2) | the tease comes back in his mouth: "You didn't shut it." |
| hook (test 3) | he leaves her memo on the copier with one line on it: "Better." |
| who notices | office talk add +1 (the cleaner sees them) |
| clip | an empty office after hours, a copier, a man close behind a woman (tease) |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| copier | he's alone with her memo; "You didn't shut it." | no | "No. I didn't." → close-in · "Get back to your desk, Ethan." → parked | parked: returns next Thursday |
| close-in | he stands behind her at the copier; hands on the edge either side of her | no | "Lean back into him." (nerve gte 10) → hook · "Stay still." → hook | nerve add +1 |
| hook | he steps away; the memo, "Better." | no | "Take the bus home." → downtown | `ethan_stage` set 2; office_talk add +1 |
