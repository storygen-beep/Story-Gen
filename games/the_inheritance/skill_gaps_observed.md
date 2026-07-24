# Skill gaps observed while re-authoring The Inheritance

> **Purpose.** Candidate fixes to the `author-game` skill, found by rebuilding this game against the archived
> v1. Recorded HERE (in the game folder) rather than patched into the skill immediately — per LO: **prove the
> fix in this game first, then promote to the skill.** Each entry names the defect, the evidence, the proposed
> skill edit, and a promotion gate ("we'll know this fix is right when ___").
>
> The test each must pass before it earns a skill edit (`CLAUDE.md`): *"Would a correct author-game skill have
> prevented this?"* If yes → it's a skill/corpus fix, not a one-off.

---

## GAP 1 — Casting can mis-shape an APEX target as an "antagonist," and every downstream check passes

**Status:** OPEN — proposed fix applied to *this game*; promote to skill after the build proves it.

**The defect.** `step-3-casting.md` gives an arc-shape taxonomy + a per-shape budget matrix (`lanes.md`), but
it never warns that **the game's climactic conquest can be cast into the `antagonist/witness` shape** — whose
whole definition is "an obstacle who *never becomes a target*" (budget 6–10). Once mis-shaped, the error is
**invisible to every later step**: Step 4 writes a story that fits the small shape, Step 5 budgets to it, the
build is green, the flag-chains validate, and the Step-6 review grades each arc *against its own declared
budget* — so an apex built to an antagonist's budget passes.

**The evidence (measured against `archive/the_inheritance_v1/`).**
- v1 cast **Margaret** — explicitly *"the final boss… taking her = the charge-ceiling payoff"* — as
  `antagonist (broken, NOT seduced)`, budget **6–10**, and built **8 canvases.** *She was inside budget.* The
  author did nothing wrong against the matrix.
- The tell was upstream and in the *story*: her v1 arc was `cold war → cornering → breaking → slavery` —
  **four big nights and some sparring, with no rungs.** The shape matched the writing; the writing was the
  bug. An apex needs a climb, and "antagonist, 6–10" cannot hold one.
- Same error, smaller, on **Grayson** (core target cast antagonist; built 14).
- Net effect at ship: the two highest-charge conquests in a 76-canvas game had the thinnest arcs in it.

**Why it's a skill gap, not a one-off.** Nothing in the pipeline asks *"is this the last/biggest thing in the
game? then it cannot be an antagonist-shaped 6–10."* The casting self-check lists structural coverage,
hooks, variety, the machine — but not **"does the apex's shape carry a climb?"** A different author on a
different game makes the identical mistake and every gate still says yes.

**Proposed skill edit** (to `step-3-casting.md`, casting self-check — hold until promotion):
> **Apex-shape floor.** Identify the game's **apex** — the highest-charge conquest, the frontier trigger, the
> last thing taken. It **cannot** be `antagonist/witness` shaped: that shape is for an obstacle who never
> becomes a target (6–10, no climb). If the apex is a *conquest*, it is a **dense climbing shape**
> (family/ambient or the arc-shape whose budget carries a real ladder), full stop — even when its register is
> cold/antagonistic. "Antagonist register" ≠ "antagonist arc-shape." A conquest you *destroy* still needs the
> rungs that make the destruction land.

Possibly also a line in `trait-design.md`'s arc-shape table: *antagonist/witness = the obstacle who is
never taken; if he/she is eventually taken, that's a climbing shape wearing an antagonist's voice.*

**How THIS game applies the fix.** Margaret + Grayson re-shaped to family/ambient dense (25–35). Margaret got
*new story* to fill it — the war fought with what she sees (catch → bank → spend → the board turns), because
re-shaping without new story would just be padding.

**PROMOTION GATE — promote to the skill when:** the built Inheritance has a Margaret arc that reads as a real
climb (the war has rungs the player feels, not four set-pieces), and the narration:dialogue + lane-mix audits
on her arc come out healthy. If her rebuilt arc lands, the rule earned its place. If it doesn't, the rule was
wrong and we learned that here instead of in the skill.

---

## GAP 2 — Step 4's own ordering is enforced, but nothing flags a game that SKIPPED the player/world/reactivity passes

**Status:** OPEN — noted; lower priority (the current pipeline already prevents it going forward).

**The defect.** v1's `design_book.md` (rev 72) had **NPC briefs and nothing else** — no Step-4 player thread,
no world pass, no reactivity pass. The current `step-4-deep-design.md` enforces the four-pass order via the
ledger's `deep_design` block, so a *new* game can't repeat it. But there is no **audit** that catches an
*imported/legacy* book missing the passes — and that omission is the documented root cause of both the starved
player-corruption track and the dead rooms (supply never designed before demand).

**Why it might still be a gap.** The re-author path (continue/expand an existing game) can inherit a
pre-four-pass book and never notice the passes are absent, because the ledger just says `authoring` and the
dispatch resumes there. A one-line resume-check ("does the book have a player thread + world + reactivity
section? if not, they were never designed") would catch it.

**PROMOTION GATE:** only worth a skill edit if we hit it again on another legacy game. For now the fresh
pipeline handles it; recorded so we don't forget the root cause.

---

## GAP 3 — (candidate) "dense arc" is budgeted but never *defined* as needing ambient scenes

**Status:** WATCH — may resolve on its own once this game's dense arcs are built.

**The observation.** v1's Audrey was a "family/ambient (dense)" arc with **19 canvases and zero ambient
scenes** — 19 things the player *did to her*, and not one moment of her simply existing in the house. The
budget was nearly met by *count*; the *shape* wasn't, because "dense" was read as "many escalation rungs"
rather than "a person who lives here." `lanes.md` implies Lane 3 is ~47% of a family/ambient arc, but the
"her ambient life" idea isn't a named requirement in the Step-4 brief template.

**Possible edit** (if it recurs): add **§ "her ambient life"** to the Step-4 story-brief template — *name the
moments where this NPC simply exists in the world when the player isn't working them; a dense arc with zero of
these is a menu, not a person.*

**PROMOTION GATE:** if building this game's four dense arcs, I find myself repeatedly *inventing* the ambient
layer because the template didn't ask for it → promote. If the briefs I already wrote (each has a §7 "ambient
life") carry through cleanly → the fix is just "make §7 a standard section," a smaller edit.

---

## GAP 4 — Step-5 Pass-4's machine self-verify can ASSERT "reachable" for a flag that has no setter

**Status:** ✅ PROMOTED 2026-07-25 → `step-5-blueprint.md` Pass 4 (the mechanical READS ⊆ SETS trace, plus the location-side `entry_conditions` blind spot). Originally: surfaced by the Step-6 review on THIS game (the one major gap it found).

**The defect.** Step-5 Pass 4 says "every gate has a reachable setter (verified)" and the author writes that
line — but nothing forces the verification to be *mechanical*. On this game, Pass 4 certified `hotel_in_hand`
"verified reachable" while the flag was **READ by three arcs and SET by zero canvases** (it was gestured at in
prose — "opens taking the purse" — but no handle produced it). A self-assessed "verified" is exactly as
reliable as the author's attention, which is what the pipeline is supposed to backstop.

**Why it's a skill gap.** The Step-6 review caught it, but only because an adversarial agent traced it — the
Step-5 self-check that was *supposed* to catch it rubber-stamped it. The fix is to make Pass-4's DAG-verify a
**mechanical trace**, not a prose claim: enumerate every flag READ in any `conditions`/gate, and confirm each
appears in some canvas's SETS. This is a grep-able check (`READS` set minus `SETS` set must be empty) that
belongs in the step, run before the phase advances.

**Proposed skill edit** (`step-5-blueprint.md` Pass 4): add — *"Verify the gate-graph MECHANICALLY: list every
flag read in a `conditions`/trigger/gate, list every flag in a §8 SETS, and confirm READS ⊆ SETS. A flag read
but never set is a build-time flag-chain hard-fail (or a silent soft-lock); do not write 'verified' until the
set difference is empty."*

**PROMOTION GATE:** this one is already proven (it caught a real major gap here that the prose self-check
missed). Promote when the skill patch is next opened — it is the highest-value of the five.

---

## GAP 5 — A lane mix-table can promise ambients that no scene section lists (double-counting)

**Status:** ✅ PROMOTED 2026-07-25 → `step-5-blueprint.md` Pass 2 per-NPC self-check (mix-table total must equal the enumerated sections). Originally: surfaced by the Step-6 review (a notable gap on Grayson's arc).

**The defect.** An NPC blueprint's header states a lane mix ("L1 7 · L2 4 · L3 13 = 28"), but the body has no
Lane-2 section — the 4 "ambients" were the same beats already counted inside Lane 3's 13. The budget looked
met; ~4 scenes were double-counted. The build never sees it (it's a design-book arithmetic slip), and it
directly reproduces v1's "mix table promises ambients no scene lists" failure, localized to one arc.

**Proposed skill edit** (`step-5-blueprint.md` Pass 2 self-check): add — *"Every lane named in a mix-table
total has a matching enumerated section; no beat is counted under two lanes. Sum the enumerated sections and
confirm it equals the header total."*

**PROMOTION GATE:** promote alongside GAP 4 — both are cheap Step-5 self-check additions proven by this
game's review. Together they'd have prevented 2 of the 8 gaps this review found.

---

## GAP 6 — ~~`location`-type exit that sets a flag is invisible to the flag-chain validator~~ → **`exit_block` silently DROPS unknown keys**

**Status:** ✅ PROMOTED 2026-07-25 → `toml-gotchas.md`, as a **CORRECTED** rule. ⚠️ **The original diagnosis
below was WRONG** — see the correction. The defect/fix text is kept as a record of how the wrong lesson
nearly shipped; the old "Proposed skill edit" paragraph (which stated the false mechanism as doctrine) and
its promotion gate were removed rather than promoted.

> ### ⚠️ CORRECTION (2026-07-25, verified in code before promotion)
> The validator does **not** miss location-type exits. `_build_flag_unlock_map` scans them explicitly
> (`v2.py:11138-11152`, the branch commented "Check flagEffects in config (for 'location' type exit
> blocks)"), so does the setter index (`:8363`), so does the importer (`template_import.py:2834`), and the
> flag **is** applied at runtime from a location exit (`v2.py:12568` → `:12888-12893`).
>
> **The real bug:** `exit_block` is parsed with exactly four keys — `type`, `text`, `config`, `choices`
> (`template_import.py:2045-2060`) — and there is **no unknown-key rejection**. Our TOML wrote
> `[canvases.nodes.exit_block.effects] flagEffects = [...]`, an unrecognised key, which was **silently
> discarded at import**. The flag was therefore set by nothing, and `✗ NEVER SET` was a **TRUE POSITIVE**
> wearing a confusing message — not a validator blind spot.
>
> **Correct shapes:** location-type → `[canvases.nodes.exit_block.config] flagEffects`; choices-type →
> per-choice `flagEffects`. Our fix (moving to a choices exit) worked, but **by accident** — it moved the
> flag onto a path the parser actually reads, rather than fixing the key.
>
> **Lesson worth more than the original:** the promotion gate ("proven now — it hard-failed a real build")
> proved a *symptom*, not a *mechanism*. A green/red build tells you something is wrong, never why. Verify
> the mechanism in code before promoting it, or the skill teaches a fiction that happens to work.

**The defect (AS ORIGINALLY RECORDED — superseded).** A `[canvases.nodes.exit_block]` of `type = "location"` that sets a flag via
`[canvases.nodes.exit_block.effects] flagEffects = [...]` **does not register with the flag-chain
validator** — the build hard-fails with `✗ <flag> NEVER SET - no canvas sets this flag`, even though a
properly-located canvas sets it. (Hit on `opening_done`, set by the located starting canvas, read by the
will-reading trigger.)

**The fix (as originally recorded):** set the flag on a **choice** — `type = "choices"` exit_block
with the flag on `[[canvases.nodes.exit_block.choices]] flagEffects`. `late_shifts` uses exactly this for
`first_morning_done`. A single forced "Continue"-style choice is the idiom for a one-shot that must set a
flag on the way out. *(Still a valid shape — just not for the stated reason.)*

---

## GAP 7 — the §7 check-1 declared-person grep false-positives on `yours` / `you're` / `you'll`

**Status:** ✅ PROMOTED 2026-07-25 → `rts-flat-prose.md` §7 check 1, BOTH greps switched to the `\byou` prefix (the third-person branch used the same pattern as an inclusion, so changing one alone would have desynced them), + a note that the calibration table predates the fix.

**The defect.** The §7 check-1 command excludes player-addressing lines with `grep -Eiv '\byou\b|\byour\b'`.
But `\byour\b` does NOT match `yours` (no word boundary before the `s`), nor `you're` / `you'll` / `you've`.
So a legitimate second-person paragraph that happens to use only those forms (*"…like it's **yours** now."*)
is flagged as a third-person leak — a false positive that will cost the author a manual re-read every time.

**The fix:** change the exclusion to a **prefix match**: `grep -Eiv '\byou'` (matches you / your / yours /
you're / you'll / you've). Verified: the beat_0008 false positive drops to 0 real leaks with the prefix
pattern, and it doesn't mask genuine third-person leaks (those have no `you`-stem at all).

**Proposed skill edit** (`rts-flat-prose.md` §7 check 1, both the `second` and inverted commands): replace
`\byou\b|\byour\b` with `\byou` in the exclusion grep.

**PROMOTION GATE:** proven now (false-positived a real clean paragraph). Bundle with the other §7/gotcha
fixes in the next skill pass — it's a one-character-class change that removes recurring audit noise.

---

## GAP 8 — the skill teaches WHERE forced content is allowed + THAT it recedes, but not HOW to build it as the player's floor (not the aggressor's trophy)

**Status:** OPEN — surfaced by a 4-agent research workflow while grounding Grayson's prey-phase (beat_0014). Promote after this game's prey content proves the pattern.

**The defect.** The author-game skill has strong doctrine on the *frame* of forced/no-refuse content but a hole in the *build*:
- `content-framework.md` §5B is the single OWNER of *where* forced content is allowed and *that* it must "act-scope out … so it FADES as she stops being prey" (also §2D line 103, §4C line 214). ✓
- `kink-ceilings.md` §2/§5/§8 bans **sanitizing** a forced beat into reluctant-but-into-it, and gates the EVENT on the PLACE ceiling / the WORDS on the NPC-vocab ceiling; a blank non-con ceiling doesn't ship undeclared. ✓
- `SKILL.md` #4 + the bridge table: forced = an **auto-fire capstone-shape canvas** (priority ≥ 9, `is_repeatable=false`, single Continue, no refuse/accept branch), no zero-choice primitive. ✓

But the **affirmative build doctrine** — how to author a forced beat so it reads as *the player's floor she climbs out of* rather than the aggressor's consequence-free win — lives ONLY in Vesper's game docs, not the skill:
- **Vesper's three tests** (`design_captivity_the_room.md` §1): *scene, not a bar* (no grindable forced meter); *the room has a verb* (agency, or it's "a cutscene with a timer"); *she leaves CHANGED* ("*and then something happened* is not an ending").
- **The aggressor's win must COST him** (§5): Bastien's victory is authored as the setup for his own reckoning ("he broke something Cain wanted intact"); scoped capture-and-flip so the payback is banked.
- **The persistent visible debt** (§4/§7): the forced beat freezes a `Core: Failing` meter that a *dedicated later chunk* pays back by flipping it — the recede is scheduled build-order, not implicit.
- The **pure-witness / no-agency scene chain** (`design_book.md` rev 64) is ALREADY flagged in Vesper's ledger as an unwritten skill gap ("the author-game skill has NO pure-witness / no-agency scene pattern … write it back as a `sex-loop.md` counterpart once the pattern proves out").

**Why it's a skill gap, not a one-off.** A different author building any prey/forced arc gets the WHERE and the DON'T-SANITIZE, but nothing tells them to make the beat sting-as-floor, leave a cost, and schedule the payback. The mis-authored Vesper release (she woke "sore and whole and released") is the exact failure this rule prevents — erasing the cost turns forced content into a consequence-free aggressor victory. The skill would let that ship.

**Proposed skill edit** (a new short section in `content-framework.md` or a `forced-content.md` reference, cross-linked from `kink-ceilings.md` §8): promote Vesper's three tests + "the win must cost him" + "plant a visible debt a later beat pays" + the pure-witness chain into the skill as the **build** doctrine for forced content, paired with the existing WHERE/RECEDE ownership.

**How THIS game applies it (the proof).** Grayson's prey liberties: banded descending-chance + hard-recede at `grayson_flipped` (the recede, scheduled — beat_0015), gate on the PLAYER's low-corruption band never his meter (the sting is *yours*), each beat authored player-cold-underneath (you *bank* the liberty for the payback), and the whole prey floor is structurally the setup for the servitude ladder that inverts it. If Grayson's prey→lapdog reversal lands *because* the floor stung and got paid back, the rule earned promotion.

**PROMOTION GATE:** promote when the built Grayson arc reads as "the floor that earned the payback" — the prey content stings, recedes hard at the flip, and the servitude ladder feels like *earned* inversion, not a separate thing. If it lands, this is the highest-value doctrine promotion of the whole re-author (it's the difference between forced-content-as-craft and forced-content-as-fanservice).

---

## GAP 9 — sequenced auto-fire capstones need strict stage-BAND gating, or an ungated feeder skips them

**Status:** ✅ PROMOTED 2026-07-25 → `beat-authoring.md` (new **sequenced auto-fire — band the stage** row) + `step-5-blueprint.md` Pass 4. ⚠️ Reworded on promotion: code shows auto-fire returns exactly ONE canvas per location entry (not several at once) and selects on **highest priority**, never authored stage order (`v2.py:4310-4330`) — the tiered selector deliberately does the opposite (lowest unvisited), which is the real root cause.

**The defect.** A capstone chain that auto-fires in order (cap1 → cap2 → cap3), sequenced by an odometer
(`richard_want` = `npc_richard.corruption`) + a "fires once" guard (`richard_stage lt N`), can fire **OUT OF
ORDER** if an **ungated feeder** can pump the odometer past a later capstone's threshold before the earlier
capstones fire. On this game: `ric_sit` is ungated (the on-ramp), and "The keys" gated only on
`richard_want >= 8` + `hotel_in_hand` + `richard_stage lt 3`. A player spamming `ric_sit` could reach
`richard_want 8` while still `richard_stage 0`/`corruption 0` — so **"The keys" fired FIRST**, handing over the
kingdom before "Back to life" or "The first night" ever played. The build was green; the flag-chain validator
passed (it only checks setters exist, not ORDER).

**The fix (proven here):** gate each sequenced capstone on a strict stage BAND — `stage gte N-1` **AND**
`stage lt N` — so it can only fire from the immediately-prior stage. Exactly the exclusive-range pattern the
homework tiers use (`gte min` + `lt max`). One-sided `lt N` alone ("fires once") is NOT enough when the
odometer is pumpable by an ungated feeder.

**Why it's a skill gap.** The skill teaches flag-chain integrity (setters exist) but not capstone
*sequencing* — nothing warns that "auto-fire once" + a threshold is order-safe ONLY if the threshold can't be
reached before the prior capstone. Any capstone-heavy arc with an ungated feeder (which is the *recommended*
on-ramp shape) repeats this. It is invisible to every build check; only a reachability sim catches it.

**Proposed skill edit** (`step-5-blueprint.md` Pass 4 / `beat-authoring.md`): *"Sequenced auto-fire capstones
must gate on a strict stage BAND (`stage gte prev` AND `stage lt this`), never a lone threshold + fires-once —
an ungated feeder can pump the spine odometer past a later capstone and fire it out of order. Verify order
with a reachability trace, not just 'setter exists'."*

**PROMOTION GATE:** proven now (the sim caught a real out-of-order handover). Bundle with GAP 4/GAP 8 in the
next skill pass — it's the third case where a reachability SIM caught what the static build checks can't.

---

## GAP 10 — winning-era NPC content must gate on the terminal-state flag, or it fires after the NPC is transformed

**Status:** ✅ PROMOTED 2026-07-25 → merged into the EXISTING terminal-flag doctrine rather than duplicated: `beat-authoring.md`'s "retire the standing surface" row + `step-5-blueprint.md` Pass 4 now carry the **mechanical post-flip verification** (set the terminal flag; confirm no pre-flip canvas is eligible). Verified in code: there is no engine auto-retirement — eligibility is schedule + authored conditions + repeatability only. Originally: FIXED IN GAME (recede pass, 2026-07-16), 15/15 eligible pre-breaking → 0/15 post.

**The defect.** An NPC whose STATE changes terminally (prey→lapdog at `grayson_flipped`; queen→slave at
`margaret_broken`) has "before" content — ambient presence, the catches, the war moves — that must **recede**
when the flag flips, or it keeps firing over the transformed NPC. On this game I gated Grayson's whole prey
floor on `grayson_flipped is_false` (correct — it hard-recedes at the flip). But I **forgot the same recede on
Margaret**: her 6 she-catches-you + 5 ambient-life canvases have no `margaret_broken is_false` gate, so after
"The breaking" a wordless family-slave would still "catch you working the floor, velvet-threaten, and file it"
— a direct contradiction of her terminal state. The build is green; the flag-chain validator can't see it
(it's a narrative-consistency gate, not a missing setter); only a reachability sim across the state change
surfaced it.

**Why it's a skill gap, not a one-off.** I *knew* the pattern (applied it to Grayson) and still missed it on
the apex, because there's no checklist item that says "every pre-transformation canvas gates on the terminal
flag `is_false`." It's the exact same lesson as GAP 8's recede, generalized: *content tied to an NPC's earlier
STATE must gate on the flag that ends that state.* A different author (or the same one, tired, on the biggest
arc) repeats it.

**Proposed skill edit** (`beat-authoring.md` self-audit / `step-5-blueprint.md` Pass 4): *"For any NPC with a
terminal state flip (flip/broken/etc.), EVERY canvas belonging to the pre-flip state must carry
`{flag: <terminal>, is_false}` so it recedes when the state changes. Verify with a post-flip reachability
check: set the terminal flag and confirm no pre-flip canvas is still eligible."*

**How THIS game will apply it (the fix).** Add `margaret_broken is_false` to Margaret's 6 catches + 5 ambients
(+ the 4 moves) so her whole winning-era presence recedes at the breaking, leaving only the terminal slave
loop — mirroring Grayson's clean prey→servitude recede. Scheduled for the pre-ship recede pass.

**PROMOTION GATE:** proven now (the sim caught a real post-breaking contradiction). Fourth case where a
reachability sim caught what static build checks can't (GAP 4 read-but-unset, GAP 8 recede, GAP 9 cap order).
The sim-as-gate is the single highest-value verification pattern of the re-author — that itself is worth a
skill note.

---

## GAP 11 — a location gated on a never-set flag (or a reachable room with zero canvases) ships GREEN — two engine/validator holes

**Status:** ✅ PROMOTED (skill half) 2026-07-25 → `location-design.md` §6 (two new rows: the unlock flag needs a real setter; every room with a declared job needs a LOCATED canvas — `grep 'trigger.location'`) + `toml-gotchas.md` (a new section on the unscanned `entry_conditions`). Both holes confirmed in code (scan scope is `v2.py:11318-11391`, triggers + choices only; and no build check exists for a reachable zero-canvas room — it renders as a navigable dead end). **The ENGINE half — extending the validator — remains open and is NOT done.** Originally: PROVEN + FIXED IN GAME (pre-ship audit + fix-pass, 2026-07-16).

**The defect (two holes, same class).**
1. **Location `entry_conditions` are NOT scanned by the flag-chain validator.** It hard-fails only on flags read by a canvas *trigger/choice* (GAP 4/6). A location locked on `entry_conditions {flag is_true}` for a flag **no canvas sets** builds green and is a **permanently-locked, unenterable dead room**. On this game `loc_hotel_private_floor` was locked on `private_floor_open`, set 0 times — byte-for-byte v1's Dining Room, which the design-book postmortem itself named "the purest specimen of the disease… it does not come back." It came back, invisibly.
2. **No build check for "reachable location with zero located canvases."** Five served rooms (both locked doors + all three private bedrooms) shipped with 0 canvases; §5A.1 *pinned* named scenes into them **in prose**, but the scenes were authored in other (public) rooms. Prose pins don't enforce placement, so §5A.1 recurred the exact defect it was written to kill — the headline anti-v1 promise ("NO dead rooms") broke at v1's own count.

**Why the build was blind to both.** The flag-chain validator (v2.py:11332-11346) only reasons about canvas-trigger/choice flags; the packager never cross-references `location.id` against `trigger.location`. Both are pure static checks — a green build + "All flag chains valid" asserted completeness it never verified. Only the reachability audit caught them.

**Proposed engine + skill edits (CLASS-KILLERS — both pass "would a correct skill/engine have prevented this?").**
- **Engine:** extend the flag-chain validator to also scan `location.entry_conditions` and hard-fail an `is_true` gate on a flag with no setter — identical to how it already treats canvas triggers. And add a packager check: every location with an `entry_from` (i.e. reachable) and no `offscreen=true` must have ≥1 canvas whose `trigger.location` points at it, OR be explicitly tagged a nav-junction; else warn (or fail) "reachable room, zero content."
- **Skill (`location-design.md` §6 self-audit + `beat-authoring.md`):** a prose "room job" (§5A.1) is not satisfied until a canvas is *located* there — add a mechanical check: for every location with a named dramatic job, grep `trigger.location = "<id>"` and confirm ≥1 hit; a job asserted in prose with the scene built elsewhere is a dead room wearing a promise.

**How THIS game applied the fix.** back_office_numbers (loc_hotel_back_office) both sets `private_floor_open`/`escort_upgrade` AND gives the office its §5A.1 function; p_floor_private located at loc_hotel_private_floor; gray_amb_owned/ric_amb_room/marg_amb_vanity located in the three bedrooms (+ Grayson/Richard bedroom schedule windows so `requires_npc` fires); p_react_town fills loc_town's job. Post-fix: every reachable non-junction location has ≥1 canvas; whole-game `is_true` READS ⊆ SETS clean.

**PROMOTION GATE:** already proven (both holes let a real dead-room/never-set-flag ship green here). Fifth case where a reachability audit caught what static build checks can't — and the first that argues for an *engine* fix, not just a skill note. Promote the validator extension in the next engine pass; the location-job grep in the next skill pass.

---

## GAP 12 — `clothing_enabled=true` + a `naked_image` portrait + zero `[[clothing]]` items = forced-naked from turn 0; never scaffold clothing before an initial garment exists

**Status:** ✅ PROMOTED 2026-07-25 → `clothing.md` §9 as the OWNER (never enable before an `initial=true` garment; can't close the beat validated with zero items; the shop/wardrobe UI is engine-auto-rendered), with pointers from `step-0-1-seed.md` item 4 and `beat-authoring.md`'s optional-system row. Code corrections applied: `equipped` initializes to seven NULL slots (not `{}`), and the Shop page additionally requires `shop_location` — so it's two dead menus only when one is declared. Originally: PROVEN + FIXED IN GAME (pre-ship fix-pass, 2026-07-16).

**The defect.** The scaffold turned on `clothing_enabled=true` + a full `[player_portrait]` (naked/topless/bottomless/underwear images) but the "clothing beat" (beat_0007) was closed with **zero `[[clothing]]` items** — the author hit a "worn_type has no matching item" dead-rule warning and **deleted the portrait outfit rule instead of supplying the garment**, then marked the beat validated. Consequences the build never flagged:
- `equipped` initializes to `{}` → `getUndressLevel()` returns `'naked'` (nothing covers top/bottom) → the marquee player portrait resolves to `naked_image` **from turn 0, forever** (blank now only because media is un-harvested; naked the moment art lands).
- The engine auto-renders `WardrobePage` + `ShopPage` from the (empty) catalog → two reachable **dead menus** ("Change Clothes"/"Browse Clothes" → "No items").
- `worn_corruption` had **zero readers** → the "reactive world (clothing-driven)" the opening advertises was inert.

**Why it's a skill gap.** Nothing in the scaffold doctrine forbids enabling clothing before a garment exists, and "validated" was allowed on a reactive-clothing beat with an empty catalog. A different author repeats it on any clothing game. Also worth teaching: **the engine auto-renders the shop/wardrobe from the `[[clothing]]` catalog (v2.py:1835/1546) — a clothing shop needs NO manual buy-canvas, just priced items at `shop_location`** (I nearly built a redundant boutique canvas before checking).

**Proposed skill edit** (`step-0-1-seed.md` scaffold + `beat-authoring.md` self-audit): *"Do NOT set `clothing_enabled=true` (or declare a `naked_image` portrait) until at least one `initial=true` garment covering the body exists — an empty catalog forces the portrait to `naked` and exposes empty wardrobe/shop menus. A reactive-clothing beat cannot be closed 'validated' with zero `[[clothing]]` items when `clothing_enabled=true`. The shop/wardrobe UI is engine-auto-rendered from the catalog; no buy-canvas needed."*

**How THIS game applied the fix.** Authored 3 `initial=true` garments (dress/bra/briefs → dressed default) + 3 bold buyable tiers (corruption 12/22/30, `type="bold"`), restored `[[player_portrait.outfits]]` bold rule, added `pregnancy_trait="pregnant"` (the suffix was a dead declaration too), and wired 3 `p_react_*` ambients so `worn_corruption`/exhibitionism finally gate content. Verified: 6 items in `clothing_data`, dressed garments equip at boot, build green.

**PROMOTION GATE:** proven now (a live forced-naked portrait + two dead menus that would have shipped). Bundle the scaffold rule with the GAP-11 engine work in the next pass.
