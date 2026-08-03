# Onboarding — the opening that teaches the machine

The opening is a **linear funnel**: a scripted first run that walks the player through the machine *once*, then
opens the world. Every game built with this skill opens this way — it is the only opening shape. (A replay
**Skip Intro** is a fine convenience; it is not a second shape.)

This file owns the half the skill kept *declaring* but never *taught*. Step 2 §8 and the framework §1E already
say the opening must "teach with no tutorial" and pass a "10-minute taste" — that is the **goal**. They do not
say **how**. This file is the how: the authorable method that surfaces each live system inside the funnel, plus
the Step-6 rubric that checks it. Read it when you blueprint the opening (Step 5 Pass 4) and when you author the
opening beats (Step 7).

**Scope — the machine, not the story.** The *story* half of the cold start (who she is, the world, the goal,
the cast named on the page) is already owned by `content-framework.md` §1E and the "name the setup in the prose"
rule in `beat-authoring.md`. This file does not restate that. It owns the **machine**: navigation, the resource
economy, the day-cycle, which systems are live, and the win/fail contract — the things a stranger who skipped
the menus must still learn just by playing the first few screens.

**The law it answers to: teach diegetically, never dump.** No tutorial popup, no static "here are the mechanics"
card. Each system is taught inside a fiction beat at the moment it first matters, or shown on the sidebar where
the player can read it. The register stays RTS-flat (`references/rts-flat-prose.md`) — the funnel is scripted,
not purple.

Every engine claim here is grounded in `apps/game_generation/twee_comprehensive/generators/v2.py` and
`apps/projects/services/template_import.py`, cited `file:line`.

## Contents
1. Why a funnel (and why it's the only shape)
2. The method — the funnel, beat by beat
3. The Step-6 onboarding rubric (hard gate vs advisory)
4. The spine is currency-agnostic (don't hardcode "rent")
5. Anti-patterns + the one sanctioned exception
6. Corpus claims not to re-inherit
7. Cheat sheet

---

## 1. Why a funnel (and why it's the only shape)

A brand-new player knows nothing: not where they can go, not what the bars in the sidebar mean, not that a day
has to be slept through, not which systems are even running. Drop them into a fully-open hub and they learn the
controls by clicking blindly — and the systems you wired carefully stay invisible. The funnel fixes this by
**controlling the first N beats** so each piece of the machine is introduced once, in order, before the sandbox
opens wide.

This is not a size cut. Build the opening at **full designed size** — a 20-node opening is fine; the engine
plays it back beat by beat (§2.1). "Funnel" is about *control of order*, not *brevity*. (The old "test slice"
instinct — collapse the opening to 3 nodes to make it linear — is wrong and banned: the engine already makes a
long chain play linearly.)

The funnel ends at one clean hinge: the beat that sets the opening-done flag and hands the player the open map
with a named next action waiting (§2.5).

---

## 2. The method — the funnel, beat by beat

### 2.1 Build the opening as a node-chain at full size
The `starting_canvas` is a **required** artifact — the importer hard-errors if `[project].starting_canvas`
names a canvas that doesn't exist (`template_import.py:6126-6130`, `starting_canvas` not-found raise). Author it at full size; its nodes play back
as a chain of single-Continue passages on their own (`v2.py:11497` `_build_node_chain`, `12350-12352` single-Continue node exit). You do not collapse the
design to make it feel linear — the chain *is* linear.

### 2.2 Split the boot from the capstone
Two canvases, not one:
- a tiny **boot** one-shot (`is_repeatable=false`, high `priority`, gated on `<opening>_done is_false`) that
  drops the player at the start location and exists only to begin the chain;
- a separate **opening capstone** (gated on the same flag) that spends the Tier-3 prose on the cast + the
  stakes.

The flag gate guarantees order without a schedule. Both auto-fire on entry via
`selectAutoFireCanvasForLocation`, which fires the highest-priority non-repeatable valid canvas and skips
repeatables (`v2.py:4161-4181` `selectAutoFireCanvasForLocation`). (Worked pattern: `the_inheritance/2_one_shots.toml`.)

### 2.3 Arm each live system once, inside a fiction beat (surface-once)
Walk the chain and wire **every switched-ON system** to a story beat at its first point of relevance — the
player meets the mechanic and the reason for it fused, never a cold rule:
- **the economy** — name what the currency buys the first time it matters (DoL arms its rent mechanic *inside
  Bailey's speech*; Late Shifts arms economy + phone *inside the hire scene*);
- **a rent/debt clock** — arm it with `[settings.rent].start_after_flag` set to a flag the opening raises
  (`template_import.py:329`, `2405`, `5742`; `last_call/0_systems_spec.toml:127` uses
  `start_after_flag="debt_explained"`), so the first session is **pressure-free** — no collector knocks, no
  debt modal fires turn one, before the player has been taught the rules;
- **phone / clothing / customization** — each gets one beat that proves it exists (the phone buzzes once; she
  changes for the first time; the customizer speaks her name back).

The rule: **a system the player never sees taught is a system you might as well not have wired.** One beat each.

### 2.4 Pre-populate the sidebar at value-zero
The sidebar is the **persistent tutorial** — it replaces a teach screen forever after. On frame one, every live
system shows as a banded item with a visible ceiling:
- a stat band — `trait_bar` (`v2.py:15240`) or `trait_words` (`v2.py:15350`) — reading near-empty against its
  max ("Corruption 0/45"); the empty-bar-with-a-ceiling **is** the "there's a climb ahead" read;
- the per-NPC `npc_panel` House-card (`v2.py:15411`) listing the cast and their meters.

Encode each stat by the right primitive (`references/hud.md`, `trait-catalog.md` §5). The whole machine should
be legible at a glance from the first screen.

### 2.5 Name the next action on frame one
The player must never be handed an empty open hub. Give the spine a **quest card** with `goals` +
`ready_canvas` + `tip` populated; the engine derives the self-updating 🎯→🔓→✓ "what next / where / when"
surface from them (`template_import.py:938-968`; `v2.py:14217-14267` `renderQuestsGoalBlock`). The `tip` states the loop in plain words
("Work his depot to earn the office — that's how you get in"). There is always exactly one obvious thing to
click. This is what kills cold-start paralysis.

### 2.6 Make the earning loop the first repeatable action, taught by play
The first repeatable thing the player can do is the core earning loop — a solo work activity with **energy as a
per-choice cost** (deducted and dimmed on entry) and **money as an effect**, plus **one locked-visible
escalation rung** (`show_when_locked` with `locked_text`). Through one button the player learns the whole
gate-grammar: spend → earn → a tier is locked → here's what unlocks it. Because the income path *is* the content
path, "go make money" is indistinguishable from playing the game (`last_call`; `references/lanes.md` Lane 3).

### 2.7 Teach the day-cycle by necessity, not by lecture
There is **no "jump to morning" primitive.** `advanceTime(minutes)` is the only time mutation, and
`advanceDay()` / the daily tick fire *only* when minutes roll past 24h (`v2.py:5094-5142` `advanceTime`/`advanceDay`; the roll-over loop is
`5105-5108` (`while current_hour >= 24 → advanceDay()`), `advanceDay` at `5127`). So the day-cycle teaches itself: ship the sleep activity as the
day-router — a time cost large enough to roll past midnight, energy restored on exit — and the player who crashes
after the first night *must* sleep to reach the next day's content. Self-explaining. (It also prevents the
dead-window bug where a needed NPC is only present at a time the player can't reach.)

### 2.8 Surface why-locked everywhere a gate shows
A gate the player can **see the reason for** is a goal; a gate with no reason is a dead end. Every locked thing
states why:
- a teased rung → `locked_text` on a `show_when_locked` choice (`v2.py:12013-12015`) — the in-world tease ("She'd
  never let you do that sober");
- a too-expensive action → the cost message via `getCostBlockedMessage` (`v2.py:12009`) ("Requires 15 Charge —
  you have 6");
- a place she can't enter yet → `blocked_message` on the greyed nav card (`v2.py:4465` `navDestBlockedReason`) ("You don't know where
  he went — yet").

### 2.9 State the win/fail contract up front — and the sandbox contract
The opening names what winning and losing look like. Step 2 §8 §1C already declares **whether** failure exists
(a forward-only ratchet is legitimate, but *on purpose*); the funnel's job is to **surface that declaration to
the player** — RTS-style honesty ("this is a grind/sandbox; here's the climb, here's what bites if you let it").
A player who doesn't know whether anything can go wrong can't read the stakes.

Two siblings of the same honesty, both from the 2026-07 top-30 mopoga study's winners:
- **The sandbox contract on the first screen.** The #1 game by engagement (Apocalyptic World) opens with the
  promise stated flat: *"You want to be a farmer, a trader, a bounty hunter, a cage fighter, a warlord — or
  something far darker? The choice is yours"* … *"Play at your own pace — the world keeps going either way."*
  One or two lines of what-you-can-become + the-world-moves; it frames every system the funnel is about to
  teach. Ours rides the **title/boot screen** — an out-of-fiction surface the player crosses before the
  fiction starts (§5 sanctions exactly this surface; the contract line must never leak into the prose).
- **Announce the content ceiling early — at PREMISE level, never arc register.** The same game puts an "Eat
  your grandfather" fork BEFORE free-roam: the darkness is shown, not sprung, so the player who stays has
  opted in. This is `content-framework.md` §1D's "content the player should know is coming" made into a
  funnel beat. Scope it to the **premise's** darkness (what kind of game this is); do NOT demonstrate any
  arc's gated vocab register early — that is the tier-linear leak `kink-ceilings.md` §4/§8 forbids (AW's fork
  is premise-level cannibalism, not a corruption arc's crude register). A beat touching a kink area whose
  ceiling row is blank doesn't ship until the ceiling is declared (`kink-ceilings.md` §3).

### 2.10 If there is a chargen, every pick pays
Course of Temptation's opening is a character sheet disguised as a story: each backstory pick is an archetype
card with **visible stat grants** ("Dated Innocently — Sexual Knowledge+1 Disinhibition+1 Hand+1"), the
sexual-history pick sets the starting sex-skill values, and body customization is **diegetic** — a mirror scene
with inline pickers, not a form. The rule: a chargen pick that changes nothing is a form field; every pick
either pays mechanically, sets a starting state, or declares a content preference — and SAYS so where the pick
is made. **The mechanism split (ours):** stat-granting picks are ordinary **funnel choice-beats with
`effects`** (a lifepath is scripted scenes, fully supported today); the **customize screen's fields**
(`references/customization.md` — `text`/`select`/`image_select`) write identity values (`$player.<id>`,
spoken back as `@`-tokens) and cannot grant stats — so anything that should PAY belongs in a beat, not the
form. Don't bend the customize screen into a stat allocator; put the paying picks in the fiction.

---

## 3. The Step-6 onboarding rubric (hard gate vs advisory)

Run this at Step 6 against the blueprinted opening. The **hard-gate** rows fail the review if unmet — fix before
authoring. The **advisory** rows are judgment, flagged not blocked.

**Hard gate (fail = don't ship):**
- **Every live system is surfaced once** — for each system declared ON at §8 (economy, rent/debt, clothing,
  phone, customization, day-cycle, each HUD band) there is either a named opening beat that arms it (§2.3) or a
  sidebar item at value-zero on frame one (§2.4). One checklist row per system; none cold.
- **A named next action on frame one** — the spine quest card has `goals` + `ready_canvas` + `tip` populated,
  or the start hub's prose names the literal next click (§2.5). Never an empty hub.
- **No greyed gate without a reason** — every `show_when_locked` rung has `locked_text`, every cost-blocked rung
  shows its cost, every locked nav card has a `blocked_message` (§2.8).
- **All condition blocks carry `version="1.0"`** — a versionless `conditions` object **fails open**
  (`triggerConditionsSatisfied` returns true, `v2.py:3534`), so a gate you think you set cold-spawns its beat
  at game start. Every trigger/choice/group/substitution condition needs the version.
- **Onboarding canvases sit on a NON-container hub** — an `is_container` location swallows attached canvases
  (`template_import.py:3506`), so a boot/opening canvas on a container goes dead. Anchor them on a standing hub.

**Advisory (flag, don't block):**
- The opening is a full node-chain, not a 3-node cut of a larger design (§2.1).
- The day-router proves the dead-window can't happen — a daytime-only presence is reachable only after sleep
  (§2.7).
- The Day-1 content budget feels like a taste of the core charge, not just chores (a tunable target — see §6).
- **First lewd content is reachable within ~15 clicks on the recommended path** (opt-in is fine; hidden is not).
  The study's winners front-load: CoT offers a full optional encounter ~12 clicks in and an explicit beat ~30;
  Apocalyptic World's first lewd verb lands at ~14. A funnel that stays cold past its first sitting teaches the
  player the game is cold. (A stricter onboarding-side cousin of Rule 9's "**A floor, not a quota**" —
  `rts-flat-prose.md` §3. That floor also passes charged slow-burn TEXTURE with no early lewd beat; this row
  only asks that something lewd be *in reach*, opt-in, for the player who goes looking. A slow-burn game that
  charges its funnel hot and offers a solo valve passes both.)
- **The sandbox contract rides the title/boot screen**, and one early beat touches the premise's darkness —
  at premise level, never an arc's gated register (§2.9).
- **Every chargen pick pays** — stat-paying picks live in funnel choice-beats with `effects`; the customize
  screen carries identity only (§2.10).

---

## 4. The spine is currency-agnostic (don't hardcode "rent")

The first pressure the opening arms is **the spine's first pressure, whatever its currency** — not always rent.
Most economic-pressure games use a rent/debt clock (RTS, DoL, Last Call), but the same method applies to any
spine: a **control economy** (`the_inheritance` runs rent OFF and pressures the player through Margaret's scheme
instead), a status/career clock, a captivity/prey spine. Arm whatever the game's first pressure is, after the
opening sets its flag (§2.3). Don't read "rent" as mandatory; read "the first thing that squeezes."

---

## 5. Anti-patterns + the one sanctioned exception

- **The static mechanics-teach card is the dump-shape we don't use.** A screen that lists "here's how energy
  works, here's the map, here's the day-cycle" is the tutorial-wall this whole file exists to avoid. Surface
  each system in a fiction beat (§2.3) or on the sidebar (§2.4) instead. (The RTS `GameMechanics` card is the
  thing *not* to copy.)
- **Two sanctioned out-of-fiction surfaces — and only these two.** (1) The quest-card `tip` (§2.5) may speak
  plainly in system-voice ("Deposit at the bank to grow the fund"). (2) The **title/boot screen** — already
  out-of-fiction (disclaimer, Start) — may carry the one-line sandbox contract (§2.9). Neither voice ever
  leaks into the prose; a mechanics LIST on the title screen is still the banned dump-shape (the contract is
  a promise, not a manual).

---

## 6. Corpus claims not to re-inherit

The deprecated corpus has onboarding craft worth lifting, but check it against the engine — it has a history of
inventing facts:
- **"Any triggerless canvas auto-fires" — FALSE.** Only the `starting_canvas` is special-cased to open the
  game; a normal triggerless canvas does not auto-fire. Auto-fire is `selectAutoFireCanvasForLocation` picking a
  non-repeatable, high-priority canvas on entry (`v2.py:4161`). Build the opening capstone as that shape (§2.2),
  not as "a canvas with no trigger."
- **The quantified Day-1 budget is an observation, not a law.** The corpus's ">=2 Lane 2 encounters + >=1
  Tier-3 intro + 1 taboo beat in the first 30 minutes" is an RTS live-log reading, not an engine guarantee.
  Treat it as a tunable target to audit against (the advisory rubric row), never a hard gate.
- **Use the real economy keys.** When wiring the economy into the opening, use `[settings.rent].start_after_flag`
  / `eviction_mode = "flag_set"` — not the corpus's fictional `rent_text = {paid, late, evicted}` keys (already
  corrected; the real shape lives in `references/rent.md`).

---

## 7. Cheat sheet

- The opening is a **linear funnel**, the only shape. Build it at full size; the engine plays the chain
  linearly. Skip-Intro on replay is fine.
- **Boot** one-shot starts the chain + sets the done-flag; a separate **capstone** spends the prose. Both
  auto-fire, gated on the flag.
- **Arm each live system once, inside a fiction beat.** A system never taught is a system wasted. Rent/debt
  armed via `start_after_flag` so turn one is pressure-free.
- **Light the sidebar at value-zero on frame one** — the empty bar with a ceiling is the "climb ahead" read;
  the sidebar is the permanent tutorial.
- **Name the next action on frame one** — quest card `goals`+`ready_canvas`+`tip`. Never an empty hub.
- **Earning loop = the first repeatable action**, teaching spend→earn→locked-tier through one button.
- **Day-cycle teaches by necessity** — sleep is the only way past 24h; no jump-to-morning exists.
- **Every gate states its reason** — `locked_text` / cost message / `blocked_message`.
- **State the win/fail contract** in the opening (§8 §1C declares whether failure exists) — plus the
  **sandbox contract** on the title/boot screen and one early beat touching the **premise's darkness**
  (premise level, never an arc's gated register — §2.9).
- **Every chargen pick pays** — paying picks are funnel choice-beats with `effects`; the customize screen
  carries identity only (§2.10).
- **First lewd within ~15 clicks** on the recommended path (advisory row — the stricter onboarding cousin of
  Rule 9's "a floor, not a quota").
- **Hard-gate rubric:** every system surfaced · named next action · no reason-less gate · every condition
  `version="1.0"` · onboarding canvases off containers.
- The first pressure is **whatever the spine's currency is** — not always rent.
- Don't ship a **static teach card**; the quest-card `tip` is the one sanctioned system-voice line.
