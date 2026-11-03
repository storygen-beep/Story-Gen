# [REVIEW] Scene — party_hookup

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md` · `proposals/COPY_FIXES_C.md`.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08, heat call A: the party's Bold repeat, with the cocky guy (21),
> Jake's teammate from her classes. Named, with a face. Not Jake: his first sex is B 5, later.

| row | answer |
|---|---|
| system · pool | parties · `party_hookup` |
| where · when | Zoe's party, within 8 hours of arriving · then Zoe's bathroom, locked |
| gate | Corruption 40 · `cocky_guy_met` · the cocky guy there, Jake not · not tonight already |
| who | the cocky guy: his portrait at the party; she knows him from class |
| his want, shown first | his stare in Figure drawing; the exam's price, if she paid it |
| want | "Bathroom's free. Just saying." |
| next step | on her knees, or on the sink |
| hook | "You still owe me for that exam." He's at the next party |
| what she wears here | not named; "pushed aside" at most |
| BRAKE | once a night, on the trigger |
| raises | each yes: Corruption +1 (cap 59) · Campus talk +1 · Hygiene -10, Energy 10 |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`party_hookup`** — Zoe's Living Room · The cocky guy there · needs under 8h since `party_went` · Corruption 40+ · `cocky_guy_met` · Jake not in Zoe's Living Room · not `hookup_today` · repeatable

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `ask` | Jake's teammate, the cocky one from figure drawing, is leaning on the wall by Zoe's bathroom … | no | "Lead the way." → `door` | `hookup_today` set |
| | | | "Not tonight." → `no` | — |
| `door` | Zoe's bathroom: fairy lights round the mirror, her makeup all over the sink. | no | "Get on your knees." → `oral` | Hygiene -10 · costs Energy 10 |
| | | | "Pull him in." → `sex` | Hygiene -10 · costs Energy 10 |
| | | | "Unlock the door." → `no` | — |
| `oral` | Zoe's bathroom door is locked, and the party thumps through the wall. | yes | "Back to the party." → `out` | Corruption +1 (cap 59) · Campus talk +1 |
| `sex` | He locks Zoe's bathroom door and lifts you onto the sink. | yes | "Back to the party." → `out` | Corruption +1 (cap 59) · Campus talk +1 |
| `out` | You come out first, fixing your hair. | no | "Go back to the party." — 2 versions, by hour → Zoe's Living Room | — · varies: `came_home_late` set, `late_party` set |
| `no` | He goes back to his wall and his beer, grinning, still watching you. | no | "Leave him to his wall." — 2 versions, by hour → Zoe's Living Room | `party_cool_cocky_guy` set · varies: `came_home_late` set, `late_party` set |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`party_hookup` · `oral`** — 153 words · 7 counted: cock, lick, suck, balls, cock, cock, fuck · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit · **past the ceiling: fuck**

> Zoe's bathroom door is locked, and the party thumps through the wall. You sink to your knees on the cold tiles. Jake's teammate leans on the sink and grins down at you. You open his jeans and pull his cock out, already hard. You lick the head slowly, so he has to watch. Then you take him in your mouth. His hand fists in your hair. He groans and pulls you into a rhythm, deeper with each stroke. You suck him hard while your hand works the base. His balls tighten against your fingers. His hips jerk, and he comes in your mouth, hot and thick. You swallow all of it, his cock still twitching on your tongue, then wipe your lip with your thumb.
>
> He sags back against the sink with his cock still wet from your mouth and fumbles his jeans shut.
>
> Fuck. Does Jake have any idea what he's missing?

**`party_hookup` · `sex`** — 142 words · 8 counted: cock, tits, suck, nipple, ass, cock, ass, cum · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit · **past the ceiling: cum**

> He locks Zoe's bathroom door and lifts you onto the sink. The party thumps through the wall. You yank his jeans open and his cock springs out, hard and thick. He pushes into you slowly, and you feel every inch stretch you. Then he starts slamming in hard. Your legs lock round his hips. His mouth finds your tits, and he sucks one nipple, then the other. You grab his ass and pull him deeper. The mirror fogs behind you. Somebody bangs on the door. You both keep going, faster. He groans into your neck and comes inside you. You come clenching around his cock, your heels digging into his ass.
>
> He stays buried in you, panting, then lifts you down off the sink. His cum runs down the inside of your thigh.
>
> Fix your hair. They're all going to know anyway.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the cocky guy, oral or sex at Bold, not Jake | LO, 2026-10-08 (heat call A) |
| Zoe's bathroom, after 23:00 | the party sheet (riskier choices after 23:00) |
| he waits for Jake to leave | guess |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
