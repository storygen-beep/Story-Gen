# Forty Miles — review ledger

Opened 2026-08-14, the day it was listed on the portal. Forty Miles is the **second clean-room
game** for `author-game-v2` — authored by a reader of the skill, after `the-surfaces.md` and R2b
existed, which `steam` was built without.

It scored **20/20, exit 0** at 0.1, and it is the best-written game in this repo. It also shipped
**three blockers that no gate, no lint and its own 11/11 play-test all missed** — two found by this
review and one found only when the fix pass re-checked its own findings. That combination is the
whole point, and it is the same shape as Steam's: **the scoreboard is green and the scoreboard is
not the review.** §0a records where the review itself was wrong.

**Same conventions as `games/steam/REVIEW.md` and `games/back_home/REVIEW.md`:** severity
`BLOCKER`/`HIGH`/`MED`/`LOW` · layer `GAME` (this build) / `SKILL` (doctrine taught it wrong or not
at all) / `ENGINE` · every claim carries a measurement, a `file:line`, or a live observation.

**Method.** Parsed `toml_phases/7_final_game.toml` with a real TOML parser (never grep), then
**played the shipped `releases/v0.1.html`** in `twine-game-explorer`: the opening funnel end to end,
free roam, Bev's handover, the Nunn settle-up, a full six-beat repeatable sex loop, an A/B of one
hub at low and high ascent, a 20-point schedule probe across every midnight and week boundary, and
boundary tests at zero money and zero energy. Every structural claim below was checked in the built
game, not inferred from source.

Current count: **10 of 10 addressed in 0.1.1**, plus **four things this review got wrong or never
looked for**, found by re-investigating before editing. Skill-layer causes for F3 and F5 shipped
2026-08-15 via `DOCTRINE_GAPS.md` study 6; the game itself was repaired 2026-08-16 and now scores
**24/24**.

---

# 0a · ⚠️ What this review got wrong

Written after the repair pass. **Every finding below was re-checked against source and against a
live build before anything was edited**, and four of them did not survive that check. Two of the
four are worse than the things the review did find.

### ⚠️ N1 · BLOCKER — 35 authored effects were silently discarded, and nothing in this review looked

`op = "subtract"` **is not an engine operation.** `applyTraitEffect` runs `add` and `set` and falls
through to `// Unknown op; do nothing` + `return` on anything else (`v2.py:5742-5751`). The string
`subtract` appears nowhere in the generator or the importer, so the build emitted
`applyAndNotifyTrait(..., "subtract", 4, ...)` verbatim into `output/index.html`, 35 times, and the
runtime dropped every one. Proven live on the shipped 0.1:

```
count 100  →  applyAndNotifyTrait('player',null,'count','subtract',4,true,null)   →  count 100
energy 100 →  applyAndNotifyTrait('player',null,'energy','subtract',12,true,null) →  energy 100
stress 20  →  applyAndNotifyTrait('player',null,'stress','add',-5,false,null)     →  stress 15
```

| trait | live `add` | dead `subtract` | what 0.1 actually did |
|---|---|---|---|
| `count` | 2 (positive) | **12** | starts at 100, clamps at 100 — **the counterweight never moved once in the entire game.** Its sidebar band was permanently "Balances to the penny". |
| `energy` | 8 | **20** | no activity ever cost energy. It left only via location `entry_costs` (2, on three locations) and `trait_decay = 9`/day. |
| `stress` | 13 | 1 | one-way ratchet, no decay declared. |
| `relation` | 52 | 1 | Nunn's short-week penalty never applied. |
| `money` | 11 | 1 | the bay-9 coffee was free. |

**Layer: SKILL + ENGINE.** `references/engine.md:497` discussed `op = "subtract"` as authored
behaviour — the skill taught it. `template_import.py:3755` validates `op` for cheat-page grants and
nothing validated it for effects. **`games/steam` has 70 of these**, which is what makes it a class
rather than a slip. Why nothing caught it: valid TOML, green build, 20/20 gates, and an 11/11
play-test, because **a number that never changes looks exactly like a number nobody has moved.**

Fixed in 0.1.1: all 35 rewritten to `op = "add"` with negative values, `engine.md` §21b written,
**gate 25** added (fails `steam` at 70, passes `back_home` at 0 — it discriminates), and
`template_import.py` now hard-fails so no future build can emit one.

### ⚠️ N2 · F2 is wrong on its central claim — the obligation WAS charged

F2 says the settle-up *"does not exist in the build."* It does. `[settings.rent]` is enabled at
`0_systems_spec.toml:61-69` with `amount = 245`, `due_day = "Friday"`, `collector_npc = "npc_nunn"`,
`start_after_flag = "first_shift_done"` (set in `canvas_opening`). Verified live, end to end:

```
Thursday 23:00 → advanceTime(90) → Friday 00:30 → rent_state.is_due = true   (v2.py:5453-5464)
Engine.play("Location_the_forecourt") → intercepted → RentDay                (v2.py:15247-15259)
"Pay $245 rent" → money 300 → 55, is_due → false                             (v2.py:15925)
```

F2's search — *"any 200 / 245 / 45 anywhere .. NONE"* — walked the canvases and never looked at
`[settings]`. **What is genuinely wrong is a duplicate, not an absence:** `rung_nunn_settle`
narrated the same handover for free, granted `relation +3`, and was re-clickable, so the player met
two settle-ups and the free one was the one with the writing in it. Three smaller things fell out:
the RentDay pages hardcoded `$` in a game whose every other price is in pounds; the demand arms at
the **midnight rollover**, not at the 18:00 Friday row Nunn's schedule and the prose both promised;
and **gate 24 could not see any of it**, so it failed a game whose obligation was charged correctly.

Fixed in 0.1.1: `rung_nunn_settle` → `rung_nunn_squared`, re-aimed to the Friday evening with
nothing owed and capped at relation 24; `rung_nunn_short_week` re-aimed to the ask made before the
draw; `[settings.rent] currency_symbol` added to the engine; the rent scene text and Bev's opening
line rewritten to the hour the demand actually lands; gate 24 taught to read `[settings.rent]`;
`engine.md` §26 written.

### ⚠️ N3 · The TRADE ladder's guidance was circular at all three rungs

Not in the review at all, and it made the game's third ascent tier effectively unclimbable by
following its own instructions. Each `trade` quest card named a choice gated at the exact value the
card was trying to reach — *"Sell a token off the book"* for `trade ≥ 15`, on a choice requiring
`trade ≥ 15`. **`nights` and `seen` were both correct** (every card names a choice gated one tier
*below* its goal), so the shape was known and one ladder simply missed it. Fixed, and the top band
re-earned: moving *"Bring somebody back here"* down to `trade ≥ 35` emptied `trade ≥ 55`, which
gate 8 caught immediately, so *"Hand a token over in here instead of at the till"* now buys it.

### N4 · Two counts in this review are off

- **F1's third-person count is 77, not 62** — and one more mixes both persons. 67 of the 147 are
  person-neutral and needed attribution only. Three are correctly third-person and were left alone:
  two are about Bev, one is Denny quoted.
- **F9's diagnosis is wrong.** The four sidebar strings are not quest-card titles; a card has **no
  title field** (`template_import.py:997-1039`). They are `[[sidebar_items]] type =
  "trait_status_text"` bands doing exactly what `the-voice.md` R1 asks. The real gap was that the
  engine had **no sidebar item type that renders a next step at all** — fixed by adding one.

---

# 0 · Read this before the defect list

**The prose is the best this project has produced, and nothing below should touch it.**

The pivot rule — the defect that recurred three increments running elsewhere — is honoured almost
perfectly. Measured across every explicit beat in the game:

```
explicit beats ......................... 165 / 1,188  =  13.9%   (floor 7.5%)
whose LAST SENTENCE leaves the body ....   2 / 165    =   1%
their length ........................... median 37w · mean 37.4w  (target 35-40)
texture beats .......................... median 31w · mean 31.5w
```

Heat beats sit dead in the target band while ordinary beats run leaner. Both of the two "pivot"
candidates are still physical (*"goes through you like a footstep"*). **This is the cleanest pivot
compliance the project has measured.**

Played live, the repeatable shower loop escalates six beats and never flinches:

> *"You strip and hang the vest on the hook and stand under it naked, tits and cunt bare to a door
> that will not hold… Two fingers in your cunt and your thumb working your clit, stood up, back to
> the tile, your tits wet and your eyes on the gap… You come with your eyes open on the door."*

That is a **re-enterable** surface at a location visited nightly — the thing the doctrine exists to
produce, and the thing the measured failure case did not have.

**The schedules are the strongest system in the game.** Twenty live probes, every one correct:

```
Hal    Tue 23:00 park → Wed 01:00 shop → Wed 03:00 park → Wed 05:30 park     ✓
Ossie  Fri 22:30 bay  → Sat 00:30 bay  → Sat 01:30 bay  → Sat 02:30 gone     ✓
Denny  Thu 23:00 park → Fri 00:30 shop → Fri 01:30 park  (and Sun→Mon same)  ✓
Tam    all seven nights, 20:00-06:00, wraps correctly                        ✓
Bev / Nunn day windows                                                       ✓
```

Every day-specific overnight window is correctly **split into two rows** with the day rolled
forward, and the all-days row correctly left single. This is the exact trap that has bitten this
project before, and the game got it right.

**The economy's enforcement works** (its pricing does not — see F2). Verified live: at £0 a costed
choice disables itself and states the shortfall — *"Buy something off the hot counter (£3).
(Requires 3 Money (you have 0))"*. At 0 energy a costed bridge refuses and routes to a block page —
*"Not Right Now / Requires 2 Energy (you have 0)"*. **And the run cannot brick:** the three
free-entry locations include `rung_shop_coffee` (+2 energy, free), so zero energy is always
recoverable.

**The locked door holds.** At nights/seen/trade = 99, *"Open the padlocked door."* still renders and
still refuses; `canvas_back_room_key` is `is_active = false` and `back_room_key` is never set. The
release ends on a visible locked door exactly as designed.

**The guidance page is the best in the repo.** Every card names a place, a time window, a verb and a
counter:

> `◯ Take his twenty minutes — the shop, Tuesday 01:00 — 0 / 40`
> `💡 One in the morning, Tuesday. Do not fill the twenty minutes with talk.`

**The NPC hubs are textbook.** 55% of their choices are gated, median **3** actionable on day one
growing to 7-8 — the field median, hit exactly. Bev's handover opens 3 of 8 with five visible locks.

**The location screens obey "a place is not a catalogue."** `Location_the_shop` renders one canvas
link and two exits; the forecourt one canvas and four exits **with the cost on the label** —
`The Lorry Park · 10m · 2 Energy`. A real improvement on Steam's 23-choice front desk.

---

# 1 · F1 · Every thought bubble is attributed to a character called "Npc" — and 62 of them are in the wrong person

**severity** BLOCKER · **layer** SKILL + GAME · **status** ✅ **FIXED 0.1.1** — all 147 blocks carry `props.speaker`; 74 rewritten to second person; 3 correctly left third-person (two about Bev, one Denny quoted). Verified live: `💭 You are thinking:`. Gate 23 reads 204/204.

Measured in the shipped `releases/v0.1.html`:

```
'💭 Npc is thinking:'  ........................  147 occurrences across 147 passages
all thought-bubble speaker labels in the build      {'Npc': 147}
screens whose LAST rendered block is a bubble ....  145 / 250  =  58%
```

**Every single one**, on **58% of all screens**. Seen live on the fourth turn, before free roam:

> 💭 **Npc is thinking:** Two hundred for him and forty-five for the van, out of a week that pays
> three-fifty. She knows the numbers.

### Cause

All 147 `thought_bubble` blocks are authored with no `props` at all:

```toml
{ type = "thought_bubble", content = "Bev does this drawer twice a day and has done for eleven years and drives a car that starts." }
```

The engine defaults a missing speaker to the literal string `"npc"` (`v2.py:14631`):

```python
speaker = props.get("speaker", "npc")
```

`"npc"` satisfies `speaker.startswith(("npc_", "npc"))`, so the unknown-speaker branch is skipped
and the NPC branch runs with `npc_id = "npc"` (`v2.py:14651`). No NPC matches, so the fallback
title-cases the id (`v2.py:14657`) — `"npc".title()` → `"Npc"`.

### The half that is not mechanical

`[settings] narration_person = "second"`. But of the 147 bubbles, **62 refer to Robyn in the third
person and only 3 use "you"**:

> *"Eleven feet. She has measured it now and she is not going to be able to stop knowing the number."*
> *"Twelve hours ago she owned this room. Now she is number five in a queue in it."*
> *"The best part of her day starts at twenty-two hundred hours and she has stopped pretending that is a normal thing."*

These are not anybody's interiority — they are an **authorial commentary track** standing outside
the second-person frame. Stamping `speaker = "player"` on them yields *"💭 You are thinking: She has
measured it now…"*, which is worse. **The 62 need rewriting as well as re-attributing.**

There is a doctrine question underneath: the game avoids the pivot *inside* explicit beats (1%,
§0) and then reintroduces meaning-commentary as a separate block on 58% of screens. That is
technically what `register.md:44` permits — *"its own beat, after"* — at a volume nobody costed.

### Why this is a SKILL defect and not just an author slip

The **v1** `author-game` skill teaches the prop in three separate places:

- `references/beat-authoring.md:394` — `{ type = "dialog", props = { speaker = "player" }, ... }`
- `references/rts-flat-prose.md:699-704` — a worked `thought_bubble` with `props = { speaker = "npc", npcId = "npc_frank" }`
- `references/npc-intro.md:64` — the `speaker="unknown"` → `"Stranger:"` branch, with its `file:line`

The **v2** skill mentions `thought_bubble` **exactly once**, at `references/register.md:44`, as a
*register* instruction, with no authoring shape and no mention of `speaker` anywhere in the skill.
**v2 told the author when to use a thought bubble and never how.** A doctrine regression from v1 to
v2. `references/engine.md` compounds it: `speaker = "unknown"` sits in the **"Unverified — do not
cite"** list, and the *absent*-speaker default that actually shipped was never documented at all.

The contrast proves it: **57 `dialog` blocks, 0 missing `props.speaker`, all rendering `Bev:`
correctly.** The author got right what they were shown and wrong what they were not.

### Why no check caught it

`gates.py`'s attribution lint walks only `type == "dialog"` (`gates.py:380`). `thought_bubble` is in
`PROSE_BLOCKS` for word-counting (`gates.py:144`) but is invisible to the one lint written for this
class of bug. The lint reported **2 dialog canvases to eyeball** — both fine live — while 147 real
breakages went unreported.

### Fix

1. **Game** — attribute all 147; rewrite the 62 third-person ones to second person.
2. **Skill** — put the `thought_bubble`/`dialog` authoring shape on the v2 authoring path with its
   three speaker variants and a `file:line`. Promote the absent-speaker default out of "Unverified".
3. **Gate** — extend the attribution lint to `thought_bubble` and make an *absent* `speaker` a hard
   finding, not an eyeball: unlike a dialog speaker, there is no case where omitting it is correct.

---

# 2 · F2 · The Friday settle-up charges nothing, and repeats without limit

**severity** BLOCKER · **layer** GAME + SKILL · **status** ⚠️ **WRONG — see §0a N2**, then ✅ **FIXED 0.1.1**. The obligation *was* charged, by `[settings.rent]`, verified live at 300 → 55. The real defect was a free duplicate canvas beside it. Read §0a before this section.

The obligation is the spine of the Want. `v2_state.json` declares it:

> *"He paid GBP 6,000 to make her problem go away and takes GBP 200 a week back, plus GBP 45 for the
> caravan."* · *"Priced in BOTH directions per the-economy.md R3: payable on a clean week and
> genuinely tight on a bad one."*

The quest card says *"💡 Have the two hundred and forty-five."*

**It does not exist in the build.** `rung_nunn_settle` carries no `costs`, no money effect, and no
day gate:

```
rung_nunn_settle · effects: [ npc_nunn.relation +3 ]
                 · costs:   []
hub_nunn_forecourt · is_repeatable: true · no max_triggers_per_day
```

Played live with £300: **before £300, after £300.** Re-entering the hub on the same Friday offers
*"Go out to the car with the week."* again, unchanged.

Searching the whole game for the money:

```
money SUBTRACT effects ......  1  (rung_bay9_coffee, £1)
money COSTS on choices ......  10 (£1-£35, total £90, all optional purchases)
any 200 / 245 / 45 anywhere .. NONE
```

Against income of **£70/night** (`canvas_shop_cash_up`, `max_triggers_per_day = 1`, `clamp: false`)
— correctly day-gated, and running against **zero recurring outflow.** Money only ever goes up.
After a week the player has £490 and the game contains £90 of things to buy.

The failure branch is the same shape: `rung_nunn_short_week` is also free, also unlimited, and
applies `npc_nunn.relation −3` + `stress +3`. **The two branches are an unlimited relation faucet in
both directions**, clickable back to back at no cost.

### Why the gates and the play-test missed it

- **Gate 16** (*money gates something*) passes on the **9 other** canvases that gate on money. The
  obligation itself gates on nothing.
- **Gate 17** (*sinks ≥ sources*) counts the 10 optional purchases as sinks and reports `11 : 11`.
  The single largest declared sink in the design is absent and nothing notices.
- **Gate 18** (*no free uncapped income*) passes because the wage is day-capped. It is uncapped
  against nothing.
- **`playtest.py` 11/11** verified *"money is UNCLAMPED so the 245 draw is payable"* — it checked the
  **precondition** and never the **transaction**.

This is a direct violation of the skill's own standard at `SKILL.md:107` — *"the BOARD DECLARES IT
and the gate checks the game against its own declaration."* `board.economy.obligation` declares a
price and a cadence. Nothing checks it.

### Fix

1. **Game** — put `costs = [{ trait = "money", value = 245 }]` on the settle-up choice, day-gate the
   hub, and give the short-week branch a real consequence.
2. **Skill/gate** — a new gate: *if the board declares an obligation with a price, some choice must
   charge that price on that cadence.* This is the cheapest possible check and it would have caught
   the game's central mechanic being missing.

---

# 3 · F3 · The location hubs never change; the NPC hubs do it right

**severity** HIGH · **layer** SKILL + GAME · **status** ✅ **FIXED** — doctrine 2026-08-15, game 0.1.1. Room hubs went 126/166 → 70/166 open on night one, median 3, matching the NPC hubs and the field. Nothing deleted; the tiers now open the rooms. Verified live: 4 open / 4 visibly locked at tier 0, 8 open at tier 60.
untouched**

> **The skill-side half shipped.** `the-surfaces.md` R3 no longer states a cap as the rule: the
> count now derives from R2b (write the room, name what she can act on, one choice per thing), with
> 8 named explicitly as a backstop for the pathological case. Gate 20 prints the distribution, so
> this game and a well-shaped one no longer read alike:
>
> ```
> forty_miles   0 screens over 8 · median 8 · 19/29 screens at the cap
> back_home     0 screens over 8 · median 5 · 0/12 screens at the cap
> ```
>
> The game itself is unchanged and every number below still stands.

Measured live: `hub_shop_counter_early` rendered at `0/0/0` and at `40/40/40` is **byte-identical** —
same prose, same eight choices, same order, only the 🔒 clearing. The reference game's cafe goes
**5 → 9 → 8** across six visits (`DOCTRINE_GAPS.md` study 5, R7). This goes **8 → 8 → 8**.

But the split is the real finding:

```
                     screens  choices  gated        open on day one   open-count per screen
NPC-bound hubs          7        47    26 (55%)     21 (45%)          min 2 · median 3 · max 4
location-only hubs     22       166    40 (24%)    126 (76%)          min 1 · median 6 · max 8
```

**The NPC hubs are exemplary** — median 3 open on day one, matching the field. **The location hubs
are not**, and three of them are fully open on night one and never change again:

```
hub_tyre_bay         8 choices · 0 gated
hub_shop_day         8 choices · 0 gated
hub_forecourt_dawn   8 choices · 0 gated
```

The author clearly understood the pattern and applied it to people and not to rooms.

### The cause is that the rooms were built to the ceiling

```
gate-20 population (repeatable, located)  ....  30 nodes, 213 choices
choices per node .......  median 8.0 · mean 7.1 · max 8
at exactly 8 (the cap) .......................  19 of 30
```

The field figure the skill itself quotes is **median 2 links, p90 4** on a parse and **median 3,
max 6 things-to-do** on the play study. A screen already at the ceiling on night one has no room to
grow, which is why R6's third mechanism — *the choice list itself varies* — is structurally
unavailable. The two lints report the same fact from two angles: `147/213 open on turn one` and
`29/29 standing menus never change their prose`.

### The cap redistributed the menu. It did not shrink it.

Measured against Steam, the game gate 20 was written to fail:

```
                            steam        forty_miles
repeatable located screens     22             29
TOTAL choices on them         214            213      <-- unchanged
choices per screen      median  7      median  8      <-- went UP
                           max 23         max  8
screens over 8                  9              0
open on day one          107 (50%)      147 (69%)     <-- got WORSE
```

**The same 213 menu items, spread over seven more screens.** Gate 20 removed nothing; it capped the
outliers and pushed the median up to the cap. Steam had a few enormous screens and some small ones.
Forty Miles has twenty-nine screens that are nearly all *at* the limit — so the player meets a full
menu **more often**, not less, and 69% of it is open on night one against Steam's 50%.

And because the location page is now its own screen (1 canvas link + exits), reaching content costs
**two lists instead of one**: pick a room, then pick a sub-surface, then pick a rung.

### Why this is a SKILL defect

`the-surfaces.md` R3 gives a **ceiling** and no **target**, and `gates.py` PASSes at exactly 8 — so 8
is what an author optimising against a green board builds, nineteen times. Steam failed this gate at
23; Forty Miles passes it at 8 on every room. **Both games have one flat menu per place, and the
same number of menu items.** The cap moved the number and did not move the shape.

A ceiling gate can only ever make the worst screen legal. It cannot make the typical screen small,
and on this evidence it makes the typical screen *bigger*, because the cap reads as the spec.

**Fix (skill):** R3 needs a target beside its ceiling — *the median location screen offers 3-4
decisions; 8 is the hard cap for the widest surface in the game, not the size of a normal one* — and
gate 20 should report the game's **median and its count-at-cap**, so a game built to the ceiling
reads differently from a game built to the field.

---

# 4 · F4 · Nothing in the game ever happens unprompted

**severity** HIGH · **layer** GAME · **status** ✅ **FIXED 0.1.1** — eight `trigger_mode = "random"` events, one per location, three behind the tier that earns them. Verified live: they fire on location entry at 13–24% and the gated three are silent at zero.

```
canvases with trigger_mode = "random"  ......  0
non-repeatable located canvases .............  4
    canvas_opening, canvas_first_hatch, canvas_blind_spot   (the opening funnel)
    canvas_back_room_key                                    (is_active = false)
```

Of 247 canvases: 213 are triggerless link-target rungs, 30 are repeatable hubs, and the four that
can fire on their own are the funnel plus one disabled stub. **After the funnel ends — around turn
11 — every single thing that happens is something the player clicked.**

This is M4, the axis the play study named as *"the layer both our games are thinnest on and for
which we currently have no number at all."* The number is zero.

The reference game replaced the whole street screen with a harassment scene on two consecutive
visits — R6's fourth mechanism, an event *instead of* the location menu. Forty Miles has no
mechanism for it: no `trigger_mode = "random"`, no chance-gated canvas, nothing that can interrupt.

The world is exceptionally well specified — nine cabs, a CB channel, a rota, six people on correct
schedules — and it never acts first. For a game premised on *forty miles of nothing and you are the
only person awake*, nothing ever arriving unbidden is a thematic loss as well as a mechanical one.

**Not a gate.** No threshold is defensible yet and inventing one would repeat the R5/R6 mistake. It
belongs in the next release's Want.

---

# 5 · F5 · A third of hub choices float free of the screen's prose (R2b)

**severity** MED · **layer** GAME · **status** ✅ **FIXED 0.1.1** — 8 unusable declared objects cut or made usable, 6 real affordances declared, three room openers gained the thing their choices act on. Gate 22 reads 0 / 0 / 0.

> **R2b is no longer ungated.** `board.locations[].objects` was backfilled for this game — derived
> by reading what each room's prose names, not from its choice lists. Two halves now watch it:
>
> ```
> [FAIL]  declared objects are real   65 declared objects across 8 rooms · 0 never written · 8 unusable
> lint · choices hang off the room  — 91/166 (55%) name something their own screen's prose said
> ```
>
> **Only the first is a gate.** The anchoring share is a lint, because a word-match fails "Mirror"
> under a paragraph about a wardrobe — including in the skill's own worked example — so a pass/fail
> line demanding zero failures could never be cleared. **Like-for-like against the by-hand 41%
> below the instrument gives 51%** — both over 213 choices including character hubs. The 55% in
> the lint is over ROOM screens only (166), a different population; do not read the two as a
> before-and-after. The *ranking* of screens is unchanged, which is what matters.

Lexical-anchor proxy across all 29 hub screens — does a choice share a content word with the prose
on its own screen: **87 / 213 = 41%** by hand, **108 / 213 = 51%** on the shipped instrument,
which stems words and counts the location's own description.

The proxy undercounts character hubs, where the anchor is the person (`hub_bev_handover` scores 0%
and is fine — all eight choices take Bev as the object of the verb, R1/R2 clean). The **location**
hubs split hard:

**Exemplary.** `hub_stock_room` — the opener names roll cages, the cold store, the recorder and its
four-picture screen, the eleven feet, and the padlock. All eight choices hang off one of them.

**Weak.** `hub_stock_room_dawn` — a 43-word opener, then choices introducing *the back door*, *the
hasp*, *the wastage sheet*, *the first Tuesday* and *a dropped crate*, none of which the prose put in
the room. `hub_showers_dawn`, `hub_park_dawn`, `hub_showers_deep_night` sit at 25%.

### The root cause is F3

```
hub openers  ....  median 60 words · min 38 · max 90
choices      ....  median 8
```

**Roughly seven words of prose per choice.** An opener that size cannot name eight things.

### The inverse case, worth naming separately

`hub_shop_counter_early` gives **the hatch an entire paragraph** — *"The hatch is up. It comes down
at midnight. That is the rule and there are two hours until it applies to you."* — the central image
of the whole game, with **no choice hanging on it.** A named object with no affordance is the mirror
of a choice with no object, and R2b as written only warned about one direction.

**Gate 22 checks that direction too**, and this game has eight of them — named, written, and
unusable: *the drawer · the safe drawer and the wage envelope · the bunk the width of a door ·
the kettle on the engine hump · the fan heater · the two-ring hob · the table that folds ·
the shelves.*

### The gate discriminates, which is the point

```
hub_stock_room       2 floating   "Work out the fourteen days." · "Bring somebody back here."
hub_stock_room_dawn  5 floating   "Do the restock." · "Get up for the first Tuesday."
                                  · "Put it on the wastage sheet instead." · "Look at the hasp."
                                  · "Pay for the crate you dropped (£6)."
```

Same ordering as the by-hand read above — the exemplary screen and the worst screen — and every
flagged line is a genuinely unanchored noun. A check that failed everything would have been as
useless as one that passed everything.

---

# 6 · F6 · No media, and two gates pass on media that does not exist

**severity** MED · **layer** GAME (disclosed) + SKILL · **status** OPEN — media is a logged promise, not a 0.1.1 fix. **The gate half is also still open**: no gate in `gates.py` touches the filesystem, so 68 declared pools with zero files still report 100%.

```
declared  ....  68 video pool_dirs · 2 fixed files · 8 location plates · 6 portraits
on disk   ....  0.  games/forty_miles/media/ does not exist.
```

Disclosed in the portal commit (`d2730de`) and in the promises, so the *state* is not a surprise.
Two things about it are.

**The gates.** Both of these PASS on pools with zero files behind them:

```
[PASS]  repeatable explicit media cycles  68 pooled, 0 fixed single-clip in repeatable content
[PASS]  traversal heat                    8/8 locations (100%) carry a cycling explicit pool
```

That contradicts `SKILL.md:107` — *"an absence is not a pass."* Both measure the **declaration** and
neither resolves it against disk.

**What it does to the screen.** Measured live: every hub renders a **~170px empty band** between the
prose and the choice list — the reader gets a paragraph, a void, then a button list, which weakens
exactly the adjacency R2b depends on. NPC presence renders through `setup.renderNpcPortraits()`, so
Ossie appears as an empty broken-image ring with his alt text spilling out. Presence stays *legible*
— the name renders in a sibling `<span class="npc-portrait-name">` — but the screen looks
unfinished in a way the TOML cannot show.

**Checked and clear:** `MissingMediaPage`, which holds all 69 pool paths with their raw AI search
queries, is gated behind `<<if $flags.debug_mode>>` in `TimeWidgets` and is unreachable in this
build. No internal strings leak to a player.

---

# 7 · F7 · Bev's entire arc is written under her declared ceiling

**severity** MED · **layer** GAME · **status** ✅ **FIXED 0.1.1** — her three tiers are written. Tier 1 across the ungated rungs, tier 2 at relation 20, tier 3 as a new node on her top rung: the stock room, on the clock. She now carries cunt/clit/tits/wet/knees across 1,628 words. See `decisions` in the ledger for what it costs the character.

Crude vocabulary actually used, per NPC arc (hub + every rung it owns):

```
npc_bev     1,221w   NONE
npc_denny   2,118w   cunt 9 · tits 8 · cock 5 · clit 3
npc_hal     1,337w   cunt 6 · tits 4 · cock 2 · clit 2 · nipple 1 · arse 1
npc_tam     1,370w   cunt 6 · tits 5 · cock 4 · clit 2 · arse 1
npc_ossie   1,435w   cunt 5 · tits 4 · clit 2 · cock 2
npc_nunn    1,259w   tits 4 · cunt 4 · cock 4 · clit 1 · arse 1
```

Bev's declared ceiling in the Want is not low:

> tier1: *crude ABOUT the drivers, as trade talk across the handover* · tier2: *crude about Robyn to
> her face — tits, cunt, wet, on your knees* · tier3: *cunt, clit, fuck, suck, fingers in her*

Her arc delivers **none of it — not even tier 1.** The doctrine is explicit that the ceiling is
*"a ceiling, never a floor, and writing under it is a defect."*

It matters more than the other five because Bev **is the Want's declared deletion test**: *"Cut Bev
and nothing Robyn does at night gets measured by anyone who understands it."* The load-bearing NPC
is the only one with zero heat.

Related and worth stating plainly rather than as a defect: the heat is overwhelmingly solo.

```
NPC-bound beats   206 · explicit  32 (15.5%)
solo/room beats   811 · explicit 133 (16.4%)
   -> 19% of all explicit beats are NPC-bound
```

The *rate* is even, so no arc is coy — the arcs are simply thin, which is a v0.1 scope consequence
of the deferred fourth rung, not a register failure.

---

# 8 · F8 · Two of eight location descriptions are in the wrong person

**severity** LOW · **layer** GAME · **status** ✅ **FIXED 0.1.1** — both clauses moved to second person; all eight descriptions re-checked.

`[settings] narration_person = "second"`, and six of eight location descriptions honour it. Two do
not, and they are the two most personal rooms, on text the player re-reads every visit:

- **`the_showers`** — *"Cubicle three's lock has been broken since before **she** started…"*
- **`her_static`** — *"Everything **she** owns is in two bags under it."*

(Checked and cleared: the 20 paragraph beats that use "she" without "you" are all about Bev, and are
correct.)

---

# 9 · F9 · The always-visible guidance carries state, not a next step

**severity** LOW · **layer** GAME · **status** ⚠️ **DIAGNOSIS WRONG — see §0a N4**, then ✅ **FIXED 0.1.1** by an engine addition: `[[sidebar_items]] type = "quest_next"`. Three objectives now render in the rail, each with a place, a verb and a counter.

The Quests **page** is excellent (§0). The **sidebar** — what a player sees on every screen — shows
only the card titles:

```
Counter only, hatch down at midnight
Fleece zipped, back to the window
Everything goes through the till
Balances to the penny
```

Four descriptions of how things currently are. None names a place, a verb, or a person. A player who
never opens the Quests page has no direction at all.

Cheapest fix: put the objective line on the chip instead of the title — *"Keep the hatch up past
midnight — the shop — 0/15"* is already written and already correct.

---

# 10 · F10 · The ledger records the opposite of what shipped

**severity** LOW · **layer** GAME (ledger) · **status** ✅ **FIXED 0.1.1** — `overnight_note` rewritten to match the build, and the four `schedule_plan.npc_*` lines still written in the one-row idiom corrected with their actual split rows.

`v2_state.json` → `board.schedule_plan.overnight_note`:

> *"Overnight windows are ONE row — setup.isCurrentTimeSlot handles the wrap explicitly. Verified in
> the-board.md section 2 against generators/v2.py; **do not split 22:00-06:00 into two rows.**"*

The game **does** split them, correctly, on every day-specific window (§0), and that is why all 20
presence probes pass. Only Tam's all-seven-days row is single, which is also correct.

The note is not describing this build. The next release will read it and un-split the rows, and the
symptom — NPCs vanishing at midnight — is one nothing in `gates.py` can catch, because gate 6 checks
that a row *exists*, never that it *resolves at the claimed hours*.

---

# 11 · Checked and cleared — do not re-investigate

- **All 57 `dialog` blocks are correctly attributed.** Recognised block types are `heading,
  paragraph, dialog, thought_bubble, image, video, cascade, group, block_pool, clip`
  (`v2.py:14673`). 0 missing `props.speaker`; they render `Bev:` live.
- **All 92 `conditions` blocks carry `version = "1.0"`.** None fails open.
- **No quest card carries `version = "1.0"`** — the documented quest-evaluator trap is avoided.
- **No adjacent `[group]` blocks** — nothing is silently dead in a merged if/elseif chain.
- **No `lt`/`lte` gates anywhere** (63 `gte`, 3 `is_true`) — no content window a player can pass and
  permanently miss.
- **The two gated choices without `show_when_locked`** are both `blind_spot_found`, set in the
  opening funnel. Hiding a discovery until it is discovered is correct, not an inconsistency.
- **Energy and money are enforced**, and the run cannot brick — see §0.
- **Navigation works.** `Leave The Shop` appearing not to fire was the explorer's text matcher, not
  the game.
- **A floating `-2 Energy` pill near an exit row is not a defect** — it is the effect toast for
  energy just spent. `.nav-cost-tag` renders inside the card; the plain-link exit is a bare
  `[[Leave The Tyre Bay->Location_the_forecourt]]` with no tag.
- **Fill matches the plan.** 37,450 words, mean 4,681, median 3,992, anchor `the_shop` 27.8% against
  a declared 27.1% and a 25% floor.
- **Sentence length passes with no margin** — median 14 words against a ceiling of 14. Know this
  before editing prose.

---

# 12 · What this says about the skill

Four of the ten findings have a SKILL component, and they are the ones that will ship again:

1. **F1 — v2 lost authoring guidance that v1 had.** The divorce from `prompts_v2` was right, but the
   `thought_bubble`/`dialog` shape did not make the crossing. Worth a sweep: what else does v1 teach
   that v2 only mentions?
2. **F2 — the board declared a price and no gate checked it.** `SKILL.md:107` already states the
   standard; the economy gates were built before it and never brought into line. This one cost the
   game its central mechanic.
3. **F3 — a ceiling without a target gets built to.** Gate 20 did its job and the shape did not
   change. Any gate expressed only as a maximum has this failure mode.
   ✅ **Fixed 2026-08-15** — R3 now derives the count from R2b, 8 is named as a backstop, gate 20
   prints `median · N at the cap`, and gate 22 checks the declarable half of R2b. Study 6 in `DOCTRINE_GAPS.md`
   generalised this past menus: three games converged on the skill's numbers rather than their own
   worlds, clearing every floor by 12–97% and sitting on both ceilings at exactly 0%.
4. **F6 — two gates read a declaration as a fact.** Same root as 2, and **still open**: the media
   gates count declared pools without resolving them against disk. Worth noting that fixing F3
   turned up a third instance nobody had looked for — `board.locations[].fill` was an exact
   post-hoc word count in all three games, so gate 1's declared check passed 8/8 everywhere and
   proved nothing. **A declaration only works if it can be wrong**, and that test should be applied
   to every declare-then-check field in the skill, media included.

And the part that is *not* a skill defect deserves saying plainly: **the prose, the pivot
discipline, the heat distribution, the schedule system, the quest cards, the locked door, the
NPC-hub gating and the location-screen size are all correct, and they are correct because the skill
taught them.** `the-surfaces.md` moved the location screens off Steam's shape; R2b's anchoring, which
was written down but never checked, drifted to 41%; and the two things that were never written down
at all — speaker attribution and *charge the obligation you declared* — are the two blockers.

**The pattern is exact: what the skill wrote down and checked, held. What it wrote down and did not
check, drifted. What it never wrote down, broke.**

---

# 13 · What the repair pass added to that pattern (2026-08-16)

The sentence above needs a fourth clause, and it is the worst one.

> **What the skill wrote down WRONG, shipped 105 times across two games — and looked completely
> fine doing it.**

`engine.md:497` discussed `op = "subtract"` as though the engine ran it. Both v2 games written
against that file used it: 35 effects here, 70 in `steam`. Every one does nothing. The TOML is
valid, the build is green, the gates are green, the play-test is green, and the symptom — a meter
that never moves — is indistinguishable from a player who has not moved it. This is a strictly
harder failure than the other three, because a missing rule leaves a gap somebody eventually
notices and a **wrong** rule produces confident, consistent, dead output.

Two other lessons, both cheap and both now doctrine:

1. **A review is a claim, not a fact — including this one.** Re-checking the ten findings before
   editing overturned F2's central claim, corrected F9's diagnosis, corrected F1's count, and found
   two defects (N1, N3) nobody had gone looking for. The skill already says a handback note must be
   verified before promotion; a *review* is the same kind of document and had never been held to it.
2. **Gate 24 failed a game that was doing the right thing.** It walked canvases; the charge lived in
   `[settings.rent]`. Second measured instance of a rule the skill already states — *a check that
   fails a game for obeying the doctrine is a bug in the check* — which suggests the rule is worth
   applying **before** a gate ships, not after it fires.
