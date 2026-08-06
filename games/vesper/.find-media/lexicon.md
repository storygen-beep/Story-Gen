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

## ⚠️ ANAL is not retrievable as a named act in the bent-over position

anal + bent over / desk / table | **Google reads it as generic doggy.** The act word holds the query in porn but does NOT select the act | renner_loop_doggy re-hunt: **198 urls over 3 rounds, only 17 slugs named anal**, and every one of those failed position (supine, seated, riding, pronebone) or cropped the faces out. Round 3 carried BOTH `anal` and `doggystyle` and returned 64 urls with **exactly one** anal-named slug | **CONFIRMED**
anal, visually | **unreadable at gif/strip resolution in from-behind footage** | across two runs on two slots, not one install could be positively verified; the single clip where it WAS legible was an extreme genital crop with no face, so it died on the gaze/affect exception | **CONFIRMED — and it is a genuine trade-off, not a throwaway:** the framing that proves the act destroys every other carrier
WHY it is unverifiable — the mechanism | **a composition conflict, not a query defect.** Every clip that positively SHOWS anal is a gonzo extreme close-up shot SUPINE; every clip with the right posture (bent over furniture, him standing) hides the junction between two bodies | calloway_loop_anal re-hunt, 25 judged clips: the two sets do not intersect | **CONFIRMED.** No query can fix this — the framing that proves the act is incompatible with the framing the beat needs
REFINED 08-03 — standing vs bent-over | **bent-over HIDES the junction; standing SHOWS the junction but not enough to resolve the ORIFICE at gif resolution** | mercer_glass answered the open question at 3x zoom: less-folded bodies do expose the junction, it just cannot be read | so standing is BETTER but still ships `unverified`. The old trade-off held exactly on the one clip that DID prove the act — extreme crop, no face, no bodies, dead on affect
what to do instead | gate on **position + affect + register**, record anal as `unverified`, and say so plainly per clip | the alternative is either shipping a crop with no people in it, or pretending a slug is proof | **DOCTRINE.** Applies to the 3 remaining anal slots: `marsh_anal_t5`, `brothel_anal_t5`, `colm_loop_anal_t5`
`--want` ordering on a RE-HUNT | `--want desk,bent` outranks `--want anal` and lands 8 clips with no act signal at all | renner_loop_doggy wave 1 | **CONFIRMED.** When the ACT is the thing that changed, put the act tokens FIRST in `--want`

## ⚠️⚠️ An act anchor is NECESSARY BUT NOT SUFFICIENT — porn-native JARGON is what holds a query

the 08-01 rule | a t5 query needs an unambiguous act word or it leaves porn entirely | measured: `riding cowgirl man in office chair gif` = 0/83 porn hosts; +`fuck` = 69/73 | **STILL TRUE, and enforced in `validate_queries.py`**
the CORRECTION | **passing that check does NOT mean the query lands in porn** | brothel_vaginal round 3: `woman on top straddling fuck man lying on his back side view gif` CARRIED `fuck` and still collapsed out of the corpus — tenor:10, everydayhealth, stylecaster, hearstapps, e621, rule34, xbooru | **CONFIRMED.** Seven ordinary-English tokens out-voted the one act word and the "sex positions" editorial corpus took over
the mechanism | **porn-native jargon (`cowgirl`, `doggystyle`) HOLDS a query in the corpus; the act word only ANCHORS it.** Descriptive paraphrase loses even with `fuck` present | same round | Write queries in the corpus's own vocabulary, not in English description. The validator can check the anchor; it cannot check for jargon — that stays a judgement call
`reverse cowgirl` | ANTI-token for any both-bodies-legible beat — 3 of 3 reverse-slugged clips failed on pov / from-behind / no-face | brothel_vaginal | belongs in `--avoid`, never `--want`
`amateur` | what actually buys a DIM, lived-in room. Room words do not | brothel_vaginal: every bright reject came from the room-word-ranked wave | **CONFIRMED** — reach for `amateur` when the beat wants dim, not for `dim`/`red room`

## ⚠️ The SHELF-GREP FALLACY — do not predict corpus scarcity from stocked urls

grepping the stocked shelves to predict what the corpus holds | **INVALID** | mercer_glass: a prior run grepped 2,808 stocked vesper urls for `window|skyline|penthouse|highrise`, got 0, and concluded the composition "has never been harvested for this game." The re-run's FIRST query returned window and high-rise slugs and the slot filled 4/4 in three rounds | **A shelf grep measures what PREVIOUS SLOTS ASKED FOR, never what the corpus holds.** Never budget a run for failure on one. (I propagated this wrong warning into a brief — it nearly cost the slot.)

## ⚠️ SCOPE LIMIT on the setting rule below — it does NOT transfer to load-bearing slots

when `setting_is_load_bearing = TRUE`, setting tokens BUY THE COMPOSITION | mercer_glass round 1: `standing anal fuck against the window city view gif` → `window`+`city view` bought it outright, first round, 27 of 29 hosts porn. Top slugs `city-high-rise-sex`, `125924-window-fuck` | **The "harmful" finding below was measured on `load_bearing=FALSE` slots ONLY.** Score the axis honestly first; the rule follows the score, not the reverse.
the ~2-token setting CAP is real, and holds even WITH a strong act anchor | renner_alley round 3: `blowjob alley brick wall night gif` = 3 stacked setting tokens (place+material+time) → 55 urls, **0 new**, grid degraded to Rule34 hentai, Instagram, Tumblr, a Freddy Krueger cosplay and a dog | same class as the act-anchor correction: enough ordinary-English tokens RECLASSIFY the query no matter what anchors it

## ⚠️ Setting tokens on a null-setting slot are HARMFUL, not merely wasted

office / desk / secretary (when `setting_is_load_bearing = false`) | **actively steer the corpus to the WRONG COMPOSITION** — office-anal queries returned roughly two-thirds SUPINE-on-desk studio scenes, which fail the position gate | calloway_loop_anal: rounds 3-4 carried the office tokens; round 5 **dropped** them and returned more anal-named slugs than both office rounds combined, and produced both installs | **UPGRADED THIN → DEAD (08-03).** Second independent measurement, brothel_vaginal: a controlled single-variable A/B (round 1 + `red room brothel`) bought ZERO new host clusters and ZERO red-lit rooms across 24 judged clips. Existing doctrine says setting words are "words stolen from act and heat" — i.e. wasted. Measured here they are worse than wasted: they pull the result set toward a composition the beat rejects. When the setting axis scores `null`, spend ZERO words on the room.

## Corpus vocabulary + traps (measured 08-03)

`bj` | beats `blowjob` in the outdoor/amateur band | renner_alley round 4, mined from Google's own labels ("Public Alley BJ") — real alleys arrived: dumpsters, graffiti, `back-alley-slut` | prefer it outdoors
`exhibitionist` / `exhibionist` | REAL term for window sex, but a **TRAP** — it indexes the ACROSS-THE-STREET VOYEUR shot where bodies are too distant to read. 3 of 3 died on `subjects unreadable` | mercer_glass round 3, its weakest | `--avoid` for any both-bodies-legible beat
posture words when the posture is the act's DEFAULT | pure cost | `kneeling` is redundant with `blowjob`; renner_alley round 1 spent them and got indoor studio kneeling, ~3 outdoor tiles in 40 | spend them on the axis that is actually contested
`night` / darkness | **NOT RETRIEVABLE.** ~2 of 28 fetched clips were genuinely night and neither survived the body gates | renner_alley, 2 rounds | the ROOM is retrievable, the DARK is not — take the bodies, an alley in daylight still reads "behind the bar"; a black rectangle reads as nothing
a caption or slug naming your EXACT beat | **strongest false positive there is** | renner_alley: a cuckold-caption gif matched the beat in words while 60% of the frame was static text over a near-motionless dark rectangle | read the pixels, never the words

## ⚠️ THE FURNITURE DECIDES WHETHER HIS FACE IS IN FRAME — an authoring constraint, not a query problem

the camera habit | **this corpus CROPS the man at the shoulders in BED scenes, and frames him WIDE when the couple is standing at a fixture** (counter, sink, desk, wall) | marsh_anal, measured over 44 fetched clips: ~12 showed his whole face, and only **2 of those 12 were on a bed** | **CONFIRMED.** A beat that needs HIS FACE *and* a BED is fighting the camera habit — no query fixes it
what to do with it | when a beat's differentiator is HIS reaction, prefer a **standing-at-a-fixture** staging over a bed at the AUTHORING stage | same | this is a note for the author, not the hunter — the media constraint should reach back into how the beat is staged
`--want side,view,standing` | a real ranking lever for getting his head in frame: **~1-in-20 → ~11-in-24 on the SAME shelf** | marsh_anal | extends the `side view` row; costs nothing, re-ranks what you already have
`quickie` cluster | retrieves a **CLOTHED, face-visible man** — answers the old "his state is never in frame" open row | colm_anal | mechanism: a nude man is shot as a TORSO (nothing above it to see); a CLOTHED man is shot full-height because the clothes are the point. Cost: ~1 in 6 arrives corporate
`stand and deliver` | **TERM COLLISION — genuine jargon, wrong position.** Denotes stand-and-CARRY: both legs wrapped, her feet off the floor. 4 of 4 were full carries; the corpus's own sibling slug is `stand-and-carry-facing-out` | colm_vaginal round 2, 64 urls, 8+ such slugs across 5 hosts | retrieves the WRONG position with HIGH precision. Use to widen, **never in `--want`**. Same shape as `face to face`→facesitting. What actually worked for one-leg-hooked was **`against the wall`**

## ⚠️ THE HASHED-HOST BLIND SPOT HAS A ONE-FLAG FIX — `--avoid` can name a HOST, `--want` cannot

the asymmetry, VERIFIED IN CODE | `rank()` matches `--want` against the **basename only** (`fetch_candidates.py:76`, `if kw in slug`) but matches `--avoid` against the **whole URL** (`:85`, `if kw in slug or kw in url.lower()`) — the source comment says so outright: *"`avoid` may name a HOST as well as a slug word"* | mercer_desk | **so penalise the SLUGGED hosts by name and the unrankable hashed third floats to the top.** Result: 12/12 fetched, 0 dead, both installs
**SUPERSEDES the earlier remedy** | an empty `--want` does **NOT** work — it leaves every candidate tied at 0 and re-serves exactly the clips prior waves already judged | mercer_desk | use `--avoid <slugged-host>`, not an empty `--want`
the unranked third is not leftovers, it is **the best material** | 4 genuine on-composition clips in 12 from the hashed wave, vs **0 survivors in 10** from a ranked wave run minutes earlier on the SAME shelf | mercer_desk | `myteenwebcam.com` characterised: live and fetchable, 3/3 clean

## ⚠️ A 4-FRAME STRIP UNDER-RESOLVES THE SUPINE / BENT-OVER AXIS — zoom before install

the defect | two clips read BENT OVER on the contact board and a 2× zoom disproved BOTH — one was **supine, face up, his hand on her throat** (the office+desk supine trap), one "navy business suit" was a **school desk and a school uniform** | mercer_desk | **the discriminator is FACE ORIENTATION, ~20 px at strip scale.** It caught two bad installs
procedure | **zoom before install**, always, on any bent-over beat | | added to the run procedure

## ⚠️ The PIN / dominance lens FAILS as a query — it steals the furniture

`hold` / `held` / `down` / `pinned` / `press` / `neck` | returned prone-on-a-bed and supine-throat-grab, **0 survivors** | mercer_desk | same shape as the "posture tokens steal the room" row. **The pin is a JUDGING criterion, never a query term** — both mercer_desk installs have the pin and neither was found by asking for it

## ⚠️ Two tooling gaps in the dedup path — they fail DIFFERENTLY

`fetch_candidates.py` does not consult `used_assets.jsonl` | near-twin slots **feed each other duplicates high in rank** | marsh_anal: 2 of its top-20 were md5-identical to clips already installed in `brothel_anal_t5` | `dedup_tracker --check` DOES catch this (`[USED]`) because the URL matches — but only if you ask. That is why the per-install check is not optional
`dedup_tracker` matches URLs, so **two hosts serving the SAME BYTES both return FREE** | a byte-identical duplicate shipped into `renner_cheerup_oral_t5` vs `calloway_loop_oral_t5` | caught only by a main-session md5 sweep | **the tool cannot see this class.** md5 the candidate against the sibling pools before install — a URL check is not sufficient

## Framing — the third axis, after act and posture

face to face | **DRIFTS TO FACESITTING.** Do not use it on a riding beat | `woman on top riding fuck face to face gif` returned 14 urls of `face-rail` / `railing-his-face` from porngif.co — a different act | **CONFIRMED.** Say `looking at him` instead
cowgirl (framing default) | this corpus shoots cowgirl **FROM BEHIND HER** — her back to the lens, his body hidden under her | marsh_ride: **3 of 8** strips died on `affect:no_face_in_frame`, a single dominant kill class | **CONFIRMED.** Naming the act and her posture does NOT fix it, because the defect is CAMERA POSITION, not body position — the same shape as `him_standing`, one axis further out
framing tokens | `face visible` / `close up` / `pov` are the likely remedy for a beat whose carrier is a face | not yet tested | **UNTESTED** — obvious remedy, not a proven one

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
⚠️ CORRECTION 08-03 — the row above OVERSTATES the gap | **hash-dedup DOES catch a large slice of it.** The row is true only for RE-ENCODES (same shoot, different bytes). It is FALSE for the commonest case: the same file served by two different URLs | renner_cheerup_oral re-run: an md5 sweep of the 8 oral pools caught **5 cross-pool byte-identical clips** that `dedup_tracker --check` passed as FREE — one had already shipped (`calloway_loop_oral_t5/c98139beb17.gif` re-installed into renner_cheerup as `cc470d47829.gif`), and 4 more were caught pre-install (colm, calloway-vaginal, mercer). **Different stems prove different URLs**, since the pool stem is `c`+md5(url)[:10] | **DOCTRINE: md5 every candidate against the whole game before install.** `dedup_tracker` keys on URL and structurally cannot see this; it is a tooling gap, not an agent error. A 6-line `hashlib.md5` sweep over `games/<game>/videos` closes it and costs nothing

## Open — no working term found

the gentle cradling hand at the back of the head | searched by every available name across two games | media_lab_c recorded the same gap independently | **NO KNOWN TERM.** Killed a pool (`lab_finish_facial_t5`, `pool_all_dead` at 24 candidates); avoid building a demand on it
face rail / railing his face / face-riding | FACESITTING, not vaginal riding | google result labels, 2026-08-01 | ⚠️ TERM COLLISION: the query token `face to face` on a cowgirl beat pulls porngif.co "face-rail" facesitting (14 of 72 urls). For a watch-his-face riding beat say `looking at him`, never `face to face`.
lap        | "on his lap" — forces HIM SEATED, the posture `riding`/`cowgirl` will not give you | google slug mining, 2026-08-01 | strongest seated-partner token found: 16/74 chair-or-lap slugs vs `in chair` alone. Retrieval improved; survival did NOT — 0 of 6 lap-slugged clips passed the beat gate (they were beds and standing lifts under a lap slug). Use it to widen the pool, still strip everything.

## Measured 2026-08-03 — `sex/brothel_vaginal_t5` (riding, side framing)

side view (+ `cowgirl` + `fuck`) | **RETRIEVES SIDE-ON FRAMING. The framing remedy is now TESTED.** | `cowgirl riding fuck side view amateur gif` -> 60 urls, 9 hosts, **100% porn**; of 12 judged, 3 were true side-on profiles with both bodies legible, and all 3 installed | **CONFIRMED.** This closes the lexicon's own open row ("framing tokens ... likely remedy, not a proven one"). It fixes the CAMERA-POSITION defect that killed 3 of 8 on marsh_ride with `no_face_in_frame`
⚠️ an act anchor is NECESSARY BUT NOT SUFFICIENT — it can be OUT-VOTED | a query can carry `fuck` and still leave porn entirely if the rest is ordinary English | `woman on top straddling fuck man lying on his back side view gif` carried `fuck` and still collapsed: 44 urls -> tenor:10, everydayhealth, stylecaster, xonecole, hearstapps, e621, rule34, xbooru. The "sex positions" EDITORIAL corpus took over | **CONFIRMED — this refines the 08-01 rule.** One act token flips a 2-3 word position query back into porn; it cannot carry 7 descriptive tokens. **Use porn-native jargon (`cowgirl`), not descriptive paraphrase (`woman on top ... lying on his back`).** Jargon is what holds the corpus, the act word only anchors it
reverse cowgirl | **retrieves POV / from-behind-and-below framing** — the camera sits at his feet, her back or ass fills frame, his face leaves | 3 of 3 reverse-slugged clips failed: `reverse-cowgirl.gif` (pure POV, her face never in frame), `thong-to-the-side-anal-reverse-cowgirl` (she is supine, not on top at all), `amateur-reverse` (shot from his feet, neither face legible) | **CONFIRMED.** On a beat that needs both bodies legible, put `reverse` in `--avoid`, not `--want`
red room / brothel (added to an ALREADY-WORKING query) | bought **volume without reach**: 45 new urls, **zero** new host clusters, **zero** red-lit rooms in 24 judged clips | controlled A/B, single variable: R1 `...side view amateur gif` vs R2 `...side view red room brothel gif`. R2 returned 22 duplicates of R1 and re-served the same two aggregators (imagex1.sx.cdn.live, myteenwebcam) | **CONFIRMED — upgrades `red light / brothel` from THIN to DEAD.** Not actively harmful the way `office/desk` was, but it bought nothing across two measurements now
`amateur` | **this is the token that actually buys DIM** — not any room word | all 3 installs came from the `amateur` round; the room-word round produced none. Wave 2's bright/high-key rejects (14,15,16,18,19,23) were the ones ranked up by room-free slug vocabulary | **CONFIRMED.** To get a dim room, ask for amateur footage, not for a dark room
LUMINANCE as a cross-pool SEPARATOR | when two pools share act+position+room-in-prose, **tone separates them and costs zero query words** | `marsh_ride_t5` is uniformly BRIGHT (daylight/white rooms, 2 of 4 B&W). Building brothel_vaginal as uniformly DIM made the two pools unmistakable without either one hunting a room | **DOCTRINE.** Strip the colliding folder FIRST; its measured look is a free separator the TOML never states

## ⚠️ The glass/window composition IS retrievable — a prior "scarce" call was WRONG

window / glass / city view (on a LOAD-BEARING setting slot) | **retrieves the composition directly, first round** | `mercer_serve_glass_t5` round 1, `standing anal fuck against the window city view gif`: 80 urls, 71 pool, and the top slugs were `Office-near-window-exibition-anal-sex-from-behind-while-standind`, `city-high-rise-sex`, `125924-window-fuck`, `long-legs-anal-standing-from-befing` | **CONFIRMED.** Three rounds returned 174 stocked options and 3 gate-surviving installs. Do not generalise the "setting tokens are harmful" finding to a slot where the setting IS load-bearing — that finding was measured on `setting_is_load_bearing = false` slots and it does not transfer
"0 hits when I grep the existing shelves" ≠ "the corpus lacks it" | a pre-search grep of all 2,808 already-stocked vesper urls for `window\|skyline\|penthouse\|highrise\|balcony` returned **0**, and was read as evidence the composition was unharvestable | the very next Google round returned window/highrise slugs immediately | **CONFIRMED FALSE INFERENCE.** Existing shelves only record what previous slots *asked for*. A shelf grep measures prior demand, never corpus supply. Never budget a slot as "scarce" on that basis
exhibitionist / exhibionist | **the term this corpus indexes window sex under** (note the widespread misspelling `exhibionist` in slugs) | google result labels, round 1 | **CONFIRMED as retrieval** — but see the caveat: it skews toward ACROSS-THE-STREET VOYEUR shots (a distant couple in a lit window), which are useless when you need readable bodies. 3 of 3 `exhibionist`-slugged clips died on `subjects unreadable`. Good for widening, bad for `--want`
standing braced on glass — does it read the ACT better than bent-over? | **PARTIALLY YES, and this answers a standing open question** | `125924-window-fuck.gif` at 3x zoom: the junction is **VISIBLE** — bodies are less folded than bent-over, so the meeting point is not hidden between two torsos | **NEW.** But the orifice still cannot be resolved at gif resolution, so the verdict stays `unverified`. Refines the old claim: bent-over HIDES the junction; standing SHOWS the junction but not enough of it. The gonzo-crop trade-off is unchanged — `big-shiny-anal.gif` proved the act and had no face, no bodies, and died on affect
silhouette against a bright window | a real and recurring shape on city-window queries; **fails the affect gate** | `city-high-rise-sex.gif` — NYC skyline, perfect composition, and every body is an unlit outline | **DOCTRINE.** A silhouetted face is *in frame* but carries no expression, so affect is ABSENT, not unverified. Rejected and left stocked; flag it to the human rather than installing it

## Outdoor / alley — measured 2026-08-03 (renner_cheerup_alley_t5)

alley bj / public alley bj | **the term that actually works for an outdoor kneeling-oral beat** | mined from google's own RESULT LABELS on a failed round ("Public Alley BJ" x3 on xgroovy, "Alley Blowjob Porn GIFs" on PH). `public alley bj gif amateur` returned 77 urls / 55 new and was the only round that put real alleys on the grid — dumpsters, graffiti, alleyway-after-club | **CONFIRMED.** `bj` beats `blowjob` here: the short form is what the outdoor/amateur corpus titles itself with
alley IS retrievable (unlike every indoor room tried) | 3 clips with a genuinely confirming alley survived all gates in one batch of 28 | contrast with `dim office`, `storeroom`, `red-lit brothel` — all DEAD or THIN on this game | **CONFIRMED.** The outdoor band is the one place the SETTING axis can actually be scored above neutral. Setting IS worth query words on an outdoor beat
posture tokens STEAL the room | `back alley blowjob on her knees amateur gif` — the alley word survived, the alley did not. Grid came back overwhelmingly INDOOR studio kneeling | round 1, 77 urls, ~3 outdoor tiles | **CONFIRMED.** `kneeling`/`on her knees` is redundant anyway (lexicon: kneeling is the act's default) — on a setting-driven slot those words are pure cost
3 stacked setting tokens kills the query | `blowjob alley brick wall night gif` -> **55 urls, 55/55 DUPLICATES, zero new**, and the grid degraded to Rule34 hentai, Instagram, Tumblr, Freddy Krueger and a dog | round 3 | **CONFIRMED — this is the ~2-token cap, measured.** place+material+time reclassifies even with `blowjob` anchoring. Its only value was the vocabulary mined off the labels
brick wall | as a query token, a trap (see above). As a THING, present in ~4 surviving clips | | **DEAD AS A TOKEN**
caption/text gifs (`pornwithtext.com`) | the room is in the WORDS, never in the picture | `back-alley-blowjob_001.gif` is 60% static caption ("...in an alley behind the bar...") over a near-motionless dark rectangle. Perfect slug, unreadable bodies | **AVOID.** A slug/caption naming your exact beat is the strongest false positive there is
the outdoor corpus is DAYLIGHT | of 28 fetched, ~2 were genuinely night; the alley clips that passed every body gate were overcast day | | **CONFIRMED.** Take the alley and lose the dark, or take the dark and lose the bodies. `night` as a token did not fix it
his state is never in frame | 27 of 28 clips crop the man to a torso or legs. Only ONE showed his face | so a beat whose register depends on HIS affect (wrecked/slumped/spent) has almost no corpus | **CONFIRMED.** Weight a clip that shows him at all, even at the cost of act legibility — but see the `quickie` row below, which is the first term found that actually *retrieves* him

## ⚠️ The QUICKIE cluster — the first term that RETRIEVES A CLOTHED, FACE-VISIBLE MAN (measured 08-03, colm_loop_anal_t5)

`quickie` / `no time to undress` / `couldn't get her pants off` | **retrieves a partner who is still DRESSED — and dressed men are shot wider, so his FACE arrives with the clothes** | 12 clips fetched by re-ranking the shelf on `quickie,clothed,undress,pants,jeans,maid,kitchen,rough,used,hotel,front-seat,homemade`: 2 had him fully clothed (shirt/tie/belt, opened at the fly) and the installed one is the **only clip in 48 judged across four runs on this slot with BOTH faces legible** | **CONFIRMED as a retrieval lever, and it directly answers the `his state is never in frame` row above.** The mechanism is compositional, not lexical: a nude man is shot as a torso because there is nothing to see above it; a clothed man is shot full-height because the clothes are the point
"clothes disturbed not removed" is a QUERY-ABLE register, not just a prose note | the whole hurried/unglamorous band indexes itself under `quickie`, not under `rough` | `rough` returned gonzo crops with no faces (3 of 3 `rough*` slugs died on affect); `quickie` returned two people who look interrupted | **CONFIRMED.** When the beat is hurried, ask for `quickie`. When it is violent, ask for `rough`. They are different corpora
the cost of the cluster | it drags toward **offices and desks**, because "quickie" and "no time" are workplace words | of 12, one was slugged `office-quickie` and landed in a bright office — the exact composition the `office/desk` DEAD row warns about | pair it with `--avoid` on office words, or accept that ~1 in 6 arrives corporate

## ⚠️ A JUDGED shelf is not an EXHAUSTED shelf — re-rank before you re-search

re-mining the SAME stocked shelf with different `--want` tokens | **found the winning clip with ZERO new Google rounds** | colm_loop_anal_t5 had **251 stocked urls from 4 prior rounds and only ~36 had ever been fetched**. Three prior judging waves (36 strips) produced 2 installs and then stalled; a fourth wave that changed nothing but the `--want` vocabulary produced the survivor on the first try | **DOCTRINE.** `--want` is not a filter over what you fetched — it is a *lens over the whole shelf*, and each lens shows a different sixth of it. Before opening a new round, ask what the previous waves' `--want` tokens were blind to
the corollary to the SHELF-GREP FALLACY | that row says *never predict corpus scarcity from stocked urls*. This is its twin: **never predict SHELF scarcity from judged strips.** | same run | the two failure modes are symmetric — one under-reads the corpus, the other under-reads the shelf you already paid for

## Measured 2026-08-03 — `sex/colm_loop_vaginal_t5` (STANDING vaginal, one leg hooked)

### ⚠️ `stand and deliver` — the vocabulary lead RESOLVED: it RETRIEVES, but it means CARRY

`stand and deliver` | **CONFIRMED as porn-native jargon — it is a site's own label and it retrieves.** `stand and deliver porn gif` → 64 urls, and the shelf now carries 8+ distinct stand-and-deliver slugs across FIVE hosts (porngif.co ×3, eporner ×2, xxxpicss, asianporngif, hardcoregify, nsfwgify) | **CONFIRMED as retrieval.** The word-hunt instinct was right: it is real corpus vocabulary, not a paraphrase
⚠️ what `stand and deliver` actually DENOTES | **STAND-AND-CARRY — he holds her entire weight, BOTH legs wrapped, both her feet off the floor.** It does NOT mean one-leg-hooked | 4 of 4 stand-and-deliver clips fetched were full carries or worse: `219954-stand-and-deliver-fucking` (full carry, RealityKings), `nikita-bellucci-stand-and-carry-facing-out` (carry, facing out), `xxxpicss/stand-and-deliver` (carry), and the corpus's own sibling slug is literally `stand-and-**carry**` | **CONFIRMED — and it is a TERM COLLISION, same shape as `face to face`→facesitting.** For a one-leg-hooked beat this term retrieves the wrong position with high precision. Use it to widen; do not `--want` it
`against the wall` | **THIS is the token that buys one-leg-hooked standing** — all 3 installs came off it | `fuck-her-against-the-wall`, `pressed-against-the-wall`, `border-inspection-at-the-wall`. The round-1 query `standing fuck against the wall one leg up gif amateur` produced every survivor; the round-2 `stand and deliver` round produced ZERO | **CONFIRMED.** On a standing beat, spend the words on `against the wall`, not on the jargon
`214450-huge-tits-stand-and-deliver.gif` | **a SLUG LIE with the act word in it** — the clip is a woman SUPINE ON A BED with him standing at the bedside. Zero standing on her part | | **CONFIRMED** — extends the existing "slugs naming a position are the untrustworthy ones" rule to this term specifically

### Standing vaginal IS retrievable, and it is the cleanest cross-pool separator measured

standing + one leg hooked | **retrievable, first round, no exotic vocabulary needed** | 26 clips fetched off a 179-url shelf → 5 clean gate survivors, 3 installed. Contrast `dim office`/`red-lit brothel`/`storeroom` (all DEAD/THIN on this game) | **CONFIRMED.** The POSITION axis retrieves reliably on this corpus even where the SETTING axis does not
POSITION as a cross-pool separator (beats luminance) | `colm_loop_anal_t5` = 3× bent-over-from-behind; `brothel_vaginal_t5` = 4× riding on beds; `marsh_ride_t5` = riding. **Nothing in any sibling pool is VERTICAL.** A standing composition is unmistakable against all three and costs zero query words | stripped all 3 colliding folders before searching | **DOCTRINE — stronger than the 08-03 luminance rule.** Luminance separated two pools that shared a position; position separates pools outright. Strip the colliders first either way
the dominant rejection class here | **`direction_from_behind`, 7 of 20 rejects** — `against the wall` retrieves standing-DOGGY (her face into the wall) about as often as face-to-face | 01, 04, 06, 19, 20, 21, 22 | **CONFIRMED.** `--avoid doggy,behind,poundstyle` is necessary but does not fix it — the slug rarely says. Budget for ~half the wall clips being from-behind
`quickie` / `clothed quickie` | retrieves the RIGHT REGISTER (clothes half-on, hurried) but the WRONG POSITION — it is overwhelmingly bent-over-a-desk office footage | round 3 `standing quickie fuck leg up clothes on amateur gif`: of 7 quickie-slugged clips fetched, 6 were bent-over/from-behind and 1 was reclining | **THIN.** Good register token, bad position token — pair it with `against the wall` or it drifts to office doggy

### ⚠️ TOOLING — `fetch_candidates.py --want` is BLIND to a third of this shelf

hashed / numeric CDN filenames | **63 of 179 stocked urls (35%) carry no slug at all** — `myteenwebcam.com/fapp/gifs/<md5>.gif` (32) and `imagex1.sx.cdn.live/images/pinporn/<date>/<id>.gif` (31) | `--want` ranks purely on the slug, so these score 0 forever and are never fetched by any run that uses `--want`. They are not bad candidates — they are *unranked* ones, and no agent has ever looked at them | **CONFIRMED BLIND SPOT.** Not a slug↔URL mapping problem: `fetch_candidates.py` writes `manifest.json` mapping `NN.gif → url`, which solves reading what you fetched. The real cost is that a third of the shelf is unreachable by ranking. To see them, fetch with an empty/neutral `--want` or walk `options/list` directly
⚠️ correction to a predecessor note | **porngif.co filenames are NOT hashed** — they are `wp-content/uploads/YYYY/MM/<id>-<full-slug>.gif` and among the most readable on the shelf (`219954-stand-and-deliver-fucking`) | | the hashed hosts are `myteenwebcam` and `imagex1.sx.cdn.live`, not porngif

### ✅ THE BLIND SPOT HAS A ONE-FLAG FIX — `--avoid` the SLUGGED HOSTS (measured 08-03, mercer_serve_desk_t5)

`--avoid <host>,<host>,…` floats the hashed third to the top | **the fix for the row above, and it is free.** The asymmetry is in the code: `rank()` matches `want` against the **basename only** (`fetch_candidates.py:76`, `slug = url.rsplit("/",1)[-1]…`) but matches `avoid` against the **whole URL** (`:85`, `kw in url.lower()`). So `want` can never reach a hashed file, while `avoid` **can name a host**. Penalise the ~27 slugged hosts at −25 each and every hashed url (score 0) sorts above them | mercer_serve_desk_t5: shelf of 195, 64 hashed (33%) never before fetched by anyone. `--want "" --avoid hardcoregify,nsfwgify,sexxxgif,xgroovy,porngifs,…` returned **12/12 fetched, 0 dead**, and **BOTH installs came out of it** | **CONFIRMED — supersedes "fetch with an empty `--want`"**, which does not work: an empty `--want` leaves every url tied at 0 and the shelf order decides, which re-serves the same slugged clips prior waves already judged. You must actively push the slugged hosts DOWN
`myteenwebcam.com` | **now characterised: LIVE and fetchable** on plain clearnet GET, no signing | 3 of 3 fetched clean in the same wave (0.4–5.1MB) | add it to the fetchable-corpus list next to `imagex1.sx.cdn.live`
what the hashed third actually CONTAINED | **the best material on the shelf** — the two installs, plus 2 more gate-passing clips that only lost on setting | 4 genuine office/desk compositions in 12, vs **0 survivors in 10** from the slugged/ranked wave run minutes earlier on the same shelf | **DOCTRINE.** The unranked third is not leftovers. It is unread. On a shelf with hashed hosts, spend a wave there BEFORE opening Google

### ⚠️ The PIN lens FAILED — "held down" vocabulary STEALS THE FURNITURE

`hold` / `held` / `down` / `pinned` / `press` / `pushed` / `neck` | retrieves the pin and **loses the desk** — every hit was prone-on-a-BED or supine-with-a-throat-grab | mercer_serve_desk_t5 wave 1, 10 clips, **0 gate survivors**: prone on bed ×3, supine from the front ×4, solo ×1, oral ×1, backward-over-the-table ×1 | **CONFIRMED — same shape as the measured `posture tokens STEAL the room` row.** A dominance word is a *bed* word on this corpus. If the beat needs a pin ON furniture, retrieve the furniture and take the pin as a bonus
`hold-her-down.gif` | **a SLUG LIE, and a total one** — the clip is a woman SUPINE on a couch in glasses, shot from the FRONT. Zero holding, zero from-behind | | extends the existing "slugs naming a position are the untrustworthy ones" rule to dominance verbs specifically
the pin is NOT retrievable, but it IS common | neither install was found by asking for the pin — both were found by retrieving the ROOM and the pin was simply *there* | both installs show a hand flat on her upper back | **DOCTRINE.** Treat a hand-on-the-back as a JUDGING criterion, never a query term

### ⚠️ A 4-FRAME STRIP UNDER-RESOLVES THE SUPINE / BENT-OVER AXIS — zoom before you install

the strip is not always the last word | **twice in one run a 4-frame strip read BENT-OVER and a 2× zoom showed SUPINE or a different scenario entirely** | (1) `how-to-discipline-secretary-after-work` read as face-down-on-a-desk; at 2.2× it is a woman **on her back, face up, his hand on her throat** — the office+desk supine trap, caught only by the zoom. (2) a clip that read as a **navy business suit** bent over a desk is, at 2×, a **one-piece SCHOOL DESK and a school uniform** | **NEW PROCEDURE.** The strip still kills most candidates cheaply, but on the two axes where this corpus lies — *supine vs bent-over* and *what the wardrobe actually is* — spend one `ffmpeg … scale=iw*2:ih*2, tile=2x2` on any finalist before installing. It is one command and it caught two bad installs here
why the strip fails on this axis specifically | a bent-over torso and a supine torso occupy nearly the same pixels at strip scale; the discriminator is the FACE ORIENTATION (down into the desk vs up at the ceiling), which is ~20px | | cheap fix, real bug class

## ⚠️ Measured 2026-08-03 — `sex/marsh_anal_t5` (anal, bent over a bed, HIS affect is the carrier)

**This slot answers the lexicon's own open row "his state is never in frame" — with a mechanism.**

WHERE his face is in frame — it is a FURNITURE question, not a query question | **this corpus frames BED scenes with the man cropped at the shoulders, and frames STANDING-AT-A-FIXTURE scenes wide enough to include his head** | 44 clips fetched and judged off one 203-url shelf. ~12 carried his whole head/face. Of those 12, **exactly 2 were on a bed** (idx 21, 37); the other 10 were kitchen counter, bathroom sink, bathtub, office desk, mirror, wall, outdoors, balcony | **CONFIRMED, and it is the most useful thing this slot produced.** A beat that needs HIS FACE *and* a BED is fighting the corpus's camera habit. If the beat can live at a fixture instead of a bed, his face comes free; if it cannot, budget for a long hunt and expect to ship torso-carriers
`--want side,view,standing` as a RE-RANK of an existing shelf | **raises his-head-in-frame from ~1 in 20 to ~11 in 24, on the SAME 203-url shelf** | wave 1 ranked on bed vocabulary (`anal,bent,over,bed,behind,edge,gripping`) → 1 of 20 clips contained his head. Wave 2 `--more` on the identical shelf ranked on `side,view,standing,bed,bent,over,behind,her` → ~11 of 24 | **CONFIRMED as a RANKING lever** (not a retrieval one — same shelf, same urls). Corroborates and extends the 08-03 `side view` row: side-on framing is specifically what puts **the man's head** in frame. Reach for it whenever HIS affect is the carrier
the affect carrier when no face exists | **"his whole standing body + his grip" is a real carrier and is NOT the hips-crop failure** | the rubric's gaze/affect exception kills a clip whose face never appears. Applied literally it would have emptied this slot: 2 of the 3 installs have his head cropped at the neck | **DOCTRINE for HIS-affect beats:** distinguish *cropped to hips-and-ass* (carrier ABSENT → fail) from *whole standing body, head out of frame* (carrier PRESENT, weaker → pass, score it down). The scope brief must say which it means, because the rubric alone does not
face MOSAIC-PIXELATION | an amateur-footage kill class the thumbnail hides | idx 40: a genuinely dim lived-in bedroom, his head fully in frame, **his face mosaic-censored by the uploader in every frame** | **REJECT as affect ABSENT** — the carrier is present but deliberately destroyed. Same verdict class as the silhouette-against-a-window row above
the shelf serves you clips ALREADY INSTALLED IN A SIBLING SLOT, ranked high | 2 of the top-20 ranked candidates were **md5-identical** to clips already living in `brothel_anal_t5`, this slot's collision twin | `fetch_candidates.py` ranks the shelf and does **not** consult `used_assets.jsonl`; two slots that share vocabulary share shelf urls. `dedup_tracker.py --check` DID flag both `[USED]` when asked | **CONFIRMED.** Always `--check` before every install (it works), and expect near-twin slots to re-serve each other's installs at the TOP of the ranking, not the bottom
LUMINANCE separator, second measurement | held again | `brothel_anal_t5` is mostly BRIGHT (white bed, white table, sunlit studio); building marsh's pool around a dim brown amateur bedroom and a warm dim hotel room made the two folders unmistakable on a side-by-side rep sheet | **CONFIRMED twice now** (first on brothel_vaginal 08-03). Strip the colliding folder FIRST and take whatever tone it is not

## Measured 2026-08-03 — `sex/renner_cheerup_oral_t5` (oral, HIM SEATED, indoor bar)

`bj` INDOORS | **works — the outdoor-only caveat is now lifted** | `bj in a chair sitting amateur gif` → 76 urls, 100% porn hosts, and the grid was ~90% seated-man-receiving-oral, the best round of the run. `couch bj amateur homemade gif` → 68 urls, also 100% | **CONFIRMED.** `bj` is not in `scene_semantics.ACT_ANCHORS`, so `validate_queries.py` would flag it `no_act_anchor` — the validator's list is INCOMPLETE, not `bj` unsafe. It anchors as well as `blowjob` in both bands measured
**`bj chair` / `bj couch` — Sex.com's own tag names** | the corpus's name for "oral to a SEATED man", the composition `kneeling blowjob` will never give you | mined off Google's RESULT LABELS: "Kneehigh - GIF BJ Chair" (sex.com) ×3, "Blowjob In A Chair: A Sizzling Gif" (sexxxgif), "Noname83 - BJ couch" ×2, "Fellatio Couch" (porngif) | **CONFIRMED — this is the answer to the lexicon's oldest open problem.** `him_standing` was the dominant rejection across 4 prior runs; this tag pair retrieves the seated partner directly and produced 2 of my 3 installs
⚠️ `imagex1.sx.cdn.live` (Sex.com) carries OPAQUE NUMERIC SLUGS | `/images/pinporn/2020/09/22/23672548.gif` — no body, act, room or posture word at all | the single best clip of this run came from there, and **`fetch_candidates.py --want` can never rank it**, because there is nothing in the path to match | **DOCTRINE.** After the slug-ranked waves, go back to the results page and fetch the opaque-slug hosts BY HAND. A slug-ranked fetch systematically cannot see Sex.com, which is one of the nine fetchable hosts
posture words for the DEFAULT posture, re-measured | `--want ...,knees` buried every chair slug | wave 1 with `knees` in `--want` returned 10 of 12 `on-her-knees-*` slugs and only 1 chair; dropping it surfaced couch/stool/chair/lap immediately | **RE-CONFIRMS the existing row for `--want`, not just for queries.** `kneeling` is redundant with the act on BOTH axes
`bar stool` | retrieves the OBJECT, and the corpus's default use of that object is **penetrative sex ON the stool**, not oral beside it | round 1, `blowjob bar stool amateur gif`: 78 urls, 100% porn, real bar interiors — and of 12 judged, the stool clips were `wife-shared-on-a-barstool`, `fucking-on-a-stool-2`, `bunette-club-stool` (a threesome). Zero oral-to-a-seated-man | **THIN — and it refines the existing `bar` row.** The room word works; the room word plus this act does not. `bar stool` is a furniture token, not a posture token
`homemade` | a second anti-studio modifier that behaves like `amateur` | `couch bj amateur homemade gif` → 68 urls, 100% porn, and it produced the DIMMEST clip of the run (`hot-bj-on-the-couch-jjrr88`) | **CONFIRMED** — stack it with `amateur` when the beat wants dark; it did not reclassify the query
his face IS retrievable when you ask for a chair | contradicts the alley row ("his state is never in frame — 27 of 28 crop the man") | of my 3 installs, **all 3 show his face**; the armchair clip shows him reclined, head tipped back, visibly low | **the crop problem is a PROPERTY OF THE OUTDOOR/STANDING BAND, not of the corpus.** Seated-partner queries frame both bodies, because the chair anchors the shot. Worth knowing for any beat whose register depends on HIS affect
a caption/slug naming your exact beat, again | 2 more kills | `on-her-knees-sucking-cock_001.gif` (handed over as a strong lead) is an OFFICE clip captioned "WOMEN in the workplace" whose loop never shows her face; "A GOOD WIFE KNOWS HER PLACE!" was a caption gif | **RE-CONFIRMED.** Both were rejected on pixels after passing on words

## 2026-08-06 — 88-slot approved-NSFW run, wave 1 findings

CONFIRMED VOCABULARY (measured on a real grid this run):
ragdoll    | limp/inert body mid-act, "past collapse" | google served literal `Limp Ragdoll Porn GIFs` slugs | highest-purity query of its slot's set
cmnf       | clothed male, nude female                | repaired a slot whose prose query returned 53% Shutterstock | 100% porn hosts, zero stock
enf        | embarrassed/exposed nude female          | pins female nudity where `nude` alone drifts | ~89% porn hosts
bukkake    | cum-covered aftermath, kneeling          | reached an almost entirely DIFFERENT host cluster from `covered in cum` | this is where shelf variety came from

POISON — measured, do not use (add beside `orgasm` / `leaning forward` / `taking turns`):
dazed      | it is DAZED MAGAZINE's brand name. Pulled dazeddigital's own CDN, dazedprod,
           | Teen Vogue, Slate, Metro, IFFR — and it did that while standing next to `fuck`,
           | so an act anchor does NOT protect you from it.
bruises    | drags impact-play BDSM *and* journalism — ProPublica, New Yorker, Wiley, an FGM
           | campaign poster, a spa-supply store. Dropping the single token repaired the query.
humiliation| pulls the FEMDOM aisle and REVERSES direction — cfnm.net, femdomdestiny,
           | cuckold.info. ~40% of that grid was clothed-female/naked-male.

SHAPE RULE RE-CONFIRMED: a prose description of the beat is not a query. Both of
`cell_inventory_the_order`'s authored queries were condemned on the histogram and stocked
ZERO — they were sentences with no act anchor, so Google reclassified one as stock
photography and the other (via `dim cell`) as prison journalism (hrw.org, aljazeera, NYT).

⚠️ CONCURRENCY GAP FOUND 2026-08-06 (not vocabulary — doctrine): v3 mandates ONE AGENT PER SLOT
with a rolling cap, and its evidence tree tells each agent to append to `run_manifest.json`.
That file has NO lock, unlike `media_options.json` (`_options_lock`, api/v1/media_finder.py:307).
Six concurrent agents doing read-modify-write on it will silently drop entries. Wave 1 survived
only because its six agents finished minutes apart. One agent refused the write and flagged it
rather than racing. FIX: the driver writes every slot's row in ONE pass at the end of the run;
per-slot agents must not touch the manifest. Owed to SKILL.md §Evidence-and-persistence.

## 2026-08-06 — t4 industrial-nude slots: the genre-tag trap (two agents, opposite calls)

⚠️ CORRECTION to the `cmnf`/`enf` entries above. Both agents ran a `cmnf` query and both saw
~100% porn hosts. `salvage_session_11` STOCKED it (noting "the room is domestic/bar/office —
the `warehouse` token barely survived"). `salvage_session_10` CONDEMNED it: the grid was
CFNM-genre — sex parties, offices, cartoons, a Manet painting, and NAKED MEN. Caught only by
the screenshot.

**The rule that explains both:** on a t4 setting slot the histogram cannot tell
"porn hosts, industrial aisle" from "porn hosts, CFNM-party aisle". `cmnf`/`enf` are GENRE
tokens, not setting tokens — they pass the host gate and eat the setting.

BEST SHAPE MEASURED for these slots: a plain nudity word + ONE place noun.
  nude woman industrial warehouse   -> proven, nude figures in real warehouse interiors
  nude woman machine shop           -> proven, real lathes and mill machinery; closest to the beat
  naked woman abandoned factory floor -> proven, real derelict interiors (not studio backdrops)
  naked woman garage mechanic amateur -> proven, slugs carried BOTH halves
Setting-anchored + plain nudity outperformed EVERY genre-tagged variant. Use `cmnf` as at most
one sibling, and only if the grid glance clears it.

POISON for this slot family:
workers    | reclassifies to HISTORICAL SHIPYARD ARCHIVE photography — alamy(22), getty(15),
           | nps.gov, nationalww2museum, BBC, Scottish Maritime Museum. Nudity drops out entirely.

WATERMARK REALITY, t4 industrial nudes: 22.7% stamped (vs 0-3.7% on t5 act slots). These beats
sit next to art-nude and stock territory in a way the explicit ones never do.

## 2026-08-06 — the cmnf rule, reconciled (third agent settles it)

`cmnf` pulls a ~100% porn crowd on its own but carries NO SETTING. Pair it with an
OCCUPATION word, not a ROOM word:
  cmnf nude woman machine shop mechanic  -> PASS, best bucket; hit native vocabulary
                                            (enf-cmnf.cc, nudeworldorder), real garages
  cmnf clothed man sitting nude woman warehouse -> composition dead-on, but `warehouse`
                                            did NOT land — rooms came back domestic/retail
That is why two earlier agents disagreed: one paired it with a room, one with an occupation.

POISON (new): `standing` on a t4 nudity slot behaves exactly like the documented
`leaning forward` — it reads as stock-photography / art-nude vocabulary and OUTVOTES `naked`.
  naked woman standing industrial workshop -> 60/105 stock+wiki+art-gallery, CONDEMNED
  naked woman amateur industrial workshop  -> ~65% porn hosts. One token was the whole fix.
`amateur` is the anti-studio modifier that repairs a stock-drifting nudity query.

## 2026-08-06 — two more setting-token poisons, both invisible to the histogram

dock   | SFW HOMOGRAPH. `shirtless dock worker naked woman amateur` returned a porn-dominant
       | histogram with real nudity — and a grid of bright outdoor lakeside JETTY/PIER nudism.
       | The histogram would have passed it. Only the grid glance caught it. Use
       | `warehouse` / `factory` instead. (Note the irony: the beat IS a dry-dock.)
hangar | NOT IN GOOGLE'S PORN-QUERY VOCABULARY AT ALL. It gets AUTOCORRECTED — the page
       | offered "Did you mean: cmnf naked woman ANGRY workers" — so the setting token
       | silently vanishes and you are left with the bare genre aisle (CMNF offices, desks,
       | museums) behind a ~100%-porn histogram. Repaired by one token: `hangar`->`factory`.

⚠️ GENERALISED FAILURE CLASS worth teaching: a setting token Google does not know is not
merely weak — it is DROPPED, and the query silently becomes the genre token alone. The
histogram cannot show you this because the genre token still lands on porn hosts. Watch the
"Did you mean" line, and do the grid glance.

CONFIRMED BEST TOKEN for this slot family: `cmnf` names the exact composition (naked woman
among clothed working men) and pulls its own dedicated corpus — enf-cmnf.cc, cmnf-stories.info,
nudeworldorder — with zero stock-agency contamination. It just needs a real occupation/place
noun beside it that Google actually knows: factory, machine shop, garage, scrap yard, mechanic.

## 2026-08-06 — male-body tokens are ALL stock magnets (corrects my own guidance)

I told two agents `shirtless` was usable if it travelled with the woman's nudity word.
MEASURED FALSE, one agent, same slot, back to back:
  nude woman muscular man shipyard amateur   -> shutterstock(19) + artblart + human-anatomy-for-artist. REJECT
  naked woman shirtless man shipyard amateur -> 44% stock, shutterstock(24) + dreamstime(16). REJECT
  cmnf naked woman shipyard men              -> ~zero stock, cleanest crowd of that run. PASS
**The man only lands through the scene-native tag `cmnf` + `men`, with NO male-body word at
all.** `muscular` and `shirtless` are stock-photo staples and they outvote the nudity word.

dry dock  | HOMOGRAPH TRAP. Google splits it: `dry` -> dry-humping aisle, `dock` -> boat jetty.
          | Passed the host histogram; only the grid glance caught it. (The beat IS a dry-dock.)
abandoned | the poison in `nude woman abandoned dry dock` (pure stock: dreamstime 22,
          | shutterstock 15, alamy, istock). Dropping it + restoring `amateur` flipped the
          | histogram back to porn hosts in ONE round trip. NOTE this contradicts an earlier
          | entry where `naked woman abandoned factory floor` passed — `abandoned` is safe
          | beside `factory`, poison beside `dry dock`. Setting pairs matter, not words alone.

⚠️ HONEST LIMIT REACHED: the dry-dock / work-cradle INTERIOR is probably not retrievable at
t4. Two agents spent their 2-round setting budget on it. `shipyard` and `engine room` hold the
porn crowd but deliver garages, machine shops and workshops. Per the setting-driven stop rule
that is a stop, not a query bug — the room is not in the corpus at this band.

shirtless man | beside `naked woman` this is a NATURIST/nudist-resort magnet — full-frontal
              | nude MEN, beach/colony content, group flashing, "naked wrestle". It passes the
              | host histogram at ~100% porn and ONLY the grid glance catches it. Third
              | independent confirmation today that no male-body token is usable on this
              | family; the man is only retrievable through `cmnf` + `men`.

welder | same failure mode as `workers` — reclassifies to industrial-trade + stock photography
       | (a welding trade magazine AND a welding foundation both charted). Nudity drops out.
       | Repaired by one token: `welder` -> `auto repair shop`, stock hosts 43 -> 8.

⚠️ THE RULE THAT EXPLAINS THE WHOLE CLASS: an occupation word only works if it is
PORN-NATIVE (`mechanic`, `auto repair shop`, `garage`) rather than TRADE-NATIVE (`welder`,
`workers`, `dock worker`). Porn-native occupations have their own tag corpora; trade-native
ones belong to stock agencies and trade journalism, and they outvote the nudity word.

ENGINEERING NOTE: the `queries/add` response echo does NOT return the stored `hosts` array,
so a successful POST reads back as hostsStored=0. Re-read the CHIP via options/list to verify
hosts landed — do not trust the POST response on this field.

EFFICIENCY (measured 2026-08-06): on an ANIMATED slot, click "More results" ONCE. A second
click added ~400 tiles and returned a FLAT url count (81->81) because the extra tiles are
.jpg/.webp, which the `gif|mp4|webm` regex cannot use. On a STILL slot the second click does
pay. Costs ~30-40s per query on the wrong slot kind.

## 2026-08-06 — SILENT place-noun drops (worse than `hangar`) + which nouns actually bind

⚠️ WORST FAILURE MODE FOUND TODAY: a place noun that is not in the porn corpus is DROPPED
silently — 100% porn hosts, no "Did you mean" line, nothing wrong anywhere in the histogram —
and the grid comes back as the bare genre aisle (bedrooms, a gyno office, living rooms, a bar,
a picnic, a kitchen). `hangar` at least warned you via autocorrect. These did not:
  engine room  (with `cmnf`) | foundry | boatyard-class words
**I (the driver) suggested engine room / boatyard / foundry to an agent. All were wrong.**

⚠️ NUANCE that reconciles a contradiction: `naked woman engine room amateur` PASSED on one
slot while `cmnf naked woman engine room amateur` FAILED on another. The GENRE token competes
with the PLACE token — `cmnf` is strong enough to consume the place. Use cmnf OR a place noun
as the load-bearing term, not both hoping each does half.

PROVEN BINDERS (t4 nudity + real working space), best first:
  construction site | best of all — unfinished interiors, scaffolding, ladders, brick, and a
                    | clothed man in overalls holding a plan beside a nude woman
  warehouse         | binds ("Caught naked in warehouse", "Exhibitionist Naked Warehouse")
  basement          | binds ("Secretly Naked Girl Basement"), bare brick/timber cellars
  garage / mechanic / auto repair shop / junkyard / salvage yard | all previously proven

NEW POISON:
shipyard | SAME homograph class as `dock` — the WATER sense wins: boats, a speedboat wake,
         | lakeside bathing, a beach, DeviantArt art. flashingjungle(17) is the outdoor-nudism
         | tell. Settles the open family question: shipyard is NOT a safe stand-in for dry-dock.
handyman | DIRECTION REVERSAL. It parses as the NAKED person's occupation — "Naked Handyman"
         | tiles show the MAN nude (CFNM). 91% porn hosts, histogram clean, grid wrong on BOTH
         | axes. RULE: avoid occupation nouns that can attach to the nude subject; prefer bare
         | PLACE nouns.

TRADE-OFF measured 2026-08-06: aisle precision and animated-url YIELD can be inversely
related. `gangbang manhandled held down rough amateur gif` hit the most on-beat aisle of its
slot (PornHub's own "Held Down Gangbang", Sex.com's "Manhandled GIFs" tag pages, zero
mainstream leak) but returned only 43 urls against 85 for a looser sibling — those tag pages
are PornHub-tile heavy and serve .jpg/.webp thumbs the `gif|mp4|webm` regex cannot use.
A THIN shelf on a precise query is not a query failure; do not "repair" it into a looser one.

throat | LIVE vocabulary for choking (`throat grabbed and fucked`, `Choking Doggystyle`), NOT
       | poison — but `throat` beside `fucked` reads as ORAL: half the grid came back
       | deep-throat / face-fuck. It needs a POSITION word outranking it. Measured fix:
       | `hand on throat fucked from behind gif` (~50% on-act, oral drift)
       |   -> `choking doggy style rough fuck amateur gif` (~100% on-act, exact beat).

spanking | AISLE-SHIFTER that survives a perfect 100%-porn histogram. `restrained face down
         | spanking bench fuck gif` -> caning, pussy-whipping, a fuckmachine, "Slave/Spanked/
         | Paddled/Caned", femdom clip-store hosts (iwantclips, clips4sale, fetishfemdom,
         | msdanakane). CONDEMNED at the grid, stocked 0. Dropping the ONE token repaired it:
         | `restrained face down bench fuck from behind gif` -> clean act grid.
         | NOTE: `bench` / `bondage bench` / `fuck bench` are SAFE — they return the ACT, not
         | product photography (1 furniture tile across 3 grids). The driver warned about a
         | gear-catalogue failure mode; that warning was WRONG. `spanking` was the poison.

limp   | HOMOGRAPH — alone it drifts into the limp-dick / sissy-caption aisle. Measured fix:
       | pair it with `ragdoll`, which disambiguates it to the inert-body-mid-act sense.
       | `ragdoll limp fuck amateur gif` -> 100% porn hosts, literal slugs "Ragdoll NSFW Gif",
       | "fucked like a rag doll", "GIFs Porno Limp Ragdoll". Zero cat-breed leak. `ragdoll`
       | has now reproduced on TWO independent slots.

⚠️ SHELF-QUALITY NOTE, phncdn: the browser extract strips query strings by construction
(`u.split('?')[0]`), and phncdn's real urls carry their signature IN the query string. So
phncdn urls harvested this way are PATH-ONLY and will mostly be DEAD on the shelf — ~17 per
slot on one measured run. They are stocked per the 2026-08-06 rule change, but the human will
find them broken. `scripts/fetch_pornhub.py` (committed today) is the route that captures the
COMPLETE signed url; the browser route cannot. Worth a janitor sweep or a doctrine note.

pinned down | WRESTLING homograph (cagesideseats / SB Nation fired on it). Survivable beside a
            | real act anchor — one agent measured only 1 wrestling url in 71 — but check the
            | tail after the More-results click.

GENERAL, measured 2026-08-06: the DEEP TAIL of any animated query degrades into generic
gif-magazine editorial (FT, Atlantic, Pitchfork, Vox, Medium, a cat gif, anime) — that is
Google's exhausted-relevance depth, not a query fault. It is largely self-filtering because
those tiles are .jpg/.webp the `gif|mp4|webm` regex cannot extract (~4 of 71 urls got through).
Judge a query on its FIRST SCREEN and its histogram, not on its tail.

## 2026-08-06 — `enf` is CONDITIONAL, not simply good or poison (reconciling 3 agents)

MEASURED BOTH WAYS on the same day:
  enf nude woman construction site workers  -> WORKED (~88% porn hosts)
  enf nude woman bare room man in chair voyeur -> WORKED (~89% porn hosts)
  enf forced to strip naked gif             -> CATASTROPHIC. ZERO porn hosts. Returned
                                               ars.els-cdn (Elsevier), journals.asm.org,
                                               pubs.acs.org, media.springernature.com.
                                               Google read `enf` as a SCIENTIFIC ACRONYM.
**Reconciliation:** `enf` is a weak tag with a strong non-porn homonym. It survives only when
something else porn-native holds the query up — `nude woman` did, `forced to strip` (all
process words) did not. **Never let `enf` be the load-bearing token.** `cmnf` is the safer
sibling: it held on its own beside `stripped naked` + `amateur` with no act anchor at all.

pussy exposed | DRIFTING PAIR — sends the query to the nude-DISPLAY aisle (already-naked,
              | spread, petting) instead of the action asked for. 100% porn hosts, wrong
              | aisle, caught ONLY by the screenshot.
undressing    | GOOD vocabulary for clothes-mid-removal: "Undressing Porn Gifs", "Amateur
              | Stripping", tops being pulled down. Repaired the query above.
clothes ripped off / stripped naked | both genuine porn tag phrases, both landed 100% porn.

## 2026-08-06 — TECHNIQUE: quoting defuses a poisoned word inside a bound genre phrase

`orgasm` is measured poison (health-explainer aisle; it survives a porn-exclusive neighbour).
But `"post orgasm torture" overstimulation gif` — with the phrase in EXPLICIT QUOTES — returned
ZERO health-aisle hosts and put pleasuretorture.com at the TOP (13/40). The quoting is what did
it: it binds the tokens to a genre tag instead of letting Google read `orgasm` as a topic.
**Rule: a poisoned word can be used if it is quoted INSIDE a real genre phrase.** Unquoted, it
poisons; quoted-and-bound, it retrieves the genre. Worth teaching — it recovers vocabulary the
poison list would otherwise cost you.
Caveat measured on the same query: the bound-tag route has an ILLUSTRATED tail (e621, rule34,
furry/hentai) because genre tags are shared with drawn corpora. Live-action is the top ~10
tiles; pair it with a live-action sibling like `ragdoll`.

wrecked / senseless | POISON, a NEW CLASS: written-erotica / prose-review vocabulary. Google
                    | served the FICTION aisle — magazine.atavist.com (longform journalism),
                    | wanderinginn.com (a web serial), Goodreads cover assets, tumblr reposts.
                    | Only 12 urls total, and the act anchor `fucked` was OUTRANKED. Rejected
                    | at the gate, 0 stocked.
⚠️ THE CLASS: words that belong to how people WRITE about sex rather than how sites TAG it.
They read as literary and retrieve prose, not footage. Suspect any word you'd find in erotica
but not on a tag page. (`ragdoll` is the counter-example — it looks literary but IS a tag.)

used hard | CONFIRMED SAFE — clean histograms in two separate queries.
ragdoll   | third independent confirmation. Strongest term found all run for limp/inert
          | mid-act, and it disambiguates the `limp` homograph when paired with it.

## 2026-08-06 — a SHAPE rule, not a token rule (and it caught one of the driver's own queries)

  she cums hard WHILE fucked and held down gif  -> 13 urls, ZERO porn hosts. New Yorker x6,
                                                   Guardian, Wired, Slate, Wikipedia, Tenor.
  she cums hard fucked and held down gif        -> 82 urls, ~100% porn hosts.
  fucked hard WHILE a man watches gif           -> 78 urls, 100% porn hosts.

`while` is NOT poison — the third query uses it and lands. **The poison is QUERY SHAPE: at ~9
tokens with TWO connectives (`while` + `and`) the string reads as a natural-language SENTENCE
and Google falls back to long-form-essay image matching.** No "Did you mean" line was shown
(the agent checked) — this is the silent anchor-drop mode, caught only by the histogram.

RULE: keep queries to ~6-7 tokens and AT MOST ONE connective. Tag-shaped, not sentence-shaped.
This one is the driver's own authored query, and it is the more valuable finding of the day
because it generalises past any single word.

sleeping | POISON on Google Images, proved by clean one-token isolation:
         |   sleeping fucked from behind amateur gif -> 25 urls, ZERO porn hosts
         |   fucked from behind amateur gif          -> 78 urls, 100% porn hosts
         | Two unrelated query shapes both landed in the MAGAZINE-EDITORIAL crowd (Slate, GQ,
         | New Yorker, Pitchfork, Guardian, Glamour, Vanity Fair, Hollywood Reporter, Tenor
         | "MAN... FUCK U" reaction gifs). The tag DOES exist on porn hosts — Google demotes
         | the porn corpus for it. Silent-failure mode 1, no "Did you mean" shown.
         | ⚠️ THE DRIVER TOLD THE AGENT "sleeping is a well-populated porn tag, it will land."
         | That was WRONG and the agent disproved it with a control query.
prone bone | THE replacement — best on-beat query for a face-down, still partner. 100% porn
           | hosts, grid near-uniform: woman flat/face-down on a bed, head on pillow, one man
           | from behind. The "sleeping" quality is recoverable BY EYE from this bucket.
           | (Keep the skill's existing rule: `prone bone` with `desk` = ergonomics; use `bed`.)
spooning   | clean, 100% porn hosts, no cuddle aisle at all; adds a side-lying POV camera.
           | Largest adjacent bucket is spooning ANAL — a position variant, not a wrong aisle.

⚠️ QUALIFICATION to the shape rule above (measured same day, opposite direction):
`fucked from behind while a man watches from a chair gif` — 11 tokens, one connective —
degraded into only a ~10% editorial tail (New Yorker 2, Hearst 2, Tenor 3) and its FIRST
SCREEN was squarely the right aisle. It was kept, correctly: binning 71 candidates over a
10% tail is the over-rejection the contract names.
So sentence-shape is a GRADIENT, not a cliff. The total collapse measured at 9 tokens
(13 urls, zero porn hosts) had TWO connectives; this one has one. Working rule stands —
~6-7 tokens, at most one connective — but a long query that lands on its first screen is a
PASS, not a repair candidate. Judge the grid, not the token count.

bare room | NEAR-WORTHLESS setting token — Google offered "Did you mean: … BASE room", i.e. it
          | does not recognise the phrase. The act anchor does all the work. Same class as
          | `dim concrete room` and `dark`: the ROOM is not retrievable at t5, full stop.
          | Correct handling: keep the query if the grid is right, and do not spend a repair
          | round trying to buy the room back.

## 2026-08-06 — ⚠️ CORRECTION: `ragdoll` is a CAT BREED without a hard anchor

  limp ragdoll used hard bed gif   -> 78 urls, ZERO porn hosts. Giphy/Tenor/Pinterest/Steam,
                                      literal Ragdoll KITTENS on beds.
  limp ragdoll FUCKED hard bed gif -> 69 urls of limp-body porn. One token was the difference.

`used hard`, `limp`, `hard`, `bed` are NOT anchors — none of them holds the query.
**THE RULE: `ragdoll` requires `fuck`/`fucked` present, or it is a cat.** This is the exact
`cowgirl` precedent (a name-word with a strong non-porn sense leaves porn entirely on its own).
The driver had been telling agents "pair `limp` with `ragdoll`" for five slots — that is the
WEAKER rule and it would eventually have produced a shelf of kittens. `ragdoll` is still the
best term of the run for a limp/inert body mid-act; it just is not self-anchoring.

prone bone | STRONG addition, confirmed twice now: porn-native for face-down-flat-fucked-from
           | -behind, i.e. the collapse end-state. Co-fires cleanly with `ragdoll`.
           | (Keep the existing rule: `prone bone` + `desk` = ergonomics; use `bed`.)

desk | NARROWER than the existing rule. `cumshot on ass bent over desk gif` returned ZERO
     | Getty/Shutterstock and a grid of real office desks ("bent over desk at office",
     | "Secretary bent over desk sex gif"). The skill's prefer-`table` rule is specifically
     | about `desk` + `prone bone` (ergonomics collision). With a CUM anchor on a genuinely
     | office beat, `desk` binds fine.
pull out + creampie | reconfirmed as THE aftermath combo (third slot).
cum dripping        | strong aftermath tag — "Cum Drip Porn Gifs", "Standing Doggy DRIPPING
                    | CREAMPIE". Note Google may offer a plural correction (thigh->thighs)
                    | without dropping your token; that is benign, not a failure signal.

balls deep / breeding | CONFIRMED live mined porn tags. Grid slugs "Balls deep creampie",
                      | "Cum Inside Me: Breeting Creampie", "Red and Bred Creampie",
                      | "life's too short to pull out". Good finish-aisle variety when the
                      | obvious `creampie from behind` is already spent by a sibling.

⚠️ A BINDING SETTING TOKEN CAN OUTRANK THE ACT TOKEN. `garage mechanic creampie fuck gif`:
the occupation BOUND (real garages, grimy, industrial-adjacent — porn-native allow-list
confirmed) but the aisle became mid-act STUDIO (Brazzers/Dorcel "Car Mechanic Porn GIFs")
and yield HALVED to 28. So "the setting word works" and "the query still says what you meant"
are two different questions. Buying the room can cost you the beat.
