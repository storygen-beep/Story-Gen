# [READY] Scene — street_seen
> Changed 2026-11-09 (DECISIONS 209, LO: "Go ahead"): her reaction drifts when she does it again, new section at the end. Signed by LO 2026-11-09 ("Sign them").
> Changed 2026-11-09 (DECISIONS 208, LO: "I say we tackle 1st fewer cloths first"): more clothes, round 2, new section at the end. Signed by LO 2026-11-09 ("Sign them").
> Changed 2026-11-08 (DECISIONS 205): everyday clothes by stage, new section below. Re-signed by LO 2026-11-08 ("Sign them").
> Signed by LO: LO, 2026-11-04.
> Changed 2026-11-04, LO's answers: skirt and no bra cap at 39, no panties at 59, both meters (F); signed by LO 2026-11-04.
> Changed 2026-11-04, writing pass: lines brought to the build (fresh text per room, her voice by level, the reader's fixes); signed by LO 2026-11-04.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. Both meters cap at 19 (DECISIONS 176).

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04.

> The signed plans behind this page: `proposals/COPY_FIXES_C.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): Vance's line ends with what comes next.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–120). From the signed meters system (`sheets/systems/meters.md`, rule 2, "wearing it out raises both";
> `wardrobe.md`). No explicit screen; the lines are mine except Vance's, which are his signed lines.

| row | answer |
|---|---|
| system · place | the meters · `street` |
| when | once a day (`out_shown_today`, cleared in the daily tick), the first time she crosses the street in a level |
| gate | what she wears: a short skirt, or no bra (level 1); no panties out of jeans, leggings, shorts (level 2) |
| pays | **the first day out in each level:** corruption add +1 · exhibitionism add +1 (`street_first_l1` / `street_first_l2` set) · **every day after:** exhibitionism add +1 · skirt and no bra cap at 39, no panties at 59 (LO, 2026-11-04) |
| who sees | Mr. Vance if he is at his house, else the shop guy (08:00-18:00), else a car |
| want | Vance: his eyes up her legs; he pats the step beside him |
| next step | "He'll be on his porch tomorrow evening. He always is." |
| hook | his Want +2 each time he sees her; his porch |
| from `cafe_footfall` 10 | the witness line gains the café: "You're the girl from the café." (`job.md`, the café reaches the rest of her life) |
| what she wears here | read from her worn state; each line names only what the group's condition backs |
| explicit? | no (under 3 list words) |

## The lines, by witness and level (mine, except Vance's signed lines)

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

| witness | level 1 (short skirt, or no bra) | level 2 (no panties) |
|---|---|---|
| Mr. Vance (`npc_vance.md`) | short skirt: "Mark's girl has good legs." He doesn't pretend to read his paper. (signed) · no bra: "He sets the paper down. He looks at your chest and doesn't look away." | "A breeze lifts your skirt as you pass his gate. Mr. Vance stands up off his chair." |
| the corner-shop guy | "He comes out from behind the counter to stack a box that doesn't need stacking, and watches you all the way past." | "He drops his change on the step. He doesn't pick it up until you've turned the corner." |
| a car slowing down | "A car slows beside you. The window comes down halfway. It stays with you to the end of the street, then goes." | "A car slows, then stops. Someone whistles. You don't walk faster." |
| footfall 10 (any witness) | + "You're the girl from the café." | + "You're the girl from the café." |

Vance's covered line ("A nod from the porch. Nothing else.") stays in his own porch hub; covered pays nothing here.
Vance's Lust add +2 when she passes in a level (his signed number, `npc_vance.md`).

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`street_seen_skirt`** — Your Street · needs not `out_shown_today` · in short skirt · underwear on · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `seen` | He doesn't pretend to read his paper. | no | "Keep walking." — 8 versions, by flags, hour, who's there → Your Street | Exhibitionism +1 (cap 39) · `out_shown_today` set · varies: Corruption, Mr. Vance's Want, `street_first_l1` set |

**`street_seen_nobra`** — Your Street · needs not `out_shown_today` · no bra · not in short skirt · underwear on · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `seen` | Mr. Vance sets the paper down. | yes | "Keep walking." — 8 versions, by flags, hour, who's there → Your Street | Exhibitionism +1 (cap 39) · `out_shown_today` set · varies: Corruption, Mr. Vance's Want, `street_first_l1` set |

**`street_seen_nopanties`** — Your Street · needs not `out_shown_today` · no underwear · not in jeans · not in leggings · not in shorts · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `seen` | A breeze comes down the street as you pass the landlord's gate, and there's nothing under … | yes | "Keep walking." — 8 versions, by flags, hour, who's there → Your Street | Exhibitionism +1 (cap 59) · `out_shown_today` set · varies: Corruption, Mr. Vance's Want, `street_first_l2` set |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`street_seen_nobra` · `seen`** — 233 words · 5 counted: tits, nipple, tits, tits, tits · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit

> Mr. Vance sets the paper down. He looks at your tits, at your nipples pushing at the cloth, and doesn't look away. He nods at the step beside him. Not tonight. You keep walking.
>
> He'll be on his porch tomorrow evening. He always is.
>
> The shop guy comes out from behind the counter to stack a box that doesn't need stacking. His eyes are on your tits, loose under your clothes, all the way past. He says it to your back as you go past, and you don't turn round.
>
> Cold out today, is it? Come in and warm up.
>
> He'll be out front tomorrow.
>
> A car slows beside you. The window comes down halfway, and the driver is staring at your tits. It stays with you to the end of the street, but you never look in, and it goes.
>
> Jesus, look at those. Get in, I'll give you a lift.
>
> Keep driving.
>
> The same car's parked at the corner the next time you look.
>
> A car slows beside you. The window comes down halfway, and the driver is staring at your tits. It stays with you to the end of the street, but you never look in, and it goes.
>
> Jesus, look at those. Get in, I'll give you a lift.
>
> Keep driving.
>
> The same car's parked at the corner the next time you look.
>
> You're the girl from the café.

**`street_seen_nopanties` · `seen`** — 218 words · 4 counted: ass, ass, ass, ass · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit

> A breeze comes down the street as you pass the landlord's gate, and there's nothing under your clothes to stop it. It lifts your hem and runs cool over your bare ass. Mr. Vance stands up off his chair with his eyes on your hips, and takes one step toward the gate, but you don't stop. Not tonight.
>
> He'll be on his porch tomorrow evening. He always is.
>
> The shop guy drops his change on the step and stares at your ass, like he knows there's nothing under your clothes.
>
> Come in a minute.
>
> You don't. He doesn't pick the change up until you've turned the corner.
>
> I mean it. Come in a minute. Just a minute.
>
> He'll be out front tomorrow.
>
> A car slows, then stops. Someone inside whistles at your ass.
>
> Get in.
>
> You don't walk faster, and you don't get in.
>
> I said get in. I saw that breeze, sweetheart.
>
> Keep driving.
>
> The same car's parked at the corner the next time you look.
>
> A car slows, then stops. Someone inside whistles at your ass.
>
> Get in.
>
> You don't walk faster, and you don't get in.
>
> I said get in. I saw that breeze, sweetheart.
>
> Keep driving.
>
> The same car's parked at the corner the next time you look.
>
> You're the girl from the café.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, once a day, first day both meters, the three witnesses | `meters.md` rule 2 (signed 2026-11-01) |
| the levels | `meters.md` rule 1 · `wardrobe.md` |
| the café line | `job.md` (signed) |
| the lines, the flag names | mine, confirmed by LO 2026-11-01 ("Continue") |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

A hook line, proposed (LO asked whether a line solves it). Each line names a thing that is in the game and comes next, so it is true; a line that points at nothing would break the truth rule instead.

| witness | the closing line (mine, signed) | what it points at |
|---|---|---|
| Mr. Vance | "He'll be on his porch tomorrow evening. He always is." | his porch row, every evening; his Lust rises each time she passes, so his line changes |
| the corner-shop guy, a car | (no line: nothing of theirs comes next) | the street's "You're the girl from the café." at footfall 10 is the hook there |

## Changed 2026-11-02 (reader a3, `READER_FAILS_A3.md`, signed by LO 2026-11-02; DECISIONS 131)

- Rows 46–48 (hook). The corner-shop render now closes on "He'll be out front tomorrow." (the shop opens every day 07:00–22:00, `corner_shop.md`). Both car renders close on "The same car's parked at the corner the next time you look." (one line). This replaces the 2026-11-01 "no line" row above.
- Row 55 (the no-panties offers refused in narration): accepted, call B. No change.

## The new pieces (2026-11-08, DECISIONS 205)

Four more looks, each gated on its piece's stage and paying Exhibitionism +1 to that stage's top: the crop top and the
bodycon dress (20, cap 39), the micro shorts (40, cap 59), the plunge dress with no bra (60, cap 79). Same witnesses
(Vance on his porch, the shop guy by day, a car at night), each with his own line. Two street accidents: the micro shorts
on the bus-stop bench ("Stay sitting.", from 40, cap 59) and the plunge dress slipping ("Let it be for a few steps.", from
60, cap 79). 1 in 4, one a day, with the other street events.

## More clothes, round 2 (2026-11-09, DECISIONS 208)

Three new looks, once a day like the others: the split skirt and the sequin dress at Daring (20, pay to 39), the backless
dress at Watched (60, pay to 79, no bra). Vance, the shop guy or a car, by the hour, each with his own line. One new
random event: the wind in the slit of the split skirt shows her panties (the fix at any stage; letting it be at 40, to 59).

## Repeats (2026-11-09, DECISIONS 209)

Each of the 11 street looks (the skirt, no bra, no panties, the low-cut top, the crop top, the bodycon, the micro shorts, the plunge, the split skirt, the sequin and the backless dress) keeps a hidden visit count. The screen after her yes gets one paragraph that moves with it: the first time, the
next few (2 to 4), and once it's a habit (5 and up). It's about her body's habit and the watchers' habit, so it is true at
every stage; her stage thought stays as it was. Lines: `iterations/002/build_scripts/drift.py`.
