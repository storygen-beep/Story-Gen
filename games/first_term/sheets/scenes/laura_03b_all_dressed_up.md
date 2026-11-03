# [REVIEW] Scene — laura_03b_all_dressed_up

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): both endings point ahead.

> **New 2026-11-01, signed by LO 2026-11-01 ("Go ahead")** (DECISIONS 99–114). From Laura's signed release-1 ladder
> (`sheets/people/npc_laura.md`; `proposals/LAURA_R1_LADDER.md`). It reworks the built canvas `laura_06_take_me_with_you`
> (the id stays; that sheet is marked reworked). No explicit screen; the lines below are mine, for LO to read.

| row | answer |
|---|---|
| person · step | `npc_laura` · 3 of 4 (canvas `laura_06_take_me_with_you`) |
| where · when | her room, `home_master_bedroom` · Saturday 17:00–18:30, Laura dressing |
| gate | her Love (`warmth`) 20 · `laura_step` eq 2 · the boost off |
| want | she leaves her door open while she dresses (the leak) |
| next step | she asks to be zipped, then asks if she's still someone you'd look at |
| hook | `laura_lonely`: her alone-in-bed screen names this night after it |
| who notices | Ella; Mark, not looking (he calls up from downstairs) |
| what she wears here | Laura: her good dress (named in prose, not an item) · Ella: not named |
| explicit? | no: an ask |
| her_line_low · her_line_high | low: "That's your mom. Go to bed." · high: "She's lonely, and you can't stop watching her be lonely." | The low line sits on the parked no; the high line is the thought on `bed`. |
| what changes after | `laura_lonely` set; the alone-in-bed line names this night |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `zip` | her door open; Laura at the mirror in her good dress, the zip open to the small of her back: "Zip me up, sweetheart? Mark's useless at it." (built line) | no | "Hold still." → `zipped` · "Ask Mark." → `no` (parked) | none |
| `zipped` | you zip her; Mark calls up the stairs that he's off to the bar; the front door goes | no | → `bed` | none |
| `bed` | Laura sits on the end of the bed, dressed up, nowhere to go: "Do I still look like someone you'd look at?" | no | "You look beautiful, Mom." → the hall · Say nothing. → `quiet` | first exit: Laura's Love add +5 · `laura_lonely` set · `laura_step` set 3 · `laura_06_done` set |
| `quiet` | you sit beside her and say nothing; she leans her head on your shoulder | no | "Goodnight, Mom." → the hall | Laura's Love add +5 · `laura_lonely` set · `laura_step` set 3 · `laura_06_done` set |
| `no` | "Mark. Right." She does the zip herself, badly, halfway (built) | no | → the hall | Laura's Love add −1 · the step waits a week |

**Dropped from the built canvas:** the `lean` screen (your fingers on her ribs, her hands over them) and the `ask`
("Take me with you one night", `laura_asked_to_come`): the climb toward Ella is cut.

## The lines (not explicit; mine, for LO to read)

**`zipped`:** "You pull the zip up slowly, all the way to her shoulder blades. She smooths the dress over her hips and turns side-on to the mirror." · Mark, from the bottom of the stairs: "Laur? I'm off to the bar with the guys. Don't wait up." · "The front door goes before she can answer. Laura stands very still in front of the mirror."

**`bed`:** "She sits down on the end of the bed in her good dress, her heels in her hand. Her lipstick is perfect. She has nowhere to go." · Laura: "Do I still look like someone you'd look at?" · *(thought)* "She's asking you, because nobody else is here to ask."

**exit "You look beautiful, Mom.":** Laura: "Liar." "She says it smiling, and her eyes are wet."

**`quiet`:** "You sit down beside her. You don't say anything. After a while she puts her head on your shoulder, and her hair smells of the perfume she put on for nobody." · Laura: "Thank you, sweetheart."

## Why — the source of each key choice

| key choice | source |
|---|---|
| the zip, Mark leaving, the ask | `proposals/LAURA_R1_LADDER.md`, step 3 (signed 2026-11-01) |
| "or she says nothing" as a second yes | the same row, "how Ella says yes" |
| the parked no "Ask Mark." and its screen | the built canvas (kept) |
| "the bar with the guys" | guess: Mark has no Saturday-evening schedule row after the garage (17:00); he leaves the house here |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

A hook line, proposed (LO asked whether a line solves it). Each line names a thing that is in the game and comes next, so it is true; a line that points at nothing would break the truth rule instead.

| node | the closing line (mine, signed) | what it points at |
|---|---|---|
| `liar`, `quiet` | "On weeknights now, her bedroom door doesn't quite close." | her gap (Sun–Fri 22:00) and her step 4 |
