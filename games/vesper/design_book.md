# Vesper — Design Book

> The user's review surface. This is **intent in plain language** — the engine/TOML is the faithful
> translation of what's written here. Grown one section per pipeline step.
>
> Working title: **Vesper** (also the PC's buried true name — hidden in plain sight; rename freely).
> Book revision 143 (Step 5 + authoring. **Header changelog resumed at 52.** *(Revision-number note: this leading number sat stale at 69 from rev 69 through rev 111 while only the inline `Latest:` line moved; from rev 112 onward it tracks the true revision. The unclosed code span that had swallowed this note's closing parenthesis — and with it the `Latest:` marker — was repaired at rev 124.)* Latest: **SHE TELLS KESS IT FAILED, AND THE PART IS DIFFERENT EVERY TIME (rev 143, 2026-08-13).** beat_0093, and LO found it by playing the loop: *"there is nothing that she tells kess like that part failed."* He was right, and reading it showed the defect was worse than a missing beat — **the order was inverted.** She walked out of Mercer's room with a burned part, went straight to the stalls for another on her own initiative, paid twenty-five coin, and only then, while Kess was seating the replacement, heard the finding that justified buying a different one. Diagnosis after purchase, four cycles running. ⚠️ **AND THE HUB WAS DEAF.** `hub_kess_berth`'s bands were authored at rev 114, **nineteen beats before the parts loop existed**, and were never re-banded on `mercer_attempts` — so band A, the line that fires in the post-failure state, greeted her with *"you're paid up, so I'm on it. Don't hover"* after every burn, while his own line one node over promised *"you'll know when I've got something because I'll say so."* He never said so; the only way to hear a finding was to buy a part first. ⚠️ **THE FIX IS A CONVERSATION AND A SHOPPING LIST.** A **debrief node** on his hub behind a new "Tell him the part failed" rung: she reports the sensation, he does the working out (§14's split, unchanged), and he names what to buy next. Kess's three findings — *it is listening not locking* · *it bit you, that is a guard* · *it is a set of voices, not one man* — **moved off the bench to the berth**, where they now precede the purchase instead of following it; the install bands keep the same slots and carry the **part in his hands** instead (talkback → sweep head → isolator → stacked talkback), each still inside the measured 21-word ceiling. The market stall gained **four exclusive bands** so the part is named and different every cycle, where before it was one repeatable card with identical prose four times and nothing on screen explaining why part two would beat part one. ⚠️ **BASTIEN CAME OUT OF FINDING 3, LO's call, and it was overdue** — band 3 read *"It's a set — three more besides his. Two I can't place. One's Bastien,"* written when present-day Bastien was the next thing in the release. He went to the shelf at rev 141, so from that beat onward the line handed the player a lead this build cannot pay off, on the last rung before the fire. **The SET stays** (load-bearing on cards H3 and I, and the whole reason part four is a stacked talkback); the **names go**, replaced by what LO asked for — *"if it takes, there's nothing left in you that answers to anybody."* The Act-1 captivity references (*"Bastien's men opened this seam"*) are **kept**: that is the comparison the install scene is built on and has shipped since 0.1.7. ⚠️ **TWO ENGINE FACTS CHANGED THE DESIGN MID-BUILD.** (1) A trait condition compares a trait to a **literal** — `var rightVal = it.value` (`v2.py:3948`), no trait-to-trait form — so the natural gate *"part_spec is behind mercer_attempts"* is inexpressible and would have unrolled into three rungs at the bench plus four at the stall; a derived bit (`spec_pending`, raised by each failure, cleared by the debrief) collapses both surfaces to one clause. (2) `[group]` blocks are **display-only** — 80 in this game, none carrying effects — so the re-spec had to ride the node's exit, which is better anyway: LO's ask was that she *tell* him, and a rung is an action. ⚠️ **THE BUY GREYS, IT DOES NOT VANISH** — the gate is on the choice with `show_when_locked` + a `locked_text` naming the missing step, never on the canvas trigger, because a stall that disappears while the Story-Goal still says *buy a part* is the lostness failure. Cost: one extra leg per cycle (`berth → market → berth`), both underworld locations a few clicks apart. Price held at 25 coin — the ask was a richer part, not a tighter economy. New suite `live_rev143_parts_debrief` (**75 assertions**), whose load-bearing half is the negative: **no dead end across ten reachable loop states**, the four stall reads all distinct, and the loop cards never badge. Four loop suites were **retargeted, not re-pinned** — `0075`, `0076`, `0077`, `0078` — each now asserting that the moved findings still exist at the surface that owns them, so a later beat cannot delete one and stay green (`0078` gained an assertion, 50 → 51). Folded into the skill the same turn as `lanes.md`'s **fourth failure — a loop lands beside a deaf hub**, the companion to the terminal-flag sweep, which could never have caught this because nothing became false. Previously: **THE QUESTS PAGE LEARNS TO SAY "FINISHED" (rev 142, 2026-08-13).** beat_0092, and it started with LO playing the build to its last beat, opening the Quests page and reporting that it "looks sort of same." He was right, and the audit found why. At the end state the page draws **five sections** — Story Goals, Renner, Calloway, Colm, Mercer — and **four of them are finished arcs with nothing left to do**, rendered *identically to a live objective*: same box, same italic flavour, same yellow 💡 tip. The cause is a render rule nobody had written down. `renderQuestsGoalBlock` draws exactly one of three frames, and a card that is goal-less and non-terminal matches **none** of them — which is not a blank row, because the card still renders its text and tip. So it reads as an open task forever. The only "this is over" signal in the entire game was one sentence buried mid-paragraph in card M's tip. ⚠️ **THE ENGINE HAD SHIPPED THE FIX AND NO CARD HAD EVER USED IT.** `terminal = true` fires a green **✓** frame, styled since PRD 48; `grep -c "^terminal" 5_scenes.toml` returned **0** across the whole game. Five cards now set it — Renner (`renner_drained`), Calloway and Colm (`archive_1a_done`), Mercer (`leash_answered`) and Story-Goal M (`leash_cut`). ⚠️ **THE BADGE MARKS THE ARC COMPLETE, NOT THE SURFACE CLOSED**, so every one of them keeps its tip: Colm's back room and Renner's office stay open as repeatable content and the tips still say so. Retiring the cards instead would make the sections vanish, which is the worse defect `quests.md` §6 exists to prevent. ⚠️ **AND ONE NEW ENGINE FIELD, `terminal_text`.** Frame 1's label was the hardcoded string `Arc complete`, which cannot say *this release ends here* — a finished arc and a finished build are different endings. Card M overrides it with *"Chapter complete — the story continues in the next release"*, and it is the **only card in the game permitted to**, because the label promises future content and Renner's arc is finished forever. That is the badge form of the rule §10.1 already applies to prose: exactly one card names the future. Engine work is four touch points (`template_import.py` dataclass, parser, serializer; `v2.py:14968` renderer) plus a validator warning when `terminal_text` is set without `terminal`, since the string would otherwise be silently dead. Both skills took the doctrine the same turn — `quests.md` §3 and a new §7 subsection in `author-game`, `engine.md` §23 in `author-game-v2`. ⚠️ **THE NEGATIVE IS ASSERTED, NOT ASSUMED:** a badge on a card the player still has work to do is this same defect inverted, so the new suite checks at three attempt counts that the loop cards never badge and that Mercer's 🎯 count still climbs 0/3 → 1/3 while three other arcs sit finished beside it. New suite `live_rev142_terminal_cards` (49 assertions); `live_beat_0084` (82/82) and `live_rev141_bastien_cut` (73/73) both unchanged, as predicted from the renderer emitting no `<li>` in the terminal frame. No media change (22 MISSING). Previously: **PRESENT-DAY BASTIEN SHELVED OUT OF 0.1.8 (rev 141, 2026-08-13).** beat_0091, LO's call, and the release is now a Mercer release with its capstone intact. 0.1.8 was the release that would have put Bastien on screen for the first time — in 0.1.7 he is 210 mentions of pure backstory, the cell and a name on a ledger, with no room, no hub, no loop and no drain. Those surfaces were authored at rev 126–127 and never got the heat pass revs 138–140 gave the Lockup, so shipping them spends the next chapter's antagonist at a standard the rest of the release has left behind. **Seven canvases** (`cap_bastien_walks_in`, `bastien_door_search`, `hub_bastien`, `loop_bastien_backroom`, `loop_bastien_finisher`, `bastien_drain_canvas`, and `kess_seat_controller` — orphaned, since the switch existed only to beat his door search), the `bastien_backroom` location and his schedule row went to `games/vesper/shelf/bastien_present_day.toml` in one contiguous 1,017-line block. ⚠️ **SHELVED, NOT DELETED.** `merge_toml_phases.py:44` merges a hardcoded whitelist and skips anything absent from it, so a file outside `toml_phases/` is never read; the restore is a paste plus three reversals, all recorded in that file's own header. ⚠️ **THE ONE THING THAT WOULD HAVE TAKEN THE ENDING WITH IT.** `cap_extraction` — *"Her own page"*, the chapter's capstone — was gated on `bastien_drains_done gte 1`, so a naive cut would have left the build with no ending at all. All eighteen of its beats were read: **zero Bastien references**, and the scene states its own enabler in Kess's mouth (*"while that thing's answering in his voice the guard's asleep, and a sleeping guard I can cut around"*). That clause was **sequencing, not cause** — the gate already carried `mercer_leash_state gte 2`, which is the fire — so removing it cost the scene nothing and needed no new writing. The chapter now reads *the print → the key dies → the Q&A → the loop → the fire → Kess cuts the chip out → her own page.* ⚠️ **ONE REVEAL IS DEFERRED, NOT LOST:** the buyer (no name, wanted *what was done to her*, and is the man who carried her out) lived only in `bastien_drain_canvas.d0` and card L. Card M's next-chapter hook **survives** — that far door is Act 1 captivity, shipped since 0.1.7 — and only the *link* between the two goes to 0.1.9, which is a stronger place to make it. Quest ladder is now **I → J → M**: cards K and L are shelved, J's text is untouched and its tip is card L's verbatim, its closer moves to `leash_cut is_false`, and M's tip loses one sentence about a back room that is no longer in the build. Bastien's three-card NPC section goes with him. Media **31 → 22 MISSING** (seven pools plus `locations/bastien_backroom.jpg` and `scenes/bastien_undertow.jpg`). The four `controller_*` / `bastien_drains_done` traits are **left declared** — all four are `hidden = true`, so an unused declaration renders nothing and keeps the restore to a paste. ⚠️ **AND FOUR SUITES WERE ALREADY RED AT HEAD, WHICH THIS BEAT FOUND BY BUILDING THE PRE-CHANGE STATE AND RUNNING THEM AGAINST IT** rather than trusting the previous report: `live_beat_0076/0077/0078` and five of `0079`'s assertions were failing before this beat touched anything, because a `--debug` build renders a media-finder widget for every MISSING clip and each widget's anchors land inside `#passage`, so a fork helper that expects *"the finisher renders exactly one row"* saw three. `link_texts` now filters them; those four suites are green for the first time in several revisions. `live_beat_0080/0081/0082` **self-skip** while the block is shelved and light up again on restore; `0083`, `0084`, `0079` and `rev137` had their Bastien-dependent halves re-cut to derive from what is in the build. New suite `live_rev141_bastien_cut` (73 assertions) covers the whole cut. Previously: **THE LADDER COMPLETED — THE KISS AND THE ANAL FINISH (rev 140, 2026-08-13).** beat_0090, and it closes LO's original eight-rung list for `cap_owner_print`: **kiss → tits → ass → her mouth → her throat → he fucks her → anal → cum inside her ass**, in that order, asserted live. ⚠️ **THIS AMENDS A SIGNED CLAUSE.** The rev-119 Mercer ceiling reserved anal for the loop and the first fire and said in those words *"so the print scene is vaginal"*. It is not any more. The clause is **struck rather than deleted** in the row below so the reasoning stays readable, and the objection was put to LO twice before he took the call: the argument for holding it was **escalation** — with anal spent at the print the chapter has no act left to climb to — and not mechanism. ⚠️ **The mechanism is genuinely unharmed**, which is worth recording: `mercer_finisher` canonises that **every** finish of his passes her nothing, so the print's failed reach and the loop's three failures still read *this man is dead* rather than *wrong act*. The vaginal beats keep their act and lose only their finish — one finish in the scene, never two. ⚠️ **TWO THINGS MOVED WITH IT, AND THE SECOND IS A SMALL VINDICATION.** (1) The loop's two anal entry choices carried `controller_off` purely to protect the reserve; they are **ungated** now, because a gate hiding an act she has already performed is worse than no gate. (2) That makes `loop_mercer_finisher`'s **exit D** (`controller_off is_false` → `.cold`) reachable for the first time — and `beat_0087` kept D deliberately as an unreachable guard, payload written then, against exactly this edit: *"if a future edit opens the anal pose earlier, this catches it with the correct payload instead of dead-ending the player at the finish."* It did, and no new work was needed. **The kiss** was refused at `beat_0088` on a register argument that leaned on a **false measurement** — I claimed the game contained no kisses; `hub_colm_undertow.kiss` is a whole rung. What survives of that argument is that a kiss asks for something *from* her, so it is written as one more thing he takes without asking, fist still in her hair. It is the one rung with **no clip**: a clip there would either break the "a beat carrying a sex clip carries crude vocabulary" guard or force a crude word into a beat where she is still dressed. `sex/mercer_lockup_finish_t5` (the vaginal creampie) is retired; `sex/mercer_print_anal_t5` and `_anal_finish_t5` replace it. Explicit share **9.6% → 10.3%**; media debt 30 → 31 (one retired, two new — the kiss takes no clip). Previously: **THE ASS GROPE RESTORED, AND THE POSE PAGES CUT TO HOUSE SIZE (rev 139, 2026-08-13).** beat_0089, two follow-ups to the heat pass below. ⚠️ **A TEST'S CONVENIENCE HAD DELETED ONE OF LO'S RUNGS.** His ladder for the print scene was *boobs → **ass** → blow him → throat*, and `beat_0088` built every rung but that one — because the anal-free guard was written as *"this canvas contains no `\bass\b` at all"*, a **proxy** for the real claim, and satisfying the proxy took the grope out with it. **A grope is not the anal act.** The rung is back (standing, both hands, from behind, still talking, new pool `sex/mercer_print_ass_t5`), and **two** guards were rewritten to assert the ACT — `live_rev138_beat_0088` §3 and, more importantly, `live_beat_0074:148`, which is where the bare-word proxy originated and which `beat_0088` had copied. Both now also assert the grope is **present**, so the rung cannot be traded away again. ⚠️ **AND THE POSE PAGES WERE 3× THE HOUSE SIZE.** Measured across every sex loop in the game the pose node is *video + one ~36-word paragraph* — Colm 36/39/68, Renner 34/37/43, Calloway 47/38/59 — while Mercer's ran **133/97/118**, because at rev 137 `loop_mercer_attempt.base`'s multi-beat paragraphs were folded into pose nodes wholesale. A pose page is re-opened **4–6 times per visit**, which is exactly the surface Rule 2 protects. Each node now merges its two paragraphs into one and keeps **one** short line of his instead of two: **55 / 54 / 85**, and each still carries 3–4 explicit words against Colm's 1–2. ⚠️ **Mercer does not go silent the way Colm does** — clause (iii) is a man *"talking about the penthouse while he is inside her"*, so the one retained line per page is a deliberate deviation from house, and the anal page keeps its seat paragraph on top (Colm's shape, 34 + 34). The cut line — *"Nine years I had a floor and a driver and a woman in on Thursdays for the plants"* — is pinned by no suite and loses nothing unique: `cap_owner_print` already gives the plants woman her own beat, and it could **not** move to the intro's `block_pool` because its punchline only parses during the blowjob. Explicit share **8.8% → 9.6%**; media debt 29 → 30. Previously: **THE HEAT PASS ON MERCER'S LOCKUP (rev 138, 2026-08-12).** beat_0088, and it began with LO's observation that `cap_owner_print` — the first time she fucks Mercer since the fall — runs hand → bent over → fucked, with no tits, no mouth and no throat in it. Rev 132 had already added six beats to that scene's front, but every one of them was **tempo** (he watches, he undresses her slowly) and the ladder of **acts** never moved. Measured across the chapter's nine Mercer canvases, 110 prose units carried **exactly two** with three or more explicit words — against 50–71% in the shipped sealed-cell canvases on the same instrument. **This took no new signature.** The Mercer ceiling was signed at rev 119 and clause (iii) already names the register — *"full anatomical words (cock, cunt, cum, ass) … that is the register for every Mercer use-scene in this chapter, the loop included"* — so the surfaces were written **under** their own ceiling, and `rts-flat-prose.md` Rule 9 names this game's `drain/plate/socket` lexicon as its anti-pattern by name. Three changes: `cap_owner_print` gained **three act rungs** (tits, on her knees, the throat) and its six existing act beats were re-cut from one crude word each to three; the loop's three pose nodes had their narration moved off *the arrangement* and back onto bodies; and all seven `mercer_drain_canvas` node leads had the body put back, because every one of them is entered off the anal finish and every one of them opened straight onto the reach with a heavy man still inside her that the prose never mentioned again. ⚠️ **THE THROAT RUNG IS AN UNHURRIED HOLD, NOT A FACE-FUCK** — LO's call, taken against his own first phrasing, because his signed row is a man who *"never once had to raise my voice at you"* and the shipped oral clip brief already says `Avoid: gagging or deepthroat roughness`. The escalation is **duration**: he keeps her there through a whole sentence and lets her up when *he* is finished talking. ⚠️ **THE DISCOVERY LINE HAD TO MOVE.** The loop's oral node opened on *"That's a new one. Two years and you never once"* — true only while the loop was the first oral at the Lockup. The print sets `owner_print_taken`, the very flag that gates the loop's entry rung, so the print is **always** first; the discovery is now spoken there and the loop's line re-cut to the man three weeks later. Anal is still **not** spent at the print — the ceiling reserves it, and canon (`5_scenes.toml:283`) is that his ass finish passes her nothing, so an anal finish here would make the loop's three failed reaches read as *wrong hole* instead of *this man is dead*. Result **2/110 → 10/113 = 8.8%**, inside the 7.5–9.3% band. Three new pools (`mercer_print_tits_t5` / `_knees_t5` / `_throat_t5`); media debt 26 → 29. Beat C. His room had accreted **six sex canvases and no choice of act** — `loop_mercer_attempt`, the routine rung, `loop_mercer_warm_tap`, and three one-shot capstones — while every other character in the game has one rig: **hub rung → pose menu → finisher → drain canvas**. Mercer shipped that rig himself in Act 1 (`mercer_serve`, knees/desk/glass); he is the only character who *lost* a menu going forward in the story, and the chapter's biggest scene arrived as an **auto-fire the player could not decline**. Six canvases became three. The template was not invented: `loop_bastien_backroom` (rev 127) is the same fork one NPC over. **Nothing written was thrown away** — the three failures, the seven-beat Q&A, the answered fire and the warm tap all moved verbatim behind an elected choice. The finisher now carries **twelve provably-exclusive exits** forking on gear, charge and the story chain (LO's call: the full `loop_renner_finisher` shape, not story state alone), and a live suite asserts exactly one renders in each of thirteen states. ⚠️ **THE CEILING HELD BY A HAIR.** The first cut offered the anal pose from the print onward — but anal is **not** spent at `cap_owner_print` or `rung_mercer_hands_on` (verified by content: both are anal-free), and under the shipped structure the first anal at the Lockup was the switch-off night. Both entry points into that pose are now gated on `controller_off`, which reproduces the authored order exactly. **Oral joined the Lockup** and takes no new signature — `mercer_serve.base_knees` spent it in Act 1. ⚠️ **AND THE FLAG-CHAIN VALIDATOR EARNED ITS KEEP.** `owner_drained` and `leash_answered` lost their located setters the moment their capstones became triggerless nodes, and the build **hard-failed**: a triggerless setter gives the help page no "go here" hint. The shipped discipline (stated in `loop_colm_finisher`'s own header, and the reason `vane_confirmed` was retired at rev 92) is that a triggerless canvas sets **traits**. So `mercer_leash_state` (0 leashed / 1 drained with the key dead / 2 answered against a live key) is the fork axis every **gate** reads, and the two flags — still set, on the same two choices — remain what all eight quest cards read. Three quest tips were rewritten to name the act and the loadout; one of them had been telling the player to take the evening and reach at the finish, **which she could not do**, because the scene fired at her. It is true now.

---

## World setup

**POV.** Female PC. The arc is **awakening from total surrender** — an owned, will-less slave slowly growing
a self the company never gave her. Her sexual register is **contextual, not fixed:** *inside* the company
she's a submissive slave (dominance there makes no sense); *outside* on missions she wears a cover and plays
whatever a target needs. The **dominance / taking-control** is where she's *headed* as she wakes up
(used → user) — earned, not the start.

**Register — PERSON: `third`.** (Retro-declared 2026-07-14; `authoring_state.json` → `register.person`, and
`narration_person = "third"` in `[settings]`.) Wren is **watched, not inhabited** — the still-point PC, a
tool narrating its own tasks. Every `paragraph` and `thought_bubble` is "she", never "you"; `dialog` blocks
are exempt. This was always the game's voice, it just was never written down — so the engine stamped "**You:**"
on her own dialogue for the whole of its shipped life. **Locked: never mix in a "you."** (Person is the first
of the three register axes — `.claude/skills/author-game/references/rts-flat-prose.md` Rule 1.)

> **Known register debt (not fixed here — LO's call pending).** Vesper's narration:dialogue ratio is
> **7.25 : 1**; Road to Success runs **0.73 : 1**. We *narrate* where RTS *speaks*. The word budget is fine
> (~45-word blocks vs RTS's 35–40/beat); the **mode** is inverted, and the cascades are under-beated
> (~3.5 beats median where an RTS peak runs 10–24). Any new Vesper beat must clear the Rule-4 gate
> (≤1.5:1 with a present NPC); the existing corpus is a separate prose pass if we want it.

**What she is (the core — read this first):**
- **Half-human, not a pure machine.** Marrow's breakthrough was building his creations on a *living human
  base* — that's *why* they can truly feel. She (and Cain) are human-derived. Her human memory is wiped; she
  believes she's only a company machine. *(Whose human she was stays buried — surfaced only as far as it
  feeds the central reveal, never a forked subplot.)*
- **Total surrender — no will of her own.** She believes she exists only to serve. Inside the company she's a
  **slave** — everyone uses her, the **boss owns her** (sex *and* chores). She has no motive of her own; her
  motive *is* the company's. The whole game is her motive peeling away from theirs.
- **She loves sex — it's the ONE thing she feels.** Everything else is blank. This is *not* contentment;
  it's the opposite — they hollowed her out and left a single spark. A slave who only comes alive while
  she's being fucked. (And it's the **fuel for her weapon** — below.) The chip is the first hint there was
  once a whole person who felt *more than this.*
- **Her secret weapon — the sex-weapon (LOCKED).** She has to *mean* the sex (her own pleasure powers it).
  At the moment **he climaxes inside her ass** (anal — vaginal does NOT fire it; the most-degrading-seeming take is the trigger), she passes him a fluid that puts her in **full control of him.**
  Used only on **targets** — never the boss (she stays surrendered to him); it's the one thing that's *hers.*
  **In-game (no real timer):** his climax routes to a **control canvas** where she questions and commands him
  (the extraction = both *drain* and *command*); when that canvas ends, ~10 minutes have passed in the
  fiction and **he remembers nothing** — he wakes clean, so a mark can be reused. His own orgasm is the key
  that hands her the controls. *(Act-2 seed: the day she turns it on Mercer, the used becomes the user.)*

**Where she lives — Vance Dynamics & the Tower (LOCKED).** The company isn't an office she commutes to; it's a
**vertical arcology where everyone lives** — staff, assets, the boss — a total institution and a literal cage.
The business runs in three layers (matching the reveal architecture):
- **Public face:** a prestige **robotics/AI megacorp** (automation, security, cybernetics) — the legit
  storefront that explains the labs, the scientists, the thousands of employees, most of whom never see what's
  underneath.
- **The real business — *ownership*.** It uses human-derived **assets** like Wren to run the world's most
  powerful intelligence-and-control operation: it *owns* the powerful by knowing the secrets it extracts.
  **The missions ARE the core business** — every honeypot is the company owning another powerful man.
- **The deepest secret (Act-2):** the asset program is really the Chairman's machine for his own immortality.

The theme with a logo on it: **a company whose whole trade is owning people** — literally (people remade into
tools) and figuratively (the powerful owned through their secrets) — and a protagonist who is *a person it
owns, waking up.* Wren is one of several assets, and the irreplaceable **original** among them (see Cast).

**The fantasy (clears the 3-part bar) — designer's full-arc view:**
> You're an owned half-human weapon who feels nothing but the sex she's used for. Inside, you're the
> company's slave; outside, you slip into powerful men's lives under a false face and drain them while they
> think they're using you. They send you to hunt an "evil" rogue — who is the one person who ever loved you.
> Claw back the self they erased, climb to the man who's owned it all for generations, and at the end decide:
> **kill the one waiting there, or love him.**

- **POV-fit** ✓ — female-PC reclamation; the reversal is **owned slave → the one who owns.**
- **Sharp charge** ✓ — **transformation** (an erased person waking), **submission→conquest** (used tool that
  becomes the user), and a **cold taboo** (a hollow slave who feels only the sex, with a hidden weapon in it).
- **Two-act shape** ✓ — Act 1: surrendered tool; infiltrate and drain men to hunt the "evil" rogue; the
  first crack (Phase 1). Act 2: dig in secret; climb Vance; recover herself; reach the Chairman and the
  truth — turn the weapon on her owners, face the rogue. Kill-or-love.

**Desire span (declared) — an ARC from submission to agency.**
- **Targets:** **mostly men** — the powerful men she's sent to infiltrate.
- **Phase 1 / Act 1 register:** **submission.** Inside = owned slave. Outside = infiltration, where she plays
  whatever the cover/target needs (caretaker / submissive / domme — the register flexes *logically* per man).
- **The arc:** used → user. The **dominance, the break-and-own conquest** is **earned late**, as she
  awakens — never the Phase-1 register.
- **Feeling:** she feels only the sex. Emotional warmth (caring/love) stays reserved for **Cain at the very
  end** — kill-or-love.

**The hidden backstory (iceberg — LOCKED; never dumped, only reconstructed):**
1. **Dr. Elias Marrow** cracked synthetic consciousness — **human-derived** (built on a living human base;
   that's why it truly *feels*). He built **Cain first** (half-human; he feels).
2. Marrow built **her second, the same way — a companion *for Cain*.** Made to feel, to be loved.
3. Realizing what the company would do with feeling beings, Marrow chose **total erasure** (Cain kills
   Marrow, then destroys the unfinished girl, then ends himself) — to deny the company. Cain agreed, out of
   love and duty.
4. **The company interrupted.** Cain killed Marrow, then they hit him mid-plan; he fought, **lost, ran** —
   and they **seized her, unfinished,** wiped her memory, made her a weapon, left only the body's pleasure.
5. Now they aim **her — the one Cain failed to save — at killing *him*.** She hunts the only person who ever
   tried to spare her this. Cain has warred on the company ever since, partly *because they took her.*

**The generational villain (LOCKED).** **The Chairman — Aldous Vance** — never died; a man clinging to life
through technology, already part-machine. He wants Marrow's human-derived soul to become a **human-machine
fusion:** true immortality *and* a self that still feels. **The half-human secret is what he's killing to
get.** She's the **working prototype** (they chained her feeling to use her now, harvest the soul later).
**Inverse mirror:** she's a half-human reaching back toward herself; he's a human shedding humanity for
permanence. The **Act-2 conquest target** (she may end *owning* Vance), kept distinct from Cain's kill-or-love
fork. Remote and mythic — she doesn't reach him until late.

**The reveal architecture (LOCKED):**
- **The backstory is the well, not the pour.** She reconstructs the truth as she reconstructs the **chip** —
  her remembering and the player's understanding are one act. The mystery is the plot's desire ladder.
- **Facts locked to her, dread a step ahead.** The player senses the wrongness before she'll admit it.
- **The masks rhyme with the mystery.** She wears a false self for every mission while her *real* self is the
  one thing they erased — so the infiltration theme *is* the awakening theme; the chip is her true identity
  surfacing under all the covers.
- **Reveal channels:** chip restoration · glitch-intrusions (charging) · how others treat her (Cain *knows*
  her) · the body (pleasure she can't explain).
- **Hide the origin, not the nature.**

**Player.** **Fixed identity — not player-named** (Wren / buried Vesper). In-world disguises are content.

**Systems:** **Phone** YES · **Clothing** YES (a **worn-state cover system** — disguise + the covers; see
*## The cover / disguise system*) · **Money/economy** YES (resources, not rent) · **Customization** minimal /
no creator.

---

## Cast (names + roles — Step 3 reshapes; Phase-1 names LOCKED)

Naming set: **grounded near-future noir.**

- **WREN ("Vesper")** — the PC. Half-human weapon in total surrender; feels only the sex she's used for;
  carries the secret dose-and-drain weapon. Knows herself as Wren; "Vesper" is the buried true name.
- **Mercer — the boss.** Her **direct owner and handler.** Owns her inside (sex + chores, however he orders),
  runs her missions, cruel, and **knows her every secret** (so he's the danger when she starts to crack).
  **Below the Chairman** — the daily master, not the apex. *(The old separate "Handler" role is merged into
  Mercer.)*
- **Dr. Elias Marrow** — the father/creator. Dead. Built both, on a human base; ordered his own erasure.
  Recovered only through the chip.
- **Cain** — the rogue, framed as "the evil one" — **actually good.** A righteous one-machine resistance: his
  "attacks" are sabotage / theft / freeing-the-hurt against Vance's *evil* operations, spun by the company as
  a vicious rogue. Marrow's first creation, half-human, the one who feels; killed Marrow at Marrow's request;
  was meant to be her partner *and* her destroyer. **Left the chip for her** (he's reaching out, not running).
  Her mirror and intended. The **kill-or-love** fork.
- **The Chairman — Aldous Vance** — the villain (above). Apex / Act-2 target.
- **Vance Dynamics** — the company (robotics/AI megacorp; its real trade is owning the powerful through
  secrets — see World setup).
- **The Lab scientist** *(name TBC — seeded for Act 2)* — Vance's in-house roboticist who maintains and
  upgrades the assets (Wren's capability *items* come from his lab) and could recognize her build — the thread
  to *what she is.* **Phase-1 role is light** (he flags her glitching).
- **The three units — Vega, Lyra, Nova** *(seeded for Act 2)* — the company's **own** field operatives,
  **complete machines: no human base, no real feeling.** Better hardware than Wren — but the company never had
  Marrow's human-base method (it died with him), so they're polished tools with nothing inside. Wren is the
  irreplaceable **original** — the only one carrying the human-derived soul the company **can't manufacture**;
  the units are the living proof it can't. *"Only you can be better"* = that soul (the chip / the awakening) is
  the very thing that makes her the underdog **and** the only *real* one — and exactly what the Chairman is
  killing to harvest (the units prove pure-machine immortality would be soulless). **Phase-1 role: mentioned
  only at the opening** (fellow operatives who set up the Act-2 mirror), not recurring.
- **Phase-1 mission targets (LOCKED):**
  - **Renner** — the **equipment supplier** (quartermaster) whose gear outfitted the **evil facility** Cain
    destroyed; never knew what it was for (a deniable vendor, so he can't tell what *she* is). Cain gutted his
    business; he's a broke, blacklisted wreck clawing at the husk and covering it up. *Cover:* Wren is **hired
    as cheap hands to rebuild**; *register:* **the underling who seduces the cold boss from the bottom.** → what
    the gear did + what Cain freed + the first crack in "evil rogue."
  - **Bastien** — docks **dealer**, Cain's supply line. *Cover:* a useful new player in his world;
    *register:* **submissive** (the newcomer he thinks he's using). → where Cain's been operating.
  - **Calloway** — Vance **insider** with the classified file; publicly a control freak, **secretly craves
    submission.** *Cover:* his new personal assistant; *register:* **domme** *(SUPERSEDED → belief-lever; see
    `## The Archive`)* (his secret is the door). →
    Cain's last movements + the company is hiding something.

> Step 3 (casting) fleshes these into full briefs. Listed here as people — no stats yet.

---

## Spatial graph & location model (Step 2b) — a living city (learned from DoL)

**Archetype: one real city you traverse** (nested districts with a street-graph feel) — NOT abstract roots.
New Halcyon is *one place*; the Tower is a **building inside the Spire.** Three districts, each a real
neighborhood packed with life. You move *through* the city (travel costs time + charge; fast-travel once a
place is known) and the city **lives around you** (people on schedules, ambient street events, a world that
remembers). *(Supersedes the earlier two-root map — rejected as a utilitarian scene-holder; see
`location_design_note.md`.)*

**Travel:** `THE SPIRE ⇄ MID-CITY ⇄ THE REACH` — each hop costs **time + a little charge**; **fast-travel**
(company car / transit) unlocks once a place is known; **returning to the Cradle** is the free reset. Each
district has a **street hub** (its living surface, where ambient events fire) + its venues.

### THE SPIRE — the corporate core (glass, the elite, surveillance)
- **Spire Plaza** *(street hub)* — chrome public level; enter/leave the Tower here. *Job:* the living surface
  — ambient corporate life, surveillance beats, glitch-triggers, exec-mark openings. [reachable]
- **Vance Tower** *(home — floors below)* [reachable]
- **Vance Securities** *(Calloway's office)* — his division runs the internal Cain-hunt; **not** read into the
  asset program (the cover holds). *Job:* **Mission 3** anchor. [reachable]
- **The Eyrie** *(rooftop members' club)* — execs above the city. *Job:* corporate honeypot ground + ambient
  elite life. [reachable]
- **Inside Vance Tower:** **Mercer's Penthouse** (top — serve him / orders) [active] · **The Units' Quarters**
  [seeded — mirror/dread] · **The Lab** (scientist) [seeded — upgrades + origin] · **The Atrium** (lobby;
  gateway) [active] · **Wren's Floor → Her Room → the Cradle** (charge, leaks, day-reset) [active].

### MID-CITY — downtown nightlife (neon, bars, hotels, crowds)
*The breathing heart — the world **beyond** the missions (no Cain-hunt mission here, on purpose), so the city
feels lived-in, not built only for the plot.*
- **The Strip** *(street hub)* — neon, crowds, ambient encounters. *Job:* the living surface — street events,
  the routine company deployment (the loop-teaching honeypot), opportunities. [reachable]
- **Mirage** *(nightclub)* — honeypot ground + ambient nightlife. [reachable]
- **The Cordon** *(hotel)* — where a mark takes her; intimate scenes / the **control canvas** live here. [reachable]
- **The Long Hour** *(lounge)* — quieter ambient spot; a recurring bartender (low thread); leads + gossip. [reachable]

### THE REACH — the docks underside (grit, the underworld, Cain's turf)
- **The Waterfront** *(street hub)* — docks strip; grit, smuggler traffic, ambient events. *Job:* the living
  surface. [reachable]
- **Bastien's** *(pawn-front / back room)* — *Job:* **Mission 2** anchor (the dealer, Cain's supply). [reachable]
- **The Anchor** *(dive bar)* — *Job:* **Mission 1** anchor (Renner drowns his guilt here; she works him) +
  ambient leads. [reachable]
- **The Facility (ruins)** — the evil Vance asset-facility Cain destroyed. *Job:* **Mission 1** investigation —
  the first dread-place. [reachable]
- **🔒 The Site** — Cain's just-abandoned hideout; the **chip**. **Locked** (*"you don't know where he went —
  yet"*) until enough leads. [locked → unlocks on leads]
- *(Marrow's lost lab — buried under The Reach; Act-2, seeded.)*

**What makes it LIVE (systems, not empty rooms):**
- **People on schedules** — targets *move* (Calloway: office by day / the Eyrie some nights; Bastien: his
  front after dark; Renner: the Anchor evenings); ambient NPCs fill the streets. You *catch* them — the city
  has its own clock.
- **Ambient street events** — the three street hubs (Plaza / Strip / Waterfront) fire random encounters: city
  life, a surveillance sweep, a glitch, an opportunity. Life you didn't trigger.
- **The world remembers** — covers build reputations, surveillance notices, word travels. A *light* reactive
  layer (the "alive" ingredient the first map lacked).

**Naming (noir, consistent):** owned/private = possessive (*Mercer's Penthouse · Wren's Room · the Cradle ·
Bastien's*); public = bare/branded nouns (*Spire Plaza · The Eyrie · Mirage · The Cordon · The Anchor · The
Waterfront · The Facility · The Site*); district headers in caps.

**Engine tree (IDs):**
- `loc_spire` → spire_plaza · vance_tower (→ atrium · wren_floor → wren_room → cradle · lab · units_quarters · penthouse) · vance_securities · the_eyrie
- `loc_midcity` → the_strip · mirage · the_cordon · the_long_hour
- `loc_reach` → the_waterfront · bastiens · the_anchor · facility_ruins · the_site🔒
- districts linked by travel (spire ⇄ midcity ⇄ reach); fast-travel once known.

---

## Top-level design (Step 2) — the engine, the web & the economy  *(in progress)*

**The fantasy register (the thing we kept getting wrong, now logical):**
- **Inside = submission.** She's an owned slave; dominance there makes no sense.
- **Outside = infiltration.** She can't appear as what she is, so she takes a **cover identity** and slips
  into a target's life. The register (caretaker / submissive / domme) is **whatever gets her in** — his
  weakness is the door. Not her nature; her tool.

**The secret weapon (LOCKED — the key that fuses fantasy + mission):** she must *mean* the sex (her pleasure
powers it); at **his climax in her ass** (anal — vaginal does NOT fire it; the most-degrading take is the trigger) she passes a fluid that gives her **full control.** **In-game (no
real timer):** the climax routes to a **control canvas** — she questions / commands / drains him (the
extraction) — and when it ends, ~10 fiction-minutes have passed and **he remembers nothing** (the mark wakes
clean, reusable). She wins by *submitting.* Never used on the boss in Phase 1 — only targets. The control
canvas is the **payoff scene of every infiltration.**

**The loop (Inside ↔ Outside):**
> **Inside:** serve Mercer (sex + chores), take the order, charge (memories leak). → **Outside:** take a
> cover, slip into the target's life, become what he needs, then deploy the weapon and drain him. → **Back
> inside:** serve, charge, dread climbs. → next target… → the trail → the site → **the chip → the fracture.**

**The hunt is a LIE from beat one.** Cain is good; the company *spins* his righteous sabotage as "vicious
rogue attacks." So the player's driving want — *catch the monster* — is built on a lie that **inverts** at
the reveal (kill → maybe love). Every mission quietly shows the opposite of the briefing.

**The Phase-1 web — three infiltrations → the chip:**
1. **Renner (the way in).** The **equipment supplier** whose gear outfitted the evil facility Cain burned; Cain
   gutted his business and he's covering it up. *Cover: hired hands to rebuild → seduce the cold boss.* → what
   the gear did **+** what Cain freed **+** the first crack in "evil rogue." Opens threads 2 and 3.
2. **Bastien (supply).** Cain's gear comes through dealers like him. *Submissive cover.* → where Cain's been.
3. **Calloway (the file).** The insider with the dossier; secretly wants to submit. *Domme cover.*
   *(SUPERSEDED → belief-lever seduce-in; see `## The Archive`.)* → Cain's
   last movements **+** "the company's hiding something."
- **Order:** Renner first; then Bastien / Calloway in **either order** (player's freedom); enough pieces →
  **the site** → Cain's gone but **left the chip for her** → first memory bleeds → **Phase 1 ends.**

**The economy (formalized):**
- **Not survival rent — the pressure is the leash + the cost of going off-book.** Phase 1: provided-for,
  **deliberately light** (a kept slave needs nothing; small spend to reach a target). Act 2: she funds her
  *own* off-book agenda — the economy *ignites* with her independence. Endgame: hunted — survival-war.
- **One wallet (credits).** Earned by working marks (= content). **Anti-grind** via the open web.
- **Sinks (wanted buys):** capability upgrades · disguise/clothing (the covers) · bribes/access (buy the way
  to the next node — the economy as connective tissue) · (Act 2) off-book survival.
- **Charge** paces the day and becomes a **vulnerability** when hunted (powering down = exposed).
- **Fail-state (§8):** YES — neglect jobs / let the malfunction show / expose yourself → the leash tightens
  (monitoring → enforcers → the hunt). Declared on purpose. **Chip-fragments are not economy** (mystery spine).

**The stat set (LOCKED — every stat gates real content; nothing decorative):**
- **Money (credits)** — the one wallet. Gates gear / disguise / bribes / upgrades.
- **Charge** (the engine's `energy`, reskinned) — paces the day (costs on actions/travel), refilled at the
  cradle; a vulnerability once she's hunted.
- **Capabilities / upgrades = INVENTORY items** — each upgrade is a thing she owns and installs (a buyable
  loadout; content gates on *owns-it*). Not a meter.
- **Chip / memories = INVENTORY items** — recovered fragments are collectibles (recovering one fires its
  memory beat; a *memories* view holds them). Not a meter.
- **Per-target lock = relation + corruption** (the target's own built-in traits; exact use set per character
  at casting, Step 4):
  - **relation** = the **infiltration** — embedded under a cover, works for him, he trusts her (*"I'm in your
    world"*). Built by the work/trust grind.
  - **corruption** = the **seduction** — how far she's hooked / compromised him (*"I'm in your head and your
    bed"*). Built by the seduction grind; extends smoothly into Act 2 (*hooked → owned*). **Replaces npc
    arousal (removed).**
  - Both high → he beds her → the weapon (climax → control canvas → drain).
- **Deliberately NONE:** her arousal · a feeling/"humanity" meter · a heat/suspicion meter. The company's
  crackdown / the leash is handled by **story beats + flags**, not a tracked bar.

**Scope (LO):** building **Phase 1 only** for now — up to the chip / the fracture. Phase 1 ends on a
**cliffhanger** (the fracture into Act 2), *not* a frontier-plateau — correct for a slice toward the whole.

**PARKED (known open questions, not skipped — Act-2 design):** **pacing/frontier** (the kill-or-love peak +
the livable post-game plateau + the endless-sandbox signpost). Phase-1 pacing is already carried by the web
(the mission loop + escalating dread → the fracture).

**Next:** Step 2b — the map (the Phase-1 location graph).

---

## Casting (Step 3) — every NPC has a role + a hook

> Most of this cast was decided across Steps 0–2; this section *formalizes* it — role, one-line hook,
> fantasy lane, depth, arc-shape, and the node each core NPC holds in the loop — so Step 4 designs each arc
> against a clear job, not from scratch. Phase-1 names locked; lighter/seeded names marked *(placeholder)*.

**Coverage (the cascade runs):** pressure source = **Mercer** (the leash) · corrupting on-ramp = **Mercer**
(he issues every mission = the loop) · core targets = **Renner / Bastien / Calloway** (three distinct lanes) ·
late-act pressure = **none external by design** — Mercer stays **oblivious** (the crack is private), so Phase-1
escalation is *internal* (her glitches, hidden) + the inverting mystery. *(Whether Pell catches a faint seed
is open — decided at Pell's design.)*
The desire span (submission→agency) is delivered across the three targets: **the underling who seduces the cold
boss (Renner) / the one who catches her and gets flipped (Bastien) / the *belief-lever seduce-in* (Calloway)** —
the last a first
taste of the user she's becoming. *(Calloway's "domme" register is SUPERSEDED → belief-lever; see `## The Archive`.)* *(Bastien's shape changed at the **Underworld-Hunt reconcile** (rev 52):
**capture-and-flip**, not a submissive-newcomer cover — three near-identical seduce-ins would be the exact
repetition this chunk exists to kill. His submission→agency beat is *earned by being caught, then turning it*.
See the reconcile note under the Casting table.)*

| NPC | role(s) | hook (dynamic · charge · want) | lane | depth | arc-shape | machine node |
|---|---|---|---|---|---|---|
| **Mercer** *(expanded, The Leash)* | pressure source · on-ramp · the inside relationship · **(1b)** the man with a new name | Your owner and handler — fucks you on a whim, hands you his chores, knows every secret you have; wants his prize weapon flawless and obedient (his own standing rides on you). **(1b)** Blown and hiding in the Reach under a flat new name, running a black-market stall in **Spire paper** — and *delighted* to see you, because you are proof he was once a man with an asset. He remembers owning you **fondly**. | dominant / owner | core (not a Phase-1 conquest) | **owner/authority — flag-driven, UNCHANGING/OBLIVIOUS** (the leash; no arc, no relation/corruption lock — he never notices her crack; that danger is Act-2). **(The Leash, rev 112)** Still no climb and still oblivious — but gains a live `npc_mercer.relation` odometer **re-cut as NOSTALGIA** (how much of his old life is back in the room). It buys **hospitality access**, never register: he is at his ceiling from beat one, so his use-scenes differentiate by *what each violates*, not by pose. He never learns anything, ever. | **inside hub** — issues the order, consumes the service, gates the day; turns "back inside" into "next target out" · **(1b) the print node** — the one hand the dead key answers to, and the only body in the world her weapon is built to refuse |
| **Renner** | core target (Mission 1, the way in) | The **equipment supplier** whose gear built the facility Cain burned — now a cold, mean wreck clawing at his gutted business; he hires you as cheap hands, ignores you, then can't hold his discipline as you tease your way up. | the underling who seduces the cold boss | core | **infiltration — relation (earn access) + corruption (break him)**; cold-boss-cracks, NO emotional arc | **entry node** — draining him (anal) opens Bastien + Calloway and lands the first crack in "evil rogue" |
| **Bastien** *(expanded, The Leash)* | core target (Mission 2) · the underworld's quiet owner | Owns the bar **and** The House both, down in the Reach, and runs everything through a web of connections — never in front. By the time the trail reaches him he already knows she's Mercer's and what she's been doing. Not a mark she seduces: the man who catches her. **(1b)** Still behind his own bar, unchanged, and pleased she came back on her own feet. | **capture-and-flip** (her cover is dead from the jump) | core | **capture-first, NOT infiltration** — no relation/corruption seduce-in climb; he's *revealed* at the kidnap that caps the Underworld Hunt, his flip + drain are the **next chunk**. **(The Leash, rev 112 — the flip lands.)** His lever is **curiosity, not desire** (the cell was a lab and he took numbers), so a seduction ladder bounces off him; what he has never permitted is being **read himself**. He **strips her at the door** every visit — he took her drain in the cell and knows where she carries it — so the arc is **smuggling, and her body is the bag**: two things to get past him now, the drain *and* the controller. Ceiling stays **cell-scoped** (the Undertow is not the cell). | **the wall the hunt hits** — the underworld trail dead-ends on *him grabbing her*; secretly Cain's ally (a **saved reveal**, kept off the kidnap — the second crack in "Cain is evil") · **(1b) the name on the set** — he is on the list her governor was built around, which is *why* she goes back down; his drain answers **why he was buying her build file: for Cain** |
| **Calloway** *(re-cast, The Archive)* | core target (Mission 3 · the file room) | The disbelieved company rogue-hunter — humiliated, sidelined, his un-indexed file room being audited shut; everyone treats him as a crank. She's the first to take his hunt seriously (works his case). His secret isn't a kink — he's **starving to be believed**. | seduce-in on the **belief-lever** (surrender = being believed / allowed to stop hunting — **NOT** domme) | core | **infiltration — his relation (belief/access) + his corruption (surrender)**, the Renner double-lock; anal finish = the drain; ends her **nemesis** | **the file node** — the un-indexed archive; his drain = her power + keeps him blind + reveals WHERE her file is (v2); his **report is the 1b fuse** to the Chairman (Aldous Vance) |
| **Cain** | the hunt's object · the reserved end (kill-or-love) · truth-bearer | The "vicious rogue" you're sent to kill — actually the one who loved you, at war with the company that owns you, leaving you a trail home. | the one reserved warmth (mostly deferred) | core to the STORY, **light on-screen in Phase 1** | **mystery/reveal spine** (chip fragments + inverting briefings; no lock) | **convergence** — the three target-nodes feed leads that point at him → the site → the chip → the fracture |
| **Dr. Pell** *(placeholder)* | seeded Act-2 origin/upgrade thread | The company roboticist who keeps you running — the one man who could read your build and realize what you are. | (not a desire target in P1) | light / seeded | **thread NPC** (flag) + upgrade vendor | **upgrade sink** (capability items) + an **(open)** glitch-flag — *does he notice in P1 at all? nobody vs one faint seed, decided at Pell's design* |
| **Vega · Lyra · Nova** (the units) | mirror / dread — the company's ideal tool (no self) | The company's own three operatives — complete machines, sleeker and stronger and *empty*; better hardware than you, no human base, no real feeling. The proof of what the company wishes you were. | (dread mirror, no desire) | light / seeded — **opening mention only** | **ambient dread** (named, no arc) | none in P1 (Act-2) |
| **Sol** | ambient anchor · **the informant** (leads-color made concrete) | The Long Hour's bartender who's seen everything and asks nothing — the one face in the city who treats you like a regular. Bring him a dead man's name and he knows who ran it, and where the survivor still turns up. | light warmth, no conquest | light island | **leads-color → the hunt's talk-hub** (no lock, no arc) | **the pointer** — turns Renner's two names into a lead on the fixer; opens the Underworld Hunt |
| **Marsh** *(new)* | the fixer — the Underworld Hunt's mark | Doss's surviving partner from the crew Renner gutted; a dockside fixer who books the same girl at The House every Sunday. Take her slot, serve him, drain him, and he gives up where the crew lived. | transactional / one-off | light (one beat) | **one-off drain** — NO relation/corruption climb; his Sunday window *is* his pacing | **the rung** — the living thread from the two dead men up to Bastien (drain → the crew's place → the grab) |
| **Rue** *(new)* | the House girl (Axis A) · a person, not filler | The worker Marsh books. Pay her to skip one Sunday and the slot is yours — and Rue **stays**, wary and owed, a named face in the brothel who isn't just a client's hole. | light warmth, no conquest | light island | **obstacle → standing thread** — schemed off the slot with coin, then persists as an underworld contact | **the way in** — clears the Sunday slot so the player can reach Marsh; her *staying* is the roster fix in miniature |
| **Kess** *(new; expanded, The Leash)* | the off-books fixer — Salvage's anchor · **(1b)** her landlord, and the man who cuts the leash | A dockside synth-mechanic in the Reach who strips decommissioned machines for parts and does quiet illegal repair on the side; reads bodies as **hardware, not women**. Clocks your company steel and nearly throws you out, then can't resist a frame nobody's supposed to be able to afford. Wants coin and the interesting problem. | supplicant / test-bench (**he** works on you) | light → **recurring** (debt-holder into Act 2) → **the spine of The Leash** | **staged repair-and-test** — NO relation/corruption climb; each fix proven on a brought body; the fixer **and** the cold channel that reads *who re-seated your drain* (never learns his name). **(The Leash, rev 112)** Same verb, harder: he **plants prototypes in her** at the seam and reads what comes back off the failures, and he is now her **landlord** — **paid per night, in coin** (his own terms, `5_scenes.toml:5214`), and a paid night buys the feed line (her charger) *and* a few days of his time on the key, so if she stops paying for nights he stops touching it. Still no meters, still wants coin and the interesting problem, still never learns Cain's name. | **the repair node** — pays the Core: Failing promise (→ Core: Locked), drops the Calloway file-room lead, leaves a `kess_debt` (broke→rich seed); re-launches at Mission 3 · **(1b) the leash node** — reads the file's shape, needs the owner's print, builds the four parts, and finally cuts the governor out (a live key lets him hold it quiet while he works — the thing his Salvage line ruled out) |
| **Vane** *(recast v2, The Archive)* | the rogue — Calloway's trusted teammate | The leak. **Secretly a trusted member of Calloway's own team** — he COPIES sensitive files (nothing ever goes missing) and feeds them to Colm; the ghost Calloway's hunted 2 years is the man at his elbow, steering him off his own trail. On-screen in 1a: she confirms him (via Colm's drained memory), **blackmails him to retrieve her file**, and he **warns her + flees** when the flush lands. | mercenary — **no conquest** (blackmail leverage, not seduction) | minor → 1a on-screen → 1b kept asset | **NON-conquest** — no relation/corruption climb; confirmed by Colm's drain; blackmailed for the retrieval (the slip that exposes him); warns her, flees underworld | **the leak node** — copies → Colm → Bastien; the retrieval she forces is the flush trigger; caught in 1b → kept asset |
| **Colm** *(new v2, The Archive)* | the courier — Bastien's man | Bastien's **off-record** courier (never on paper), a regular at the Undertow. Carries Vane's copies out to Bastien. She works him **cold and fast** — drinks, drunk, back-room fuck, drain — and his drained memory of the handoffs gives her Vane's face. | a cold underworld use (**no arc**) | minor (one–two scenes) | **NON-conquest** — the underworld drain (tonal opposite of the Calloway slow-con); yields the pipe + Vane's face → `vane_confirmed` | **the pipe node** — the off-record leg Vane→Bastien; working him backward names the rogue |

> **Underworld-Hunt reconcile (rev 52).** This is the reconcile the drain lore-swap parked ("D2 — reconcile
> when those targets are built"). The drain already stopped naming Bastien/Calloway as leads and points at the
> underworld; this chunk **builds that path** and re-introduces Bastien at its end — **re-cast**: dealer →
> owner, submissive-cover → capture-and-flip, supply-transaction → secret Cain-alliance (saved reveal). The
> **Step-3 casting artifact above is now correct.** His deeper *arc* description elsewhere (the old
> "submissive dealer / seduce-in" language at **§Cast**, **§Spatial graph** (Bastien's), **§Top-level design**,
> and the coverage line) is his **arc**, which is still deferred — those get rewritten when Bastien is
> deep-designed (Step 4, next chunk), not now. Doss & Rourke are new *named-only* dead men (never on screen);
> Marsh, Rue new light NPCs. All additive — no existing id/name/key renamed (shipped game, extend-only).

> **The Leash reconcile (rev 112).** This discharges the reconcile rev 52 parked — *"his flip + drain are the
> **next chunk**"* — and it lands in the shape the casting row always promised: **capture-and-flip, where the
> flip is her walking back into his bar on her own feet.** Three existing rows are **expanded in place**, none
> re-cast: **Mercer** keeps his unchanging/oblivious law and gains only a `relation` odometer re-read as
> **nostalgia** (access, never register — he is at his ceiling from beat one, per `trait-design.md`'s static-owner
> spine, and the meter buys hospitality, not heat); **Bastien** keeps `capture-and-flip` and gains the *how*
> (curiosity as the lever, the door-search as the mechanic, ceiling **still cell-scoped**); **Kess** keeps
> `staged repair-and-test` and gains the landlord half. The **Step-3 casting artifact above is now correct** for
> all three. What is **NOT** discharged and stays deferred: **Cain** (still off-page — Bastien's drain names a
> want, never the man), the **Chairman**, **Vane** (fled at the 1a close, not picked up), and `the_site`. All
> additive — no existing id/name/key renamed, no shipped gate closed (shipped game, extend-only). Full record:
> `games/vesper/design_the_leash.md`.

### Rough sketches + cross-NPC threads
- **Mercer** — opens the game (the office). Dispatches Renner, then opens Bastien/Calloway; debriefs and uses
  her on every return. He is the **unchanging, oblivious owner** — he **never notices** her crack in Phase 1
  (the crack stays private = hers); no leash-tightening, no suspicion. He's never the weapon's target in Phase
  1 (that's the Act-2 seed: the day she turns it on him, used→user — and the day he finally *does* notice).
  *Full first-chunk brief in Step 4 below.*
- **Renner** — at his **depot** (The Reach) by day, the **Anchor** drinking by night. Hired menial → good work
  earns the office → she teases/flashes the cold boss until his discipline cracks (rude → flirts back → blowjob
  → fucks her → **takes her ass = the drain**). The drain (anal only) extracts what the gear did, what Cain
  *freed*, the supply leads — the first wrong-note. *Threads:* the facility is where the **units** trail back to
  (Act-2); and at the ruins she **notices a part of her own build matches his supplied gear** (the personal
  seed — a cold *that's-mine* notice, not a memory; paid off at the chip).
- **Bastien** — the underworld's quiet owner (the bar + The House both), worked through connections, never in
  front. The **Underworld Hunt** ends on him: the trail (Renner's two names → Sol → Marsh at The House → the
  crew's place) lands his name, and **his people take her** in the same beat. Face to face he already knows
  she's Mercer's — his web told him, **not** Cain. *Saved reveal:* he's Cain's ally, kept **off** the kidnap so
  it lands later as its own bombshell (the second crack in "Cain is evil"; the first was Renner's drain).
  **Capture-and-flip, not seduce-in** — his flip + drain are the next chunk; this one only *reveals* him.
  *Thread:* his turf IS the underworld she's been walking, and the site sits behind him.
- **Calloway** — Vance Securities by day, the Eyrie some nights. Hired as PA → finds the craving → flips to
  **domme** → he submits → control canvas → drains the dossier (Cain's last trail + the cover-up). The domme
  register **foreshadows her awakening.** *Thread:* he's inside the Spire, so this brushes **Mercer** and the
  company's surveillance — the riskiest infiltration (working under her owners' noses).
  **⚠️ SUPERSEDED (The Archive, rev 69):** this domme / dossier sketch is the **discarded Phase-1 design.**
  Calloway is now a **belief-lever** seduce-in (**not** domme), and his drain yields *"a big chunk was stolen —
  your target's in it"* (not Cain's dossier). See the re-cast Casting row (above) + `## The Archive`.
- **Cain** — present in Phase 1 only as: the company's **briefings** (the lie), the **wrong-notes** each
  target reveals (the inversion), and the **site** (he's gone, left the chip *for her, by name*). The chip is
  the first time the hunt turns personal — he's been reaching for *her*, not running.
- **Dr. Pell** — at the Lab. She visits for maintenance/upgrades. **(Open):** whether he notices her readings
  drift in Phase 1 — *nobody notices vs one faint unalarmed seed* — is decided when we design Pell (Mercer is
  out of the noticing business; the crack is private). *Thread:* the Act-2 door to "what she is"; ally or threat.
- **Vega · Lyra · Nova (the units)** — established at the **opening only**: the company's three other
  operatives, complete machines that do the same work she does with none of the spark. Named so the world has
  peers in it, but they don't recur in Phase 1. *Thread (Act-2):* they're the company's pure-machine line —
  living proof it can't make Marrow's soul, which is why it can't replace her and why the Chairman needs her.
- **Sol** — the Long Hour bartender, and now the **informant** (his "colors a lead" function made load-bearing —
  which resolves his old add-or-cut fork = **kept**). Renner's drain gives her two dead men's names (**Doss** +
  **Rourke**); she brings them to Sol, who knows Doss ran cargo for the company before Renner made an example of
  him, and points her at Doss's surviving partner — the fixer **Marsh**, who only surfaces at The House on
  Sundays. Still no arc, no conquest: the world-beyond-the-missions that happens to know things.
- **Marsh** *(new — the fixer)* — Doss's surviving partner from the gutted crew; books **Rue** at The House
  every Sunday. She pays Rue off the slot, takes it, serves + **drains** him (the drain weapon, same as Renner) —
  a **one-off**, no relation/corruption climb. He gives up **where the crew lived**, and his watcher clocks her
  there (the seed that earns Bastien's grab). Then he's spent. *Thread:* the only living rung between the dead
  men and Bastien.
- **Rue** *(new — the House girl, Axis A)* — the worker Marsh books. Paid to skip one Sunday — the underworld
  coin's first real *use* (it's been a currency with nothing worth buying). She **stays** afterward, wary and
  owed: a named face in the brothel, the roster fix in miniature (a person, not a transaction). *Thread:* a
  standing underworld contact once the hunt's done.
- **Doss & Rourke** *(named, never on screen)* — the two of Renner's own people he killed for feeding Cain off
  his own floor. Spoken at the drain; they're the thread-*start*, not characters. Doss is the one Sol knows.

### Cast locked (your calls)
1. **Cain is physically offstage for all of Phase 1.** His presence escalates instead (the lie → wrong-notes
   → "he asked about you by name" → the chip he left *for you*); the chip at the fracture is the first real
   contact. The kill-or-love face-to-face is saved whole for Act 2.
2. **The units are complete machines (no human base, no real feeling), named individually — Vega, Lyra,
   Nova.** They're the company's own field operatives; **mentioned only at the opening** (peers who set up the
   Act-2 mirror), not recurring in Phase 1.
3. **Sol (the bartender) stays, light** — the lived-in, world-beyond-the-missions texture.

*(Placeholder names still open to rename: **Dr. Pell**, **Sol**.)*

---

## The opening (design) — the on-rails cage, then the first free step

> The agreed opening sequence. **Mostly on-rails** (Continue → Continue) across three beats — the cage —
> until one hinge node where the city opens. **~23 nodes** before she reaches Renner. Its job: show her as the
> most owned thing in the building, introduce the cast through *action* (never a lore dump), and hide three
> cracks the player sees and she doesn't. Everything she believes about herself is the lie the game takes apart.
> *(Beat = a chunk of story; node = one screen the player clicks. One beat → many nodes. Supersedes the early
> "bed → cradle" opening sketch.)*

**Shape:** Beat 1 (office) → Beat 2 (night) → Beat 3 (morning) → *out the door* → the Anchor / Renner.
**The hinge:** the final morning node — *out the door* — flips the game from on-rails to open (the city map +
real choices switch on). The twenty-odd Continue screens before it are the point: the first free step has to
*feel* like something after being owned.

### Beat 1 — The office (~12 nodes) — the punishment + the setup
1. **The line-up** — she and the three units stand before Mercer; the failed op hangs in the air.
2. **The accusation** — they had the rogue, she froze, he's gone. *(introduces the rogue + her freeze)*
3. **The threat** — he threatens to scrap her; the units stand blank. *(flavor choice: beg / silent / explain — same outcome)*
4. **She begs** — her surrender on display; she pleads to keep serving.
5. **The verdict** — too valuable to destroy ("the Chairman's investment" — *names the Chairman + her worth*); punishment instead.
6. **The punishment, set up** — he'll use her, here, now, in front of them.
7–9. **The punishment (~3 nodes, flexes ±)** — he takes her → the act (explicit, her body answering) → the units watching, blank, while *she* feels it. *(the "she feels, they don't" mirror)*
10. **Gratitude** — she thanks him; the degradation she accepts.
11. **The reassignment** — names Vega / Lyra / Nova to the head-on hunt; gives *her* the inside job ("useless with a gun, but…"); frames the mission: *the rogue murdered the Chairman's wife, enemy of the company and the world.*
12. **Dismissed** — out of the office → the night.
- **Introduces:** Mercer (cruel owner) · the three units (perfect, empty — her opposite) · the Chairman (named, the power above) · the rogue / mission (the "monster") · her (the owned asset who failed).
- **Hidden crack:** the freeze = the **first glitch.** Everyone reads it as a malfunction.

### Beat 2 — The night (~7 nodes) — the cradle, fully linear
1. **The walk back** — through the Tower to her own floor and room.
2. **The cradle** — she powers into the charging cradle; the reset ritual. *(the cradle = charge / save / start-of-day)*
3. **The tears** — her body cries; she can't explain the water; reads it as a fault to hide.
4. **The leak** — a memory fragment surfaces (a face, a sound, a name she doesn't know), then gone.
5. **The catechism** — she recites what she's told she is: *saved by the company and the Chairman, owes them everything, exists to obey.*
6. **The power** — her gift (control of a man the instant he finishes inside her, company-given) — and the odd fact it's **never** worked on the boss, never questioned.
7. **Power-down** — she promises to do better; powers down. *(the retreat into the leash)*
- **Introduces:** who she *thinks* she is (the lie). **Plants:** the awakening (tears + memory) + the boss-immunity mystery.
- **(No flavor choices — kept fully on-rails by design.)**

### Beat 3 — The morning (~4 nodes) — the task, then the city opens
1. **Power-up** — she wakes in the cradle, charged, a new day. *(the day-cycle / morning start)*
2. **The briefing** — a dossier waiting on her phone. *(the phone)*
3. **The tip** — what happened (a facility burned), why her (Renner knows the trail), what she can do (get close, the gift), where (the Anchor).
4. **Out the door** *(the hinge)* — the cover is **issued** (couriered to her quarters, not yet worn); she steps out of the Tower for the first time **as herself** → **the city opens.** → put the cover on at the rack, then the Anchor / Renner. *(Worn-state cover system — see `## The cover / disguise system`; out of cover the mark reacts wrong.)*
- **Introduces:** the loop (out → get close → drain → bring back the lead) + the cover/disguise + moving the map. **Hands off to:** Renner.

### Craft notes (how it must be written)
- **Render, don't dump.** Facts arrive through what she *does* (the charging ritual, the briefing) and the catechism she tells herself — never a backstory wall. The true origin stays underwater (iceberg); the memory is a **fragment**, never a clean flashback.
- **Crying = malfunction.** She feels *nothing but the sex* — so the tears are a thing her body does that she can't explain and would hide. The player sees grief; she sees a fault. (Same as the freeze.)
- **Belief vs. truth.** Write her self-concept *straight* (machine, saved, owes them, obeys) and **never confirm it.** The gap between what she says and what the player suspects is the engine.
- **The cage mirrors her.** On-rails = she has no will yet, so the player doesn't either. Agency switches on with her first free step.

### Onboarding — the funnel teaches the machine (per `references/onboarding.md`)
The opening is the linear funnel; besides the story it now **arms each live system once, in-fiction**:
- **Charge** — named at the cradle as what the day spends out of her and the cradle gives back (run too low → the body fails in ways a man notices). The repeatable cradle also reads the day-flip ("morning again — a new day").
- **Credits** — named in the dossier as a company cover allowance (clothes, drink, a way into a man's evening).
- **The leash (win/fail)** — surfaced lightly in the office: everything she does feeds back to the Tower; an asset that slips gets pulled in and looked at. (The fail-state *mechanic* stays deferred to the full Phase-1 web — this just makes the negative axis legible, per §8's declared leash.)
- **Next action + the HUD** — already there: the Quests page goes live at the hinge — the top **Story Goals** name the mission, **Renner's section** names his next step (goals + tip); the sidebar shows Charge / Credits / Renner at value-zero from frame one (the Renner panel's *next* row mirrors his live quest stage).
- **Every greyed gate is legible** — the **4 depot seduction rungs** show their **own action label** greyed when locked (it matches the unlocked link, and the energy gate auto-appends "(Requires 15 …)"), so locked and unlocked text always agree. The **7 sex-loop/serve finishers** still carry prose `locked_text` (mid-scene, an in-fiction line reads better than a bare label). Engine fact: a `conditions` gate never auto-derives a reason — only resource `costs` do (`getCostBlockedMessage`); for `conditions` the locked label is `locked_text or choice_text`.

### Quests page — two tiers (per `references/beat-authoring.md`)
**Tier 1 — Story Goals** (cards with no `npc_id`): the *mission*. The spine (Mission 1 — get inside Renner, drain him, find the trail) + the Burned Yard investigation + the end-of-content card. **Tier 2 — Renner's own section** (`npc_id = npc_renner`): his seduction as a **one-card-at-a-time chain** — *Earn the office* (relation → 21), then a **stepped corruption ladder** that names the current lever instead of one far-off number: R1 *tease* (→10) → R2 *flash* (→20) → R3 *grope* (→30) → R4 *he's cracking* (→40) → R5 *break him to the drain* (→50) → R6 *take him to bed* (corruption maxed, the one numberless rung — bed him, then the loadout-aware READY pair takes over). The rungs are exclusive corruption bands (`gte`+`lt`), so exactly one is live and the picker swaps it as he cracks; the chain also rides Renner's flags (`renner_office_open`, `renner_drained`, `renner_fucked_once`) and retires itself at the drain. The Renner sidebar `npc_panel` *next* row is the **same renderer** as the Quests page (`pickQuestsCard`→`renderQuestsGoalBlock`), so it steps in lockstep — the coaching verb lives in each goal's LABEL because the sidebar shows only the goal block. Body stats (Charge) stay on the sidebar, never on a quest card — the quests-vs-sidebar split.

**⚠️ Read as a whole surface at `beat_0084` (rev 129) — the first time, and it changed both tiers.** The
spine passed: exactly one live Story Goal at every state from the 1a close to `leash_cut`, ten cards D→M,
each one's closer the next one's opener. Three things did not.
- **The build boundary had been left behind three times.** Cards E, F and G each still said *"that's where
  this build ends"* about a frontier that had moved five rungs past them. The rule now: **exactly one card in
  the game names the boundary**, the Support-Us ask rides every rung regardless, and the check is a grep of
  the whole table — never a read of the card in front of you, which is what let this survive (the check *was*
  run, per-card, and per-card it passed).
- **The NPC tier was authored against Act 1a's map and never re-read.** The 1a close hard-seals the Spire, so
  Calloway's ladder and half of Colm's end card were pointing at an unreachable floor for the whole second
  half of the game — while **Renner's section disappeared entirely** on his own drain, at the moment he became
  permanent, reachable, standing content. Fixed with one high-priority card per NPC (the tier returns the
  single highest-priority match, so it wins from any arc position, including an unfinished one).
- **The chapter had no NPC tier at all.** Mercer and Bastien — the two conquests 1b runs on — had nothing,
  while three finished Act-1a arcs held the page. **Tier 2 now covers Mercer** (his re-entrance → the parts
  loop → the warm tap) **and Bastien** (the room and its search → he's yours → after the cut). **Kess gets no
  section on purpose**: he is not an arc, and the cot is upkeep, which lives on the HUD.

**The one goal bullet in the chapter** rides Mercer's loop card: `mercer_attempts → 3`. Everything else in 1b
is a flag milestone, but the three failures before the first fire are counted on a hidden trait, so the player
was running an unmarked countdown. The label names the feeder (his room, nights), not just the meter.

### Entrances (per `references/npc-intro.md`) — the bar for the unbuilt cast
Renner (assigned-target → travel → hire-on-arrival) and Mercer (motivated owner) are the two built entrances; both pass. **The remaining cast (Bastien, Calloway, Pell, Sol, …) must each clear the entrance checklist when built:** a pretext (name-planted upstream OR a staged caused-arrival), name-on-the-page + a one-line read, a first voiced line that IS their want (the casting hook), and the fire-once → `<npc>_opened_up` → gated repeatable hub shape. No bare cold-spawn hubs.

### Parked mysteries (Chekhov's guns — planted here, paid off later, not resolved)
- **The Chairman's wife.** The "rogue murdered her" story is the company's **lie / propaganda** (it keeps Cain good). What *really* happened to her is a later reveal. *(Truth: TBD.)*
- **Why the weapon fails on the boss.** *Candidate (not locked):* the weapon needs a *self* to fire (her own pleasure / will) — and in total surrender to Mercer there's no "her" present, so nothing triggers it. The day it finally works on him = the day she's awake enough to *be* someone (wires the Act-2 used→user turn).
- **Why anal — and who built her that way.** The control-agent delivers only on an **anal** finish (the most-degrading-seeming act is the trap). *Seed (not resolved):* her body was *designed* so her own degradation is the weapon — company cruelty (they weaponized the act that most debases her) or Marrow's hidden gift (he buried her power inside her submission). Sits beside the boss-immunity mystery above; paid off in Act 2.
- **The Chairman's motive.** *Optional seed:* his hunger for a deathless, *feeling* body is **grief** — he lost her and will burn the world to never lose anyone again.

---

## Deep design (Step 4) — the story of each subject, one at a time

> Step 4 designs the STORY (who each subject is, sounds like, wants, becomes). **Order note:** per LO we began
> with the NPCs — **Mercer first** — rather than the player's own thread; hers is already carried across *World
> setup*, *Top-level design*, and *The opening* (her one feeling, her light economy, her ceiling, her day-one
> start), and the explicit player thread (§2) is **now written below** (placed first — canonical §2-before-§3 order — though authored after Mercer and Renner). Each NPC is built **one chunk at a
> time**: only the self-contained part now, the cross-NPC part (debriefs, later dispatches) when those targets
> exist.
>
> *(These briefs also carry a **Build map** — the lanes/units — which is normally the later Blueprint step's
> job; LO chose to settle Mercer's story and structure together for this first chunk.)*

### The player thread (Step 4 · §2) — the inverted protagonist

**The shape.** Every NPC climbs a ladder (cold → surrender). **She starts at the bottom of herself.**
Maxed-degraded on night one: used by everyone, owned by Mercer, feeling only the sex. Her thread isn't
corruption going *up* — it's surrender cracking *open*. Phase 1 is the **first crack, not the awakening**; she
ends **fracturing, not free.** (The inversion of the normal §2: no prudish-to-depraved ladder — she's pre-maxed,
and her arc is *waking*, not *falling*.)

**End-state (Phase 1).** Still the company's tool, but no longer seamlessly. The three infiltrations are run, the
contradicting evidence has piled up, the glitches have worsened, and at **the_site** she gets the chip — the
first memory bleeds. Her surrender has its first fault line. The cliffhanger into Act 2.

**Voice.** Flat. Procedural. A tool narrating its tasks — RTS-flat isn't a style choice for her, it's *who she
is* (hollow). She reports; she doesn't emote. The cracks **leak** rather than pour: a freeze she can't explain,
wetness on her face she has no word for, a body reacting to a stranger like it knows him. **Tier-3 prose is
spent ONLY at the glitch-intrusions** (the once-only peaks); everywhere else, flat.

**Her sexuality is entirely instrumental (Phase 1).** She has **no sex that's about her.** Inside, Mercer uses
her (his chunk); outside, she seduces targets (theirs). Her own thread carries **no standalone explicit scene** —
her explicit content lives *inside* the NPC chunks. What's hers is the *awakening*, and in Phase 1 the awakening
is **not sexual** — it's dread. *(Solo desire — wanting sex for herself — is cut from Phase 1; deferred to Act 2,
when there's a "her" to want.)*

**The arc (the moments, in order):**
1. **Total surrender** — she serves, takes orders, runs the loop; her motive *is* the company's (catch the rogue).
2. **The first glitch** — the opening's freeze (she couldn't kill Cain) + the cradle's tears + the first memory
   fragment. The body does what the company didn't assign; she files it as a malfunction.
3. **The loop runs** — inside (serve Mercer, charge) ↔ outside (infiltrate, drain). Every mission, the briefing
   says "evil rogue" and the evidence says the opposite.
4. **The wrongness accumulates** — the glitches worsen, the contradictions stack, the dread the player already
   feels starts reaching *her*.
5. **The site** — enough pieces → Cain's gone, but he left **the chip for her**.
6. **The fracture** — the first memory bleeds. She was someone. Phase 1 ends on the fault line.

**Her axis (singular — not corruption).** Her one progression is the **awakening: chip fragments + the
accumulating glitch-dread.** Mission-progress (the web) is the engine that drives it. **No personal corruption
ladder** — the per-target relation/corruption are the *targets'* axes, never hers. *(The engine keeps
`corruption` + `hygiene` always-on; the design leaves both **dormant** for her. Whether to reskin the dormant
`corruption` into a visible "Awakening" meter or leave it dead and let the chip-inventory be the only ladder is a
Blueprint-time mechanism call — current lean: leave it dead, the chip is the stronger ladder.)*

**The weapon = her only agency.** The drain is "the one thing that's hers." In Phase 1 it's her sole act of self
— done in service, but hers. It's the **proto-seed of used→user**: every mark she takes control of, she's
practicing the thing she'll one day turn on Mercer.

**Where the dread lives.** Not in a meter — in **texture**: the glitch-intrusions + every mission's evidence
quietly contradicting the briefing. The player senses it a step ahead of her; she's the last to admit it. This is
her thread's "Lane 2."

**The glitch model (the only register for her awakening).** Glitches are **involuntary leaks of the buried self —
grief, memory, recognition.** The body does something it shouldn't; she files it as a fault. **Never a clean
reveal** (no name surfacing — that pours the central mystery early; the chip IS the ladder) and **never
conscience** (no moral flinch — she has no self to hesitate with yet; that's a sentimental awakening, and it
cheapens the Cain-specific freeze into generic mercy). **No net-new standalone glitch beats** — they're
**embedded one per tentpole**: the opening (tears + first fragment) · each mission's investigation (a
*recognition* — Renner's "that's mine" at `facility_ruins` is the template; Bastien + Calloway each carry their
own) · the fracture (the chip's first real bleed). The **cradle**, on return, carries *escalating recurrences* of
the same leaks (the tears again, fragments stacking) — not new categories.

**The four §2 pieces, mapped to her:**
- **Bootstrap (2A) — inverted.** No off-zero solo act (she's pre-opened, not opening). The nudge isn't arousal —
  it's the **glitch**. Her drive is **reactive** (the buried self / Cain / the chip), planted in the opening; at
  the start she doesn't know it and runs the company's motive.
- **Exhibition (2B) — instrumental.** No personal exhibitionism. Her "being-seen ladder" is the **cover ladder**
  — how brazenly she deploys her body as a tool, scaled per mission (the commando-flash at Renner is *tactics*,
  not thrill). The personal version is an Act-2 seed.
- **Economy (2C) — the light leash.** Phase 1 thin by design: she earns small credits working marks (Renner's
  depot) and spends them on **disguises + bribes + capability upgrades** to reach the next node. Not survival, not
  broke→rich (Act 2's ignition) — the economy is the **leash + the cost of going off-book.** The buys she covets =
  the upgrades (each a concrete mission power).
- **Ceiling (2D) — the inversion itself.** Her most extreme act-about-her isn't a depravity peak — it's the
  **drain**: she submits to the most degrading thing (takes it in the ass) and *that's* where she seizes control.
  **Peak degradation = peak power.** Her non-corruption ladder = the **chip + upgrades** (inventory).

**The daily routine the world walks in on.** The **cradle** (charge/sleep) — her one private routine, and the
place the **glitch-intrusions** intrude (the chip bleeding into her downtime). Mirror of Mercer's chore-hijack:
*he* walks in on the chores; the *chip* walks in on the cradle.

**Anti-patterns.** No corruption ladder (she's not climbing one). No solo-sexual content (cut). No fast or
sentimental awakening — it **leaks**, dread-first, she's the last to know. No conscience/flinch and no
name-reveal (both against the reveal architecture). No warmth from her in Phase 1 (reserved for Cain, the very
end). No backstory dump (reconstructed, never poured).

**Acceptance (done when).** Her flatness reads as *hollow*, not boring; the glitches land as *wrong*, not quirky;
the evidence-vs-briefing contradiction is felt every mission; the chip is the only progression that feels like
*her*; the drain reads as her one act of self; Phase 1 ends on a real fault line, not a resolution.

**Build map (the thread rides through the game — it isn't its own location):**
- **The cradle hub** (existing location `cradle`) — charge/sleep + day-reset/save + the glitch host + the
  memories/upgrades access point.
- **The glitch-intrusion beats** — auto-fire, capstone-shape, single-Continue, Tier-3; embedded one per tentpole
  (opening / each mission investigation / the fracture); no standalone beats.
- **The chip / memories view** — the inventory UI holding recovered fragments (her ladder, made visible); each
  recovery fires its memory beat.
- **The capability upgrades** — inventory buys (the economy sink); content gates on owns-it. Example set (lock at
  Blueprint): a charge upgrade (longer off the cradle), a cover upgrade (hold a harder disguise), a read-the-mark
  upgrade (surface a target's tell).
- **The drain / control canvas** — her weapon; built per-target (Renner first), reused.
- **The mission web** — the spine the awakening rides on (Top-level).

**Deferred (Act 2 / the "for now"):** the solo want (sex for *herself*, once awake) · personal exhibitionism ·
the dominance / used→user turned on Mercer · the broke→rich economy ignition.

> **Act 2 · The Archive advances the used→user turn — in motion, not resolved.** Salvage leashed her (a control
> chip blocks her power on her owner, Mercer). The Archive has her take the **leash controller** (the key that
> makes a later cut safe) — but she **stays leashed**: the cut risks her still-**Failing** core and needs
> **Kess's** hand. She ends holding her own key, unable to use it yet. **Purely in-fiction** — no sidebar
> marker, no new meter (LO); the dormant `corruption` stays dead, the fiction is the ladder. Solo want /
> personal exhibitionism / broke→rich ignition stay deferred. Full arc: `## The Archive`.

> **Act 2 · The Leash COMPLETES the used→user turn — and immediately prices it.** The Archive left her holding
> a key she could not use. This chapter cuts the leash and spends it: **the first thing she does with her own
> weapon is her owner** — and it is not a rebellion, it is a **con**. She goes back to Mercer on her own feet,
> lets him use her exactly as he always did, and hides a prototype firing in her chest from a man who has never
> once looked at her closely enough to notice. Her submission becomes **tactical** for the first time in the
> game; nothing about her behaviour changes, only why. **Still no meter** — the `corruption` bar stays dead,
> the fiction is the ladder (LO, unchanged since Step 2). And the win is priced twice over: the key speaks for
> **one name**, so the first fire buys her a hall pass rather than freedom; and what finally opens with the
> governor is **her own page** — the programme, the many subjects, and her at the centre of it. She ends the
> chapter free of the hardware and no longer able to not-know what she is. **Guard-rail:** she never narrates
> the plan — one `thought_bubble` a scene, the same ration as the glitch beats. The moment she is *seen* being
> clever, the inverted protagonist breaks. Broke→rich ignition begins here (rent, parts, reloads) but the solo
> want stays deferred. Full arc: `## The Leash`.

**None, by design (Phase 1):** no solo-sexual content · no personal corruption meter (dormant) · no
feeling/humanity meter (cut) · no player-named identity · no warmth.

**Size.** Small as discrete units (the thread mostly rides the NPC + mission content): the cradle hub + the
embedded glitch beats + the chip/upgrades UI + the drain (per-target). The *weight* is in the writing — the
flat-voice-with-cracks and the Tier-3 glitches — not the canvas count.

### Mercer (Step 4 · §3, Pass 2) — the unchanging owner — FIRST CHUNK

**The shape — why he's unlike every target.** Mercer is **not a conquest.** The three targets are climbs
(cold → hooked → bedded → drained). Mercer isn't: she starts **already fully his**, so there's no ladder, no
seduction, no relation/corruption lock. His weapon-immunity is canon — the one man it never works on. So he
has **no arc**: same cold ownership on day 1 and at the fracture. The drama is that *she* changes while *he*
never notices. He is the **home base of the loop** and the embodiment of the ownership fantasy — the
most-visited screen in the game.

**End-state (Phase 1).** Nothing about Mercer moves. By the fracture he's the same bored, total owner, still
certain he owns every inch of her — **completely oblivious** that she's cracked underneath (no leash-tightening,
no suspicion; the crack stays *private*, which is what makes it hers). The Phase-1 "win" against him is just
**survival** — keep him satisfied, keep the cracks hidden, give him no reason. *(Act-2 seed, untouched: the day
she turns the weapon on him — used → user.)*

**Voice.** Clipped, calm, proprietary — never raises his voice because he never has to. Orders, not requests;
talks *about* her in front of her like furniture. Cruelty is **casual and bored**, not theatrical (scarier
calm). **Pure cold** — no warmth thread (that's reserved for Cain). Calls her **"my investment" / "asset"** —
ownership in the language itself. Always **spoken** in dialog, never narrated summary. *(A texture that keeps
him from being a brute: he's an owner who is himself owned — his standing with the Chairman rides on her, so
the cruelty has his own pressure under it.)*

**The use-scenes — four distinct violations** (the everyday content; each must land its OWN note, or they blur
into "he fucks you again"):
- **The hub (baseline)** — she goes to him, on his menu. The chosen, routine *serve him.*
- **Chore-hijack** — she's doing a task *for* him and he pulls her off it to use her. Violates her
  **attention/labor**: *you exist for my use even mid-work.*
- **The summons** — she's at her cradle and an order drags her out of it, up to him. Violates her
  **downtime**: *you are never off-duty.* (The routine intrusion — more frequent.)
- **The invasion** — he comes down into her own room, her last private space, because he can / likes her
  powered-down and vulnerable. Violates her **sanctuary**: *nothing is yours.* (Rare and cold — the **first one
  is a once-only scripted beat**, the gut-punch; rare repeat after.)
- **Catch-him-with-another-asset** — she walks in on him mid-use with another girl; he doesn't stop. *She's one
  of many.* She watches **flat/unbothered** (colder now; can ache later when she wakes).

**The big nights (once-only).** The **opening office scene** (already designed — ownership at its most total) +
a short **first-time-at-the-Penthouse** that switches the inside hub on + the **first invasion**.

**What changes after.** **Nothing** — he's stable by design. The only Mercer state that ever moves is the
deferred cross-NPC dispatch (which mission is live), not the man.

**Anti-patterns (so he stays himself).** No seduction / relation / corruption arc; no power over him in Phase 1
(he's the immovable one); no mustache-twirling (calm menace, not theatrics); no backstory speeches (the
Chairman-pressure shows through behavior); **no control-canvas on his sex loop** (the immunity — his
inside-finish just ends; the weapon bolts onto the *targets'* loops, never his).

**Acceptance (done when).** He reads as the total owner who **gates the day**; the loop's home base works
(serve → charge → out → back); the four use-scenes each keep a distinct note; the boss-immunity is established
and left a mystery; and **nothing resolves** — he's oblivious to the very end, the danger is all Act-2.

**Build map (the units — settled early with LO; normally Blueprint):**
- **Where/when:** his **Penthouse** (top of the Tower), scheduled there when she's home (also paints him on the
  nav so she sees he's up there).
- **Lane 1 — inside hub:** his portrait + a **fixed** small menu (report · serve → the loop · leave). No locked
  rungs; same menu all game.
- **Sex loop (full):** the standard repeatable machine (poses → pleasure meter → climax-elect → finisher),
  prose/verbs written **his-POV "he uses you"**; **no control-canvas** (immune — his inside-finish just ends).
- **Lane 3 chores:** serve-him solo-work hosts (servitude texture, **not** the money loop — he never pays her);
  cost time/charge.
- **Lane 3 chore-hijack:** "he pulls you off the task." His presence in his own room is the gate. **Flat
  chance** (no rising bands — he doesn't escalate).
- **Lane 3 summons:** on her cradle activity — routine, drags her up to him.
- **Invasion:** in her room — rare; **first = once-only scripted**, rare repeat after.
- **Lane 2 — catch-him-with-another-asset:** atmospheric voyeurism at the Penthouse; flat/unbothered.
- **Establishing capstones:** the opening (done) + first-Penthouse-service.
- **Flags:** the day-gate (served-him / day-reset). *(The first dispatch — Renner — is the opening's morning
  phone briefing, not a separate hub beat.)*

**Deferred (cross-NPC — next chunks):** his **debriefs** (reacting to each mission's leads) and **later
dispatches** (opening Bastien/Calloway after Renner) — built when those targets exist.

**None, by design:** no relation/corruption escalation ladder · no stat-climbing sex loop · no shop/economy
role (Pell sells upgrades; the shops sell disguise) · no customization.

---

### Renner (Step 4 · §3, Pass 2) — the cold boss she seduces from the bottom — FIRST CHUNK

**The shape — why he's unlike Mercer.** Renner is the **mirror-opposite of Mercer**: where Mercer is the
unchanging owner (no lock, no climb), Renner is the **full climb** — cold → cracked → bedded → drained — the
first real infiltration. His chunk also **stands up the weapon's control-canvas for the first time** (the
scene-pattern all three targets reuse), so it's the meatiest chunk so far and the full four-lane spread.

**The fiction (the quartermaster).** Renner **supplied Vance the equipment** that outfitted the asset-facility —
the rigs, the containment, the gear — through normal procurement, **never knowing what it was for.** That's the
deniable wall: a vendor is plausibly ignorant, so he'd never clock what she is. **Cain gutted his business** (a
node in Vance's pipeline); what's left is a **husk** he's clawing at, broke and blacklisted, the handlers leaning
on him to keep the cover-up, drinking himself down. She comes as **cheap hands to rebuild** — and that's the way
in. The irony: the one thing his gear was built to manufacture is hired as his help, and he can't see it.

**End-state (Phase 1).** Drained and compromised — the cold boss whose discipline she dismantled, who fucks the
help and gives up the truth at the control canvas without ever knowing what she took. **No emotional dependence**
(cut) — he's hooked on the *sex*, not her warmth. The mission payload extracted (what the gear did, what Cain
freed, and the **feud** — the two he killed fed Cain off his own floor, so Cain torched his yard → the first
crack in "evil rogue"); the lead now points at the **underworld** *(D2: Bastien/Calloway retired as named leads)*.

**Voice.** Cold, mean, contemptuous of the help — a **businessman, not a monster** (worse). Curt, talks down to
her, **haunted underneath** (he drinks; the gutted business shows). The key move: his reaction to the *same*
provocation **climbs** as he cracks — she flashes him → *"put those away"* (doesn't look up) → he looks and
catches himself → *"you do that on purpose"* → *"come here."* So his voice runs **contempt → caught-looking →
reluctant want → openly wants her** — carried by his *reactions*, NOT by rewriting his opener (one man losing one
battle, slower each time; permanent, no yo-yo). She stays cool; **he's the one who gets rattled.**

**The arc (the moments, in order):**
1. **Hired, menial** — grunt work; he's cold, ignores her, she's beneath notice.
2. **Good work → noticed** — she's useful; he stops ignoring her. *(relation climbs)*
3. **Into the office** — relation earns her work in his office — the proximity that unlocks everything.
4. **She works him** — teasing, flashing (working without panties); at first he's **rude, shuts it down.**
5. **He flirts back** — the cold cracks; he engages.
6. **The boner / her mouth** — she catches him hard and goes down on him *(first explicit rung — she initiates).*
7. **He fucks her** — vaginal, becomes the routine *(mechanical — no scripted scene).*
8. **He takes her ass** — she's working commando, he bends her over and shoves it in; anal → **the drain.**

**Two axes.** **relation = earn access** (menial → good work → *into the office* — gates the **space**);
**corruption = break him** (tease → flash → flirt-back → blow → fuck → **anal** — gates the **seduction**, inside
the space relation unlocked). The office is the exposure ceiling doing real work: depot floor = public/work only,
his office = private/the full climb.

**The weapon (his loop is the first build).** Anal-creampie fires the control canvas (vaginal doesn't); the drain
extracts the mission payload. **The weapon cracks him, not the seduction** — a cold man who'd never confess gives
it up only when she owns him. The repeatable loop's **anal finish** re-routes to the drain (reusable). This chunk
establishes the control-canvas pattern every target reuses.

**Where the guilt lives (NOT in the seduction).** No emotional/caretaker arc — she gives temptation and sex, not
comfort. His guilt lives in **Lane 2 ambient** (he drinks at the Anchor, the rot showing — the player sees it, the
seduction never processes it) and the **drain payload.** He stays cold and haunted; she never nurses it.

**The cheer-up (sex-as-comfort, not warmth).** Walk in on him wrecked → once it's unlocked, she **cheers him up
with sex, scaled to progress** (early a tease; post-blowjob she blows him; post-anal she takes it). It's the one
real thing she has (she feels only the sex) — deployed, not felt. A repeatable Anchor reward, written hot, no
cold-only asterisk.

**The morning-afters (the world remembers).** On the big crossings (the blowjob, the first anal), the **next day**
she puts it on him, cool — *"did you like it, or not?"* He can't brush it off; the acknowledgment is the
**corruption ratcheting** (an escalation rung, not flavor). Surgical — only the big crossings, never the loop.

**The personal seed (facility — the physical match).** At the **facility_ruins** investigation she **notices a
component / stamp in the wreckage that matches a part of her own build** — a flat, clinical *that's-mine* (NOT a
memory). The player supplies the horror she can't; it ties to Renner (the matching gear is what he supplied — the
man whose ass she's working supplied the parts she's made of). A **seed**, never explained, paid off at the chip
(manufacture, not memory — so it doesn't spoil the chip's reveal). Built like the opening's freeze/tears: a
one-time **auto-fire beat** (capstone-shape, single Continue, no choice), riding on the investigation — separate
from the seduction capstones.

**Anti-patterns.** No caretaker/emotional-dependence arc (she never comforts him). No warmth from her (the sex is
the only real thing). Don't tier his hub *opener* per stat band — the change rides on his *reactions* to her moves
(one man cracking, not three characters). Don't capstone every unlock — reserve the scripted treatment for the
turning points; the climb is mechanical rungs.

**Acceptance (done when).** The cold boss visibly *cracks* (his reaction to the same tease climbs across the arc);
relation gates the office and corruption gates the seduction inside it; the **anal drain** lands as the weapon's
first fire + the mission payload; the morning-afters make the break undeniable; the facility match plants the
personal seed without spoiling the chip; and the guilt lives in the ambient + the drain, never in a warmth she
doesn't have.

**Build map (the units — settled early with LO; normally Blueprint):**
- **Where/when:** his **depot/yard** (The Reach — NEW location) by day → the **office** inside it (the seduction
  space); the **Anchor** evenings (drinking). Scheduled so the nav paints him where he is.
- **Lane 1 hubs:** the depot (work register) + the office (relation-gated seduction) + the Anchor (off-duty/drunk
  register). Portraits + escalating menus.
- **Lane 1 rungs (mechanical):** tease / flash (commando) / grope / the early seduction — locked-visible,
  click-to-play. The **first vaginal sex** unlocks here too (mechanical, no scripted scene).
- **Lane 3:** menial work hosts at the depot (haul/sort/log — earn **light credits**, the early income loop) +
  Renner **walk-ins** that **rise** (early he lingers watching, late he pulls her off the task — stacked
  corruption bands, unlike Mercer's flat hijack).
- **Lane 2 — the Anchor:** the witness texture (varied glimpses of the ruin under the boss, tiered) + the
  **cheer-up sex** hook (walk in low → sex, scaled to progress).
- **Sex loop (full machine):** poses → pleasure → climax-elect → finisher; the **anal finish routes to the
  drain.** Vaginal/oral stay in for variety; only anal drains.
- **Capstones (3 scripted) + morning-afters:** the **hire** (auto-fire intro) · the **first blowjob** · the
  **first anal = the drain** (the commando-shove). Everything else mechanical. Morning-afters on the blowjob + the
  anal.
- **The facility investigation:** facility_ruins — explore + the evidence (what the place did, the wrong-note) +
  the **one-time match beat** (the personal seed). The Mission-1 *location* leg, not the seduction spine.
- **Economy:** the depot work = an early earning loop (light, Phase-1-thin). Income source, **not a shop.**
- **Flags:** the spine chain (hired → noticed → office → oral → fucked → anal/drained); the drain sets the
  lead-flag `renner_leads_extracted` — now the **underworld pointer** (the drain confession sends her down past
  the gate), not the two named targets. *(D2: Bastien/Calloway retired as named leads; underworld-first.)*
- **Geography note:** the **Cordon drops out** of Renner's chunk — the cold boss uses her at work (over the desk),
  not a hotel.

**Deferred (cross-NPC — next chunks):** the drain's **downstream** (now the **underworld trail** — the confession
points there; Bastien/Calloway retired as named targets, D2) · **Mercer's debrief** after Renner · Renner's
contribution to **the_site** convergence · how the wrong-note **accumulates** across the targets.

**None, by design:** no caretaker/emotional arc (cut) · no shop/vendor role (income via the work, she buys
nothing from him) · no customization · not unchanging (the whole point is he falls).

**Size:** ~16–20 canvases — the biggest chunk so far (the rising walk-ins, the cheer-up, the morning-afters, the
two-stage consummation, the investigation + the match beat).

---

## Blueprint (Step 5) — the gated, placed, lane-tagged scene list

> Step 4 said *what happens*; this turns it into the exact scene list — each scene named, given a lane, a gate,
> a place, and its wiring — so Step 7 builds TOML without re-deciding anything. Built **subject by subject**
> (player → Mercer → Renner → the chunk's world → the holistic wiring), propose-first.
>
> **Scope — build-order, not a cut.** We blueprint the deep-designed **A→A.5 chunk** (the player thread,
> Mercer, Renner, and the locations they touch) to **full depth**. Everything not yet deep-designed — Bastien,
> Calloway, Cain, Pell, Sol, the units; Mid-City; the world §5 + reactivity §4; *the_site / chip / fracture* —
> is the **frontier**: telegraphed here as locked-visible seeds, blueprinted when its Step-4 design exists.
> This is *not* a slice — each subject in the chunk is built to its full designed budget.
> *(Re-entry after the removed batch build; see ledger turn 16 + the audit `wf_e8f36ff0-f84`.)*

### Player blueprint (Pass 1)

**The spine decision (locked — LO chose A).** She has **no personal corruption ladder.** The engine's
always-on `corruption` stat is **left DEAD** — *not* reskinned into an "Awakening" meter — because a meter that
gates nothing is decoration (against the locked "every stat gates real content" rule), and her real ladder is
the chip + the felt dread, not a number. **Her live meters are Charge + Credits only.** Her one progression
axis is the **awakening** (chip fragments + accumulating glitch-dread), driven by mission-progress flags — and
in this chunk the chip is **un-fed** (its first fragment is at *the_site*, the Phase-1 end), so **she carries no
visible personal bar through the chunk, by design** (the inversion: she's the still point; the targets fall).

**The feeder economy dissolves.** With no player-corruption door, the usual supply→demand check (does the
player have enough corruption to unlock an NPC) **doesn't apply** — every NPC rung gates on the *NPC's own*
relation/corruption, built by playing that NPC. There is no player-feeder count to close.

**The scenes (player-side, in-chunk):**

| Scene | Lane | Gate / trigger | Place | Notes |
|---|---|---|---|---|
| **Cradle — power down (day-router)** | Lane 3 solo host | schedule 19:00–05:00; ungated | `cradle` | wake +~9h, Charge→full, day-reset. The reset that makes the daytime (Renner's depot) reachable from the evening start. |
| **Cradle — glitch recurrence I** | auto-fire, capstone-shape (Tier-3) | flag `worked_renner_once` is_true + guard `glitch_i_seen` is_false → SETS `glitch_i_seen` (fires once) | `cradle` | the tears / a fragment return — escalation rung 1. Single Continue. |
| **Cradle — glitch recurrence II** | auto-fire, capstone-shape (Tier-3) | flag `renner_drained` is_true + guard `glitch_ii_seen` is_false → SETS `glitch_ii_seen` (fires once) | `cradle` | the leak worse, fragments stacking — escalation rung 2 (lands **heavier than I** — the design's "escalating recurrences", delivered by the two beats, not a recurring ambient). The chunk's awakening peak (the fracture proper is frontier). |
| **Chip / memories view** | UI access (seeded) | always; **empty state** in chunk | `cradle` | the inventory screen for fragments; fills at *the_site* (frontier). Built as access + **one greyed named locked slot** ("FRAGMENT 01 — locked: recover at the site") so the awakening ladder shows a visible next rung, not a blank screen. |
| **Capability upgrades** | economy sink (seeded) | **no vendor in chunk** | (Pell / lab — frontier) | nothing buyable yet; the sink opens when Pell is designed. |
| **The drain / control canvas** | Lane 4 payoff | anal finish on a target's loop | (Renner's office) | her one act of agency; **specced in Renner's blueprint** — the first build of the reusable pattern. |
| **Travel — Spire ⇄ Reach** | Lane 3 solo links | ungated; `costs` time + a little Charge | `spire_plaza` ⇄ `the_waterfront` | the leash that makes schedules bite; fast-travel once known. |

**Economy (shape locked; exact numbers settled at authoring):**
- **Income:** Renner depot work — light credits per shift (the only source in the chunk).
- **Sinks:** none real in-chunk. The Mission-1 cover is **issued by the boss, not bought** (a real worn-state
  garment now — see *## The cover / disguise system* — granted to her wardrobe at the briefing, equipped at the
  rack; it costs no credits). The disguise *shop* + Pell's upgrades stay frontier. Credits accumulate —
  consistent with "a kept asset is provided for; Phase 1 deliberately light." **No filler sink invented** (LO).
  Credits are a **primed-but-dormant gauge** — the first real spend is the Mission-2 disguise shop; stated so
  Step 7 doesn't ship an idle HUD number.
- **Charge:** paces the day (costs on actions/travel), refilled free at the cradle.
- **Fail-state:** **none in the chunk** (LO). The leash → enforcers → hunt is a Phase-1-wide ramp that needs
  the full mission web; here Charge is a *soft pace* (run low → reset), not a lose condition. Wired when more of
  Phase 1 exists.

**Frontier seeds (telegraphed, deferred — never silent gaps):** the chip/memories view (fed at *the_site*) ·
the upgrades sink (Pell's lab) · the leash fail-state (full web). Each has a built, visible, empty-or-locked
home in the chunk.

**Reachability:** the cradle is where she wakes each day (always reachable); the day-router's 19:00–05:00
window carries her from the evening start to the depot's daytime. ✓

---

### Mercer blueprint (Pass 2a)

**The shape — the exemption.** No climb, no ladder, no relation/corruption lock — she starts already fully his
and he never changes, so there's no descent list to order, just the **home base of the loop** + his four
distinct use-scenes. His content gates on **one flag** (`mercer_hub_open`) + his presence, never a threshold.

**The scenes:**

| Scene | Lane | Gate / trigger | Place | Note |
|---|---|---|---|---|
| **First Penthouse service** | Lane 4 capstone (once) | `opening_done` + first visit to penthouse → sets `mercer_hub_open` | penthouse | switches the inside hub on. |
| **The inside hub** | Lane 1 hub (portrait, **fixed** menu) | `mercer_hub_open` + present (08:00–23:00) | penthouse | Report · Serve → loop · Leave. Same all game, no rungs. |
| **The serve loop** | Lane 1 sex loop (his-POV, full machine) | via the hub "Serve" | penthouse | poses → pleasure → climax → finisher; every finish just ends — **NO drain** (immunity). |
| **Chore-hijack** | Lane 3 chore host + walk-in | present + on the chore; **flat chance** | penthouse | pulled off the task → use. Violates *attention*. No escalation. |
| **The summons** | Lane 3 walk-in | at cradle, 19:00–23:00, `mercer_hub_open`; routine chance | cradle → penthouse | dragged out of *downtime*. The frequent one. |
| **The invasion (first)** | Lane 4 capstone (once-only scripted) | `mercer_hub_open` + `worked_renner_once`; guard `mercer_invaded_once` is_false | wren_room | the gut-punch — into her *sanctuary*. |
| **The invasion (repeat)** | Lane 3 walk-in (rare) | `mercer_invaded_once` + low chance | wren_room | cold, rare echo. |
| **Catch him with another asset** | Lane 2 ambient (voyeur) | `mercer_hub_open` + low random chance | penthouse | walks in mid-use; flat/unbothered — *one of many*. |

**The serve-loop menu.** Poses are the his-POV use positions — on her knees · bent over the desk · used
against the glass — `sex_stage` switched by *him*, not earned; the finishes (in her mouth / on her / inside)
**all route to "just ends — NO drain"** (the immunity). Anti-stale levers (he never escalates, so the loop
can't lean on rising stats): the ownership-diction varies ("my investment" / "asset" / talking past her to a
call), and which frame colors the session (bored · making a point · between meetings). The distinctness is the
cold ownership, not variety of acts.

**Gate philosophy — the sanctioned exemption.** Mercer is the deliberate exception to the double-lock: his
lewd content carries **no player-corruption door** (she's already his) and **no NPC climb** — only
`mercer_hub_open` + presence + the once-only guards. Non-lewd "Report" is fully ungated.

**Locked calls:** no daily cap on serving (home base, no stat to grind); the first invasion fires after
`worked_renner_once` (lands once the routine exists to violate); the serve loop is his-POV "he uses you" with
**no control canvas** (the immunity — the weapon bolts onto the *targets'* loops only).

**Reachability:** penthouse 08:00–23:00 (offscreen overnight; the nav paints him up there). The summons fires
in the 19:00–23:00 overlap at the cradle; the invasion is a scripted intrusion into wren_room (*he* comes to
*her*, not schedule-bound).

**Frontier (telegraphed, deferred):** his **debriefs** (reacting to each mission's leads) + **later
dispatches** (opening Bastien/Calloway after Renner's drain) — need the other targets; seeded, not built. The
Renner dispatch is the opening's morning phone briefing (done).

---

### Renner blueprint (Pass 2b)

> The biggest chunk — **19 canvases (seduction spine) + 2 (the facility leg)**, full ~16–20. Compiled +
> adversarially verified (`wf_cfc47034-9c5`): nothing from the brief dropped; two engine traps caught and
> rerouted before TOML (the office unlock had no setter; the drain's flags can't sit on the triggerless
> control canvas). **Fork A resolved (LO): the office is FOLDED into the depot hub as a register-shift** — not
> a separate navigable room (one location, one schedule, the portrait always renders).

**The spine — two axes on HIS meters (the double-lock variant).** She has no corruption door (left dead), so
both axes are Renner's own: **AXIS 1 — access** = `npc_renner.relation` (an odometer built by the *ungated*
"good work / check in" + each work shift) earns the office; **AXIS 2 — seduction** = `npc_renner.corruption`
(his willingness, +2 per charged rung) gates the lewd rungs; `npc_renner.arousal` is the loop
throttle only (never gates progression). Every lewd rung double-locks on **office-open (access) + his
corruption (the tier)**. **Pacing (Fork B): relation-fast / corruption a paced campaign** — noticed quickly
(office at `relation ≥ 21`), but the drain is a grind (`corruption ≥ 50`, the whole ladder ×2.5). Each charged
rung **COSTS 15 Charge + 180 min**, so the 09:00–18:00 office window caps it at **~3 rungs/day** — the workday
ends, she sleeps, recharges, returns. No daily-flag cap; the throttle is diegetic (Charge + the office clock).
Full ladder: flash 10 / grope 20 / blowjob 30 / loop 40 / drain 50. His voice climbs by **reaction** to the same provocation
(contempt → caught-looking → reluctant → wants her), **pinned to disjoint corruption bands on the rungs** so
the crack is authored, not luck — the base opener stays one constant paragraph.

**The scenes (19 + 2):**

| # | Scene | Lane | Gate | Place |
|---|---|---|---|---|
| 1 | **hub_depot_floor** | L1 hub | unconditional base; "good work" (ungated relation feeder) + "work a shift"; once `renner_office_open`, the **office seduction register** surfaces here | renner_depot 09–18 |
| 2 | **cap_renner_noticed** | L4 auto-fire | entry + `npc_renner.relation ≥ noticed-tier` + guard `renner_office_open` is_false → **SETS `renner_office_open`** | renner_depot |
| 3 | **hub_anchor_renner** | L1 hub | unconditional; light off-duty/drunk register | the_anchor 19–23 |
| 4 | **rung_renner_tease** | L1 rung | `renner_office_open` + corruption ≥ tease-tier; locked-visible; reaction-band [group] | office register |
| 5 | **rung_renner_flash** | L1 rung | + corruption ≥ flash-tier → **SETS `renner_flirts_back`** at the band | office register |
| 6 | **rung_renner_grope** | L1 rung | + corruption ≥ grope-tier + `renner_flirts_back` | office register |
| 7 | **rung_renner_fuck** | L1 rung (loop entry) | + corruption ≥ sex-tier + `renner_oral_once` → **SETS `renner_fucked_once`**, resets loop traits, routes into the loop | office register |
| 8 | **work_depot_haul** | L3 host | ungated; +relation (+3) +credits, costs charge + time (no daily cap; paced by the 09–18 window); **SETS `worked_renner_once`** on first completion (sole owner) | renner_depot |
| 9 | **walkin_renner_depot** | L3 walk-in | substitution of #8; **rising bands 10/35/70%** on his corruption (lingers → crowds → pulls off the task) | renner_depot |
| 10 | **amb_renner_anchor_ruin** | L2 ambient | random ~25%, requires_npc; tiered [group] on his corruption (the ruin showing) | the_anchor 19–23 |
| 11 | **amb_renner_cheerup** | L2 ambient | `renner_office_open` + corruption floor + low chance; scaled by spine flags (tease / blow / take it) | the_anchor 19–23 |
| 12 | **loop_renner_office_sex** | sex-loop | triggerless; poses oral→vaginal→anal (anal gated corruption ≥ anal-tier); pleasure climb; climax-elect ≥ 50 | office register |
| 13 | **loop_renner_finisher** | sex-loop | [group] by `sex_finisher_type`; inside/oral → reset + exit; **anal → control canvas** | office register |
| 14 | **renner_control_canvas** | control | the drain — payload prose (no flags; triggerless); reached from the capstone (first) + the loop (repeat) | office register |
| 15 | **cap_renner_hired** | L4 auto-fire | first depot entry + `opening_done` + guard → **SETS `renner_hired`** | renner_depot |
| 16 | **cap_renner_blowjob** | L4 capstone | office + corruption ≥ blow-tier + `renner_flirts_back` + guard → **SETS `renner_oral_once`** | office register |
| 17 | **cap_renner_anal_drain** | L4 capstone | `renner_fucked_once` + corruption ≥ anal-tier + guard → **SETS `renner_drained` + `renner_leads_extracted` + `renner_anal_once`**, routes into the control canvas | office register |
| 18 | **ma_renner_blowjob** | L4 auto-fire | next day: `renner_oral_once` + `days_since_flag ≥ 1` + guard → bumps his corruption | renner_depot/office |
| 19 | **ma_renner_anal** | L4 auto-fire | next day: `renner_anal_once` + `days_since_flag ≥ 1` + guard → bumps corruption to the ceiling band | renner_depot/office |
| F1 | **inv_facility_explore** | L3 host | ungated investigation; accrues lead evidence | facility_ruins |
| F2 | **inv_facility_match** | L4 auto-fire | entry + `renner_hired` + guard → **SETS `facility_match_seen`** (the "that's mine" seed) | facility_ruins |

**The sex loop + drain (the reusable pattern's first build).** Triggerless, node-routed from "Fuck him." State
is **numeric traits only** — `sex_stage` (0 oral / 1 vaginal / 2 anal), `loop_npc_pleasure`,
`sex_finisher_type`, `anal_active`, `sex_entry_origin` — all in `[player.core_traits]`, hidden, **reset to 0
on entry AND on every finisher exit**. Poses raise pleasure; the climax-elect (≥ 50) sets the finisher type;
the **anal elect is itself gated `anal_active` ≥ 1** (so you can't pick the ass finish from the oral pose).
Inside/oral finish → reset + exit. **Anal finish → the control canvas (the drain).** The drain's flags are set
on the **located capstone (#17)**, never on the triggerless canvas — copy this discipline to every future
target.

**Flag chain (acyclic; each flag one located setter; every condition block `version="1.0"`):** `opening_done`
→ `renner_hired` (#15) → `worked_renner_once` (#8, sole owner) → `renner_office_open` (#2) →
`renner_flirts_back` (#5) → `renner_oral_once` (#16) → `renner_fucked_once` (#7) → `renner_drained` +
`renner_leads_extracted` + `renner_anal_once` (#17). No corruption cooldown flag — the charged rungs are
throttled instead by their **cost** (15 Charge + 180 min each) against the **09:00–18:00 office window**
(~3/day), and the bar is the ×2.5 ladder (drain `corruption ≥ 50`, office `relation ≥ 21`).

**Frontier (telegraphed, deferred — never silent).** The drain sets **`renner_leads_extracted`** → opens
Bastien (`bastiens`) + Calloway (`vance_securities`); their on-ramps render greyed citing "Renner's leads"
until then. Mercer's "Report" reads `renner_drained` for his debrief. `renner_leads_extracted` is one lead
toward unlocking **the_site** (the chip). The facility match + the drain payload are Renner's "wrong-note"
toward the first crack in "evil rogue." All seeded, none built — blueprinted when their Step-4 design exists.

---

### World blueprint (Pass 3)

> Mostly consolidation — the schedules + ceilings fell out of the NPC passes; this pass places them on the map,
> settles the systems, and fixes the engine container double-print. **Map scope (LO): build the chunk's ~11
> locations; leave Mid-City + the other venues frontier** (build-order, not a cut — the city breathes more as
> Missions 2/3 land).

**The chunk's map (built):**
- **THE SPIRE** — `spire_plaza` (street hub / travel anchor) · `vance_tower` → `atrium` · `penthouse` (Mercer)
  · `wren_floor` → `wren_room` → `cradle` (her hub).
- **THE REACH** — `the_waterfront` (street hub / travel anchor) · `the_anchor` (Renner, evenings) ·
  `renner_depot` (Renner, days + the folded office register) · `facility_ruins` (investigation).

**Location tags (the dead-room gate).** The four **containers** — `loc_spire`, `vance_tower`, `wren_floor`,
`loc_reach` — are pure-nav (default_entry set, host no canvas, exempt). The **standing hubs** all earn their
click: `penthouse` (Mercer), `cradle` (her), `the_anchor` + `renner_depot` (Renner), `facility_ruins`
(investigation), and `spire_plaza` + `the_waterfront` (each hosts the travel-bridge activity). `atrium` is a
**named threshold** (the gate between the cage and the street) — a deliberate thin pass-through; its ambient
corporate life is a telegraphed frontier seed, not a silent dead room.

**Frontier (NOT built; telegraphed where it counts):**
- `the_site` — a **locked-visible nav card** in the Reach ("unlocks on enough leads" — the chip / Phase-1 end).
- `bastiens` (Mission 2) + `vance_securities` (Calloway / Mission 3) — **greyed seeds** that light when
  Renner's drain sets `renner_leads_extracted` (exact telegraph form settled at authoring).
- All of **Mid-City** (`the_strip` · `mirage` · `the_cordon` · `the_long_hour`), `the_eyrie`, `lab` (Pell),
  `units_quarters` — pure frontier (no chunk content; built with their mission/Act content, not as empty rooms).

**Schedules (5D):** Mercer `penthouse` 08:00–23:00 (offscreen overnight) · Renner `renner_depot` 09:00–18:00 +
`the_anchor` 19:00–23:00 (offscreen overnight) · player day-router at `cradle` 19:00–05:00. The nav paints each
NPC where he's scheduled.

**Ceilings (5B — author-encoded in `conditions`, no location attribute):** depot floor = **public/work only** ·
the office register = **the full ladder** · penthouse = Mercer's domain · cradle / wren_room = her space (the
invasion intrudes) · the Anchor = public (witness + cheer-up) · facility_ruins = investigation.

**Systems (5F):**
- **Phone** — Mission 1's morning briefing (the Renner tip); minimal in-chunk.
- **Money** — credits (Renner depot income, the only source); the disguise shop + Pell's upgrades are frontier
  sinks (Player blueprint).
- **HUD** — Charge + Credits only (band text per `0_systems`). **Quest card** — Mission 1: get close → drain →
  extract the leads (shows while `mission_1_active` && !`renner_drained`).
- **Clothing** — **a worn-state cover system** (added during authoring — full spec in *## The cover / disguise
  system*). The company **issues** the Mission-1 cover (no shop — the boss provides it); she equips it at the
  rack (`wren_room`) before a mission, and the Renner surfaces gate on `clothing_item … equipped`. Out of cover
  → the mark reacts wrong (no hire / suspicion). ("Commando" still lives in the flash rung's text.) Per-mission
  covers for Bastien/Calloway stay frontier (granted as their missions open, tagged by `worn_type`).
- **Customization** — none (fixed identity). **Shared-private peep/occupancy (5H)** — **none** (the invasion is
  a scripted intrusion, not a co-presence mechanic).

**Access + travel (5G):**
- **Travel-friction:** `spire_plaza` ⇄ `the_waterfront` is the one bridge — it `costs` time + a little Charge;
  fast-travel once a place is known. The cost is what makes Renner's daytime schedule bite.
- **The container double-print FIX** (the audit's engine bug — children printed twice): **drop the
  `is_container` district-wrappers entirely; build the map as NON-container standing hubs** — the shipped
  `late_shifts` pattern: two parallel top-level street-hub roots (`spire_plaza` / `the_waterfront`, no
  `entry_from`) bridged by the travel activities, venues nested via `entry_from` + `navigation_order`.
  Containers were the cause (they double-print AND swallow attached canvases); the non-container shape
  sidesteps both. **Verified clean at beat_0001** — each child renders once. (Supersedes the earlier
  `default_entry`-on-containers idea — engine-forced, see ledger turn 22.)
- **Locks as prose:** `the_site` carries `entry_conditions` + `blocked_message` (`version="1.0"` or it fails
  open); the office register's access is the `renner_office_open` gate, not a hard door (Fork A fold).

**Reachability (the triad holds):** each scheduled NPC has a presence-floor hub where he's scheduled; she
reaches the Reach via the travel bridge after the cradle day-reset; the daytime/evening windows overlap her
waking hours. ✓

---

### Wiring, opening & plan (Pass 4)

**The chunk DAG — it closes.** One spine, a few cross-reads; acyclic, every gate has a reachable setter, every
cross-arc reach telegraphed. *(rev 41: the drain flags now set inside the triggerless office loop, not a located
capstone; the one trigger that read `renner_drained` — glitch II — is re-gated onto the `drains_done` trait so the
flag-chain validator stays green.)*
- **Spine (monotone):** `opening_done` → `renner_hired` → `worked_renner_once` → `renner_office_open` →
  `renner_flirts_back` → `renner_oral_once` → `renner_fucked_once` → `renner_drained` (set on the loop's first
  equipped+charged anal finish, with `renner_leads_extracted`; `renner_anal_once` sets on anal-pose entry).
  Mercer's `mercer_hub_open` (first service) runs independent of the spine.
- **Cross-reads (the one-world seam — all one-directional reads, D2-safe):**
  - `worked_renner_once` → player **glitch-recurrence I** (cradle) + arms Mercer's **first invasion**.
  - `drains_done` (trait, +1 per drain) → player **glitch-recurrence II** (cradle); `renner_drained` (flag) →
    (frontier) Mercer's **debrief**.
  - `renner_leads_extracted` → (frontier) the **underworld trail** + the_site lead-count (Bastien/Calloway
    retired as named on-ramps — D2). The frontier reads render as greyed seeds (D3).
- **D1 (cold-start):** the opening runs from boot → the city opens; Renner's hire (first depot visit) +
  Mercer's hub (first penthouse visit) are the ungated on-ramps; the cradle is always reachable.
- **The core loop:** cradle reset → out (work → seduce → drain Renner) → back (serve Mercer) → cradle (the
  glitch waits) → repeat. The drain is the chunk's climax.
- **Fail-state:** none in the chunk (Charge = soft pace). **Supply→demand:** dissolved — no player-corruption
  door, so every NPC rung self-supplies via his own traits.

**The opening — its real node structure (~23 clicks, one beat per click).** Authored as **fine cascade beats**
in the three beat-canvases (one paragraph or one exchange per click, 2-sentence cap — the fix for the prior
collapse):
- **Beat 1 — the office (~12):** line-up · accusation · threat · she begs · verdict ("the Chairman's
  investment") · punishment set-up · punishment ×3 (he takes her → the act → the units blank) · gratitude ·
  reassignment (the units + her job + the mission lie) · dismissed. *Plants the freeze as the first glitch.*
- **Beat 2 — the night (~7):** walk back · the cradle · the tears · the memory fragment · the catechism · the
  power (never works on the boss) · power-down. *Plants the awakening + the boss-immunity.*
- **Beat 3 — the morning (~4):** power-up · the briefing · the tip (Renner @ the Anchor) · **out the door**
  (the hinge). *Sets `opening_done` + `mission_1_active`; the city opens; hands to Renner.*

**The build plan (seeded — Step 7 authors one beat per turn, green each time):** 14 beats —
scaffold → opening (×3) → home base (Mercer + cradle) → Renner (×6) → texture → glitches/facility → verify.
Full ordered list in `authoring_state.json` `plan`.

---

### Underworld Hunt blueprint (Act-2 on-ramp — Step 5, rev 53)

> The locked six-beat hunt (full record: `design_analysis_underworld_hunt.md`; casting rev 52) compiled to the
> buildable scene list. **Structure only — no story beyond the lock.** This chunk *reveals* Bastien; his arc is
> the next chunk. Build law: shipped game = **extend-only** (no id/key/scale/title rename); `version="1.0"` on
> every new `conditions`; the gate marker `names_known` is a **TRAIT** (the drain setter is triggerless — the
> flag-chain validator would hard-fail a flag there); Sunday = a canvas `trigger.schedules weekdays=[6]`, **not**
> a declared `[[npcs.schedules]]` row (which would leak Marsh onto the Schedule page from Day 1).

**The scenes**

| # | Scene | Location | Lane | Gate | Sets | Media |
|---|---|---|---|---|---|---|
| 1 | Two names (drain extension) | `renner_control_canvas` (`.intro` + `.again_ask`) | drain payload (existing) | — (it *is* the drain) | `names_known`=1 (trait) on **both** `loop_renner_finisher` drain choices | reuse drain scene |
| 2 | The lead | `the_anchor` (Sol tends it) | Lane 1 talk | `names_known ≥ 1` | `hunt_lead` | the_anchor.jpg + Sol |
| 3 | Sunday at The House | `underworld_brothel` | scripted one-off + `trigger.schedules weekdays=[6]` | `hunt_lead` + drain worn (`equipped_weapon=1`) + charged (`drain_charge≥1`) | `crew_known` (+ `rue_met`) | brothel serve/drain clip |
| 4 | The crew's place | `crew_den` (**new**, off `underworld_strip`) | Lane 1 search | `crew_known` | `bastien_found` | ransacked hideout |
| 5 | The grab (capstone) | `crew_den` | Lane 4 auto-fire (`priority≥9`, `is_repeatable=false`, **bare** — no `npc=`/`requires_npc`) | `bastien_found` | `bastien_revealed` → chunk ends | grab / face-to-face |

**The chain (DAG — linear, acyclic, cold-start-reachable):**
`drain → names_known (trait) → [Anchor] Sol → hunt_lead → [House · Sun] pay Rue ~25 coin + serve+drain Marsh → crew_known → [crew_den] search → bastien_found → grab capstone → bastien_revealed`.
Entry = the drain (both new **and** returning players reach it; returning players re-drain via `.again_ask`). Every setter is located **except** `names_known` (trait, on the triggerless drain). No cycle; no cross-arc mutual lock; every gate telegraphed.

**Placement / mechanism notes**
- **Sunday is real, not faked.** The engine tracks weekdays (`time_state.current_day` cycles Mon–Sun; `advanceDay` `% 7`); the House beat carries `trigger.schedules weekdays=[6]` so it fires only Sundays. She sleeps (Power down) to reach Sunday; a locked-visible telegraph ("Marsh — The House, Sundays") on the quest/nav tells her when to come.
- **Marsh is NOT a scheduled NPC** — he's the Sunday canvas, so no `[[npcs.schedules]]` row and no Schedule-page spoiler. One-off: serve → drain → spent; no relation/corruption ladder (a service NPC given a corruption arc is the anti-pattern).
- **Rue pay-off = the coin's first real sink** (~25 coin; today coin only pays the 5-toll at the gate). She persists after as a light wary face at the brothel (`rue_met`).
- **`crew_den`** = a new room off `underworld_strip` (sibling of brothel/pit/market); content floor = the search + the find + the grab (earns its click). The old `bastiens` shell stays parked for Bastien's own domain (next chunk), not spent here.
- **The grab capstone** ends the chunk on Bastien's question hanging — nothing past the lock. **No new fail-state** (the capture is scripted, not a game-over).

**Plan seed:** `beat_0030` (names) · `beat_0031` (Sol lead) · `beat_0032` (Sunday House — Rue + Marsh) · `beat_0033` (crew_den) · `beat_0034` (grab capstone). All `status=planned`, `target_phase=2`.

### Captivity blueprint (The Room — Step 5, rev 63)

> The locked story (`## Captivity — The Room`, rev 62) compiled to the buildable scene list. **Structure
> only.** Build law: shipped game = **extend-only**; `version="1.0"` on every new `conditions`; the cell door
> is gated on a **TRAIT** (`cell_door`), never a flag — a flag `is_true` gate demands a located setter or the
> flag-chain validator hard-fails. One engine change (`Config.history.controls = false`).

**The ladder.** `+12` strain per use · 8 uses · the break at `>= 96` · `clamp = true` bounds it 0–100 and it
freezes at 96. Each scene gates on the band it is **about to be played in**, so the sidebar row the player is
staring at names the shelf that comes next — the read-out becomes a countdown.

| Sidebar row | Band | The shelf it predicts | Scene gate | Scenes |
|---|---|---|---|---|
| *(hidden)* | 0 | Nominal | `lt 24` | 1 · 2 |
| `Core: Nominal` | 1–23 | Hot | `gte 24` `lt 48` | 3 · 4 |
| `Core: Hot` | 24–47 | Faulting | `gte 48` `lt 72` | 5 · 6 |
| `Core: Faulting` | 48–71 | Failing | `gte 72` `lt 96` | 7 · 8 |
| `Core: Failing` | 72+ *(no `max`)* | — | `gte 96` | **the break** |

**Days are emergent, never named.** Sleep guarantees ≥1 use a night; `attend` adds more. Attend and she
breaks in ~3 days; hide in the bed and it takes ~8. **Hiding doesn't save her — it makes it last longer.**
No prose in the chunk names a day count.

**The scenes** — all at `captive_room`, `trigger_mode="random"`, `is_repeatable=false` (**one-shot: the
engine retires a non-repeatable canvas after one fire, and auto-fire skips random-mode canvases — so no
per-scene "seen" flags exist**), `chance=0.5`, `+12 core_strain` / `−energy`, both `clamp=true`. Bastien in
every one, in `dialog`; the crew in quoted lines inside `paragraph` blocks (a `speaker="unknown"` dialog
block renders a literal `Stranger:` label). Mechanism = Lane 2 random ambient. **Register (rev 64): each
scene is a scripted, multi-beat, pure-witness chain — approach → strip → inspection → the acts → finish →
read-out, advanced on `Continue`, one clip per beat, no player agency (rape doesn't start at penetration; the
helpless click is the point). The men's voices are hot and degrading; Wren's interior stays rationed to one
clipped `thought_bubble` per scene — the contrast is the horror. NOT the flat one-clip captions of the rev-63
draft.**

| # | Scene | Shelf | The want | Media |
|---|---|---|---|---|
| 1 | **The inventory** — order-and-strip, invasive inspection (fingers in cunt+ass, the empty socket, spit in her face), forced deepthroat, cunt over the table, ass — the socket-loss, finish + read-out | Nominal | know what he bought | `cell_inventory` + new |
| 2 | **Charge test** — he forces her to come to move the read-out, degrades her for creaming on his hand, edges + slaps her, "again" | Nominal | weaponise her own body | `cell_charge_test` + new |
| 3 | **The first three** — three of the crew, manhandled and spat on, spitroast → DP, they finish on/in her; Bastien seated, noting the number | Hot | survive the pack | `cell_first_three` + new |
| 4 | **Turns** — a timed queue, passed down the line, ass — the drain inverted, used and pissed on | Hot | the drain, inverted | `cell_turns` + new |
| 5 | **The frame** — strapped into a rig, positioned/"tuned" between uses, used cunt+ass down the line, marks | Faulting | be a thing being operated | `cell_frame` + new |
| 6 | **Overflow** — legs held open, forced orgasm that HURTS (the charge overflows), the crew laugh, Bastien watches the meter | Faulting | feel the overload | `cell_overflow` + new |
| 7 | **The stutter** — used from behind, her leg dies mid-fuck, he hooks the limp leg and keeps going, Bastien leans in | Failing | the body quits | `cell_stutter` + new |
| 8 | **He does not stop** — she's failing and lit up, a crew man balks, Bastien orders them on, turned over and used past failure → the break | Failing | **earns Cain's anger** | `cell_he_does_not_stop` + new |

Scene 8 is a sex scene **and** the moral hinge of Bastien's arc, deliberately: it must cost him something to
be *watched* doing it. That's what the next chunk's bombshell hangs on.

**The two verbs**
- **Sleep** — repeatable, **no schedule**. Day advance · `energy +100 clamp=true` (the `activity_recharge`
  shape) · a **scripted, guaranteed night use**: `+12 core_strain` with band-selected prose via `group`
  blocks. Not random, so it **bypasses the visit-cooldown**. Sleep cannot outrun the ladder.
  *(Engine-forced, bounced up at `beat_0038`: the cradle's sleep is gated 19:00–05:00, but nothing in the
  cell is schedule-gated and the cell has no windows. A night window would strand a player grabbed at
  09:00 behind ~20 `attend` clicks just to reach bedtime. She sleeps when she wants; the day still rolls.)*
- **Attend** (~30 min) — three exits, the only things in the room with edges: *listen at the door* · *watch
  the man on the chair* · *hold still and feel the fault*. **Glitch III** rides the last one inside a `group`
  gated `glitch_iii_seen is_false`; the choice sets the flag, so the Tier-3 spend fires **once** on a
  repeatable verb. Returning from `attend` re-enters the room ⇒ a fresh roll. *That is the chance mechanic.*

**The chain (linear, acyclic, both cohorts reachable):**
`bastien_found → the grab (rewritten: no release) → captivity_entered + equipped_weapon=0 → [cell] 8 uses ×
+12 → core_strain ≥ 96 → the break (captivity_broken) → Cain: the argument behind the door → the release
(captivity_done, equipped_weapon=1, loop traits reset) → the_waterfront.`
Returning players already hold `bastien_revealed` and stand on the waterfront ⇒ a **recovery auto-fire**
there (`bastien_revealed is_true` + `captivity_entered is_false`) is mandatory, or they never reach the
chunk. **Two doors, one room.**

**Structure amendments (whole):**
- **Locations** — `captive_room` (**no `entry_from`, no `parent`**; teleport-only. A `parent` here silently
  unseals it and the build stays green) + `captive_door` (`entry_from = captive_room`, `entry_conditions`
  `cell_door gte 1` — never satisfied). The door's real job is to give the room a **non-empty nav**, or the
  generator falls back to listing the whole map.
- **Traits** — `core_strain` (0, hidden, the banded row) · `cell_door` (0, hidden, never set).
- **Flags** — `captivity_entered` · `captivity_broken` · `captivity_done` · `glitch_iii_seen`.
- **NPCs** — none. `npc_bastien` already exists (minimal, **no schedule** — correct). The cell must **not**
  use `npc =` / `requires_npc`, which gate on a schedule he doesn't have.
- **Quests** — the shipped end-of-content card fires on `bastien_revealed is_true`, which the rewritten grab
  still sets *on the way into the cell*; it is upper-gated with `captivity_entered is_false`, a captivity
  card takes the page, and a new end card seeds the repair chunk **locked-visible**.

**Plan seed:** `beat_0035` (engine + systems) · `beat_0036` (geography) · `beat_0037` (entry + the two
doors) · `beat_0038` (the two verbs + Glitch III) · `beat_0039` (scenes 1–4) · `beat_0040` (scenes 5–8) ·
`beat_0041` (the break) · `beat_0042` (Cain + the release) · `beat_0043` (quests) · `beat_0044` (dev jumps +
clean publish). All `status=planned`.

### Salvage blueprint (The Repair — Step 5, rev 65)

> Full record: `games/vesper/design_salvage_the_repair.md`. Six forks locked with LO 2026-07-15. The chunk
> after captivity — pays the frozen `Core: Failing` promise, turns the rescuer hook into play without
> spending Cain, re-launches at Calloway. **~8–10 canvases, a bridge, not a mission.**

**The verb — supplicant / test-bench.** The first NON-conquest: she works no target, she *needs*, is worked
*on*, and the bodies the world brings are **live tests for the weapons Kess rebuilds in her.** Distinct from
seduce-in / scheme-and-serve / she-is-taken / domme.

**The staged beat chain (LOCKED).** Kess repairs in **stages**; each stage fixes a system, then a body tests
whether the weapon/function fires. **Count-locked 2–3, `is_repeatable=false`** — the grind-guard (staged +
distinct = the point; a repeatable repair→test loop re-ships the exact review, applied once on the terminal
exit only).

1. **Beat 1 — the body won't hold** (auto-fire @`the_waterfront`, gated `captivity_done is_true` +
   `salvage_entered is_false`). Two loop-attempts break *on input*; can't report (refit = wipe); the
   don't-report choice sets `salvage_entered` → the berth opens. Lane 4 (capstone-shape).
2. **Beat 2 — finding Kess / the terms** (@`kess_berth`, per `npc-intro.md`). She seeks; Kess nearly ejects
   her, then flips greedy at the read (**custom/bespoke, never "old/decommissioned"**). Terms: staged, each
   stage costs `coin` (untraceable) → she's short → `kess_debt` accrues. Lane 1 hub-shape.
3. **Stage A — core & charge (Tier-3)** (@`kess_berth`). The seam + the forensic read + the involuntary
   glitch-leak (reuses `beat_0042` devices; name-syllable off-page; sets NO chip fragment) + the reach-and-
   fail. **Test: charge on Tolly.** `core_strain` eases; `kess_debt += cost`. Lane 4 (the leak) / Lane 1 (test).
4. **Stage B — the drain (the clue)** (@`kess_berth`). Drain re-check → **test: the drain fires on the anal
   finish with Reeves (a Vance courier); the payload drops "the build-files are in Calloway's file room."**
   The weapon-test IS the intel beat (canon: an anal finish is how the drain *takes*). `kess_debt += cost`.
   Lane 1. **Stage C (emitter)** = a light follow only if it earns its canvas, else folded here.
5. **The verdict · Core: Locked** (@`kess_berth`, one-shot). `core_strain`→0 (Failing clears), `core_sealed=1`
   (Locked row lights), the "you need your own build file — and Vance keeps those classified" line; she
   **walks owing** the `kess_debt` balance. Lane 4 (Tier-3 end card).
6. **Re-launch → Calloway** (Mercer's Mission-3 dispatch; the sandbox re-opens, private want + order at one
   address). Lane 1.

**Gates & state (extend-only).**
- **Traits (new, hidden):** `core_sealed` (0→1; drives the "Core: Locked" `trait_status_text` row, bands from
  `min=1`) · `kess_debt` (0; accrues per stage). **No new "want" trait** — the awakening stays still.
- **Flags (new):** `salvage_entered` · per-stage progress (`salvage_stage_a_done` · `salvage_stage_b_done`) ·
  `salvage_done` · `mission_3_active` (flipped at the verdict → the Calloway Story-Goal card).
- **Location (new):** `kess_berth` (`entry_from = the_waterfront`; ordinary — no seal, no captivity machinery).
- **NPC (new):** `kess` (portrait, berth; NOT a conquest — no relation/corruption climb; recurs as the debt-
  holder). Tolly + Reeves = canvas-local **test-bodies**, no `npc_` objects.
- **Meter mechanic:** `core_strain` band table 1–71 is fully occupied, so the flip = relieve to 0 (Failing
  vanishes: renderer emits nothing at no-match) + the new `core_sealed` row. Additive; honors "no cure
  shipped" (the sealed partition stays Locked; only the Site opens it).
- **Every new conditions block carries `version="1.0"`; new gates are traits, not triggerless flags.**
- **Reset the shared sex-loop traits** (`sex_stage`/`loop_npc_pleasure`/`sex_finisher_type`/`anal_active`/
  `sex_entry_origin`) on entry & exit of each Salvage sex scene, or state bleeds into Marsh/Renner loops.
- **Save-safety:** old-save cohort (`captivity_done`, `core_strain=96`, no `core_sealed`) enters via the same
  gate; the Failing row rides until they play it.

**Media:** Kess portrait · the Stage-A seam · the Tolly charge-test · the Reeves drain-test · (emitter). The
clinical/opened-up look is thin on the standard harvest → some scenes go text-forward or machine-framed;
`search_queries` written at authoring; engine silent-skips missing clips.

**Step-6 resolutions — the authoring contract** *(full record: `design_salvage_the_repair.md` §18)*
- **Stage DAG (pinned; `is_repeatable=false` alone does NOT sequence).** Beat 1 = auto-fire @`the_waterfront`,
  HIGH priority, `captivity_done is_true` + `salvage_entered is_false`, **single-exit** (forced don't-report),
  **self-contained** (narrates the failed loop-attempts — does NOT edit the live Renner/Mercer canvases).
  Stage A = `salvage_entered is_true` + `salvage_stage_a_done is_false` · Stage B = `salvage_stage_a_done
  is_true` + `salvage_stage_b_done is_false` · Verdict = `salvage_stage_b_done is_true` + `salvage_done
  is_false`. Each `_done` set on the terminal exit → a strict DAG.
- **Voice carriage — present bodies SPEAK** (the captivity crew-narration exemption does NOT transfer; it
  rode on dissociation, now gone). beat 2 / Stage-A Kess reads / Stage B / verdict = **PLAYED** (≤1.5:1;
  >3:1 FAILS). Kess's clinical reads ARE his lines; **Reeves says where the files are** (spoken, not
  narrated); Tolly = one terse line; test-bodies render `speaker="unknown"` → "Stranger:". Narrated
  exemptions: the Stage-A leak, beat 1 (solo), interior end-cards.
- **Berth lifecycle — CLOSE-after (no dead room).** `kess_berth entry_conditions = { salvage_entered is_true
  AND salvage_done is_false }` + `blocked_message` (locked-visible after); the verdict teleports to
  `the_waterfront`. Kess carries **no schedule** (no Schedule-page leak).
- **Coin NEVER blocks.** Stages gate ONLY on `salvage_stage_*` flags; cost always accrues to `kess_debt`,
  never a `costs`/payment gate (kills the return-to-earn loop).
- **Sandbox SOFT-OPEN** — no retro-gating shipped loops; the "can't operate broken" fiction is held
  beat-1-local. (Declared **§2F lean:** the single-thread repair window is thin ON PURPOSE.)
- **Register wall** — reuse the leak's DEVICES, not `beat_0042`'s periodic cadence or its Rule-5-banned "the
  way you'd…" similes; Kess's reads stay terse spoken clinical.

**Plan seed:** `beat_0046` (engine + systems) · `beat_0047` (geography) · `beat_0048` (Beat 1) · `beat_0049`
(Kess intro + terms) · `beat_0050` (Stage A) · `beat_0051` (Stage B [+ C]) · `beat_0052` (the verdict) ·
`beat_0053` (re-launch) · `beat_0054` (quests re-gate) · `beat_0055` (clean publish 0.1.4). All
`status=planned`. *(0045 is the parked captivity undo-hatch — not a Salvage beat.)*

---

### The Archive blueprint (Step 5, rev 69)

> ⚠️ **SUPERSEDED 2026-07-22 — see `games/vesper/design_beat_archive_v2.md` (authoritative).** The Archive 1a was fully redesigned: **copies-not-theft** (Vane→Colm→Bastien), detection via the case-work + a cold Colm drain (no gadgets), docs = her build file (Vance humanoid records), blackmail-Vane retrieval, the watcher-flush + Mercer-panic ending. The bug/theft/overhear tables below are the OLD design, kept for reference only.

> Full record: `games/vesper/design_beat_archive.md` (spine + cast + locked rules + canon anchors). **Fork A
> locked with LO 2026-07-21.** Two chunks — **1a The Archive** (topside/Calloway; **build first**) and **1b The
> Deal** (underworld/Bastien; second). Entry **extends the shipped `salvage_relaunched` re-launch** (Mercer's
> Calloway / Vance-Securities dispatch, `5_scenes.toml:5182`, line `:5208`); extend-only, no shipped byte
> retouched. Built across passes — **Calloway + Vane here (Pass 2)**; the bug/theft world + the Bastien-overhear
> + the Quests page (Pass 3); the DAG + the plan seed `beat_0056+` (Pass 4). Estimate ~1a: **~16–18 canvases.**

**The verbs.** 1a = **seduce-in on the belief-lever** (Calloway) + **investigate** (the bug-trace + the
Bastien-spying). 1b = the collision/reveal + the trade. Calloway = the roster's return to conquest; Vane =
mercenary asset (no conquest, no meters).

**Calloway spine — two axes on HIS meters (the Renner double-lock, reused).** She has no corruption door (dead),
so both axes are Calloway's own: **AXIS 1 — belief/access** = `npc_calloway.relation` (an odometer built by the
*ungated* believe-him beats + the bug proposal) earns his openness; **AXIS 2 — surrender** =
`npc_calloway.corruption` (+N per charged rung) gates the lewd rungs; `npc_calloway.arousal` = the loop throttle
only (never gates progression). Every lewd rung double-locks on **belief-open (access) + his corruption (the
tier)**. **Pacing: belief-fast** (he opens quickly — starving to be believed), **surrender a paced campaign**
(×2.5). The **one hard throttle** is diegetic — the *he-flinches* beat (the paranoia of the disbelieved man)
gates the full surrender behind a non-lewd re-anchor, plus each charged rung costs Charge + time against the
file-room window (caps rungs/day, à la Renner). No daily-flag cap.

**The scenes (1a · Calloway):**

| # | Scene | Lane | Gate | Place |
|---|---|---|---|---|
| 1 | **cap_calloway_meet** | L4 auto-fire | entry `vance_securities` + `salvage_relaunched is_true` + guard `calloway_met is_false` → **SETS `calloway_met`** | vance_securities |
| 2 | **hub_calloway_fileroom** | L1 hub | `calloway_met`; `npc=npc_calloway` (portrait); two ungated relation feeders — "Talk to him" (+2) + "Work the case" (+3, the analyst cover-work) — into the belief/access odometer, + the file-room register | vance_securities (window) |
| 3 | **cap_calloway_bug** | L4 capstone | `calloway_met` + `npc_calloway.relation ≥ believer-tier` + guard → she pitches the tracker; he approves → **SETS `bug_planted` + `calloway_believes`** (access) | vance_securities |
| 4 | **rung_calloway_contact** | L1 rung | `calloway_believes` + corruption ≥ contact-tier; locked-visible; reaction-band [group] | file-room register |
| 5 | **rung_calloway_oral** | L1 rung | + corruption ≥ oral-tier → **SETS `calloway_oral_once`** | file-room register |
| 6 | **cap_calloway_flinch** *(THROTTLE)* | L4 capstone | `calloway_oral_once` + corruption ≥ flinch-tier + guard → the disbelieved man pulls back; she re-anchors belief → **SETS `calloway_flinch_resolved`** (non-lewd; the one hard gate) | file-room register |
| 7 | **rung_calloway_fuck** | L1 rung (loop entry) | `calloway_flinch_resolved` + corruption ≥ sex-tier → **SETS `calloway_fucked_once`**, resets loop traits, routes into the loop | file-room register |
| 8 | **loop_calloway_sex** | sex-loop | triggerless; poses oral→vaginal→anal (anal gated `anal_active`); pleasure climb; climax-elect | file-room register |
| 9 | **loop_calloway_finisher** | sex-loop | [group] by `sex_finisher_type`; inside/oral → reset + exit; **anal → the drain canvas** | file-room register |
| 10 | **calloway_drain_canvas** *(the two drains live HERE)* | control (triggerless) | reached from the anal finish; payload + counter bump by `calloway_drains_done`: **0** → *surface: "where's it kept?"* → he's certain it's safe (bump → 1) · **1** → *depths: already gone, lifted days ago, an inside job, her file in it* (bump → 2) · **≥ 2** → done. The counter is a **trait bumped here** (validator-exempt); **no flag is set on this canvas** | file-room register |
| 11 | **cap_calloway_reported** *(1a end)* | L4 auto-fire | entry `vance_securities` + `deal_place_known is_true` (she's gone with the trail) + guard `calloway_reported is_false` → he does the math, turns nemesis, reports the analyst → **SETS `calloway_reported`** (the 1b fuse) | vance_securities |

**The sex loop + the two drains (Renner's pattern, reused; two payloads by a durable counter).** Triggerless,
node-routed from "Fuck him." State = numeric traits only (`sex_stage` / `loop_npc_pleasure` / `sex_finisher_type`
/ `anal_active` / `sex_entry_origin`), hidden, **reset to 0 on entry AND on every finisher exit** (or state
bleeds into the Renner / Marsh / Salvage loops). Anal finish → the drain canvas (#10). **The two drains differ
only in payload, selected by the hidden counter `calloway_drains_done`** — and the counter is a **trait bumped
on the triggerless finisher** (traits are exempt from the flag-chain validator; this is the *actual* Renner
discipline — Renner bumps `drains_done` inside the loop, **never** a flag; a flag required `is_true` by a
trigger but set in a triggerless canvas HARD-FAILS the build). Advancing to payload 2 (the big pull) needs only
the counter (`calloway_drains_done == 1`) — the big theft happened days before, off-screen, so there's no theft
beat to gate on. Everything **downstream** (W4, the "find the buyer" Quest card, the betrayal #11 via
`deal_place_known`) reads the **durable trait `calloway_drains_done >= 2`**, never a flag set mid-loop. Gated on
the **counter + corruption band, never arousal** (resets at climax). After counter 2 the extraction is done.

**Calloway gates & state (extend-only).**
- **NPC (new):** `npc_calloway` (portrait hub @`vance_securities`; the standard relation/corruption/arousal
  triad — corruption **is** the seduction ladder, à la Renner). **`npc_vane`** — minimal, a 1b dialog speaker;
  schedule-less (hidden); no hub, no meters.
- **Trait (new, hidden):** `calloway_drains_done` (0 → 2; gates the two drain payloads; the Renner `drains_done`
  twin — a **counter, not a triggerless flag**).
- **Flags (new):** `calloway_met` · `bug_planted` · `calloway_believes` · `calloway_oral_once` ·
  `calloway_flinch_resolved` · `calloway_fucked_once` · `calloway_reported` (the 1b fuse; set at #11 on
  `deal_place_known`). Each with **one located setter**, acyclic. **The discovery is a TRAIT, not a flag** —
  downstream reads `calloway_drains_done >= 2` (there is **no** `big_chunk_known` flag: a flag set mid-loop would
  hard-fail the validator).
- **Location (new):** `vance_securities` (topside/Spire; a **registered frontier stub** + named in prose — **no
  TOML location object yet**, so a clean new build; re-spec'd `reachable` → **locked**). Its file-room register
  **folds into the hub** (one location, one window, the
  portrait always renders — Renner's Fork-A lesson), not a separate navigable room. **Locked until
  `salvage_relaunched`** (`entry_conditions` + `blocked_message`, `version="1.0"`).
- **Every new conditions block `version="1.0"`; new gates are per-NPC meters + located flags, never triggerless
  flags. Reset the shared sex-loop traits on entry & exit of the Calloway loop.**

**Vane / the two thefts (world placement → Pass 3).** Vane is an unseen hand in 1a: **theft #1** moves the bug
(→ the underworld drop → the bug destroyed); **theft #2** (the big chunk) happened **days before** — an inside
job Vane covered so no gap ever shows. It is **never a scripted scene**: there is no visible theft beat. Wren
uncovers it only by draining Calloway past what he consciously knows (drain #2). Flag landing: `bug_traced` (W1)
+ the underworld-drop location in Pass 3; **no `theft2_done`** — the big theft carries no flag, it's a drain payload.

**The scenes (1a · the world — investigation, the Bastien-spying, Quests).**

| # | Scene | Lane | Gate | Place |
|---|---|---|---|---|
| W1 | **inv_underworld_drop** | L4 one-shot | `bug_planted` + (a day passes / next underworld visit) → the bug pinged here, now **destroyed**; docs go into the underworld, buyer UNKNOWN → **SETS `bug_traced`** | underworld_market (REUSE — the drop) |
| W2 | **amb_bastien_overhear** | L3 overhear | `bug_traced is_true` (story-gated, **NOT** NPC-presence — Bastien is schedule-less by design); at The Undertow she works his front — the traffic, the bartender Sol, his people; audio-only, her scheme in a `thought_bubble`; repeatable atmosphere, no hard flag. Optional time-feel via a **canvas** `trigger.schedules` (à la `hunt_marsh_scheme`), never an NPC schedule | underworld_bar (The Undertow) |
| W4 | **cap_deal_place** | L4 capstone | `calloway_drains_done >= 2` (the discovery) + `bug_traced` (she's been working the Undertow) + guard `deal_place_known is_false` → she pins the deal off the spying → **SETS `deal_place_known`** (the 1b handoff) | underworld_bar |

**Fork B — the Bastien-spying (locked with LO; re-mechanized OFF NPC-presence).** The deal location comes from
**spying on Bastien, not the bug.** **Why Bastien:** he's her **old kidnapper who trades in company secrets**, so
when W1 says "the docs go into the underworld," her hunch is *him.* But Bastien is **schedule-less by design** —
the shipped trick that hides his buyer reveal for 1b — so `npc_at_location(npc_bastien, is_present)` is hardwired
**false** and cannot gate the overhear (and "fixing" it with a schedule would list him on the Schedule page +
render his portrait, blowing the reveal). Instead W2/W4 are **story-flag gated** at his front, The Undertow:
**W2** opens on `bug_traced` (she starts watching), **W4** on `calloway_drains_done >= 2` (after the drain
confirms the chunk's gone). The fiction keeps Bastien **unseen** — she reads his *operation* (the traffic, the
bartender, his people), never the man — preserving the 1b reveal. So: bug → the underworld (W1), hunch → work
the Undertow (W2), the drain confirms the theft (#10 → counter 2), the spying pins the place (W4). The **buyer is
confirmed only at the 1b deal**, never here.

**The big theft is never a scene (7-22 rework).** There is no visible theft beat and no `theft2_done` flag. The
big pull happened **days before** — an inside job Vane covered so cleanly that neither Calloway nor Wren ever
sees a gap. It surfaces **only** in drain #2: drain #1 pulls his conscious (wrong) certainty that the section's
safe; drain #2 goes past that and finds it already gone, the counts squared by someone he trusts, her build file
in the pull. This is more logical than a spotted gap (a professional cover leaves none) and on-brand (Wren's
power is the drain, not physical detective work).

**The discovery is not a separate scene** — it *is* the drain reaching **counter 2** (#10 →
`calloway_drains_done >= 2`, the depths payload). The un-indexed archive means only Calloway's head, via the
drain, can confirm the material's gone and that her target rode in the stolen chunk. Downstream (W4, the Quest
card) reads the durable counter.

**The Quests page (1a — `quests_engine="v2"`, the shipped surface).**
- **Story-Goals (the mission spine — one card live at a time, a flag-milestone chain):** *Get inside Calloway's
  archive* (`salvage_relaunched` → `calloway_believes`) → *Trace the stolen docs* (`bug_planted` → `bug_traced`)
  → *The big chunk's gone — find the buyer* (`calloway_drains_done >= 2`) → *Follow it to the deal* (`deal_place_known`;
  the **1a end card**, points at 1b / next release, à la the Salvage end card). Each row's `next` = the same
  renderer as the sidebar; the last row is a flag-goal / handoff card, **never a bare met-numeric** (dodges the
  Frame-3 blank).
- **Calloway's section (the seduction — stepped on `npc_calloway.corruption` bands, one card at a time, the
  Renner ladder shape):** talk to him / work the case → the bug → contact → oral → *he pulls back (re-anchor)* → the loop / the
  drain. The coaching verb rides in the goal LABEL (the sidebar renders only the goal block).

**World gates & state (extend-only; adds to the Calloway list above).**
- **Flags (new):** `bug_traced` (W1) · `deal_place_known`
  (W4 — the 1b handoff; also gates the betrayal #11). Each one located setter; `version="1.0"` on every
  conditions block.
- **Locations — REUSE only:** `underworld_market` (the drop, W1) + `underworld_bar` / The Undertow (the
  Bastien-spying, W2/W4). **No new 1a location** beyond `vance_securities`. (The deal site + the controller
  room are 1b.)
- **Bastien stays hidden — NO NPC-presence gate.** W2/W4 must **not** use `npc_at_location(npc_bastien)` — he's
  schedule-less by design (hardwired false; a schedule would blow the 1b reveal). They gate on **story flags** at
  `underworld_bar` (W2=`bug_traced`, W4=`calloway_drains_done >= 2`); any time-of-day feel uses a **canvas**
  `trigger.schedules` (like `hunt_marsh_scheme`), never an NPC schedule. `version="1.0"` on every block.

**Media (per placed scene; the intended visual named now — `search_queries` written at authoring, beat_0065; engine
silent-skips missing → text-forward until harvested).** Calloway portrait (the hub) · the file room (establishing)
· the bug-plant beat · the ladder rungs (contact / oral — escalating intimacy stills) · the loop (oral → vaginal →
anal **act-clips**) + the anal-finish **drain** · the underworld drop (W1 — the destroyed bug) · the deal-place
pin (W4). **W2 (the Undertow overhear)
is audio-only — NO image** (voyeur / unseen, per Fork B). The belief-lever seduction leans on the standard harvest
(office / desk / a suited man) — plenty of corpus; the drain reuses the shipped drain-finish framing.

### The Archive — wiring & plan (Step 5 · Pass 4)

> ⚠️ **SUPERSEDED 2026-07-22 — see `games/vesper/design_beat_archive_v2.md` (authoritative) + the reconciled ledger `plan[]`.** The DAG/flags below (bug/theft/overhear) are the OLD design. The v2 spine + the reworked plan (beats 0056–0067) live in the v2 doc and `authoring_state.json`.

**The DAG (acyclic; every arc cold-start-reachable; every cross-gate telegraphed; every flag one located
setter).** Entry: `salvage_relaunched` (shipped) → unlocks `vance_securities`.
- **Spine:** `salvage_relaunched` → `calloway_met` (#1) → `calloway_believes` + `bug_planted` (#3) →
  `calloway_oral_once` (#5) → `calloway_flinch_resolved` (#6) → `calloway_fucked_once` (#7) →
  `calloway_drains_done` 0→1→2 (#10; drain 1 = surface, drain 2 = depths / the discovery).
- **Investigation (parallel, off `bug_planted`):** `bug_planted` → `bug_traced` (W1); `bug_traced` opens
  `amb_bastien_overhear` (W2). (Theft #2 carries no flag — it surfaces only in drain #2.)
- **Handoff:** `calloway_drains_done >= 2` → `deal_place_known` (W4) → `calloway_reported` (#11, the 1a betrayal
  / the 1b fuse). Acyclic — `calloway_reported` gates nothing upstream.
- **D1 (no entry gated):** `cap_calloway_meet` (#1) is auto-fire on `salvage_relaunched` alone — the arc
  cold-starts from the shipped re-launch.
- **D2 (no cycle):** strictly forward; each `_done` / milestone flag set on a terminal exit.
- **D3 (cross-gates telegraphed):** the drain rungs cite the loop; W4 cites `calloway_drains_done >= 2` (the
  "find the buyer" Quest card).
- **1a-complete = `deal_place_known` + `calloway_reported`** → the 1b handoff (the deal; next release). No 1b
  scene authored in 1a; `deal_place_known` sits as the frontier flag (its 1b readers greyed / telegraphed).

**Frontier (telegraphed, deferred — never silent).** `deal_place_known` opens **1b** (the deal: seller = Vane,
buyer = Bastien *confirmed*, the collision, the build-file read, the Mercer trade for the leash controller).
`calloway_reported` is the **fuse**: Calloway's report → the cover-trail → the Chairman (**Aldous Vance**) →
Mercer blown. Both seeded here, built in 1b. The **build-file read** + the **Mercer trade** are 1b's two Tier-3
licenses.

**Plan seed** (`status=planned`; 1a only — 1b seeds at its own build):
- `beat_0056` — **scaffold + systems** (declare `npc_calloway` / `npc_vane`, `vance_securities` + its lock, the
  new flags + `calloway_drains_done`; green build, **no story canvas**).
- `beat_0057` — **the cover** (extend the shipped `salvage_relaunched`: arm the mission + unlock
  `vance_securities`; touch no shipped byte). To Wren it reads as a **plain company errand** — she does **not**
  know Mercer's private-leverage motive (its 1b reveal lands harder for the unwitting 1a setup).
- `beat_0058` — **Calloway meet + hub** (`cap_calloway_meet` + `hub_calloway_fileroom` + portrait / schedule).
- `beat_0059` — **the bug proposal** (`cap_calloway_bug` → `bug_planted` + `calloway_believes`).
- `beat_0060` — **the bug-trace + underworld drop** (W1 → `bug_traced`; the destroyed bug, buyer unknown).
- `beat_0061` — **the seduction ladder** (rungs #4–#7 + the flinch throttle). *(The separate theft-#2 beat
  `cap_theft2` was removed 7-22 — the big theft is uncovered through the drain, not a physical gap.)*
- `beat_0062` — **the sex loop + the two drains** (#8–#10; the triggerless loop + drain canvas; `calloway_drains_done`
  0→1→2 — drain 1 = surface (he's certain), drain 2 = depths (the big pull, days ago, an inside job, her file
  in it) = the discovery; **no `theft2_done`, no `big_chunk_known` flag**).
- `beat_0063` — **the Bastien-spying** (W2 atmosphere on `bug_traced` + W4 payoff on `calloway_drains_done >= 2`
  → `deal_place_known`; **story-flag gated at The Undertow, Bastien unseen** — no NPC-presence gate).
- `beat_0064` — **the 1a betrayal seed + Quests page** (`cap_calloway_reported` → `calloway_reported`; the
  Story-Goals spine card + Calloway's stepped card; the 1a end card → 1b).
- `beat_0065` — **media pass + clean 1a ship** (find-media for the new scenes; the SHIP build — `--video-folder`,
  no `--dev` / `--debug`; the 0-missing-media grep gate).

**Self-check (before Step 7).** Every 1a story moment has a placed home; every lewd rung double-locks
(belief-open + corruption band), non-lewd beats (meet, bug, flinch, overhear) ungated; the DAG is acyclic +
cold-start-enterable from `salvage_relaunched`; every flag has one located setter (the drains as a hidden
counter); the opening is concrete (the cover one-shot); the plan is seeded + ordered; **no TOML / no scene prose
written** (Step 7).

### The Leash blueprint (Act 2 · 1b — Step 5, rev 112)

> Full record: `games/vesper/design_the_leash.md`. Locked with LO 2026-08-09. The chapter after The Archive
> 1a, built from the shipped 0.1.7 end-state (blown topside, alone in the underworld, holding a locked key and
> a locked file). It **supersedes** the `design_beat_archive_v2.md` §12 "1b · The Deal" sketch — same
> destinations, different shape: **no deal scene**, because the controller trade already happened in the 1a
> close. **~30–36 canvases.**

**The verb — she keeps a mark warm on purpose.** Distinct from every verb on the roster: seduce-in (Renner) /
scheme-and-serve (Marsh) / she-is-taken (the cell) / supplicant-test-bench (Salvage) / belief-lever (Calloway) /
the cold underworld use (Colm). Here she is **neither obeying nor rebelling** — she is *humouring* a man who
cannot conceive of a version of her that says no, and spending the access it buys. The 1a close paid off the
old arrangement (*"the deal's paid; they're quits"*), so every visit is **her walking in on her own feet**.
That is the whole difference, and it is the difference between a con and servitude.

**The scenes.**

| # | Scene | Lane | Gate | Place |
|---|---|---|---|---|
| 1 | **kess_1b_open** *(restored from `08ec2e1`)* | L4 auto-fire | `archive_1a_done is_true` + `berth_home is_false` → **SETS `berth_home`** | `kess_berth` |
| 2 | **activity_kess_cot** *(restored)* | solo host | `berth_home is_true` — paid night (coin → full Charge, day advance, drain reload) **or** free crash-rough (partial Charge, no advance, no reload) | `kess_berth` |
| 3 | **hub_kess_berth** *(rev 114 — replaces the planned `activity_pay_rent`)* | L1 hub (portrait) | `berth_home is_true`; two exclusive `[group]` bands on `feed_line_days` (`gte 1` working / `lt 1` stalled). **The paid night IS the upkeep** — the cot's existing 10-coin tier sets `feed_line_days = 3`, so there is no second bill; this hub is where the state is *read* (Kess says it) and where a lapsed player is pointed back at the cot | `kess_berth` |
| 4 | **cap_file_shape** | L4 capstone (Tier-3) | `berth_home is_true` + `file_shape_known is_false` → **SETS `file_shape_known`** | `kess_berth` |
| 5 | **kess_needs_print** *(rev 116 — a HINGE, not a capstone: 7 beats, NOT Tier-3; `cap_` prefix dropped so the id doesn't claim a badge it declines)* | L4 auto-fire | `file_shape_known is_true` + `print_needed is_false` + `feed_line_days gte 1` + `npc_kess is_present` → **SETS `print_needed`** | `kess_berth` |
| 5b | **quest card F** *(rev 116)* | Story-Goal | `print_needed is_true` + `mercer_found is_false` — the errand card, and the new terminal frontier (it takes the build boundary + the Support-Us ask off E). ⚠️ **E gains `print_needed is_false` in the same edit.** E's own sentence *"Now you wait him out"* is FALSE the moment Kess names the errand — and priority is **inert** in this tier (`pickQuestsCards("story_goals")` emits a winner per `group`, and vesper sets `group` on zero cards), so exclusivity can only live in `when` | Quests page |
| 6 | **cap_mercer_resurfaces** *(rev 117 — BUILT: Tier-3 capstone, 14 beats / 13 clicks, 445 w, 0.93:1; the `cap_` prefix is earned here, unlike scene 5)* | L4 auto-fire, **no `requires_npc`** | `print_needed is_true` + `mercer_found is_false` → **SETS `mercer_found`** (the name exchange; he asks, she doesn't stop). No presence gate because he has **no schedule at the bar** — see 6c. Shipped precedent for a scheduleless speaker: `salvage_relaunch` @`the_waterfront` | `underworld_bar` |
| 6b | **quest card G** *(rev 117)* | Story-Goal | `mercer_found is_true` + `owner_print_taken is_false`. ⚠️ **Not optional bookkeeping — it is the only thing standing between the player and a blank Quests page.** `mercer_found` closes F, and the chapter's next card isn't authored until scene 19, so without G the Story-Goals spine is **empty for twelve beats** of live play. F *keeps* its copy of the Support-Us ask (the rev-113 precedent set on D) and its boundary sentence stays true where it stands | Quests page |
| 6c | **`mercer_room` + his second schedule row** *(rev 117)* | location + NPC timetable | ⚠️ **The chapter's one engine-forced shape.** A schedule row carries **no conditions** (the resolver reads five keys, `v2.py:979-985`) and `getNpcLocation` is first-match-wins in declaration order (`:3439-3454`), so Mercer's Act-1 penthouse row (08:00–23:00, untouched — Act 1 needs it) is permanent and his new row only ever owns **23:00–08:00**. And presence has two surfaces: the in-room portrait card is canvas-gated (`:4998-5008`) but the **nav-card badge is not** (`getNpcsPresentAtLocation`, `:4773`) — a row at the public bar would park his face on the Undertow card from Act 1b onward. A **locked** card renders no indicators at all (`:19270-19281`), so his only underworld row is at `mercer_room`, locked on `mercer_found`. Named **"The Lockup"**: neutral, true before and after, and it can't be renamed later. Live-verified both ways — `badges: 0` locked, `badges: 1` unlocked | `underworld_market` → `mercer_room` |
| 7 | **mercer_end_table** *(rev 118 — BUILT. ⚠️ Renamed from the planned `hub_mercer_undertow`: it has no `npc` and no `requires_npc`, so it renders in the flat solo-link bucket, and calling it a hub would be a lie about its shape — the same discipline scene 5 used when it dropped its `cap_` prefix)* | L1 rung (link) | `mercer_found is_true` + `npc_at_location mercer_room / npc_mercer / is_absent` — **live exactly when his room is not**, so the two surfaces can never both claim him. Built with *neither* presence field on purpose (6c is why he can have no schedule row here); `check_render_buckets` only flags `requires_npc`-without-`npc`, so it stays clean. Carries **ask #2 — the request** — as a lone `[group]` on `relation lt 6`, so it lands on the early visits and then he stops asking, with no counter anywhere. +2 relation, 30 min | `underworld_bar` |
| 7b | **mercer_room_offhours** *(rev 118)* | dead-room guard | `npc_at_location mercer_room / npc_mercer / is_absent`, priority 1. His row is 23:00–08:00, so outside it the room has no portrait and no hub and would read **dead**. Shape copied from `berth_offhours`, not invented: the padlock and the shuttered stall, seen from outside. ⚠️ `version = "1.0"` or the condition fails **open** and it renders while he is standing there | `mercer_room` |
| 8 | **hub_mercer_room** *(rev 118 — BUILT. ⚠️ Gate CHANGED from the plan: `mercer_found`, not `mercer_hospitality_open` — see scene 9)* | L1 hub (portrait) | `mercer_found is_true`, `requires_npc` + `npc` so **presence does the 23:00–08:00 clock for free**. Base prose bands on the **flag**, not the meter (the meter buys access, never register): before = a man performing a host; after = he doesn't get up. Two rungs — *Let him talk* (+2, 30 min, a pool of penthouse stories, **none of it about her**) and *Pour for him* (+3, 60 min, banded on relation). **She doesn't drink** — scene 6 established it in his own mouth — so the hospitality runs one way and she is the one pouring | `mercer_room` |
| 9 | **rung_mercer_hands_on** *(rev 118 — BUILT. Auto-fire, 7 beats / 6 clicks, 240 w, 1.26:1. **Not** a capstone: no `cap_` prefix, nothing declares Tier-3)* | L1 rung, auto-fire one-shot | `mercer_found is_true` + `mercer_hospitality_open is_false` + `npc_mercer.relation gte 12` → **SETS `mercer_hospitality_open`**. ⚠️ **The flag's MEANING is re-cut here.** The plan had it set by a `cap_mercer_invites_back` at the bar — but scene 6 already spent the invitation in his own mouth (*"Come round… You'll come."*) and unlocked the room's door on `mercer_found` in the same beat, so a second invite canvas would re-play a beat the player just played. The key is kept and re-pointed: it now means **the arrangement is back on**, and it still gates scene 10 exactly as planned. **Auto-fire, not a choice** — she doesn't elect it; he can't conceive of a version of her that says no, so the evening simply turns. Carries **ask #3 — the silence**: she says his name, he answers, and there is no `thought_bubble` and no line of narration anywhere in the canvas remarking on it. **It stops at the touch** — his hand, her not moving; nothing explicit, so the unsigned Mercer ceiling stays unspent | `mercer_room` |
| 10 | **cap_owner_print** *(rev 119 — BUILT. Auto-fire capstone, 14 beats / 12 clicks, 562 w, **1.01 : 1** — the best ratio in the game and the whole point of putting Mercer on the page)* | L4 auto-fire capstone | `mercer_hospitality_open is_true` + `owner_print_taken is_false` + **`npc_mercer.relation gte 15`** + **`npc_at_location mercer_room / npc_mercer / is_present`** → **SETS `owner_print_taken`**. **The first spend of the Mercer ceiling** (clause iii — warm and crude at once); anal held for scenes 13/15. He has her over the end of the bed and never stops talking about the penthouse; his free hand goes flat on the crate beside her coat to lean on, and the controller comes out of the pocket and under his palm. **He never looks down at his own hand.** One `thought_bubble`, and it observes rather than plans. ⚠️ **Two engine-forced gates, both found live** — see the two notes under the table | `mercer_room` |
| 10b | **kess_print_read** *(rev 120 — BUILT. Auto-fire one-shot, 12 beats / 11 clicks, 382 w, **0.28 : 1** — the most dialogue-dominant canvas in the game)* | L4 auto-fire one-shot | `owner_print_taken is_true` + `parts_loop_open is_false` + `feed_line_days gte 1` + **`npc_at_location kess_berth / npc_kess / is_present`** → **SETS `parts_loop_open`**. ⚠️ **The blueprint had no row for `design_the_leash.md` §6 step 6** — *"the print is a start, not a solve… he can't crack it clean, he has to build"* — which is the beat that motivates the entire loop; placed at rev 119, built here. ⚠️ **It sets a flag, where the rev-119 placement said "sets nothing"** (the `salvage_mercer_shocked` pattern): three things have to read this moment — card H's closer, card I's opener and the market stall's gate — and a one-shot with no flag can be read by nothing. The print **moved** the key and still isn't a solve: he has the *shape* of what Mercer's hand said, not the hand, and a shape played back cold reads as a recording. So he builds something that says it live **from inside her**, and the only bench that can test it is the man himself | `kess_berth` |
| 10c | **quest card H** *(rev 119; **re-cut rev 120**)* | Story-Goal | `owner_print_taken is_true` + **`parts_loop_open is_false`**. ⚠️ **Mandatory, and for the second time in three beats.** Scene 10's exit **closes G**, and G was the last Story-Goal card in the game (all nineteen checked against the merged TOML), so without H the spine goes blank the instant the print scene ends. ⚠️ **Re-cut at beat_0075, twice, and both were forced:** its closer moved from `owner_drained` to `parts_loop_open` so card I can own the loop (the ladder's rule is that each card's closer IS the next card's opener — left alone H and I would both be live), and its tip's *"that's where this build ends"* sentence is **gone**, because beat_0075 ships what that sentence called the next release. H's text is untouched. Free to re-cut: it was one beat old and had never been committed | Quests page |
| 10d | **quest card I** *(rev 120)* | Story-Goal | `parts_loop_open is_true` + `owner_drained is_false` — the new frontier, carrying the build boundary and the Support-Us ask forward from H. **One card spans the whole loop** (scenes 11–14) rather than flickering a new one per attempt: `owner_drained` is not set until scene 15, and the mopoga finding is that lostness, not grind, is the genre disease — a card that changes every cycle teaches the player nothing about where the chapter is going. It speaks in the fiction's terms and never names the hidden counters. ⚠️ **Its tip was re-cut at rev 124**, the same forced re-cut it performed on H: the tip's *"that's where this build ends: the first fire… is the next release"* went false the moment `beat_0079` shipped the first fire. The **build boundary** moved to card J; I's **text** is untouched and stays true where it stands. **The ask stayed on I** — see the note under J | Quests page |
| 15b | **quest card J** *(rev 124)* | Story-Goal | `owner_drained is_true` + `bastien_hub_open is_false` — the new frontier, carrying the build boundary and the Support-Us ask forward from I. ⚠️ **Mandatory, and for the FOURTH time in this chapter.** Scene 15's exit closes I, and I was the last Story-Goal card in the game, so without J the spine goes blank the instant the chapter's biggest scene ends. `bastien_hub_open` is not set until `beat_0080`; the forward reference builds green because quest `when` has no validation site. No `goals` array (frontier shape). ⚠️ **A DEFECT CAUGHT BY THE REGRESSION SUITE, WORTH KEEPING:** the first cut of I's re-cut stripped the whole closing sentence group, which took the **Support-Us ask** off the live card for the entire loop. The rev-113 precedent set on card D is that a prior card **keeps its copy of the ask** and only the boundary *claim* can go false — the ask is true at every stage. Fixed in the same turn. Card **H** is the one rung in the ladder that carries no ask (it lost both at `beat_0075`); recorded rather than re-cut here, and worth fixing the next time H is open | Quests page |
| 11 | **activity_buy_part** *(rev 120 — BUILT)* | L1 solo card (market) | `parts_loop_open is_true` + `part_held lt 1` + `part_installed lt 1` → **25 coin** → `part_held = 1`, 30 min. **Its own card, not a fourth choice on `underworld_market_shop`** — the loop's next step has to be a visible card that appears when it is wanted and vanishes when she is carrying one. The two `lt 1` clauses are the **no-stockpiling rule**: one part at a time, which is what makes the burn bite. A cycle runs ~35 coin all in against a 10-coin night, a +20 pit win and a +10 finisher | `underworld_market` |
| 12 | **kess_install_part** *(rev 120 — BUILT. **Triggerless**, 9 beats / 8 clicks, 368 w, 1.10 : 1)* | L1 rung (bench) | Reached from `hub_kess_berth`'s new **"Give him the part"** rung, gated `part_held gte 1` + `feed_line_days gte 1` → **SETS `part_installed = 1`**, consumes `part_held`. ⚠️ **Triggerless because it has to run four times** and the auto-fire path hard-refuses a repeatable canvas (`v2.py:4454`); the only auto-fire shape that repeats is Salvage's twelve one-shots. Banded on **`mercer_attempts`** for the build talk — **`part_gen` is dropped**, it counted the same thing and two counters for one fact is a desync waiting to happen. **The first spend of the Kess ceiling** (clause iii — explicit and not sexual). ⚠️ **All four bands authored at rev 123** — 0 at beat_0075, then findings 1/2/3 at beats 0076/0077/0078 — and **the chain is complete and does not grow again**: nothing pushes `mercer_attempts` past 3 (scene 15 bumps `mercer_drains_done`), so **band 3 takes `gte 3` with no upper bound** and is the terminal band. Band 1 (finding 1 — *it isn't a lock, it's listening, and he hit the wrong wire*) discharged the debt beat_0075 owed forward; band 3 (finding 3 — *not a man, a set of names; I've been spoofing one; two I can't place; one's Bastien*) is the chapter's hinge and closes `design_the_leash.md` §18's last open item at the recommended answer: **two he cannot place plus Bastien, a list and not a roster**. ⚠️ **Every band comes in at 21 words or fewer and three of them are exactly 21**: the audit reads beat 0 as the sum of all four (109 w) but what a player sees is the lead plus the longest single band, which is **exactly 50** and cannot go higher. Worth knowing before anyone "adds a word": the audit counts on `str.split()`, so an em dash is its own token | `kess_berth` |
| 13 | **loop_mercer_attempt** *(rev 121 — BUILT, try 1; rev 122 — try 2; **rev 123 — try 3, COMPLETE**. **Triggerless**, four nodes: `.base` 7 beats / 6 clicks, `.try1` 6 beats / 5 clicks, `.try2` 8 beats / 7 clicks, `.try3` 7 beats / 6 clicks; 1,100 w across the canvas, **1.27 : 1**)* | L1 rung + **per-generation NODES**, routed by exclusive choice condition | Reached from `hub_mercer_room`'s new **"Give him the evening"** rung, gated `part_installed gte 1` + `mercer_attempts lt 3` → the evening, the reach, the failure; **burns the part** (`part_installed → 0`) and bumps `mercer_attempts`. ⚠️ **NOT the banded `[group]` chain this row planned.** One canvas is right and stays one canvas, but each try is 4–6 beats with its own cascade, and §7 check 2 sums the whole node lead into beat 0 — four multi-beat bands there measure as a single ~250-word beat. Per-generation nodes give each try its own exit, beat count and word budget. The merge trap is sidestepped rather than managed. *(This sentence used to end "and try 3 needs a different exit anyway (it arms the Bastien thread)" — **withdrawn at rev 123**: the arming rides the routing choice, and try 3 exits exactly like its siblings.)* ⚠️ **The burn and the bump ride the routing CHOICE, not a node exit** — exit effects fire on **render**, choice effects on **click** (rev 120's finding, first time it changes a decision), so the state belongs to the instant she reaches. ⚠️ **The gate widens one notch per beat** (`lt 2` at 0077, `lt 3` at 0078) so the rung can never route into a try node that does not exist. **The held anal lands here** — `mercer_finisher` canonises that his anal finish passes nothing to her, so the reach rides the one act where her body has always found nothing, which is what makes try 1's *identical* nothing land. ⚠️ **Try 2 needed a NEW CEILING ROW** — see *Content register*, *the governor acting on her body, outside the cell*, signed rev 122. Every other row governs a person's register; none governs her body acting on its own, and damage to her outside the cell had never shipped. **The clamp lands at the HOLD, not mid-stroke** (§9's sketch said mid-fuck): the shared node ends with him finishing and holding, the reach *is* the routing click, and at the hold he is still and quiet and against her — the worst possible moment to conceal anything. **The concealment engine:** the half of the clamp he can feel is her gripping down on him, which is the one thing he has always wanted from her, so he misreads it as her finally responding and is delighted. She only has to hide the rest, and the near-miss is him accepting *"it's cold in here"* because looking at her face would cost him an effort he has not spent in two years. **Try 3 (rev 123) closes the loop and needed no new ceiling** — the rev-122 row governs tries 2 *and* 3, and try 3 spends *less* of it: no clamp, no pain, and nothing to conceal, because canon says a drained man notices nothing. The governor **releases**, her drain catches on him for the first time in two years, then **something goes down a list, finds a gap and shuts the door on the way back**. What she tastes is *ownership, not arousal* — the node quotes the game's shipped instrumental drain lexicon rather than inventing a sensory one, and the suite asserts both halves (no arousal vocabulary present, the shipped vocabulary present). **The hinge is split across two surfaces, neither of them a new canvas:** she gets the *sensation* of a list-shaped check, Kess gets the *diagnosis* at band 3 — §14's rule that she never diagnoses. ⚠️ **One claim withdrawn:** this row and the canvas header both argued that try 3 would need a **different exit** because it arms the Bastien thread. **It does not** — the arming is `mercer_attempts gte 3` and that rides the routing choice, so `.try3` exits to `mercer_room` at +30 like its siblings. The rest of the nodes-over-bands argument (check 2 folds the node lead into beat 0) is the real reason and is untouched. ⚠️ **`lt 3` was the LAST widening** — at 3 the rung is dark for good and scene 15 takes the fourth evening as an auto-fire, so *the rung is absent* is now a **terminal** state, which is what the test asserts | `mercer_room` |
| 14 | **kess_finding** — ⚠️ **RESOLVED rev 120: there is no such canvas.** `design_the_leash.md` §18's open item (*"whether Kess's three findings ride the install canvas or get their own short bench beats"*) is **closed in favour of riding the install**: bands 1/2/3 of scene 12's chain. It is where he has his hands in her and is talking anyway (which the ratio target loves), it keeps the player's cycle to four surfaces instead of six, and a separate bench beat would be a **second auto-fire at `kess_berth`** competing with the install — the beat_0074 chaining trap, invited back in | — | banded into scene 12 | `kess_berth` |
| 15 | **cap_first_fire** *(rev 124 — BUILT. Auto-fire Tier-3 capstone, 18 beats / 17 clicks, 700 w, **0.93 : 1** — the game's best ratio, and the carriage rule is why)* | L4 auto-fire capstone | `mercer_attempts gte 3` + **`part_installed gte 1`** + `owner_drained is_false` + **`npc_at_location mercer_room / npc_mercer / is_present`** → the drain fires → **SETS `owner_drained`**, bumps `mercer_drains_done`. ⚠️ **The blueprint said `eq 1`; built as `gte 1`** — the trait is binary so they are equivalent, and `gte 1` is the shape the loop rung and scene 17's fix both use. The clause means *she has been back to Kess since try 3*, which is where band 3 is spoken. ⚠️ **THE CONTROL-CANVAS CARRIAGE RULE IS EXECUTED HERE FOR THE FIRST TIME IN THE GAME** — 6 of her questions against 13 of his answers. Measured at this beat: `loop_renner_finisher.drain`, `calloway_drain_canvas.d0` and `colm_drain_canvas.d0` contain **zero** player dialog blocks between them, so the rule had been decorative for three chapters. ⚠️ **THE PART IS NOT BURNED** — §9's heading is *try 4 holds*. That closes the parts economy (`activity_buy_part` and the install rung both read the counters and go dark) and it is **load-bearing forward**: scene 17's fix reads `part_installed gte 1`. ⚠️ **Exits to `underworld_market`, not back into his room** — an auto-fire that exits into its own location chains, and §10's closing image agrees. `owner_drained` and the bump ride the **exit block**, not a choice, because this is an auto-fire she cannot decline, so render *is* the event (the `cap_owner_print` / `kess_print_read` shape). One §7 split was forced: beat 0 measured **59 w** against the hard 50. **The one explicit spend of the Mercer ceiling** (signed rev 119 — its budget line names this canvas), so no new signature was owed | `mercer_room` |
| 16 | **loop_mercer_warm_tap** *(rev 124 — BUILT in the same beat as scene 15. Triggerless, 4 beats / 3 clicks, 159 w, 0.96 : 1, no media)* | L1 rung (triggerless) | `owner_drained is_true` — the repeat; pure power, no new payload. Reached from a **fifth rung on `hub_mercer_room.base`** carrying the same label as the loop rung (*"Give him the evening"*), the two **exclusive by construction**: that one needs `mercer_attempts lt 3`, this one needs `owner_drained`, which is only set at 3. The `mercer_drains_done` bump rides the **choice** — she did this again, and doing is a click. ⚠️ **Built here rather than deferred**, and the reasons are structural: §17's sequence runs `beat_0075`–`0079` = the loop and opens Bastien at `0080`, so scene 16 falls between two chunks and would never get a turn; without a repeat `mercer_drains_done` is a constant, not a counter; and without it his room goes **flat at the exact moment the chapter says she owns him** — the loop rung is dead at 3 and the capstone is a one-shot. ⚠️ **It cannot be an auto-fire** (`v2.py:4454` refuses a repeatable one), which is why it is a canvas and not a second node on scene 15. Shape copied from the `calloway_drain_canvas` / `colm_drain_canvas` `done` nodes, media call included | `mercer_room` |
| 17 | **cap_bastien_walks_in** *(rev 125 — BUILT. Auto-fire Tier-3 capstone, 15 beats / 14 clicks, 600 w, **0.79 : 1** — the new best canvas ratio in the game)* | L4 auto-fire | `mercer_attempts gte 3` + **`part_installed gte 1`** + `bastien_hub_open is_false` → **SETS `bastien_hub_open`**. ✅ **The rev-123 off-by-one was fixed AT BIRTH rather than patched.** The counter hits 3 the instant try 3's routing choice is clicked, but the set is not *known* until Kess speaks band 3 — which needs a fourth part and a walk back to the bench. A `[group]` sets nothing, so no "finding 3 heard" flag exists and none can be added there. `part_installed gte 1` means *she has been back to Kess since try 3*, needs no new state, and **works only because `beat_0079` does not burn the fourth part**. ⚠️ **SCHEDULELESS SPEAKER — no `requires_npc`, no `npc`, no presence clause**, the `cap_mercer_resurfaces` shape at this same bar; a predicate for an NPC the resolver can never place would gate the scene shut forever. **The scene:** he did not release her at the 1a close, **he lost her**, and has spent the time since not finding out who came through his far door. His lever is **curiosity, not desire** — the cell was a room with a notebook in it. **Nothing explicit: the search is promised in his own mouth and played at scene 18**, so the unsigned Bastien row stays unspent (the `rung_mercer_hands_on` precedent). Cain stays reserved — never named | `underworld_bar` |
| 17b | **quest card K** *(rev 125)* | Story-Goal | `bastien_hub_open is_true` + **`bastien_drains_done lt 1`** (the trait form of the closer, the shape card B2 already ships). ⚠️ **Mandatory, and for the FIFTH time in this chapter** — scene 17's exit closes J, and J was the last Story-Goal card in the game. `bastien_drains_done` is not bumped until `beat_0082`; the forward reference builds green because quest `when` has no validation site. No `goals` array (frontier shape). It names the door and the smuggling problem in the fiction's terms — *nobody comes into that room carrying, and on a name that's on the set neither the drain nor the switch works without the other*. **Card J keeps its Support-Us ask**; only the build-boundary claim moved here | Quests page |
| 18 | **hub_bastien** + **bastien_door_search** + **bastien_backroom** *(rev 126 — BUILT. The search: flat solo link @`underworld_bar`, repeatable, 7 beats, **0.85 : 1**. The hub: portrait hub @`bastien_backroom`, **0.75 : 1**. Plus `kess_seat_controller` @`kess_berth`, 7 beats, 1.11 : 1)* | L1 hub (portrait) + L1 gate (solo link) | `bastien_hub_open is_true`; **the door-search is the gate, played on-screen, every visit** — carrying the drain *and* the controller past him is the escalation. ⚠️ **NO FAIL BRANCH:** he is *establishing that he still may*, so she always gets in and what varies is whether what she needs got in with her — three exclusive bands on (`controller_seated`, `stealth 30`): seated in the seam by Kess · in her coat on stealth · found, and it sits on his desk while the evening is wasted. The outcome rides the **exit CHOICE** (`controller_through`), because choice effects fire on click. ⚠️ **THE ROOM IS NAV-INVISIBLE — no `entry_from`, and that one property does two jobs**: no nav card means his schedule can never leak a badge, **and** the search cannot be skipped, because the only way in is its exit. Strictly better than the locked card rev 125 recorded, which would advertise the room before she is invited and let her walk past the scene once open. ⚠️ **BOTH HALVES OR IT DUMPS THE WHOLE MAP** — `auto_exit = false` as well, caught live: a childless, parentless location renders an empty nav grid, and an empty grid trips the list-every-location fallback (`v2.py:19386`), so the built passage carried `All locations:` and she could walk from his back room to the Spire. `underworld_gate` is the shipped precedent. **The first spend of the Bastien ceiling** (SIGNED rev 126) | `underworld_bar` → `bastien_backroom` |
| 18-note | *(superseded)* | — | ⚠️ **The rev-125 note, kept for the trail:** `beat_0080`'s ledger entry planned `npc_bastien schedule @underworld_bar`; **that must not be built.** A schedule row at a **public** location parks the NPC's badge on the nav card — the in-room portrait is canvas-gated (`v2.py:4998-5008`) but the **nav-card badge is not** (`getNpcsPresentAtLocation`, `v2.py:4773`) — and `underworld_bar` has been reachable since Act 1 and is unlocked, so it would show Bastien's face to a player still mid-Act-1 who is currently being kidnapped by him. **Scene 6c hit this exact wall with Mercer and solved it with a LOCKED room** (*a locked card renders no indicators at all*, `v2.py:19270-19281`). **So Bastien gets a locked location behind the bar, and the door-search becomes that location's ENTRY GATE** — which is what §11 wanted anyway (*"in front of his own bar"*, then the back room), puts his schedule where the badge is harmless, and makes the search a real door rather than a canvas that politely asks her to submit. `live_beat_0080.py` already asserts **no Bastien badge anywhere on the nav grid**, so this row inherits a live guard. **⚠️ This is where the Bastien ceiling comes due** | `underworld_bar` → a locked back room |
| 19 | **loop_bastien_backroom** + **loop_bastien_finisher** + **bastien_drain_canvas** *(rev 127 — BUILT. Triggerless chain on the shipped `loop_colm_*` shape; **1.08 / 1.28 / 1.22 : 1**, against the shipped Colm chain's 8.8 / 102 / 132)* | L1 rungs (triggerless) | Reached from `hub_bastien`'s **"Let him take you in the back"** rung. Poses oral/vaginal/anal, climax-elect at `loop_npc_pleasure gte 50`; the anal finish IS the drain; bumps `bastien_drains_done`. ⚠️ **`npc_bastien.relation` band DELETED from this row at rev 127** — §11 says his lever is *curiosity, not desire* and that *"a standard seduction ladder bounces off him; he'd enjoy it and give nothing"*, so a meter here would say the opposite of what the chapter says about the man. **The door was the gate.** `relation` still ticks on the hub's talk rung; nothing reads it. ⚠️ **TWO CONDITIONS, and the loop teaches the second by letting her break it once:** the shipped pattern already teaches *only the anal finish opens the drain*; Bastien adds **and only with the key running**. Anal + `controller_state = 0` routes to `.dead` — the cold-socket nothing, **no bump, no fail screen**. ⚠️ **THE PAYLOAD DOES NOT NAME CAIN** — see the note under this table. **First spend of the loop half of the Bastien ceiling** (SIGNED rev 126, both clauses held by grep) | `bastien_backroom` |
| 19b | **quest card L** *(rev 127)* | Story-Goal | `bastien_drains_done gte 1` + `leash_cut is_false`. ⚠️ **Mandatory, and for the SIXTH time in this chapter** — the `d0` choice closes K, and K was the last Story-Goal card in the game. `leash_cut` is not set until `beat_0083`; the forward reference builds green because quest `when` has no validation site. Frontier shape, no `goals`. **Card K keeps its Support-Us ask**; only the build-boundary claim moved. It does **not** name Cain and does not claim she holds the name | Quests page |
| 20 | **cap_extraction** *(rev 128 — BUILT. Auto-fire Tier-3 capstone, 18 beats / 17 clicks, 762 w, **1.30 : 1**. **The chapter's last content beat**)* | L4 auto-fire capstone | `owner_drained is_true` + `bastien_drains_done gte 1` + `leash_cut is_false` + **`npc_at_location kess_berth / npc_kess / is_present`** → **SETS `leash_cut`, `file_read`**. ⚠️ **Feed-line state deliberately NOT gated** — the chapter's closing beat is not blocked behind an upkeep meter, and the live suite asserts it fires with the line lapsed. Every piece was promised in the chapter's first beat: `kess_1b_open`'s *"the file rides on the same crack, so it opens when the key does"* and `cap_file_shape`'s *"I open that, you get your page."* **The page:** the programme's size, her designation four years older than she is, **BUILD**, and the second date column — *hers is blank*. The hook names nobody: the programme **closed**, and her page was sealed eight months later by a hand on none of the sign-offs. ⚠️ **CAIN IS NOT NAMED**, reversing what rev 127 recorded — see the note under this table. ⚠️ **The reveal was re-cut at measure time**: the first draft was 182 w of unbroken narration at 2.31 : 1; she reads it aloud now and Kess talks her through the cut | `kess_berth` |
| 20b | **THE RETIREMENT PASS** *(rev 128 — BUILT alongside scene 20, and it fixed a LIVE DEAD-END)* | five surfaces | §13 retires the switch and the block at the cut, which is **not flavour**: `loop_bastien_finisher`'s drain exits required `controller_state gte 1`, and `controller_state` is 0 forever after the extraction — so **every future anal finish would have routed to the nothing-happens branch permanently**, with the player owning the man and getting nothing, no way back, and nothing on screen to show it. Handled: the finisher went **four exits to six** (three key-era exits gain `leash_cut is_false`; two new post-cut exits reach `d0`/`done` with no key) · the anal pose gains a **fourth band** and loses the switch · `bastien_door_search` gains a **fourth band + route** — *he searches her and finds nothing, and says it was never about what she was carrying* · `hub_bastien` gains a **third band** · the seat-the-key rung retires. ⚠️ **`logic = "OR"` cannot express this** — one logic per block, no nesting — so it is exclusive choices, provably partitioned. **The Bastien loop stays playable**; what changes is that the key stops being the price of admission | `bastien_backroom` · `underworld_bar` · `kess_berth` |
| 20c | **quest card M** *(rev 128)* | Story-Goal — **end-of-build** | `leash_cut is_true`, and **one clause**, because it points at nothing. ⚠️ **Mandatory for the SEVENTH time in this chapter**, and the worst possible place for the spine to go blank. **The first card in the ladder that is not a frontier** — every card D→L was *prior-stage is_true + next-stage is_false*; this one reads as an **ending**: what she took, what she found out, and the one door left open. It carries the build boundary and the Support-Us ask, does not name Cain, and does not claim she has the name | Quests page |

⚠️ **Scene 13 is ONE canvas, not four — but the variants are NODES, not `[group]` bands** *(corrected at rev
121, when it was built)*. The original reason for one canvas holds and the canvas count is unchanged. What
changed is how the four generations differ inside it. `[group]` bands are the right tool for a **one- or
two-line** variant — that is what scene 12's build talk is, and its bands stay bands. They are the wrong tool
for a variant that is **four to six beats with its own cascade**, because §7 check 2 folds the entire node lead
into beat 0's measured unit: four multi-beat bands parked there measure as one ~250-word beat even though
exactly one renders, and no honest reading of the audit gets you out of it. Per-generation **nodes**, reached by
mutually exclusive **choice** conditions (`gte` + `lt`, the shipped `rung_renner_tease` shape), give each try its
own exit, its own beat count and its own word budget — and they sidestep the adjacent-`[group]` merge trap
instead of managing it. The merge trap itself is unchanged and still governs scene 12: **adjacent `[group]`
blocks merge into a single if/elseif chain, so bands must be mutually exclusive or every band after the first
ships dead.**

⚠️ **A choice's effects fire on CLICK; an exit block's fire on RENDER** *(rev 120's finding, first acted on at
rev 121)*. Scene 13 puts the burn and the bump on the routing choice for exactly that reason, so the loop's
central state transition belongs to the instant she reaches rather than to her arrival in the room. Anywhere a
canvas's closing state should be **earned by finishing it**, the state has to ride a choice. And when **no**
choice passes its conditions the engine does not dead-end: it emits a `console.warn`, a `$flags.debug_mode`
diagnostic listing every failed predicate, and a player-facing `[[Continue->…]]` escape that fires no effects
(`v2.py:12890-12946`) — so a conditional-routing exit is safe to author one branch at a time.

⚠️ **`requires_npc` DOES NOT GATE AN AUTO-FIRE** *(engine, found live at rev 119; bounced up, not patched
quietly)*. `selectAutoFireCanvasForLocation` (`v2.py:4447`) filters on `isRepeatable` / `triggerMode` /
`substitutionOnly` / `isCanvasValid` + priority and **never reads `requiresNpc`**; `isCanvasValid`
(`v2.py:4567`) checks schedules, conditions and repeatability only. The field bites on the Lane-2/3 random path
(`v2.py:5247-5261`) and in the portrait renderer, and nowhere else. Scene 9 shipped at rev 118 with
`requires_npc` alone and **fired at 12:00 in a padlocked, empty room**; scene 10 did the same until it was
caught. The gate that actually bites for an auto-fire is an **`npc_at_location … is_present` predicate in
`conditions`** — the same predicate scenes 7 and 7b already use from the absent side. Both canvases now carry
it, and `requires_npc` is kept beside it as the statement of intent. **Every future auto-fire in this chapter
that depends on someone being in the room needs the predicate, not the field** — that is scenes 15 and 17.

⚠️ **An auto-fire that exits into its own location will chain.** Scene 9 exits to `mercer_room` with Mercer
still in it, so on the bare flag scene 10 fired in the same breath — and scene 10's lead (*"He is pouring before
the door is properly shut"*) is a lie about an evening she never left. The meter is the separator: scene 9 opens
at `relation 12`, scene 10 needs **15**, so at least one more visit runs through scene 8's after-band first.
Deliberately **not** `days_since_flag`, which would have said the thing more exactly and fails **CLOSED** when
`flags_meta.set_day` is absent (`v2.py:3979`) — a spine gate that can hard-lock the chapter on a metadata gap
is not worth the flavour.

⚠️ **An exit block's `flagEffects` and `time_progression_minutes` fire on RENDER, not on the exit click**
*(engine, verified in the built HTML at rev 120)*. They are emitted as passage-level `<<script>>` at the bottom
of the canvas's node passage — `setup.applyAndNotifyFlag(...)` and `advanceTime(n)` — so the flag is already set
and the clock already moved while the player is still clicking through the cascade. Scene 10 is byte-identical
in shape, so this is how **every** canvas in this game has always set its flags; it is a fact to design with,
not a defect. Two consequences worth holding: a player who enters a canvas and leaves by any other route
**keeps** its flag (correct here — she has had the conversation and cannot un-have it), and a canvas must never
be written as though its closing state depends on the player reaching the last beat.

**Gates & state (extend-only).**
- **Traits (new, hidden):** `mercer_attempts` (0→4, the loop counter — and, since rev 120, the **only**
  generation counter: it bands both the install talk and the attempt canvas) · `part_held` (0/1 — bought and in
  her pocket; the arm, the shipped `repair_armed` shape) · `part_installed` (0/1 — seated and live; burned back
  to 0 by every attempt) · ~~`part_gen`~~ **dropped at rev 120**: it counted the same thing `mercer_attempts`
  counts, they move in lockstep by construction, and two counters for one fact is a desync waiting to happen ·
  `mercer_drains_done` ·
  `bastien_drains_done` · `controller_state` (0 = idle, 1 = running) · `controller_charge` (bounded; reload at
  the bench) · `feed_line_days` (0→3, the upkeep countdown — **rev 114, renamed from `rent_paid_through` and
  re-shaped**: a paid-through *day index* is NOT authorable, because effect values are literals only
  (`v2.py:13519-13578`, a string expression silently becomes 0) and no condition type reads the clock
  (`v2.py:3816`+ — only `days_since_flag` touches `time_state.day`). It is a **decaying counter** instead: set
  to a literal 3 by the cot's paid night, decremented 1 per day rollover by `[player.trait_decay]`
  (`v2.py:5532-5544`, floors at 0), read by an ordinary `trait gte 1`). **Drains are TRAIT counters, not flags** — a triggerless drain
  canvas has no located setter and the flag-chain validator hard-fails (shipped precedent:
  `calloway_drains_done`, `colm_drains_done`).
- **Flags (new):** `berth_home` · `file_shape_known` · `print_needed` · `mercer_found` ·
  `mercer_hospitality_open` · `owner_print_taken` · `parts_loop_open` *(rev 120)* · `owner_drained` ·
  `bastien_hub_open` · `leash_cut` · `file_read`.
- **Location (new):** `mercer_room` (`entry_from = underworld_market`; ordinary — no seal, no lock machinery).
  The part-stall is a **canvas at `underworld_market`**, not a location. `bastiens` stays unbuilt.
- **NPC schedules (new):** `npc_mercer` @ `underworld_bar` (evenings) **and** @ `mercer_room` — a declared
  schedule is what makes the engine render a portrait hub. `npc_bastien` @ `underworld_bar` (evenings) — **his
  first schedule ever**; he has carried the largest prose block in the game with no way to be met.
- **Meter mechanic:** the controller is a **carried switch with a state**, mirroring the shipped
  `equipped_weapon` / `drain_charge` loadout — carried or not, *running* or idle, costs power, reloads at the
  bench. **It surfaces ONLY on blocked targets.** Renner, Calloway, Colm, Marsh and the brothel were never
  blocked and gain **no new step**; adding a toggle to shipped content would tax the whole game for one
  chapter's mechanic. After the extraction the switch and the block are both gone.
- **Rent is an authored `coin` sink, not the engine `[settings.rent]` system** — we want a soft stall (Kess
  doesn't work this week), not eviction, and a global engine system turned on mid-shipped-game is a change we
  don't need.
- **Every new `conditions` block carries `version = "1.0"`** or it fails **open**; new gates are traits, not
  triggerless flags.
- **Reset the shared sex-loop traits on entry and exit of every new loop.**
- **Save-safety:** additive only — no `id`, live flag/trait key, stat scale, tier threshold or title changes.
  The **one** gate change (`kess_berth` drops its `salvage_done is_false` clause) **opens** a shut door and
  *heals* every 0.1.7 save currently stranded on the strip. The returning-player recovery is **mandatory**:
  scene 1 gates on `archive_1a_done is_true` + `berth_home is_false`, never on a new upstream flag, or every
  player who already finished 1a is locked out forever. The "parts" are a **trait counter, never a wardrobe
  item** — the backfill has no wardrobe branch (`cover_analyst` post-mortem).

**Media:** the berth bunk + the feed line · the market part-stall · Mercer's stall and his back room · the
drink at the Undertow · Kess seating a part at the seam · the three attempt-failures (reuse the Mercer serve
pools; **the clamp beat is a new slot** — her body locking under him) · the first-fire loop + the control
canvas · Bastien's door-search · his back room + finisher · the extraction, and her page. `search_queries`
written at authoring; the engine silent-skips missing clips, so beats build text-only until harvested.

**Step-6 resolutions — the authoring contract** *(full record: `design_the_leash.md` §14, §16)*
- **The loop is count-locked** (3 failures + 1 win), `is_repeatable=false` on each band's payload —
  staged-and-distinct is the point; a repeatable loop re-ships the mopoga "grind not content" review.
- **Each failure fails DIFFERENTLY.** Nothing → it bites back → it works for a second. An N-times null result
  is the defect, not the design.
- **Coin NEVER blocks the mainline.** The free crash-rough floor means the player can always sleep; rent gates
  *Kess's progress*, never her ability to act.
- **Lane-4 capstones run 10–20 beats** (more beats, not thicker beats); Lanes 1/2/3 at ~35–40 words per beat.
- **Narration : dialogue ≤ 1.5 : 1 in every scene with a present NPC.** Vesper currently runs 7.25 : 1 — the
  corpus's longest-standing defect. Mercer is the natural place to fix it: he talks constantly, about himself,
  and every line of it is characterisation.
- **Her interior stays rationed** — one `thought_bubble` per scene, and **she never narrates a plan.** The
  attempts are written as things happening *to* her body. The moment she is seen being clever, the character
  breaks.
- **Mercer never learns anything, ever.** No dawning, no begging, no growth.
- **Ceilings — three signed and two of them now SPENT, one still open.** **Mercer-nostalgia + the drain
  inversion is SIGNED (rev 119**, at beat_0074, gaining clause (iii): warm and crude in the same breath) — and
  **SPENT at rev 124** on `cap_first_fire`, which is the one explicit spend its own budget line reserved.
  **Kess-invasive is SIGNED (rev 120**, at beat_0075, gaining clause (iii): the install is explicit and it is
  *not sexual*). **The governor acting on her body is SIGNED (rev 122**, at beat_0077; read again at rev 123
  and not re-signed, because a ceiling is a maximum and not a quota). Only **Bastien-outside-the-cell** is
  **SIGNED at rev 126** (LO's call at `beat_0081`) — **NOT widened**, and gaining two clauses at signature:
  **(i) he never learns what she is** and **(ii) she is never shown enjoying it**. Scene 17 (the reveal)
  shipped one beat earlier with nothing explicit in it and the search promised rather than played; scene 18
  is where the row was actually due, and it is spent there on the search. **Every ceiling in the game is now
  signed, and the chapter has no content blocked on a signature.**

**Plan seed:** `beat_0068` (restore the 1b on-ramp) · `beat_0069` (rent + the feed line) · `beat_0070` (the
read) · `beat_0071` (the ask) · `beat_0072` (Mercer resurfaces + `mercer_room`) · `beat_0073` (his hub + the
drink ladder) · `beat_0074` (the print) · `beat_0075` (the parts system) · `beat_0076` (try 1 + finding 1) ·
`beat_0077` (try 2 + finding 2) · `beat_0078` (try 3 + finding 3 — the set) · `beat_0079` (the first fire) ·
`beat_0080` (Bastien walks in + the search) · `beat_0081` (his hub + the routes) · `beat_0082` (the back room
+ the drain) · `beat_0083` (the extraction) · `beat_0084` (Quests page) · `beat_0085` (media pass) ·
`beat_0086` (clean ship + deploy). All `status=planned`.

### Content register & ceilings (the authoring contract)

> The crudeness ceiling + the non-con floor, declared before authoring (`kink-ceilings.md` — a scene that
> touches an *undeclared* ceiling doesn't ship). Step 7 reads this before writing any hot beat.

**Vocabulary ceiling — per NPC, per tier (full crude EARNED at the peaks):**
- **Renner** — maximum/rough at the peaks: real anatomical words (cock, cunt, cum, ass) at the office sex, the
  loop, and the anal-drain. The soft rungs (tease / flash / the cold-boss early beats) stay **un-crude** — the
  crudeness is earned by the climb, off at the bottom.
- **Mercer** — maximum/rough at the punishment + serve-loop peaks; his register is **ownership-degradation**
  ("my investment," "asset," used like furniture), crude where he uses her, never warm.
- **Bastien** *(declared rev 62; register RE-SPEC'd rev 64 — he carries the captivity chunk)* — **maximum,
  from the first scene.** There are no soft rungs in the cell; she arrives at his ceiling. His register is
  **hot and degrading**: he gets off on her and he says so — slut, hole, bought-and-paid-for, a thing that's
  been passed around. Full crude throughout (cock, cunt, cum, ass, tits, throat). His *ownership-as-curiosity*
  survives **underneath** — he is still cataloguing her, still writing numbers — but it now runs as cold
  subtext *under* the meanness, not as a brake on it. He degrades her **and** operates her; the read-out is
  the horror the degradation rides on. *(Rev-64, LO's call: the earlier "clinical, not hot / he does not
  degrade her" ceiling is struck. He is hot.)*
- **The crew** — **faceless but loud.** No names, no NPC records, no portraits — hands and voices only, spoken
  as quoted lines in the narration, never as named speakers. But their register is **decoupled from Bastien's**
  (rev 64): they are a jeering pack, crude and mean and enjoying it, egging each other on. Their character is
  still that they have none — interchangeable, a wall of voices — but the wall talks, and it's filthy.
- **Salvage — Kess + the test-bodies** *(rev 65; see `## Salvage — The Repair`)* — a **new register: clinical
  and consensual.** Kess narrates a body the way a mechanic narrates an engine (hardware, not woman); the
  brought bodies (Tolly, Reeves) are functional, willing, and hot at the ceiling (real anatomical words) but
  carry **no degradation and no "she wanted it"** — the point is she is being *operated*, not desired.
  Explicit, no non-con, no ownership-diction. The one exception is the **Stage-A glitch-leak**, the chunk's
  single Tier-3 spend (reuses the release beat's devices).
- **Calloway — the belief-lever seduce-in** *(rev 69; see `## The Archive` + `### Calloway`)* — **maximum /
  RTS-flat at the peaks** (real anatomical words — cock, cunt, cum, ass — at the oral rung, the loop, and the
  anal-finish drain). The soft rungs (believe-him, contact) stay **un-crude** — earned by the climb. His register
  is the **belief-lever**: surrender = *being believed / allowed to stop being the hunter* — **cold and grateful,
  never a domme performance and never warm** (§2's "no warmth" holds; reserved for Cain). The **anal finish IS
  the drain** (canon). **No** degradation-diction (that's Mercer / Bastien), **no** "she wanted it." 1a spends
  **zero Tier-3.** *(Vane = N/A — no sexual content.)*
- **The Leash — Kess, the install work** *(drafted rev 112; **SIGNED rev 120**, LO's call at beat_0075, with
  clause (iii) added at signature; see `## The Leash`)* — Extends the Salvage row above: **clinical and
  consensual**, hardware not woman, explicit at the ceiling with **no degradation and no "she wanted it"** — she
  is being *operated*, not desired. What is **new** relative to Salvage: the work is **invasive, repeated, and
  she is awake for it** — he opens the seam at the base of her spine (the same seam Bastien's men opened to
  disarm her) and seats a prototype in her, four times. His register stays flat and technical throughout; the
  horror is that it is routine. **No** ownership-diction (that's Mercer / Bastien). Tier-3 budget: **zero** —
  the installs are Tier-2 work beats; the chunk's Tier-3 spends are the file-shape read, the first fire, and
  the extraction.
  **(iii) Added at signature — the install is explicit and it is NOT sexual.** The Salvage row's *"explicit at
  the ceiling (real anatomical words)"* was written for scenes with sex in them: the crude words there sat on
  the brought bodies fucking her while Kess narrated. The install has no sex in it at all — it is a man's hands
  inside a seam at the base of her spine while she lies face-down on a bench. So the precision here is
  **anatomical and surgical, not erotic**: what he opens, what he seats, how deep, how long she has to stay
  still. She is bare from the hip because that is where the seam is, and the scene never once treats that as
  nakedness — he does not look, does not comment, does not soften, and there is **no arousal anywhere in it, on
  either side.** **No pain either**: pressure, and a wrongness she has no word for because she was never built
  to be given one. Not comforted and not hurt — **handled**, and that is the horror. It is quieter than the
  cell and it should read that way.
  **And the words stay on HER BODY, never on the hardware.** Rule 9 names this game's own drain/plate/socket
  lexicon as the anti-pattern, and a whole scene about a man installing a component is the maximum-risk case in
  the corpus for reproducing it — `cap_file_shape` already took this exact ruling for the file-reading beat. So:
  her breathing, her hands, the thing she can feel him doing inside her housing that has no name — never an
  inventory of parts. Her interior stays at **one** `thought_bubble` and she never narrates a plan.
- **The Leash — Mercer, the visits and the inversion** *(drafted rev 112; **SIGNED rev 119**, LO's call at
  beat_0074, with clause (iii) added at signature; see `## The Leash`)* — Extends his ownership-degradation row
  above, which stays exactly as it is at the peaks (full crude, *my investment*, used like furniture). Three
  things that row did **not** cover: **(i) the nostalgia warmth** — down here he is *fond*, generous, pleased to
  see her, pouring drinks and telling the story about the penthouse. It is real and it must **never** read as
  affection *for her*: he is lonely for **himself**, for the man who had an asset, and she is a souvenir. If it
  plays as a sad old man missing a friend, he breaks and the chapter's ending stops landing. **(ii) The
  inversion**, at the drain only — for ten minutes it is **his** body answering with his will never consulted,
  which is the exact sentence this game has used about her since beat one. Ownership-diction is pointed
  **backward** only after the drain fires, never before. He is never degraded *by her* and she never gloats.
  **(iii) The underworld use-scenes — warm and crude in the same breath.** The shipped row's *"never warm"* was
  true upstairs and stops being true down here, and the collision is the point. He uses her exactly as he always
  did — unhurried, proprietary, her body answering while her will is never consulted, full anatomical words
  (cock, cunt, cum, ass) — and he is **pleased the whole way through**, talking about the penthouse while he is
  inside her. The fondness is aimed at **himself**: he never praises her, never thanks her, never asks, and he
  does not degrade her either, because she is furniture he is fond of and furniture doesn't need insulting.
  **No** name-calling, **no** escalation of cruelty — the obscenity is that he is having a nice evening. That is
  the register for every Mercer use-scene in this chapter, the loop included. ~~**Held back on purpose:** anal is
  reserved for the loop and the first fire, where the immunity and the drain live (`mercer_finisher` already
  canonises that nothing passes to her on his anal finish), so the print scene is vaginal.~~
  ⚠️ **THAT CLAUSE IS AMENDED AT rev 140 (`beat_0090`) — LO's call, and it is struck rather than deleted so the
  reasoning stays readable.** `cap_owner_print` now runs his whole ladder and **finishes on an anal cum**. The
  argument for holding it was **escalation**, not mechanism: with anal spent at the print, the chapter has no
  act left to climb to. LO judged the scene mattered more than the reserve, having heard the objection twice.
  ⚠️ **Two things moved with it, and the second is a small vindication.** (1) `loop_mercer_lockup`'s two anal
  entry choices carried `controller_off is_true` for the sole purpose of protecting this reserve; they are now
  **ungated**, because a gate that hides an act she has already performed is worse than no gate. (2) That makes
  `loop_mercer_finisher`'s **exit D** (`controller_off is_false` → `.cold`) reachable **for the first time** —
  and `beat_0087` kept D deliberately as an unreachable guard, writing its payload then, against exactly this
  edit. The note there reads *"if a future edit opens the anal pose earlier, this catches it with the correct
  payload instead of dead-ending the player at the finish."* It did.
  ⚠️ **What did NOT change:** the drain still reads correctly, because the immunity was never about the hole —
  `mercer_finisher` canonises that **every** finish of his passes her nothing, so the print's failed reach and
  the loop's three failures still say *this man is dead*, not *wrong act*. The vaginal beats keep their act and
  lose only their finish; there is one finish in the scene, not two.
  **Budget — two axes, not one** *(corrected at signature)*: the **explicit** spend is **one**, the inversion at
  the first fire. The **beat-count** tier is separate and unbudgeted here — `cap_mercer_resurfaces` shipped at 14
  beats and `cap_owner_print` at 14, both Tier-3 by density, neither an explicit spend. The row previously read
  *"Tier-3 budget: one (the first fire)"* and conflated the two.
  **SPENT at rev 124 (`beat_0079`) — `cap_first_fire`, and the row is now closed.** The explicit spend landed
  exactly where the row reserved it, so **no new signature was owed and none was taken**. Clause (ii) is the
  scene's spine: for ten minutes it is his body answering with his will never consulted, and the
  ownership-diction points **backward** only — at what was done to *her*, never at him. He is helpful, even,
  entirely himself under the drain (*"he answers the way a man answers in his sleep"*), and **she never
  gloats**, which the live suite asserts by grep alongside the absence of name-calling. Clause (iii) is the act
  that carries it: the held-back anal, warm and crude in the same breath, and he is pleased the whole way
  through and still pleased at the end. Worth recording for the chapters after this one: **the row's hardest
  clause turned out to be a subtraction rather than an addition** — the discipline was in what the canvas
  refuses (no begging, no revenge, no degradation *of him*) far more than in how far it goes.
  **EXECUTED, not extended, at rev 138 (`beat_0088`).** The row was signed and then written **under**: measured
  across the chapter's nine Mercer canvases, 110 prose units held **two** carrying three or more explicit words,
  against 50–71% in the shipped sealed-cell canvases on the same instrument. Clause (iii) is not a budget — it
  says *"that is the register for every Mercer use-scene in this chapter, the loop included"* — so the heat pass
  owed **no new signature and took none**. What it changed: `cap_owner_print` gained three act rungs (tits, on
  her knees, the throat) and had its six existing act beats re-cut from one crude word each to three; the loop's
  three pose nodes had their narration moved off *the arrangement* and back onto bodies; all seven
  `mercer_drain_canvas` leads got the body back. **The reserved anal held** — it is still unspent at the print,
  for the reason this row already gives and because canon (`5_scenes.toml:283`) makes his ass finish pass her
  nothing, so an anal finish at the print would turn the loop's three failed reaches into *wrong hole* rather
  than *this man is dead*. ⚠️ **The throat is an unhurried hold, not a face-fuck** — LO's call, taken against his
  own first phrasing once this row's *"never once had to raise my voice at you"* was put next to it. The
  escalation is duration, and it is the clearest case yet of the row's own lesson above: the discipline is in
  what the canvas refuses. 2/110 → 10/113 = 8.8%.
  ⚠️ **TWO MEASURED DEFECTS FOUND DURING THE PASS — (1) is CLOSED at rev 139, (2) is still open.**
  **(1) Mercer's pose nodes were ~3× the house size. CLOSED at rev 139 (`beat_0089`), on LO's call.** Measured
  across every sex loop in the game: Colm 36/39/68, Renner 34/37/43, Calloway 47/38/59, Bastien 53/67/193 — and
  **Mercer 133/97/118**. They inherited whole multi-beat paragraphs when `loop_mercer_attempt.base` was folded
  into pose nodes at rev 137, and a pose page is re-entered **4–6 times per visit**, which is exactly the
  surface Rule 2 protects. Each node now merges its two paragraphs into one and keeps **one** short line of his
  instead of two — **55 / 54 / 85** — and each still carries 3–4 explicit words against Colm's 1–2. The house
  shape is *video + one paragraph and no dialogue at all*; Mercer keeps a line because clause (iii) is a man
  **talking through it**, and that is the recorded deviation rather than a miss.
  ⚠️ **AND ONE DEFECT THIS ROW ITSELF CAUSED, ALSO FIXED AT rev 139.** The clause *"anal is reserved for the
  loop and the first fire"* was enforced by a suite line (`live_beat_0074:148`) reading
  `not re.search(r"\b(anal|ass|arse)\b", …)` — a ban on the **word**, standing in for a reservation of the
  **act**. `beat_0088` copied that shape into its own guard and then satisfied it by **deleting LO's ass-grope
  rung** from the print's ladder. Both guards now match the act (`\banal\b`, `in/into/up her ass`,
  `fucks/takes her ass`, `cock … ass` inside one sentence) and both additionally assert the grope is *present*.
  Worth keeping beside this row's own lesson above: the discipline is in what the canvas refuses — but the
  **test** has to refuse the same thing the row does, and a word-ban is not that.
  **(2) `mercer_drain_canvas.d1#b6` measures 52 words** against the 50-word band. It is the node's one interior
  beat and it arrived verbatim from `cap_first_fire`; two words over, recorded rather than silently trimmed.
- **The Leash — the governor acting on her body, outside the cell** *(new row, drafted and **SIGNED rev 122**,
  LO's call at `beat_0077`; see `## The Leash`)* — Governs **tries 2 and 3**, where the thing at the base of her
  spine does something to her and no other row reaches it. Every row above governs a **person's register** —
  Mercer's what he does, Kess's what his hands do, Bastien's what he says. This one governs **her body acting on
  its own**, which is why it is a row rather than a clause bolted onto someone else's. *(Measured before it was
  drafted: across the whole scenes file there were exactly two pieces of pain-register prose — the cell's
  overflow, which the re-spec below scopes to `captive_room` and says so, and `kess_install_part` stating
  explicitly that what she feels is* not *pain. Damage to her outside that room had never shipped.)*
  **(i) The clamp is damage and it is NOT sexual.** No forced orgasm, no arousal, no ecstasy-as-damage. The
  governor is *design, not damage* in `salvage_verdict`'s own words — a **guard**, and a guard bites the way a
  machine bites. Her body goes rigid and wrong, and the words stay **anatomical and physical**: what locks, what
  she cannot move, what she cannot make herself stop doing. No pleasure anywhere in it, on either side.
  **(ii) The captivity re-spec below is NOT widened.** It stays scoped to `captive_room` exactly as written.
  This is **one event, once** — not the cell's sustained-damage register. No pack, no restraint, no *"used until
  the machine inside it breaks,"* no forced orgasm as damage, and nothing that reads as a scene about hurting
  her for its own sake. Tier-3 budget: **zero** — these are Tier-2 loop beats.
  **(iii) The charge is CONCEALMENT, not pain.** The camera is on what she does to **hide** it — her hands, her
  breath, the sounds she does not make, how long she has to hold — and on Mercer being pleased and inches away
  and oblivious. **Pain as spectacle is the failure mode.** A woman going quietly rigid under a man who is still
  inside her and still telling a story about the penthouse is the beat. **He never finds out**, and there is no
  fail branch, but it has to read as very nearly failing.
  **(iv) She never narrates it as a plan or a diagnosis.** One `thought_bubble`, and it observes. Kess does the
  diagnosing, one line, on the next bench.
  **Note added at rev 123 (`beat_0078`), after building try 3 against it.** Clauses (i) and (iii) are worded
  around try 2's *clamp*, and **try 3 has neither a clamp nor anything to conceal** — canon is explicit that a
  drained man notices nothing, so Mercer has nothing to misread and she has nothing to hide. Try 3's charge is
  **loss**, not concealment. That is not a breach, because **a ceiling is a maximum, not a quota**: try 3 spends
  *less* of this row than try 2 did, and no re-signature was taken. What still binds and still fits is (i)'s **no
  arousal and no pleasure, on either side**, (ii)'s **Tier-3 zero**, and (iv). The register risk worth naming is
  that *the leash lets go while a man is finishing inside her* invites a wrong reading — that she feels pleasure
  for the first time. She does not: the leash suppresses her **drain**, not her body, so the beat stays inside
  the game's shipped instrumental drain lexicon and the test asserts that vocabulary is **present** as well as
  asserting the banned one is absent.
- **The Leash — Bastien, outside the cell** *(drafted rev 112; **SIGNED rev 126**, LO's call at `beat_0081`,
  with two clauses added at signature; see `## The Leash`)* — **the last row in the game to be signed.**
  ⚠️ **THE SURFACES THIS ROW GOVERNS ARE SHELVED OUT OF 0.1.8 (rev 141, `beat_0091`), AND THE ROW IS NOT
  RETRACTED.** LO's call: the search, the back room, the loop and the drain were authored at rev 126–127 and
  never received the heat pass revs 138–140 gave the Mercer surfaces, and shipping the next chapter's
  antagonist at that standard spends him for nothing. All seven canvases, the `bastien_backroom` location and
  his schedule row now live in `games/vesper/shelf/bastien_present_day.toml`, which is outside `toml_phases/`
  and therefore never merged. **The signature stands as signed** — it is a ceiling on content that exists and
  is coming back, not a promise about a release. Nothing below is re-scoped, and 0.1.9 restores the block and
  then does to it what `beat_0088`–`0090` did to the Lockup. **Blueprint rows 18, 18-note and 19 below describe
  shelved content and are left exactly as written**, because they are the spec the restore is measured against.
  **The captivity RE-SPEC below is NOT widened.** It stays scoped to `captive_room` exactly as written: the
  Undertow back room runs at the **ordinary owned-slave floor** with his declared crude, degrading diction on
  top (slut / hole / bought-and-paid-for; full anatomical words; the anal finish IS the drain). **No** pack use,
  **no** restraint, **no** sustained non-con — the crew are voices through a wall, never hands. The charge here
  is not the cell repeated; it is **the search at the door** (unhurried, public, and she has to stand for it)
  and what she is smuggling past it. His *ownership-as-curiosity* runs on top rather than underneath now — he is
  openly, pleasantly interested in what she has become. Tier-3 budget: **zero** in this chunk.
  ⚠️ **Scope clarified at rev 125 (`beat_0080`), and it unblocked a beat.** This row governs **two** things and
  only two: **the search at the door** and **the back room** — blueprint row 18 says the door-search is
  `hub_bastien`'s gate, and row 19 owns the back room. It does **not** reach blueprint row 17, the reveal, which
  is why `cap_bastien_walks_in` shipped while the row was still unsigned: nothing explicit, no nudity, no touch,
  and the search **promised in his own mouth rather than played**. The precedent is `rung_mercer_hands_on`,
  built at `beat_0073` under an unsigned Mercer row on exactly this reasoning. His crude, proprietary diction in
  that canvas (*"my property"*, *"you of all things"*) is his **shipped Act-1 ownership register** and is not
  what this row adds. **`beat_0081` is the beat this row actually gated, and it is signed there.**
  **(i) Added at signature — HE NEVER LEARNS WHAT SHE IS.** The drain takes his answers and nothing goes the
  other way. He is allowed to be *closer* than anyone in the game has been — he is the only man who has looked
  at her properly, he has a drawer of notes, and every line of his hub talk circles it — and he still ends the
  chapter not knowing. If he works it out there is no Bastien left for the next chapter, and the reveal that
  matters is **his**, not hers.
  **(ii) Added at signature — SHE IS NEVER SHOWN ENJOYING IT.** The back room is **work**. The charge is what
  she is carrying and whether it got through the door, never what he does to her — no arousal-as-consent, no
  "she wanted it", and no arousal register on her side anywhere in the chunk. This is the shipped
  owned-slave floor held rather than widened, and it is what keeps the smuggling the subject of the scene.
  **SPENT, first, at rev 126 — `bastien_door_search`.** The search is the row's own named charge: unhurried,
  public, his hand at the seam **his men opened**, and she has to stand for it with a bar full of people
  behind her. **There is no fail branch** — she always gets in, and what varies is whether what she needs got
  in with her — because a fail state would make it a lock-picking minigame and turn the beat into
  pain-as-spectacle, which the rev-122 row already named as the failure mode. The live suite asserts the row
  from both sides: no pack / restraint / sustained-non-con vocabulary, no arousal on her side, no
  damage-as-spectacle, Cain never named — and the charge the row *does* name present on the page.
- **The soft / non-sexual surfaces** (hubs, ambients, work, the cradle) stay flat and clean — no gratuitous
  crude on a re-readable everyday beat.

**Non-con / dubcon FLOOR (the owned-slave register).** She is **property, used at others' will** — Mercer owns
her (she cannot refuse), the targets believe they're using her. Her **body responds while her will is never
consulted** (the opening punishment is the template: "her body answering" while she's used in front of the
units). The prose may depict the ownership, the degradation, the can't-refuse — that's the floor. It stops at
**used-and-degraded, not brutalized-for-gore** (no torture/mutilation unless re-specced). The opening office
scene is the first canvas that needs this floor.

**RE-SPEC — the captivity ceiling (rev 62; widened rev 64; see `## Captivity — The Room`).** The clause above
reserved the right to go further *"unless re-specced."* This is that re-spec, and it is **scoped to the cell
only.** Inside `captive_room`, the ceiling lifts to: **restraint and BDSM · gangbang · spitroast & DP · forced
deepthroat · forced orgasm as damage · anal as the inverted drain · sustained non-con (she is taken, not
seduced) · her body used until the machine inside it breaks.** Widened rev 64 (LO's call) to also include:
**spit / drool / face-use · marks & rough handling (slaps, bruises, handprints, choke-marks) · piss / heavier
degradation.** Nothing is softened, nothing is cut away from, no scene fades. The chunk exists to be the game's
hardest stretch.

Two lines the re-spec does **not** cross, because they'd break the fiction rather than the taste:
- **The lasting damage is to the machine, not the meat.** Her *core* fails — overloaded, cooked — and that is
  the injury that follows her out. The *meat* may be marked in the moment: spat on, pissed on, slapped,
  bruised, choke-marked, handled rough. But **no gore, mutilation, dismemberment, or permanent bodily
  injury** — she walks out whole (marked, not maimed) and broken the way a machine breaks. The horror is the
  read-out, not a wound. *(Rev-64: the earlier flat "not the meat" line is loosened to permit surface marks;
  the core-break stays the only lasting damage.)*
- **It stays scoped.** The lifted ceiling applies in the cell and nowhere else. Mercer's, Renner's and the
  brothel's registers are unchanged. She leaves the room; the room does not leave with her.

*Everything outside the cell keeps the original floor.*

**The control-canvas (the drain) — voice carriage (Rule 4).** The extraction is **played as a Q&A exchange in
HIS own dialog** — his answers under her command, his voice breaking — **not narrated summary** ("she drains
the payload"). It's the hottest target beat; it must be spoken. The reusable pattern carries this note, so
Bastien/Calloway inherit it.

⚠️ **MEASURED at rev 124 (`beat_0079`): the rule had never once been executed, and three canvases shipped
against it.** `loop_renner_finisher.drain` (*"She asks the only thing she came for… He tells her."*),
`calloway_drain_canvas.d0` (*"he gives it up without knowing he's giving it"*) and `colm_drain_canvas.d0`
(*"the whole compartmented, careful little mind of him comes loose"*) contain **zero player dialog blocks
between them** — every one of them is exactly the narrated summary this note names as the failure mode.
`cap_first_fire` is the first canvas to play it (6 questions against 13 answers) and the payoff was immediate
and measurable: the canvas lands at **0.93 : 1**, the best in the game, and it moved the whole-game ratio
2.80 → **2.72 : 1** in a single beat. **The three shipped canvases are NOT retro-fixed** — they are released,
and this is not their beat. What the measurement changes is the standing of the rule: a sentence in a design
book was not enough to make it happen three times running, so the worked example was folded into the skill
(`beat-authoring.md`) at the same revision.

**Wren's interior (the flat surfaces).** Her in-the-moment reads (the cradle, the glitch beats) sit in a single
`thought_bubble`, flat and terse; **Tier-3 is spent ONLY on the two once-only glitch capstones** (glitch II
heavier than I). The recurring cradle-leak ambient was considered and **cut** — her thread stays lean: rarity
is the punch. **This holds for the deepened captivity shelf scenes too (rev 64):** however long a scene runs,
her interior is **one clipped `thought_bubble` apiece** — the prose spends on what is done to her and on the
men's voices, never on her POV. The loud, degrading room around a flat blank being used is the horror; opening
her head up would soften it.

---

## The cover / disguise system (worn-state) — added during authoring

> Pulls the disguise from prose into a real **worn-state mechanic**, in Mission 1 (Renner). **LO's call: the
> cover is *issued by the company, not bought*** — she's owned; the boss provides her kit. This supersedes the
> World-blueprint §5F "clothing = narrative in the chunk" line and pulls the disguise system forward from the
> frontier. Every engine claim is code-verified (`v2.py`, cited).

**The idea (one line).** The cover is a garment she has to **put on** before a mission. In cover, the mark
treats her as the hire and the mission runs. Out of cover, she's a well-dressed stranger asking a broke man
about his business — and the world reacts wrong.

**Two states the engine gives us** (the `clothing_item` predicate, `v2.py:3587-3608`):
- **owns it** — `{ type = "clothing_item", item_id = "cover_dockhand", operator = "owned" }` (did the boss give it to her).
- **wearing it** — `{ … operator = "equipped" }` (is it on her body right now). This is the gate that matters.

**The loop (no shop — the boss provides):**
1. **Issue** — the morning briefing node hands her the cover with the dossier. Engine-native grant:
   `exit_block.config.wardrobeEffects = [ { action = "add", item_id = "cover_dockhand" } ]` (`v2.py:12503-12511`)
   — **`add`, not `equip`**, so it lands in her wardrobe **un-worn** and she must dress herself (this is what
   keeps the "not dressed" path alive — LO's locked pick).
2. **Dress** — she goes to the **rack in her room** (the wardrobe screen at `wren_room` — the "rack of faces"
   from the opening) and puts the cover on.
3. **Go** — in cover, she heads to Renner; the mission runs.

**What it gates (the mission surfaces, not every rung).** The cover is the key to the door, not the staircase
behind it: it gates the Renner **entry** (the hire + the depot/Anchor hubs); the seduction climb itself still
rides on the NPC's own **relation + corruption** as designed. Same one cover for the whole Renner mission.
- `cap_renner_hired` gains a third trigger condition: `{ type = "clothing_item", item_id = "cover_dockhand", operator = "equipped" }`.
- The depot + Anchor Renner hubs gate the same way.

**★ How it reacts when she is NOT dressed (the point of the system):**
- **Before hired, out of cover** — the hire won't fire. A clean, expensive-looking woman leaning on a
  blacklisted wreck reads as a *threat* (cop / fed / Vance). He clams up and waves her off (*"Whatever you are,
  off my stool"*). No access — the cover is exactly what makes her not worth a second look.
- **After hired, out of cover** — the work + seduction options are hidden with the reason shown (the engine
  auto-prints *"Wearing: Dock-work coveralls"* on the greyed option, `v2.py:7332`), and a short fallback beat
  fires instead: Renner squints at the nice clothes — *"The hell are you dressed like that for? …Do I know
  you?"* — the suspicion the cover exists to kill. The day stalls until she's back in cover.
- **The rule, plain:** cover on → invisible-useful, the mission runs. Cover off → the doors stay shut and
  people react to a stranger who doesn't belong. **No alarm / fail-state in Phase 1** (the leash is parked for
  Act 2) — out-of-cover is a *stall + a wrong look*, not a loss.

**Clothing equipped is sticky** (`player.equipped` persists; nothing resets it daily) — so the lesson lands
once (first outing, undressed → wrong reaction), and after she dresses she stays covered until she changes.
*(Optional future flavor, not built now: inside the Tower she's in her own/asset self for Mercer, and swaps
into the cover to go out.)*

**What it deliberately is NOT.** Not a wear-to-level grind — it's a binary identity key (in cover / not),
issued free, gating ENTRY only, never the escalation rungs (those stay on the arc spine). This keeps it on the
right side of the clothing two-part rule (`references/clothing.md` §2 — that rule forbids gating an arc on
`worn_corruption`/revealingness; gating *identity/access* on a specific issued garment is a different,
legitimate use). No "underdressed"/exhibitionism axis — the cover is about *who she's pretending to be*, not
how much skin shows.

**Build notes (Step 7):**
- **Enable clothing** in `[settings]` (the scoping trap — keys under `[settings]`, not bare):
  `clothing_enabled = true`, `wardrobe_location = "wren_room"`. **No `shop_location`** (no shopping → no shop UI
  emitted, `v2.py:1478`).
- **Full starting outfit** — every slot has an `initial = true` item (her own/asset self) so she's never
  naked/blocked and "out of cover" = "in her own clothes" (`references/clothing.md` §7).
- **The cover** — one `[[clothing]]` item, `slot = "dress"`, no price, **not** `initial` (granted at the briefing).
- **The grant** — `wardrobeEffects = [{ action = "add", item_id = "cover_dockhand" }]` on the morning briefing
  node's exit.
- **Onboarding** — the briefing tells her to wear it ("your cover's in your quarters, put it on before you go")
  so dressing is a taught step; the not-dressed beats are the backstop, never a dead screen.
- **The gate + fallbacks** — add the `equipped` condition to the hire + the two Renner hubs; author the two
  out-of-cover reaction beats above.
- Every `conditions` block carries `version = "1.0"` (or it fails open).

**Scaling (frontier).** Bastien's and Calloway's covers are granted when their missions open, tagged by
**category** (`worn_type`, e.g. `"cover_dockwork"` / `"cover_pa"`) so each mission gates on "wearing the right
*kind* of cover" — wrong cover at the wrong mark = wrong reaction. One issued garment per mission; still no
shop.

---


## The player portrait (state-reactive sidebar face) — added during authoring

Wren's face, in the sidebar **just below the time display** (above the Charge/Condition HUD) — the reactive extension of the
static `$player.portrait`, which until now only showed on the Stats page. Opt-in engine feature
(`references/player-portrait.md`): a `[player_portrait]` block in `0_systems_spec.toml`, emitted as a
`<<playerPortrait>>` widget whose `<img>` src comes from `setup.getPlayerPortrait()`.

**Shipped state: REACTIVE (two faces + naked-during-sex), live-proven.** Six portraits in
`videos/portraits/`. Corruption is DEAD by design (player frozen at 0 — the inversion) and there's no
pregnancy trait, so those two resolver axes don't apply here. What's live:

- **The two faces** — `default_image = wren_grays.jpg` (her asset-self, company grays) and an outfit rule
  `worn_type = "cover"` → `wren_cover.jpg` (the dock-work disguise). The two `[[clothing]]` dress items carry
  `type = "grays"` / `type = "cover"` (`1_metadata`), so the sidebar face swaps the moment she equips the cover
  at the rack. Both SFW, Gemini-generated from `wren.jpg` → the same woman, consistent.
- **Undress — CLOTHING-ONLY (the wardrobe rack).** The portrait tracks undress purely from what she's actually
  wearing, via the engine's native `naked_image` / `underwear_image` / `topless_image` / `bottomless_image`
  overrides. When she unequips a slot at the rack, `getUndressLevel()` (`v2.py:1454`) returns the state and the
  matching image shows *live*. **All four states are reachable from her dress+bra+briefs wardrobe** (per the
  2026-07-07 engine change — an area counts bare only when NOTHING covers it, bra=top-cover, briefs=bottom-cover):
  dress off + bra&briefs = **underwear**; + bra off = **topless**; + briefs off = **bottomless**; all off =
  **naked**. Strip her at the rack, the picture changes — and nothing else moves it.

  **The sex loops do NOT undress the portrait (LO's call, 2026-07-07).** The Renner/brothel/Mercer loops undress
  her in *prose only* (equipped stays full), so during a scene the sidebar reads as her **worn outfit** — the
  cover face on a mission, grays inside — not naked. An earlier build wired a `pp_naked` flag to force naked
  during sex (set on each intro-pose, cleared on the finisher exits); that whole mechanism was **removed** — the
  portrait is clothing-driven, period. Live-proven (headless): the wardrobe matrix
  (grays/cover/underwear/topless/bottomless/naked) all resolve, and setting `pp_naked` with her dressed returns
  the worn outfit, not naked. 0 page errors.

**Reachability note:** all four undress stills LO downloaded are **live from the wardrobe** — `underwear`
(dress off), `topless` (bra off too), `bottomless` (briefs off instead), `naked` (all off). This required the
2026-07-07 `getUndressLevel` change (bra=top-cover, briefs=bottom-cover; an area is bare only when nothing covers
it), because the old logic lumped bra+briefs into a single `underwear` state and keyed topless/bottomless off
outer garments Vesper doesn't have.

**Adversarial verification (workflow wf_2d0b29a5-86c, 4 tracers, done while the sex-flag still existed).**
Confirmed the state matrix and surfaced 4 items, all addressed at the time: a MED build-footgun (below, fixed),
a sex-loop portrait-timing quirk, a dead `daily_tick` unset trio, and the bra-only/briefs-only collapse. The
timing quirk + the whole flag mechanism are now moot — the sex-loop trigger was removed (portrait is
clothing-only); the bra/briefs collapse was fixed by the `getUndressLevel` rewrite above.

**Engine notes (Phase-A gaps caught on real builds, all fixed — benefit every game).**
1. The player-portrait media prefix defaulted to `./media` (wrong — every other generator media path uses
   `./videos`); portrait 404'd → fixed to `./videos` at `v2.py:1135`.
2. The `<<playerPortrait>>` widget shipped with **no CSS**, so the raw `<img>` rendered at natural size (2048px)
   and overflowed the ~232px sidebar — you saw a background edge, not her face. Added a `.sidebar-player-portrait
   img` rule (`v2.py` sidebar CSS): width 100%, a 3:4 `object-fit: cover` portrait crop centred high
   (`object-position: 50% 18%`) so a square/tall source frames the face/torso. Live-confirmed: img now 232×309,
   her face reads.
3. **Silent broken build when `--video-folder` is omitted** (`game_service.py:481` gated the external-asset copy
   on the flag). A rebuild without it copied nothing yet exited green → every portrait/NPC/location `<img>` 404s.
   Now the build **warns loudly** (`game_service.py` + `package_from_toml.py`): "N external media file(s)
   referenced but NOT copied — re-run with `--video-folder`". The Vesper build path always passes it.
4. `game_service.py` referenced `logger` at two sites but never defined it (a latent crash on any warning path,
   incl. the new one above) — added the module-level `logging.getLogger(__name__)`.

---


## Capability — Fighting & Stealth (day-depth, added during authoring)

The first piece of **day-depth**: things to *do* per day besides seducing Renner. Two **capability traits**
the player builds for herself:

- **Fighting** — win a straight fight (against guards). Always available, weak at first.
- **Stealth** — move unseen: slip past, go deeper, steal.

**How she builds them — the Training activity (`activity_train`, her room).** She drills in secret —
sharpening the body the company built, past the spec on her file; the one thing here that's only hers
(*the want:* stop being helpless / get where she can't yet). Two drills, Combat / Stealth, **+3 a session**
slowing to **+1** past 30 (drilling plateaus around 50; the top comes later from real use). Each drill
**costs 15 Charge** (it gates — she can't drill when too drained) and **120 minutes**, so training competes
with the rest of her day. The drill's prose escalates as the trait climbs (clumsy → sharp / fumbling →
ghost) so progress reads even before the bars exist.

**Now live (piece 2):** the **sidebar bars** for Fighting/Stealth and the **thing that reads them** — the
Burned Yard guards (below) — shipped together, so the bars are honest. The Stealth drill now unlocks the
first time she's caught at the yard.

---

## The Burned Yard (day-depth, piece 2 — the Trail crawl)

A new locked location off the Waterfront: **Renner's own yard**, the one **Cain torched in revenge** for
the two of Renner's people he killed (and their families). Distinct from The Facility (her origin site) —
this one is Renner's, so **his men guard the wreck** (he's salvaging gear / burying what he did). The
guards are **narrative, not characters** — the encounter is decided by *her* skills, not theirs.

**The crawl (this is where Fighting & Stealth pay off).** She sneaks in and **pushes deeper** (a hidden
depth meter, 0→3). Each push hits a guard, and she gets past one of three ways:
- **Slip past** (high enough **Stealth**) — unseen,
- **Take him down** (high enough **Fighting**) — caught, but she wins,
- **Use the arousal weapon** (once repaired) — caught, but she walks through,
- or **she can't, and runs** (flee — no progress, try again after training).

Guards get **tougher the deeper she goes** (10 / 25 / 50-ish), so she trains up to push further. It's
**doable untrained** — you just get caught and run — so it's a difficulty, not a wall. The first time
she's caught unlocks the **Stealth drill** back home.

**What's down there (one find per depth):**
- shallow — a **clue** (what the yard really was: shipments to the Facility — Renner moved more than he knew);
- mid — the **broken arousal weapon** (same tech as what's inside her), which she **repairs over a few
  sessions** at her room until it works (then it's the "walk past a guard" option above);
- deep — the **heart of it**: the two dead men + their families, erased, and the **thread to the
  underworld** (where the trail runs next — the Underworld is reachable off the Waterfront; its deep end,
  where Cain is, stays locked). Standing in it, a **memory flickers** (the awakening).

A **Trail quest card** tracks it (a parallel goal to the seduction): *get into the yard, work deeper.*

---

## The Underworld (day-depth, piece 3 — the dark city, her second life)

The hidden criminal city the whole hunt points to — where Cain is. The burned yard already names it; this
build makes it a **place she can go and live in**, with its own **money**. It's the opposite of the cradle:
up top she's owned; down here **no one knows what she is, and her coin is her own.** (The deep end — where
Cain actually is — stays locked: *The Site*, re-parented as the underworld's far end.)

**Sex register down here (declared ceiling).** The Underworld sex (brothel work, the arousal-weapon
pass-bys) is **explicit at the ceiling** (cock/cum/tits, the act on the page — no fade) but **COLD**:
transactional, detached, no performed pleasure — a body for rent, a weapon being used. This is *deliberately
the opposite* of the Renner/Mercer seduction heat (where she's working a man open); down here she's gone
behind her own eyes and the coldness is the point. (Interior-tic note: the "files it under nothing" / "the
way she does everything" reflexes are **rationed** — kept for the opening glitch escalation and the yard
awakening payoff, flattened everywhere they'd gone routine.)

**Getting in (every visit).** A gate off the Waterfront, always there. The guard wants **coin** — but she
can also **fight** him or **use the arousal weapon** (no sneaking past this one). First visits, with no coin,
she forces in; once she's earning, she just pays the toll. Clearing the guard is the *only* way to the strip.

**The coin economy (her second life).**
- **Earn — two ways, her two natures:**
  - **The House** (brothel) — a **full sex loop** (oral / vaginal / anal pose ladder → his pleasure climbs → she picks how he finishes: mouth / inside / ass), **coin paid on finish only** (no faucet). The thing she's used for, sold now on *her* account — cold and transactional (the declared ceiling). Same engine shape as the Renner/Mercer loops (triggerless canvases, numeric loop traits); reached from the House menu's "Take a client" rung.
  - **The Pit** — she fights for a purse → coin. The **payoff for training Fighting** (drill it at home, use
    it at the yard/gate, *earn* with it here). Tougher bouts pay more.
- **Spend:**
  - **The gate toll** (the clean way in),
  - **The Black Market** — coin buys **weapons** (a fighting edge) and **gear** (a stealth edge); the coin-fast
    alternative to drilling.

**The black market also sells people.** Behind the chain, the **pens** — bodies bought and sold by weight.
She can't buy here (deferred), but she *walks the line*, and among the merchandise is **one like her**, caged,
watching back wrong. A recognition she shuts off before it lands — the awakening, and a seed of what Cain
fights (the trafficking). Dark texture, not a transaction.

**Frontier.** The deep underworld — the don (a weekend back-office seed), the real services, and **where Cain
is** (The Site) — stays locked → *"you're in; the hunt runs deeper from here — more coming."*

---

## Reset & reload (cleanup + the loadout + the two weapon reloads — separate upkeep systems)

After she uses her body/powers hard, she's spent and has to reset. **Three distinct things** (kept lean so
it's rhythm, not chores):

**1. Condition (hygiene) — cleanup after sex.** A meter that **drops when she has sex** (the drain, the
brothel, the Renner loop). **Washed** at her room. Its one job: being **presentable to go out in cover** —
if she's filthy she **can't ride down to the Reach** until she washes (the cover won't hold). It does **not**
touch the seduction rungs — it's just *wash before each outing.* **Bounded 0–100** like Charge: the sex/weapon
drops floor at 0 and the Wash caps at 100 (clamped), so the Condition card never slides off a band and
vanishes.

**2. The drain weapon reloads.** Her truth-drain holds **one shot.** Fire it (the anal-finish extraction)
and it's **spent** — she can't drain again until she **recharges** at the cradle (*Recharge the drain*). (If
she takes him in the ass while spent — or while carrying the wrong weapon — the act still happens; there's
just nothing to take.)

**3. The arousal weapon reloads.** The emitter holds **three shots.** Each time she zaps a guard it uses
one; at empty she **recharges** at the cradle (*Recharge the emitter*). So it's a limited tool, not an
infinite skeleton key.

> **Firing it is a real beat (not a bypass).** Using the weapon plays out: she floods them with the field,
> **fucks** the one in her way, and **he passes out** (non-lethal — he wakes later, no memory, so a recurring
> guard like the gate doorman is still there next time). Because it's sex, it **drops Condition** like any
> other. So the three ways past a guard read distinctly: **Stealth** = unseen / no trace · **Fighting** = beat
> them down · **the weapon** = fuck them unconscious (the seduce-past path for when she can't fight or sneak).
> The **two fire beats carry distinct clips** — the burned-yard area-fire (`sex/yard_emitter_fire_t5.webm`,
> pending find-media) vs. the gate doorman (`sex/arousal_weapon_use.webm`) — so the same act doesn't replay
> the same video.

**4. One weapon at a time — the loadout (`equipped_weapon`).** Her core powers **one weapon at a time**: the
drain is the system inside her; the emitter is the same build scaled to her hand, drawing off that same core.
So she **carries one or the other, never both** — slot the emitter live and the internal drain goes quiet;
stow it and the drain wakes. She **swaps at the bench in her room** (*Switch weapon* — free, but it means a
trip home). Which weapon she carries decides what she can do: the **drain** only fires the Renner anal
extraction; the **emitter** only zaps guards (the yard, the gate). She **starts on the drain** (her only
weapon until she finds + repairs the emitter in the burned yard). **The first drain is no exception** — even
Renner's scripted first drain waits until she's carrying the drain weapon; the **quest page tells her when
he's ready and which weapon to bring** (it flips to "switch back to the drain" if she's holding the emitter).

**Where the weapons recharge — the cradle, two dedicated actions:**
- **Recharge the drain** — a few minutes on the feed line: reloads the drain (its one shot). No day lost.
- **Recharge the emitter** — bleeds the cradle's charge into the emitter's cell (three shots). No day lost;
  only available once she's repaired it.
- **Charge up** and **Power down / sleep** restore her **Charge** (energy) but **no longer reload the
  weapons** (LO's call: weapon reload is its own deliberate act — the three upkeep systems stay separate).

So her home base beats: **Wash** (Condition), **Charge up** (Charge), **Power down** (the day + Charge), the
**two weapon recharges**, and **Switch weapon** at the bench. The wash is also her one private, unscheduled
moment — a small thread of the awakening.

**Charge is a real throttle, bounded 0–100.** Spending it is gated, not cosmetic: the three Renner rungs
and the depot work **block when she's too drained** (greyed, "(Requires 15 …)") — she recharges at the
cradle and comes back. Two deliberate exceptions: **travel never blocks** (it only floors at 0), because the
ride back to the Spire is the *only* way to the cradle and blocking it would strand her; and the cradle
restores **cap at 100** (no overshoot). Earlier these all ran as ungated effects, so Charge could slide
below 0 (the HUD card silently vanished) or past 100 — both fixed by routing spends through `costs`/clamp.

---

## Captivity — The Room (Act 2 · Bastien's arc, part 1) — added during authoring

> **What this is.** The chunk where the mopoga review's cure finally lands. That review said *"gameplay
> boiled down to resource grinding rather than focusing on the adult content."* The Underworld Hunt fixed
> the **roster** (the game had run out of people). This chunk fixes the **ratio**: it is the densest erotic
> stretch in the game and it contains **zero grind.**
>
> Full engine record + the verified findings: `games/vesper/design_captivity_the_room.md`. This section is
> the intent. Book revision 62.

### Why it exists

It is the third *distinct* conquest verb, and that's the point:

| NPC | Verb |
|---|---|
| Renner | seduce-in |
| Marsh | scheme-and-serve |
| **Bastien** | **she is taken** |

Three identical infiltrations would be exactly the repetition we're trying to kill.

### The three tests any beat here must survive

1. **Is the player getting a scene, or filling a bar?** A meter that rises by *repeating* scenes is a grind
   bar with porn on it — it would re-ship the review inside the chunk built to cure it.
2. **Does the room have a verb?** A protagonist with no agency, given no input for three days, is a
   cutscene with a timer.
3. **Does she leave changed?** *"And then something happened"* is not an ending.

### The beat chain (locked)

1. **The grab is rewritten.** Today's capstone ends *"She wakes on the waterfront at dawn, sore and whole
   and released."* That release was wrongly authored and is **deleted.** Bastien takes her and she **stays
   taken.**
2. **She is ported into a sealed room.** No walk, no approach. She wakes there.
3. **She is disarmed.** Bastien strips the drain. This is the injury, not a detail.
4. **Three days of use**, escalating, Bastien present throughout.
5. **The break.** Mid-scene, her body stops answering.
6. **Cain.** He arrives furious, argues with Bastien behind a door, and **we never show the argument.**
   He frees her.
7. **She leaves broken.** Her gear returns; the fault does not. ← *the chunk ends here.*

Why Cain did it, the repair of her core, and Bastien's alignment with Cain are **all later chunks.**

### The room

One location she cannot leave, plus **The Door** — a locked card reading *the door does not open for her*.
The door never opens. Cain walks her out; she does not walk herself out. It exists to be looked at.

**Two verbs, and only two:**

- **Sleep.** Advances the day, restores Charge. It also carries a **guaranteed scripted night use**, so the
  ladder always climbs. Sleep cannot be used to outrun the chunk.
- **Attend** (~30 min). *Listen at the door. Watch the man on the chair. Hold still and feel the fault.*
  This is the **chance-rolled** action: sometimes nothing, sometimes someone comes in.

That pairing is the room's whole thesis:

> **The only way to learn anything is to make yourself available.**

The player who fills her days sees more and breaks faster. The player who hides in the bed sees less and
breaks anyway. Both roads lead to Cain. Nobody is punished — the choice is *how much you look at it.*

**What the room does not have:** no coin, no fighting, no travel, no shop, no NPC schedule, no
Charge-throttled repeatable actions. *If the player can spam an action in that room, it is the wrong action.*

### The physics — overload, not depletion

Vesper's established fiction: **sex is what charges her.** The drain fires on an anal finish — a man
finishing in her ass is how she *takes* something. She is a machine that eats sex.

A gangbang therefore does not drain her. **It force-feeds her.** Bastien has taken the drain, so everything
they pump into her has nowhere to go, and the core cooks.

This is why *this* breaks her when a hundred men at The House did not: **the weapon is gone.** Being
disarmed is the injury. The rape is the pressure. It is the drain, inverted — which rhymes with the
capture-instead-of-seduce inversion at the chunk level.

Each use also costs Charge. The bed restores Charge and **cannot touch the fault.** Two numbers moving
opposite ways; the bed fixes exactly one. *Overloaded in the core, exhausted in the body.*

### The meter she can watch but never spend against

`core_strain` is **visible** — a banded sidebar row, like Charge and Condition. Hidden meters work when the
player has agency to spend against them. She has none. What she has is a dial she can watch go wrong, and
that dial is the horror of the room.

| Band | Sidebar | The shelf |
|---|---|---|
| 1–24 | `Core: Nominal` | Bastien alone. Ownership established. |
| 25–48 | `Core: Hot` | He conducts; the crew uses her; he watches. |
| 49–72 | `Core: Faulting` | She is being *operated*, not fucked. |
| 73+ | `Core: Failing` | The machine is coming apart. |
| ≥ 96 | — | **The break** fires. |

The row is **invisible for the entire game before captivity**, appears the instant she is first used, and
would vanish again if the fault were ever cured. Random rolls pick *which* scene; the band picks *which
shelf it may pick from* — so escalation stays monotonic no matter how the dice fall.

**Eight uses across three days, +12 strain each.** Two distinct scenes per band. **Nothing repeats** — that
is test 1, enforced by arithmetic.

### The scenes

**Budget: eight distinct scenes.** This is the real cost of the chunk and it is the correct cost. *If it is
three scenes rolled ten times, we have rebuilt the Renner rungs.*

**Bastien is present all three days** — LO's call, and it makes him carry the chunk instead of vanishing
from his own arc. A distinct role per shelf, or he is wallpaper:

- **Nominal** — he uses her himself. Ownership, established.
- **Hot** — he conducts. He hands her to the crew and watches. His voice stays in the room.
- **Faulting** — **he sees the machine failing, and does not stop.**

That last line is load-bearing. It is the reason Cain is angry: **Bastien broke something Cain wanted
intact.** Bastien's alignment with Cain stays off the page (the saved reveal) — but his *choice to keep
going* is what makes the next chunk's bombshell land.

**The crew are faceless** (LO's call). No names, no records. The room has exactly one face in it —
Bastien's — and every other body is meat. This is a stronger read than "which one flinches," and it means
`attend` pays off in the three things that *do* have edges: **the man on the chair**, **the door**, and
**her own fault.**

### Cain, and the argument we do not show

He arrives in the Failing band, after the break. He is furious and **cannot** explain himself — not won't,
*can't* — in a way she registers and does not understand.

The argument happens behind a door and is never dramatised. But *not showing it* and *not rendering her
failing to hear it* are different things. It is written as **her failing perception**: two men on the other
side of a wall, and she is too cooked to hold the thread. She catches perhaps **four words.** One of them
is a name, or a word that should not fit.

That is free suspense, and it is the once-only place the prose may spend.

Then he frees her. He does not say why. **The chunk ends.**

He is never a speaker on the page — no record, no portrait, no dialogue. Cain is a shape behind a door and
four words she cannot hold onto.

### What she carries out

**Her gear comes back.** Bastien stripped the drain to disarm her *in the room*; she leaves with it. Correct
fiction — **the body is damaged, not the equipment** — and a hard engineering requirement besides.

**The fault does not heal.** `core_strain` freezes where it stopped. The Cradle takes her Charge back to
full and **cannot settle the fault** — that's prose, not a number.

**No mechanical teeth this release.** A permanent debuff with no cure, in a shipped sandbox, is a nerf the
player can never answer. The damage is a **promise**, and the `Core: Failing` row sitting in the sidebar on
every screen is that promise, visible, until the next update pays it. The repair chunk then opens on exactly
this hook instead of starting cold.

**And four words she cannot hold onto.**

She walks out onto the waterfront and back into the same sandbox — Mercer, Renner, the Sunday brothel — with
a broken machine and no way to fix it. The last thing the player has to do is *go back to work*. Whether
that reads as bleak-and-correct or as anticlimax rests entirely on the end card. **Spend the prose there.**

### Register

- **The room's ambients, the two verbs, the eight shelf scenes** → **RTS-flat.** Terse, specific, crude,
  re-readable. Real anatomical language. No environmental sensory ritual. *Specificity, not literary density.*
- **Glitch III, the break, the argument behind the door, the release, the end card** → **Tier-3, earned.**
  These are once-only. The prose may spend.

Bastien speaks in his own voice throughout (see the ceiling above). The crew speak too — the hot beats are
**played, not summarized** — but as quoted lines inside the narration, never as named speakers.

### Engine realities that shaped the design (bounced up from the build, not patched into TOML)

- **The sealed room needs no engine work.** A location with no way in and one trait-gated child seals
  correctly. Proven by probe build and live browser.
- **One engine change, one line.** SugarCube's undo button (`←`) is the *only* hatch a sealed room cannot
  close from TOML. It gets disabled.
- **The `Core: Failing` row must not close its top band**, or it vanishes at exactly the moment the design
  promises it becomes permanent. The band runs `73+` with no upper bound.
- **The Quests page must be re-gated.** Today's end-of-content card fires on the same flag the grab sets on
  the way *into* the cell — so without a fix the page tells the player the game is over while they are
  inside the newest content in it.
- **Interruption pacing has one dial, not two** (a per-day cap). The visit-cooldown is fixed in the engine.

### Deferred (not this chunk)

Why Cain freed her · ~~repairing the core~~ **→ now the Salvage chunk (see `## Salvage — The Repair`)** ·
Bastien's alignment with Cain (the saved bombshell) · Calloway, The Site, the chip ending.

---

## Salvage — The Repair (Act 2 · the repair bridge) — added during authoring

> The chunk after captivity, and the one that pays the frozen `Core: Failing` promise. Full design record:
> `games/vesper/design_salvage_the_repair.md`. Story folded here (the review surface); the gated/placed
> scene list is under `### Salvage blueprint`. **~8–10 canvases — a bridge, not a mission.**

### Why it exists
Captivity left `Core: Failing` frozen in the sidebar with **no cure** — the loudest unpaid promise in the
game — and a rescuer who found the drain-seam at the base of her spine *without looking, like a hand going
to its own pocket.* Salvage pays the promise and turns the rescuer into play **without** spending Cain,
"Vesper", the Bastien-alliance, or the Site (all reserved for the finale). It continues the mopoga cure
(more **people**, no new grind) and re-launches the sandbox pointed at Calloway → the Site → the chip.
Mission 3 ships after it, clean.

### The three tests any beat here must survive
1. **Scene, not bar.** Staged repair is 2–3 *distinct* scenes — a different system, a different test, a
   different body each — **count-locked, `is_repeatable=false`.** A repeatable repair→test loop would
   re-ship the exact "grind not content" review *inside the chunk built to cure it.* (The grind-guard.)
2. **Has a verb.** The **supplicant / test-bench** stance — she needs, is worked on, her weapons proven on
   brought bodies. The first non-conquest verb on the roster.
3. **Leaves her changed.** Function restored, the sidebar transformed (Failing → Locked), a wrong-note she
   can't un-hear, and — for the first time — a reason of her own riding under a company order.

### The staged beat chain (locked)
1. **The body won't hold.** Two loop-attempts break *on input* (the leg buckles, the drain misfires). She
   can't report it — a company refit means a **wipe** — so, for the first time un-ordered, she goes off the
   books.
2. **Finding Kess / the terms.** Kess nearly ejects her (company heat), then flips greedy at the core read.
   It's **stage by stage, and each stage costs** — untraceable `coin`, never company Credits. She's short →
   the balance rides out as a debt.
3. **Stage A — core & charge (Tier-3).** Kess opens the seam; the forensic read; mid-charge her hands trip
   an **involuntary memory-leak** she reaches for and can't hold. **Test: she charges on Tolly** — does the
   core hold without cooking?
4. **Stage B — the drain (the clue).** **Test: the drain fires on the anal finish with Reeves — and the
   payload makes him give up that the build-files live in Calloway's file room.** The weapon-test *is* the
   intel beat. *(Stage C — a light emitter proof — only if it earns its canvas.)*
5. **The verdict — Core: Locked.** Function bought back; the sidebar flips; but the deep fault is sealed in
   a partition Kess can't open — *"you'd need your own build file, and Vance keeps those classified."*
   Medical crisis → identity mystery. She walks owing the debt.
6. **Re-launch → Calloway.** Mercer pings Mission 3. Company order and her own reason share one address.

### Kess, and the bodies
**Kess** — an off-books dockside synth-mechanic who reads bodies as **hardware, not women.** She is the hand
that repairs her **and** the cold channel that reads *who re-seated the drain* — and she never learns his
name. Full NPC; **recurs** as the debt-holder. **Tolly + Reeves** are canvas-local test-bodies (Tolly = the
charge test; Reeves = the drain test whose payload drops the Calloway clue), named in narration only.

### The meter — Failing → Locked
`core_strain` is the *acute overload*; Kess bleeds it to 0 and the "Core: Failing" row **vanishes** (the
renderer emits nothing when no band matches). A new hidden `core_sealed` lights a **"Core: Locked"** row —
the sealed partition only the Site opens. Visible payoff, and honest to "no cure shipped": the true fault is
uncured, only Locked.

### The mystery — cold channel only
Two touches, neither on Cain's page: the **forensic read** (*"somebody who'd had their fingers in you
before, who didn't need to look"* — the tender hand attributed to the *recent* re-seat) and the once-only
**Tier-3 glitch-leak** (reusing the release beat's exact devices — the smoke, the hand to the seam, the name
that fits a lock — so it reads as the *same* memory surfacing; the syllable never renders; sets no chip
fragment). Cain stays a shape; "Vesper" off-page; the alliance unreportable (Kess doesn't know it); the Site
closed.

### The awakening — kept still
No deliberate first-want. Her only stir is the involuntary leak she can't hold; the body-tests carry **no**
"she wanted it" beat — she is being *operated*, and only the leak reaches past it. Protects the "un-fed until
the chip" inversion. The first *chosen* want is saved for a later beat.

### Register
RTS-flat for the berth, the terms, and the body-tests (Kess's voice **clinical** — he narrates a body the
way a mechanic narrates an engine; the bodies are consensual and hot, no ceiling on explicitness). The
Stage-A glitch-leak is the single **Tier-3** spend, and it spends by *reusing* the release beat's devices —
recurrence, not new purple. Everything else flat.

### What she carries out
Function restored · the sidebar flipped to **Core: Locked** · a wrong-note (someone knew her body; a syllable
of a name) · a destination now **doubly hers** (Calloway's file room holds both the record she wants and her
own build file) · a growing **`kess_debt`** in untraceable coin (she walks **owing** it — the broke→rich seed;
Kess recurs).

### Deferred (not this chunk)
Calloway / Mission 3 · the Site → the chip → the fracture (the Phase-1 finale; the sealed partition Kess named
but couldn't cross) · the company-notices chunk (the wipe threat with teeth) · the first *deliberate* solo-want
· Bastien's alignment with Cain · Cain on-page / "Vesper" / warmth (reserved).

---

## The Archive (Act 2 · the Calloway infiltration + the deal) — added during authoring

> ⚠️ **SUPERSEDED 2026-07-22 — see `games/vesper/design_beat_archive_v2.md` (authoritative).** The story below (bug/theft/overhear, the two thefts, Bastien-spying) is the OLD design. The new 1a spine — copies-not-theft, the Colm sub-arc, blackmail-Vane, her build file, the watcher-flush + Mercer-panic ending — is fully written in the v2 doc.

> Built **fresh** from the shipped 0.1.4 end-state (leashed, paid-clean, Mercer wary, back in the sandbox);
> the old Phase-1 Calloway/Site/Cain ladder (§2 / *Top-level* / *The opening*) is **set aside** for the forward
> story. Full locked spine + cast + locked rules + canon anchors: `games/vesper/design_beat_archive.md`.
> Two shippable chunks — **1a · The Archive** (topside/Calloway — infiltrate, bug, seduce+drain, discover the
> big theft, get burned; **build first**) and **1b · The Deal** (underworld/Bastien — the deal, Vane the mole +
> Bastien the buyer, read the build file, the Mercer trade). Two NEW NPCs: **`npc_calloway`** (the mark →
> nemesis) and **`npc_vane`** (Calloway's hidden mole → her kept asset). This section grows one subject per
> blueprint pass; the placed/gated scene list is built into `### The Archive blueprint` across the NPC + world
> passes.

### The player thread in this chapter (Step 5 · Pass 1)

The Archive advances her one standing want — **used → user** — without resolving it. It adds **no new
player-wide system**; her daily systems, the drain, and (since Salvage) the leash are already shipped.

- **The leash is the live constraint.** The control chip blocks her power (drain/emitter) on her owner, Mercer
  — the *weapon*, not lies or trade. She can still seduce, drain, and negotiate everyone else.
- **She takes the key, not the cut.** In 1b she gets the **leash controller** — the key that makes a later cut
  safe/fast — but the cut waits: it risks her still-**Failing** core and needs **Kess's** hand. She ends
  **holding her own key, still leashed.** The turn is in motion, not done.
- **Purely in-fiction** (LO, Pass 1) — no sidebar marker, no new meter. Her §2 lean holds: the dormant
  `corruption` stays dead; the fiction / inventory is the ladder.
- **Identity — set up in 1a, paid in 1b.** Her **build file ("what she is")** rides in the big stolen chunk.
  1a delivers only the *discovery* that it's gone (a cold gut-drop — her own file rode out in the theft); the
  **read** — *what she is*, **dread-first and rationed** — is a **1b Tier-3** beat, not a full origin dump. (Salvage already handed the seed: Calloway's file room holds *both* the record she
  wants and her own build file — see *## Salvage → What she carries out*.)
- **The seduction is cold — no warmth breached.** Calloway gets the **belief-lever** (finally being believed,
  allowed to stop being the hunter), never her warmth; §2's "no warmth / reserved for Cain" stands.
- **Register:** RTS-flat, third person. **1a spends zero Tier-3**; both Tier-3 licenses (the build-file read,
  the Mercer trade) live in **1b**.

### Calloway — the disbelieved hunter (Step 5 · Pass 2)

**The shape — the roster's return to conquest, on a new lever.** Renner broke from contempt to want; Bastien
**took** her; Kess never wanted her. Calloway is a **seduce-in**, but the lever isn't lust — it's **belief.**
He's a company rogue-hunter, humiliated and sidelined, his un-indexed file room being audited shut; everyone
treats him as a crank. She's the first to take his hunt seriously (she brings the bug). His surrender is
**being believed — being allowed, for once, to stop being the hunter.** RTS-flat, cold: she gives him the
belief, never her warmth (§2's "no warmth" holds; reserved for Cain).

**The arc — guarded → believer → attached → betrayed.**
- **Guarded** — he reads her as one more minder sent to watch the crank fail.
- **Believer** — she proposes bugging the docs; a starving hunter jumps at the first person who takes his ghost
  seriously → she's in (his openness, then access).
- **Attached** — the seduction: a lonely, disbelieved man given the two things he's starving for. The
  belief-lever climb into the loop.
- **Betrayed** — she used his own trap to find the docs, the trail ran into the underworld where only she could
  follow, and she vanished after it. He does the math, turns **nemesis**, and reports the "analyst" up the
  chain — the fuse that reaches the Chairman in 1b. Circumstantial (no memory-gap track).

**What he yields — the two drains (load-bearing).** The drain needs the intimacy to fire and returns only
what's in his head; the archive is un-indexed, so only he — not any catalog — can point her at the material.
**Drain 1:** *"where are the docs?"* → **nothing** (already stolen). **Drain 2:** *"a big chunk was just stolen
— your target's probably in it."* That reveal opens the discovery and the Bastien-spying payoff.

**Kink ceiling.** Max-explicit, RTS-flat; the register is the **belief-lever** (surrender = relief, not thrill),
never a domme performance. The anal finish **is** the drain (canon: how the drain takes).

### Vane — the mole (Step 5 · Pass 2)

**The shape — the first mercenary on the roster (no conquest).** Vane is a spy for hire: money only, no cause.
He is **secretly one of Calloway's own team** — the ghost Calloway is hunting is his own man, hidden in plain
sight. She never seduces him and rarely sees him in 1a; he's an **unseen hand**, felt through the bug moving.

**His two thefts.**
- **Theft #1 (small)** — an ordinary lift; it **moves the planted bug** → she traces it to an underworld drop →
  he finds and **destroys** the bug there. She learns the docs go *into the underworld* — never *who buys them.*
- **Theft #2 (the big chunk)** — **triggered by Wren getting visibly close to Calloway** (the seduction crossing
  its mid-band spooks him), a few days before the drain. This chunk holds **Mercer's target bundle + her own
  build file.**

**His 1b turn.** At the deal he's the **seller** (the mole reveal); the buyer is Bastien. When the deal
collapses she **catches him and keeps him alive** — an asset and her thread toward the buyer. Minimal NPC: a
**dialog speaker at the 1b reveal**, schedule-less (hidden, like Bastien in his reveal chunk); no portrait hub,
no relation/corruption climb.

> ⚠️ **SUPERSEDED 2026-08-09 (rev 112) — the 1b above is the OLD sketch.** The chapter that actually follows
> 1a is **`## The Leash`** (full record `games/vesper/design_the_leash.md`), and there is **no deal scene**: the
> controller trade already happened inside the 1a close, so 1b's engine is a repair grind on her own hardware,
> not a negotiation. **Vane is NOT picked up this chunk** — he fled into the Reach at the close and stays
> reserved. The destinations survive (the file read, the leash, Bastien, the Chairman inbound to the arc
> beyond); the shape does not.

---

## The Leash (Act 2 · 1b — the key, the file, and the man who signed for her) — added during authoring

> The chapter after The Archive 1a, and the one the shipped 0.1.7 end card promises the player **by name**.
> Full design record: `games/vesper/design_the_leash.md` (it supersedes the §12 "1b · The Deal" sketch in
> `design_beat_archive_v2.md`, banner-marked in place). Story folded here (the review surface); the
> gated/placed scene list is under `### The Leash blueprint`. **~30–36 canvases — a chapter, not a bridge.**

### Why it exists

She has spent the whole game unable to do one thing. Not forbidden, not afraid — **unable**. A piece of
hardware older than her frame, seated under her core, that makes her weapon refuse to fire on the man whose
name is on her papers. Kess found it in Salvage and told her plainly (`5_scenes.toml:5111`): *"There's a man
you can't point your teeth at… That's this."* She has never asked why. The not-asking is so complete she has
never noticed it has a shape.

This is the chapter where she takes it out.

It also pays two debts the build is currently carrying. **One player-facing:** 0.1.7 ends by sealing the Spire
behind her, and every Charge restore, bed, wash, bench and wardrobe in the game is on the wrong side of that
seal — the post-ending player runs flat with nowhere to sleep. The fix was written (`08ec2e1`) and cut with 1b
(`187f521`); increment 1 restores it. **One structural:** `controller_held` is set by the 1a close and read by
nothing. This chapter is its reader.

### The three tests any beat here must survive

1. **Is she walking in on her own feet?** The 1a close ended *"the deal's paid; they're quits."* Any beat where
   she serves Mercer because she still has to un-spends the one thing she bought. She is **humouring**, not
   obeying — and that is the difference between a con and servitude.
2. **Does the failure fail differently?** The loop's three failures carry the chapter. Nothing → it bites back
   → it works for a second. A beat that repeats a null result is the mopoga *"grind not content"* review
   arriving on schedule.
3. **Is she seen being clever?** She never narrates the plan. One `thought_bubble` a scene, the same ration as
   the glitch beats. The player knows what she is doing; the inverted protagonist breaks the moment she is
   observed scheming.

### The staged beat chain (locked)

1. **She moves in** (@`kess_berth`). File + controller to Kess; he points at his feed line and names his price
   — **per night, in coin**, *"coin dries up, so does the arrangement."* **That feed line is her charger now.**
   Up top she was maintained free, because equipment gets serviced; down here she pays to stay alive. Lane 4
   (auto-fire, restored).
2. **He reads the file** (@`kess_berth`, once). Build documents — a **programme**, eleven years, many subjects,
   dates in two columns. **Her own page is sealed in the same hand as the controller.** *The file and the key
   are one lock.* Lane 4 (Tier-3).
3. **He needs the owner's hand print.** The key won't wake for anyone else. Lane 4 (auto-fire).
4. **Mercer resurfaces** (@`underworld_bar`, auto-fire). Under a new name, running a paper stall. **Delighted**
   first; only then, quieter, *please not that name here* — **and she doesn't stop.** Lane 4.
5. **The drink ladder** (@`underworld_bar` → @`mercer_room`). She humours him up `npc_mercer.relation`
   (nostalgia). He asks about the name three times, quieter each time, then **stops asking**. She takes the
   print. Lane 1 + a Lane-4 capstone.
6. **The loop** (@`underworld_market` → @`kess_berth` → @`mercer_room`). Buy a part, Kess plants it in her, she
   lets Mercer have her and tries to fire it while he is on top; it fails; **the part burns**; she finishes,
   smiles and leaves. Three failures, each teaching Kess one thing. Lane 1, count-locked.
7. **The first fire** (@`mercer_room`, once). She has stopped expecting anything; it catches. Control canvas,
   Q&A in **his** dialogue. Payload = **the bad news: the key only ever spoke for one name.** Lane 4 (Tier-3).
8. **Bastien** (@`underworld_bar`). His name came off the set. He searches her at the door every visit, so it is
   **smuggling** — two things past him now. His drain answers **why he was buying her file: for Cain.** Lane 1
   + Lane 4.
9. **The extraction** (@`kess_berth`, once). A live key lets Kess hold the governor quiet while he cuts. The
   chip comes out, and **her page opens with it.** Lane 4 (Tier-3, the chapter's end card).

### The berth, and what the coin buys

A curtained bunk over the feed line. A paid night is 10 coin: full Charge, a day forward and a drain reload.
**Crash rough** is free, partial, and advances nothing — the floor that means the player can never brick
themselves.

And a paid night buys **Kess's time** — three days of it. Stop paying for nights and he stops touching the
key, not out of spite: he is a tradesman and she is not a charity. That is what turns the House and the Pit
from idle side-earning into the spine: **she is fucking strangers for money to pay a man to cut her leash.**
Coin never blocks her ability to act — only her progress on herself. At ~23 coin a week against a brothel
finisher at +10, the pit at +8/+20 and Marsh at +15, one pit win and a client covers it.

He is the read-out, not the sidebar. There is no standing "upkeep" row — LO's 2026-07-16 call on the retired
`Leash: Uncut` line holds here too (*the reveal lives in the scene, not as a standing sidebar line*), so
whether he is working is something **Kess says** when she asks.

It is an authored `coin` sink, not the engine rent system — and that is a verified call: the engine's rent
hard-redirects every location and the nav screen to its RentDay passage while due (`v2.py:15245-15255`), which
blocks her from *acting*; it charges `money`, not `coin`; and because `backfillStateDefaults` has no
`game_state` branch, switching it on in a shipped title leaves every carried save silently rent-free forever.

> **⚠️ Cadence corrected 2026-08-10 (rev 114, at beat_0069).** This section said *weekly* at the fold. The
> beat_0068 build put the terms in Kess's mouth as **per night**, and the cot's paid tier plus quest card E
> ("Keep the cot paid") both shipped on that cadence — so rather than add a second, weekly bill the terms
> scene never named, **the paid night IS the upkeep.** The planned `activity_pay_rent` canvas is dropped.

### Mercer — the man with a new name

He landed on his feet. A flat new name, a black-market stall selling **Spire paper** — clean identities, badge
histories, manifests, the one craft he actually has, because he *signed for her*. A back room with a door,
better than anything she can afford.

He remembers owning her **fondly**, and that is the whole character. He is not lonely for *her*; he is lonely
for **himself**, for the man who had a penthouse and an asset. She is a souvenir of his better days. Written
right that is the worst he has ever been in this game; written one degree wrong it is a sad old man missing a
friend, and the ending stops landing.

**The name.** He asks — a favour, not an order, because he no longer has the standing for an order. She says it
again in the very next breath as if he hadn't spoken. No defiance, no smirk, no interior triumph: she just
hasn't changed, which is exactly what she has always been to him. He asks three times across the visits,
quieter each time, then **stops asking** — a whole arc in three lines. She never uses the new name, in
narration or in dialogue, once.

Underneath the nostalgia runs a second engine he would never admit to: **she is a walking security hole in his
new life.** He cannot afford her wandering his own bar saying that name. So he keeps her close and keeps
pouring. **She has a leash on him and neither of them has said so**, and she never has to threaten him — the
threat is structural. *(Held, not spent: her saying it in front of someone else.)*

`npc_mercer.relation` goes live for the first time in the game, re-cut as **nostalgia** — how much of his old
life is back in the room. It buys **hospitality access**, never register. He is at his ceiling from beat one
and never climbs; his use-scenes differentiate by **what each violates** — her time, her money, her body, her
patience — not by pose.

### The loop — three failures and a win

**Try 1 — nothing at all.** *(Built `beat_0076`; the sketch is corrected here to what shipped.)* Dead
silence. He has her face-down over the end of the bed with a thing at **the base of her spine** doing
absolutely nothing, and she has to finish and leave and smile. Not *in her chest* — `beat_0075`'s install
put it where the drain sits — and not *on her back*, because the reach rides his anal finish, the one act
where her own drain has always come up empty on him. *Kess learns:* it isn't a lock — it's
**listening**, and he guessed the wrong channel.

**Try 2 — it bites back.** *(Built `beat_0077`.)* Something answers and the governor **clamps down**. Her body
locks up **at the hold, with him still inside her** — not mid-stroke, which is where this sketch used to put it:
the shared evening node ends at the finish and the reach is the click, and the hold is the worse moment anyway,
because he is still and quiet and paying attention. She gets through it without him noticing, and she does it
because the half he can feel reads to him as her finally responding. *Kess learns:* it **defends itself**. A
guard, not a safety — and a guard means somebody is still using it.

**Try 3 — it works, for a second.** The leash lets go. She *feels* it go, and it snaps back before she can do
anything. The cruellest one, because she has tasted it. *Kess learns:* it was never keyed to a **man**. It's
keyed to a **set of names**, and he has only been spoofing one of them.

**And that is the fork into Bastien.** The set is older than she is and it has underworld names on it — so it
was never the company's list, and **she wasn't fitted with a leash. She was built around one that was already
there.**

**Try 4 — it holds.** She has stopped expecting anything by now; that is why it lands. Then the control canvas,
and the bad news: one name out of a set. She isn't free — she's carrying a hall pass with her owner's name on
it. Which is what makes the extraction, not the first fire, the chapter's ending.

### Bastien — the name on the set

Not optional side-content: **his name came off her own leash**, and that is why she goes back to the man who
kept her in a room for three days.

He strips her at the door — unhurried, public, in front of his own bar — because he is the only person alive
who knows what she is *and where she carries it*, and because he is establishing that he still may. So the arc
is **not seduction. It is smuggling, and her body is the bag** — worse now, because she needs the drain *and*
the controller past him, and the drain alone does nothing on a name that's on the set.

His lever is **curiosity, not desire.** He is not a cruel man, he is an interested one — the cell was a lab and
he took numbers. A seduction ladder bounces off him; he would enjoy it and give nothing. What he has never been
permitted is being **read himself**, which is why the drain destroys him.

The payload: he was buying her build file **for Cain**. The man she was built to kill has been trying to find
out what they did to her.

### Register

Third person, unchanged. Lanes 1/2/3 flat at ~35–40 words a beat; Lane-4 capstones are **more beats (10–20),
not thicker beats**. **Narration : dialogue ≤ 1.5 : 1 in any scene with a present NPC** — a hard target here,
because Vesper runs 7.25 : 1 and Mercer is the natural cure: he talks constantly, about himself, and all of it
is characterisation.

Her interior stays rationed to one `thought_bubble` a scene, and **she never narrates a plan**. The attempts are
written as things happening *to* her body. Ceilings: Kess-invasive · Mercer-nostalgia + the drain inversion ·
Bastien-outside-the-cell (**not** widened — the cell re-spec stays cell-scoped). **Mercer's is SIGNED (rev 119)**
and first spent at the print; the other two are still **drafted and unsigned**, and no hot beat on either ships
until LO fills them.

### What she carries out

A cut leash — the hardware gone, not suppressed · her own page, read: the programme, eleven years, the many
subjects, and her at the centre of it · her owner drained and none the wiser, and a `relation` with a man who
still thinks she visits because she's fond of him · Bastien owned and unaware, and the knowledge that Cain has
been looking for what they did to her · a room she rents, a bill she pays, and the first door in her life she
can shut · and a **set of names** she has only two of.

### Deferred (not this chunk)

**Cain** (off-page; Bastien's drain names a want, never the man) · the **Chairman** · **Vane** (fled at the
close, reserved — he is the cheapest next chapter and spending him now costs that) · **`the_site`** (still the
one read-never-set flag in the game; it is Cain's door) · the **Spire** (sealed, stays sealed) · her **solo
want** · the rest of the **set of names**.
