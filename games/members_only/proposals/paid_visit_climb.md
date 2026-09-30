# Proposal — the climb into the paid visit (repair item 7, NC2)

> Draft for LO, 2026-09-30. **LO answered the three questions on 2026-09-30 (all as recommended):**
> her no still opens upstairs, with a later line that remembers it; the note is its own scene at the
> Bar; the first time is in room six. Built from this page the same day.
> Rule: `the-arc.md` A15 (LO decided, D7). Gate: `her climb` (`gates.py:12206`).
> Examples only from In Her Own Hands, Cupid's Way, Course of Temptation and Shady Deals.

## The problem, as the gate prints it

- `paid_visit: (d) open on a new save`: it needs only `opening_done` and energy ≥ 20, so she can go
  upstairs and be fucked for money on night one.
- `paid_visit: (d) no step between the introduction and the first time`: there is no introduction,
  no step and no first time.
- `paid_visit.hands / .mouth / .fucked: (c) 0 live group(s) read a declared tier`: each act has one
  voice.

## The shape: three one-time scenes, then the repeatable opens

The gate walks a chain of **one-time** canvases, each reading what the one before sets
(`_her_climb`: intro, then a step, then the first time, then `paid_visit`).

| # | scene (canvas id) | where · when | reads | sets | what happens |
|---|---|---|---|---|---|
| 1 | **Noor raises it** (`noor_upstairs_talk`) | Dressing Room · Tue–Sat 17:15–18:00, Noor's own hours | `first_shift_done`, `noor_stage ≥ 1` | `heard_about_upstairs` | Noor, doing her face, tells her how the members' floor works: a member asks Julian, Julian sends you up, the money's on the dresser, and Dana went up most nights. Companion and rival together: she's showing her how, and she wants the members who asked for Dana. Her ask: "Don't take room four. He's mine." |
| 2 | **The note** (`the_note`) | Bar · Tue–Sat 18:00–22:00 (her shift) | `heard_about_upstairs` | `took_the_note` | The folded note the shift pool already hints at: a room number and a price. This time it's hers. A member at table six, and his want shown first (A13): he's watched her three nights, and he says so. She reads it at the bar. Ade sees her read it (who notices). |
| 3 | **The first time** (`first_visit`) | Upstairs · Tue–Sat 18:00–00:00 | `took_the_note` | `first_visit_done` | The full A15 first time: his want, then her hesitation on screen, then the price named, which she can bargain, then the act, then her feeling after as its own beat. |
| — | `paid_visit` (exists) | unchanged | **+ `first_visit_done`** | — | Opens only now. |

**Why Noor introduces it, and not Julian:** WANT §4a says Julian is *not* the pipe the sex comes down.
Noor is declared companion and rival, one step ahead. That is the In Her Own Hands shape: Abby
pushing her "out of the nest" [AbbyDBDareStart1].

**Why the note is its own scene:** In Her Own Hands teaches the job before the job, with a paid
dinner and no sex before the gala (R1 K2). Here the note is that step: an offer she can hold,
and read, before she goes up.

### Scene 3 in beats (its prose goes to `v2-prose`, measured with `gates.py --beat`)

1. **His want:** room six, the member from the note, already undressed to his shirt. He tells her what he's thought about for three nights.
2. **Her hesitation:** her own line, not a narrator's. The model: Cupid's Way's *"That wasn't the deal."* [waitress5]; In Her Own Hands' mirror, *"If you accept this, you are now a sex worker."* [EscortDate2_Suite3B].
3. **The price:** he says $100. Choices:
   - "Take the hundred."
   - "Two hundred, or I walk." A number lock on `shown`, shown greyed with its need, the way Cupid's Way's Roman bargain is (R1 K2).
   - "No. I'm not Dana." The written no.
4. **The act:** the same rung as `paid_visit.hands`, his hands, and then her mouth if she lets him go on. It stays on the body to its last sentence (register.md, the pivot).
5. **After, as its own beat:** her thought beside what she does. She counts the money, and what she thinks about that. This is the beat Course of Temptation carries as a line instead of a scene, and its players call that route thin (R1 K2).

### Her no, and the one-time trap (finding #37)

A one-time canvas is spent the moment it fires (`v2.py:4640-4643`). A no that just leaves would
lose the route for good. Two ways out. **LO picks one:**

- **(a) Taken (LO, 2026-09-30).** The no still sets `first_visit_done`, and also `first_visit_said_no`.
  `paid_visit` opens either way. Its first screen carries a `group` on `first_visit_said_no`: "Room six
  again. Last time you walked out on him." It's true on every visit it can show on, because the flag
  records it (the truth rule).
- ~~(b) The no parks it.~~ Not taken (LO, 2026-09-30).

## Two voices on each act node (`hands`, `mouth`, `fucked`)

One `group` chain per node on `favour`, highest band first so the chain can't go dead (engine.md §35):

| band | her voice | model |
|---|---|---|
| `favour ≥ 15` | eager: she asks for it | Shady Deals' third kiss: *"You crash your lips against his…"* |
| `favour ≥ 5` | going along: the job, and she's good at it | the middle band |
| else | the pushback, while she does it | In Her Own Hands: *"Hmmmm . . . should I?"* |

Same event, same length, same click (register.md, "One event, several levels"). The act stays
the same; what changes is who she is when she does it. The existing `after` node already runs this
chain; the three act nodes copy its shape.

## What it costs and what it changes

- 3 new one-time canvases, about 150–250 words each, plus 9 act-band paragraphs (3 nodes × 3 bands).
- `paid_visit` gains one trigger read (`first_visit_done`).
- New flags: `heard_about_upstairs`, `took_the_note`, `first_visit_done`, `first_visit_said_no`.
  They go in the ledger, plus a guidance card per step, with place and window.
- Upstairs is closed on a new save. The first paid money now comes after at least 3 in-game days.
  The Sunday $300 is still payable from shifts (5 × $50–80), so the pressure row should hold. I'll
  re-check it with `gates.py --ship` after the build.
- `work_shift` stays as it is; its NC2 red is finding #58.

## LO's answers (2026-09-30)

1. Her no: (a).
2. The note: its own scene at the Bar.
3. Room six.
