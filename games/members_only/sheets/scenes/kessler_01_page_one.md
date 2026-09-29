# [READY] Scene — Kessler, step 1: page one
> Signed by LO 2026-09-29, the day it was drafted — LO bypassed the day-after rule for this test.

| | |
|---|---|
| WANT | he wants her voice and her standing in his light — shown on his hub before this (holds the page too close, watches her instead) |
| NEXT STEP | first time anyone hands her a piece of Dana |
| HOOK | "J. keeps the book." · "Page two is longer. Come back Thursday. Wear the one she wore." |
| where · when | Library · Tue–Sat 22:00–23:00 · plays once |
| gate | `opening_done` · `kessler_stage` 0 |
| sets | `kessler_stage` 1 · `read_for_kessler_today` |
| clip | a woman in a black dress reading aloud under a lamp, a man in an armchair watching — intent only |

## Branch map

```
arrive ── Read it all, standing ──▶ standing ──▶ his eyes ──▶ end
       ├─ Read it sitting down ───▶ sitting ───▶ his eyes ──▶ end
       ├─ "Give me the page first" ▶ page_first ─▶ his eyes ──▶ end
       └─ Walk out ───────────────▶ walked_out (step stays open)
```

| node | effect |
|---|---|
| standing | `shown` add 1 |
| sitting | nothing extra; he stops her halfway |
| page_first | nothing extra; one paragraph only |
| walked_out | sets `kessler_walked_out`; `kessler_stage` stays 0 — he asks again tomorrow |

## The voice sample — written in full

**arrive**
> The library is dark except for one lamp. Kessler sits under it with a page on his knee, holding it
> an inch from his nose.
>
> "You're the new one. Dana's sister." It isn't a question. "Come here, girl."
>
> You stay by the door. "How do you know who I am?"
>
> "Everybody knows. Julian can't stop smiling." He lifts the page. "Her handwriting. Her first week.
> You want it?"
>
> *Of course I want it. It's the only reason I'm standing in this room.*
>
> "Then read it to me. Standing. In the light. Slowly."

**standing**
> You step into the light of the lamp, and he sits back to look at all of you, from your shoes up.
>
> You read. Dana's words come out of your mouth: *The manager says I'm a natural. He says the members
> will fight over me.*
>
> "Slower," Kessler says. "Stand in the light. I want to see your mouth when you say her words."
>
> Your face burns, but you read slower. Every time you look up, his eyes are on your lips.
>
> *He isn't listening. He's watching me say it.*

**his eyes**
> The last line is underlined twice: *J. keeps the book. Nobody goes upstairs without it.*
>
> You hold the page out. He doesn't take it. "I can't read her hand any more. My eyes are going." He
> says it like an order. "So you'll come back. Page two is longer. Come back Thursday. Wear the one
> she wore."

**walked_out** (one line, then the library card)
> "You walked out on me, girl. Don't do it tomorrow."

*Measured with `gates.py --beat`: 235 words over three screens (92 · 86 · 57), median sentence 7,
no dashes, 35% spoken (the target is under 5 words of narration to 1 spoken). The first two screens
run long for a phone; each can split into two cascade beats at the build.*

**Who notices:** Ade, next shift — "Library, huh. Dana used to come down from there at one too."
