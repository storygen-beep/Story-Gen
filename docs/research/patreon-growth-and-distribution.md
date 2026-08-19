# Where adult-game Patreon members actually come from

**Research date:** 2026-08-19. All figures were pulled live on that date; Patreon and
Graphtreon numbers are snapshots and move daily.

**Question this answers.** We know the top games on Mopoga and Gamcore, and we can see
their Patreon pages, but not how those pages acquire members — one page added over a
thousand members inside 90 days and nothing on the page explains it. Two hypotheses were
on the table: pricing, and a distribution channel we are not using. Both turn out to be
real, and they are connected.

---

## 0. Method and evidence quality

Everything below is either measured directly or explicitly flagged as inferred.

| Source | How it was read | Confidence |
|---|---|---|
| Graphtreon creator pages and category charts | Fetched HTML, parsed the stat block and the embedded `monthlyGraph_patronSeriesData` / `monthlyGraph_earningsSeriesData` chart arrays | High — these are Graphtreon's own daily-scraped series |
| F95zone game catalogue | The public JSON endpoint `f95zone.to/sam/latest_alpha/latest_data.php?cmd=list&cat=games&…` (views, likes, rating, tags, engine prefix, last-update timestamp, catalogue counts) and the public thread pages | High — first-party counters |
| SubscribeStar tier ladders | Fetched creator pages directly (`subscribestar.adult/<slug>`) | High — verbatim tier text and per-tier subscriber counts |
| Mopoga game pages | Fetched directly | High |
| Patreon's own pages | **Not reachable.** `patreon.com` returns 403 to every fetch route available here (Cloudflare bot check), including the help centre and a reader proxy | Tier ladders on Patreon are therefore *inferred* from per-patron averages and from the same devs' SubscribeStar ladders |
| Similarweb traffic for f95zone / mopoga / gamcore | Blocked (bot challenge, empty 202) | Not used. Site-scale claims below rest on F95's own view counters, not on third-party traffic estimates |

Two caveats worth carrying: Graphtreon's percentage-growth column on its "top growing"
chart does not reconcile with its own 30-day member deltas (e.g. DrPinkCake is listed at
"4%" growth next to a +5,185 member delta), so only the absolute deltas and the chart
series are used here. And the recently-updated F95 sample is survivorship-biased by
construction — it contains only games whose devs are still shipping.

---

## 1. The headline answer

1. **Patreon is not a discovery channel for us and never will be.** Adult/18+ pages are
   excluded from Patreon's own search and browse, and adult creators are forbidden from
   showing explicit material on any public-facing surface of the page — banner, tier
   descriptions, free posts. A porn-game Patreon page is a checkout counter, not a shop
   window. Every member arrives from somewhere else.
2. **The channel we are missing is F95zone**, and the specific mechanism is that a game
   thread is a standardised storefront whose *download and developer links are hidden
   from logged-out visitors*. The forum converts anonymous traffic into registered users
   and then hands those users the dev's Patreon link. The catalogue is 26,874 game
   threads; ~70 game updates land per day; a currently-updated new thread carries a
   median of 71,137 views, and a currently-updated HTML thread a median of 168,424.
3. **The "1,000 members in 90 days" number is a release pulse, not accumulation.** Every
   page we sampled has a sawtooth: a release month spikes members by 30–60%, then three
   or four months of decay, then the next spike. Growth is the rising *floor* under the
   sawtooth, and the visible member count is whichever point of the tooth you happened to
   look at.
4. **Pricing does matter, but not as a price point — as what the tier unlocks.** The
   pages that clear $10+ per patron sell *in-game content* per tier (an NPC, a quest, a
   camera mode, a cheat console), delivered by a patron code typed into the build. The
   pages that sit at $2–3 per patron sell early access only. Both work; they are different
   businesses.

---

## 2. The money shape: sawtooth on a rising floor

Monthly paid-member series, straight from Graphtreon's chart data. Release months are the
spikes; everything after is churn.

**Life in Woodchester** (Dirty Sock Games — open-world adult sandbox, one of the closest
things in the market to our shape):

```
2025-01  2,146   <- release
2025-04  1,403
2025-07  1,278   <- floor
2025-08  2,075   <- release (+62% in one month)
2025-12  1,398
2026-02  1,616   <- release
2026-07  1,403
```

Current snapshot: **2,276 paid members, 23,180 total members, $12,628/month, $5.55 per
patron, +885 members and +$5,225 in the last 30 days** — i.e. we caught it mid-spike.

**Tukann** (*Confined and Horny* — HTML sandbox, the single most relevant case study in
this document) shows the same tooth on a clearly rising floor:

```
2024-10  2,358
2025-04  3,328
2025-10  3,683
2026-02  4,265
2026-04  5,086
2026-06  5,376
2026-07  5,129
```

Current: **5,735 paid members, 58,430 total members, +757 in 30 days**, rank 22 in
Graphtreon's Adult Games category, estimated $11K–$41K/month.

**TheGrowState** (launched 2025-01-13, weight-gain niche) is the clean new-entrant curve:
227 → 520 → 1,079 → 1,455 → 1,766 → 2,097 over eighteen months, sawtoothing the whole way.
Current 2,190 paid / 5,154 total, +648 in 30 days.

**Incontinent Cell** (*!Ω Factorial Omega: My Dystopian Robot Girlfriend*) is what a
breakout looks like: 2,411 (2024-11) → 4,257 (2024-12 release) → drift down to ~3,000 →
3,794 (2026-01) → **6,734 (2026-02) → 8,697 (2026-03)** → decaying since. Current 8,803
paid / 39,879 total, +1,894 in 30 days.

**DrPinkCake** (*Being a DIK*, the biggest VN on the board) is the exception that proves
it: 11,700–14,000 for two straight years, almost no tooth. At that size the page is an
institution and the release pulse is noise.

### What this means

- Patreon bills on the 1st. A player joins the month a build drops, takes the build, and
  cancels. That is not a failure mode of these pages; it is how the market works.
- Therefore the metric that matters is **the floor between releases**, not the peak, and
  the lever that raises the floor is a benefit that only exists while you keep paying —
  early access, an accumulating gallery, a code that unlocks the *newest* content.
- And therefore "1,000+ new members in 90 days" is almost always one release landing on a
  page that already had an audience waiting. It is a distribution result, not a pricing
  result.

---

## 3. Pricing anatomy

### 3.1 What the market actually charges

Computed from Graphtreon's top-50 Adult Games earners (earnings ÷ paid members, n=50
pages that publish earnings):

| statistic | per-patron / month |
|---|---|
| minimum | $1.12 (Oni — 6,821 members, $7,646) |
| 25th percentile | $4.78 |
| **median** | **$5.79** |
| 75th percentile | $6.93 |
| maximum | $12.69 (Grimdark Studios — *Masters of Raana*, HTML) |

60% of the top 50 sit between $4.50 and $7.50 per patron. That is the market's answer:
whatever ladder you build, the blended outcome lands near $6 unless you do something
structurally different.

Two structurally different strategies are visible at the ends:

- **Volume / low blended price.** Anthaum (*Course of Temptation*, HTML): 3,429 members,
  $8,033, **$2.34** per patron. CyanCapsule: 10,555 members, $25,147, $2.38. Oni: $1.12.
  These pages are built on a $1–3 entry tier and win on headcount.
- **Content-gated / high blended price.** Grimdark Studios (*Masters of Raana*, HTML):
  1,750 members, $22,204, **$12.69** per patron — the highest in the top 50, on *fewer*
  members than Anthaum. Lust Madness $11.33, SRT $10.30, TitDang $9.03.

Grimdark earns nearly 3× Anthaum from half the members. The difference is entirely in
what the tiers sell.

### 3.2 Three real ladders, read verbatim

Patreon blocks scraping, but the same developers publish identical or near-identical
ladders on SubscribeStar, which does not.

**Grimdark — *Masters of Raana*** (HTML open-world RPG; 828 SubscribeStar subscribers on
top of 1,750 Patreon members):

| tier | what it unlocks |
|---|---|
| $3 Novice | polls, subscriber-only posts |
| $5 Gunslinger | **a whole questline** ("your lost brother"), a unique weapon, the ability to found a Great House, **a fully rendered NPC (Stacey McClung) with a 100+ scene render archive, unique dialogue and her own assignment**, plus a randomised relic-hunting mission framework |
| $10 Nobility | new version 1–2 weeks before public release |
| $25 Acolyte | NPC/MC/world debug (cheat) menus, "MoR Enhanced" (special starting templates, extra creation points, unique quests), a bonus quest, all alpha builds, alpha Discord channels, high-res render archive |
| $50 Spheremaster | high-tier Discord, name in credits |
| $100 Chancellor | can request content — renders, NPCs, small quests |

**Tukann — *Confined and Horny*** (HTML sandbox). Per-tier subscriber counts are public
on SubscribeStar and are worth reading closely:

| tier | subs | what it unlocks |
|---|---|---|
| $3 Confined Follower | 16 | Discord rank, thanks |
| **$7 Confined Lover** | **123** | **bonus scenes unlocked by entering a patron code in the game**, God Mode, a gallery of unlocked story scenes, preview channel |
| $15 Confined Admirer | 47 | "Lewd Camera" — a code that unlocks a bonus in-game quest collecting pictures of the girls; builds 3 days early |
| $25 Confined Fan | 9 | builds 1 week early |
| $50 Confined Master | — | — |

The $7 tier holds 63% of the subscribers. The mid tier is the business; the $3 tier is a
doorbell and the $25 tier is a tip jar.

**Volen — *Become Someone*** (HTML) is the purest version of the pattern:

| tier | what it unlocks |
|---|---|
| $2.50 Supporter | access to the **online premium version** and the premium build |
| $5 Sponsor | + cheat code (lvl 1), money code |
| $10 Lover | + cheat code (lvl 2), holidays code |
| $25 Pro | + cheat code (lvl 3), gallery code |
| $50 Alpha | + cheat code (lvl 4) |
| $100 Supreme | + cheat code (lvl 5), **suggest one quest**, capped at 15 slots (8 taken) |

### 3.3 The mechanic to steal: patron codes

Every high-yield HTML ladder above monetises the same way. **One public build ships
everywhere — F95, itch, the browser portals — and is freely piratable. The product being
sold is not the build; it is a code you type into it.** Bonus scenes, a gallery, a cheat
console, an extra quest, a "premium online version".

This is why these devs can be relaxed about F95 hosting their paid builds: the paid build
without the code is the free build. It also removes the tension between "give the game
away for reach" and "charge for it", which is the exact tension our Gamcore/Mopoga
placement currently sits in.

Secondary mechanics visible in the same ladders, all cheap to implement:

- **Early access as the retention floor** — 3 days at $15, 1 week at $25, 1–2 weeks at
  $10. This is the only benefit that punishes cancelling.
- **Scarcity at the top** — Volen's $100 tier is capped at 15 seats and shows 8 taken.
- **A named identity per tier**, not "Tier 1/2/3".
- **Content requests at the top tier** — Grimdark's $100, Volen's "suggest one quest".

---

## 4. Why Patreon itself sends no traffic

Per Patreon's own help-centre text (surfaced via search; the pages themselves are
unreachable from this environment, so treat the wording as reported rather than quoted):

- Pages categorised **Safe for All Audiences are searchable on Patreon**; Adult/18+ pages
  are the ones that must complete age verification and are not carried by those surfaces.
- Adult/18+ works — nudity, sexual activity, sexually explicit imagery *or themes* — must
  live behind the paywall and be visible only to paying members.
- **Public-facing spaces must be clean**: profile image, banner, **tier descriptions**,
  and any post visible to free members.

Consequences that decide our strategy:

1. 100% of member acquisition is external. There is no "optimise the Patreon page for
   Patreon" move to make.
2. The page cannot show the product. So the shop window has to be a place that permits
   explicit screenshots — an F95 thread, an itch page, a portal page. **That is what the
   F95 thread is for.** It is not a piracy nuisance we tolerate; it is the storefront
   Patreon forbids us from having.
3. The free-member tier is the one funnel Patreon does give us, and the top pages run it
   hard. Free-to-paid ratios measured today:

| page | total members | paid | paid share |
|---|---|---|---|
| DrPinkCake | 62,809 | 19,117 | 30% |
| Incontinent Cell | 39,879 | 8,803 | 22% |
| Tukann | 58,430 | 5,735 | 10% |
| Cheesecake Studio | 13,677 | 2,548 | 19% |
| Nebula Team | 13,819 | 1,604 | 12% |
| The Cumbusters | 11,755 | 2,524 | 21% |
| Life in Woodchester | 23,180 | 2,276 | 10% |
| TheGrowState | 5,154 | 2,190 | 42% |
| Blue Swallow | 2,076 | 690 | 15% |

Tukann is carrying **52,695 free members**. Those are people who clicked the Patreon link
from a thread or a portal, did not pay, and are now on a mailing list that fires every
time a build drops. That list is the mechanism behind a release-month spike of several
hundred paid members: the spike is not new traffic, it is the free list converting for one
month.

**So the free tier is not charity — it is the retargeting list.** We should be capturing
free members deliberately, and every public post should be written to make the free list
convert on release day.

---

## 5. F95zone, in detail

### 5.1 Size and shape

Measured today from the public API:

- **26,874 game threads** in the catalogue.
- Update cadence: the 90 most recently updated games spanned **31.1 hours** → about
  **70 game updates per day** site-wide.
- Engine split (threads carrying each prefix): Ren'Py 10,124 · VN tag 9,622 · Unity 4,777
  · RPGM 4,731 · Others 4,284 · **HTML 1,364** · Flash 314 · QSP 67.
- Status prefixes: **Completed 12,666 · Abandoned 7,001**. Roughly a quarter of every game
  thread on the site is a corpse. Merely continuing to ship puts you in a minority.
- **HTML is 5% of the catalogue and sees ~6.4 updates a day** (the 90 most recent HTML
  updates spanned 336 hours). Our engine's lane is the least crowded one on the biggest
  site in the genre.

### 5.2 What a thread is worth

Views by thread-age cohort, over a 720-game sample of *currently-updated* games (thread ID
is monotonic with creation date, so it proxies age):

| cohort | n | median views | median likes |
|---|---|---|---|
| newest threads (id ≥ 270k) | 413 | **71,137** | 46 |
| id 230–270k | 113 | 348,500 | 129 |
| id 180–230k | 56 | 924,950 | 281 |
| id 120–180k | 64 | 1,379,677 | 331 |
| id 60–120k | 34 | 2,165,453 | 469 |
| oldest (id < 60k) | 40 | 4,124,694 | 719 |

Currently-updated HTML threads: median **168,424** views.

At the top of the market a thread is a permanent asset: *Being a DIK* has **110,794,638
views and 13,007 likes** on one thread; *Corruption of Champions II* 27.3M; *Trials in
Tainted Space* 17.3M; *Degrees of Lewdity* 16.0M with 1,894 likes (the most-liked HTML
game on the site); *Masters of Raana* 12.4M; *Course of Temptation* 5.9M; *Confined and
Horny* 4.6M; *Life in Woodchester* 3.3M.

Individual brand-new HTML games observed in this week's update feed: *Meridian* v0.2 at
27,951 views; *A Modern Pornstar* v0.1 at 29,286; *Hexmoor Academy* v0.02 at 35,692. **A
v0.1 with nothing behind it still gets tens of thousands of views.** Nothing we currently
do produces that.

### 5.3 The conversion mechanism — this is the part that matters

Fetched as a logged-out guest, every game thread's opening post renders the developer
line and the download line as:

```
Developer: GrimDark - You must be registered to see the links
         - You must be registered to see the links  (×5)
...
DOWNLOAD
All: You must be registered to see the links - You must be registered to see the links …
```

Guests see the pitch, the screenshots, the tags, the rating, the version and the changelog
headings — and **no links at all**. Sections like Genre, Installation, Changelog, Developer
Notes and Features are inside spoiler blocks that also demand an account. The site's
"Latest Updates" browser (`/sam/latest_alpha/`) returns *"Sorry, you have to be logged in
to access this page"*.

So the funnel is: search engine or portal → thread → wall → register → now the visitor is
a member of a forum with 26,874 games, subscribed to the thread, receiving alerts on every
version — **and the dev's Patreon/SubscribeStar links sit at the top of the post, in the
same masked block as the download links.** The forum monetises reach in registrations; the
dev monetises the same click in Patreon members. That is the channel.

### 5.4 The thread template

Every OP follows the same fixed schema, and matching it is table stakes:

`Overview` · `Thread Updated` (date) · `Release Date` · `Developer` + support links ·
`Censored: No` · `Version` · `OS` · `Language` · `Genre` (spoiler) · `Installation`
(spoiler) · `Changelog` (spoiler) · `Developer Notes` (spoiler) · `Features` (spoiler) ·
`DOWNLOAD` per-platform mirrors · `Extras` (mods, cheat consoles — often third-party) ·
a long screenshot wall.

### 5.5 Tags are the search surface

Threads carry very large tag sets (*Being a DIK* carries 43). Catalogue-wide counts, with
tag names resolved by cross-referencing 70 thread pages against the API's tag IDs (a
handful of IDs stayed ambiguous and are omitted):

```
male-protagonist 18,297 · vaginal-sex 18,027 · oral-sex 16,155 · big-tits 15,865
2dcg 14,381 · big-ass 12,568 · animated 12,498 · creampie 10,357 · 3dcg 9,540
anal-sex 8,692 · female-protagonist 7,979 · groping 7,720 · handjob 7,717
teasing 7,069 · fantasy 6,897 · masturbation 6,795 · romance 5,979 · adventure 5,801
milf 5,548 · mobile-game 5,116 · sandbox 5,077 · corruption 5,039 · monster-girl 4,978
lesbian 4,774 · voyeurism 4,754 · rpg 4,026 · exhibitionism 3,919 · virgin 3,389
```

The taxonomy is act-level and body-level, not theme-level. A game gets found by the act it
contains. Our TOML already tracks per-NPC kink ceilings; those ceilings map almost
one-to-one onto this tag vocabulary, and the mapping is worth making explicit when we
write a thread.

### 5.6 How a developer gets in

Threads are usually created by the community, not the dev. The documented route is: check
the request lists, post one game per thread in the request area with the title formatted
`Game Name [vX.Y]` plus the dev links; and if a thread for your game already exists, open
a ticket to **claim thread ownership** and apply for the **Game Developer tag**, after
which you post your own updates into your own thread. Registration is free.

---

## 6. The rest of the channel map

| channel | what it is | evidence | our status |
|---|---|---|---|
| **F95zone** | The genre's index, review layer and update feed. Link-gated behind registration | Section 5 | **absent** |
| **itch.io** | Storefront that hosts *playable-in-browser* NSFW HTML5 builds, with devlogs and a follower list you own | The NSFW/HTML5 top list today includes *Confined and Horny*, *Course of Temptation*, and *!Ω Factorial Omega* — three of the fastest-growing Patreons in the category | **absent** |
| **SubscribeStar (.adult)** | Second subscription rail; allows explicit public tier descriptions, which Patreon forbids, and shows per-tier subscriber counts | Grimdark 828 subs *on top of* 1,750 Patreon members; Tukann and Volen run full ladders there | **absent** |
| **Browser portals** (Mopoga, Gamcore, Lewdspot) | Zero-friction play, SEO pages, no account | Mopoga's *Confined and Horny* page carries a full description, an "About the Developer" block **and a live link to `subscribestar.adult/tukann-games`** | **present, links unverified** |
| **Discord** | Where the release pulse is announced and the whales live; every ladder above sells Discord roles | Tier text on all three ladders | absent |
| **Steam / storefronts** | Where finished Ren'Py VNs graduate: *Being a DIK* Season 1 $13.99, Season 2 $19.99; *Eternum EX* $7.99 | Steam store API | not applicable to our shape yet |
| **Reddit** (r/NSFWgaming, r/adultgamedev and similar), **X**, ad networks | Secondary; devs report them as supplements to F95 | community reports | absent |

The portal we already use is not worthless — Mopoga's page is a clean, indexed,
description-rich landing page that does carry the dev's subscription link. It is simply the
*last* mile. F95 is the first.

---

## 7. What this implies for Story-Gen

Ordered by expected return, all of it inside what our engine already does.

1. **Get every shipped game an F95zone thread, and own it.** Register, request or claim the
   thread, apply for the Game Developer tag, and write the OP to the standard schema with a
   full screenshot wall and an honest tag set. Expected value from the cohort data: tens of
   thousands of views for a v0.1, six figures once it is a live HTML thread that updates.
   Nothing else on this list matters until this exists.
2. **Ship on a visible cadence and make each ship an event.** The sawtooth is the business
   model. A version number, a changelog, a thread bump and a Patreon post on the same day.
   Abandoned threads are 26% of the catalogue; simply not stopping is a competitive edge.
3. **Rebuild the tier ladder around patron codes, not early access alone.** Our engine is
   flag-driven; a code that flips `patron_tier` and unlocks a gated NPC, an extra location,
   a gallery, or a debug console is a small change to the importer and the SugarCube
   substrate. That is precisely the difference between a $2.34 page and a $12.69 page.
   Suggested shape, matching where the market's mass actually sits:
   - $3 — Discord role, polls, name in credits
   - **$7 — the money tier: bonus scenes via patron code, gallery unlock, "god mode"**
   - $15 — a code-gated extra questline or capture mode, builds 3 days early
   - $25 — cheat console, all alpha builds, builds 1 week early
   - $50/$100 — capped seats, content requests
4. **Run the free tier as a mailing list.** Explicit invitation to join free on every
   surface; a public post per release; the paid ask only at the release moment. Tukann's
   52,695 free members are the engine behind the spikes.
5. **Add itch.io with a browser-playable build.** It is the one storefront that natively
   hosts what we make, allows explicit imagery, and gives us a follower list we own.
6. **Audit our portal pages.** Confirm every Gamcore/Mopoga listing carries our
   subscription link and Discord in the description, the way Mopoga's *Confined and Horny*
   page carries Tukann's. If a portal strips outbound links, put the support link *inside*
   the build, on the title screen and the pause menu.
7. **Open a Discord and sell roles into it.** Every high-yield ladder in this document uses
   Discord roles as tier texture at zero marginal cost.

Two things this research says we should *not* do: do not try to optimise the Patreon page
for discovery (there is none for adult pages), and do not treat F95 hosting our build as a
loss (the build is the advertisement; the code is the product).

---

## 8. Open questions

- **Patreon tier ladders are inferred, not read.** Cloudflare blocked every route to
  `patreon.com` from this environment. Confirming a handful of ladders — Tukann, Life in
  Woodchester, Incontinent Cell — from a normal browser would firm up section 3.2.
- **Relative traffic of F95 vs the portals is unquantified.** Similarweb blocks us. The
  cheap in-house answer is a referrer breakdown once we have a thread and a portal listing
  pointing at the same landing page.
- **Discord's contribution is unmeasured.** The only Discord invite found on Mopoga's
  *Confined and Horny* page is Mopoga's own server (2,126 members), not Tukann's.
- **Churn is inferred from the shape of the member series, not measured.** We cannot see
  cancellations directly; the sawtooth is consistent with heavy month-of-release churn but
  does not prove the rate.
- **A single verified counter-example is missing** — a game huge on F95 with a page that
  fails to convert — which would isolate how much of the funnel is the thread versus the
  ladder.

---

## Appendix A — Adult Games leaderboard, 2026-08-19 (paid members)

DarkCookie 36,674 · DrPinkCake 19,117 · Project Helius 16,844 · MeshedVR 16,512 ·
TURBODRIVER 16,400 · DotArt 15,778 · CyanCapsule 10,555 ($25,147) · Adeptus Steve 10,439 ·
Babus Games 9,292 · NLT 8,988 · Tiny Secret Games 8,909 · Incontinent Cell 8,803 ·
GB Patch 7,921 · Caribdis 7,522 · MITY 7,454 · Beachside Bunnies 7,127 · Oni 6,821 ·
The Majalis Duo 6,342 · Anduo Games 6,151 · Nuteku 5,901 · Fenoxo Fenfen 5,805 ·
**Tukann 5,735** · Heat 5,189 · Zanith 4,965 · PocketSweeties 4,902 · Nisa K. 4,753 ·
Shybox 4,589 · CutePercentage 4,550 · Noir 4,397 · ZnelArts 4,396 · RadLord 4,239 ·
Runey 4,222 · Carnal Instinct 4,204 · Kritical 4,192 · Young & Naughty 3,962 ·
Evaan 3,952 · Gunsmoke Games 3,926 · Altos and Herdone 3,837 · Horny Union 3,774 ·
BIG BANG 3,736 · WICKED PIXXEL 3,735 · Tinkerer 3,687 · DPMaker 3,662 · Team Nimbus 3,441 ·
**Anthaum 3,429** · Sad Crab 3,393 · ERONIVERSE 3,296 · Undercover Pop 3,142 · Hyao 3,138 ·
Ghosthug 3,131

## Appendix B — Largest 30-day member gains in Adult Games, 2026-08-19

DrPinkCake +5,185 (19,117) · Incontinent Cell +1,893 (8,803) · Life in Woodchester +881
(2,276) · Scrappy +758 (1,224) · The Cumbusters +719 (2,524) · TheGrowState +648 (2,190) ·
Cheesecake Studio +511 (2,548) · Nebula Team +500 (1,604) · WickedWare +434 (1,127) ·
Bobbyboy Productions +426 (1,290) · Shadow Portal +416 (1,566) · Brim +412 (1,158) ·
AceStudio +381 (1,430) · Mutt & Jeff +366 (1,758) · Winterlook Games +333 (691) ·
Lazy tarts +322 (1,481) · MeshiSOFTWORKS +303 (1,535) · PinkPawg +297 (527) ·
Five Nights at KinksDom +296 (711) · HSK Company +292 (292)

Over a 90-day window the top of this list clears a thousand members comfortably — which is
the number that prompted this research, and it is a release pulse landing on an existing
free list.

## Appendix C — Top HTML games on F95zone by likes

Degrees of Lewdity (Vrelnir) 15.96M views / 1,894 likes / 4.45 · The Company (Westane)
12.09M / 1,348 / 3.77 · Masters of Raana (GrimDark) 12.38M / 1,077 / 4.45 · College Daze
(G28) 10.14M / 1,024 / 4.67 · A Spell for All (Cmacleod42) 7.08M / 931 / 4.30 ·
X-Change™ Life (Aphrodite) 6.44M / 804 / 4.42 · Course of Temptation (Anthaum) 5.94M /
724 / 4.09 · Hentai University 4.24M / 687 · Incubus City 4.26M / 685 · Become Someone
(Volen) 10.66M / 682 / 3.57 · Female Agent 4.01M / 678 · Friends of Mine 6.52M / 662 ·
Confined and Horny (Tukann) 4.65M / 644 / 3.56 · Secret Taboo 4.06M / 608 · Love & Vice
(MakinWaves) 3.86M / 600 / 4.52 · Apocalyptic World (ttyrke) 8.33M / 584
