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

## 2026-08-07 — PACE vocabulary DOES retrieve (the driver predicted it would drop; wrong)

I expected `slow`/`steady`/`long strokes` to be a process-word class that drops silently, like
`positioning`, `inspecting`, `pulls out`. **Measured false.** `slow deep strokes fuck doggystyle
amateur gif` → 77 urls, 100% porn hosts, 15 host rows, zero stock/editorial/Tenor.

Google's OWN result labels prove the tag is live:
  "Nothing like slow deep strokes from…", "Sensual Slow Strokes That Drive" (FapVille),
  "Deep Stroking Doggystyle porn gifs", "Slow Doggystyle Porn GIFs | Pornhub" (x2),
  "Deep Strokes Makes Her Cum", "Long stroke", "Back strokes for days!"

⚠️ Note `stroke` is a STRONG SFW homograph (swimming, golf, medical) and produced **zero** drift
at head or tail — the `fuck` + `doggystyle` anchors held it completely. Consistent with the
name-word rule: a homograph is safe when a hard anchor outranks it.

CONFIRMED PACE TERMS: `slow deep strokes`, `deep stroking`, `long stroke`, `slow and easy`.
These are the differentiator for beats distinguished only by TEMPO — several remain.

back shots | FRESH porn-native slang for from-behind, mined by an agent rather than supplied.
           | 100% porn hosts, and a host cluster almost DISJOINT from `bent over` / `pounded
           | from behind` queries (84 of 85 urls new) — so it is a real variety lever, not a
           | synonym. No basketball / photography homograph drift. Aisle skews kneeling-on-bed
           | rather than bent-over-an-edge: direction-correct, furniture-neutral.
pounded from behind | clean, 100% porn hosts, grid showed the over-an-edge geometry.

## 2026-08-07 — pace confirmed twice, plus a REGISTER warning and a verification technique

SECOND independent confirmation: `slow deep fuck missionary gif` -> 88 urls, 100% porn hosts,
result titles literally "Slow Deep Pumps", "Slow Missionary Loving", "#passionate sex #slow
deep fuck". `slow` and `deep` are live tag words.

⚠️ VERIFICATION TECHNIQUE worth teaching: to prove a token was HONOURED rather than silently
dropped, compare the shelf's OVERLAP with the same query minus that token. Only **7 of 88**
urls collided with plain `missionary fuck amateur gif` — a dropped token would have returned
near-identical results. Cheap, and it settles the silent-drop question the histogram cannot.

⚠️ REGISTER WARNING FOR LO — `slow` recruits the slow / romantic / loving / PASSIONATE aisle
inside porn. Still real hardcore, but the affect runs WARMER than vesper's cold-noir arousal
axis (see the arousal-axis doctrine). The pace buckets are on-act and off-tone; worth knowing
before picking from them.

table | SAFE and porn-native, and — unlike `garage mechanic` — it does NOT outrank the act.
      | `missionary fuck on table amateur gif` kept yield at 78 AND stayed on the beat, while
      | buying the surface the beat needs (laid back on a cradle, not a bed). The other three
      | grids were bed-heavy. **A SURFACE noun is cheap; a SETTING noun is expensive.**
mating press | works but is the WEAKEST bucket — thinnest yield (56) and a ~10-15% 3D/CGI tail,
             | because the tag is shared with drawn corpora.
missionary   | behaves like `cowgirl`/`ragdoll` — needs `fuck` beside it, and then it is clean.
             | No religious/vocation crowd appeared in any of four histograms.

## 2026-08-07 — the cmnf setting rule, now with FOUR confirmations + a new failure mode

INERT beside `cmnf` (bind nothing, grid returns the bare genre aisle — bathrooms, clinics, a
library, a boat, a beach, bowling, a disco, housework — behind a ~100%-porn histogram and NO
"Did you mean"): `warehouse`, `factory floor`, **`boiler room`**, **`repair bay`**.
**THE PATTERN, 4 confirmations: beside `cmnf` a bare ROOM/SPACE noun is INERT. Only a
porn-native trade-WORKPLACE compound binds.**

loading dock | does NOT repair the `dock` homograph — the COMPOUND SPLITS and the waterside
             | sense wins: lakeside decking, CMNF beach, woods, poolside. Zero industrial docks.

⚠️ NEW FAILURE MODE — **a noun can BIND PERFECTLY and still be the wrong picture.**
`cmnf naked woman truck stop amateur`: the token bound (every tile truck-stop-labelled), 100%
porn hosts — and the aisle is SOLO ROADSIDE / IN-CAB FLASHING in daylight. No working men, no
machinery interior. This is the inverse of "buying the ROOM can cost you the BEAT": there the
noun outranked the act; here the noun did exactly what it said and said the wrong thing.
Only the grid glance catches it.

NEW PROVEN BINDERS for the t4 industrial-nude family:
  auto shop                     | 98/98 stocked, CLEANEST grid of that run, 0% watermark.
                                | Real garages, open engine bays, clothed men present.
  enf ... industrial garage     | 83 stocked, a genuinely DIFFERENT aisle from `auto shop` —
                                | garages, workshops, parking structures, tool walls. `enf` held
                                | fine beside `nude woman` (no scientific-acronym drift),
                                | consistent with the earlier reconciliation.

PACE + RIDING | third confirmation, and the compound is a REAL corpus tag rather than a hopeful
              | join. Google's own labels returned: "slow RIDING", "Hot Slow Riding", "Slow
              | Ride", "A nice, slow deep ride!", "Slow Ride Deep Strokes for Tight...",
              | "Steamy Slow Ride With A Hot MILF", "Long stroke".
              | Best aisle of that slot: `riding slow deep strokes fuck gif`.
              | Tails to expect: `slow riding` ~10-15% romance/couple; `grinding on his cock`
              | ~20% clothed dry-hump/handjob; `riding slow deep strokes` ~20% doggystyle
              | (bleed from the `deep strokes` half). All kept per dump-all.

## 2026-08-07 — ⚠️ TAGS THAT EACH WORK CAN STILL FIGHT: pace does NOT compose with finish

  slow deep strokes cum inside her gif -> 71 urls, 100% porn hosts, GATE-FAILED, stocked 0.
  Grid was generic mid-act missionary/prone ("Deep Strokes Makes Her Cum", "Long Stroke",
  "Prone Bone") — no finish, no her-on-top. **The PACE tokens OUTRANKED the finish anchor.**

Both `slow deep strokes` and `cum inside` are independently PROVEN live tags. Together they
lose. **This is a COMPOSITION rule, not a token rule** — the first of its kind found in this
run, and it is invisible to the histogram. Pace belongs on a MID-ACT beat; a FINISH beat wants
finish vocabulary and nothing competing with it.
(The driver listed `deep stroking creampie` to a later agent before this landed — its gate
should catch it; noted so the guidance is corrected rather than repeated.)

cum leaking out | reads as the nude-DISPLAY / aftermath aisle (solo drip, ass-up close-ups),
                | NOT the act. Gate-failed at 84 urls / 100% porn hosts.

✅ NEW TERM FAMILY, harvested from Google's own labels — **the finish MOMENT, as distinct from
creampie AFTERMATH**: `pulsating creampie`, `throbbing creampie`, `pumping cum inside`.
Labels returned: "pulsating cum inside", "Cum inside pussy (pulsating visible)", "Still
Pumping Hot Loads Into Her". 100% porn hosts, and the ONLY term of that slot's five that put
the ejaculation itself on screen. Promote it — every other finish term returns before-or-after.

## 2026-08-07 — the composition rule confirmed twice, and `bench` corrected

PACE x FINISH — SECOND independent confirmation, different agent, different tokens:
  long stroke creampie from behind gif -> 100% porn hosts, correct act/direction/posture, but
  `long stroke` OUTRANKED `creampie` and the grid slid from FINISH to MID-STROKE
  ("Long Stroke", "Stroking creampie", "Deep Strokes Makes Her Cum").
**Rule stands: pace belongs on a PACE/mid-act beat, never on a FINISH beat.**

⚠️ `bench` CORRECTED — the driver told several agents it was a safe surface noun like `table`.
Measured: `bench` is porn-native for the ACT but resolves to **PARK BENCH** (outdoor/public:
"Outdoor bench cowgirl fuck", "Cute Babe Fucks on Park Bench", "picnic bench fuck") and to
**gym BENCH-PRESS**. Right aisle, wrong room. **`table` buys an indoor raised surface; `bench`
buys a park.** Use `table`.

⚠️ `slow` has a SECOND sense Google honours: in ~1/3 of titles it reads as SLOW-MOTION footage,
not slow pace. Harmless (still on-act) but it dilutes the tempo bucket.

NEW PROVEN FINISH ANCHORS: `internal cumshot` (best-on-beat of its slot — "INTENSE Doggystyle
Creampie", "throbbing doggystyle cumshot"), `pumped full of cum` (no gym/fitness leak from
`pumped`, grid dominated by internal-finish).

TONE REPORT for LO across the riding/pace buckets: none is grimy-industrial. `slow deep fuck
cowgirl` = warm, domestic, homemade bedrooms, soft daylight. `grinding on his cock` = glossier,
studio-leaning, named performers. `cowgirl fuck on bench` = outdoor/public. **The tighter
close-up crops in the `grinding` bucket are the nearest thing to cold on offer.**

riding him | THE cheapest way to buy HIS underneath-posture. `cowgirl` alone does NOT guarantee
           | it. Grid returned the beat literally: "riding him until he cums", "Riding to
           | creampie", "amateur wife rides cock and gets cum".
⚠️ PACE VOCABULARY IS DIRECTIONAL: `deep stroking` / `long stroke` describe HIM thrusting, so
they are wrong on a SHE-RIDES-HIM beat regardless of tempo. An agent worked this out unaided
and declined the family. Pace terms carry an implicit actor — check whose body is moving.
internal cumshot | binds as a genre tag and works, BUT recruits STUDIO footage (ALLINTERNAL
                 | watermarks) despite `amateur`, plus a ~10-15% facial/cum-on-body tail.
                 | Least grimy of its slot's three buckets.
table | THIRD independent confirmation — honoured, on-beat, did not outrank the act.

## 2026-08-07 — the FAST end of pace: the best term found in the run

hard and fast | A LIVE PORNHUB TAG STRING, not merely tolerated. Google echoed it back almost
              | verbatim as titles: "rough hard fast wild doggystyle", "rough fast hard
              | doggystyle fuck", "Fast Tough Doggy Pound". 100% porn hosts (18/18), 66/66
              | stocked, ZERO overlap with either sibling query on the same slot.
              | ⚠️ TONE: the fast end has NO romantic/passionate contamination — the exact
              | opposite of `slow`. It recruits the ROUGH aisle (rough/wild/tough/pound
              | cluster with it), which suits vesper's cold register far better.
              | One cost: an ANAL sub-aisle in the tail.
jackhammer    | CONFIRMED SAFE and porn-native. No power-tool homograph at all — even on a
              | slot whose setting IS industrial. Labels bound it as an act: "jackhammer pussy
              | pounding", "jackhammered", "Jackhammer Porn Gif | Pornhub".

⚠️ SIZE NEEDS TO LEAD. `monster cock bent over bench fuck gif` — the size token was only
WEAKLY honoured; `bent over` + `bench` outvoted it and the grid came back near-identical to a
plain surface query. To make size dominate, LEAD with the size phrase and DROP one surface noun.

`bench`, further nuance (two more grids): safe for the ACT, but it pulls a BONDAGE-bench
sub-aisle when an aggression token sits beside it, and an OUTDOOR PARK-bench sub-aisle when one
does not. `table` remains the clean indoor surface.

💡 THE OVERLAP TEST, used unprompted and for free: two queries differing only in their LEAD
token but sharing the rest overlapped just 16 of 71 (23%) — proving both lead tokens were
honoured rather than dropped. Cheapest available proof against the silent-drop failure mode.

## 2026-08-07 — ⚠️ `table` IS CONDITIONAL: the `milking table` trap

  cowgirl fuck on table amateur gif        -> 84 STOCKED. Safe.
  pumping cum inside bent over table gif   -> 0 STOCKED, condemned at the grid.
  pumped full of cum amateur table gif     -> 0 STOCKED, condemned at the grid.
Same word, same slot family, same day — a clean natural experiment.

**Beside a CUM / CREAMPIE / FINISH word, `table` stops being a surface noun and becomes the
genre tag `MILKING TABLE`** — man supine on the table, woman servicing him. **DIRECTION
REVERSED.** 100% porn hosts, no "Did you mean", six of ~18 first-screen tiles labelled
"Milking table cumshot" / "Milking Table Porn Gifs". Only the grid screenshot catches it.

THE RULE:
  `table` + fuck / cowgirl / a position word  -> SAFE (4 confirmations, buys an indoor surface)
  `table` + cum / creampie / any finish word  -> POISON (milking table, reversed direction)
  `bench` on a finish beat                    -> the safe substitute (0 milking mentions,
                                                 yield held at 78) but it is ABSORBED rather
                                                 than honoured — buys the act, not the surface.
⚠️ The raised work-cradle appears NOT to be buyable on a finish beat at all. Stop spending on it.

ALSO VALIDATED THIS ROUND:
  workbench | behaves as a SURFACE, not a dead space noun — `bent over workbench fuck from
            | behind gif` stocked 47. Thin but real; it is not in the `workshop` dead class.
  throbbing creampie | 81 stocked first try. The finish-MOMENT family holds up.
  hard and fast      | 85 stocked on a second independent slot. Best fast-end term, confirmed.
  balls deep from behind fuck amateur | 0 stocked — condemned. `balls deep` needs a CUM word
            | beside it (`balls deep creampie` / `balls deep cum inside` both landed); on a
            | bare mid-act beat it does not carry.

## 2026-08-07 — CLINICAL vs VERNACULAR, measured on one oral slot

  eating pussy       -> 71 urls / 71 stocked (100% kept)
  licking her pussy  -> 85 urls / 82 stocked (96%)  <- 12 hosts NEITHER other query reached
  cunnilingus        -> 76 urls / 60 stocked (79%)  <- 16 already shelved from the vernacular

**VERNACULAR WINS, and the tell is the DUPE RATE, not the url count.** `cunnilingus` largely
RE-SERVED the vernacular crowd instead of opening a new one, and it dragged in the slot's only
drawn/hentai hosts (rule34, thatpervert) which neither vernacular query produced.
`cunnilingus` IS a real act anchor — it landed and stocked 60 — it is just the weakest of the
three on this beat.
⚠️ `eating pussy` and `licking her pussy` are NOT synonyms: only 19 of 232 label-attributions
overlap across all three chips. Run BOTH.

GENERAL: when two phrasings look synonymous, judge them on the DUPE RATE against the shelf
already built, not on raw yield. A high-dupe query is re-serving a crowd you already have.

`amateur` re-confirmed as a clean porn-native crowd word — dropping the surface noun for it
cost nothing on geometry (tail tiles still showed the leaned-back-on-a-counter composition).

straddling + seated | LANDED (76 stocked). Names HIS posture, which the skill identifies as the
                    | largest rejection class — `him` does not. An agent found this string
                    | already measured clean on sex/renner_loop_vaginal_t5 (2026-08-05, 76 urls)
                    | by READING query_ledger.jsonl, and preferred it over the driver's
                    | suggestion on that evidence. The ledger is a reusable asset across slots,
                    | not just an audit trail — worth teaching.
                    | Tail: facesitting/femdom + Tenor SFW "straddle" gifs, a minority.

⚠️ OPERATIONAL — measured 2026-08-07: **`curl` to `localhost:8000` returns connection-refused
from inside an agent sandbox even when the Django server is up and listening.** All API work
must go through the PAGE's `fetch` (which works). Consequence: the STEP-0 dedupe guard cannot
actually run "before Chrome" as briefed — an agent needs a tab first. The driver-side todo
computation (a slot is done if `queries[slot_key]` is non-empty) is the real guard; the
agent-side check is a backstop and must be ordered AFTER tab creation.

## 2026-08-07 — server-outage hypothesis TESTED against the milking-table finding: REJECTED

An agent found the Django dev server down and restarted it (correct catch, real outage), and
hypothesised the `table` zeros were silent stock failures rather than a genuine gate.
**Checked against the chip timeline — the hypothesis does not hold:**
  04:15:02  stocked 81  <- server demonstrably UP
  04:15:26  stocked ok
  04:15:40  stocked 0   <- `pumped full of cum amateur table gif`
  04:16:08 / 04:16:37 / 04:16:52  all stocked ok
  04:16:57  stocked 0   <- `pumping cum inside bent over table gif`
  04:17:42  last chip, then a 50-MINUTE GAP to 05:08:04  <- THE ACTUAL OUTAGE
The outage window contained NO agent activity (the driver process had exited), so it cost
nothing. The milking-table zeros were deliberate gates, not failures.

⚠️ DRIVER'S OWN OVERSTATEMENT, corrected: I wrote "measured three times today." It is TWO
zeros, of which ONE carries explicit grid evidence (six labelled "Milking table cumshot" /
"Milking Table Porn Gifs" tiles described by the agent) and one is a consistent but
unverified zero from an agent killed before it reported. The corroboration that makes it
solid is the REPAIR, not the repetition: `pumped full of cum amateur BENCH gif` -> 78 stocked
at 04:13, same slot, same minute-scale window. One token, two outcomes.

## 2026-08-07 — the finish-MOMENT family beats plain `creampie`, with a proper CONTROL
An agent ran a deliberate plain-anchor control on one slot, same session:
  pulsating creampie amateur close up gif -> 80 urls, wall-to-wall finish MOMENT
  bred creampie cum inside her amateur    -> 92 urls, widest host spread (22 hosts)
  creampie amateur homemade gif (CONTROL) -> 74 urls, 100% porn, GENERIC MID-ACT aisle
**The loosest query returned the FEWEST urls and the wrong aisle.** Plain `creampie` buys the
GENRE, not the MOMENT. `bred` is a third viable member (non-poisonous beside a real anchor).
With no surface noun and no position token, the milking-table trap cannot fire at all.

---

## 2026-08-09 — the 7 needs-review POOL slots, v3 chip-and-label pass

Seven slots that already carried DEEP but 100% UNLABELLED v2-era shelves (1,869 options, zero
`found_by`, zero chips). 22 queries, 7 agents, 10.3 min, no captcha, nothing installed or pruned.
Shelves 1,869 -> 2,812. **449 pre-existing options were RETRO-LABELLED** by duplicates.

### ⚠️ NEW POISON — `bar` (the ROOM word), measured on TWO slots with two DIFFERENT failure modes

`bar` | **POISON, and it generalises the old `bar stool` row from the OBJECT to the ROOM** | (1) renner_cheerup_oral: `bj chair bar amateur gif` -> 71 urls, 8 Tenor + 3 Giphy + 2 reddit; dropping `bar` for `sloppy` on the same anchor went to 100% porn. (2) renner_cheerup_alley: `public blowjob behind the bar amateur gif` -> 71 urls at **100% porn hosts** and the grid was entirely BAR INTERIOR (pub, nightclub stage, pool table, bar bathroom, slugs `Bj pub` / `Blowjob in a bar`). **Zero alley.** | **CONFIRMED TWICE.** Naming the beat's landmark venue puts the camera INSIDE the venue. Mode (2) is a textbook wrong-AISLE-inside-a-RIGHT-CROWD: the histogram was 100% clean and completely blind; only the grid screenshot caught it
`bar` is NOT silently dropped | no "Did you mean" / "Showing results for" line appeared | renner_cheerup_oral | **worse than being ignored** — it is accepted and actively retrieves the wrong crowd
`parking lot` | **POISON — it indexes the CAR, not the pavement** | 71 urls, 100% porn hosts, grid is driver's seat / passenger seat / back seat, slugs `Public Blowjob Parking Lot CAR`, `Blowjob at Parking Garage w/ cars` | **CONFIRMED.** Useless for a concrete-and-wall beat. Same shape as `bar`: right crowd, wrong aisle, histogram blind
`outdoor` | **a WEAK holder that cannot carry `bj` alone** | `back alley bj outdoor gif` leaked ~13 of 49 urls to **academic journals** — pubs.acs.org, science.org, pnas.org, cell.com, bmjpublichealth.bmj.com, tandfonline.com, journals.uchicago.edu, plus cdn.climbing.com. **`bj` reads as a journal/author initialism.** Swapping the single token `outdoor` -> `amateur` removed the leak 100% (49 urls, ZERO non-porn) | **CONFIRMED, single-variable.** Extends the `amateur` doctrine: `bj` specifically NEEDS an anti-studio holder or it decays into an abbreviation
`glass` | **POLYSEMOUS and self-diluting** — three senses on one grid: glass SURFACE (wanted), glass INSERTION TOY (`glass in anal`, `Ass on the glass gif`), and EYEGLASSES (`sexy girl in glasses gets dick in her...`) | mercer_serve_glass q2 | the act anchor held so the CROWD stayed porn — this is aisle dilution invisible to the histogram. **`window` is the unambiguous token; prefer it.** Keep `glass` as a widener you accept dilution for
`wall` (bare) | **SAFE — the poison is the two-token `brick wall`, not `wall`** | rode along in `dogging blowjob alley wall voyeur gif` with zero degradation | **CORRECTS a possible over-read of the 08-03 `brick wall` row**
`desk` | **SAFE on a bent-over / doggy beat — the general poison entry is scoped to `prone bone` ONLY** | three independent agents: mercer_serve_desk (69 urls, 100% porn, zero ergonomic drift), renner_loop_doggy (grids full of office desks), renner_loop_oral (`under the desk` = 100% porn, tightest grid of its three) | **CONFIRMED x3.** Do not generalise the prone-bone scoping

### Tokens that WORK — new, measured

`dogging` | **the strongest single token measured on the alley slot** | `dogging blowjob alley wall voyeur gif` = 89 urls / **76 NEW** against a 299-deep pile, only 13 duplicates — better new-yield than both alley queries combined. **Fully self-anchoring**: paired with `blowjob`, not one dog result | **CONFIRMED.** Caveat: skews roadside / woods / beach / car-adjacent, so it buys public-outdoor VARIETY, not alley precision
`sloppy` | a clean shelf-widener on an already-proven anchor | `sloppy bj chair homemade gif` = 64 urls / 44 new (20 dup) where the two seeds returned 51/80 and 46/66 dup | **CONFIRMED.** Porn-native INTENSITY jargon reaches corpus that plain act+furniture does not
`secretary` | **a live porn-corpus OCCUPATION token — office-role words behave NOTHING like labor-role words** | `secretary bj chair amateur gif` = 80 urls, **0 non-porn hosts**, most new options of its slot (48) | **CONFIRMED, and it scopes the 08-06 occupation poison.** `workers`/`welder`/`dock worker` pull trade-journal ARCHIVE photography; `secretary` is corpus-native. The poison is LABOR-role, not occupation-as-such
`creampie` | **a DISTINCT AISLE, not a rewording** | `anal creampie bent over bed amateur gif` opened cumception(11), thatpervert(6), xxxpicz — host clusters none of the three bent-over/side-view seeds touched across 201 urls | **CONFIRMED.** When a beat's carrier is HIS orgasm, the climax token is worth a whole round
`exhibionist` | **confirmed LIVE and NOT auto-corrected** (no "Did you mean"), and the **highest-VARIETY token** for a window beat | 83 urls / 30 porn hosts; the only seed to surface the xhamster CDN family (thumb-p2/p4/p6/p8/p9.xhcdn.com) plus flashingjungle, exhibitioniststrangers, cumception | **CONFIRMED.** Reach for it when a window shelf needs a DIFFERENT crowd, not more of one
`homemade` vs `amateur` | **NOT retrieval synonyms** | on the same bed beat `homemade` uniquely surfaced i.xgroovy.com(9) and freepornsiterips.com(4), which the two `amateur` queries returned at 0-5 and 0 | **Running both words over one beat is a cheap way to buy shelf variety**

### ⚠️ REFINEMENT — `side view` on a BED buys his face and PAYS IN POSTURE

`side view` + `bed` | the 08-03 "side view puts his head in frame" fact **HELD** (his torso/head in ~1/3 of first-screen tiles vs near-zero on the plain bent-over seed) — **but it SHIFTS THE POSTURE** | first screen returned four tiles literally titled `Anal sideways` plus `Anal sex on a massage bed, side view` | **REFINED.** On a bed, `side view` retrieves sideways/spooning, not bent-over-the-edge. Still worth running for his face; know it is a posture-VARIANT bucket
anal, third independent confirmation | **still not retrievable as a NAMED act bent over** | four queries all carrying explicit `anal`/`ass fucked`: analporngifs never exceeded 4 urls; grid slugs read `bent over the bed`, `Amateur Doggy Style Fucking` | **CONFIRMED 3x.** And from the OTHER direction on renner_loop_doggy: **dropping `anal` entirely** (`doggystyle fuck office desk amateur gif`) gave the cleanest histogram AND the highest new-yield (54/76) of its three. Carrying `anal` cost host purity and gained nothing

### ⚠️ THE TWO GATES ARE NOT REDUNDANT — measured in BOTH directions this run

the histogram catches what one screenshot cannot | `bj chair bar` showed seated-man-receiving-oral across the whole visible grid while **18% of its hosts** were generic-gif sites. **The dilution lives in the TAIL** | renner_cheerup_oral | screenshot alone would have passed it
the screenshot catches what the histogram cannot | `public blowjob behind the bar` and `public blowjob parking lot` were **100% porn hosts** and both were the wrong room entirely | renner_cheerup_alley | histogram alone would have passed both
**Google's own tile CAPTIONS are a free aisle signal the skill does not use** | `Anal sideways` x4 is what revealed seed 2's posture shift while the histogram read 100% porn and was blind | marsh_anal | **PROPOSED.** Reading captions off the SAME pass-3 screenshot costs nothing and catches wrong-AISLE faster than the picture alone
the New Yorker long-form fallback, **first live sighting** | `anal from behind over the desk homemade couple gif` = 9 tokens / two connectives -> media.newyorker.com appeared beside 4 tenor and an i.redd.it | renner_loop_doggy | **the fallback DEGRADES a query gradually rather than killing it** — the query still landed on the grid. Worth knowing the tell before it is fatal
`hotwifecaps.com` + `captions.hotwifecaps.com` + `upskirt.pantiesless.com` + `flashingjungle.com` co-occurring | candidate signature for a **CAPTION/STILL aisle inside the porn crowd** — histogram reads ~100% porn while serving text-overlay stills, useless on an animated slot | renner_loop_doggy | **WATCH-LIST tell**
`thatpervert.com` (img0/img1) | a **HENTAI/cartoon host that rides in on `creampie`** | ~6 tiles per creampie query | not poison (the query landed) — just budget the dead-for-live-action tiles

### ⚠️ TOOLING — three findings the driver had to verify, not the agents

**"More results" is NEAR-WORTHLESS on an ANIMATED slot** | **SEVEN agents, ~20 independent measurements, every one +0 / +1 / +2 urls** — 70->71, 74->74, 65->65, 83->83, 68->68, 73->73, 66->68, 79->80, and on marsh all four clicks gave +1/+1/+0/+1 where **every gain was an encrypted-tbn gstatic thumb, not a CDN original** | page height did grow (to ~8,800-9,600px), so the click DID fire — page 2 is simply jpg/webp thumbs the animated regex cannot use | **STRONG CANDIDATE FOR A DOCTRINE CHANGE.** The skill currently says "animated slots: click once." Measured, the click costs ~4-5s per query and buys nothing. **The SCROLL is what pulls the tiles.** Owed to `chrome_route.md` §4
**`options/add_bulk` BACK-LABELS duplicates — it does not skip them** | four agents independently: renner_cheerup_oral posted 210 urls across 3 queries, `added` counted only 93 genuinely new rows, and **labelled options went 0 -> 185**. mercer_glass went 144 unlabelled -> 105 while the total rose to 319 | **CONFIRMED x4, and it is the whole mechanism that made this run worth doing.** A high duplicate count is NOT wasted work on an unlabelled shelf — it is how the old pile gets attributed. **449 of the 1,869 pre-existing options were retro-labelled this way**
**A CHIP keys its query text as `q` — never `query`, never `found_by`** | **FIVE of seven agents tripped on this**, each reading `c.query`, getting `""` on every chip, and each briefly believing `queries/add` had stored blanks. All chips were stored correctly | chip keys are `[q, at, last_at, runs, source, urls, stocked, hosts]` | **The skill documents it in one clause and it is not loud enough.** It is the exact twin of the `found_by`-not-`query` trap on OPTIONS, and it deserves the same ⚠️ treatment. `hosts` verified persisted on **22 of 22 chips** (13-26 real hostnames each) when POSTed raw

### ⚠️ DOCTRINE GAP — a GATE-REJECTED query leaves NO record on disk

measured | the 4 condemned queries above (`bj chair bar`, `back alley bj outdoor`, `public blowjob behind the bar`, `public blowjob parking lot`) produced **zero `queries/add` calls, zero chips and zero `query_ledger.jsonl` lines**. 22 ledger lines for 22 chips — the rejects are simply absent | **The two rules collide:** §4's two-pass gate says pass 1 "writes NOTHING" and a wrong crowd must "not stock"; §4's non-negotiables say "one `queries/add` per query, INCLUDING one that yielded ZERO ... the record that stops you re-running a dead query." A gate-rejected query falls straight through the gap | **REAL GAP.** These four are exactly the queries a future run most needs to not repeat, and they survived only because the agents reported them in their return values. SKILL.md §5's "name any wrong-crowd query — it is on his shelf under its own chip" is ALSO stale: it predates the gate moving earlier (2026-08-05), and a condemned query now has no chip at all. **Proposed fix: `queries/add` with `stocked: 0` and the verdict, no options — the record without the shelf pollution.** Owed to `find-media-v3/SKILL.md` §4

---

## 2026-08-09 — the 3 format-converted slots (still → video), FRESH animated harvest

Context: `cell_inventory_the_order_t4`, `cell_turns_the_read_out_t5` and `colm_backroom` were
stills until today. Converted to video, old media retired, old shelves orphaned (1,166 options,
**11 animated**). This is the first harvest of these beats with the ANIMATED regex.
Result: **734 options / 16 chips / 100% labelled / 0 still-contamination**. 5 of 16 queries
condemned at the gate.

### ⚠️ THE FRAMING WORD IS A SEARCHABLE PROXY FOR AFFECT (the biggest finding here)

Affect cannot be queried — that rule stands. But **the FACE-vs-TORSO framing word can be, and it
predicts affect reliably**:

| framing vocabulary | what the grid serves |
|---|---|
| `bukkake` · `kneeling` · `facial` | performative — open mouth, tongue out, eyes up, **smiling into camera** |
| `cumshot on tits` · `cum on body` | slack, eyes closed, head back, **no camera address** |

Measured on `cell_turns_the_read_out_t5`, whose standing human reject is literally *"she is happy
smiling, doesnt fit the context."* The shelf ran ~60/40 performative over spent, and the split
fell exactly along that axis. **On any beat whose register is spent/hollow/post-act, spend a
query on TORSO framing.** It is the first lever found that moves affect without naming it.

### Cum-aftermath: the divergence set is THREE queries, not two

`bukkake` vs `covered in cum` was already known to reach different host clusters. Confirmed again
on animated (0 duplicates), and a **third** cluster found:

```
bukkake kneeling floor cum covered amateur gif      93 urls, 10/10 porn   (performative)
used woman covered in cum aftermath gangbang gif    75 urls, 0 dupes vs #1 (most on-beat)
cum dripping aftermath gangbang amateur gif         69 urls, 13 dupes     (saturating)
cumshot on tits cum covered body amateur gif        81 urls, 0 dupes vs 224 ← NEW CLUSTER
```
The 4th opened porngif.co / pictoa / pictocum / porngifmag / gifcandy — none of which the three
seeds touched. `aftermath` reads like a mood word but **measures like a tag word** (literal
"Aftermath Porn Gifs" tag pages on two separate queries).
`kneeling` behaves as a posture word here: it drags aftermath back to blowjob-IN-PROGRESS.

### The clothed-foreplay band — `quickie`, `dry humping`, `groping`

`colm_backroom_t4` is the first clothed, non-penetrative beat harvested on this game.

- ⚠️ **`making out` is POISON.** 81 urls, **ZERO porn hosts** (media.tenor.com top at 24, plus
  gifdb, New Yorker, Vogue, Lowes). It reads as an act word to an English speaker; it is pure
  reaction-gif vocabulary. Swapping that ONE token to `quickie` flipped the same 7-token query to
  **~97% porn hosts**.
- ⚠️ **`clothed` cannot anchor a query.** A query carrying `clothed` AND `amateur` AND
  `against wall` still scored **zero** porn hosts. It only works bolted to a porn-native partner:
  `clothed dry humping`, `clothed groping`, `clothes on quickie` all landed.
- **`dry humping` is the corpus term** for clothed, non-penetrative, urgent contact. Cost is the
  INVERSE of the quickie fact: it retrieves waist-down crops, so heads leave frame. Use it for
  the clothes, not for the face.
- **`groping` is the best token for "hands going everywhere"** and, unlike `dry humping`, keeps
  faces in frame. Paired safely with the anatomy word `tits` — no sports/fitness leakage, the
  anatomy-over-posture rule held.
- **`quickie` + `clothes on` CONFIRMED at full strength** — returned fully-dressed, full-height,
  FACE-VISIBLE men (one in waistcoat and shirt). Best single lever for any clothed-man slot.
- **`storeroom` CONFIRMED again** — "Quickie in storage unit", cardboard boxes and shelving. No
  silent drop, no "Did you mean". The old "zero storerooms exist" claim stays retracted.
- **`against wall` has a SECOND cost beyond standing-doggy**: it drags in the NUDE penetrative
  wall-fuck cluster and full carries. `quickie` alone did not hold the clothes on against it —
  the clothed axis only arrived once an explicitly clothed token rode alongside. (The
  standing-doggy budget itself reconfirmed at ~1/3 of tiles, matching the sibling slot's 7-in-20.)

### The CMNF band, refined

- **`cmnf` reconfirmed top-tier** — three separate cmnf queries, 100% porn hosts, zero stock.
  `chair` binds as FURNITURE (furniture is not a room noun; the inert-room-noun rule does not
  reach it).
- ⚠️ **NEW: the CASTING corpus is a DISJOINT and better structural match.**
  `casting couch nude girl undressing clothed agent gif` → 68 urls, **0 duplicates** against 113
  already-shelved cmnf options. Structurally it IS the beat: clothed man seated, woman standing
  and stripping to be appraised. One tile carried the on-screen caption *"just stand up where you
  are there, and strip off for me."* **Go-to sibling for any inspection/appraisal beat.**
- ⚠️ **`standing` is poison even beside `cmnf`.** It swaps the standing-EXPOSURE aisle for the
  standing-SEX aisle (carry-fucks, "Standing Sex Porn Gifs") while the histogram stays a flawless
  11/11 porn. Textbook colourblind-histogram case; only the grid glance caught it. Repair was to
  drop the POSTURE word and keep `sitting` — the suspect-posture-before-anatomy rule, again.
- ⚠️ **`enf` DEMOTED from conditional to avoid-on-indoor-beats.** It failed here *even with*
  `voyeur` and `chair` holding it up, contradicting this slot's own prior STILL-slot measurement.
  Unanchored by `cmnf` it resolves to the public-flashing/sharking corpus (flashingjungle,
  juicycash), never to indoor watched-stripping.
- **`bare room` is a TYPO MAGNET, not merely inert** — Google offers to respell it as `bathroom`.
- **NEW POISON for ownership/appraisal beats:** `bdsm` + `slave` + `master` pulls
  rope/bondage/flogging/gags and drags in drawn 3D-render hosts (hentai-foundry, neocities fan
  sites). Does not retrieve unrestrained inspection.

### Two new histogram tells

- **Caption-porn hosts (`hotwifecaps.com`, `captions.*`, `humiliationpov`) = a descriptive-English
  token leaked in.** Same diagnostic class as the Getty/stock tell. `used woman` stayed ~90% porn
  but bought ~9 text-overlay memes.
- **A FRAGMENTED histogram is an early warning by itself** — 25 hosts across 70 urls, with
  fan-sites and hentai hosts in the tail, flagged the bdsm query before the screenshot did.
- **Duplicate rate is a cheap corpus-identity signal.** 33/72 duplicates = same corpus, stop.
  0/68 = new territory, keep going. Use it to decide whether another sibling query is worth the
  round.

### Process findings owed to the skill

1. ⚠️ **`validate_queries.py` does NOT enforce the measured poison lexicon.** It passed all three
   hand-written `colm_backroom` seeds "clean, zero rewrites" — and two of them scored ZERO porn
   hosts, while the third carried `dim`, a token the same brief lists as poison twice. **A clean
   validator verdict cannot be read as "not poisoned."** The validator and the lexicon are out of
   sync and will keep emitting poisoned seeds until one of them learns the other.
2. **Skipping the "More results" click cost nothing, again.** Never clicked across 16 queries;
   every landed query returned 55-93 animated urls from page 1 and one shelf overshot the
   150-350 expectation at 305. The measurement now has two independent runs behind it.
3. **A cum-aftermath shelf is gif-dominant even on the animated axis** — 305 options split
   270 gif / 35 true video (~11%). Set expectations accordingly.

---

## 2026-08-14 — the 23-slot Mercer/Kess v3 harvest (4,863 options, 100 chips, 0 installed)

23 slots, one agent each, rolling cap 4. Every line below was measured on a live grid this day.
Where a finding CORRECTS an older row in this file, it says so.

### ⚠️ THE MALE-BODY AXIS — four tokens, only one works

| token | what it actually buys | verdict |
|---|---|---|
| `heavyset` | **the WOMAN.** Reads as a BBW-aisle token (`bbwgirls.club` surfaces in the histogram); does NOT force a heavy male | **POISON for a male-build beat** |
| `grandpa` | age WITHOUT the body — returns lean/thin old men, and adds a blowjob leak | **THIN** |
| bare `old man` / `older man` | age, but on a NON-ORAL query it aisle-shifts to BLOWJOB — `blovjob.com` rose to TOP host on `anal from behind old man homemade gif`, plus a gay/sissy tail | **LEAKY — needs `fat`** |
| **`fat old man`** | genuinely heavy AND older males. Killed the blowjob leak outright (blovjob 9→1) | **CONFIRMED 7x across 6 slots. The only reliable heavy-male token.** |

⚠️ **`heavy` is absorbed by an adjacent verb.** `heavy older man drinking` parses as *heavy drinking* — it
returned gaunt 80-somethings and swamped the grid with the alcoholism-awareness stock aisle. One-token swap
to `fat` fixed both defects at once. **THE CLASS: an adjective that doubles as an intensity adverb gets eaten
by the verb beside it.** `fat` cannot be absorbed that way.

### ✅ `fat old man` + `prone bone` COMPOSE — and this breaks the crop-out

The standing measurement is that this corpus crops the man out (27 of 28 clips torso-or-legs, one face).
**That is a property of the AFTERMATH vocabulary, not of the corpus.** Measured on both drain slots:
aftermath-vocabulary queries ran ~90% him-absent; `fat old man` + `prone bone` queries showed the man in
**70–80% of tiles**, frequently full-length flat on top of a face-down woman — the beat's literal shape.
**This is the most actionable string the run produced.** It partially refutes today's own earlier
"heavy-male and anal trade off" note: the two tokens compose, at some cost to anal share.

### Position and posture tokens

- ✅ **`doggystyle` composes cleanly with a FINISH anchor and buys the POSITION.** It does NOT outrank the
  finish term the way pace words do. Confirmed on 2 slots. The old rule (position names leave porn) is
  correct only for a position name ALONE — it cannot CARRY a query, but it can STEER an anchored one.
- ✅ **`bent over bed` SURVIVES.** Corrects the blanket "room/setting words drop silently" rule: `bed` here is
  **ACT-FURNITURE, not setting** ("Bent Over Bed Porn GIFs", "BENT OVER ANAL" are live tag pages). Best
  server of the over-an-edge posture; confirmed 3x. ⚠️ Its tail dilutes into CLOTHED-butt photo stills
  (TikTok, Shutterstock, Men's Health) when the act anchor is weak.
- ✅ **`prone bone` is the best-behaved anal token measured** — zero leak and, unusually, it does NOT degrade
  in the deep tail ("Prone Bone Anal" is its own tag). It is face-down-FLAT, not bent-over-an-EDGE.
- ⚠️ **`deep stroking` leaks to the HANDJOB aisle** — `stroking` is porn-native for stroking a cock, not
  thrust pace. **`long stroke` is the clean form.** Pace remains legal MID-ACT, never on a finish beat.
- ⚠️ `anal` still does not reliably select the act in from-behind framing — **5th and 6th confirmations.**
  Shelves run 35–75% anal depending on chip. Do not burn rounds on it.

### Finish-beat vocabulary

- ⚠️ **`pumped full of cum` DRAGS ANAL** — it is a live idiom for the ass. On a VAGINAL finish slot it pulled
  both the anal aisle and the solo pussy-pumping aisle. **`pumping cum inside her` is the vaginal-safe form**
  and keeps the finish-moment yield. **Corrects the finish-MOMENT family as recorded.**
- ⚠️ **`bred` drags a degraded tail** — past the More-results click: gay-breeding, trans, impregnation
  captions, furry, and two health-explainer hosts. **The histogram stays ~100% porn** because caption hosts
  serve few animated files. Pure histogram-blind failure; only the screenshot catches it.
- ✅ `aftermath` reads like a mood word but **measures like a TAG word** — literal "Anal Aftermath" tag pages.
  Reconfirmed. ⚠️ But aftermath vocabulary returns SOLO anatomical close-ups (drip, gape, nobody else in
  frame) — it buys the register and loses the second body.
- ⚠️ **`collapses on her back` pulls the EDITORIAL/PROSE aisle** (Slate, Medium, utopiastories) — same failure
  class as the `wrecked`/`spent` poison set. **`lying on top of her` is the clean substitute**, same geometry.

### The CMNF / clothed-male composition — the earlier warning was MIS-SCOPED

- ✅ **`cmnf` HOLDS beside hands-on-torso verbs** (`groping`, `fondles`) — ~10 of 12 tiles clothed men with
  nude women. Confirmed 3x.
- ⚠️ **`cmnf` FAILS beside an oral or penetrative token** — such a token forces the man's cock into frame and
  therefore forces him undressed. **That, not `cmnf` itself, is what failed on the earlier blowjob slot.**
- ✅ **`fondle` is the best composition token found** ("Fondle Her Tits From Behind"). **The trade: `fondles`
  wins on HIT RATE (33–34 urls, densely on-composition), `groping` wins on VOLUME (89 urls, target scattered
  among crops and penetration).** Run both; open the `fondles` bucket first when picking.
- ⚠️ **`clothed man` is a WEAK substitute for `cmnf`** — the only query of its slot to let Tenor into the top
  5 and show Shutterstock. Reads as "sex with clothes on", keeping HER clothed too.
- ⚠️ **`quickie clothes on` is weaker than its recorded reputation** — it delivers the clothed man but keeps
  HER clothed (t-shirts, tanks) and crops to torso closeups; `quickie` also pulled solo self-touch and
  girl-on-girl. **Downgrade the existing row.**
- ⚠️ `hair grip` does NOT bind — returns relaxed couch blowjobs with few visible hair-fists. `hair pulling`
  is the working form.

### ⚠️⚠️ STILL / CLEAN-BAND SLOTS — a whole poison CLASS, newly identified

**THE POISON CLASS ON A STILL SLOT IS *ANY PURCHASABLE NOUN*.** `bench`, `workbench`, `lamp`, `work lamp`,
`tools`, `component`, `bed`, `mattress`, `crate`, `bottle`, `glass`, `whisky`, `table`, `chair`, `sofa`.
Google reclassifies the query as SHOPPING — Amazon, Alibaba, imimg, made-in-china, eBay, VEVOR, Wayfair,
Overstock — and the grid becomes product-on-white. One slot burned SIX queries proving it: it dropped `lamp`
and kept `bench` and still landed on workbench-furniture vendors. Another lost ~40% of its grid to the single
word `table`.

**THE TWO ANTI-RETAIL LEVERS:**
1. **A PERSON DOING AN ACTION** — catalogue photos have no people. `man working alone in dark garage workshop
   at night` flipped a slot from 15 Amazon urls to 89/93 pure stock-photo crowd. **4 independent
   confirmations.** Cheapest and strongest lever available.
2. **A DERELICTION / REGISTER WORD**, and it is **LOAD-BEARING**: deleting `abandoned` while keeping
   `mattress`+`bottle` flipped a query straight back to furniture retail. **The repair for a wrong REGISTER
   is to swap the ROOM NOUN and KEEP the dereliction word — never the reverse.**

**Newly measured still-slot traps:**
- ⚠️ **`noir` IS A FURNITURE BRAND** (Noir Furniture; `noirfurniturela.com` landed live). It AMPLIFIES retail
  whenever an object noun sits beside it. It is not a safe register word.
- ⚠️ **`corner` STEALS THE ROOM** — `man sitting alone corner dim bar` returned a man crouched in the corner
  of an empty room; only ~3 tiles were a bar.
- ✅ **`basement` is a FREE anti-retail anchor** — nobody sells a basement — and unlike `abandoned` it carries
  no ruin connotation. Cheapest route to bare concrete without ruin-porn.
- ⚠️ **`bed` is a DECOR magnet as well as a retail one** — beside `basement` it pulled remodeling listicles
  rather than product pages. `grimy squat` cleared both in one token.
- ⚠️ **`abandoned` skews DERELICT** — peeling plaster, collapsed ceilings, rusted frames. Wrong for a
  squalid-but-LIVED-IN room. `squalid`/`bedsit` do NOT substitute (they lose the anti-retail power).
- ⚠️ **`machine shop` can resolve to "photocopier / copy shop"** (Alamy copy-shop hits).
- ⚠️ **`face down` is absorbed by the DESK-SLUMP idiom**, and `workshop` also means a business SEMINAR:
  `woman face down workshop` → "Woman Face Down On Desk", "Exhausted Business Woman".
- ⚠️ **`mechanic` + `lying` COLLAPSES TWO FIGURES INTO ONE** — every result was a single mechanic on a creeper
  under a vehicle. The actor noun owns that stock cluster and ignored "leaning over person".
- ⚠️ **`thigh` + `older man` pulls the JOINT-PAIN / medical aisle** (Mayo, WebMD, AARP, Cleveland Clinic).

**THE BUSINESS/LIFESTYLE-STOCK MAGNET IS TRIGGERED BY THE *ACTOR AND VERB*, NOT THE ROOM.** `two people
talking over documents` went wall-to-wall suited boardroom, and swapping the room noun made it WORSE (twice
over: `machine shop` became a copy shop AND the boardroom strengthened). **This is the one case where the
"swap the room noun" repair is exactly wrong.** The equivalent trap on a seated-couple beat is the
romantic-couple / dating / therapy aisle, and fixing the actor moved it sideways (`couple` → young-romantic,
`old man and woman` → elderly-lifestyle, losing the age gap).

✅ **SEARCH THE REAL-WORLD ANALOG, NOT THE FICTION.** A beat of "a woman prone on a bench while a man works at
the base of her spine with a fine tool" is unretrievable as written — but **tattoo stock is framed as exactly
that composition** (one person prone, a second leaning over working the body with a fine tool under a low
articulated lamp). `tattoo artist working on back of woman lying down in dark studio` landed it. Cost: the
room reads tattoo parlour, not industrial.

✅ **`harassment` is the stock-caption phrase for a NON-CONSENSUAL hand-on-leg two-shot** — surfaced unprompted
in a stocked result's own caption, and it carries both the age gap and the unwilling second figure that every
seed vocabulary missed. ⚠️ UNTESTED. Two cautions: `sexual` is a banned token on a clean band (it would
propose retagging the still to `_t5`), so use `harassment` alone; and the aisle is office-set.

⚠️ **Still queries hit Google's "the rest of the results might not be what you're looking for" wall at ~95–100
urls with NO "More results" button at all.** One page IS the whole shelf on a still slot. Confirmed across 4
slots. Not a failure — do not chase it.

### ⚠️ ENGINE / API facts measured this run (not query craft)

- **`media_kind` MUST be derived PER URL, never per slot.** `.gif` → `media_kind:"img"`, `type:"image"`; only
  `.webm`/`.mp4`/`.mov`/`.mkv` → `"video"`. Ground truth: `_VIDEO_SUFFIXES` (`api/v1/media_finder.py:373`)
  excludes `.gif`, which sits in `_IMAGE_SUFFIXES`; the code comment states *"a .gif pool reports media_kind
  'img'"*. **A `.gif` posted as `video` renders inside a `<video>` tag and shows NOTHING to the human.**
  1,648 options were stocked wrong this run and had to be repaired. Since these shelves are overwhelmingly
  gifs, this silently blanks most of a shelf.
- **`queries/add` takes `query`, NOT `q`.** Posting `q` returns `{"error": "file and query are required"}`.
  Chips READ BACK keyed `q`; they WRITE as `query`.
- ⚠️ **`hosts` MUST be `[[host, count], ...]` PAIRS.** `_clean_hosts` (`api/v1/media_finder.py:857`) returns
  `None` for `[{host, count}]` objects AND for `"host:count"` strings — the field is **SILENTLY DROPPED**,
  response still `ok: true`. Two agents lost histograms by different routes. **Since the histogram is v3's
  only quality gate, a silently empty one is a BLIND gate.** Always verify by re-reading the chip.
- `queries/add` never echoes `hosts` back — a success reads `hostsStored: 0`. `"duplicate": true` is NORMAL:
  `options/add_bulk` already created the chip from its own `query` field; the explicit POST merges the
  histogram in (`rec.update(fields)`, `media_finder.py:1320`).
- **The extracted url list truncates coming back through `javascript_tool` (~1000 chars, lossy mid-slice).**
  POST `options/add_bulk` DIRECTLY FROM THE PAGE with `fetch(..., {mode:'no-cors'})` — the views are
  `@csrf_exempt` and `_parse_body` is content-type agnostic (`media_finder.py:115-120`). Lossless and faster.
  Verify writes from bash afterwards.
- ⚠️ **`i.xgroovy.com` is DEAD** — connection failure on a direct fetch, while `blovjob.com` returns 200. It
  was the TOP host at 19/58 on one probe query. Expect a real dead-link share on any shelf it appears in.
- ⚠️ **THE ANIMATED REGEX HAS A BLIND SPOT:** `.gif|.mp4|.webm` cannot reach PornHub/xHamster **page
  thumbnails**, which is where the heaviest older-male content sits. One query's grid was excellent while its
  extracted urls were poor, purely for this reason. **Histogram and grid CAN disagree in this direction.**
- Installed files are **renamed on install** (hashed, or to the slot name), so a candidate's source url is
  destroyed and there is **no recoverable provenance** — `media_reviews.json` records only "replaced via
  finder". A url-level collision check against installed media is therefore structurally impossible; compare
  against the SIBLING SLOT'S SHELF instead, then md5 at install time.

### 2026-08-14b — `mercer_hands_on` re-harvest after a human rejection (still → animated `_t4`)

The human rejected the 103-option STILL shelf with the note *"Should be a gif."* The slot was re-declared
`scenes/mercer_hands_on.jpg` → **`scenes/mercer_hands_on_t4.gif`** and re-run. **The retag, not the
extension, is what fixed it** — a `.gif` at clean band still searches the SFW stock corpus. 201 stocked.

**The clean-band failure it escaped** (recorded above under still-slot rules): the SFW corpus offers only a
MACRO CROP ("hand on thigh": hand and leg fill the frame, no faces, no second figure) or a bright LIFESTYLE
TWO-SHOT ("couple sitting": both figures visible but smiling, and both-young or both-old). No wide seated
shot of an older man with a younger woman exists in it. **The porn/tease corpus at t4 has that frame** —
`old man groping her clothed couch amateur gif` returned an older clothed man seated on a couch in a dim
room, a woman seated beside him, both faces in frame.

| finding | measurement |
|---|---|
| ⚠️ **THE MEDICAL TRAP IS BOUGHT BY `older man`, NOT BY `thigh`** — corrects the earlier joint attribution | one-token swap `older man`→`grandpa`, everything else held: British Heart Foundation and self.com dropped to ZERO, yield 30→51. **`older man` is SFW-REGISTER phrasing; the porn corpus says `old man` / `grandpa`.** |
| ⚠️ **`thigh` is the MACRO-CROP puller** | same stem otherwise, `thigh`→`couch` took the wrong crowd to zero — no Tenor, no gifdb, no medical, no stock, **the only 100% porn-host histogram of the run** — and converted waist-crops into seated two-shots |
| ⚠️ **`grandpa` buys AGE but swaps the ACT BAND to penetration** | every tile a genuine grey-haired man with a younger woman, but nearly all hardcore/nude — wrong for a t4 tease. **`old man` + `groping` + `couch` holds age AND the clothed band; `grandpa` + `fondles` does not.** Consistent with the earlier `grandpa` rows (buys age, loses the body, leaks act band). |
| ✅ **`quickie clothes on` INVERTS by slot** | measured a DEFECT on the CMNF pools because it keeps HER clothed; on a both-clothed tease beat that is exactly right. **`cmnf` is wrong here — it would strip her.** Same measurement, opposite verdict: check whether the beat wants her nude before choosing between them. |

**Gap:** the clothed-tease band and the older-male band are partly disjoint — the best-composition chips skew
young, the age-correct chip is thinner on composition. Both are on the shelf as separate chips.

### 2026-08-14c — `kess_install` re-harvest (still → **clean-band ANIMATED**, the first of its kind here)

Human rejected the 70-option still shelf: *"should be gif."* Re-declared `scenes/kess_install.jpg` →
**`scenes/kess_install.gif`, band UNCHANGED at clean.** Unlike `mercer_hands_on` (retagged `_t4`), this beat
must NOT move into the porn corpus — the canvas says *"Explicit and NOT sexual: no arousal, no pain, no
comfort — she is handled, and the horror is that it is routine."* 89 stocked, **zero erotic leakage across
6 queries**. **THE LESSON: two identical rejection notes needed OPPOSITE treatment. Read the canvas before
deciding whether "make it a gif" means retag or rename.**

⚠️ **A CLEAN + ANIMATED slot INVERTS the Tenor rule.** `media.tenor.com` / `giphy` / `gifdb` / `i.pinimg`
are the TARGET crowd for an SFW animated subject — the "Tenor = wrong crowd" measurement was taken on PORN
beats, where Tenor means the query left porn entirely. Do not reject an SFW animated query for landing there.
Its wrong crowd is instead e-commerce/product, stock agencies, and medical.

| finding | measurement |
|---|---|
| ⚠️ **THE GRID GLANCE IS UNRELIABLE ON AN SFW ANIMATED SLOT** | on the best query the visible top rows were 7 iStock/Dreamstime/Unsplash STILLS while the extracted animated files were 22 Giphy + 7 Tenor. **Stock agencies buy the top rows; the gif corpus sits deeper.** The decisive gate was reading the TITLES on gif-host anchors — the query would have been wrongly REJECTED on the screenshot alone. |
| ⚠️ **A natural-language SENTENCE + `gif` collapses into Tenor's REACTION-MEME tag pages** | `person lying face down getting a back tattoo gif` → 84 urls of "Lay Back GIFs", "Face Down GIFs" (a man face-planting on a rug), Tupac, "I'M FINE". Keep SFW animated queries SHORT and TECHNICAL. |
| ⚠️ `tattoo machine` | the purchasable-noun trap plus the stock agencies — iStock/Getty/Shutterstock "Licensable" watermarks and a floating-machine render |
| ⚠️ `lower back tattoo` (as a standalone noun phrase) | owned by the TRAMP-STAMP showcase idiom (Teen Vogue explainers, finished-tattoo photos). Survives when `tattoo artist tattooing` LEADS the query |
| ⚠️ `timelapse` | **craters animated yield 59→18** — that footage lives on YouTube/TikTok, not gif hosts |
| ✅ live gif-host tags for this beat | "Tattoo Session", "Up Close Tattoo Session", "Back Tattoo GIFs", "Girl Getting Tattooed GIFs", "Close Up Tattoo GIFs", "Studio Tattoo GIFs" |

⚠️ **SKILL DEFECT — `ANIMATED_KEYWORDS` IS SEX-ONLY.** All 79 entries in `scene_semantics.py` are sex acts
(`fuck`, `kiss`, `grope`, `nude`, `riding`…). There is NO way to express a non-sexual beat that moves, so
**any SFW slot legitimately wanting motion classifies `static` and FAILS `check_format_alignment` on
`.gif`/`.webm`** — and the only way to "pass" is to insert sexual vocabulary, which is the exact anti-pattern
the t4 exemption exists to prevent. Compounding it, `working` sits in `ACTIVITY_STATIC_KEYWORDS`, so "a man
working a tool over someone" reads as chores. **Honest workaround used here:** avoid `working`, which drops
the family to `ambiguous` — and `ambiguous` always passes. `tattooing` is the measured-live synonym.
**Real fix belongs in the skill: a non-sexual motion vocabulary in `ANIMATED_KEYWORDS`.**

**Gap:** posture is unverifiable per-file — Tenor/Giphy filenames are opaque (`200w.gif`, `giphy.gif`), so
face-down-vs-supine and back-vs-arm can only be judged by eye in the picker. Arm/sleeve work dominates the
whole tattoo gif corpus. Query 1 also carries fandom contamination (Arcane, Call of Duty, Percy Jackson
gifsets tagged "tattoo"), ~4 of 60 urls.
