# vesper lexicon — terms measured 2026-07-31 / 2026-08-01

Format per `references/chrome_route.md` §1: `term | what it means | where it came from | verdict`.

All of this comes from one wave of five NSFW pool slots plus a controlled A/B on two of them.
Everything here is a **retrieval** claim — what a term pulls out of the corpus — never a
correctness claim about any individual clip. The frame strip still decides truth.

## Partner posture — the biggest finding

kneeling blowjob | she kneels and **he STANDS** — the canonical composition on this corpus | 4 runs across 3 slots; `him_standing` was the dominant rejection every time (11/15, 12/26, 15/19, 9/25) | **CONFIRMED.** If the beat needs him seated, this phrase alone will not get it
office chair / under the desk / man sitting in chair | retrieves a **SEATED** partner | renner: **13 of 43** fetched slugs carried seated/chair/desk | **CONFIRMED as a retrieval lever.** Untested whether it *rescues* a slot that lacked it
glasses / close up / pov (with NO posture token) | retrieves the act's default partner posture, i.e. him standing | calloway: **0 of 43→10** fetched slugs seated; wardrobe and framing words do not constrain posture at all | **CONFIRMED.** Naming wardrobe is not naming position

## Act tokens — a query needs an unambiguous one or it leaves porn entirely

riding / cowgirl (alone) | **NOT act tokens — they are POSITIONS, and both are ambiguous with equestrian** | `riding cowgirl man in office chair gif` returned 83 urls and **zero** porn hosts: tenor, BBC, Wikipedia, Billboard, NFL, Shutterstock, Warhol | **CONFIRMED**
+ fuck / sex | adding one explicit act token flips the same query back into porn | `cowgirl riding fuck office chair gif` -> 73 urls, **69 on porn hosts (95%)**, 7 seated/chair slugs. Only difference is the act word | **CONFIRMED — one token, 0% -> 95%**
blowjob | already an unambiguous act token; needs no reinforcement | every oral slot | **CONFIRMED.** The asymmetry matters: `blowjob` anchors a query by itself, `riding` does not
urls_yielded (again) | the FAILED query returned MORE urls than the one that worked | 83 (0% usable) vs 73 (95% usable) | **CONFIRMED twice.** Never read yield as quality

## Settings — what this corpus actually shoots

storeroom / stockroom | **DOES** retrieve utility/linen stores | colm wave-1 retrieved `cdn.nsfwgify.com/44903/kneeling-blowjob.gif` — a linen store with shelving and stacked linens, later ranked #1 by both A/B arms | **CONFIRMED — and a prior claim that "zero storerooms exist" was FALSE.** It was made after the clip proving otherwise had already been removed from the pool
bar / behind the bar / barmaid | retrieves real bar interiors, but they arrive with the wrong act or an extra body | colm: 3 genuine bars in 47 clips — one died on `count` (a third woman on the counter), two on `act` (bent over, not oral) | **THIN.** The room exists; the room + act + count combination mostly does not
red light / brothel / prostitute | 1 red-lit clip in 4 rounds, and it failed on affect (posed burlesque) | brothel, 223 urls | **THIN**
dim office / after hours / records room | zero dim clips in 26 judged | calloway. Both A/B arms independently: *"office porn is lit like an office"* | **DEAD TERM.** Do not spend a round on it
hard floor / concrete / not carpet | never appeared as a retrievable distinction | colm's `must_show` required it; nothing retrieved on it | **DEAD TERM** — a floor material is not indexable vocabulary

## Slugs — what they do and do not tell you

setting words in a slug | **frequently absent even when the room is present** | the one genuine storeroom in 47 clips is slugged `kneeling-blowjob.gif` — no room word at all | **CONFIRMED.** Consequence: `fetch_candidates.py --want <room-word>` ranks that clip DOWN and buries exactly what you were hunting. Prefer body vocabulary in `--want`
body/act words in a slug | roughly directional, still not evidence | `indiasummer-knees-blowjob-hairpulling-handonhead` delivered kneeling+oral but the promised hand-on-head was absent | **PARTIAL** — matches media_lab_c's rule that slugs naming an act, a gaze or a position are the untrustworthy ones

## Query mechanics

urls_yielded | **not a quality signal** | 31 queries logged in `query_ledger.jsonl` returned 40–92 urls with no relationship to whether the query worked | **CONFIRMED.** Record it, never tune on it
duplicate footage across slots | different urls, different byte sizes, different watermarks, one source video | 6 events in one session; one shipped as two different NPCs before it was caught by eye | **CONFIRMED.** Neither URL-dedup nor hash-dedup sees this — only a cross-folder visual check does

## Open — no working term found

the gentle cradling hand at the back of the head | searched by every available name across two games | media_lab_c recorded the same gap independently | **NO KNOWN TERM.** Killed a pool (`lab_finish_facial_t5`, `pool_all_dead` at 24 candidates); avoid building a demand on it
