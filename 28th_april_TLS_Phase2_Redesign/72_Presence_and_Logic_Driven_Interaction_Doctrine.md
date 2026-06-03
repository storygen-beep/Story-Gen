# Doc 72 — Presence Acknowledgement & Logic-Driven Interaction Doctrine

**Date:** 2026-05-31
**Status:** Active doctrine
**Sibling docs:** Doc 24 (3 Lanes), Doc 56 (RTS Principles + Alignment — R1 constant hub openings), Doc 49 (Story Goals vs Sidebar), Doc 67 (Solo Activity + Multi-NPC Dispatcher)
**Triggered by:** The Weekly Schedule page fix (2026-05-30) made every NPC's whereabouts honest from day one — which exposed that a player can stand in a room with a present NPC and get *nothing*, because the NPC's whole arc is gated behind escalation flags. Same root cause as the "corruption 0→5 is too thin" observation: the world has presence but no floor.
**Scope:** How a player's *visit* to a place where an NPC is present should behave. Governs the relationship between **presence** (the schedule — where the NPC is) and **interactability** (what the player can actually do there). Applies to every hub/ambient canvas with a scheduled NPC in a reachable location. This is a **design-judgment** doctrine, not a quota.

---

## §1 — Why this doc exists

**One-line rule: the door is always open; what's behind it follows the logic of the relationship.**

Two systems were getting conflated. **Presence** is where an NPC is at a given time — it comes from `[[npcs.schedules]]` and is independent of the player's progress. **Interactability** is what the player can *do* when co-present — it comes from canvas gates. The defect: we were gating *interactability* so hard that it swallowed *acknowledgement*. A new player walks into her own kitchen, her housemate is standing right there per his schedule, and the game shows her nothing — because every authored beat for him needs the arc to already be running, and the arc's on-ramp needs a stat she can only raise through content she can't reach yet.

That is backwards. Cohabitation, neighbours, coworkers-on-site — these produce ordinary contact *first*, and escalation grows out of it. This doc fixes the framing without swinging to the opposite error (a dumb "every NPC must have an ungated action" quota). The fix is judgment: **presence is always acknowledged; the actions available follow in-world logic.**

This is the enforcement Doc 56 R1 implies but does not state. R1 says the hub *opening prose* shouldn't vary by progression. R72 says the opening must *exist at all*, and the choices on top of it layer by logic.

## §2 — Definitions

A hub or ambient canvas has two layers:

- **Base content** — the `base` node. Renders on every visit, regardless of player stats or flags: an image, a line of ambient prose describing what the NPC is doing in the space, optionally one line of dialogue. This is *acknowledgement* — "you are here, they are here, this is the moment."
- **Choice layer** — the `exit_block.choices`. Conditional. Each choice carries its own `conditions` / `show_when_locked`. Some are open immediately; some are locked-visible (published but gated); some are absent until earned.

**Base content + an exit, with zero choices, is a complete and valid canvas.** A canvas does not need a choice to justify its existence. It needs only to acknowledge the moment and let the player leave.

## §3 — Presence is acknowledged

If an NPC is present somewhere the player can already reach, visiting that place must always *show something* — the base moment. Never a dead, empty room; never a silent "nothing happens"; never a screen that reads as though the NPC isn't there when the schedule says they are.

This is the real **floor**. The floor is *acknowledgement*, not a forced action. It is the thing that makes the world feel alive between escalation beats. Whether there is anything to *do* on top of it is a separate, logic-driven question (§4).

> **Evolution (2026-06-02).** This doc originally let either a hub *or* a Lane 2 ambient base carry the floor, by judgment. That is now hardened: the floor must be a **Lane 1 hub, per schedule row** — a Lane 2 ambient is a dice roll (`chance` ⇒ nothing on most visits) and cannot be a floor. The *choices* on a hub remain logic-driven (R2/R3 unchanged — no choice-quota); only the *floor mechanism* became a hard, checkable requirement. Three new rules formalize it: **R6** (per-row Lane 1 hub coverage), **R7** (a hub's escalation ceiling = location exposure, not time), **R8** (same-NPC hub consistency). The corpus home for R6–R8 is `prompts_v2/doctrine/04` §6 + `doctrine/02` §2.8–§2.9. The "no engine linter" stance in §10 is relaxed for the floor: per-row hub coverage is exactly the kind of check that *should* be mechanized; the choice-quota stays rejected.

## §4 — Rules

### R1 — Presence is always acknowledged

When the player visits a location where an NPC is present, the canvas's base content renders, regardless of stats or flags. A choice-less base + exit is valid and sometimes correct.

*Why this rule exists:* The schedule page now tells the player exactly where everyone is. If the player acts on that information — walks to where the NPC is — and the game shows nothing, the schedule is exposed as a lie and the world reads as dead. Acknowledgement is cheap and it is the difference between "a populated world" and "a set of locked doors."

*How to apply:* Author the `base` node first and unconditionally — image + one ambient paragraph of what the NPC is doing (folding laundry, wiping the counter, reading on the couch) + optionally one line of dialogue. Do not gate the base node behind escalation flags. Gate *escalation choices*, never the act of seeing the NPC.

*Worked example:* The player visits the laundry room at a time the housemate is scheduled there. Base renders: *"X is feeding sheets into the dryer, sleeves shoved to the elbow."* Exit: "Head back." That alone is a finished canvas. Nothing forces a deeper interaction into existence.

### R2 — Interaction is logic-driven, not quota-driven

The choices available on top of the base appear by the logic of the situation — some open now, some earned later, sometimes none. There is **no requirement that every NPC offer at least one ungated action.** "Sometimes none" is a legitimate, correct outcome.

*Why this rule exists:* The opposite error to dead presence is mechanical quota-stuffing — bolting a hollow "Talk" onto every NPC so a checklist passes. That produces texture-less filler and is exactly the format-driven thinking this doc rejects. What belongs on a canvas is what the fiction supports right now, no more and no less.

*How to apply:* For each potential action ask "does this make sense, here, now, given where the relationship is?" If yes and nothing in-world forbids it → it's open. If it only makes sense after something has happened → gate it. If nothing extra makes sense → base + exit, done. Never add a choice solely to avoid an empty choice list.

*Worked example:* At the laundry hub, "Help him fold" makes sense immediately (helping a housemate with chores needs no permission) → open. A flirtatious move only makes sense once there's a charge between them → gated. On a given visit where neither applies, the canvas is just the base moment, and that is fine.

### R3 — Gate for an in-world reason, not by reflex or format

Lock a choice when there is a fiction reason it isn't available yet. Do **not** withhold a naturally-available action just because the arc "hasn't officially started," and do **not** lock *acknowledgement* (the base moment) behind escalation stats.

*Why this rule exists:* The Late Shifts defect was reflex-gating: the housemate's entire presence sat behind his escalation flags, so the most natural thing in the world — greeting someone you live with — was impossible until the arc was already deep. Gating should encode in-world truth ("he wouldn't do that until he trusts her"), not authoring convenience ("stage 1 comes before stage 0 because that's the template").

*How to apply:* Before adding a gate, name the in-world reason out loud. "He wouldn't proposition his housemate on day one" is a reason. "Because it's the lowest stage" is not. If you can't name a fiction reason, the action is probably an open one.

*Worked example:* "Greet him / help with the dishes" — no fiction reason to lock; open from a cold start. "Press up against him at the sink" — fiction reason exists (no charge yet); gated. The acknowledgement that he is *in the kitchen at all* is never gated.

### R4 — Every arc has a cold-start on-ramp

An arc must be enterable from a cold start — corruption 0, no flags set — through ordinary life. An arc must never require, as its entry condition, a stat or flag that can only be raised by content the cold-start player cannot yet reach. This is the **backwards on-ramp** and it is banned.

*Why this rule exists:* If the front door to an arc is locked with a key that's inside the room, the arc is unreachable from a fresh save and the player stalls staring at locked affordances. This is the structural twin of the "corruption 0→5 is too thin" problem — both are "the world has no floor, only a ceiling."

*How to apply:* For each arc, trace the literal first beat a brand-new player could trigger. It should be reachable by being in a place at a time, nothing more. Escalation conditions layer *after* that first beat. If the earliest beat needs a stat, ask where that stat comes from — if the only source is downstream of this arc, you have a backwards on-ramp; add an ordinary-life entry beat.

*Worked example (anti):* The Late Shifts housemate's arc opened only at `worn_corruption ≥ 15` — i.e. the player had to buy and wear provocative clothing before her own housemate would register her. The on-ramp should instead be an ordinary shared-kitchen moment that needs only co-presence; the clothing-driven escalation belongs further up the ladder.

### R5 — Location-entry gating is legitimate when entering IS the first contact

Gating an entire location behind a flag is fine when *walking into that place* is itself the first interaction with what's there. The rule targets people already embedded in the player's everyday space — housemates, neighbours, coworkers once she's on-site — not destinations the player has no reason to be inside yet.

*Why this rule exists:* "Presence floor" is about people who are unavoidably in the player's orbit. It is not a mandate that every location be open from minute one. The diner behind "get hired" is correct: the player has no standing to be behind the counter until hired, and the act of walking in to ask for the job *is* the first contact. Forcing ungated diner-employee activities pre-hire would be nonsense.

*How to apply:* Ask "does the player share this space as a matter of daily life?" If yes (home, building, workplace-on-shift) → presence must be acknowledged (R1) and the arc needs a cold-start on-ramp (R4). If no, and entering is the first contact (a job not yet held, a home not yet visited) → location-entry gating is legitimate and R1/R4 apply only *after* entry is unlocked.

*Worked example:* Housemate in the shared kitchen → daily space → must be acknowledged from day one. Diner floor before being hired → entering is first contact → the hire scene is the on-ramp; locking the rest until `hired_at_diner` is correct.

### R6 — Every schedule row has a live Lane 1 hub (2026-06-02)

For every `[[npcs.schedules]]` row an NPC has — each (location × time-window × weekdays) — there is a Lane 1 hub whose own `trigger.schedules` covers that window. The hub's `base` renders unconditionally (the floor). A Lane 2 ambient does **not** satisfy it (dice roll). Multiple windows at one location = separate hub canvases (period-split, Doc 56 R1).

*Why:* the engine renders a hub portrait only when the hub's own `schedules` is live AND the NPC is present (`isCanvasValid` `v2.py:4356` + presence gate `v2.py:4384`). Late Shifts authored hubs for narrow arc windows while scheduling the NPC present far wider; a per-row audit found 13 of 22 rows dead — the schedule page promised a body the room didn't deliver.

*How to apply:* list the rows; confirm a hub whose window covers each. "A hub at the location" is not enough — it must be open at that time. *Corollary:* a schedule row is a promise of a hub — a pure rent/phone "system" NPC (landlord) carries no schedule row.

### R7 — A hub's escalation ceiling = location exposure, not time

Which rungs a hub may offer is set by the **exposure** (privacy) of the location at that window — who can see, what's at risk — not by time. Public → talk/look only; semi-private → tease/grope (sex gated or interrupted); private → full ladder (private can be several locations). Relationship state (corruption/relation/stage, global) unlocks within that ceiling. Time and co-present NPCs are *inputs to exposure* (an after-close diner is private), not the gate.

### R8 — An NPC's hubs are mutually consistent

Relationship state is global (no per-location re-grind); voice + rung names + gate thresholds stay consistent wherever a rung appears; the full ladder appears wherever it's private; the ladder is context-scaled, **not cloned** into rooms whose exposure can't support it. Optional: locked-visible higher rungs at public hubs for telegraphing, unlockable only where private.

## §5 — Decision test (T1–T3)

Run per NPC, per location, when authoring:

- **T1 — Reachable before the arc starts?** Can a cold-start player stand where this NPC is, before any of their flags are set? If **yes** → the base moment must render there (R1). If no → R5 may apply (entry is first contact).
- **T2 — Does this action need a reason to be locked?** For each candidate choice, name the in-world reason it isn't available yet. No nameable reason → leave it open (R3). Reason exists → gate it. No sensible action at all → base + exit (R2).
- **T3 — Can the arc be entered from a cold start?** Trace the earliest triggerable beat. If its condition is downstream of the arc itself → backwards on-ramp; add an ordinary-life entry beat (R4).

## §6 — Canonical worked example: the laundry hub

Player goes to the laundry room. The housemate is scheduled there this hour.

- **Base (always):** image + *"X is folding shirts at the dryer, a basket balanced on the lid."* Exit: "Head back upstairs." → This is a complete canvas on its own. (R1)
- **Open choice (cold start):** "Help him fold." Helping with chores needs no permission and no charge — it's the kind of ordinary contact cohabitation produces. Available from the first visit. (R3)
- **Gated choice (earned):** a flirtatious or charged move — only surfaces once the relationship has a charge (a flag/stat set by prior beats). Locked-visible per Doc 56 R2 if you want to publish that it's coming. (R2)
- **None applies:** on a visit where the player has no reason to help and the charge isn't there, the canvas is just the base moment + exit. Correct, not a gap. (R2)

The point is the *layering*, never a count. The base acknowledges presence; "Help him fold" is open because the fiction allows it; the charged beat is gated because the fiction requires it; and an empty choice list is a valid state, not a failure.

## §7 — Relationship to the lanes

This doctrine sits underneath the Lane model (Doc 24), it does not replace it:

- **Lane 1 (hub):** the base node is the hub opening, and it **is the floor** (R1 + R6 — the opening exists, acknowledges presence, and is present for every schedule row). Doc 56 R1 = "the opening prose doesn't vary by progression." Sibling rules — floor, coverage, constancy.
- **Lane 2 (ambient):** ambients are **texture layered on top of the hub**, not the floor (post-2026-06-02, R6). They make presence feel *alive* between escalation beats, but because they are dice rolls they cannot *acknowledge* presence on their own — that is the hub's job. An ambient that renders only when escalation conditions are met is dead presence by another name; an ambient relied on *as* the floor is dead presence ~3 of 4 visits.
- **Lane 3 (substitution) / Lane 4 (capstone):** unaffected — these are by definition earned, gated content. The floor is about the base layer beneath them.

## §9 — Anti-patterns

- **Dead presence.** NPC is scheduled at a reachable location (and now shows on the schedule page), but visiting yields nothing — no base moment, no acknowledgement. The world reads as a set of locked doors. (Violates R1 / R6.)
- **Hub window narrower than the schedule.** A hub exists at the location but its own `trigger.schedules` covers only part of the NPC's scheduled presence there; the rest of the rows are dead (Hank: hub open 22:00–01:30, scheduled 06:00–22:00). Period-split into per-window hubs. (Violates R6.)
- **Lane 2 used as the floor.** Relying on a `chance` ambient to acknowledge a scheduled NPC — dead presence on most visits. Author the hub. (Violates R6.)
- **Physical schedule on a hub-less system NPC.** A rent/phone-only NPC carrying a schedule row advertises a body the world can't deliver. Drop the schedule or give them a hub. (Violates R6 corollary.)
- **Cloned full ladder / public-space escalation.** The same full ladder offered at every hub regardless of context ("Have sex" at a public counter). Scale the rung set to the location exposure tier. (Violates R7 / R8.)
- **Backwards on-ramp.** An arc's entry condition is a stat/flag that can only be raised by content downstream of that same arc. The cold-start player can never begin it. (Violates R4.) *Example:* housemate arc gated on `worn_corruption ≥ 15`.
- **Escalation-only authoring.** Writing only stage-1+ beats for an NPC and never the stage-0 base moment — so the NPC simply doesn't exist to a new player. (Violates R1 + R4.)
- **Quota / format enforcement.** The opposite error: bolting a hollow ungated action onto every NPC to satisfy a checklist. This doc explicitly rejects "every NPC must have ≥1 ungated interaction." Acknowledgement is required; an *action* is not. (Violates R2.)

## §10 — Scope & non-goals

- **No *choice* quota.** There is no minimum interaction-count on a hub's menu; actions are by judgment (R2). What is hard is *floor coverage*: a Lane 1 hub per schedule row (R6). The two are different axes — "every row needs a hub" is not "every hub needs an ungated action."
- **Engine linter (revised 2026-06-02).** The originally-dropped validator targeted a *choice*-quota ("scheduled NPC with no ungated canvas → warn") — that stays dropped, it re-encodes quota thinking. But **per-row hub coverage (R6) is a legitimate, checkable rule** a future validator *should* enforce ("schedule row with no hub whose `schedules` covers it → warn"). The floor is mechanical; the choices stay editorial via §5's decision test.
- **Applies to** schedule-present NPCs in spaces the player shares as daily life (home, building, workplace-on-shift).
- **Out of scope:** locations where entering is itself the first contact (jobs not yet held, places not yet visited) — see R5.

## §11 — References

**Sibling docs:**
- Doc 24 — RTS Three Lanes. The Lane model this doctrine sits beneath (§7).
- Doc 56 R1 — "Lane 1 hub openings stay constant within a canvas." The constancy rule; Doc 72 R1 is its floor-side sibling (the opening must *exist*, not just stay constant).
- Doc 49 — Story Goals vs Sidebar. Complementary: where NPC state is surfaced vs. what the player can do about it.
- Doc 67 — Solo Activity + Multi-NPC Dispatcher. Lane 3 dispatch surfaces, which ride on top of the base layer this doc governs.

**Memory:**
- Late Shifts built end-to-end (2026-05-29) — the game whose pre-hire start exposed the defect.
- Schedule page declared-data fix (2026-05-30) — surfaced honest presence, which made dead presence visible.

**Shared root:** the "corruption 0→5 is too thin" observation is the same disease from another angle — an arc with a ceiling but no floor. R4 (cold-start on-ramp) is the structural fix for both.

**Deferred follow-ups (not in this doc's pass):**
- Fold a logic-first version into the prompts_v2 corpus (`doctrine/02` near Lane-2/arc-flow + an anti-pattern line in `doctrine/07`), then regenerate `COMPREHENSIVE_SYSTEM_REFERENCE.md`. Phrase as judgment, not a quota.
- Late Shifts NPC-by-NPC audit + author the missing base moments (housemate, neighbour) so the live game demonstrates the doctrine.
