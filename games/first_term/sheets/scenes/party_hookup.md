# [READY] Scene — party_hookup

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08, heat call A: the party's Bold repeat, with the cocky guy (21),
> Jake's teammate from her classes. Named, with a face. Not Jake: his first sex is B 5, later.

| row | answer |
|---|---|
| system · pool | parties · `party_hookup` |
| where · when | Zoe's Friday party, after 23:00 · Zoe's bathroom, locked |
| gate | Corruption 40 · he is met and at the party (ledger change 26) |
| who | the cocky guy: his portrait at the party; she knows him from class |
| his want, shown first | his stare in Figure drawing; the exam's price, if she paid it |
| what she wears here (test 8) | not named; "pushed aside" at most |
| BRAKE (S9) | once a night, on the trigger |
| raises | corruption add +1 until past Bold · `campus_talk` add +1 |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `ask` | Jake's teammate, at the party, his eyes on her: "Bathroom's free." | no | "Lead the way." → `door` · "Not tonight." → the party | none · a no costs nothing |
| `door` | Zoe's bathroom, locked; the party through the wall | no | "Get on your knees." → `oral` · "Pull him in." → `sex` | none |
| `oral` | she takes his cock in her mouth until he comes | yes | "Back to the party." → the party | corruption add +1 · `campus_talk` add +1 |
| `sex` | on the sink, his cock inside her, they both come | yes | "Back to the party." → the party | corruption add +1 · `campus_talk` add +1 |

**Jake at the party:** if Jake is there (until midnight), the ask waits until he has gone (guess), so the hookup never
plays in front of him.

**Who notices:** Zoe sees them come out of her bathroom; campus talk rises.

## The explicit screens, written

**`oral`** · 125 words · explicit words 5 (balls, cock, lick, suck) · median sentence 11 · act rungs: hands, oral

> Zoe's bathroom door is locked, and the party thumps through the wall. You sink to your knees on the cold tiles. Jake's teammate leans on the sink and grins down at you. You open his jeans and pull his cock out, already hard. You lick the head slowly, so he has to watch. Then you take him in your mouth. His hand fists in your hair. He groans and pulls you into a rhythm, deeper with each stroke. You suck him hard while your hand works the base. His balls tighten against your fingers. His hips jerk, and he comes in your mouth, hot and thick. You swallow all of it, his cock still twitching on your tongue, then wipe your lip with your thumb.

**`sex`** · 111 words · explicit words 7 (ass, cock, nipple, suck, tits) · median sentence 8

> He locks Zoe's bathroom door and lifts you onto the sink. The party thumps through the wall. You yank his jeans open and his cock springs out, hard and thick. He pushes into you slowly, and you feel every inch stretch you. Then he starts slamming in hard. Your legs lock round his hips. His mouth finds your tits, and he sucks one nipple, then the other. You grab his ass and pull him deeper. The mirror fogs behind you. Somebody bangs on the door. You both keep going, faster. He groans into your neck and comes inside you. You come clenching around his cock, your heels digging into his ass.

One change after `v2-prose`: "deeper every time" became "deeper with each stroke" (no history words on a repeat).

**A tool limit, not a defect:** `--beat` tags the `sex` screen's act as oral, from "sucks", because the words its list
uses for intercourse are all outside this ceiling. The screen still counts as explicit.

No history words on either screen: both repeat.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the cocky guy, oral or sex at Bold, not Jake | LO, 2026-10-08 (heat call A) |
| Zoe's bathroom, after 23:00 | the party sheet (riskier choices after 23:00) |
| he waits for Jake to leave | guess |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
