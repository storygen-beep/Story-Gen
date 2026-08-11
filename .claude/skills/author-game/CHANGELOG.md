# author-game — CHANGELOG

The ledger for this skill. Record **every** change to any file in this skill
(`SKILL.md`, `references/*`, `scripts/*`, etc.) — including small fixes and wording.
Newest first. One bullet per change; group bullets under the date they were made.
Per entry: **what** changed (name the file) — **why** (the motivation / root cause) — and
how it was verified if relevant (grep / build / live-play).

Convention lives in `story_gen_django/CLAUDE.md` → "Skill ledger".

<!-- entries recorded going forward; example shape:
## YYYY-MM-DD
- reworded dispatch note (`SKILL.md`) — clarified phase resume — n/a
-->

## 2026-08-11
- **A hidden rung still owes the player a reason, and it is owed in PROSE (`references/lanes.md`, the
  "Grey vs hide" bullet).** The rule taught hide-vs-grey as a property of the *rung type* (escalation rungs
  grey, everything else hides). That is right when the precondition is a story the player has not reached and
  a trap when it is an **upkeep or inventory step they can act on right now** — a lapsed rent, a decayed feed
  line, a part bought but not installed. There the rung is real, earned, and vanishes silently, which reads as
  a broken game. Added the second half of the rule plus the state-not-rung check ("enumerate the states where
  the rung is hidden; for each, what on this screen tells them what to do?"), and the reason
  `show_when_locked` cannot be the fix: it greys on the choice's **whole** conditions block (`v2.py:12798`),
  so it is all-or-nothing and would advertise the content from the moment the canvas exists. Also recorded
  that banding a base node on a **recoverable state** is not the banned "tiering the opener" — a read-out
  tracks something the player can change this minute, not arc progress. **Root cause of `vesper`'s parts-loop
  stall**, where LO lost his own loop in playtest: both gates were correct, both were commented as checked,
  and no state on screen named the part in her pocket or the bill she had not paid. Verified live —
  `repro_parts_stall.py`, 33/33, with the four Kess bands and the Mercer band asserted at every gate combination.
- **`§10` now sweeps EVERY guidance surface, not just the card table (`references/quests.md`).** `beat_0084`
  added "the map seals or opens" as a sweep trigger, swept the Quests page, and declared it clean — while the
  **Schedules page** went on advertising `vesper`'s owner as "NOW: Mercer's Penthouse" for fifteen hours of
  every twenty-four, his real address filed as the inactive row, plus two more NPCs standing in a building
  sealed an act earlier. Added the surface table (quest cards / Schedules page / off-hours cards / hub prose)
  with why each goes stale — schedule rows **cannot** be gated, the resolver reads five keys and drops the
  rest — the note that a page naming a locked door is worse than one saying nothing, the `blocked_message`
  obligation for a location with two gates in two acts, and a live-read step to the audit, since no grep
  catches staleness produced at render time. Verified live: no `NOW:` badge on any locked location for
  Mercer, Calloway or Vane in a 1b save, Kess's row unaffected.
- **Both QA build flags poison absence-assertions in a live suite (`references/beat-authoring.md`, the
  build-flags note).** Each injects text that is not the game, so a check reading a wide scope reads the
  scaffolding and calls it content — and it is always the *absence* checks that die, since a presence check
  simply finds what it wanted. `--debug` bakes the `MISSING` placeholder's **authoring metadata**
  (`description`, `search_queries`) into the passage, so a vocabulary hold trips on the word inside an
  `avoid: … <that act>` clause. `--dev` puts the **DEV JUMPS list in the sidebar**, and jump labels name NPCs
  and chapters, so "this NPC must not appear here" fails on the label. Both found while re-running `vesper`'s
  regression set against the rev-130 fix, and both were false alarms that cost a full diagnosis each:
  measured on identical TOML, `live_beat_0074` fails under `--debug` and passes **46/46** without it, and
  `live_beat_0081`'s six nav-badge checks fail under `--dev` and pass **68/68** clean. Recorded with both
  fixes — run suites against a **clean** build, or scope absence checks to `#passage` rather than `body` —
  and with the reason it matters: a suite that only runs on a QA build is one whose failures you learn to
  ignore, which is worse than not having it.
- **`§9` gains a fifth check: no two CO-LIVE cards may repeat a clause (`references/quests.md`).** The
  Story-Goals card and every NPC section render on one screen, so a phrase carried over from the spine prints
  twice in the same view — and authoring an NPC tier *next to* the spine cards it belongs with produces that
  echo almost every time, because the sentence is right there and it is the best one you have. Found by
  measurement, not by reading: a six-word-run comparison over the live set at each reachable state caught
  **eight** repeats in `vesper` `beat_0084`'s first draft of its nine new cards, including whole lifted
  clauses ("he keeps a stall on the black market and a room behind it"). Every card was rewritten; the check
  is now a permanent assertion in that game's live suite. The rule stated positively is the same one that
  justifies two tiers at all: the NPC card says **what the spine leaves out** — the man, the count, the state
  of him — never the mission beat again in different words.
- **New `§10 — Sweep the whole table when the world moves` (`references/quests.md`), plus a third case added
  to `§6`.** The file taught how to author a card and how to lay the page out once, and had no maintenance
  rule at all — so every defect where the card stayed still and the world moved around it was invisible to it.
  Found by reading `vesper`'s Quests page end to end at `beat_0084`, which turned up three independent
  instances at once. **(1) The frontier moves.** Three Story-Goal cards still carried "that's where this build
  ends … is the next release" after the frontier walked five rungs past them; the worst named cutting the
  leash, opening the file and reading her own page as *the next release*, in the build that ships all three.
  The interesting part is why it survived: the TOML comments record the check being **run and passed**, against
  the card's own rung — and from that card's rung the sentence is true. A boundary claim is a statement about
  the **whole build**, so it cannot be evaluated locally. New rule: exactly one card names it, moving it is a
  two-step edit, the check is a whole-table grep anchored on `^tip\s*=` (a bare string grep matches the comment
  blocks quoting what you stripped), and the **Support-Us ask never walks with it** — only the claim does.
  **(2) The map seals or opens.** A tip is a *direction*, so it is coupled to reachability: Act 1a's close
  hard-seals the Spire, and Calloway's whole four-rung ladder plus half of Colm's end card went on pointing at
  it for the rest of the game. The unfinished arc is the worse case, because its rungs are live instructions —
  and the fix is one card at a priority above the ladder, not N edits, because the NPC tier returns the single
  highest-priority match. **(3) A mechanic retires** — `lanes.md`'s terminal-flag sweep binds to cards too.
  §6 gains the case it was missing next to the Frame-3 blank: when an arc's last card retires with nothing
  behind it, the section does not go stale, it **disappears** (`pickQuestsCard` returns null and `:: QuestsPage`
  skips it), at the exact moment that NPC becomes permanent sandbox content — Vesper's Renner vanished off the
  page on his own drain while his office stayed open for the rest of the game. Verified live: 85/85 on
  `live_beat_0084.py`, which reads the real renderer at every state from the 1a close to `leash_cut`.
- **Terminal-beat retirement had only half the failure mode: gates the flag makes permanently FALSE**
  (`references/lanes.md`, extending *Retire the standing surface on the terminal flag*). The existing sweep is
  thorough about surfaces that become a **lie** — courtship for a man she owns, a hub for a man who fled — and
  it is entirely about **prose and presence**. It does not name the case where a terminal beat removes the
  **enabling state of a mechanic**, which makes nothing stale: it makes every gate that requires that state
  stop passing **forever**, and the content behind them unreachable with nothing on screen to show it. The
  engine actively hides it — no passing choice emits a `console.warn` and a bare Continue escape, which reads
  as a scene that simply stopped having anything in it. Found at `vesper` `beat_0083`: the extraction cuts the
  controller out, so `controller_state` is 0 for the rest of the game, and the sex loop's drain exits required
  it — every future anal finish would have routed to the "nothing happens" branch forever, so the player would
  own the man and get nothing. Five surfaces read the retired state; only that one was fatal. The new section
  gives the one-grep audit (list every reader of the retired state, and ask of each whether it still has a
  **true branch** after the flag), the three legitimate answers (re-partition / retire / repoint), the warning
  that `logic = "OR"` cannot express the re-partition because it is one logic per block with no nesting, and
  the assertion shape that catches it — **verify from the failing side: after the flag the surface must still
  reach its payload and must NEVER reach the wrong-answer branch.** Verified by building against it: 52/52
  live assertions green including that failing-side pair, with the six-way exit partition asserted by
  derivation rather than by count.
- **The sex LOOP is where the dialogue ratio actually dies — measured, and added to Rule 4's worked example**
  (`references/beat-authoring.md`, extending the extraction-beat blockquote). The `beat_0079` fold covered the
  *payload* beat; applying it a second time at `vesper` `beat_0082` showed the payload is the smaller half of
  the problem. Measured across that game's three shipped sex loops: the pose canvases and finishers run
  **8.8 : 1**, **102 : 1** and **132 : 1**, and the finishers and drain payloads contain **zero** dialogue
  blocks between them. The reflex — a man mid-act has nothing to say — is wrong twice: he is the most
  talkative he will ever be, and what he says while using someone is the most characterising line he gets.
  Authored fresh with his voice on, the same three-canvas chain measured **1.08 / 1.28 / 1.22**, and the fix
  cost **eight lines**. The note also carries the procedural half that would have caught it earlier: run
  `§7 check 3` on **each canvas of a chain separately**, because a chain average hides a 100 : 1 finisher
  inside a healthy-looking whole. Verified by building against it — the new chain's three canvases each pass
  check 3 independently, 57/57 live assertions green, and the whole-game ratio moved 2.60 → **2.55 : 1**.

## 2026-08-10
- **The nav-invisible interior named as a map SHAPE, where map shapes get chosen**
  (`references/location-design.md` — new §4.2, under the locked-location unlock contract). ⚠️ **This is not a
  case of the skill teaching something wrong** — `engine-reference.md` §5 already documents `auto_exit`
  correctly, including the exact sentence *"Both halves are required: without the fallback half, the location
  dumps the whole map."* The gap is where it lives: it is a **field row in a reference table**, and the
  author who needs it is not looking up a field, they are choosing a **map shape** in `location-design.md`.
  Found the hard way at `vesper` `beat_0081`: a room that must not be advertised and whose door is an
  unskippable scene was built with no `entry_from` and *without* `auto_exit = false`, and the built passage
  came out carrying `All locations:` and the entire world — from a locked back room the player could walk to
  the Spire. Caught by the live suite before any content assertion ran. The new section names the two
  situations that call for the shape (do not advertise the room; getting in is a scene), states that **both
  halves are required** with the code path (`v2.py _generate_hierarchical_navigation`,
  `if not navigation_html and auto_exit`), contrasts it with the other legitimate answer (give the room a
  child — a door location — when the door *is* content), and ends with a four-item pre-ship checklist whose
  sharpest item is greppable: **the built passage must not contain `All locations`**. Verified by building
  against it — 67/67 live assertions green, including one that asserts the room is nav-less and one that
  asserts no NPC badge for its occupant renders anywhere in the game.
- **The extraction beat is a conversation — a worked example for Rule 4** (`references/beat-authoring.md` —
  new blockquote under *dialogue carries character (Rule 4)*). The rule already said "play it, don't report
  it" and named capstones and sex scenes as the place to push hardest, but it had no example and no named
  case for the single highest-value instance: the beat where an NPC **gives something up** — a drain, an
  interrogation, a confession. Measured at `vesper` `beat_0079`: that game's design book has carried a
  *control-canvas carriage rule* ("played as a Q&A in HIS own dialog, not narrated summary") since its first
  such scene, and **all three canvases written under it broke it** — `loop_renner_finisher.drain`,
  `calloway_drain_canvas.d0`, `colm_drain_canvas.d0`, with **zero** player dialog blocks between them, every
  one narrating the take. A prose rule in a per-game design book did not survive contact three times running,
  so the fix goes in the skill as a wrong/right TOML pair plus the three rules that keep the pattern from
  becoming an interview (her questions ≤ 4 words; the payload never also appears in narration; open is not
  broken — he answers helpfully and is never made pathetic). Verified by building against it: the rewritten
  canvas measured **0.93 : 1** by `§7 check 3`, the best in that game, and moved the whole-game ratio
  2.80 → **2.72 : 1** in one beat; 68/68 live assertions green, including one that greps the paragraph blocks
  to prove the payload is not reported twice.
- **§7 check 2 never said how a "word" is counted** (`references/rts-flat-prose.md` — new blockquote under
  *2 — Per-beat density*). Check 2 says "sum the words in each `beats[]` entry" and leaves the author counting
  by eye, while check 3's script counts `str.split()` tokens — so the two checks silently use different
  definitions, and a spaced em dash or ellipsis is a word to one and not to the other. Found while authoring
  Vesper's `beat_0078`: a Kess line planned as "twenty words, one under the 21-word ceiling" measured **21**,
  because its em dash is its own token. It passed, but the same off-by-one against a beat sitting at 50 is a
  surprise FAIL — or worse, an author trims real prose to fix an arithmetic error that was never there. The
  blockquote states the definition, gives the worked example, and says to count with the script whenever the
  budget is exact. *(Deliberately NOT changed: `kink-ceilings.md` §4 already says "the ceiling is a CAP, not a
  quota", which is exactly the reading `beat_0078` needed when a signed row worded around one scene had to
  govern a quieter one. The doctrine was there and correct.)* Verified by re-running the beat's §7 audit and
  re-reading §4.
- **Three gaps in the `exit_block.choices` reference, all found by reading the generator while authoring
  Vesper's `beat_0076`** (`references/engine-reference.md` §3 — three new blockquotes after the `costs`
  paragraph). (1) **Choice effects fire on CLICK, exit-block effects fire on RENDER.** §2 gained the
  render-time note yesterday but §3 never stated the contrast, so the two shapes read as interchangeable when
  they are not — and the practical rule ("anything meaning *she finished this scene* has to ride a choice")
  was nowhere. (2) **What happens when no choice passes.** The table documented every `TemplateChoice` key
  and was silent on the zero-match case, so an author either assumes a dead end and avoids conditional
  routing altogether, or defensively adds an unconditional fallback choice that then double-renders whenever
  a real choice passes. The engine actually emits a `console.warn`, a `$flags.debug_mode` per-predicate ✓/✗
  diagnostic, and an effect-free `[[Continue->…]]` escape (`v2.py:12890-12946`) — which also means a
  conditional-routing exit is safe to author one branch at a time. (3) **When to use a `[group]` band and when
  to use a routed sibling node.** The skill named the adjacent-`[group]` merge trap exactly once
  (`system-patterns.md:125`) and never taught the positive alternative, so "one canvas, banded chain" reads as
  the only shape for a state-varying canvas. The deciding factor is size, and the forcing constraint is §7
  check 2: a beat's measured unit is the **sum** of its blocks and beat 0's unit swallows the whole node lead,
  so four multi-beat bands measure as one ~250-word beat even though one renders. A one-line variant is a
  band; a multi-beat variant is a node. Same arithmetic noted for `block_pool`. — verified by reading
  `template_import.py:1955-1988` and `v2.py:12890-12946`, and by building the pattern live (Vesper
  `loop_mercer_attempt`, 56/56 assertions including a direct click-vs-render test of the effect timing).
- **A `type="location"` exit block's effects fire on RENDER, not on the exit click**
  (`references/engine-reference.md` §2, the `exit_block` bullet — a new blockquote, plus `effects` and
  `flagEffects` added to the `config = {…}` line, which had listed only `destinationType`, `locationId` and
  `time_progression_minutes` despite every real canvas putting its state change there).
  **Why:** the skill described the exit block's config keys and never said *when* they run, while §3's
  per-choice table says `time_progression_minutes` "advances the clock on click" — so the obvious reading is
  that a node's exit effects also wait for the click. They do not. They are emitted as passage-level
  `<<script>>` at the bottom of the node body (`advanceTime(n)` at `v2.py:13376`,
  `setup.applyAndNotifyFlag(...)`), and the engine documents this itself at `v2.py:15400-15412` as the reason
  canvas nodes are excluded from `setup.isRerenderSafe`. The bug class it invites is an author writing a canvas
  whose closing state is meant to be *earned* by finishing the scene: a player who reads two beats and leaves
  by the sidebar has already banked the flag and the minutes. The note gives both authoring rules — put an
  earned state change on a **choice**, and when the render-time set is the wanted behaviour (a one-shot that
  opens the next stage), gate around it rather than against it. Per-choice effects genuinely do fire on click;
  the two shapes look identical in TOML, which is why it bites.
  **Verified:** read out of Vesper's built `index.html` for `kess_print_read` and `cap_owner_print` (identical
  emission), cross-checked against the generator and against the engine's own `isRerenderSafe` comment. A live
  test written at `beat_0075` asserted the opposite and was corrected against the artefact, not against memory.
- **`requires_npc` is INERT on the Lane-4 auto-fire path** (`references/engine-reference.md` §2.2 field table,
  a new note under the `npc` ≠ `requires_npc` block, and the Lane-4 row of the §2.3 fingerprint table).
  **Why:** the skill taught `requires_npc` as an unqualified presence gate — *"ANDs
  `getNpcLocation(npc).location === location`"* — with no hint that the AND only happens on two of the four
  selection paths. `selectAutoFireCanvasForLocation` (`v2.py:4447`) filters on `isRepeatable` / `triggerMode` /
  `substitutionOnly` / `isCanvasValid` + priority and never reads `requiresNpc`; `isCanvasValid`
  (`v2.py:4567`) checks schedules, conditions and repeatability only. So a capstone authored as *"auto-fires
  when he's in the room"* fires whether or not he is there, the build is green, and only a player entering at
  the wrong hour finds out. This is a **bug class, not a one-off**: vesper's `rung_mercer_hands_on` shipped
  with it for a whole beat and `cap_owner_print` reproduced it immediately, because the skill is what taught
  both. The note gives the fix that actually holds — an `npc_at_location … is_present` predicate in
  `conditions`, which `isCanvasValid` does evaluate — and says to keep `requires_npc` beside it as the
  statement of intent.
  - **Second trap folded into the same note: an auto-fire that exits into its own location will CHAIN.** If
    capstone A exits to the room it fired in and capstone B is eligible there, B fires in the same breath and
    B's opening narrates an arrival that never happened. Separate them with real state, and **prefer a trait
    band to `days_since_flag`** on anything load-bearing: that predicate fails **closed** when
    `flags_meta.set_day` is absent (`v2.py:3979`), so a flag set by any path that skips the metadata locks
    the content forever.
  - **Verified live, not from docs:** headless Playwright against a clean vesper build — at 12:00, with Mercer
    scheduled at `penthouse` and `getNpcLocation` confirming he is **not** at `mercer_room`, both canvases
    fired in the padlocked empty room; after adding the `npc_at_location` predicate both correctly declined,
    and the daylight guard rendered instead. Chaining reproduced and fixed the same way (46/46 assertions).
- **Documented `[player.trait_decay]` / `[npcs.trait_decay]`** (`references/trait-catalog.md` §1). **Why:** the
  file asserted that the only way to get a daily passive was `[engine.daily_tick].traitEffects` — *"`advanceDay`
  just iterates whatever you put in `[engine.daily_tick].traitEffects`"* — which is incomplete. A second route
  exists, is applied unconditionally by the engine, floors at 0 for free, and is **shipped in
  `games/late_shifts`**; it was invisible to the skill (`grep trait_decay .claude/skills/` returned nothing).
  Found while authoring vesper's feed-line upkeep, where it is the right primitive precisely *because* it's an
  unconditional countdown with a floor. Added the TOML shape, the parse/apply sites
  (`template_import.py:1657-1666` → `v2.py:5532-5544`; the NPC variant's interacted-today skip at `:5516-5531`),
  the choose-between rule vs `daily_tick.traitEffects` (conditional vs not), and two traps: only the calendar's
  own spend belongs there, and the auto-emitted `trait_decay_warning` sidebar item.
  - **Verified live, not from docs:** built vesper with `[player.trait_decay] feed_line_days = 1`, confirmed
    `player_trait_decay = {"feed_line_days": 1.0}` in the emitted HTML, and drove a headless playthrough across
    a real midnight crossing — 3 → 2, floored at 0, no sidebar row drawn.
  - ⚠️ **Line numbers in this skill's references are drifting.** `trait-catalog.md` cited the `daily_tick` loop
    at `v2.py:5255-5275`; it is now at `:5567-5588`. I cited only sites I read myself. A sweep of stale
    `v2.py:` refs across the references is worth its own pass.

## 2026-08-09
- **Added recipe #9 — "Iterated prototype — *a fix that has to fail first*"** (`references/system-patterns.md`).
  **Why:** designing Vesper's next chapter (`## The Leash`, book rev 112) needed a
  buy-a-part → install-it-in-her-body → field-test-it → it-burns-out → iterate loop, and the menu had **no
  matching recipe** — the closest entries were #5 (consumable/reload), #2 (capability track) and #6 (loadout),
  none of which model a loop where **failure is the content**. `system-patterns.md:19-20` says to design a
  missing system from first principles and add the recipe back, so this is that. The recipe carries four traps
  learned from shipped code rather than invented: the part must be a **trait, not an inventory item** (the save
  backfill has no wardrobe branch — the `cover_analyst` post-mortem in `save-safety.md` §5, which soft-locked
  every 0.1.4→0.1.5 Vesper carry-over); the attempts must be **one canvas with an exclusive banded `[group]`
  chain** (adjacent groups merge into a single if/elseif chain, so non-exclusive bands ship dead); the counter
  must be a **trait not a flag** (a triggerless canvas has no located setter and the flag-chain validator hard-
  fails); and **N identical failures is the "grind not content" review** — if you can't write three *different*
  failures, the loop wants to be one scene.
  - **Verified:** the four traps are each grounded in a shipped Vesper precedent or an engine fact already cited
    elsewhere in the skill (`save-safety.md` §5; the merged-group behaviour; the `calloway_drains_done` /
    `colm_drains_done` trait-counter pattern). No file outside `system-patterns.md` changed; no build run
    (design-fold turn, no TOML).

## 2026-07-31 (later)
- **Documented the optional media-block `id`** (`references/media.md` §1). **Why:** a slot's
  stocked options and its approve/disapprove verdict are both filed under a *string*, and by
  default that string is the declared path — so a tier retag or a pool conversion silently orphans
  both. Measured live: **148 stocked options stranded** the first time a slot was converted to a
  pool. An authored `id` becomes the key instead and doesn't move.
  - **Taught as OPT-IN, deliberately.** ~560 media blocks exist repo-wide; untagged stays the
    default and behaves exactly as before. The guidance is to tag what you expect to *edit* —
    anything you plan to pool, anything whose tier is still settling, hero assets.
  - **Warned that the id must be a real name, not `b3`-shaped.** The importer assigns every block
    a positional fallback id of that form; it shifts when a block is inserted above, so keying a
    shelf on one would be worse than keying on the path. The engine refuses them.
  - Pointed at `manage.py check_shelves [--repair]` for a slot whose shelf was stocked before it
    was tagged.

## 2026-07-31
- **Pools are declared as a FOLDER now — `pool_dir` + `pool`, replacing `files = [...]`**
  (`references/media.md` §1 + §7 + cheat sheet, `references/toml-gotchas.md`).
  **Why:** an explicit list forces the author to guess the count *before seeing a single clip*,
  and every entry it can't fill sits on the missing list forever. A folder inverts that: the
  contents play, so curation is adding/removing files in the review UI rather than editing TOML.
  `pool = 4` survives as a **target for find-media, not a manifest** — the folder is the truth,
  so 3 clips play a 3-cycle and the audit says "3 of 4" instead of a half-filled pool passing as
  finished. Engine: `v2.py:11871` `_resolve_pool_dir`, `:11895` key-on-folder, `:14290` video branch.
  - **The folder shape removes a silent bug rather than working around it.** Numbering *filenames*
    (`oral_t5_1.webm`) pushes the `_tN` tier tag off the end of the stem, and tier detection is
    `$`-anchored (`_(t[0-8]|base)$`, `apply_retags.py:36`) — explicit content would have gone
    untagged and been routed as SFW. On a folder the tag stays last on the folder name. Documented
    in `toml-gotchas.md` so nobody re-invents the numbered-filename version.
  - **The cycle counter is keyed on the folder**, not the contents — so selecting/unselecting a
    clip never resets a player's position mid-playthrough.
  - **`files = [...]` demoted to legacy**, not removed: `the_long_summer_test` ships 30, and
    precedence (`pool_dir` > `files` > `file`) is declared once in `apps/common/media_blocks.py`.
- **Restructured §7 as three ordered GATES, and deleted the duplication.**
  **Why:** the 07-30 pass stated the same facts 2–3× each across §1 and §7 (`"3–4"` 3×,
  `"searches once"` 3×), and it taught *how many* before *whether*. §7 now asks, in order:
  (1) **is it NSFW and on a repeatable canvas** — both, per LO; (2) **are the clips
  interchangeable** under one description (the fillability gate); (3) **should it rotate or
  escalate** (a `group` chain, not a pool). Sizing and cost come after. §1 keeps the block shape
  plus one pointer.
- **⚠️ Corrected two wrong numbers from the 07-30 entry below.**
  - *"How many: 3–4, not a taste call"* — that was a **clip** figure (frame-strip survival
    3-of-5 / 4-of-6) applied to stills as well, and stills are never stripped. It also
    contradicted the only shipped precedent, whose image pools hold **5–11**. Moot now that the
    count lives in `pool = N` rather than in the author's head, but the doctrine said something
    false and the ledger should not preserve it.
  - *"+320 MB"* — real arithmetic on an invented premise ("pool a third of a game"). Replaced
    with the marginal figure: `vesper` averages **2.9 MB/clip** (380 MB / 113), so a 4-clip pool
    costs **~8.7 MB** more than a single clip. Multiply by your own count.
- **Wired the doctrine into where authors actually decide** (`references/beat-authoring.md` Step-7
  `**Media:**` hook, `references/lanes.md` Lane 1 + Lane 3). **Why:** measured reachability before
  this change — `beat-authoring.md` **0** mentions, `content-design.md` **0**, `SKILL.md` **0**,
  `lanes.md` **1** (Lane 2 only), while `lanes.md:57` records Lane 3 as **~47%** of canvases. The
  guidance existed only in the file consulted for block *shapes*, so an author following the
  skill's own workflow authored a singular `file` every time and never met the question.

## 2026-07-30
- **Taught WHEN and WHERE to pool — the first pass only taught the mechanism**
  (`references/media.md` §1 pointer, §7, cheat sheet). **Why:** the morning's rewrite shipped a single
  line of usage guidance ("repeatable beats only"), which is a slogan, not doctrine — it left four real
  decisions unmade and one claim wrong.
  - **How many: 3–4, and it's not a taste call.** The author declares `files = [...]` *before*
    find-media ever runs, and measured strip survival is **3-of-5 / 4-of-6**. Declaring 8 writes four
    slots that will never fill and will read as unfinished work in every future audit.
  - **Corrected "Cost: near zero"** → **free to FIND, expensive to SHIP**. True for search effort, false
    for bytes: `vesper` is **380 MB / 113 clips / 2.9 MB avg** (measured `du`), so pooling a third of a
    game that size at 4 entries adds ~**+320 MB** — near enough to double the download for a game
    distributed as a zip. The original wording would have encouraged reflexive pooling.
  - **"Repeatable" replaced by expected VIEW COUNT** as the axis. A beat hit three times does not earn
    four clips — that's three files found, shipped and paid for so one can be seen once.
  - **Interchangeability test added — it decides whether a pool is fillable at all.** All N entries must
    satisfy the *same* `description`, so loose descriptions pool and tight ones can't. Grounded in the
    measured `lab_finish_facial_t5` result: *"his hand gentle at her head"* → `pool_all_dead`, **24
    candidates, all rejected**. A 4-entry pool there is 4× impossible, not 4× the variety.
  - **Pool vs. variant chain framed as the real decision.** Rotation ≠ progression: a pool asserts the
    entries are interchangeable and nothing changed but a counter. If the 4th viewing should differ
    because *state* differs, that's a `group` chain. Called out as the more dangerous error because it
    looks like it worked — it silently swaps character development for a slideshow.
  - Noted the residual: a pool freezes the prose, so on a heavily-repeated beat the words become the
    stale thing (→ N separate canvases, `lanes.md`).
  - **Deliberately NOT added:** a ship-gate check for "declared N, filled 1" (silent degradation is
    real but it's a different piece of work), and any new §. This is ~5 sentences into existing sections.
- **Media pools rewritten: `files = [...]` works on `video` too, and pools CYCLE**
  (`references/media.md` §1 + §7 + cheat sheet, `references/toml-gotchas.md`,
  `references/lanes.md`, `references/engine-reference.md` block vocabulary).
  **Why:** an engine change this day (`v2.py:11878` `_render_media_pool`, image branch `:14111`,
  video branch `:14290`) made three of this skill's claims **false**:
  1. *"The pool is IMAGE-ONLY, and it drops video SILENTLY"* (`media.md` §1, `toml-gotchas.md`) —
     a `video` block now takes `files` and applies no format filter at all. An `image` pool still
     refuses clips but now emits a `logger.warning` instead of vanishing unrendered/unrecorded.
  2. *"To rotate CLIPS, use a `block_pool` of `video` blocks"* (`media.md` §1/§7,
     `toml-gotchas.md`, `lanes.md:159`) — this is now the **wrong** advice, and expensively so:
     N video children means N `description`s and N `search_queries` sets for one beat, i.e. **4×
     the find-media cost** of a `files` pool for the same result. `block_pool` is retained and
     re-scoped in the docs to what it is actually good at — varying **prose** (Lane-2 ambient
     text) — and it deliberately stays random.
  3. *"emits `either(...)`"* / random selection (`media.md` §1/§7) — pools now **cycle**
     (1→2→3→1) off a counter in `$game_state.media_cycle`. Random was the bug, not the feature:
     over four clips `random()` repeats back-to-back 25% of the time, which is exactly the
     staleness a pool exists to remove.
  Added, because the skill never taught it: **where** pools belong (repeatable beats only —
  activities, ambients, sex loops; never a one-shot capstone, which plays once), the
  `<stem>_1 … <stem>_N` naming already shipping in `the_long_summer_test`, and the cost argument
  (one description + one query set ⇒ one find-media search; measured strip survival is 3-of-5 /
  4-of-6, so a slot already ends with 3–4 clean clips that used to be discarded).
  **Also corrected** the stale `v2.py` line refs in the passages touched (`image` handler was
  cited as `:13455-13659`, now `:14110`; `video` as `:13908+`, now `:14285`).
  **Verified:** 28 new v2-targeted unit tests + a real Tweego build + a headless Chromium probe
  showing `1,2,3,1,2,3,1,2` across eight visits; `vesper` rebuilt **byte-identical** at 2,154,638,
  so the feature is inert for every game that doesn't opt in.

## 2026-07-29
- **Documented the studio-identity keys and closed a recurring `[project]` drift**
  (`references/engine-reference.md` §8 + `references/ship-gate.md` §3 and the release checklist).
  **Why:** an engine change this session made the funding link and studio credit data
  (`[project] support_url` / `studio_name`, defaulting to the old literals so all 14 existing games build
  byte-identical). But §8 was the *third* instance of the same bug class, not a one-off: it listed only
  `id`/`title`/`description`/`quests_engine`, and `version`, `release_date` (shipped 7-16) and
  `starting_canvas` had never been added. Since `SKILL.md:76` makes §8 binding ("never invent a field the
  engine lacks"), a key missing from §8 is a key the skill actively tells authors *not* to use — and
  nothing rejects an unknown `[project]` key, so the failure is silent at merge, `--validate` and package
  alike. Fixed all of them: §8 now states the full nine-key set, both read sites (`:1597` constructor +
  `:1773` for `starting_canvas`), the silent-drop warning, and why the identity fallback lives
  generator-side (`build_guide.py` reads `[project]` raw, so an importer-side default would let the guide
  PDF and the sidebar disagree). ship-gate §3's "We don't monetise, so the choice is easy" was made false
  by the same engine change — reworded to the distinction that actually carries the argument (we take
  support, we don't sell access), so the cheat-page-is-free conclusion still stands on its own reasoning.
  Added a release-checklist item to verify the link's host and its 3-site count in the built HTML, with
  the reason it matters (re-hosting portals strip page credit but copy the file verbatim, so the in-build
  link is often the only surviving funnel). **Verified:** rebuilt Vesper before and after the engine change
  — both `index.html` hash `1c1a989f…`, identical to the shipped file, so the doctrine describes a change
  that provably moves zero bytes for games that don't author the keys; 24 new tests
  (`apps/game_generation/tests/test_support_url.py`) + 61 in `apps/game_generation/tests/` green; the 4
  failures in `apps/projects/tests.py` are pre-existing V1-generator tests, confirmed by re-running them
  against a stashed baseline. Live-checked the escaping in Chrome (a `&` in the URL round-trips to one real
  `&` and two parsed query params — the `&amp;amp;` in the source bytes is the normal SugarCube
  source-byte behaviour, not a bug). Note `generators/v1.py` keeps the old literals by design — it is
  frozen, so `--gen-version v1` and the DRF preview views still emit the hardcoded URL.

## 2026-07-28
- **Rewrote the paid-build media doctrine to SELF-CONTAINED** (`references/media.md` §3 + `references/beat-authoring.md`)
  and **added a git-tracked deploy check to the ship gate** (`references/ship-gate.md` §4). **Why:** both files
  taught "a paid build must go to a **gitignored** `output-paid/`" — stale. In practice the paid build is
  committed, served publicly (portal `paidBuild: true` → Beta Nut Build), and LO wants it **self-contained**
  (own `output-paid/videos/`, same structure as the free build, so the folder archives standalone). Following
  the old doctrine 404'd every paid clip on Pages: the media was on disk but gitignored, so it never deployed.
  New doctrine: build paid with the plain command (own `./videos`, NOT `--video-path`), **whitelist
  `output-paid/videos/` in `.gitignore` (required or it 404s live)**, commit both builds' HTML + media
  together; `--video-path` demoted to a niche weight-saver (borrows another build's tracked media, yields a
  non-standalone folder — don't use for a normal paid ship). The ship-gate check is the class-kill: every media
  path in the built HTML must resolve to a **git-tracked** file, not just a file on disk — catches
  "fine locally, 404s live" for any build/model. **Verified:** ran the check against both live vesper builds →
  0 not-tracked each (matches the live 200s); it flags gitignored media because `git ls-files --error-unmatch`
  fails on it. Engine untouched (the flags already existed since Apr; no `apps/` change).
- **Added save-safety §5 — "a gate-item's grant must be re-assertable, not a one-shot a carried save already
  burned"** (`references/save-safety.md`; renumbered the old §5 Pre-update checklist → §6, fixed the two live
  cross-refs in `references/ship-gate.md` and `references/prose-truth.md`, and added a §2 caveat that "adding is
  safe" covers flags/traits only). Cross-ref added in `references/clothing.md` §7 (story-granted gate garments).
  **Why:** a live Vesper player on 0.1.5 soft-locked — "wrong face for the floor, but I only have two outfits and
  neither is correct." Root cause (13-agent diagnosis, survived adversarial refutation): the disguise item
  `cover_analyst` was granted only on a one-shot dispatch that also set its gating flag, and the item landed a
  release *after* that dispatch shipped; the save-migration backfill (`setup.backfillStateDefaults`) carries
  flags/traits but has **no wardrobe branch**, so every 0.1.4→0.1.5 carry-over had the flag set, never received
  the kit, and jammed forever (the out-of-cover reaction gates on `unequipped`, not ownership). A correct skill
  would have taught putting the grant on the repeatable point-of-need reaction (idempotent `add` = no-op if owned)
  from the start, so this is a class-kill, not just a one-off. **Verified:** the doctrine matches the shipped
  Vesper fix (idempotent `add cover_analyst` on `react_calloway_precover`'s `exit_block.config`); grep confirms
  no dangling `§5`/`§6` references remain in the skill; the game hotfix built green (both free + paid, 0 media
  missing, `addToWardrobe(cover_analyst)` 2→3) and passed a live Playwright heal repro.

## 2026-07-27
- **Rewrote the `search_queries` craft** (`references/media.md` §4) after a measured A/B against the live
  search route. **Why:** every rule in that section was tuned for querying PornHub's own index directly and
  was taught as universal search law. find-media now searches Google Images, which behaves close to
  oppositely — long descriptive queries are fine, but *story* words wreck them. Retired "3-5 words,
  **setting word goes FIRST**"; the setting is now spent only when it carries meaning (danger / secrecy /
  squalor). Measured: on a dim-storeroom beat, six setting-led queries → 72 candidates / 2 usable; one
  act-led query → 28 / 5. Counter-case kept honest: on a dark-alley beat the darkness *was* the point and
  bright clips were rejected twice, so the setting word earned its place there.
- **Added the story-word prohibition** (same section) — names, "drunk", "nervous", plot state. These do not
  merely add noise; on a general image index they reclassify the query as mainstream. Measured: adding
  `drunk guy` to a working query returned film stills, news and social posts, zero usable candidates.
  Re-framed the old "banned words" list as merely *wasted* words, since that was the milder problem all along.
- **Added the anti-studio modifiers** (`amateur` / `real` / `voyeur` / `hidden cam`) — bright-studio-when-the-
  beat-wants-grimy is our most repeated rejection and these are the only reliable lever against it.
- **Added "the `description` is a checklist, not a caption"** (same section). **Why:** find-media derives its
  accept/reject gates from the description, so an unphysical description means whatever gets installed can
  never be judged wrong. Cost of getting it wrong, found this session: `vesper`'s
  `sex/renner_cheerup_alley_t5.webm` shows the woman **standing** while its beat says "on her knees" — it
  survived months because nothing was checkable enough to fail. Also asks the author to state what makes the
  beat *land* (eye contact / being used / him visibly wrecked), which is the one thing a searcher cannot
  infer from an act name.
- **NOT done deliberately:** did not introduce `must_show` / `avoid` as new TOML props. The engine tolerance
  for unknown props under `props` is unverified, and teaching a key that might fail a build is worse than
  teaching description craft that cannot. Revisit only with a green build behind it.

## 2026-07-26
- **Documented the new `--build free|paid` flag** in the two places that publish the build command line —
  `references/beat-authoring.md` (the "Prove green" block) and `references/media.md` §3 (QA vs publish
  build). **Why:** the flag ships the engine's new first-class cheat page (`[ui.cheat_page]`), and it
  **defaults to `free`** — so an author who never reads about it still produces the safe artifact, but one
  who wants the supporter build needs to know it exists. These two files are the *real* callers: the skills
  shell out to `manage.py package_from_toml`, so a flag missing from here is a flag nobody uses. Both notes
  record the tripwire — a `paid` build is refused into any directory named `output` (git-tracked, PUBLIC
  repo) and must go to a gitignored `games/<slug>/output-paid/` — and that both builds come from ONE merged
  TOML, never an edited source. **Verified:** `package_from_toml --build paid --output games/vesper/output
  --dry-run` raises the CommandError; `--build bogus` dies in argparse; `git check-ignore` confirms
  `games/*/output-paid/` is ignored.
- ⚠️ **Still owed (tracked, not yet done): `ship-gate.md` §3 is stale.** The supply/demand studies of
  2026-07-26 refuted four of its eight claims, and it still specifies the cheat page as hand-authored TOML
  with a `[settings] cheat_grants` switch — both superseded by the engine feature. Two new doctrine rules
  also need a home: **an `lt`-only gate is a WINDOW too** (raising a trait past it deletes the alternative
  route — measured in Vesper's burned yard, where buying stealth removes the fight/emitter/flee routes), and
  **random/substitution bands are never step-safe** (reachability is chance × in-band dwell, so any step can
  skip them). Evidence: `games/vesper/design_cheat_page.md` §13 + the memory notes
  `cheat_page_mechanism_study` / `cheat_demand_study`.

## 2026-07-25
- **Batch F — PROMOTED 8 proven gaps from The Inheritance's staging log into the skill** (the last batch of
  the doctrine pass). Sources: `games/the_inheritance/skill_gaps_observed.md`, whose entries are written
  against the standing test *"would a correct author-game skill have prevented this?"*. Landed:
  **GAP 4** → `step-5-blueprint.md` Pass 4, the **mechanical READS ⊆ SETS trace** (Pass 4 used to accept a
  prose "verified"; on this game it certified `hotel_in_hand` reachable while it was read by three arcs and
  set by zero canvases) · **GAP 5** → Pass 2's per-NPC self-check, the **lane mix-table must equal its
  enumerated sections** (a header promised 4 ambients that were the same beats already counted in Lane 3) ·
  **GAP 6** → `toml-gotchas.md`, **CORRECTED** (below) · **GAP 7** → `rts-flat-prose.md` §7 check 1, the
  person-grep fix, **both branches** (the third-person branch used the same pattern as an *inclusion*, so
  changing one alone would have desynced them) · **GAP 9** → a new `beat-authoring.md` row +
  Pass 4: **sequenced auto-fire capstones need a strict stage BAND**, because auto-fire picks the
  highest-priority eligible canvas and never consults your intended order — an ungated feeder (the
  *recommended* on-ramp shape) pumped the odometer and handed over the keys at stage 0 · **GAP 10** →
  **merged into** the existing terminal-flag doctrine rather than duplicated (`beat-authoring.md`'s
  "retire the standing surface" row + Pass 4 now carry the **mechanical post-flip check**: set the flag,
  confirm no pre-flip canvas is eligible) · **GAP 11** (skill half) → `location-design.md` §6 ×2 rows +
  `toml-gotchas.md`: `entry_conditions` are **never scanned** by the flag-chain validator, and a room with
  a declared job needs a canvas actually LOCATED in it (`grep trigger.location`) — the v1 Dining Room bug
  shipped twice, the second time in the rebuild written to prevent it · **GAP 12** → `clothing.md` §9 as
  OWNER (never enable clothing before an `initial=true` garment; the empty catalog pins the portrait to
  `naked_image` from turn 0, permanently) with pointers from `step-0-1-seed.md` and `beat-authoring.md`.
  **GAP 1 HELD** (LO's call — its own gate is a subjective read of built prose nobody has made); GAPs 2/3/8
  stay staged. All eight statuses updated in the game log.
  **⚠️ GAP 6 was FALSE as recorded, and that is the batch's real lesson.** The log blamed the flag-chain
  validator for not seeing `location`-type exits. Code says the opposite: it scans them
  (`v2.py:11138-11152`), the setter index scans them (`:8363`), the importer scans them
  (`template_import.py:2834`), and they apply at runtime (`:12888-12893`). The actual bug is that
  `exit_block` is parsed with exactly four keys — `type`/`text`/`config`/`choices`
  (`template_import.py:2045-2060`) — with **no unknown-key rejection**, so the game's
  `[exit_block.effects] flagEffects` was **silently discarded at import**: the flag was set by nothing and
  `NEVER SET` was a **true positive** wearing a confusing message. The game's fix (move to a choices exit)
  worked *by accident*. Promoted as the corrected rule; the log entry now carries a dated correction block
  preserving the wrong diagnosis as a record. The meta-lesson, written into that block: the old promotion
  gate ("proven — it hard-failed a real build") proved a **symptom, not a mechanism** — a red build tells
  you something is wrong, never why. **Verified:** one adversarial agent re-checked all six engine claims
  in code and found **five defects**, all fixed pre-commit: (1) **my `\byou` prefix grep introduced 8 real
  false negatives** — it also matches *young*/*youth*, silently swallowing genuine third-person paragraphs;
  corrected to `\byou\b|\byour` (empirically tested: catches yours/yourself/you're, ignores young/youth),
  and my stated rationale was itself wrong since `\byou\b` already matched `you're`/`you'll`/`you've`;
  (2) "the packager silently drops empty rooms" was unsupported — an empty room *renders* as a navigable
  dead end, which is worse and truer; (3) "`entry_conditions` fail open ONLY on an empty item list" missed
  the second fail-open (a missing `version = "1.0"`, `v2.py:3683`); (4) a new `clothing.md` row restated
  two rows directly above it — folded the three novel sentences into the existing owner row; (5) the GAP-6
  block claimed the original was "kept verbatim" while the diff had removed its proposed-edit paragraph —
  wording corrected to say what was removed and why. Plan:
  `~/.claude/plans/lets-make-these-changes-sprightly-teacup.md` — doctrine pass COMPLETE; the eval round
  against `skill-snapshot-v2` is the remaining step.
- **Batch E of the mopoga-study doctrine pass — TEXTURE: glimpse rotation · media insurance · the register
  guard.** (a) `references/lanes.md` Lane 2 gains four additive bullets (no new heading — Lane 2 already IS
  the glimpse ambient): **an ambient is a POOL, not one canvas**, with the two buildable shapes and what
  each is for (N random canvases = clip *and* prose vary together, proven; one canvas with a `block_pool`
  = the clip rotates while the prose stays put); **it's an interstitial, not a backdrop** (a random ambient
  `<<goto>>`s away and takes the screen — the location page carries no media of its own; a location's
  `image` is a CSS background on its *nav card*); the **no-NPC boundary** (same mechanism, but world
  texture is `location-design.md`'s question); and **the pool can heat up with the accumulation state**
  (Batch B). (b) `references/media.md`: `block_pool` documented as the **video-capable** rotation (§7),
  the `files`-pool **image-only silent-drop** warning (§1), stale `v2.py` refs corrected, and NEW **§7b
  media insurance** — the repo is not a backup, the find-media manifest needs the same off-tree mirror,
  scene identity slots want replaceable framing (**both portrait surfaces exempt**), never name a
  performer in prose. (c) NEW `references/toml-gotchas.md` entry for the `files`-pool landmine. (d)
  `references/rts-flat-prose.md` NEW **§1E** — a *second evidence class*, explicitly labelled and
  explicitly not re-derivable inside the skill, recording the field study's finding that the flat
  caption-over-clip economy is what the market's top tier ships, ending in the regression clause. One
  checkbox in `references/ship-gate.md` §4. **Why:** the study's porn-as-wallpaper finding (the densest
  games rotate per-location clip pools so the world is never dry between authored scenes) + three media
  cautionary cases (a top-20 game legally forced to swap real porn for AI art and its audience revolted;
  another recast its performer-NPCs — "I want my mom back"; a third had to rewrite quests when actresses
  retired) + the register needing a market anchor, not just a house one. **Verified:** 2 adversarial
  agents, engine claims re-read in code. **The design was overturned twice and both saves mattered.**
  Pre-write exploration killed the original "wallpaper behind the room" concept — a random ambient
  `<<goto>>`s AWAY from the location and the location passage emits no media block, so that shape is
  unbuildable; the doctrine was rewritten around what the engine actually does. Then the coherence pass
  killed my replacement shape: I prescribed "each pool entry = a clip + its ~30-word beat", but a
  `block_pool` branch renders **exactly one block** (`v2.py:13681` passes `[pool_item]`) and `video`
  carries no caption prop — so that pool would have emitted N silent clips. Rewritten to what works, with
  the two-pools-don't-sync trap (`_bp` is rolled independently per pool) named. Other fixes: "no shipped
  game uses `block_pool`" was false (it ships in three games with text children — only *video* children
  are unproven); **two factual errors in my own numbers** — I called the measured game "the single
  most-played real-porn sandbox" when it's rank 12 of 30, and said "several winners market the opposite"
  when exactly one does; the ~36-word median is a 400-passage sample, not the full 3,694; a
  self-contradiction where my no-NPC rule disqualified the very `vesper` canvases I cited as the proven
  shape; `.find-media/` being git-ignored (so "treat it as part of the game" needed the mirror caveat);
  the NPC portrait card missing from the framing exemption; the claim landing three times in one file
  (preamble + §1E + a §7 check-6 bullet that duplicated the bullet three lines above — cut); and a stale
  video-handler line ref. Plan: `~/.claude/plans/lets-make-these-changes-sprightly-teacup.md` (F + the
  eval round pending).
- **Batch D of the mopoga-study doctrine pass — SHIP GATE + the player cheat page.** NEW
  `references/ship-gate.md` — the skill's **first whole-game, post-authoring gate**. Every other audit fires
  earlier (Step 6 reviews the *blueprint*, before prose exists), narrower (per beat / canvas / location), or
  only on a *re*-ship (`save-safety.md` presupposes a last-shipped baseline; nothing covered a first
  release). Six sections: **§1 meter-ceiling audit** (`max reachable` ≤ `highest authored gate`, or an
  honest terminal band — a bar that fills past what it can buy) · **§2 dangling-promise sweep** (every named
  person/place/teased act is paid, cut, or *logged* as a telegraphed seed; a scanner, not a verdict) ·
  **§3 the cheat page** (player-facing, free, diegetically skinned — grants money + declared climbing meters
  ONLY, never a story flag, never a `<slug>_stage`/`awareness`/loop-counter trait, routed
  `targetType="location"` so gates re-evaluate) **+ the `dev_mode_enabled` dev-shortcut contrast** ·
  **§4 build gate** (drop `--dev`/`--debug`, keep `--video-folder`; MISSING-placeholder grep == 0; no dev
  surface leaked; `type="video"`-shipping-`.jpg` mismatch) · **§5 re-run the whole-game scanners** (both lint
  scripts, `prose-truth.md` §4 over the release range, `rts-flat-prose.md` §7 checks 3+7,
  `location-design.md` §6) · **§6 release discipline** (`save-safety.md` §5 + the `releases/vX.Y[.Z].html`
  convention, documented for the first time). **Deliberately NOT a new pipeline phase** (LO's call): the
  `pipeline_phase` enum ends at `authoring` and shipping recurs — Vesper has shipped v0.1→v0.1.3 and is
  still authoring — so the gate is invoked per release, which also reconciles with `run-mode.md`'s
  "playable ≠ done". Wiring: `SKILL.md` (index + the step-2 declarations row), `beat-authoring.md` (step 8
  milestone build = the invocation point, + the Step-7 ENTRY flags note), `media.md` §3, `save-safety.md`
  §5, `systems.md`, `step-2-toplevel.md` §8 + Output + Self-check, `trait-catalog.md` §4, `run-mode.md`.
  **Why:** the study found cheat-code demand is the genre's most universal player behaviour (the #1 game
  ships a free default-on menu and draws essentially no grind complaints; the ones that sell codes monetise
  their own friction — we don't monetise), that a meter exceeding its content reads as a paywalled insult,
  and that players quote unpaid named hooks years later. Plus our own live `--debug` ship that baked 147
  MISSING placeholders into a public Vesper build. **Verified:** 2 adversarial agents; the highest-risk
  area — §3's engine claims — **verified clean in code** (`v2.py:8285-8311` `_is_dev_shortcut_canvas`: the
  `dev_mode_enabled` marker detection, five skip sites across the flag-chain validator / hint index /
  flag-setter index, the `--dev`-only StoryInit flag, the `<<devJumps>>` render). **12 confirmed defects
  fixed pre-commit**, notably: two citations pointing at `notes/*.md` files that live OUTSIDE the skill
  (restated narratively — `SKILL.md` promises you never need to leave the skill); the `trait_effects`
  preview claim overstated (value>0 filtering is the FLAT path only — the tiered path is an unfiltered
  all-tiers flatten, `v2.py:10514-10519`); **the cited cheat-page template would have failed my own §4**
  (`mothers_place`'s file is a dev page labelled `[DEV] Shortcuts` — now cited for its SHAPE only, with an
  explicit re-skin instruction); "each with the `cap` its band expects" contradicted by money being
  correctly uncapped; **three gate-free publish exits** (`media.md` §3 — the file ship-gate delegates the
  command to — plus the Step-7 ENTRY note and `save-safety.md` §5, all now carrying back-pointers); a
  `systems.md` paragraph that was a second copy of §3 in a file whose own scope statement excludes authored
  canvases (cut to a pointer); an unenforced Step-2 §8 declaration (added to Output + Self-check + the
  SKILL row); a `trait-catalog.md` insert that split a two-item list; a mis-placed `run-mode.md` corollary;
  a `quests.md` §6 over-claim (same code path, different trigger — now worded as an extension); and
  section-name drift. Plan: `~/.claude/plans/lets-make-these-changes-sprightly-teacup.md` (E, F + the eval
  round pending).

## 2026-07-24
- **Batch C of the mopoga-study doctrine pass — PITCHING: how to propose the next thing so it lands hot.**
  NEW `references/pitching.md` (125 lines) — the quality bar for every content pitch *after the seed* (a
  beat, an arc, an NPC, a chunk): **the five parts — charge · ladder · person · deposit · cost** — plus
  **the heat test** ("can the reader see the erotic trajectory from the pitch alone, or is it a plot idea
  wearing lingerie?"), a worked ✗/✓ contrast from `vesper`, the present-it-as-editable-prose rule (LO's
  standing preference), and the two anti-patterns the five parts don't already catch (the systems pitch,
  the costless pitch). The five parts deliberately hook the rest of the skill: part 1 names kink areas from
  `kink-ceilings.md` §2, part 4 deposits into Batch B's accumulation object / machine, part 5 names Batch
  B's fail-state form. Wiring: `SKILL.md` knowledge index, `references/run-mode.md` ("Navigation at
  junctions" — *when* you propose stays there, *what the proposal contains* is pitching.md; they compose on
  Mode A forks), `references/step-6-feedback.md` (gap-fixes that propose new content), `references/
  step-2-toplevel.md` §6 (a frontier next-hook seed is a promise of desire, not plot), `references/
  step-0-1-seed.md` (Step 0's 3-part bar fires ONCE on the founding fantasy; pitching.md governs every
  pitch after). **Why:** LO's ask — "the main part is the story… I want good hot ideas, the story ideas
  that work, that give the experience of the level that matches the top games." The study found the field's
  winners pitch a legible desire trajectory (ordinary person + instrument of power + institution), that
  players praise characters and never plots, and that our own instinct is to pitch intrigue with the sex
  attached afterward — Vesper's best beat worked *because* it accidentally inverted that. Step 0 already
  gated the GAME's fantasy; nothing gated the pitches after it. **Verified:** adversarial coherence agent
  confirmed 4 real defects, all fixed pre-commit — most seriously **the worked example invented `vesper`
  facts**: it gave Calloway an "estate" (he works at `vance_securities` + a file room), inverted his
  characterization (the TOML says *humiliated, sidelined… starving to be believed*, not a controlled man
  who's never been out-played), mis-gendered Vane (male) and inverted his function (he's the mole who gets
  caught, not a watcher), and cited the doc-bug that was DEMOLISHED from the game. Example rewritten from
  the actual NPC blocks — and it's a better example, since Calloway's real lever (belief, not charm) is
  exactly the "one trait that makes this corruption theirs" the doctrine asks for; also rewritten into
  third person to match vesper's locked register. Other fixes: a `kink-ceilings.md` §3→§2 pointer (the file
  cited both for one rule; §3 is the near-inverse "default to most explicit" rule), a Mode-A contradiction
  (run-mode makes core-target/hook pitches an ASK; the no-menu rule now explicitly governs option *content*,
  not whether you ask — stated in both files), and an anti-pattern list that restated the body (trimmed
  6→2, keeping only what the five parts don't already catch). Plan:
  `~/.claude/plans/lets-make-these-changes-sprightly-teacup.md` (batches D–F + one eval round pending).
- **Batch B of the mopoga-study doctrine pass — THE MACHINE: what compounds · deposit legibility · the
  fail-state FORM.** (a) **`references/step-2-toplevel.md` §4 OWNS "What compounds — declare it"**: name the
  ONE thing that grows and becomes hers, its sinks, and its states — *each state unlocking CONTENT* (a room,
  a person, a kind of scene), built as flags / a hidden `<thing>_stage` gated by ordinary `gte` thresholds —
  **or declare "nothing compounds" on purpose** (the house style of the fail-state / systems-ON-OFF /
  thin-on-purpose declarations; LO's call — a declared choice, not a blanket mandate). Positioned as the
  *noun* §7's core loop deposits into (NOT a second loop, NOT Form 3 — still G6-deferred), deferring the
  management-collapse test to its owner `content-framework.md` §1F. Recipe appended as
  `references/system-patterns.md` **§8** (never inserted — `content-framework.md`/`step-6-feedback.md` cite
  "§7" by number), with the file's "not picked at the seed" premise explicitly excepted for it. (b)
  **`references/lanes.md` Lane 3 OWNS the deposit rule**: a charged repeatable lands something the player can
  SEE it bank *that turn* (coin on the HUD · a readable odometer tick · a quest goal's live `current / value`
  line), **pay-AND-brake**, with the presence floor / Lane-2 texture / zero budget cells **exempt on
  purpose**. (c) **`references/content-framework.md` §1C** (already the single OWNER of "does failure
  exist") gains the four form-names — **danger · debt · deadline · decay** — plus the requirement that a "no
  failure" answer **state its cost**; deliberately NOT a new doctrine and NOT named "teeth" (that term
  already means NPC pushback at §3A). Sync surfaces: step-2 §7→§4 back-pointer, Output sentence ×2,
  Self-check ×2, `content-framework.md` §2C question + **both mechanism-bridge-table rows** (§1 fail-state
  forms, §2 accumulation object — the file's own law is that a question whose answer can't land on a real
  knob doesn't ship), `step-5-blueprint.md` Pass-1 Gate + "Economy made real" (without which the Step-2
  declaration never got blueprinted), `trait-design.md` throttle recipe (+ "the rung PAYS, visibly"),
  `beat-authoring.md` ×2 self-audit rows, `step-6-feedback.md` ×2 echo rows, `SKILL.md` / `systems.md` /
  `run-mode.md` recipe enumerations. **Why:** the mopoga top-30 study (report §F2/F4/F9) found the winners
  are engines of accumulation with arcs hanging off them (buildings gate content in Apocalyptic World;
  per-girl ladders nest in Patriarch's city; Free Cities logs 1 grind complaint in 831 because management IS
  the fantasy; Destroyer mints perk currency for replay), that legibility — not payout size — is what makes
  repetition read as progress, and that players beg for consequence over scenes. Vesper (133 canvases) and
  The Inheritance (105) have nothing that compounds; money is only rent-pressure. **Verified:** 2 adversarial
  coherence agents + 1 design agent reviewed the cut and confirmed **9 defects**, all fixed pre-commit — most
  seriously **a hallucinated engine fact of mine**: I wrote "the engine has no built-in decay" on the
  strength of `rts-design-philosophy.md` P2's absolute-sounding line, then verified in code that
  **`trait_decay` is a first-class, neglect-keyed primitive** (`v2.py` daily tick skips any NPC the player
  interacted with that day and floors at 0; player-side variant runs daily; importer-validated; sidebar
  auto-emits `trait_decay_warning`; documented at `engine-reference.md`). Both the new text and **the P2
  source line that misled it** are corrected (P2 now reads "never reset **by default** — nothing decays
  unless you opt in", with a dated correction note). Also fixed: `bands` conflated with gate thresholds
  (bands are a sidebar *render* field); "hiding a trait prevents the banded-stat vanish" (it does NOT —
  `trait-catalog.md` §5 says the band renders regardless; only clamping fixes it); "nightly ledger" invented
  as an engine surface (replaced with real knobs); §1C linted against a "decay" label it never defined; a
  "Pushback named" review row colliding with §3A's "teeth"; §1C reaching into §5C/§5E territory without
  defer-pointers; the "empty cell" term smeared onto payless-but-filled surfaces; and one-directional
  ownership (step-2 named lanes.md as owner while lanes.md never claimed it). Plan:
  `~/.claude/plans/lets-make-these-changes-sprightly-teacup.md` (batches C–F + one eval round pending).
- **Batch A of the mopoga-study doctrine pass — GUIDANCE: walkthrough-grade quest cards + onboarding
  winner-patterns.** Files: `references/quests.md` (§3 gains three rules — the **walkthrough-line standard**
  for `goals[].label` (place + person + verb (+ window)), the **gate-tell/feeder rule** (a meter-gated rung
  names the repeatable that raises the meter, in-world), and the **NPC-voice `tip` sanction**; §9 checks
  updated to enforce both), `references/step-2-toplevel.md` (§5 aligned: trait gates name their feeder;
  quests.md §3 named as the mechanics OWNER so the standard lives once), `references/beat-authoring.md`
  (Quest-cards bullet corrected — the step must ride `goals[].label` because the sidebar renders only the
  goal block, `text`/`tip`-only steps vanish from the sidebar; new **quest-card walkthrough-line row** in the
  per-beat doctrine self-audit incl. the Frame-3 blank check), `references/onboarding.md` (§2.9 extended with
  the **sandbox contract on the first screen** + **announce the content ceiling early**; new **§2.10 every
  chargen pick pays**; §3 advisory row + §7 cheat-sheet: **first lewd within ~15 clicks** on the recommended
  path — advisory, the stricter onboarding cousin of Rule 9's floor). Also `references/hud.md` (both
  `next`-row formula statements now point at the quests.md §3 standard instead of restating the old
  PLACE+TIME-WINDOW+REQUIREMENT wording). **Why:** the 2026-07-24 top-30 mopoga Twine-sandbox study
  (`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/report.md` §F1) measured lostness as the genre's #1
  killer — guidance-lost median 4.7% of ALL player comments vs grind 0.9%; the winners ship literal in-game
  walkthroughs (New Lust per-girl progress pages, CoT hint-cards, Destroyer's ~151 NPC-voice hint pages)
  while our doctrine taught a one-sentence directive style. Evidence cited inline in each edit. **Verified:**
  2 adversarial coherence agents reviewed the edits against every cross-referencing file and CONFIRMED 9
  defects in the first cut — 3 stale contradicting rows (beat-authoring's old legibility row still said "put
  the action in `text`/`tip`" and its trait-naming row conflicted; hud.md carried the competing formula
  twice), a mis-homed §3-vs-§6 pointer, §5's "single sanctioned out-of-fiction line" contradicted by the new
  first-screen contract, a kink-ceilings mis-attribution (game-level "ceiling register" isn't a concept that
  file defines — rescoped to premise-level darkness per content-framework §1D, with the tier-leak ban
  respected), a §2.10 rule the customize screen can't express (stat grants rerouted to funnel choice-beats
  with `effects`), two silently-condensed "verbatim" study quotes (restored exact), one phantom term
  ("reachability floor" → Rule 9's actual "a floor, not a quota"), and missing rubric rows for 2 of the 3
  new onboarding beats (added as §3 advisory). All 9 fixed in the same turn; the engine claim (sidebar
  renders only the goal block) was independently re-verified against v2.py by the reviewer. Committed as the
  Batch-A commit. Plan: `~/.claude/plans/lets-make-these-changes-sprightly-teacup.md` (batches B–F + one
  eval round pending).
- **added the AROUSAL AXIS — a game-wide "write to arouse / player-as-erotic-subject" doctrine — as `references/rts-flat-prose.md` Rule 9 + §7 check 7, hooked in at every design decision point.** Files touched: `references/rts-flat-prose.md` (new **Rule 9 — "Write to AROUSE"** after Rule 8: player-is-the-subject-not-spectator · show-the-act anti-elision · a reachability FLOOR with the two-model nuance · a cold→hot same-act example · a "hot ≠ purple" guard; new **§7 check 7** "Written to arouse" read-audit; a preamble contract clause; a Rule-4 "passing the ratio makes prose SPOKEN not HOT — necessary, not sufficient" caveat; the `third`-person bullet now names the cooling; Contents/§3-header/never-relax counts **8→9**), `SKILL.md` (register bullet gains "the three axes serve one end"; doctrine-library entry **8→9 rules** naming Rule 9 — "three axes"/"All three" deliberately left intact, the axis count is unchanged), `references/step-0-1-seed.md` (person-choice `third` bullet: third-person cools the porn), `references/content-framework.md` (§1A new "whose pulse, from what seat?" bullet + §1B "Who climbs?" still-point cooling caveat), `references/step-2-toplevel.md` (still-point variant: know its cooling cost), `references/step-6-feedback.md` (new self-check row: player-as-erotic-subject / heat-on-the-page / anti-elision), `references/sex-loop.md` (`## Voice` anti-elision rule + a self-check bullet: every act-result beat DEPICTS the act), `references/kink-ceilings.md` (§1 "lead with the hot version" now flagged as the per-scene corollary of Rule 9), `references/lanes.md` (Voice-register note points to Rule 9). **Why:** a review said Vesper "reads as black-noir, not a porn game." A 9-game external study (DoL, The Company, Newlife, Girl Life, CoC2, …) + player-sentiment sweep + first-hand full-corpus measurement of our own two games found it **systemic, not one-off**: `vesper` (third person, 3.67:1 narration:dialogue, negation-heavy lexicon `doesn't`/`nothing`/`empty`, 100%-plot interiority) AND `the_inheritance` (a CLEAN 1.47:1 + second person, yet **zero explicit vocabulary in 673KB** and **every sex act elided** behind a closed door + stat bump) both read cold. Root cause (doctrine audit): the skill optimized SHAPE / STRUCTURE / COMPLETENESS and defined "flat/specific/crude" but **never defined "hot," never named the player as the erotic subject, never forbade eliding the act, and had no arousal check at Step 6** — and it *blessed* the two cooling choices (third person, still-point owned-weapon PC) framing their cost only as lost *craft*, using Vesper as the worked exemplar for both. The narration:dialogue rule (the "one that matters") is a screenplay-ness metric a noir author passes while writing nothing arousing. **The reachability rule is written as a FLOOR, model-agnostic** (protect "something hot is always reachable"; respect both ambient-survival à la DoL and earned slow-burn à la Being a DIK/Karryn) rather than pushing "frequent sex" — LO's flagged call, so it fixes coldness without flattening a slow-burn game. **Verified:** grep sweep confirms (1) zero stale "8 mechanical prose rules" / "satisfies all 8" / old never-relax line; (2) new "9" / "all 9" / "Rules 1, 2, 4 and 9 never relax" present; (3) SKILL.md "three axes" + "All three" UNTOUCHED (additive, not a 4th axis); (4) Rule 9 reachable from all 9 skill files; (5) §7 check 7 numbering unique (checks now 1–7). Pre-edit grep confirmed the doctrine was genuinely ABSENT skill-wide (0 hits for "arousing"/"written to arouse"/"erotic subject"/"elide"/"blue balls") so nothing was duplicated — the new rule cross-references the existing siblings (`kink-ceilings.md` §1 "deliver at the ceiling"; `rts-flat-prose.md` Rule 3 "a hot beat with no body in it is under-written"; the `arousal`-throttle heat-of-the-moment rule) rather than restating them. Doc-only change (the skill is patterns, not code) so no build/eval was run — this is subjective craft doctrine and the real gate is LO's read of Rule 9 + §7 check 7. Scope: Vesper ships as-is (not rewritten); the Inheritance elision fix is a separate follow-up. Committed 2026-07-24 (this commit also fixes the one stale count the sweep missed: `rts-flat-prose.md` intro line 6 "eight numbered rules" → nine).

## 2026-07-23
- added the **"retire the standing surface on the terminal flag"** doctrine (`references/lanes.md`, new subsection right after Lane 4) + surfaced it (`references/beat-authoring.md` per-beat doctrine self-audit bullet, next to `frontier`; back-pointer added to `references/content-framework.md` §4E). **Why:** the skill taught authors to *think about* "what changes after a turning point" (scattered story prompts — content-framework §3C/§4B/§4E, step-4 item 6, all deferring wiring to Blueprint) and how a one-shot capstone retires *itself* (lanes.md self-retire), but had **no consolidated rule to sweep every STANDING surface an NPC still offers and gate it on the terminal flag** — confirmed absent by a skill-wide grep. Root cause of a real Vesper bug class: after the Archive-1a drain + blowup, Calloway's hub choices / `work_the_case` / floor cluster and Mercer's hub kept running pre-milestone content (courtship offered to a man she owns; a hub for a man who fled). The new section names the full cluster (hub · Lane-2 ambients · Lane-3 walk-in/drain/work · schedule presence · floor), teaches both fix mechanisms (per-canvas gate-or-`[group]`-swap **and** the zone-seal chokepoint shortcut), reconciles with the presence-floor rule (leave a still-in-character quiet hub; retire only a surface the beat makes *contradictory*), and gives a "name every surface, keep-or-gate each" test. **Verified** against the Vesper Phase-1/2 case — the doctrine names exactly the surfaces that were missed (hub / work / floor) and both mechanisms actually used (per-canvas gate for Calloway, zone-seal for the whole Spire); grep confirms the named pattern now exists and is reachable in ≤1 hop from the beat-authoring self-audit. **No lint** (a clean one is infeasible — it would false-positive on the zone-seal pattern the doctrine itself recommends, since a location-sealed cluster references no per-canvas flag) and **no subagent eval** (the cascade-gap eval this session came back non-discriminating; verified directly against the real case instead).

## 2026-07-22
- added the "`show_when_locked` + first-time-only gate" gotcha (`references/toml-gotchas.md`) — a rung gated on a consumed clause (`X lt 1` / `flag is_false`) with `show_when_locked` re-emits its `locked_text` after the gate is consumed, leaking a stale/contradictory line above the working repeat choice. Root cause: `show_when_locked` greys the choice whenever conditions are false, which includes the permanently-consumed state. Fix taught = drop `show_when_locked` on first-time-only rungs (they should hide, not preview). Live-caught in Vesper's Colm hub (the "Take him in the back" first-drain rung leaked "he still flinches" post-drain); verified the fix builds green + the stale line = 0 in the built HTML.
- added the "`cascade` must be the LAST content block" contract (`references/engine-reference.md`, right after the beat-0 contract) + a trap entry (`references/toml-gotchas.md`) — the engine draws every top-level block eagerly in source order and a `cascade` reveals only its own beats, so any prose placed AFTER a cascade renders immediately below the advance link (the `[content][link][content][link]` layout), and two cascades in one node splice the `exit_block` twice → a duplicate nav link. Root cause traced in v2.py (`_convert_blocks_to_game_html` eager loop + the exit-splice machinery); the rule (cascade last, one per node, fold trailing prose into an `advance_text` or no-`advance_text` terminal beat) was assumed by the engine (a code comment even says so) but never surfaced to authors. Diagnosed via a 4-agent workflow (engine read + live repro + whole-game TOML audit + skill-doctrine check); live-caught in Vesper's `cap_vane_blackmail` + `cap_1a_close` capstones, both fixed + rebuilt green.
- RESOLVED the cascade gap PROPERLY (the bullet above was the first-pass gotcha; LO asked to close it for real, via the skill-creator flow). Four moves: (1) **completed the cascade contract** in `references/engine-reference.md` — added the previously-ABSENT buildable SHAPE (copy-ready TOML, from the `_render_cascade` docstring at v2.py:13293-13316) + a "when to reach for it" line, so all cascade knowledge (shape + when + the beat-0 and cascade-last contracts) sits in one coherent home; (2) **de-duped** `references/toml-gotchas.md` — trimmed the verbatim contract copy down to a short trap statement + the runnable lint + a pointer; (3) **surfaced it at the author's entry points** — one-line pointers to the cascade contract from `references/rts-flat-prose.md` (top, "read before you write any scene body") and `references/beat-authoring.md` (the cascade note), the two surfaces a scene author actually starts from (they carried neither the shape nor the ordering rule before); (4) **added `scripts/check_cascade_order.py`** — a bundled lint (models `check_render_buckets.py`: same arg/`tomllib`/exit-1 shape) that walks canvases→nodes→`blocks` and flags any node with a content block AFTER a `cascade` (or >1 cascade), and **wired it into** the `beat-authoring.md` per-beat validation (now a two-script "Mechanical guards" step). Lint validated on real data: current Vesper clean (exit 0), git-HEAD Vesper correctly flags all 3 historical defects (`cap_vane_blackmail` / `cap_1a_close` / `act_colm_drain`), **0 false positives** across the other 5 games (last_call, late_shifts, mothers_place, the_inheritance, the_long_summer_test) — confirming cascade-then-`exit_block` passes. The skill-creator eval loop (3 trap prompts × resolved-vs-baseline, in `author-game-workspace/`) came back **NON-DISCRIMINATING** — 6/6 both configs produced cascade-last scenes, because the strong (Opus) subagents self-corrected by reading the engine / `late_shifts` (the baseline agent even stated the render-order WHY the baseline skill never taught). Honest read: the **lint is the load-bearing fix** (teeth proven on the historical defects), and the doctrine is a documentation-completeness improvement whose behavioral value this eval did NOT isolate — it tested a careful single-scene author, not the fast-pour condition that produced the real defect. To measure the doctrine's behavioral effect, the eval must replicate pour-pressure (a faster model / one-shot no-engine-read); deferred.

## 2026-07-19
- **NEW `scripts/check_render_buckets.py` (the skill's first bundled script) + wired into the per-beat validation
  (`references/beat-authoring.md`, new step 3) + delivered the long-promised grep guard (`references/toml-gotchas.md`
  npc section; `references/lanes.md:366`).** Root cause — the "gate-gap": the skill *taught* the `npc` vs
  `requires_npc` render-bucket rule correctly and redundantly, but nothing *enforced* it. An author who sets
  `requires_npc` and forgets `npc` ships an NPC hub that renders as a flat solo LINK (not a portrait) with a GREEN
  build; it shipped across every hub in The Inheritance, and `lanes.md:366` even promised a "grep guard:
  toml-gotchas.md" that was never written. The script parses a merged `7_final_game.toml` and flags every
  repeatable/manual/non-substitution canvas with `requires_npc` and no `npc` (one signature = the Lane-1 hub trap
  AND the Lane-2 ambient-missing-`random` trap). It is a **review** guard, not a hard gate — a deliberately
  presence-gated flat link is a rare legit exception (e.g. vesper's `react_renner_threat`, whose own description
  says "Solo-link"). Also corrected the toml-gotchas note's unverified "8 hubs + 7 ambients" to the verified **8**
  (0 mis-bucketed ambients in the final game). **Verified:** exit-0 / 0 flags on the fixed Inheritance `7_final`,
  exit-1 / 8 flags on the pre-fix (`HEAD~1` 617d899); cross-game sweep clean on `last_call`/`mothers_place`, and it
  surfaced latent hits in `late_shifts` (2) + `vesper` (1) to review. Documented limit: it can't catch a hub
  authored with NEITHER field (mechanically identical to a real solo activity — needs a content read).

## 2026-07-17
- **`references/engine-reference.md` §location table — NEW engine field `auto_exit` (bool, default true).**
  Root cause: the engine assumes every location sits in a tree — a root-with-children or a child-with-a-parent
  — and Vesper's `underworld_gate` is neither. It's a **transit stop**: arrived at by canvas (the travel car)
  and left by canvas, and it is the only location in that game with **zero children** (spire←1, waterfront←5,
  strip←7, gate←0). A nav-less location trips the list-every-location fallback, so `entry_from` had been bolted
  onto the gate purely to feed the nav check a link, and `parent` added right after to undo `entry_from`'s side
  effect — two hacks cancelling out, with `[[Leave The Underworld Gate]]` as their exhaust. LO's diagnosis, and
  the right one: the engine had no *word* for this shape. `auto_exit=false` is that word — it skips the
  hardcoded `[[Leave <name>]]` **and** reads an empty nav list as intentional. Both halves are required; with
  only the first, the location dumps the entire map.
  - Engine: `TemplateLocation.auto_exit` (`template_import.py`) + carried via `loc.properties` in **both** build
    paths (`game_graph.py` no-DB default and `template_import.py` `--use-db`) + two guards in `v2.py`
    `_generate_hierarchical_navigation`. Additive default → existing games byte-identical. **Regression-verified:**
    `late_shifts`, which never heard of the field, rebuilds green and still emits all 15 of its `[[Leave ]]` links.
  - Worth knowing for future authoring, both found while doing this: the `[[Leave {location.name}]]` label is a
    **hardcoded f-string** with no TOML override — and the importer **silently ignores unknown location keys**,
    so an author writing `exit_text = "…"` gets no error and no effect. Also: `entry_conditions` gate the
    **passage**, not just the nav card (the emitted `Location_` passage wraps its whole body in
    `<<if setup.triggerConditionsSatisfied(...)>>`), so they cannot be used to grey a nav card while leaving a
    canvas-exit route open.
  - ⚠️ **A doc claim I got wrong, recorded so nobody repeats it:** I told LO `getNpcsWithSchedules` gates on
    `_isCanvasAvailable`, so a scheduled-but-unmet NPC wouldn't leak onto the Schedule page. **False** — I read
    the first loop and stopped. A second loop adds every NPC in the declared `setup.npcSchedules` registry
    *"regardless of whether any of its canvases are unlocked yet"*; the canvas scan is only a back-compat
    fallback for games declaring no schedules. **Declaring a schedule lists that NPC from turn 1.** That is a
    real design consequence of `[[npcs.schedules]]` and the skill does not currently say so anywhere.
- **`references/prose-truth.md` — NEW. The skill mandated a copy of every field into prose and never said the
  copy was a maintenance obligation.** Root cause: two same-day Vesper bugs of one class — Kess *said* "Twenty a
  session" after `costs` went 20→10, and a quest `tip` said "the Berth off the waterfront" after `kess_berth` was
  re-parented to `underworld_strip` (it also taught the deleted two-zone map). **Both builds stayed green** —
  flag chains valid, no warning; the game just lied to the player. Passes CLAUDE.md's "would a correct skill have
  prevented this?" test, so the skill gets fixed, not just the game.
  - **The framing matters more than the rule, and my first two designs were wrong.** (1) I proposed a "prefer
    derived over hand-copied" tier — **dangerous, killed.** `renderQuestsGoalBlock` gates the derived `📍`/`🕒`
    behind `goalState.allMet && card.ready_canvas` (`v2.py:14479`); the whole climb takes Frame 3 (`!allMet`,
    `:14494`) which renders goal bullets only. `getCostBlockedMessage` (`v2.py:4527`) prints only into
    `<span class="locked-choice">` (`:12233`) — silent when affordable. `_formatCanvasSchedule` (`v2.py:6842`)
    emits machine register ("Mon–Fri", "every day") and *cannot* write "evenings 6 pm–close". An author told
    "the engine derives it" would strip the tip and leave the player nothing. **The legibility mandate
    (`step-2-toplevel.md` §5) is correct and load-bearing — left untouched.** Derivation is reframed as an
    *oracle that checks the copy*, never a substitute. (2) A prose scanner — **killed**: a field-scoped digit
    grep is ~164 hits / ~2 true positives on Vesper, and value-matching reports **clean on the real bugs**
    because the prose form is deliberately a different register (`125` → "Hundred and twenty-five";
    `09:00` → "Nine sharp"). So the skill's sin is narrow and precise: it **creates an obligation it never
    names**. "Causes the bug" → "copy less" (wrong); "names the obligation" → "re-read on change" (right).
  - **The audit scopes by the diff, not the prose.** `games/` is git-tracked, so `git diff` knows which coupled
    fields moved AND their OLD value — the search key, otherwise unrecoverable once saved. Inline fenced block
    (no `scripts/` dir — this skill has none by design; audits are inline per `rts-flat-prose.md` §7), excludes
    generated `7_final_game.toml` + `#` comments + canvas `description`. Verified against all four real cases:
    the uncommitted re-price surfaces `costs value 20 → 10`; `7dc5e36^..7dc5e36` surfaces
    `entry_from "the_waterfront" → "underworld_strip"` (the OLD value being exactly the grep key that finds the
    stale tip); a rebuild-only commit and a prose-only commit both report **0** — a real false-positive floor.
  - **Worked example is the block this skill ships as canonical**, not Vesper: `rent.md` calls
    `late_shifts/toml_phases/0_systems_spec.toml` the "verbatim shipped block to copy" — `amount = 125` with a
    hand-authored `greeting = "Rent. Hundred and twenty-five. …"`. Verified `v2.py:15367`: the default
    interpolates `_rent`, an **authored override is a literal**, and the live value prints two lines below
    (`Rent is $<<print _rent>>`) + on the `Pay $N rent` button. Re-price → the NPC contradicts the UI in one
    screenshot. Named `prose-truth` (not `*-drift`: "drift" already carries four senses — literary, citation,
    design, `ledger-schema.md`'s anti-drift invariant; not `*-sync`: implies a mechanical reconciliation that
    provably cannot exist). Modelled on `save-safety.md` — same "green build, quiet break" shape; save-safety
    guards the player's *save*, this guards the game's *truth*. States the limit of the engine-citation analogy
    it generalises: that protocol tolerates staleness because the reader can re-grep — **the reader of prose is
    the player, who cannot.**
  - wired it in: `SKILL.md` (stable-and-extensible bullet — "changing what already exists is an amendment too";
    KB pointer beside save-safety) · `references/beat-authoring.md` step 3 "Amend structure — WHOLE" extended
    from **ADD-only** to cover MOVE / RE-PRICE / RE-SCHEDULE / RENAME-label (the site `save-safety.md` misses,
    and where the bug actually fires — pointers at the ~14 *creation* sites were rejected as counterproductive:
    the author is doing the right thing there) · `references/beat-authoring.md` legibility self-audit row
    amended from an **existence** check ("a goal-only card with no place+window fails this") to existence+truth
    ("…and so does one whose place+window no longer MATCHES the canvas's `location`/`schedules`") — closes the
    "no audit checks TRUTH" gap in one clause, no 26th row · `references/rent.md` §4 gains the
    authored-override-is-literal fact (a genuine factual gap, independent of this doctrine).
    Doc-only — no TOML, no engine, no game rebuilt. grep-verified every new pointer resolves.

## 2026-07-14
- **`references/rts-flat-prose.md` — REWRITTEN. The register doctrine was partly false, and it had never once
  been obeyed.** Root cause found by re-measuring the register claims against the **real** Road-to-Success
  source (`game_explorations/road_to_success/archive/2026-06-02T18-27-18-582Z/passage_catalog.json` — 364
  passages, 273 prose-bearing) instead of the inherited prompts_v2 summary. Three defects, all load-bearing:
  - **Rule 8's headline stat was an artifact.** "Half of RTS scenes are 25 words or less" → **actually 28%**,
    and those are Tier-1 one-liners; the **median RTS scene is 126 words**. The original figure (137 chars,
    `prompts_v2/doctrine/05_rts_flat_prose.md:121`) came from a **rendered-DOM capture**, and SugarCube
    `<<linkreplace>>` beats aren't in the DOM until clicked — so it measured **beat 0** and called it the
    scene. Retired explicitly in the file, with its root cause, so it can't come back.
  - **The real invariant is PER-BEAT and FLAT: ~35–40 words/beat across every tier** (1 beat → 15w · 2–4 → 27
    · 5–9 → 35 · 10+ → 38). **Tier scales BEAT COUNT, not prose density** — RTS's biggest scene is 24 beats of
    ~25 words. The old doctrine implied Tier-3 = thicker prose, which is exactly how we shipped 3-beat
    capstones of 90-word paragraphs. New §5 (tiers = beat counts) + §6 (canvas budget = beats × 35–40).
    Deliberately did **NOT** restore the recovered prompts_v2 caps (Lane 1 ≤200 / L2 ≤100 / L3 ≤150 per
    canvas): measured against RTS, the **Lane-2 cap is 2.6× tighter than RTS's own ambients** (median 270w),
    and a flat cap forces the wrong fix (compress the beat) over the right one (cut a beat).
  - **THE BIG ONE — the drift is MODE, not length.** Narration:dialogue — **RTS 0.73 : 1** (more dialogue than
    narration, and its *deepest* scenes are its most spoken: `PriestVisit`, 19 beats → 0.40:1) vs **every game
    we have ever shipped**: last_call 5.77 · the_inheritance 5.79 · vesper 7.25 · late_shifts 15.04 ·
    mothers_place 19.34. Our block *lengths* were roughly right all along; **we narrate where RTS speaks.**
    Rule 4 already said "dialogue does the character work" — with no number and no audit, so it had no teeth.
    It now carries a **gate** (≤1.5:1 on any scene with a present NPC; **>3:1 = FAIL**; ≤2:1 whole-game) and a
    runnable check. Root cause of the toothlessness found too: `rts-flat-prose.md` said "the full mode rule is
    in `lanes.md`" while `lanes.md:336` said "the full rule is in `rts-flat-prose.md`" — a **citation cycle
    with no owner.** Broken: `rts-flat-prose.md` §2 now OWNS all three axes; `lanes.md` "Voice register" is
    demoted to the lane → value lookup.
  - **Rule 3 restated: ban the ROOM, require the BODY.** "Zero environmental sensory detail" read as "no
    sensory anything," but RTS writes body sensation constantly (*"Heat flares in your belly"* is verbatim
    RTS; it uses the body to encode **reluctance** as readily as arousal) and paints a room almost never — 25
    environmental lines in 364 passages, and the room-painting ones are all **location cards** on a fixed
    ~25-word formula. Authors were hitting a rule that contradicted the corpus and quietly ignoring the file.
    The room now has exactly one home (the location card → `location-design.md`); one exception survives
    inside a body: a sensory detail that is a **gate signal** (the shower running = someone's in there).
  - **NEW §1 (the measured shape of RTS)** — every number now cited, none asserted. **NEW §7** — three runnable
    audits (declared-person grep · per-beat density grep · the narration:dialogue script). **NEW §8** — the
    skill had **zero verbatim RTS**; every ✓ example was an invented Frank/Maya line, i.e. we asked authors to
    hit a voice we never showed them. Now pasted: `BedroomStudy` (Tier-1, 7 words) · `PeepBrotherSex` (Tier-2
    cascade at 41 w/beat — doubles as Rule 3's body exhibit AND Rule 4's *exemption* exhibit, since she's alone
    behind a door) · **`MeetEmma`** (a whole NPC intro in 68 words: 15 narrated, 53 spoken — the Rule-4
    hammer) · `PriestVisit` (Tier-3 = more beats AND more dialogue) · `Church` (the location card) · plus the
    BEFORE/AFTER drift rewrites and the Marge case study recovered from the deprecated corpus.
  - Rule numbers **1–8 kept** deliberately — `beat-authoring.md` and `lanes.md` cite them by number.
- **Person is now a DECLARED, per-game choice (`register.person`) — was hardcoded to second.** LO's call.
  Rule 1 read *"Second-person voice. 'You,' not 'she.'"* while `vesper` shipped **third** (568 third-person
  narration blocks) — so the doctrine branded a deliberate game a permanent violation, and nothing checked
  consistency either way. Worse, the grep turned up **`late_shifts` mixing both persons in one file** — it is
  a *third*-person game (362 of 398 paragraphs narrate "she") that leaks second person (*"He looks up when
  **you** come in from the floor"*, same `5_scenes.toml`). Nobody chose that; nobody noticed; no build gate
  can see it. Person is now declared once at the seed,
  immutable after, and the self-audit greps against the **declared** value — so it *protects* each game's
  choice instead of attacking it. Density and mode stay **non-optional** (making person a choice must not
  launder the literary drift).
  - wired it in: `SKILL.md` register-authority block ("two axes" → **three**, with the numbers);
    `references/lanes.md` "Voice register" (new person bullet + demoted to lane→value lookup + the mode gate);
    `references/beat-authoring.md:135` ("two axes" → three) **and its per-beat self-audit** (four new checks —
    declared person · per-beat density · tier=beat-count · body-yes-room-no; Rule-4 bullet given the ratio +
    the §7 command); `references/step-0-1-seed.md` (**new seed item 5 — "Voice — the person"**, Mode A, with
    the explicit **"person is NOT POV"** note: POV in this skill has always meant protagonist *gender*, and
    the collision would have caused exactly the confusion it now prevents); `references/ledger-schema.md`
    (new top-level `register.person`, `schema_version` stays **2** — additive; plus a **back-compat rule**: a
    ledger with no `register` must **detect** the person by running §7 check 1, never assume `second`).
    Grep-verified every new pointer resolves.
  - stale figure swept: `~30-word caption` → `~35–40 words per beat` in `references/kink-ceilings.md`,
    `references/media.md`, `references/lanes.md`, `references/step-5-blueprint.md`,
    `references/step-6-feedback.md` (grep-verified zero residual `30-word` refs).
  - **ENGINE — `[settings] narration_person` SHIPPED (same session).** The engine hardcoded
    `<strong>You:</strong>` on every player dialog line and `💭 You are thinking:` on every player thought
    bubble, so `vesper`'s shipped build rendered "**You:**" ×10 and "💭 You are thinking:" ×3 **directly
    under third-person prose** — the mismatch was live, not hypothetical. New `[settings] narration_person`
    (`second` default / `first` / `third`), enum-validated in `template_import.validate()` so a typo
    **fails the build** rather than silently falling back to "You:"; read in `v2.generate()`; consumed by a
    new `v2._get_player_speech_labels()` at the two player-speaker render sites. Third person emits the
    **runtime macro** `<<print $player.name>>` (not the build-time name) so a renamed customizable PC still
    resolves — the NPC branch of the same renderer already did this. Gotcha found while building: the
    portrait **`alt` text is HTML-escaped downstream**, so the macro can't go there — the helper returns a
    separate plain-text `alt_label`. Documented in `engine-reference.md` §7.
    **Deliberately OUT of scope:** the ~40 UI-chrome strings (`Your money`, `Your Traits`, `Your Activities`,
    `(you have 6)`, `Your Boldness ≥ 40`) and the rent/clothing/travel default messages (already
    author-overridable). Chrome reads fine in any person; the *scene body* is what contradicted itself.
    **Verified:** vesper rebuilt → `You:` ×0, name-labelled player lines ×10, thought bubbles ×3, portrait
    alt = "Wren". `late_shifts` rebuilt with **no** setting → `You:` ×6 still renders (default intact, no
    regression). Enum test: `"secnod"` / `"You"` fail the build; absent key → `"second"`. Display strings
    only — no ids/flags/traits/title touched, so **save-safe**.

## 2026-07-09
- **`references/step-3-casting.md` — added a "Still-point cast floor" bullet to the casting self-check.** Root
  cause: Vesper (a still-point / owned-weapon protagonist) shipped thin with only 2 developed NPCs and drew a
  mopoga "lacks content / grind not content" verdict. §2F (the day-breadth audit) already catches this at Step 6
  and names Vesper as its example (added earlier, `#10`) — but *casting* didn't proactively floor cast SIZE for
  still-point games, where the player's feeder economy is dormant so ALL day-breadth must come from the NPCs and
  the cast size IS the content budget. The new bullet catches a too-thin still-point cast at Step 3 (casting)
  rather than only at the Step-6 review. Doc-only; ties to `content-framework.md` §1B/§2F. This **closes the
  "author-game skill defect" track** opened during the Vesper Underworld-Hunt work: the primary §2F day-breadth
  patch was already in and proved itself this session by failing the hunt blueprint at the Step-6 review (which is
  how the corridor was caught before building); LO's call was to add this one early-catch corollary and close the
  track. (LO chose to leave the secondary "time-to-first-payoff cadence" floor unwritten — §2F suffices.)
- **`references/player-portrait.md` §1 — portrait now mounts BELOW the time display, not top-most (ENGINE, `v2.py:14853`).**
  LO's call: the time/clock stays at the very top of the sidebar; the portrait sits just under it, above the HUD/stat
  items. Moved the `{portrait_line}` fragment from the first StoryCaption line to just after `<<timeDisplay>>` in both
  the dev and non-dev blocks. Doc + Vesper design-book/config comments updated from "top-most" to "below the time
  display". Live-confirmed (DOM order + screenshot).
- **`references/player-portrait.md` §2 — undress model changed (ENGINE change to `getUndressLevel`, `v2.py:1454`).**
  Old logic keyed topless/bottomless off the OUTER slots only (`top||dress`, `bottom||dress`) and lumped
  `bra||underwear` into one `hasUnder` flag — so a game with only a one-piece dress (+ bra/briefs) could reach
  only `underwear` and `naked`, never topless/bottomless (dogfooded on Vesper; LO wanted bra-off = topless).
  New model asks *is this body-area bare?* per area: **bra covers the top, briefs (`underwear` slot) cover the
  bottom**; `topCovered=top||dress||bra`, `bottomCovered=bottom||dress||underwear`; topless = top bare (not even
  a bra), bottomless = bottom bare (not even briefs), underwear = both covered by only bra/briefs, naked = both
  bare. Verified `getUndressLevel` has ONE consumer (the portrait resolver) — no game gates on it, so the
  semantic change is contained. Live-proven on Vesper: all 4 undress stills now reachable from a dress+bra+briefs
  wardrobe (unequip dress→underwear, +bra→topless, +briefs→bottomless, all→naked), faithful wardrobe-UI test +
  10-state matrix green. Also updated the doc's "fires only if the image key is declared" note.

## 2026-07-06
- **`references/player-portrait.md` §1 — added the render-framing note (portrait-composition author
  implication).** First real-game application (Vesper) surfaced two Phase-A ENGINE gaps, both fixed in `v2.py`
  (engine, not skill): (1) the media prefix defaulted to `./media` while every other generator path uses
  `./videos` → portrait 404'd (fixed `v2.py:1135`); (2) the `<<playerPortrait>>` widget shipped with **no CSS**,
  so the `<img>` rendered at natural size and overflowed the ~232px sidebar (background edge, not face) → added
  a `.sidebar-player-portrait img` rule (3:4 `object-fit:cover`, `object-position:50% 18%`). Skill doc updated
  so authors source portrait-composition art (subject centred, face upper-third). Verified: rebuilt Vesper +
  headless live test (img 232×309, face reads, resolver green, undress falls through to default).
- **NEW `references/player-portrait.md` + wiring — state-reactive player portrait (ENGINE CHANGE, not
  doctrine-only).** The RTS discrete-swap portrait is now a real OPT-IN engine feature: a top-level
  `[player_portrait]` block emits a TOP-MOST sidebar `<img>` that swaps by undress / dominant-outfit-`type` /
  corruption-LEVEL / pregnancy-suffix, resolved by `setup.getPlayerPortrait()`. The skill had ZERO doctrine
  for it. `player-portrait.md` owns it: the four axes, the resolver priority + dominant-slot keying, the
  `[player_portrait]` TOML, the traps, the budget, the enabling checklist — every claim cited `file:line`
  against the CURRENT `v2.py`/`template_import.py` (implemented + verified this session).
  - wired it in (`engine-reference.md` §7 new home-map row + `[player_portrait]` TOML example;
    `systems.md` new dispatch row + intro count five→six/four→five + Seed yes/no bullet; `SKILL.md`
    knowledge-base full-reference list + Engine-ground-truth item 10; `step-0-1-seed.md` item 4,
    `step-2-toplevel.md` §8, `step-5-blueprint.md` §5F, `beat-authoring.md` system-homes + optional-system
    trap; `customization.md` + `hud.md` cross-refs) — why: a reference is dead unless the steps cite it where
    the author works; grep-verified every new pointer resolves to `player-portrait.md`.
  - **Engine (not this skill, logged for the trail):** `v2.py` = `getUndressLevel`/`getPlayerPortrait`
    helpers, unconditional `setup.player_portrait` emit, `<<playerPortrait>>` widget mounted first in
    StoryCaption, Preg-variant asset tracking; `template_import.py` = `TemplatePlayerPortrait` dataclass +
    `[player_portrait]` parse/validate/serialize (key mirrors `[bank]`). Verified: **live-play 9/9** in the
    built SugarCube game (undress/outfit/corruption/pregnancy/dress-exclusivity + DOM render) + a
    no-`[player_portrait]` game builds byte-identical (feature off). Signature trap taught: `corruption.value`
    is a LEVEL 0–4, not raw points (`value = 30` never fires).
- **player_portrait ↔ clothing sync-drift guard** (follow-up) — a new clothing `type` with no matching
  portrait outfit rule silently showed `default_image` (drift as the wardrobe grows). Closed both ways:
  doctrine (`player-portrait.md` §4 "keep `worn_type` coverage in sync" rule + §6 checklist reminder;
  `clothing.md` §6 cross-warning at the `type`-tag site) + a build-time **WARNING** in `template_import.py`
  (clothing type with no portrait rule → warn; a rule whose `worn_type` no clothing carries → dead-rule
  warn). Verified: covered type = no warning; an uncovered `school` type = the warning fires.

## 2026-07-04
- **Vesper-history gap sweep — 6 doctrine follow-ups (batch 8).** An exhaustive workflow sweep (`wf_84dd0761`:
  231 raw candidate lessons mined across the 76-entry decisions_log / design_book / iteration-log / 10k-line
  transcript, deduped, adversarially verified) confirmed the just-closed backlog covered the vast majority; **6
  survived as genuinely-missed.** All doctrine-only, zero engine change (each composes primitives the skill
  already documents):
  - **Cascade beat-0 contract** (`engine-reference.md` + `beat-authoring.md` drift-check note) — beat[0] renders
    into the node lead and its `advance_text` is silently ignored; visible clicks = beats−1; a beat-count
    "dropped first beat" is the expected merge, not a bug (the Vesper turn-23 false-alarm). Kills a false-alarm
    class.
  - **Distinct-violation axis** (`trait-design.md` static-owner row) — differentiate stacked use-scenes by WHAT
    each violates (attention/downtime/sanctuary/status), not only pose/diction. Follows on #15.
  - **Rarity is the punch + thin-on-purpose** (`rts-flat-prose.md` + `lanes.md`; `content-framework.md §2F` +
    `step-6-feedback.md`) — a scarce beat escalates by WEIGHT not FREQUENCY (the rising-frequency curve is for
    repeatable ambients only); a *declared*-lean day is thin-on-purpose (say so, like the fail-state / systems
    declarations), not an auto-fatten gap. **Corrects the #10 day-breadth audit.**
  - **Floor-not-block refill path** (`location-design.md §5` + `§4 Case C` + `toml-gotchas.md`) — a costed move
    that's the ONLY route to its own refill must floor the cost (deduct + clamp), not gate it; a blocking toll
    strands the player. Kills a softlock class + removes a travel-friction contradiction.
  - **No real-time timer** (`engine-reference.md`) — time is click-driven minutes only; a "lasts N minutes"
    fiction is canvas-routed (`targetType="node"`), never a live countdown.
  - **Reverse ledger hygiene** (`beat-authoring.md` resume + `ledger-schema.md`) — on resume, also prune orphan
    flags, reconcile stale deferred notes, and advance a frozen `_active_beat`.
  Dropped a phantom `content-framework §G` cross-ref the verify agent mis-cited (that section doesn't exist).
- **#15 + #16 the "who climbs?" axis (static-owner NPC + still-point player)** — the skill taught exactly ONE
  progression model: the player climbs a corruption ladder + each NPC climbs their own odometer on top. The
  arc-shape table (`trait-design.md:35-41`) had 5 rows, ALL climbs — no row for a static/already-at-ceiling owner
  (Vesper's Mercer, hand-rolled as "the exemption" / "the sanctioned exception to the double-lock") — and
  `step-2-toplevel.md` + `rts-design-philosophy.md` baked in a player-corruption spine as the master "lewd door",
  with no room for a still-point player (Vesper's honeypot: player is the constant, global `corruption`
  legitimately DEAD, both axes on the NPC — `relation` = ACCESS + `corruption` = SEDUCTION, the "double-lock
  variant"). Both are GENERAL, field-recognized shapes (`nonlinear_rpg_skill_research`'s #1 gap "no
  player-identity axis"; `writing_craft` §5 fantasy-position; player-corruption is a CONVENTION not an engine
  requirement — `engine-reference.md:41-49`), so they're now named as first-class shapes on ONE **"who climbs?"**
  axis (both-climb / player-climbs-NPC-fixed / **player-fixed-NPC-climbs = still-point** / **neither-climbs =
  static owner**). Added: 2 arc-shape rows + a framing line (`trait-design.md`); the **"Who climbs?"**
  player-position question (`content-framework.md §1B`, linking §2F); the still-point **double-lock variant** +
  the "corruption may be legit-dead" exception (`step-2-toplevel.md`); a static-owner budget row (`lanes.md`);
  P1/P3 variant one-liners (`rts-design-philosophy.md`); a "not every NPC is a climb" note (`step-3-casting.md`).
  Anti-overfit: each shape lists ≥3 exemplars (spy / veteran / domme; spouse / regular / mentor) with Vesper cited
  SECOND, not as the definition. Grounded in 3 research agents (Mercer + the Renner honeypot + the field survey).
  Doctrine only, zero engine change (both compose existing machinery — an odometer initialized at ceiling / a
  flag; the per-NPC `relation`+`corruption` odometers already exist).
- **#12 location-design aliveness calibration** — `location-design.md` was created this build but its
  room-content-floor was a PURE-PLOT filter: "content" = a firing canvas, and it explicitly disqualified
  atmosphere ("a kitchen with nothing to do is not 'atmosphere,' it's a dead end"), so a zone whose only job is
  AMBIENT LIFE (street events, NPC routines you cross, a place to just *be*) had no way to earn its keep — and the
  only sizing axis was SCALE, never how ALIVE. That's how Vesper's first map shipped "utilitarian, not a living
  world" (`decisions_log[19,20]`, `iteration-log` Loop 7). Folds in the corrected principle LO logged in
  `games/vesper/location_design_note.md` (never integrated until now): (1) a **"how alive?" content-budget fork**
  at `step-2b-map-design.md` (sizing move + Mode-A + self-check) — tight mission-slice ↔ living city, set on
  purpose, leaning living for a sandbox; (2) `location-design.md` §2 reworked so **sizing is scale × aliveness**
  + **depth over breadth**; (3) §6 floor + audit reworked so **"earns its keep" counts ambient life** (a solo
  activity / street event / NPC routine) — only an **empty-dead** room (neither plot nor ambient) is cut, plus a
  new audit line that the map delivers the declared aliveness. Reconciled the surface tension with `lanes.md`
  (world ambient life ≠ padding an NPC's arc-shape cell — different axes). Grounded in 3 research agents (Vesper
  decisions_log + the best-games living-world model). Doctrine only, zero engine change; the mechanical half
  (presence-on-nav, travel-friction) already lived in §5.
- **#10 the day-breadth audit (`content-framework.md` §2F "walk a representative day")** — every content audit in
  the skill counted feeder DEPTH vertically (§2E, per corruption band) or checked each chore's fusion QUALITY;
  nothing counted HORIZONTALLY how many distinct non-grind threads a representative day offers, so a lean
  single-thread game (one NPC grind + one fused chore) passed every Step-6 row green. Worse: when a game has NO
  player-feeder economy (Vesper's inverted, already-degraded protagonist) §2E passes VACUOUSLY — exactly how
  Vesper shipped a thin day ("grind Renner + serve Mercer"): the feeder axis was zero by design
  (`decisions_log[27,28]`), Step 6 graded GO (`[33]`), and the emptiness surfaced only in play → the whole
  post-ship day-depth rescue (`[59]`–`[63]`, beats 0016–0020). Added **§2F** (the horizontal sibling to §2E):
  walk a representative mid-game day, enumerate every distinct non-grind thread against a 7-category checklist
  (solo self-care / exhibition / capability ladder / second economy / exploration / ambient walk-ins / the main
  grind), tagged feeder-vs-texture, floor ~2–3 live threads; **bites even when §2E is vacuous.** Wired:
  `step-5-blueprint.md` (seed the day-breadth count beside the feeder count), `step-6-feedback.md` (a new
  whole-game-check row — day-breadth is caught only here, not by the per-item rows), `system-patterns.md` §7 (the
  day-depth recipe now points back to §2F as its review-time trigger). Grounded in Vesper's decisions_log + the
  RTS content-design model (3 research agents). Doctrine only, zero engine change.
- **#9 grind-tuning / rung-pacing throttle menu** — a repeatable escalation rung with no throttle trivializes an
  arc (Vesper's Renner climb broke on first play; it collapsed the instant its single daily-cap flag was removed,
  `decisions_log[53]`→`[58]`). The skill taught the PRINCIPLE (`rts-design-philosophy.md` P8) and `§5E` even asked
  "what stops her maxing him out in an afternoon?" but that compiled to NO knob (no §5E bridge row), only ONE
  lever was taught (the daily-cap flag, brittleness un-noted), and threshold spacing wasn't taught at all. Added
  a **throttle menu** to `trait-design.md` "Slow-burn pacing": (1) ~×2.5 threshold spacing (don't over-space a
  thin repeated beat), (2) a diegetic time cost that closes the NPC's schedule window — the fiction-friendly cap,
  SIZED to the window (a window is not a one-shot; Vesper 180/540 ≈ 3/day vs a 3-min cost farmable ~50×), (3) a
  counted daily cap (`max_triggers_per_day` / a `_today` flag) — robust backstop but brittle alone, (4) a
  conditional per-rung energy `costs`; with the recipe "spacing **+** at least one hard throttle, never one flag
  alone." Wired: `step-5-blueprint.md` (both Gate bullets — spacing + pick-a-throttle), `rts-design-philosophy.md`
  P8 (pointer), `content-framework.md` §5E bridge-table row (cadence now compiles to a knob). Reconciled the
  contradiction at `trait-catalog.md:136` — energy is the wrong PRIMARY gate for NPC escalation, but a legitimate
  per-rung throttle-COST when the fiction supports it. Engine re-verified this session (3 agents): time-cost
  `advanceTime`/`getNpcLocation` window-close, per-choice `costs` gate-enforced by `checkCostsAffordable` (not
  clamped), `max_triggers_per_day` `canTriggerCanvas`. Doctrine only, zero engine change.
- **NEW `references/quests.md`** + wiring (backlog #11) — the Quests page was authored as per-beat plumbing, never
  designed as a surface (Step 2 designed the desire-ladder CONTENT; Step 7 authored cards one at a time; Step 5
  buried "the quest-card chain" in a 5-system bullet). No pass laid out the whole page — which cost Vesper 5
  reworks (`decisions_log[54,55,57,65,75]`). `quests.md` owns it: the two-tier layout (Story-Goals spine +
  per-NPC sections via the `npc_id` field), the two ladder shapes (flag-milestone chain vs NEW stepped trait-band
  ladder — exclusive `gte X`+`lt Y` bands, coaching in `goals[].label`), the three render frames + the
  **Frame-3-blank trap** (a met numeric top rung with no `ready_canvas`/`terminal` → blank sidebar; fix = a
  flag-goal/`ready_canvas` card), the end-of-content card (no fake objective, no dev-speak), the
  sidebar-`next` == Quests-page single-renderer fact, and the design-the-page process (the Step-5 deliverable).
  Wired: `SKILL.md` doctrine library; `step-2-toplevel.md` (desire ladder = the Story-Goals column);
  `step-5-blueprint.md` §5F.1 (elevated the buried clause into a design-the-page sub-pass); `step-6-feedback.md`
  (NEW page-as-a-surface rubric row); `beat-authoring.md` (pointer + the stepped-ladder alternative); `hud.md`
  (cross-ref). Every engine claim re-verified against the CURRENT `v2.py` this session (3 research agents):
  `renderQuestsGoalBlock:14217`, `pickQuestsCard:14065`, `checkQuestsCondition:14131` (ops gte/lte/gt/lt/eq, NO
  version key), Frame-3 blank `:14244/:14266`, sidebar parity `:15449`. Corrected 3 stale memory facts
  (`computeHintGoal` is a SEPARATE stage-hint engine `:6709`; the table is `[[quest_cards]]` not `[[quests]]`;
  there is no `title` field). Doctrine only, zero engine change; Vesper is the proof-of-concept (6-rung ladder,
  28/28 live-test).
- **#20 (beat vs node) + #26 (engine-citation sweep).**
  · **#20** `beat-authoring.md` — named the two granularities under "beat": the Step-7 beat = a PLAN unit (a story
  chunk authored/verified per turn), which explodes into many single-click NODES (the `rts-flat-prose.md` Rule-2
  sense) — "design in beats, build in nodes; 3 beats → ~23 nodes; one beat per turn ≠ one screen." Closes the
  jargon trap that helped collapse Vesper's 23-node opening to 3.
  · **#26** — swept ALL engine-code `file:line` cites after the no-DB/save-safety renumber left them stale (one
  change shifted `v2.py` +5→+294 across 67 hunks). A per-file verify-and-fix workflow (18 agents, one per file)
  grep-confirmed each cite's claimed symbol against the CURRENT engine and corrected the line: **262 corrected ·
  204 already-correct · 62 load-bearing cites given a stable function-name anchor · 0 unresolved.** Finding: only
  `v2.py` renumbered — every `template_import.py`/`package_from_toml.py` cite was grep-confirmed still exact.
  Deliberate "old corpus cited the WRONG line" examples were preserved as historical prose. Added a standing note
  to `engine-reference.md` (line-cites are approximate — grep the named symbol). Verified: 12/12 random
  spot-checks (incl. template_import "unchanged" cites) resolve to the claimed symbol in live code. Cite-accuracy
  + one doctrine note; zero engine change.
- **Batch: 7 small backlog fixes** (#22, #23, #21, #19, #18, #17, #6) — verified against the CURRENT engine
  FIRST (renumbered by the no-DB/save-safety commits), which corrected three stale premises before writing:
  · **#22** `SKILL.md` — built-in traits `(always-on)` → "(engine-privileged, NOT auto-created — declare each)";
  the false line seeded an arousal-always-on hallucination in Vesper.
  · **#23** `SKILL.md` — the one-line pipeline summary omitted map design; added `→ map` to match the dispatch table.
  · **#21** `step-2-toplevel.md` + `trait-design.md` — the dead-stat test was spatial only; added the TEMPORAL
  clause (a meter that only pays off in a later act is a dead stat *now*; lock the set at Step 2, don't add a core
  meter mid-game — LO's "if corruption isn't used now, no sense adding it later").
  · **#19** `location-design.md` — added the container **double-emit** symptom (no `default_entry` → child nav
  prints twice, `v2.py:9201-9233`) beside the existing swallow note.
  · **#18** `sex-loop.md` rule 1 + NEW `toml-gotchas.md` "Flag-chain hard-fail" section — CORRECTED the wrong
  error label (a flag set only by a triggerless canvas is NOT `NEVER SET`; it hard-fails with
  `MISSING HINT - set by '<canvas>' but no location/schedule`, `v2.py:11135`/`:11165`, `CommandError`
  `package_from_toml.py:396`) + taught the milestone-flag-in-loop case (hidden trait counter) + the exempt sources.
  · **#17** `beat-authoring.md` + `media.md` — the build examples hardcoded a now-optional `--owner-id` (no-DB is
  the default) and showed no deploy build; added a labelled PUBLISH build (drop `--dev`+`--debug`, keep
  `--video-folder`), documented that `--debug` bakes `[IMAGE MISSING]`/`[VIDEO MISSING]` TEXT into the HTML at
  build time (frozen — ships even after media is added), corrected the "--debug picks ./media" myth (real 404
  risk = missing `--video-folder`, in ANY build), and fixed `media.md`'s drifted `v2.py` cites (`:13348`/`:13313`
  → `:13606`/`:13571`).
  · **#6** `sex-loop.md` NEW "Variant: anonymous / paid service venue" — the same triggerless pose-ladder loop for
  an anonymous john: no NPC/relation gate (access+coin+hygiene), **pay ON FINISH not the entry faucet** (a bug
  Vesper's brothel fixed), upkeep drop on the exit-reset, cold register.
  Doctrine only, zero engine change. Facts verified against v2.py/package_from_toml.py this session (3 parallel
  grounding agents); grep-consistency across `references/`.
- **content-framework.md §1A + step-3-casting.md — pressure-test the premise's internal logic** (backlog #13) —
  two premise holes LO caught in Vesper, not the author: the central institution (Vance Dynamics) had a tower,
  boss, villain, and missions built on it with no defined FUNCTION ("what is this company even about?"), and the
  infiltration cover didn't hold — Renner was cast as a company insider who'd recognize what she is on sight
  (recast to a deniable outside supplier who never knew what his gear was for). §1A (the premise/hook) asked only
  the PLAYER's role, never what the institution DOES; casting had a "serves the fantasy" coherence check but no
  cover-coherence test. Added a §1A bullet ("pressure-test the premise's internal logic") carrying both questions
  + the "engine builds an incoherent premise green, catch it at the premise" why (§1 is owned by Step 2, re-run at
  Step 6 — both touches inherit it); a per-target "cover holds" line in the casting self-check (cross-ref §1A);
  and a one-line pointer from the `system-patterns.md` disguise recipe. Doctrine only, zero engine change.
- **kink-ceilings.md — "a character truth is a writing LENS, not a content GATE"** (backlog #14) — the skill's
  explicit-content doctrine covered vocabulary crudeness (§1 deliver-don't-soft-pedal, §8 anti-patterns) but not
  the reflex LO stopped twice in Vesper's Renner round: using a characterization note ("she feels only the sex,
  never comfort") to VETO/narrow a hot beat (cheer-him-up-with-sex → "cold help only"; a "but never I care about
  you" asterisk) — "this is not a society-helpful game, we are building an adult porn game." Added a §1 subsection
  (the lens/gate split + why + the reconciliation that the DECLARED caps — vocab ceiling §2, place ceiling §5,
  tier gate §4, `lanes.md` honest empty cells — stay legitimate; the rule bans only ad-hoc keyboard-time purity
  narrowing), citing the existing precedent `trait-design.md` (throttle-keyed prose is heat-not-status); + a §8
  anti-pattern bullet ("Character-purity restraint reflex"); + a Contents pointer. Reconciled against a skill-wide
  sweep's 4 tension points so it can't be read as overriding "consummation if vocab allows" (`lanes.md`). Doctrine
  only, zero engine change.
- **NEW `references/system-patterns.md`** + wiring — reframes backlog item #1 (the "systems invented after the
  game was called done" root cause). Root problem: the skill's only "systems" moment was `step-2-toplevel.md §8`,
  which declared **engine toggles only** and implied systems are decided up front — but ~half of Vesper's systems
  (disguise, capability/skill track, the underworld coin economy, weapon reload, loadout, day-depth) legitimately
  **emerged from play** and then got jammed in raw as Step-7 beats, skipping the design passes, after the ledger
  had effectively said "done." Fix is NOT "decide earlier" (that fights how sandbox design works); it's (a) a
  reach-for-it **recipe menu** of the common authored subsystems, framed explicitly as *not* a seed-time
  checklist, and (b) a first-class **mid-stream fold-in loop** so a discovered system still gets its quick
  design→place→build→fold passes instead of duct-tape, with **"playable ≠ done"** made doctrine. `system-patterns.md`
  carries 7 starter recipes (disguise/cover · capability · crawl · second economy · reload upkeep · loadout ·
  day-depth), each with when-you-reach-for-it / the shape / the trap, cross-linked to the owning references and
  the #8 clamp rule; engine facts kept to stable anchors (no brittle line cites, since the engine was just
  renumbered by `8446b3d`). Wiring: `run-mode.md` NEW section "Systems grow through iteration — playable ≠ done"
  (the 4-pass loop); `SKILL.md` operating rule "Structure is stable-and-extensible" extended from
  location/NPC/flag to whole systems + a doctrine-library bullet; `step-2-toplevel.md §8` reframed to declare
  engine toggles now but let authored subsystems emerge; `systems.md` gains a pointer distinguishing ENGINE
  toggles from these AUTHORED patterns. Doctrine only, zero engine change. Verified: grep-consistency (every new
  cross-ref resolves); the menu is deliberately distinct from `systems.md`. Also updates the root
  `AUTHOR_GAME_SKILL_BACKLOG.md` (#1 reframed; #2–#7 now have starter recipes, deepen on demand).

## 2026-07-03
- **NEW `references/save-safety.md`** + wiring in `SKILL.md` (Engine-ground-truth item 9, a Knowledge-base
  index bullet, and a reinforcement on the "Structure is stable-and-extensible" operating rule) — the skill
  had **no** release/save-safety doctrine, so after the engine shipped slug passage names + constant slug ids
  + a save-migration seam, nothing told an author which changes still break a *returning player's* save on an
  update. Documents the four join keys that must stay fixed on a shipped game (immutable slugs/ids · never
  rename/repurpose a live flag or trait key · don't rescale a stat range or move tier/stage thresholds · don't
  change the game title) + a pre-update grep-guard checklist + what IS safe (add content, insert/reorder/delete
  beats, rename display names). Verified: every `file:line` cite grepped against the shipped
  `games/vesper/output/index.html` + `v2.py` — slug passage naming (`_node_passage_name` :11246 /
  `_location_passage_name` :11259), `$npcs` slug keying + `npc_slug_map` identity, `Config.saves.id`/`version`
  (:2812), `setup.stateDefaults`/`backfillStateDefaults` (:14549), `npc.id = <slug>` (`game_graph.py:144`).
- **Corrected now-stale engine facts** the same fixes obsoleted (the skill must not teach false engine facts):
  `references/dev-console-jump.md` — node passages are `Node_<nodeSlug>` not the 1-based `Node_<n>`; `$npcs` is
  keyed by slug not `npcs[uuid]`; retired the "NPC uuids regenerate every build → stale-save" framing (the bug
  is fixed); fixed the grep guard (`[0-9]+`→`[a-z_0-9]+`) and the Renner worked example
  (`Node_4`→`Node_base_doggy_r`). `SKILL.md` — the dev-console bullet's `Canvas_<id>_Node_<n>`→`Node_<nodeSlug>`.
  `references/customization.md` — `$npcs[uuid]`→`$npcs[slug]`; `npc_slug_map` `slug→uuid`→identity. Doctrine +
  fact-correction only, zero engine change (the engine work shipped in commits 8446b3d + 1d9ce93).

## 2026-07-02
- **clamp-or-vanish lint** (backlog item #8 from the Vesper→skill analysis) — hardened the banded-stat clamp
  doctrine across 5 files after an unclamped banded body-stat shipped a **blank HUD twice** in Vesper
  (`decisions_log[64]` Charge went negative; `[66]` Condition/hygiene over-capped AND went negative — `[66]`
  records it as the SECOND time and asks for a lint that was never actioned). Root cause: effects run
  `eff.clamp || false` (unbounded by default), and a banded sidebar card only draws when the value lands inside a
  band (`trait_words` closed-match `v2.py:15252`; `trait_status_text` open-on-omit `v2.py:15183`) — out of range
  it renders **nothing**, reading as a *missing* HUD element, not a wrong number, so a quick playtest sails past
  it. Changes: (1) `references/trait-catalog.md` §4 — replaced the advisory "clamp recommended on a restore" with
  the hard two-part rule (bound the value on body-need/resource stats · cover the range for unbounded odometers),
  cross-citing the `engine-reference.md` Clamp trap; fixed the bare-`+N` energy-restore example to `cap = 100`;
  turned the §5 "renders nothing when no band matches" cell into an active pointer to the rule. (2)
  `references/beat-authoring.md` — added a hard clamp row to the Step-7 resource self-audit. (3)
  `references/step-6-feedback.md` — added the review-time "no unclamped banded stat" lint (the hard lint begged
  for twice). (4) `references/toml-gotchas.md` — capped the bare-`+N` Sleep/Shower restore example so it stops
  contradicting the rule. (5) `references/engine-reference.md` — one-clause pointer at the corruption Clamp-trap
  line so mechanism + application agree. Reconciles the "unbounded is correct for corruption" carve-out
  (completes it — the value may climb, but the top band must still cover it) rather than contradicting it; `money`
  stays exempt (unbanded number, never vanishes). Verified: engine facts read from `v2.py` this session;
  grep-consistency across `references/` (no surviving "recommended on a restore" or bare-`+N` counter-example);
  the two load-bearing engine cites re-checked against the current `v2.py` after HEAD moved to `8446b3d`
  (`trait_words` closed-match `:15252`, `trait_status_text` open-bound `:15183`). Doctrine only, zero engine change.

## 2026-07-01
- NEW `references/dev-console-jump.md` + one index line in `SKILL.md` — LO asked to save the browser-console
  "jump/arm" testing technique (fast-forward a built game to a gated state via `State.variables`) as a
  reference, **on-request only**. Documents: serve over `python3 -m http.server 8080` (not `file://`) +
  console context = `top` (not an extension); the `SugarCube` API handle (this build hides bare
  `State`/`Engine`/`setup` globals); the code-verified write paths (`player.core_traits.<k>`,
  `flags.<k>`, `setup.resolveNpcId(slug)`→`npcs[uuid].core_traits`, `Object.values(player.equipped)` for
  equip); `Canvas_<authoredId>_Node_<n>` passage naming (authored ids, stable — NPC uuids are not); ARM vs
  FIRE + the "leave/re-enter to re-eval" caveat; Renner-drain worked example. All paths verified by grepping
  the live `games/vesper/output/index.html` (evaluator branches, passage-name stems all authored-id, no
  uuid). Dev convenience, explicitly gated off the authoring flow.
## 2026-06-23
- NEW `references/onboarding.md` + `references/npc-intro.md` — closed two recurring doctrine gaps an
  adversarially-verified audit found behind LO's "set the player up properly / a new character can't start
  randomly". The skill *declared* the opening must "teach with no tutorial" (step-2 §8, content-framework §1E)
  but never taught the **method**, and treated `npc_intro` as hub-plumbing with no **dramatic** first-encounter
  craft. `onboarding.md` owns the linear-funnel machine-teaching method (surface each live system once in a
  fiction beat; sidebar at value-zero; named next-action on frame one; the three why-locked surfaces; the
  win/fail contract) + a HARD-gate Step-6 rubric. `npc-intro.md` owns the first-encounter craft (pretext +
  name-on-page + hook-as-want → fire once → open the hub; the 7-step Renner template
  `vesper/5_scenes.toml:315-346`; the Hank cold-spawn anti-pattern `late_shifts/5_scenes.toml:14-35`) on top of
  the intact mechanical on-ramp doctrine. LO's locked calls: linear-funnel is the ONLY opening shape; files
  kept split (different lifecycles — onboarding fires once/game, npc-intro every NPC); rubric is a hard gate on
  load-bearing rows. Every engine knob code-verified this session (starting_canvas hard-error
  `template_import.py:6104-6118`; auto-fire `v2.py:4025`; locked_text/cost/blocked_message
  `v2.py:11762/11756/4329`; `start_after_flag`; advanceDay-only-past-24h `v2.py:4958-4999`; quest
  goals/ready_canvas/tip; sidebar bands; `speaker=unknown` `v2.py:13590`; getNpcsWithSchedules leak
  `v2.py:3132`; conditions fail-open `v2.py:3398`; is_container swallow `template_import.py:3506`) — n/a
  (doctrine; dogfooded read-only by running the rubric against Vesper's opening → flags its known machine gaps)
- wired both files in (`SKILL.md` doctrine-library bullets; `step-2-toplevel.md` §8 method pointer;
  `step-5-blueprint.md` Pass-4 opening bullet; `content-framework.md` §1E machine clause + §3B on-ramp pointer;
  `step-6-feedback.md` two self-check rubric rows; `hud.md` §1 persistent-tutorial note; `lanes.md` `npc_intro`
  beat-type expanded from plumbing to designed-encounter; `beat-authoring.md` cold-start firewall + cold-spawn
  ban; `step-3-casting.md` hook→first-encounter forward wire) — why: a reference is dead unless the steps cite
  it where the author works — grep-verified the pointers resolve to the new files

## 2026-06-22
- NEW `references/media.md` — the skill had almost NO media doctrine (its whole footprint was a 1-line block-
  vocab mention + 1 location field in `engine-reference.md`), so authors hand-rolled media and missed the
  acquisition layer: Vesper (and Last Call, Late Shifts) shipped image refs with no `search_queries`, no video,
  silently-skipped media. media.md owns it: the 3 block types (`image`/`video`/`clip`) from engine truth, the
  extension-agnostic resolve law, the silent-skip-when-missing model, the `search_queries` craft (grafted from
  `prompts/toml_generation_prompt_v4.txt:905-1001`), the tier→format contract, the text-media-text rhythm
  (`prompts/media_writing_guide.md:657-705`), folder/naming, the `find-media` hand-off — with 4 corpus lies
  explicitly corrected (clip-uses-`file`; extension-is-authoritative; "t5+ must be webm or it won't render";
  inline `[image:]` syntax). Every engine claim re-verified against `v2.py`/`template_import.py` this session —
  n/a (doctrine; dogfooded by rebuilding Vesper with `search_queries` → Missing-Media page populated)
- wired media.md in (`SKILL.md` doctrine-library bullet; `engine-reference.md` §2.5 clip `{props.file}`→
  `{props.clipId}` fix + media.md pointer, and the `image_search_queries` row's key-name-trap note;
  `beat-authoring.md` Step-7 media instruction; `step-5-blueprint.md` Pass-2 **Media** placement bullet;
  `rts-flat-prose.md` Rule 8 — flagged the `[image:]` shorthand as non-engine, point to real TOML) — why: a
  reference is dead unless the steps cite it where the author works — grep-verified pointers resolve to media.md

## 2026-06-18
- added skill-ledger pointer note in the State section (`SKILL.md`) — distinguishes the game ledger
  (`authoring_state.json`) from this skill's own ledger (`CHANGELOG.md`); part of introducing the
  per-skill CHANGELOG convention (documented in `CLAUDE.md` → "Skill ledger") — n/a (docs only)
