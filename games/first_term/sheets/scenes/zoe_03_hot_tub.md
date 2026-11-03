# [REVIEW] Scene — zoe_03_hot_tub

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–118): Zoe's release-1 ladder (`sheets/people/npc_zoe.md`, signed). Changed: the gate comes down to Curious and Daring (Corruption 20 · Exhibitionism 20, was 40/40), so the dares open before Bold; her voice row. The screens and the signed kiss beat stand.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. **Zoe's voice sample, in full:** every screen written by
> `v2-prose` from a spec, measured with `gates.py --beat`, pasted here. LO picked this step.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 3 (Zoe A 3) |
| where · when | the party house hot tub · Saturday 20:00-23:30 |
| gate | her step 2 · Corruption 40 · Exhibitionism 40 · the boost off · pays +3 each, cap 79 |
| mixed act? | yes: topless, seen by Zoe, and a kiss: both meters, as built (+3 each) |
| her_line_low · her_line_high | low: "It's a dare. It doesn't count." · high: "You want her to dare you something worse." (the person sheet's pair) | |
| want | "There's a hot tub Saturday. Just us." (A 2); her knee against @player's |
| next step | topless for Zoe alone, and @player kisses her first |
| hook | "You could've asked." Zoe answers on her couch (A 4); Ryan sees her come home |
| what she wears here | she strips to her bra and panties at the tub's edge (top and bottom off on the first screen); "it" is her bra, and taking it off takes the bra off |
| only Zoe sees her | her friends go inside first (LO, 2026-10-08): SP2's group rule holds |
| the crude-word ceiling | Zoe's middle column: tits, nipples, wet · early: tits, ass (LO, 2026-10-08) |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** naked by choice for someone she knows, and a kiss · Bold · Showing (40)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| her friends go in; topless for Zoe alone, and Zoe kisses her | Zoe; her friends, until the door shuts | being seen topless; a girl's mouth on hers | "Take your bra off." or "Let her look." | she pulls her into the tub; the kiss | yes | her step 3; home late; Ryan's Want +5 at the door |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`zoe_03_hot_tub`** — The Party House · Sat 20:00-23:30 · needs Zoe's step = 2 · Corruption 40+ · Exhibitionism 40+ · drinks boost off · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `tub` | Zoe drags you into the hot tub on the back deck, laughing. | no | "Stay in the water." → `alone` | changes her clothes (unequip) |
| `alone` | The door slides shut behind her friends. | no | "Take your bra off." (bra on) → `kiss` | unequip plain bra · unequip sports bra |
| | | | "Let her look." (no bra) → `kiss_bare` | — |
| | | | "Not tonight, Zo." (1h)" → `home_no` | changes her clothes (equip) |
| `kiss` | You get your bra off and toss it on the deck. | yes | "Hold her." → `asked` | Exhibitionism +3 (cap 79) · Corruption +3 (cap 79) |
| `kiss_bare` | You don't have anything to take off. | yes | "Hold her." → `asked` | Exhibitionism +3 (cap 79) · Corruption +3 (cap 79) |
| `asked` | Zoe pulls back, flushed and breathless, and laughs. | no | "Go home (6h 40m)." (20:00-21:00) → `home` | Zoe's step = 3 · `zoe_03_done` set · changes her clothes (equip) |
| | | | "Go home (5h 40m)." (21:00-22:00) → `home` | Zoe's step = 3 · `zoe_03_done` set · changes her clothes (equip) |
| | | | "Go home (4h 40m)." (22:00-23:00) → `home` | Zoe's step = 3 · `zoe_03_done` set · changes her clothes (equip) |
| | | | "Go home (3h 40m)." (23:00-00:00) → `home` | Zoe's step = 3 · `zoe_03_done` set · changes her clothes (equip) |
| | | | "Go home (2h 40m)." (00:00-20:00) → `home` | Zoe's step = 3 · `zoe_03_done` set · changes her clothes (equip) |
| `home_no` | She doesn't sound annoyed. | no | "Go to bed." — 2 versions, by hour → Your Room | back in 7 days · varies: `came_home_late` set, `late_party` set |
| `home` | You let yourself in. | no | "Go to bed." — 2 versions, by hour → Your Room | Ryan's Want +5 · back in 7 days · varies: `came_home_late` set, `late_party` set |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`zoe_03_hot_tub` · `kiss`** — 120 words · 9 counted: tits, nipple, kiss, moan, tits, nipple, nipple, ass, tits · ceiling: Zoe's middle column: tits, nipples, wet

> You get your bra off and toss it on the deck. The steam rolls over your bare tits. The night air is cold on them, so your nipples go hard above the water. Zoe stares at them.
>
> Babe.
>
> She breathes.
>
> Look at you.
>
> You grab the back of her neck and pull her in. You kiss her hard, open-mouthed, until she moans into you. Her tits press flat against yours. Her nipples drag across your nipples, hard and wet. Her thigh slides between your thighs under the water. It presses up, slow and firm. Her breath catches. Your hands run down her slick back to her ass. You grab it with both hands and pull her tits tight against yours.

**`zoe_03_hot_tub` · `kiss_bare`** — 128 words · 9 counted: tits, nipple, kiss, moan, tits, tits, nipple, ass, nipple · ceiling: Zoe's middle column: tits, nipples, wet

> You don't have anything to take off. You just rise up out of the water to your waist and let her look. Your bare tits come up out of the steam, wet and shining, and the night air hits them, so your nipples go hard. Zoe's mouth falls open.
>
> Babe.
>
> She breathes.
>
> You came in like that? All night?
>
> You grab the back of her neck and pull her in. You kiss her hard, open-mouthed, until she moans into you. Her tits press flat against your bare tits. Her wet nipples drag across yours. Her thigh slides between your thighs under the water and presses up, slow. Your hands run down her slick back to her ass, and you squeeze it and pull her nipples tight against yours.

## Truth checks

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

| line | what backs it |
|---|---|
| "All term she has dared you" | Zoe A 1 and A 2 are in her counter; this step needs them |
| her friends gone; only Zoe sees | the `alone` screen sends them in before anything comes off |
| "Zoe's lipstick on your neck" | the kiss on the screen before |
| Ryan awake at his door | his night row, his room, every night |
| no garment of hers is named | she takes it off inside the act |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene: the hot tub, the kiss, Ryan at home | the arc ideas, Zoe A 3 (heat 10-06) |
| her friends go in first | LO, 2026-10-08 (question 6) |
| this step as the voice sample | LO, 2026-10-08 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| Ryan's Want +5 on seeing her | guess |
| fix from the false-line sweep | sweep A4-24 (2026-10-08) |
