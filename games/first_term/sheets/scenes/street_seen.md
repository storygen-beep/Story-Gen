# [REVIEW] Scene — street_seen

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_C.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): Vance's line ends with what comes next.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–120). From the signed meters system (`sheets/systems/meters.md`, rule 2, "wearing it out raises both";
> `wardrobe.md`). No explicit screen; the lines are mine except Vance's, which are his signed lines.

| row | answer |
|---|---|
| system · place | the meters · `street` |
| when | once a day (`out_shown_today`, cleared in the daily tick), the first time she crosses the street in a level |
| gate | what she wears: a short skirt, or no bra (level 1); no panties out of jeans, leggings, shorts (level 2) |
| pays | **the first day out in each level:** corruption add +1 · exhibitionism add +1 (`street_first_l1` / `street_first_l2` set) · **every day after:** exhibitionism add +1 · each under her stage cap |
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
| Mr. Vance (`npc_vance.md`) | short skirt: "Mark's girl is growing up." He doesn't pretend to read his paper. (signed) · no bra: "He sets the paper down. He looks at your chest and doesn't look away." | "A breeze lifts your skirt as you pass his gate. Mr. Vance stands up off his chair." |
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

**`street_seen_nopanties` · `seen`** — 213 words · counted: ass, ass, ass · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit · **past the ceiling: pussy**

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
