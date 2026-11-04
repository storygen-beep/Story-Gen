# [READY] Scenes — the walk-ins on the refill places (B21-B24), and Laura's lace set (Q12)
> Signed by LO: LO, 2026-11-04.
> Changed 2026-11-04, writing pass: lines brought to the build (fresh text per room, her voice by level, the reader's fixes); signed by LO 2026-11-04.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. A next-step row on each of the four, from the build; Mark's "Give me a minute."

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. She leaves the lace set in what she came in (`remember_outfit`, `restore_outfit`).

> New 2026-11-04: written from the build, for LO to read and sign. LO's answers of 2026-11-04: Q4 ("Add walkins in
> this release itself") at the four refill places the gate `a refill place rolls an event` listed, and Q12 (Laura's
> black lace bra and panties become wardrobe items, worn in `walkin_wardrobe_mark`). The build does not read this
> sheet; the canvases live in `iterations/002/build_scripts/walkins.py` (B21, B22, B6) and `walkins_out.py` (B23, B24).

## How each one works, as built

The same machine as the walk-ins at home and outside (`walkins_home.md`, `walkins_out.md`):

| row | answer |
|---|---|
| where it starts | she clicks the refill activity; on entry the game rolls, and a hit shows the walk-in instead |
| odds | 0.25 · 0.35 · 0.45 by her Exhibitionism band (under 20 · 20–39 · 40+) |
| screen 1 | the moment, once a day per walk-in; Lust +2 on its only button where the walker has a Lust meter (Ryan, Mark) |
| screen 2 | her answer: the cover pays 0; one bolder button per band pays her Exhibitionism +1, capped at the band's top (19 · 39 · 59) |
| no meter | Zoe, the cocky guy: nothing of theirs moves; a flag records it |
| once a day | each sets its own `walkin_*_today`, cleared at midnight |
| a miss | her activity, as it is today |
| the refill | a walk-in pays the refill only when the screen shows her doing it (LO, 2026-11-04): the nap and the sink do; the garden and Zoe's bathroom do not, and the activity is still there after them |

---

## B21 · her nap (`room_nap`)

### `walkin_nap_ryan`

| row | answer |
|---|---|
| who · when | Ryan, from his room · Saturday and Sunday, the nap starting 10:00–12:00 (after Kayla's Saturday row in his room ends at 10:00; the two-hour nap ends before his 14:00 TV row) |
| want | his: he comes in for her phone charger and stands looking at her asleep on the covers |
| her clothes | read on screen 2, when she wakes: towel come undone · naked · bra and panties · sleep shirt · short skirt · dressed · half dressed |
| his leak (H7) | under his Want 40 he goes red, turns to the wall and holds the charger in front of his shorts; from 40 he leans on her desk and keeps looking |
| screen 1 | she lies down; "Sleep (2h)." spends the nap it replaces (120 minutes, energy +30, cap 100) · his Lust +2. The one walk-in that pays the refill: it is her nap, slept through before the door clicks (reader pass 4, 2026-11-04) |
| her answers | "Pull the blanket over you." 0 · "Don't move." +1, cap 19 · "Stretch." (Daring) +1, cap 39 · "Roll onto your back." (Showing) +1, cap 59 |
| not yet | "Not now. Not with Mark down the hall." (on her Showing answer) |
| next step | her bolder answer at the next band; nothing after "Roll onto your back." this release |
| hook | `ryan_saw_nap` is set; nothing reads it this release · "Lock your door next time. Or don't." |
| every way out | "Get up." back to her room |
| words | Ryan's early column: ass, tits |

## B22 · the lounger (`garden_sun`)

### `walkin_garden_mark`

| row | answer |
|---|---|
| who · when | Mark, out of the kitchen on his Sunday table row · Sunday 10:00–18:00 (Laura is out until her 18:00 kitchen row) · after `mark_saw_her` |
| want | his: he comes out with a beer and the hose for the tomatoes and stops on the back step |
| her clothes | read on screen 1: topless · bra only · anything else |
| his leak (H7) | under his Want 20 he turns his back and waters the tomatoes, the beer held in front of his jeans; 20–49 he waters the same pot over and keeps looking; from 50 he drops the hose and looks |
| screen 1 | "He's stopped on the step." · his Lust +2 |
| her answers | "Sit up and cover up." 0 · "Stay as you are." +1, cap 19 · "Stretch your legs out." (Daring) +1, cap 39 · "Turn over for him." (Showing) +1, cap 59 |
| not yet | "Not yet." (Daring) · "Not today. That's all you get." (Showing, from his Want 20) |
| next step | her bolder answer at the next band; nothing after "Turn over for him." this release |
| hook | `mark_saw_garden` is set; nothing reads it this release · "Tomatoes need doing every Sunday." |
| the way out | "Go in." after the cover; "Get up off the lounger." after the others |
| words | Mark's early column: legs, ass |

## B23 · the women's toilet (`toilet_wash`)

### `walkin_toilet_zoe`

| row | answer |
|---|---|
| who · when | Zoe, from her lunch row in the canteen · Monday–Friday 12:15–12:45 · after `zoe_met` |
| want | hers: in to fix her lipstick, she pushes open the stall with the broken lock while @player washes, and leans on the frame to look |
| her clothes | read on screen 1: top up with a bra · top up with no bra · anything else |
| screen 1 | "She doesn't shut the door." · hygiene add +15 (she washes, as `toilet_wash` pays; the one walk-in that pays its refill, pass 4) |
| her answers | "Shove the door shut." 0 · "Keep washing." +1, cap 19 · "Turn round and do your back." (Daring) +1, cap 39 · "Let her look." (Showing) +1, cap 59 |
| not yet | "Later. Not in a toilet stall. But later, babe." (Showing) |
| next step | her bolder answer at the next band; nothing after "Let her look." this release |
| hook | `zoe_saw_toilet` is set; nothing reads it this release · "I know where to find you at lunch now." · "Later. Not in a toilet stall. But later, babe." |
| every way out | "Done." back to the toilets |
| words | Zoe's early column: tits, ass |
| the host | `toilet_wash` lives in `3_activities.toml`; its `substitutions` line is pasted there by hand and `extras.py` checks it against `walkins_out.RULES` |

## B24 · Zoe's bathroom (`zoe_bathroom_face`)

### `walkin_zoebath_cocky`

| row | answer |
|---|---|
| who · when | the cocky guy, on his party rows in Zoe's flat · Friday 23:00–00:00 · Saturday 00:00–02:00 · after `cocky_guy_met` |
| want | his: the bolt is loose, he barges in for the toilet, finds her bent over the sink doing her liner, and stays to look |
| her clothes | read on screen 1: no bra · a short skirt |
| how he looks | openly, from the first look: he is from outside the house (H7) |
| screen 1 | "He doesn't back out." · nothing moves (he has no meter) |
| her answers | "Yank the door open and point." 0 · "Finish your liner." +1, cap 19 · "Lean in closer to the mirror." (Daring) +1, cap 39 · "Turn round and lean back on the sink." (Showing) +1, cap 59 |
| not yet | "Not in Zoe's bathroom. Not yet." (Showing) |
| next step | her bolder answer at the next band; nothing after "Turn round and lean back on the sink." this release |
| hook | `cocky_saw_bathroom` is set; nothing reads it this release · "Find me later and I'll tell you." |
| every way out | back to Zoe's living room: "Open the door." after "Yank the door open and point."; "Back to the party." after the other three |
| words | strangers' and extras' list (DECISIONS 41): tits, nipples, ass, cock, wet, clit |

---

## Q12 · Laura's lace set in `walkin_wardrobe_mark` (B6)

| row | answer |
|---|---|
| the items | `laura_lace_bra` "Laura's black lace bra" (bra) · `laura_lace_panties` "Laura's black lace panties" (underwear) · type `lingerie`, beauty 3, corruption 2 · no price, so no shop shows them |
| screen 1 | she finds the set under the stockings in Laura's drawer, strips (her towel, or her own things, in a heap on Laura's bed) and puts both on |
| on the moment's button | everything she wore comes off and the lace pair goes on, so from screen 2 on the sidebar shows what the words say |
| every way out | both pieces are removed (back in Laura's drawer, never in her wardrobe), and she gets back what she wore when she came in (`restore_outfit`), the towel too |
| what she leaves in | what she came in, as LO asked: `remember_outfit` on the moment's button, `restore_outfit` on every way out (LO, 2026-11-04). The same two actions run the tub, the party house soak, Ryan's exits, Zoe's hot tub and Mark's "Give me a minute." After a shower, "Get dressed." gives back what she wore before it. The opening's "Get dressed." and the café's "Clock out." are unchanged |
| new line | on "Let him look.", after he goes: she looks at herself in Laura's set a second longer, then folds it back into the drawer |
