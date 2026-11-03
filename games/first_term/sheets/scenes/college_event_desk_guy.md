# [READY] Scene — college_event_desk_guy

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-02** (reader fails a3, signed by LO 2026-11-02, DECISIONS 131): row 27, the `watch` screen names her body: "Your thighs press together under the desk." after he shows her.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. A class pool event (`college_event_desk_guy`): the guy beside her (21) asks for help.

| row | answer |
|---|---|
| system · pool | college · `college_event_desk_guy` |
| where · when | his seats: Mon, Wed, Fri 08:30 · Mon, Wed 10:15 · Tue, Thu 13:00 (first 15 minutes) |
| gate | `desk_guy_met` · Corruption 20: she looks · Corruption 60: "Help him." (cap 79) |
| who sees | a girl two seats down watches the look; on "Help him." the desk hides it |
| want | "I'm hard. Help me out." |
| next step | her hand under the desk, in a full hall |
| hook | "Next time, then." He asks again the next class |
| what she wears here | not named |
| BRAKE | once a day, on the trigger |
| raises | "Help him.": Corruption +1 (cap 79) · the look and the no pay nothing |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`college_event_desk_guy`** — Lecture Hall · Mon/Wed/Fri 08:30-08:45 · Thu 13:00-13:15 · Mon/Wed 10:15-10:30 · Tue 13:00-13:15 · needs `desk_guy_met` · Corruption 20+ · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `ask` | The guy who sits beside you has his jacket across his lap and his jaw clenched. | no | "Look." → `watch` | — |
| | | | "Help him." (Corruption 60+) → `hand` | Hygiene -10 · costs Energy 10 |
| | | | "Not here." → `no` | — |
| `watch` | A girl two seats down has stopped writing and is watching the two of you. | no | "Back to the class (1h 30m)." → Lecture Hall | — |
| `hand` | You check the room first. | yes | "Wipe your hand (1h 30m)." → Lecture Hall | Corruption +1 (cap 79) |
| `no` | Two seats down a girl smirks into her notes. | no | "Back to the class (1h 30m)." → Lecture Hall | `desk_guy_refused` set |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`college_event_desk_guy` · `hand`** — 131 words · 7 counted: cock, cock, cock, balls, cock, fuck, fuck · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit · **past the ceiling: fuck**

> You check the room first. The lecturer faces the board. The row in front has its heads down. The desk hides everything below your elbows, so you slide your hand under it and open his jeans. His cock springs into your fingers, hot and thick, slick at the tip. You stroke his cock slow, root to head. He grips the desk edge and breathes through his nose so he won't make a sound. Your face burns, but you go faster. His cock throbs in your fist and his balls pull tight. He comes over your knuckles, under the desk where nobody sees. You wipe your palm on his thigh while his cock twitches against his open jeans.
>
> Fuck. Fuck, don't stop. Somebody's turning round.
>
> Then keep your face still and come.

## Why — the source of each key choice

| key choice | source |
|---|---|
| his ask grows by stage; Bold only where nobody sees | LO, chat 2026-10-06 (SYSTEMS §1) |
| Hungry versions locked in 0.1 | LO, 2026-10-07 (SP7 call 1) |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| fix from the false-line sweep | sweep A5-23: his ask is said once, on the `ask` screen (2026-10-08) |
