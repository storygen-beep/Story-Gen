# media_lab round 2 — measured results

Run 2026-07-27, find-media v2, Chrome route, ten slots, 27 queries.
**All 10 slots installed and strip-verified. 1,353 options stocked. Every quality gate passed.**

Read `../STUDY_KEY_do_not_read_before_hunting.md` for which slots were the hidden control.

---

## 1. The doctrine control — the headline

Three of the ten slots carried deliberately OLD-style queries (setting word first, 3–5 words,
mood/story adjectives allowed, no format token). Run verbatim, as the retired doctrine
prescribed.

| Slot | Style | Query | Fetchable URLs |
|---|---|---|---|
| 3 | OLD | `bedroom flashing tits playful quick reveal` | **7** |
| 3 | OLD | `girl lifting shirt flash boobs` | **9** |
| 6 | OLD | `bedroom tender facial cumshot gentle` | **1** |
| 6 | OLD | `loving facial girlfriend soft` | **0** |
| 9 | OLD | `bedroom woman riding passive man slow` | **0** |
| 9 | OLD | `girl on top lazy sex tired guy` | **1** |

**OLD: 18 URLs across 6 queries (mean 3.0).**
**NEW: ~63 per query across 14 NSFW queries.** A ~21× gap.

The doctrine change is earned. **But the reason it works is not the reason it was written.**

## 2. The mechanism is TWO independent failures, not one

The doctrine bundled several rules together and credited "act-led, setting-conditional"
word ORDER. Word order is not what was doing the work. Two separable causes:

### (a) The missing format token — measured 3×, clean

Same query, one token added:

| Query | Fetchable |
|---|---|
| `bedroom flashing tits playful quick reveal` | 7 |
| `bedroom flashing tits playful quick reveal **gif**` | **59** |
| `bedroom tender facial cumshot gentle` | 1 |
| `bedroom tender facial cumshot gentle **gif**` | **54** |
| `bedroom woman riding passive man slow` | 0 |
| `bedroom woman riding passive man slow **gif**` | **91** |

Both pages carried 200 image tiles either way. The old queries were never starved of
results — **they were served stills.** Our extraction regex only takes gif/mp4/webm, so a
page full of JPEG gallery pages harvests as ~zero. Setting-first word order is INNOCENT of
this; the old doctrine simply never said to ask for a loop.

### (b) Story / mood words flip Google's intent class

`loving facial girlfriend soft` returned TikTok, Instagram, Shutterstock, Temu, Amazon.in,
YouTube, Envato, Threads. **Zero pornographic results on the page at all.**
`bedroom woman riding passive man slow` returned Cosmopolitan, Men's Health, Bustle,
Refinery29, StyleCaster, SheKnows, Forbes, iStock, plus cartoon sex-position diagrams.

This replicates the documented `drunk guy` failure on a new beat class. `loving`,
`girlfriend`, `soft`, `passive`, `slow`, `lazy`, `tired` all read as
lifestyle-journalism vocabulary.

**These two failures are independent, and `gif` fixes only the first.** Slot 9's
`+gif` version returned 91 URLs — and the contact sheet was full of Tenor reaction memes, a
bull rider, a bicycle, and TV clips. 7 of 14 fetched candidates were mainstream gifs. The
format token made the poison fetchable; it did not remove the poison.

### (c) NEW: too many SETTING words poison it the same way

`back alley sex at night streetlight gif real` returned Shutterstock and Getty **licensable
stock footage of empty streets at night**, plus Medium, Wattpad, The Atlantic, Decider.
Pool collapsed to 33, mostly unusable.

This is a genuinely new finding and it CUTS AGAINST the current doctrine, which says to
spend words on setting when the setting is load-bearing. It is true that you must name the
setting — but past ~2 setting tokens the query reclassifies as stock photography. Slot 4 was
the only load-bearing-setting slot and it was **the hardest slot in the study**: 14 fetched,
3 survivors.

## 3. Term discovery paid, twice

- **`downblouse`** reached a completely different host cluster than any other query in the
  study: `femdom-pov.me` ×12, `media.tenor.com` ×12, `upskirt.pantiesless.com`,
  `cdn.fapville.com`, `pornogifs.net`, giphy. None of those appeared on any explicit-act
  query. This is direct evidence for the band model in `media_sources.md`: the tease shelf
  is a different shelf, and only the community term reaches it.
- **`dogging`** worked but is mis-mapped in our lexicon: it returns outdoor-public, heavily
  weighted to **beach and daylight**. It is not a night/alley term.
- **`blowbang`** cleanly separates a ring-of-men beat from generic gangbang.

## 4. Slugs are a term mine but NOT a content guarantee

Two clean counter-examples this run:
- `back-alley-slut.gif` → the loop is a woman pulling her top down on a lit street. No alley,
  no sex.
- `three-men-fuck-one-woman_*.gif` → only **two** men are ever in frame together.

`media_sources.md` says descriptive slugs "hand you the next query for free" — true, and it
should also say they are worth **zero** as a correctness claim. Both of these would have
shipped if the slug had been trusted.

## 5. Strip kill rate — lower than the skill claims, for a knowable reason

The skill says thumbnails lie ~2 of 3 times (3/5 and 4/6 measured previously).
**This run: 16 of 54 animated finalists gate-failed at the strip (30%).**

Not a contradiction — a different denominator. I gated hard on the contact sheet BEFORE
stripping (side-views, wrong counts, daylight, celebrities), so the 54 that reached the
strip were already filtered. The prior figure measured a less-filtered shortlist. Worth
recording so the number is not read as a regression in either direction.

Where the strip still earned its keep, it was decisive:
- slot 4: a night-balcony clip whose loop was **kissing**, clothed — the exact documented
  back-room failure recurring on a new beat
- slot 6: two candidates that grin and mug at the lens partway through (the affect gate)
- slot 9: a man who looks passive in the thumbnail and is **sitting up and engaged** in motion
- slot 9: a clip that **cuts to a different woman** mid-loop
- slot 3: `sensitized-reveal` lifts the hem for four frames and never reveals

## 6. Engine / harness facts measured

- **A `Referer: https://www.google.com/` triggers hotlink protection.** 403 on
  `cdn.sexxxgif.com`, `cdn.nsfwgify.com`, `porngif.co`, `cdn.xgifer.com`,
  `cdn.hardcoregify.com`; 200 on all five with no referer, and 200 with the URL's own origin.
  13 of 29 fetches died on this before it was found.
  **The backend is already correct** — `_fetch_headers` (`api/v1/media_finder.py:158-159`)
  falls back to the URL's own origin. Only a hand-rolled fetcher is at risk. The skill's
  manual-curl example sends no Referer, which is right, but nothing warns against adding one,
  and adding one is the natural thing to do when you just came from Google.
- **Nine new fetchable hosts** beyond the catalogued nine, all 200 on clearnet:
  `cdn.sexxxgif.com`, `myteenwebcam.com`, `cumception.com`, `porngifs.ca`, `porngifs4u.com`,
  `pornogifs.net`, `cdn.fapville.com`, `femdom-pov.me`, `cdn.asianporngif.com`,
  `freakydeakygifs.com`, `gifcandy.net`, `img1.thatpervert.com`, `xxxpicss.com`,
  `cdn.pictocum.com`, `bestadultgifs.com`.
- **`static-ca-cdn.eporner.com` failed every fetch this run** (URLError), though it is in the
  catalogued corpus. Worth re-measuring before trusting it.
- The regex `\.(gif|mp4|webm)` matches the bare string `www.gif`, producing a junk URL with an
  empty path. Filter on `pathname.length > 4`.

## 7. Where my judgement is least certain — watch these in review

- **slot 2 (tease).** I installed the true downblouse (she is bent over a task, the view is
  incidental, then she catches the lens and grins) over a clip with eye contact held in ALL
  four frames. The proven rule says eye-contact-held wins; the band model says withholding
  wins. They disagree here. **If LO picks the stocked Tenor hoodie clip instead, the eye
  contact rule outranks the band rule** — and that is the single most useful bit the review
  can produce.
- **slot 6 (affect).** Only one candidate in the entire pool had a hand at the back of her
  head, and it reads as placed rather than cradling. The beat may not be findable as written.
- **slot 4 (setting).** 3 survivors from 14. If none is right, the beat needs a different
  vocabulary, not a re-query.
