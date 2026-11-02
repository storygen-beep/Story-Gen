# [REVIEW]] Scene — zoe_01_first_party

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 1 (Zoe A 1) = `npc_jake` · 1 (Jake B 1): one canvas |
| where · when | Zoe's bedroom, then the party · Friday 19:00–23:00 |
| gate | `zoe_met` · neither counter started |
| want (test 1) | Zoe: her head in @player's lap · Jake: he watches her, not Zoe |
| next step (test 2) | her first party, Zoe's first dare, and a guy who picks her out |
| hook (test 3) | Jake's number; Zoe's dares go on (A 2) |
| what she wears here (test 8) | Zoe's party dress: the scene adds and equips it |
| her stage here | Good Girl can only refuse the dare; the kiss opens at Curious |
| explicit? | no |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `dress` | Zoe's bedroom: she changes; Zoe watches: "Turn around. Let me see." | no | "Zoe! Eyes up here." → `party` | `zoe_party_dress` added and worn |
| `party` | the party; Zoe: "Kiss someone. Or don't, and I'll keep asking." | no | "Not tonight, Zo." · Curious: "Kiss Zoe." · "Kiss the guy staring." → `jake` | `party_went` set · exhibitionism add +3 |
| `jake` | across the room, a guy watching her: "You've been staring since I came in." | no | "Here's my number." → the party · "Not tonight." → the party (parked) | `jake_number` set · `zoe_step` set 1 · `jake_step` set 1 |

Both counters move on this one canvas (LO, 2026-10-06). A refused dare costs nothing.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Zoe A 1 and Jake B 1 (heat 10-06) |
| Good Girl refuses only; the kiss at Curious | LO, 2026-10-04 (the fixes) |
| the dress equipped by the scene | the truth rule · guess for the mechanism |


## Changed 2026-11-03 (LO: "I think dare refusal shouldn't be counted as done", then "Go"; DECISIONS 133)

- "Not tonight, Zo." still meets Jake (his number or his "Not tonight."; `jake_step` 1) but is no longer Zoe's step 1:
  `zoe_step` stays 0 and `zoe_kiss_refused` is set.
- New screen `zoe_01b_kiss_again` ("Same dare"): a later Friday party, 7 to 11 PM, at least 24 hours after the no, only
  from Curious. Zoe: "You chickened out on me last time. Same dare. Kiss someone. I told you I'd keep asking." From the
  second no, also: "That's twice you've said no, babe. I'm counting." Yes: "Kiss Zoe." or "Kiss the guy by the
  speakers." (Exhibitionism +3, her step 1). No: "Boo. Next Friday, then. I'm not giving up on you." (`zoe_refused` +1,
  back in a week). Lines mine, signed by LO 2026-11-03 ("Signed").
- Her card while she waits: "You said no to her kiss dare. She said she'd keep asking." · goal Reach Curious (Corruption 20).
