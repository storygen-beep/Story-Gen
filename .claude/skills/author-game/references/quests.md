# Quests page — designing the whole surface (Story Goals + per-NPC ladders + end card)

The Quests page is a **designed surface**, not a pile of per-beat cards. It answers the player's "what do I do
now / where / how far am I" — and because the sidebar's *next* row is the **same renderer** (§4), a badly-designed
page is also a broken sidebar. Design it as one thing: the **Story-Goals spine** (the mission) + **one section per
arc'd NPC** (their own goal ladder) + an **end-of-content card**. Then author the cards.

Read this at **Step 5** (lay out the page — the design deliverable, §9), at **Step 7** (author each card —
`beat-authoring.md` owns the per-card field mechanics), and at **Step 6** (audit the page as a surface). This file
owns the **whole-page design + the ladder patterns + the traps**; `beat-authoring.md`'s "Quest cards" section owns
the card fields/modes; they don't overlap.

*(Why this file exists: Vesper reworked its Quests page **five** times — the two-tier split, the stepped ladder,
the end card, and a blank-sidebar bug were all found live because no step designed the page up front.)*

Engine facts are grounded in the current `v2.py` / `template_import.py` by **symbol + line** — line numbers drift
when the engine is regenerated, so if a line looks wrong, `grep -n` the named symbol (see `engine-reference.md`).

## Contents
- §1 — Two tiers, free from the engine
- §2 — The card shape (`[[quest_cards]]`)
- §3 — The three render frames (how a card shows)
- §4 — Sidebar `next` == Quests page (one renderer)
- §5 — Pick the ladder shape: milestone-chain vs stepped trait-band
- §6 — The Frame-3-blank trap
- §7 — The end-of-content card
- §8 — The quests-vs-sidebar split
- §9 — Designing the page (the Step-5 deliverable)
- §10 — Sweep the whole table when the world moves (⚠️ the three triggers)

---

## §1 — Two tiers, free from the engine
One field on a card picks its tier — no engine work:
- **No `npc_id`** → the top **Story Goals** section (the mission spine). Rendered by `pickQuestsCards("story_goals")`
  (`v2.py:14090`, returns every matching story card).
- **`npc_id = <slug>`** → that NPC's **own** section. `pickQuestsCard(slug)` (`v2.py:14065`) returns the **single
  highest-`priority` match** for that NPC — so an NPC's cards form a **one-live-at-a-time chain**.

What goes where: the **mission** and its investigation threads (a burned-yard clue trail) stay top-level Story
Goals even when an NPC touches them; only the **NPC-as-a-person arc** (a seduction) goes in the NPC tier. The page
is assembled by the `:: QuestsPage` passage (`v2.py:14355`): story section first (`:14363`), then one section per
NPC (`:14376`).

## §2 — The card shape (`[[quest_cards]]`)
The table is **`[[quest_cards]]`** — NOT `[[quests]]` (that's the unrelated v1 quest table). Requires
`quests_engine = "v2"` in project metadata or the V2 overlay isn't emitted (`template_import.py` gate ~`:2322`,
generator `v2.py:230`). Fields (`QuestsCard`, `template_import.py:868`, fields `:880-903`):

| field | what it is |
|---|---|
| `text` | the narrative line (there is **no `title`** field — section headers come from the NPC name / the literal "Story Goals") |
| `tip` | 💡 the one sanctioned system-voice coaching line (Quests page only — NOT the sidebar; §4) |
| `npc_id` | tier selector (§1) — omit for Story Goals |
| `priority` | higher wins when several of an NPC's cards match — the one-live-at-a-time selector |
| `when` | the gate: an array of conditions (flag/trait) that must all hold for this card to be live |
| `goals` | the 🎯 *To advance* bullets (each `{flag\|trait, subject, npc_id, op, value, label}`) |
| `ready_canvas` | set → the 🔓 Ready frame (the capstone is launchable) |
| `terminal` | `true` → the ✓ Arc-complete frame |
| `ready_text` | prose for the Ready frame |

**No `version = "1.0"` on `when`/`goals`.** Quest conditions use a *different* evaluator (`checkQuestsCondition`,
`v2.py:14131`) than canvas `conditions` — there is **no fail-open** here, so don't paste the `version` key onto a
quest card. Operators: `gte / lte / gt / lt / eq` (`v2.py:14155-14159`) + flag `is_true` / `is_false` (`:14135`).

## §3 — The three render frames (how a card shows)
`renderQuestsGoalBlock` (`v2.py:14217`) renders **exactly one** frame per card, in priority order:
1. **✓ Arc complete** — if `terminal = true` (`:14221`).
2. **🔓 Ready** — else if `ready_canvas` is set (`:14229`): the capstone is launchable, with **📍 location**
   (`:14237`) + **🕒 window** (`:14238`) pulled from that canvas.
3. **🎯 To advance** — else, and **only while a goal is UNMET** (`!allMet`, `:14244`): the goal bullets with live
   progress (`:14243-14262`). A **trait** goal renders `label — current / value` (`:14255`); a **flag** goal
   renders **label-only** (numberless).
Fall-through (none of the three) → `return ""` (`:14266`) → a **blank** row. That's the trap (§6).

**Coaching rides in `goals[].label`.** The sidebar shows only the goal block (§4), never the card's `text`/`tip` —
so the per-step verb ("Flash him at the depot") must live in the goal's `label`, not the prose. The label prints
`label || trait || flag` (`:14252`), so you may also bake the trait key in (`Break him to the drain (corruption)`)
if you want the meter named.

**The label is a walkthrough line — place + person + verb (+ window).** "Flash him at the depot" passes; "Prove
yourself to Renner" fails (no place, no clickable verb). If the step is schedule-gated the window rides too
("Catch Sol at the bar — evenings"). This is survival, not style: across the 2026-07 top-30 mopoga Twine-sandbox
study, lostness is the genre's dominant complaint (median 4.7% of ALL player comments; grind: 0.9% — players
quit lost, not bored), and the field's winners ship literal in-game walkthroughs (New Lust: per-girl pages with
progress bars + "Locked" cross-dependency labels; Course of Temptation: hint cards each ending in one concrete
"go to X, do Y"; the loudest counter-example is Corpo Life, whose off-site walkthrough died and left "how do I
trigger X" as its #1 comment theme). Atmosphere lives in the card's `text`; the label is load-bearing
navigation. (Evidence: `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/report.md` §F1.)

**A meter-gated rung names its FEEDER, not just its number.** When the next rung waits on a trait, the label or
`tip` says — in-world — which repeatable moves that meter: not "she isn't ready" but "she won't go further until
the lessons do — bring her a new word (her room, evenings)". The HUD already shows the number; the ROUTE to
raising it is what the player can't see. (Cross-ARC gates already obey this law via the locked-visible telegraph
naming the other arc's state — `step-2-toplevel.md` §7 D3; this extends it to trait feeders.)

**`tip` may speak in the NPC's own voice** where the register fits — "Buy a phone. Then find me in the kitchen."
(Destroyer ships ~151 one-line staged hints in NPC voice; its players ask for cheat codes, never for directions.)
Plain system-voice stays the sanctioned default (`onboarding.md` §5).

## §4 — Sidebar `next` == Quests page (one renderer)
The sidebar `npc_panel` **next** row calls the *identical* functions as the page: `pickQuestsCard(slug)`
(`v2.py:15454`) → `renderQuestsGoalBlock` (`:15456`) — the code even labels it "EXACT Quests-page parity"
(`:15450`). **There is no separate "sidebar quest."** Edit a `[[quest_cards]]` card and BOTH surfaces move in
lockstep — you never align them by hand. Two corollaries:
- An `npc_panel` pointing at a slug with **no `npc_id`-tagged card** → the next row renders **blank**. Creating
  that NPC's card fixes the sidebar for free.
- Static instructional prose in `text`/`tip` (e.g. "wear the cover") shows on the **Quests page only**, never the
  sidebar next row (goal bullets only). And quests can't read clothing — only flags/traits.

## §5 — Pick the ladder shape: milestone-chain vs stepped trait-band
An NPC's section is a **chain of cards, one live at a time**. Two shapes — pick by how the arc advances:

**A. Flag-milestone chain** (also in `beat-authoring.md`) — for an arc that advances in **discrete story beats**
(met her → first date → moved in). One card per stage, gated on the prior stage's flag `is_true` + this stage's
completion flag `is_false`. The card flips when a beat sets the next flag.

**B. Stepped trait-band ladder** (NEW) — for an arc riding **one climbing trait** (corruption 0→50). One card per
**exclusive band**, gated in `when` by a pair `{op="gte" value=X}` + `{op="lt" value=Y}`, so **exactly one** card
matches and the picker swaps it as the meter crosses each band. Recipe (Vesper's Renner, proven 28/28 live):

```
R1 tease    when corruption lt 10            goal → 10   label "Tease him at the depot"
R2 flash    when corruption gte 10 + lt 20   goal → 20   label "Flash him"
R3 grope    when corruption gte 20 + lt 30   goal → 30   label "Get your hands on him"
R4 cracking when corruption gte 30 + lt 40   goal → 40   label "He's cracking — push"
R5 break    when corruption gte 40 + lt 50   goal → 50   label "Break him to the drain"
R6 bed      when corruption gte 50 + flag renner_fucked_once is_false   goal = FLAG   label "Take him to bed"
```
- **Keep the number**: each rung's numeric goal denominator is the **next** band's threshold (the near lever), not
  one far-off 50. (A band crossing resets the denominator, 9/10 → 10/20; if you'd rather a stable /50, use one
  card with a `/50` goal + per-band `text` variants instead — a design trade, name it.)
- **Ride existing flags/traits** for the handoff (`renner_fucked_once`) — add no new flags, so flag-chain
  validation stays green (`toml-gotchas.md`).
- R6 is the **flag rung** that closes the trap (§6).

## §6 — The Frame-3-blank trap
The 🎯 *To advance* frame renders **only while a goal is UNMET** (`v2.py:14244`). So a card whose numeric goal is
**MET**, with **no `ready_canvas`** and **not `terminal`**, hits none of the three frames → `return ""`
(`:14266`) → a **blank** next-row (and blank Quests section). This bites the **top rung** of a stepped ladder:
once corruption hits 50, R5's `→ 50` goal is met and the sidebar goes blank.

**Fix:** the terminal window needs its own card with something still UNMET — either a **flag goal** (Vesper's R6
"take him to bed" gated on `renner_fucked_once is_false`, the one numberless rung) or a **`ready_canvas`** (the 🔓
Ready frame). Never leave a met-numeric card as the last thing an NPC's chain points at.

**⚠️ And the third case, which is worse because nothing looks wrong: the section DISAPPEARS.** A blank row at
least shows a heading. If the arc's last card retires with **nothing matching behind it**, `pickQuestsCard`
returns `null`, `:: QuestsPage` skips the section entirely (`v2.py:15141`), and the NPC vanishes off the page —
at the exact moment the arc ends and they become **permanent sandbox content the player can still go and use**.
So: **every arc'd NPC needs one card that matches forever after the arc closes** — the warm-tap / end-of-content
shape (§7). Audit it by walking each NPC's chain to its last rung and asking what matches *after* it.
*(Measured: Vesper's Renner ladder gates all nine cards on `renner_drained is_false` or
`renner_office_open is_false`; his heading disappeared on the drain while his office stayed open for the rest of
the game. Calloway and Colm both had an end card and did not. Nobody noticed for eleven beats.)*

## §7 — The end-of-content card
When an arc (or the whole build) runs out of content, show a **frontier-seed card**, not a dead number. A card
that is **goal-less + `ready_text`-less + non-terminal** renders as **flavor `text` + `tip` only** (Frame 3 is
skipped with no goals; nothing else matches). Rules:
- **Don't dangle a live `(locked)` bullet** whose goal never flips in this build — it reads as a fake objective
  forever. Remove the goals array.
- **Don't leak dev-speak** ("Bastien is Act-2 work") into a player tip. Keep the earned payoff, frame it forward:
  *"Renner's trail is logged. The hunt picks up from here in a future update."*

## §8 — The quests-vs-sidebar split
Quest cards carry **goals** (flags/traits toward content). **Body-need stats** (Charge / energy / hygiene) belong
on the **sidebar HUD** (`hud.md`, `trait-catalog.md` §5), never on a quest card — a quest is "what to chase," not
"how tired you are." Keep them separate or the page reads as a stats dump.

## §9 — Designing the page (the Step-5 deliverable)
At blueprint (Step 5), lay out the **whole page** in the design book, before authoring cards:
1. **The Story-Goals column** — from the desire ladder (`step-2-toplevel.md`): the mission's current want + next
   action, plus any mission investigation threads. One live card, advanced by story flags.
2. **One section per arc'd NPC** — choose the shape (§5): milestone-chain (discrete beats) or stepped trait-band
   (one climbing trait). Write the rungs, each with its `when` band and its `goals[].label` **walkthrough line**
   (place + person + verb — §3); a meter-gated rung names its feeder (§3).
3. **The end-of-content card** (§7) — where the current build stops.
4. **Check it as a surface:** every NPC section is non-stale (§6 — no met-numeric dead end, and nothing that
   *disappears*), every live label passes the walkthrough standard (§3), parity-matched to its `npc_panel` next
   row (§4), and free of dev-speak. Confirm at Step 6.
5. **⚠️ No two CO-LIVE cards repeat a clause.** The Story-Goals card and every NPC card render on **one
   screen**, so a phrase carried over from the spine prints twice in the same view. This is not a hypothetical
   tidiness note: authoring an NPC tier *next to* the spine cards it belongs with produces the echo almost
   every time — the sentence is right there and it is the best sentence you have. Vesper's `beat_0084` shipped
   eight of them into one draft and had to rewrite every card to kill them. The rule that fixes it is the same
   one that justifies the two tiers at all: **the NPC card says what the spine leaves out** — the man, the
   count, the state of him — never the mission beat again in different words. Audit mechanically: for each
   reachable state, take the live set and flag any **six-word run** shared by two of them.

## §10 — Sweep the whole table when the world moves
§9 lays the page out **once**. This section is the maintenance rule, and it is the one the page actually fails
on: a card is written true, the world changes around it, and the card keeps saying the old thing. Nothing warns
you — the build is green, the card renders, the sentence is grammatical. **Three triggers, each one a
whole-table grep, never a read of the card in front of you.**

**⚠️ The trap that makes all three hard: these defects cannot be checked LOCALLY.** Asking "is this card's
sentence true from where this card stands?" answers *yes* for every one of them. That is the wrong question.

### 1. The frontier moves → re-grep the boundary claim
When the build ends somewhere, the frontier card says so ("that's where this build ends; X is the next
release"). When the next chunk ships, that card **is still saying it** — and it is now describing this
release's own contents as the next one.

**Rule: exactly ONE card in the game may name the build boundary.** Moving the frontier is a **two-step**
edit — *strip the old, add the new* — and the check is
`grep -c 'build ends' <the tip assignments>` over the whole table, expecting **1**. Anchor the grep on the
syntax that **declares** a tip (`^tip\s*=`), not on the bare string: the comment blocks quote the sentences you
stripped, so a naive count matches its own history.
The **Support-Us ask is a separate thing and rides EVERY rung** — a player who stops anywhere should see it.
Only the *claim* walks. (Strip both at once and the live card loses the ask for the whole chunk.)

*(Measured, Vesper 1b: the boundary walked forward five times and three cards were left holding it. The
comments above two of them record the check being **run and passed** — against the card's own rung. The worst
of the three named "cutting the leash, opening the file, and reading what you are" as the next release, in a
build that shipped all three.)*

### 2. The map seals or opens → re-grep every place-name
**A `tip` is a direction, so it is coupled to reachability.** When a beat locks a region, greys out a travel
choice, or moves a location's parent, every live card naming somewhere inside it becomes a false direction —
and pointing a player at content they cannot reach is the purest form of the genre's dominant complaint (§3).
Sweep by NPC **and** by place: for each live card, is the place still reachable *from where the player now
is*, and is the person still there?

Watch for the **half-stale** card, which is the easy one to miss: Vesper's Colm end card kept a back room that
was still open and a "take it to Vane at Vance Securities" that pointed through a sealed floor.
**The fix is usually ONE card, not N edits** — the NPC tier returns the single highest-priority match
(`pickQuestsCard`, §1), so a new card at a priority **above the whole ladder**, gated on the sealing flag,
covers every rung at once and cannot be defeated by where the player's arc stopped. That last part matters:
the *unfinished* arc is the worse case, because its rungs are live instructions.

### 3. A mechanic retires → sweep the cards with the canvases
`lanes.md`'s terminal-flag sweep ("when a flag makes something permanently true, list what it makes
permanently false") binds here too. If a beat retires an item, a switch, a meter, or a gate, then any card
whose subject is *acquiring or smuggling that thing* is now an instruction about an object that no longer
exists. Give it a post-retirement partner card gated on the terminal flag, exactly as you would re-partition a
canvas's exits.

### The audit, as three commands
Run at Step 6, and again in the beat that moves any of the three:
```
grep -n '^tip'  <scenes>.toml | grep -c 'build ends'     # expect exactly 1
grep -n '^tip'  <scenes>.toml | grep -i '<sealed place>' # expect 0 live cards
```
plus, for each arc'd NPC, walk the chain to its last rung and ask **what matches after it** (§6).

---

**Cross-references (in-skill):**
- `references/beat-authoring.md` — the per-card field mechanics + the three card modes (author each card at Step 7).
- `references/hud.md` — the `npc_panel` `next` row (same renderer, §4) + the sidebar band mapping.
- `references/step-2-toplevel.md` — the desire ladder = the Story-Goals column (§9).
- `references/step-5-blueprint.md` — where the page is laid out (Pass 3 §5F).
- `references/trait-catalog.md` §5 / `references/toml-gotchas.md` — the sidebar band split + the flat `when`/`goals`
  condition shape (no `version` key).
- `references/engine-reference.md` — the `QuestsCard` / `QuestsCondition` field tables.
