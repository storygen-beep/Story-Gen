# [READY] Scene — martin_01_first_friday

> Signed by LO, 2026-09-30. Written into sheets/ by the author at LO's instruction for this game (NOTES.md).

| row | answer |
|---|---|
| person · step | npc_martin · 1 |
| where · when | study · Fri 19:00–22:00, one time |
| want (test 1) | her close, grateful, and reading him for what he'll allow |
| next step (test 2) | first time she chooses how close to sit |
| hook (test 3) | "Callahan will ask me about you. What should I tell him?" |
| who notices | Diane knocks with his coffee, approves, and from now on stays upstairs on Fridays |
| clip | a lamp-lit study, a man in a leather armchair, a young woman on its arm, his hand on her knee (tease) |

## Branch map — one row per screen

| node | what happens | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| door | "Come in, Emma." The money's already his. He asks for her pay stub | no | "Hand him the stub." → stub | — |
| stub | he reads it like a review; pats the arm of his chair: "Sit." | no | "Stay by the desk." → parked · "Sit on the arm." → sat1 · "Lean into his shoulder." → sat2 · "Sit, and leave his hand where it lands." (nerve gte 5) → sat3 · "Leave. (ends his path)" → final | parked: `martin_friday_parked` set; martin_power add +5 · final: `martin_final` set |
| sat1 / sat2 / sat3 | one node each: his reaction, her line at her nerve band | no | "Stay while he reads." → diane | `martin_friday_sat` set; martin_want add +5; nerve add +1 (sat2), +2 (sat3) |
| diane | Diane knocks: "Look at you two. I knew you'd come round to him." | no | "Smile at your mother." → close | `diane_blessed_fridays` set |
| close | door shut: "Your mother thinks this is sweet." Then the hook line | no | "Go up to bed." → her_room | `martin_stage` set 1 |
| parked | "Next Friday, then." | no | "Go up." → her_room | step returns next Friday |
| final | he nods; Fridays stay a transaction | no | "Go up." → her_room | — |

## Voice sample — written out in full

*door*

> Martin's study door is open for once. He is in the leather armchair with a glass of whisky, and he doesn't get up. "Come in, Emma. Shut the door." You shut it. He already has your $250. He took it at breakfast and didn't count it. So you don't know what this is.

*stub*

> "Your pay stub. Let me see it." You hand it over. He reads it slowly, the way Callahan reads a contract. "Seventy a day. I want to see what Callahan thinks you're worth." Then he pats the arm of his chair. "Sit." It is not a question. Your stomach drops, but your feet are already moving.

*sat2 (the branch that leans in and leaves his hand; sat1 and sat3 are shorter variants)*

> You sit on the arm and lean into his shoulder. He smells of whisky and aftershave. He doesn't look up from the stub, but his hand settles on your knee. It stays there. It is warm and heavy, and you can feel every one of his fingers through your tights. You don't move it. You don't want to.

*diane*

> Someone knocks. Your mother comes in with his coffee and stops. Then she smiles, wide and relieved. "Look at you two. I knew you'd come round to him." She puts the cup down and goes. You hear her on the stairs, going up, not coming back.

*close*

> The door clicks shut behind her. Martin's hand hasn't moved. "Your mother thinks this is sweet," he says. He folds the stub and hands it back. "Callahan will ask me about you. What should I tell him?"

*Measured with `gates.py --beat`: 250 words over 5 screens · median sentence 6 · 0 dashes · but 8.0 / and 40.0 per 1,000 (inside the field's range; printed, not judged under 500 words) · not explicit, by design (a tease step).*
