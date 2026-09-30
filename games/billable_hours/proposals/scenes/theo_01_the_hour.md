# [REVIEW] Scene — theo_01_the_hour

| row | answer |
|---|---|
| person · step | npc_theo · 1 |
| where · when | hotel_bar · Tue–Thu 18:00–21:00, one time · after Martin step 1 |
| want (test 1) | an hour of her, priced; he names it |
| next step (test 2) | first money that is hers, paid for her, not the firm |
| hook (test 3) | "Thursday. Same table. Bring my file." |
| who notices | Martin on Friday, if paid: "Resourceful." |
| clip | a hotel bar, a woman sliding her blazer off, folded bills under her glass (clothed tease) |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| papers | Callahan's errand; Theo: "Your firm bills me six-fifty an hour. This hour I'm paying you." | no | "I'm on the clock for the firm." → parked · "Sit. Keep the jacket on." → talk · "Take the jacket off." → paid · "Two-fifty. That's what my Friday costs." (nerve gte 10) → price · "Take it up with Callahan. (ends his path)" → final | — |
| talk | he tells her what his file is really about | no | "Finish your drink." → close | `theo_hour_talked` set |
| paid | the hour; he looks, she lets him | no | "Take the money." → close | money add +200; `theo_hour_paid` set; nerve add +1 |
| price | he pays; now he knows about Friday | no | "Take the money." → close | money add +250; `theo_hour_paid`, `theo_knows_friday` set; nerve add +2 |
| close | the hook line | no | → downtown | `theo_stage` set 1 |
| parked | "Offer doesn't expire. Neither does your Friday." | no | → downtown | returns in 3 days |
| final | he stays a client | no | → downtown | `theo_final` set |

Note: SP4 said $200; the (d) branch pays $250. The honest week maximum stays $550 (SP4 counts one hour at $200). Flagged for LO: raise `week_income` to $600, or keep (d) at $200.
