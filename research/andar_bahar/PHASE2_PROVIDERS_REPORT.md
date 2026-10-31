# Andar Bahar — Phase 2: 1xBet Platform and Game Provider Investigation

Research date: 2026-10-30. Method: web research by four parallel researchers (one per
provider, one on 1xBet and Vivo), every load-bearing claim re-fetched and checked by
hand, every payout table re-priced against the exact model in `andar_bahar_model.py`
by `provider_tables.py` in this folder.

Trust labels used throughout:

- **PRIMARY** — the provider, the operator, a regulator, a court, or a test lab.
- **TRADE** — iGaming Business, SBC, Gaming Intelligence, CasinoBeats, casino.org news desk.
- **REVIEW** — affiliate and review sites. Low trust. Used only where nothing better
  exists, and said so each time.
- **UNVERIFIED** — nothing better than REVIEW, or sources conflict.

Access limits that shaped the evidence: ezugi.com blocks automated fetches, Pragmatic Play
has no Andar Bahar page on its site, 1xBet's lobby is rendered by JavaScript and shows no
game tiles to a fetch, and web.archive.org was unreachable from this environment. No
provider publishes an RTP or a paytable for its Andar Bahar table on a reachable page.

---

## 1. Which Andar Bahar tables 1xBet offers

**PRIMARY.** 1xBet's own Indian-market Andar Bahar landing page names four live
providers: Ezugi ("the first provider to offer Andar Bahar online"), Evolution Gaming
("over 10 optional side bets and random multipliers up to 4,000x", which is Super Andar
Bahar), Pragmatic Play, and Vivo Gaming ("well known for its lower minimum bets").
Source: https://indian.1xbet.com/en/casino/andar-bahar

**PRIMARY.** 1xBet's main casino page lists its live suppliers as "Evolution, SA Gaming,
Vivo Gaming, and Ezugi". Source: https://1xbet.com/en/casino

**PRIMARY.** 1xBet also runs an in-house RNG title, "Andar Bahar Game" under 1xGames,
with its own rules page. Provider is not named ("the game developer"). Stakes INR 20 to
INR 11,876. No demo mode. Source: https://indian.1xbet.com/en/games/andar-bahar

**TRADE.** Pragmatic Play's live suite launched on 1xBet in May 2019 with a dedicated
studio environment. Vivo built exclusive baccarat tables for 1xBet in 2019.
Sources: https://casinobeats.com/2019/05/29/pragmatic-play-takes-live-portfolio-to-1xbet/ ;
https://lcb.org/news/1xbet-reveals-completely-fresh-offering-of-vivo-gaming-s-baccarat-tables

**REVIEW, UNVERIFIED.** Affiliate pages additionally list Ezugi "Ultimate Andar Bahar",
Ezugi "Casino Marina Andar Bahar" (the OTT table from Colombo), Playtech, Live88,
7Mojos and XPG tables on 1xBet. None confirmed.

So the candidate set on your account is at least five: Ezugi, Evolution Super Andar
Bahar, Pragmatic Play Live, Vivo, and the in-house RNG game. The lobby could not be read
remotely. Task 4 settles which one you actually have.

---

## 2. Provider-by-provider findings

### 2a. Ezugi (Evolution group)

**Ownership.** PRIMARY. Evolution announced the acquisition on 21 Nov 2018 and completed
it on 9 Jan 2019. Sources: https://news.cision.com/evolution/r/evolution-gaming-to-acquire-ezugi,c2679362 ;
https://news.cision.com/evolution/r/evolution-gaming-completes-acquisition-of-ezugi,c2714694

**Variants.** TRADE. Studio "Andar Bahar" launched 8 Aug 2019 from Bucharest. "OTT Andar
Bahar" launched 17 Nov 2020, streamed from the Marina Casino in Colombo, Sri Lanka, with
"additional betting rounds every game compared to the studio version". "Ultimate Andar
Bahar" launched 24 Nov 2022 with 2x/3x/5x card multipliers and a UI refresh of the
standard table at the same time.
Sources: https://soloazar.com/en/category/online-games/ezugi-enhances-offering-with-andar-bahar-game-and-its-baccarat-30 ;
https://www.intergameonline.com/igaming/ezugi-breaks-new-ground-with-ott-andar-bahar ;
https://www.gamingintelligence.com/studio-showcase/?p=3672

**Architecture.** Live dealer, physical cards, one 52-card deck. Deck count is REVIEW
only; Ezugi's own page is unreachable. Shuffle: a Bucharest job posting for "Shuffler for
online Casino" ("Shuffles and changes the cards on the Live tables", logging each shuffle)
shows a human shuffler role; whether a machine is also used and whether the deck is
reshuffled every round or every N rounds is UNVERIFIED. Review sites say every round.
Source: https://www.hipo.ro/locuri-de-munca/locuri_de_munca/178084/Ezugi/Shuffler-for-online-Casino

**Which side gets the first card.** CONFLICTING. The Wizard of Odds wrote in Nov 2019
"At Ezugi, the Andar side always gets the first card. Wins on that side pay 0.9 and on
Bahar pay 1." Review sites in 2025–26 say the first card goes to Bahar and Bahar pays
0.9:1. One review site says the joker's colour decides. The Nov 2022 UI refresh could
explain a rule change; that is inference. The in-game help panel settles it.
Source: https://wizardofvegas.com/forum/gambling/other-games/33989-andar-bahar/

**Payouts.** First-card side 0.9:1, other side 1:1 (consistent everywhere). Card-count
side bet 2.5 / 3.5 / 4.5 / 3.5 / 14 / 24 / 49 / 119 to 1 for 1–5 / 6–10 / 11–15 / 16–25 /
26–30 / 31–35 / 36–40 / 41+. REVIEW, but the table matches Wizard of Odds' generic table
exactly and prices cleanly (section 4). OTT adds "Andar 2nd Bet" paying 1:1 and "Bahar 2nd
Bet" paying "0.25 to 1:1", trigger conditions UNVERIFIED.

**Published RTP.** A search snippet of Ezugi's own OTT page says "Theoretical RTP of Andar
Bahar main bet is 94.85%". That number is not derivable from 0.9:1 / 1:1 payouts (which
give 97.85% and 97.00%). Unresolved. Flag for the in-game panel.
Source snippet: https://old.ezugi.com/game/ott-andar-bahar/ (host unreachable here)

**Licences and labs.** PRIMARY. Evolution's licence page lists for Ezugi: Romania ONJN
licence 2115/27.09.2018, Curaçao accreditation certificate, Malta MGA Recognition Notice
RN/141/2019. Ezugi's GB supply runs under Evolution Malta's UKGC licence; 11 games
including Andar Bahar were certified for GB in Jan 2022. BMM audited Ezugi's Colombian
studio for Coljuegos. No GLI, iTech Labs or eCOGRA certificate naming Ezugi was found.
Sources: https://www.evolution.com/about/licences ;
https://casinobeats.com/2022/01/06/ezugi-takes-momentous-step-upon-securing-uk-entry/ ;
https://casinobeats.com/?p=49414

**History in the UI.** Last 100 rounds shown in-game (TRADE, 2019 launch coverage). No
public data feed.

**Provably fair.** None. Evolution mentions a certified RNG only for Ezugi's EZ Dealer
Roulette (pre-recorded video plus RNG), not for live card tables.

**Incidents.** No regulatory action, fine, or documented fairness dispute involving Ezugi
Andar Bahar was found. One Lithuanian finding (2023) that an operator offered Ezugi Sic Bo
without the right certificate: operator breach, no sanction.

### 2b. Evolution (own brand): Super Andar Bahar

**Exists.** PRIMARY. Launched 27 Apr 2022 under Evolution's own name. Live dealer, ten
optional side bets on card count ("Cards 1–5" through "Cards 46–49"), one to five random
multipliers applied to side bets each round, up to 4,000x. Evolution's game page states
"the dealer will deal cards first to Andar, then to the Bahar, alternating between the two
sides." Deck count, shuffle method, reshuffle cadence, RTP and studio city are not on the
page.
Sources: https://www.evolution.com/news/evolution-launches-super-andar-bahar-indian-classic-with-added-massive-multipliers ;
https://games.evolution.com/live-casino/super-andar-bahar/

**Payouts.** REVIEW. Andar 0.9:1, Bahar 1:1. Side-bet base payouts 2 / 3 / 4 / 5 / 8 / 12 /
20 / 40 / 110 / 800 to 1 across the ten five-card buckets, with multipliers lifting the top
bucket to 3,999:1. Review sites quote 96% side-bet RTP. Priced without multipliers, the
base table returns 76% to 87% (section 4), so the multipliers carry 10 to 20 points of
return, and their frequency and distribution are published nowhere found. That makes the
side bets unauditable from outside.

**Licences and labs.** PRIMARY. Malta MGA/B2B/187/2010; UKGC account 41655 (Gambling
Software and Game Host, active, one regulatory action listed); New Jersey, Pennsylvania,
Michigan and other US licences. eCOGRA live-dealer certification dates from 2010; current
status unverified. No GLI, BMM or iTech Labs certificate naming Evolution was found.
Sources: https://www.gamblingcommission.gov.uk/public-register/business/detail/41655

**History in the UI.** Not stated by Evolution. Third-party trackers log results.

**Provably fair.** None.

**Incidents.** All PRIMARY unless marked.

- **Michigan Gaming Control Board, three orders filed 9 June 2026, $40,000 each.** Read
  from the orders themselves. SDA-2025-17: on 27 Feb, 3 Mar and 5 Mar 2025 "a game
  presenter/shuffler/dealer failed to follow the card shuffling procedures by not
  consistently completing the required number of single riffle shuffles. The employee also
  manipulated the cards to predetermine the outcomes of the first hands of four different
  blackjack games", one participant in all four, impact $9,977.50, self-reported.
  SDA-2026-3: 10–24 Dec 2024, "three game presenters/dealers from Evolution blocked camera
  views of the gaming table and were able to manually input an incorrect game outcome number
  for four craps game rounds", 18 participants, impact $177,961, Board notified seven days
  late. Both cite GLI-19 v3.0 Appendix C.6, "detect and prevent patron/dealer collusion".
  Sources: https://gamblingharm.org/wp-content/uploads/2026/06/Evolution-Final-Decision-and-Order-AOV-SDA-2025-17.pdf ;
  https://gamblingharm.org/wp-content/uploads/2026/06/Evolution-Final-Decision-and-Order-AOV-SDA-2026-3.pdf
- **New Jersey DGE, July 2025, $12,000** for dealer errors including "more than 400 rounds
  with a deck short five cards". Source: https://www.nj.gov/oag/ge/docs/Rulings/2025/jul16_31/B6evolutionailoc.pdf
- **Pennsylvania GCB, 2024,** $7,500 (unauthorised person in the studio) and $25,000
  (surveillance footage lost for two days). Source: https://gamingcontrolboard.pa.gov/node/608916
- **UK Gambling Commission, 23 July 2026, £4,750,000** in lieu of penalty for AML
  failures: Evolution games on six unlicensed sites serving GB consumers. Not a game-fairness
  finding. Source: https://www.gamblingcommission.gov.uk/news/article/evolution-malta-holding-limited-to-pay-gbp4-75m
- **2021 anonymous report and NJ DGE review.** Closed Feb 2024 with no action; the
  regulator "found no evidence that Evolution sanctioned, promoted, permitted, or otherwise
  materially benefitted" (Evolution's quotation of the regulator; no DGE document found).
  Evolution's defamation suit later named Black Cube and, in Oct 2025, Playtech as the
  client (Evolution's allegation; Playtech denies). An Evolution-commissioned Spectrum
  Gaming report unsealed in Sept 2026 found Evolution "does not review the operator's
  compliance" with enhanced due diligence. A market-access and compliance fight, not a
  shuffle-integrity one.
  Sources: https://news.cision.com/evolution/r/new-jersey-division-of-gaming-enforcement-has-closed-its-investigation-of-evolution-ab-with-no-furth,c3931925 ;
  https://igamingbusiness.com/legal-compliance/what-we-learned-from-spectrum-gamings-evolution-report/

What the Michigan orders mean for this project: dealer-side outcome manipulation at a
top-tier live studio is documented fact, not speculation. It was small, caught, and
self-reported because Michigan requires GLI-19 collusion controls and a regulator reads the
incident reports. The same studios serve 1xBet's Curaçao-licensed lobby, where no such
regulator exists. Studio controls travel with the provider; regulatory scrutiny does not.

### 2c. Pragmatic Play Live

**Exists.** TRADE. Launched 6 Oct 2021, live dealer, Bucharest studio (ONJN Class II
licence, April 2019). Pragmatic Play's site has no game page; its live-casino page carries
only a paragraph ("the odds are 50/50", which is wrong, see Phase 1).
Sources: https://igamingbusiness.com/company-news/pragmatic-play-rolls-out-two-new-indian-focused-live-casino-products ;
https://news.worldcasinodirectory.com/pragmatic-play-adds-pair-of-new-indian-themed-games-to-live-casino-portfolio-97256 ;
https://www.pragmaticplay.com/en/live-casino/

**Architecture.** One 52-card deck, first card to Andar, new shuffled deck each round:
REVIEW only. Shuffle machine versus manual: CONFLICTING across review sites. Pragmatic's
live page says "a team of shufflers is ensuring that card games are operating without
interruptions", suggesting manual shuffling by staff.

**Payouts.** REVIEW, consistent across four sites. Andar 0.9:1, Bahar 1:1. Card-count side
bet 2.5 / 3.5 / 4.5 / 3.5 / 14.5 / 24.5 / 49 / 119 to 1. "First on Andar" 15:1, "First on
Bahar" 15.5:1. "First Three" poker side bet on joker plus first two cards: straight flush
120:1, straight 8:1, flush 5:1. No second-bet window described. Limits reported as 0.10 to
5,000 (currency unstated). Betting time 15 seconds.

**Licences and labs.** PRIMARY. UKGC account 56015, Pragmatic Play (Gibraltar) Limited,
remote gambling software and game host, active, "Regulatory actions: None listed".
Gibraltar B2B licence (2018), MGA recognition notice (2019), ONJN Class II (2019). Site
claims RNG certification by GLI, Quinel and Gaming Associates (RNG games, not live) and
live certification "by an independent and internationally recognised Accredited Testing
Facility", unnamed. Gaming Associates certified live titles for Colombia in June 2021,
before Andar Bahar existed. No lab certificate naming Pragmatic's Andar Bahar was found.
Sources: https://www.gamblingcommission.gov.uk/public-register/business/detail/56015 ;
https://www.pragmaticplay.com/en/about-us/

**History in the UI.** Last 27 results in a baccarat-style road (REVIEW).

**Provably fair.** None.

**Incidents.** PRIMARY. Ontario AGCO, 7 May 2026: CA$40,000 penalty on Arrise Solutions
(the Pragmatic Play content supplier) for games appearing on unregulated sites. Named in
the Aug 2025 Los Angeles civil suit against Stake.us; Pragmatic exited US sweepstakes
after. Both market-access matters. No fairness finding, no studio incident, no dealer
case found. The "TopGame rigged RNG" origin story circulates on one unsourced page and is an
allegation about slots a decade ago.
Source: https://www.agco.ca/en/news/agco-takes-enforcement-action-against-two-companies-allowing-their-games-unregulated-gaming

### 2d. Vivo Gaming (additional candidate)

PRIMARY: Vivo's site describes a live-dealer Andar Bahar with "a real-life dealer using
physical playing cards" and "a standard deck of cards", dealt by in-region native speakers.
Compliance page: "Operating under a Gaming Curacao license", licence numbers "shared under
NDA", no lab named. TRADE: GLI audited Vivo studios in Colombia, Bulgaria and Cambodia
(2021) for Isle of Man supply; whether Andar Bahar is in any certified scope is UNVERIFIED.
Payouts, shuffle method and reshuffle cadence are published nowhere. Review sites conflict
on whether the table has side bets or a three-stage "Double Up" format.
Sources: https://vivogaming.com/games/andar-bahar/ ; https://vivogaming.com/compliance/ ;
https://www.gamblingnews.com/news/vivo-gaming-studios-complete-successful-gli-audit/

### 2e. 1xBet in-house RNG "Andar Bahar Game" (1xGames)

PRIMARY: https://indian.1xbet.com/en/games/andar-bahar. Two rounds. Round 1 bets on the
joker: suit match 3.7x, value 2–7 2x, value 8 12x, value 9–A 2x. Round 2: "The distribution
always starts with Andar"; Andar 2x, Bahar 2.1x, "+20" (21 or more cards dealt) 4x. Stakes
INR 20 to INR 11,876. No provider named, no RTP, no certification statement, no demo.

Priced under the standard deal (section 4), Round 1 bets carry a 7.5% to 7.7% house edge
and the "+20" bet 13.7%, but **both main bets come out positive for the player**: Andar
+3.0%, Bahar +1.8%. Under every alternative deal tried in Phase 1 (separate-deck joker,
2 or 8 decks, infinite deck) they stay positive. A house does not ship that. The
possibilities, in order of likelihood:

1. The page's figures are wrong or stale, and the real panel shows 1.9x or similar.
2. "2x" and "2.1x" are correct but the game does not simulate a deck. Many RNG table games
   draw the winner from a programmed RTP and animate cards to match. In that case the
   card sequence is decoration and P(Andar) is whatever the developer set.
3. A rule not on the page (a push on a first-card match, a commission, a tie) removes the
   player edge.

This is the single most decision-relevant unknown in the whole lineup, and it is answered
by one screenshot of the in-game info panel.

---

## 3. Comparison matrix

| | Ezugi | Evolution Super AB | Pragmatic Play Live | Vivo | 1xBet in-house RNG |
|---|---|---|---|---|---|
| Game type | live dealer | live dealer | live dealer | live dealer | RNG |
| Physical cards | yes | yes | yes | yes | no |
| Decks | 1 (REVIEW) | 1 (REVIEW) | 1 (REVIEW) | "standard deck" (PRIMARY) | unknown, possibly none |
| Shuffle | human shuffler role (job ad); machine use unknown | unknown; shuffler roles exist | "team of shufflers" (PRIMARY, generic); sites conflict | unknown | software |
| Reshuffle cadence | every round (REVIEW) | every round (REVIEW) | every round (REVIEW) | unknown | n/a |
| First card to | conflicting: Andar (2019) vs Bahar (2025 reviews) | Andar (PRIMARY) | Andar (REVIEW) | unknown | Andar (PRIMARY) |
| Main payouts | 0.9:1 first side, 1:1 other | Andar 0.9:1, Bahar 1:1 (REVIEW) | Andar 0.9:1, Bahar 1:1 (REVIEW) | unpublished | Andar 2x, Bahar 2.1x (PRIMARY, implausible) |
| Main house edge (model) | 2.15% / 3.00% | 2.15% / 3.00% | 2.15% / 3.00% | unknown | negative as stated |
| Side bets | card count (8 buckets); OTT adds 2nd bets | card count (10 buckets) with random multipliers | card count, first-on-side, first-three poker | unknown | joker suit/value, +20 |
| Side-bet house edge (model) | 1.9% to 8.5% | 13% to 24% before multipliers; multipliers unpublished | 1.9% to 14.6% | unknown | 7.5% to 13.7% |
| Provider-published RTP | "94.85%" snippet, inconsistent | none | none | none | none |
| Lab certification found for this game | GB certification Jan 2022 (TRADE) | none specific | none specific | none specific | none |
| Licences | ONJN, MGA RN, Curaçao; UKGC via Evolution | MGA, UKGC, NJ, PA, MI and others | UKGC, Gibraltar, MGA RN, ONJN | Curaçao | 1xBet's Curaçao licence only |
| Regulator with live-studio oversight | Romania ONJN, UK | UK, NJ, PA, MI | UK, Romania | none found | none |
| Documented studio incidents | none | MI dealer card manipulation and outcome input (2024–25); NJ short deck; PA footage loss | none | none | n/a |
| Round history in UI | last 100 (TRADE) | not stated | last 27 (REVIEW) | unknown | unknown |
| Provably fair | no | no | no | no | no |
| Free observation without betting | yes | yes | yes | yes | no (no demo) |

### Ranking by independently verifiable information

1. **Evolution Super Andar Bahar.** Only table with a PRIMARY rules page stating the
   dealing order, and the only provider whose studios sit under regulators that publish
   incident orders. The incident record is a point in its favour for verifiability: it shows
   there is a regulator reading the reports. Against it: side-bet multipliers unpublished.
2. **Pragmatic Play Live.** UKGC register clean, named labs for RNG, consistent review-site
   paytable that prices cleanly. Against it: no game page, no RTP, unnamed live-casino lab,
   shuffle method unresolved.
3. **Ezugi.** Longest track record on this game, GB certification covering Andar Bahar,
   100-round history. Against it: own site unreachable, first-card rule in conflict, the
   94.85% RTP claim cannot be reconciled with the payouts.
4. **Vivo.** Curaçao only, licence numbers under NDA, payouts unpublished.
5. **1xBet in-house RNG.** Nothing verifiable: no provider, no RTP, no certificate, no demo,
   and a stated paytable that cannot be true as written.

---

## 4. Pricing of every collected table

Output of `provider_tables.py`, standard deal assumed. The main bet is identical across the
three live providers.

| bet | P(win) | pays | RTP | house edge |
|---|---|---|---|---|
| Andar (first card) | 51.5006% | 0.9:1 | 97.85% | 2.15% |
| Bahar | 48.4994% | 1:1 | 97.00% | 3.00% |

Ezugi and Pragmatic card-count side bets price between 1.90% (16–25) and 8.52% (Ezugi
26–30). Pragmatic's "first on Andar" 5.88%, "first on Bahar" 6.82%, "first three" 14.6%
(exact enumeration of 22,100 three-card sets; review sites say 8.75%, difference
unexplained and unverified). Evolution's side-bet base table prices at 13% to 24% house
edge before multipliers. The 1xGames table prices as in section 2e.

The point of this exercise: wherever a review-site paytable prices cleanly against the exact
model (Ezugi and Pragmatic card counts, Pragmatic first-on-side), the review site is almost
certainly copying the real in-game panel, and the game is dealing a real deck. Wherever the
numbers cannot be reconciled (Ezugi's 94.85%, the 1xGames main bets), the panel must be read
directly.

---

## 5. 1xBet itself: licensing and enforcement record

**Licence.** PRIMARY. Curaçao Gaming Authority certificate: Caecus N.V., company 163779,
licence OGL/2024/1262/0493, B2C, licensed since 7 Nov 2024, active, 15 domains including
1xbet.com. Source: https://cert.cga.cw/token?id=493. The earlier operating entity, 1X Corp
N.V., was declared bankrupt in Curaçao on a petition by a foundation representing players
with about $3.3m in unpaid winnings; the Dutch Supreme Court dismissed its appeal in Jan
2023. 1xBet said 1X Corp does not own it, citing a "franchise model".
Source: https://ggbmagazine.com/article/netherlands-supreme-court-upholds-1xbet-bankruptcy

**Verified enforcement.**

- Netherlands KSA, 2019: €400,000 fine on 1X Corp N.V. and Exinvest Ltd for unlicensed
  activity; the company refused to pay and compulsory collection followed.
- UK, 2019: 1xBet never held its own UKGC licence. It ran as a white label under FSB
  Technology, which took the site down after a Sunday Times exposé; FSB later paid £634,300
  for oversight failings.
- Russia: banned since 2014, criminal case for unlawful gambling (2019), founders on a
  wanted list, first conviction of a manager in 2021.
- Ukraine, 2022: licence of the 1xBet licensee cancelled after a public petition.
- India: MeitY blocked the app under section 69A (2023). Enforcement Directorate
  attachments under PMLA totalling about ₹37 crore by March 2026, with ED stating 1xBet
  "operated in India without requisite authorisation through multiple mirror websites" using
  "dynamically generated UPI IDs linked to mule accounts". Delhi High Court dismissed a writ
  against one attachment order.
- Morocco, Jan 2026: court-ordered ISP blocking.

Sources: https://igamingbusiness.com/casino-games/1xbet-hit-with-e400k-dutch-fine-over-unlicensed-activities/ ;
https://igamingbusiness.com/legal-compliance/gc-issues-new-white-label-warning-following-fsb-settlement ;
https://meduza.io/en/feature/2021/10/21/betting-on-bryansk ;
https://en.lb.ua/news/2022/09/09/16841_russian_bookmaker_1xbets_licence.html ;
https://www.taxscan.in/top-stories/ed-attaches-cr-assets-linked-to-1xbet-illegal-online-betting-platform-issues-public-advisory-1443632 ;
https://www.moroccoworldnews.com/2026/01/274865/moroccan-authorities-order-immediate-block-on-unauthorized-online-betting-platforms/

**Player complaints (UNVERIFIED individual reports).** AskGamblers rates 1xBet Casino
2.9/10 with roughly 420 of 452 complaints marked resolved, average amount about $2,650,
average duration 18 days. Recurring themes: repeated document demands, withdrawals
reversed after approval, one case demanding a medical certificate of non-addiction before
paying. No Andar Bahar-specific voided-win complaint found.
Source: https://www.askgamblers.com/online-casinos/reviews/1xbet-casino

**Consequence for this project.** Whatever the provider, the money sits with 1xBet. The
operator is unlicensed for India, under active ED proceedings in India, and has a documented
history of unpaid winnings large enough to bankrupt its former entity. For a ₹500 account the
dominant integrity risk is not the shuffle; it is deposit and withdrawal. Any ₹10,000 win
would have to clear 1xBet's verification process through payment rails the ED describes as
mule accounts.

---

## 6. Card shuffling and integrity assessment

Separated as asked: shuffle manipulation versus outcome manipulation.

**Shuffle manipulation, live tables.** All three main candidates deal one physical deck,
reshuffled per round by human staff, on camera. Nothing public states the shuffle protocol
(riffle count, machine use, cut) for Andar Bahar. The Michigan order shows the protocol
exists and is auditable in a regulated market (it cites "the required number of single
riffle shuffles"). A rigged physical shuffle that steered the first-match position across
thousands of rounds would be detectable from the round history (section 7), but no such
test has been run by anyone we found.

**Outcome manipulation, live tables.** Documented once, at Evolution, by dealers, small
scale, caught. The attack surfaces visible in the orders are: a dealer pre-arranging cards
during a short shuffle, and a presenter manually entering an outcome while blocking the
camera. The second does not apply to Andar Bahar if card recognition is automatic; the
first does. Both are collusion with a specific player, not a house-wide bias. For a stranger
betting ₹20 they are irrelevant as a threat and unusable as an edge.

**Shuffle and outcome manipulation, RNG table.** For 1xGames there is no deck to shuffle.
The outcome is a number. Without a named provider, a lab certificate, or a demo mode, no
property of this game can be verified from outside except by paying for rounds and counting
them. Its paytable as published is impossible for a fair deck, so either the page is wrong
or the win probability is programmed. Treat it as unknown until the panel is read.

**Provably fair.** Not offered by any candidate. Nothing to verify cryptographically.

**Dynamic or player-specific behaviour.** Live tables are shared streams: every player at
the table sees the same cards, so per-player outcome shaping is physically impossible there.
Per-player payout or limit changes remain possible at the operator layer. For the RNG game
nothing rules out per-player behaviour, and nothing we can do from outside tests it.

---

## 7. What still needs verification

1. Which table your account actually has (Task 4).
2. That table's in-game help panel: first-card rule, full paytable, RTP line, limits, any
   second-bet window, number of decks, reshuffle statement.
3. For 1xGames: whether Andar 2x / Bahar 2.1x is real, and the stated RTP.
4. Ezugi's 94.85% figure versus the 0.9:1 / 1:1 payouts.
5. Shuffle protocol and reshuffle cadence for whichever live table is chosen (observed, not
   read: watch whether a card repeats within what the UI calls one round; watch whether a
   new deck appears each round).
6. Evolution multiplier frequency, if the table is Super Andar Bahar and side bets are ever
   in scope. They should not be; they price at 13% to 24% before multipliers.
7. 1xBet's actual withdrawal path for an Indian account in 2026, limits, and documents
   demanded. This decides whether any win is collectable.

---

## 8. Recommended next steps for controlled observation

1. **Identify the table** from screenshots (Task 4, below). Do not bet.
2. **Read the panel**, photograph it, and feed the exact paytable into `provider_tables.py`.
   If anything prices positive, assume an unread rule and find it before believing it.
3. **Observe only.** Live tables stream whether or not you bet. Log 300 to 500 rounds by hand
   or by the capture tool from Phase 6: joker, winner, card count. That is 4 to 8 hours at
   30 to 60 seconds per round.
4. **Run the Phase 1 tests on the log**: winner frequency against 51.50 / 48.50, card-count
   distribution against the exact table, runs test for independence between rounds, and a
   check that no rank appears more than four times within a round. These detect gross
   defects only. Phase 1 showed an exploitable bias needs 1,000 to 9,500 rounds to confirm.
5. **Do not touch the RNG game for observation.** It costs money per round, shows no demo,
   and names no provider. If it is the only table on your account, that is itself the
   finding.
6. **Resolve the withdrawal question before any deposit** by reading 1xBet's current
   verification terms for Indian accounts. A win that cannot be withdrawn is a loss.

---

## 9. Task 4: what to screenshot

Open the Andar Bahar section on 1xBet and capture, with the whole browser window visible:

1. The lobby or search results showing every Andar Bahar tile, with provider logos or
   labels.
2. The table you intend to play, open, with the dealer and table visible, the game title in
   the header, and any table name or identifier.
3. The in-game help, info, or "?" panel: every page of it, especially the paytable and any
   line that says "RTP", "theoretical return", "decks", "shuffle", or "first card".
4. The bet limits panel (minimum and maximum per bet type).
5. The round-history or statistics widget, with as many past rounds as it shows.
6. For the 1xGames tile, if present: the rules page inside the game and any RTP line.
7. The casino footer links: "Fairness & RNG Testing Methods" and the licence seal, opened.

No bets. Screens only.

---

## 10. Task 4 result: the tables actually on the account (screenshots, 2026-10-30)

Domain in use: `1-x-bet-india.com`. That domain is **not** among the 15 domains on the
Curaçao licence certificate for Caecus N.V. (section 5). It is a mirror. The Enforcement
Directorate's description of 1xBet operating in India "through multiple mirror websites"
is what this is. Whatever licence protection exists attaches to the listed domains.

Three live tables were captured. All three are shared multi-player streams (other players'
winnings scroll on screen), which rules out per-player outcome shaping at the table layer.

### Table A: "1x Andar Bahar" (1xLIVE dedicated table, Ezugi)

Game-info panel captured in full. Its structure (Objective, Game Rules, Payout table, Side
Bets, Betting Instructions, Return To Player, Error Handling, Connection, Disconnection) is
word-for-word the Ezugi template seen on Ultimate Andar Bahar, and the user reports the
Ezugi name on launch. A 1xBet-branded dedicated Ezugi environment. PRIMARY for this table.

- One 52-card deck "shuffled/changed before each round by the dealer". Joker revealed, then
  betting. **Bahar receives the first card.** Studio dealer at a table, shuffling machine
  visible; earlier shots were an overhead camera of the same table.
- Andar 1:1, Bahar 0.9:1. Cards-dealt side bet 2.5 / 3.5 / 4.5 / 3.5 / 14 / 24 / 49 / 119 to 1.
- Published "optimal return to player": Andar 96.99%, Bahar 97.86%, side bets 94.86%, 97.68%,
  92.96%, 98.10%, 91.45%, 92.48%, 94.97%, 95.20%.

**This is the validation of the model.** The exact model (one deck, three matching cards,
alternate deal starting with the 0.9:1 side) reproduces every one of Ezugi's ten published
figures to within 0.13 percentage points, and the two main bets to within 0.01:

| bet | model RTP | Ezugi published | difference |
|---|---|---|---|
| Bahar 0.9:1 | 97.851% | 97.86% | +0.009 |
| Andar 1:1 | 96.999% | 96.99% | −0.009 |
| cards 1–5 | 94.874% | 94.86% | −0.014 |
| cards 6–10 | 97.671% | 97.68% | +0.009 |
| cards 11–15 | 92.965% | 92.96% | −0.005 |
| cards 16–25 | 98.103% | 98.10% | −0.003 |
| cards 26–30 | 91.477% | 91.45% | −0.027 |
| cards 31–35 | 92.437% | 92.48% | +0.043 |
| cards 36–40 | 94.838% | 94.97% | +0.132 |
| cards 41–49 | 95.078% | 95.20% | +0.122 |

The provider's own certified numbers and an independent first-principles calculation agree.
That answers Task 5's question for Ezugi tables: the published rules, the published payouts
and the mathematics are mutually consistent. What it does not prove is that the physical
deal matches the rules; that is what observation (section 8) is for.

- Result road shows about 90 rounds. Sample shares were 42/58 and 45/55 Andar/Bahar across
  two captures. Expected Bahar share 51.5%. Within noise.

### Table B: "Ultimate Andar Bahar" (Ezugi, confirmed)

Lobby tile carries the Ezugi logo. Game-info panel captured in full. PRIMARY for this table.

- One 52-card deck "shuffled/changed before each round by the dealer". Joker revealed, then
  betting. **Bahar receives the first card.**
- **A 20% fee is added to the player's total bet.** A ₹100 bet costs ₹120.
- Andar 1:1, Bahar 0.9:1. Side bets 1–5 2:1, 6–10 3:1, 11–15 4:1, 16–25 3:1, 26–30 12:1,
  31–35 20:1, 36–40 40:1, 41–49 100:1.
- After bets close, one to three multiplier cards are drawn from a **virtual** 52-card pack
  (joker excluded) and given 2x, 3x or 5x. A winning main bet whose pile contains a multiplier
  card is multiplied. Side bets are "randomly awarded one multiplier".
- Published "optimal return to player": Andar 97.44%, Bahar 97.82%, side bets 95.05% to 95.68%.

Priced (`observed_1xbet_tables.py`): without multipliers the fee drives the main bet to
81.5% return. Ezugi's published 97.82% therefore requires an average multiplier of about
1.42x on a winning Bahar bet. That is consistent with the stated mechanics but cannot be
derived independently, because the multiplier draw probabilities are not published. The
multiplier draw is software (a virtual pack), so one component of this live table's return
is an RNG whose certification was not found in Phase 2.

Consequence: Ezugi's own figure puts the house edge at 2.18% (Bahar) and 2.56% (Andar),
almost the same as the plain table, but with 16 points of the return carried by rare
multiplier hits. Lumpy. A ₹500 bankroll paying 1.2 per unit wagered loses ordinary rounds
faster and waits for multipliers to catch up.

### Table C: "Andar Bahar" by ElCasino (1xBet "TV Games" section)

Identified by the ElCasino watermark on its rules panel and the ElCasino tile with the same
dealer and set under TV Games in the lobby. Not Pragmatic Play. ElCasino has no findable
public footprint: no provider site, no press, no lab certificate, no licence listing turned
up in a search. Treat its certification status as unknown.

Fully documented from its own rules panel (sections 1 to 9 captured). PRIMARY for this table.

- One standard 52-card deck. Each card has a barcode read by a scanner in the table; the
  software, not the dealer, determines value and suit (rule 6.1). A certified shuffling
  machine shuffles; each game begins with the shuffled deck taken from the machine (3.1), and
  after the result the cards go back into the machine (3.4). Decks are replaced several times
  a day (6.2). Burn-card and cancellation rules exist (4.1 to 4.4).
- **Andar receives the first card** (2.2, 3.3). Andar 0.9:1, Bahar 1:1. So on this table
  **Andar is the better bet.** Opposite of Tables A and B. A player who assumes "Andar is
  always the first side" will take the 3.00% side on two of the three tables.
- Two betting rounds per game (1.6); the joker is revealed before betting begins (3.2), so
  a bet can be placed knowing the joker.
- Limits: main bets 20 to 500,000 INR; 1st Andar / 1st Bahar 20 to 100,000; First 3 20 to
  50,000; cards-dealt 20 to 100,000 down to 20 to 2,500 for 46–49.
- Side bets: 1st Andar 15:1, 1st Bahar 15.5:1, First 3 (flush 5:1, straight 8:1, straight
  flush 120:1, ace high or low, bet loses if only two cards are dealt), cards dealt 1–5 2:1,
  6–10 3:1, 11–15 4:1, 16–20 5:1, 21–25 8:1, 26–30 12:1, 31–35 20:1, 36–40 40:1,
  41–45 110:1, 46–49 800:1.
- Provider: ElCasino, as above. The rules text is 1xBet's template ("the betting company").

### Pricing of Table C from its own panel (`observed_1xbet_tables.py`)

| bet | house edge |
|---|---|
| Andar 0.9:1 | 2.15% |
| Bahar 1:1 | 3.00% |
| 1st Andar 15:1 | 5.88% |
| 1st Bahar 15.5:1 | 6.82% |
| First 3, bet before the joker | 14.64% |
| First 3, bet after seeing a joker of 3 through Q | 10.12% |
| First 3, bet after seeing a joker of A, 2 or K | 29.73% |
| cards dealt, every bucket | 13.2% to 23.8% |

The only in-game information advantage on any of the three tables is the second betting
round on Table C, where the joker's rank changes the First 3 odds. It moves the bet from a
14.6% house edge to a 10.1% house edge at best. No joker makes it positive. The side bets on
this table are the worst bets on the account.

### What the three tables share

- Main bet: 2.15% house edge on the first-card side at 0.9:1, 3.00% on the other side at 1:1.
  Exactly the Phase 1 model. Nothing provider-specific changes it.
- Physical single deck, machine-shuffled every round, outcome read by barcode on Table C
  (Tables A and B presumably the same; their rules pages will say).
- Free observation: all three stream whether or not you bet.

### The full live lineup on the account

Live Casino search for "Andar Bahar" shows, in order: ElCasino "Andar Bahar" (also listed
under TV Games), 1xLIVE "1X Andar Bahar" (Ezugi dedicated), Ezugi "Ultimate Andar Bahar",
Ezugi "Andar Bahar", SA Gaming "M Andar Bahar", Evolution "Super Andar Bahar" (501 players
seated at capture), Ezugi "OTT Andar Bahar", Playtech "Andar Bahar", and at least one more
tile cut off. Slots show two RNG Andar Bahar titles (a "G" logo and a hat logo). The 1xGames
in-house title did not appear in the search.

So the Phase 2 research set (Ezugi, Evolution, Pragmatic, Vivo) was right on two of four:
Ezugi in four variants and Evolution Super Andar Bahar are on the account. Pragmatic Play
and Vivo tables did not appear in the search. Playtech, SA Gaming and ElCasino did, and were
not researched in depth. Of those three, Playtech is a listed, UKGC-licensed supplier with a
long audit record; SA Gaming is an Asia-facing supplier with GLI certification claims;
ElCasino has no public footprint at all.

### Still needed

1. The withdrawal and verification terms for this account.
2. The footer "Fairness & RNG Testing Methods" page.
3. If Playtech or SA Gaming is ever preferred over Ezugi or Evolution: their game-info
   panels. Not needed otherwise.

### Table choice, for when the time comes

Every table prices the main bet at the same 2.15% to 2.18% on the first-card side. The
choice is about trust, not edge, and the Phase 2 ranking stands: Evolution Super Andar Bahar
(Andar first) and the Ezugi standard tables (Bahar first) are the two whose provider,
licences and published mathematics all check. Ultimate adds a software multiplier draw and
a 20% fee for the same edge with far more variance. ElCasino is unverifiable. Side bets on
every table are worse than the main bet, by 2 to 24 points.

Correction 2026-10-31: on 1x Andar Bahar (Ezugi) two cards-dealt bets beat the main bet. "16-25" at 3.5:1 returns 98.10% (Ezugi's published figure, model 98.103%) against Bahar's 97.85%, and "6-10" returns 97.67%. The earlier statement that every side bet is worse holds for ElCasino (Table C), not for this table. All bets still have negative EV.

### Withdrawal page, first look (2026-10-30)

INR withdrawal, "Recommended" tab: three methods. "Bank Transfer new" and "iCash.One" show a
padlock, meaning not available to this account as it stands. The only open method is a
generic "Withdrawal" with a 72-hour badge. No minimum amount, fee, or document list visible
yet. Two of three recommended routes locked on a fresh account is the pattern behind the
AskGamblers complaints in section 5: a win exists on screen, the route to a bank is gated.

### Table limits and page structure (2026-10-31)

Read from the game's own footer through Claude in Chrome, without interacting with the game:

- "1x Andar Bahar" is game 63587 on the account. Footer: `1x Andar Bahar ₹ 100 - ₹ 200,000`.
  Paytable on screen matches Table A above: Andar 1:1, Bahar 0.9:1, cards-dealt 2.5 / 3.5 / 4.5 /
  3.5 / 14 / 24 / 49 / 119 to 1.
- "Ultimate Andar Bahar" is game 67426. Footer: `Ultimate Andar Bahar ₹ 100 - ₹ 200,000`. Side bets
  on screen 2 / 3 / 4 / 3 / 12 / 20 / 40 / 100 to 1, as in Table B.
- Both games load in a cross-origin iframe from `play.livetables.io`. The outer 1xBet page cannot
  read the game's state; observation has to attach to that frame (Phase 6, `capture.py`).
- The road summary on game 67426 read 36% Andar / 64% Bahar at the moment of capture, and on game
  63587 57% / 43%. These are the game's on-screen summaries of a single road of about 90 rounds,
  not logged data, and no test is pre-registered on fewer than 300 logged rounds. They are recorded,
  not interpreted.
