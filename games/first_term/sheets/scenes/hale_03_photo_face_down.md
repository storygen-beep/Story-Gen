# [READY] Scene — hale_03_photo_face_down

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–117): Hale's release-1 ladder (`sheets/people/npc_hale.md`, signed). Reworked as **Private coaching**: his office, the photo turned down, his offer, his hand on her shoulder. The canvas id stays. The lines below are mine, signed by LO 2026-11-01, except where marked built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| what changes after | `hale_coaching_offered` on every answer; Laura reads her grade on the portal |
| person · step | `npc_hale` · 3 of 4 (canvas `hale_03_photo_face_down`) |
| where · when | his office · Thursday 18:00-19:30 |
| gate | his step 2 · the boost off |
| want | he turns his wedding photo face-down before he speaks |
| next step | the coaching offer, his hand on her |
| hook | "Thursdays. Half past six. The door will be locked." |
| who notices | Hale; Laura, through the grade |
| what she risks | her grade; Laura reading it |
| what she wears here | the skirt line only in a group on her short-skirt state (as built) |
| explicit? | no: a non-sexual touch, the offer |
| her_line_low · her_line_high | low: "He's your professor. He's married." · high: "You want to know what he'd do next." (the person sheet's pair) | |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** his offer in private, no act of hers · no stage gate in the build (his step 2)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| his office: the photo face-down, the coaching offer, his thumb on her collarbone | Hale; Laura, through the grade portal | her grade; Laura reading it | "When?" · "That isn't coaching." · "Walk out." | turns the photo down; names her grade; the offer | yes | his step 3; `hale_coaching_offered`; Laura's line about the grade |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`hale_03_photo_face_down`** — Dr. Hale's Office · Thu 18:00-19:30 · Dr. Hale there · needs Hale's step = 2 · drinks boost off · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `desk` | His office door is open an inch. | no | "Lean over to see." → `offer` | — |
| `offer` | He reaches over without looking and turns the photo face-down. | no | "When?" → `when` | — |
| | | | "That isn't coaching." → `isnt` | — |
| | | | "Walk out." → `out` | — |
| `when` | His thumb moves once on your collarbone. | no | "Pick up your paper." → `portal` | `hale_coaching_offered` set |
| `isnt` | He takes his hand away, but he doesn't turn the photo back over. | no | "Pick up your paper." → `portal` | `hale_coaching_offered` set |
| `out` | You pick up your bag and walk out without a word. | no | "Keep walking." → `portal` | `hale_coaching_offered` set |
| `portal` | That week your grade goes up on the tuition portal, and Laura reads it at the … | no | "Go back to the faculty floor." → Faculty Floor | Hale's step = 3 · `hale_03_done` set · `hale_office_booked` cleared |

## The lines (mine, signed by LO 2026-11-01)

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

**`offer`:** "He reaches over without looking and turns the photo face-down." · Dr. Hale: "Your grade is a C, @player. I coach students who want to understand the material." · "He comes round the desk and stands behind you, and his hand settles on your shoulder, warm and heavy, and stays." · Dr. Hale: "Psychology starts with a person's sexuality. If you don't understand yours, you won't get past a C." · *(thought, low)* "He's your professor. He's married." · *(high)* "You want to know what he'd do next."
**`when`:** Dr. Hale: "Thursdays. Half past six. The door will be locked." · "His thumb moves once on your collarbone. Then he lets go."
**`isnt`:** Dr. Hale: "Then you'll stay at a C." · "He takes his hand away. He doesn't turn the photo back over."
**`out`:** "You pick up your bag and walk out without a word. His voice follows you into the corridor, calm, not raised." · Dr. Hale: "Thursday, @player. The offer stands."

**Cut:** the built `photo` exits ("Is that a no on my paper, or a yes?", "Just the paper.") and the `paper` no-node; the
`portal` keeps its three Laura lines.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the office, the photo, the speech, the hand, the three answers | `proposals/HALE_R1_LADDER.md`, step 3 (signed 2026-11-01); the speech is LO's words (2026-10-31) |
| no grade on this step | the same: "the grade goes up only if she comes back" |
| the portal kept | the same, "who sees or knows: Laura, through the grade" |
| "Half past six", the locked door | mine: his step 4 window starts 18:30 (`npc_hale.md`) |
