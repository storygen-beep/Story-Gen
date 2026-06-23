# NPC introduction — the first encounter as a designed beat

A new character can't just start standing in a hub. **A first encounter is a designed beat**: it carries a
**pretext** (why this meeting happens here, now), **names the NPC on the page**, and **lands the casting hook**
(who they are + what they want, in one charged line) — *then* fires once and opens the repeatable hub.

This file is the **craft standard** for introducing anyone. It sits *on top of* the mechanical on-ramp doctrine,
which it does not replace: the reachability rules (an on-ramp must be ungated, non-lewd, cold-start enterable —
the backwards-on-ramp ban) stay fully intact (`references/lanes.md` Lane 1 + the runtime rendering rules at
`lanes.md:349-359`). What lives here is the **dramatic** layer the skill used to leave out — turning
`npc_intro` from hub-plumbing into a real meeting. Read it whenever you author any NPC's first appearance.

Engine claims are grounded in `apps/game_generation/twee_comprehensive/generators/v2.py`, cited `file:line`.

## The seam with `onboarding.md` (read this first)
The opening funnel also introduces the first NPCs. The split:
- **Met *during* the funnel** (e.g. an owner the player serves in the opening) → introduced **inside the
  opening chain**; `onboarding.md` owns the *placement*, this file supplies the *craft bar* (the meeting still
  names them + lands the hook). No standalone first-contact canvas — the opening *is* their introduction.
- **Met *after* the opening hands over the open world** → a standalone first-contact one-shot (the 7-step
  template below). This file owns it fully.
- **The test:** before the hinge → onboarding places it; after the hinge → npc-intro owns it.
- **Named-in-passing ≠ met.** A character merely *named* in the opening (an offstage boss, an unseen antagonist)
  is world-building prose, not a first meeting. This file governs only NPCs who become **navigable** — who get a
  hub/portrait. Don't build a first-contact for someone the player can't yet go meet.

## Contents
1. The 7-step template (Renner pinned)
2. Choosing the pretext (the ranked default)
3. The forbidden shape — the bare cold-spawn hub
4. The rubric
5. Cheat sheet

---

## 1. The 7-step template

Worked model throughout: **Renner**, `games/vesper/toml_phases/5_scenes.toml:315-346` (`cap_renner_hired`) — a
clean assigned-target → travel → meet entrance. Mirror its shape.

1. **Plant the name before the face.** Name the NPC — and where to find them — *upstream*, before the player
   reaches them, so the entrance pays off an expectation instead of introducing a stranger. Renner is named
   twice before the meeting: on the wall screen in the office, and in the dossier with his situation *and* his
   location ("drinking himself down at a dock bar called the Anchor"). The on-ramp location was then reconciled
   to match the tip that sent her there (`vesper/5_scenes.toml:311-313`). When no upstream plant is possible,
   supply the pretext at the meeting itself (§2).

2. **Stage the meeting with a reason — never a bare teleport-in.** The pretext is a caused arrival: an
   assigned target she travels to, a hub activity that produces the person ("you flash the room — one of them
   comes over"), a third-party broker who vouches, or an ambient face finally promoted to a real meet. The
   encounter answers *why here, why now* before the player asks.

3. **Auto-fire at the reachable, open location.** The first-contact is a one-shot, authored like the boot
   canvas (`lanes.md:349-353`): `is_repeatable=false`, `priority≥9`, `requires_npc` set so it fires where the
   NPC is, **no `npc=`** (an `npc=` one-shot renders nowhere — `renderNpcPortraits` skips non-repeatables,
   `v2.py:4065`), gated on `<arc>_precondition is_true` + `<npc>_met is_false`, **`version="1.0"`** (a
   versionless gate fails open and cold-spawns the beat at game start, `v2.py:3398`). It auto-fires on entry
   (`selectAutoFireCanvasForLocation`, `v2.py:4025`). The on-ramp stays cold-start-enterable — never gate the
   *first* meeting on a stat only that arc raises (the backwards-on-ramp ban, `beat-authoring.md:160`).

4. **Name them on the page + a one-line character read** in the first paragraph. State who they are, their
   state, the angle — render, don't dump: *"Renner's at the end of it — a big man gone soft and sour, three
   drinks into the evening and looking like the fourth won't help."* Where the player can't yet know the name,
   use `speaker="unknown"` — the engine prints **"Stranger:"** until names are exchanged, then switch to the
   NPC speaker (`v2.py:13590-13596`). Description-as-reward, not a stat-block on sight.

5. **Land the hook as a WANT in the first voiced line.** The character's first line states their need or role —
   the Step-3 casting hook spoken aloud (`step-3-casting.md`), not a bio. Renner's refusal-then-hire gives him
   teeth and a transaction: *"Whatever you're selling, I'm broke… Depot. Nine sharp. You're late, you're
   gone."* Close by naming the work-under-the-work so the player knows what the hub is *for*.

6. **Fire once, flip the flag, then open the hub.** The `exit_block` sets `<npc>_opened_up` (a plain author
   flag — one flag is the whole gate) via `flagEffects`. The ongoing **hub** is a *separate* canvas: repeatable,
   `npc=` set (so it renders the portrait), gated on that flag, with a **distinct `name`** from the first-contact
   (a shared name collides in the name-group selector — `lanes.md:358-359`). The one-shot can never repeat; the
   hub can never appear before the meet has fired.

7. **Sequence the cast in waves.** Don't make everyone reachable on Day 1 — stage entrances so each arrival is a
   punctuation mark (immediate cast in the opening; later NPCs earned through story flags). For a **mid-game
   arrival**, the meet-canvas *is* this one-shot, gated on a progression flag — and **withhold the NPC's
   schedule until the meet fires**, because `getNpcsWithSchedules` leaks every scheduled NPC onto the Schedule
   page from Day 1 regardless of unlock (`v2.py:3132-3139`); a schedule given early spoils the entrance.

---

## 2. Choosing the pretext (the ranked default)

When step 1's upstream name-plant isn't available (a peripheral or wave NPC with no natural setup), pick a
pretext. The default ranking, best-first:

1. **Hub-activity-produces-the-meet** — the player's own action at a place she already visits surfaces the
   person (the strongest: the meeting is *caused* by play).
2. **Caused arrival / assigned-target → travel → meet** — a task or lead sends her somewhere and the person is
   there (Renner's shape).
3. **Third-party broker** — an NPC she knows vouches for / introduces the new one.
4. **Ambient-promotion** — a face seen in hub captions ("you keep seeing her around") finally cashes into a
   formal meet that references the prior sightings.

Author's call, but don't stall on it — default to #1 where the geography allows.

---

## 3. The forbidden shape — the bare cold-spawn hub

The anti-pattern: a repeatable hub (`is_repeatable=true`, `npc=` set) whose **base node is the de-facto
introduction**, with no first-contact one-shot gating it. The player walks in and the character is simply
*there*, the hub's first paragraph standing in for a meeting. Worked example of the mistake:
`games/late_shifts/toml_phases/5_scenes.toml:14-35` — Hank's hub opens with *"Hank behind the counter. He looks
up when you come in. He doesn't say anything,"* no entrance, no hook, no `_opened_up` gate. Never ship this.
Every navigable NPC's hub sits behind a dramatized meet (§1.6).

---

## 4. The rubric

Run at Step 6, per NPC (for NPCs met **after** the opening; opening-cast naming is checked once in the
`onboarding.md` rubric — no double count). **Hard gate:**
- **Every NPC hub is gated on an `<npc>_opened_up`/`_met`/`_hired` flag that ONLY a dramatized first-contact
  one-shot sets** — no portrait goes live before the meet has fired (no bare cold-spawn, §3).
- **The first-contact is an auto-fire one-shot** — `is_repeatable=false`, `priority≥9`, `requires_npc`, **no
  `npc=`**, `version="1.0"` gate.
- **A pretext is present** — name-planted upstream, or a staged hub-activity / caused arrival / broker (§2);
  never a bare teleport-in.
- **Name-on-the-page + a hook-as-want first line** — the NPC's opening line states their want/role, not a bio;
  `speaker="unknown"` used wherever the player can't yet know the name.
- **Distinct `name`** on the one-shot vs the hub; the `exit_block` sets the open flag.
- **The on-ramp stays cold-start-enterable** — the first meeting isn't gated on a stat only its own arc raises.
- **Mid-game arrivals withhold their schedule until the meet fires** (no Schedule-page spoiler).

---

## 5. Cheat sheet

- A first encounter is a **designed beat**: pretext + name-on-page + hook-as-want → fire once → open the hub.
  The mechanical on-ramp doctrine (`lanes.md`) stays intact; this is the dramatic layer on top.
- **Seam:** met during the funnel → `onboarding.md` places it; met after → this file owns it. Named-in-passing
  (offstage) ≠ a meeting — only navigable NPCs get a first-contact.
- **The shape:** auto-fire one-shot (`is_repeatable=false`, `priority≥9`, `requires_npc`, **no `npc=`**, gated
  `<arc>_pre is_true` + `<npc>_met is_false`, `version="1.0"`) → sets `<npc>_opened_up` on exit → separate
  repeatable `npc=` hub, distinct `name`, gated on that flag. Renner = `vesper/5_scenes.toml:315-346`.
- **Plant the name before the face**; stage the meeting with a reason; **never a bare teleport-in.**
- **Land the hook as the first voiced line** — a person with a want, not a meter-waiting yes-man.
- **Sequence in waves**; mid-game arrivals withhold their schedule until the meet (else `getNpcsWithSchedules`
  spoils them, `v2.py:3132-3139`).
- **Forbidden:** the bare cold-spawn hub whose base node is the introduction (Hank,
  `late_shifts/5_scenes.toml:14-35`).
