# Growing a system — the pattern menu (reach for it when you feel a gap)

This is **not** a checklist you fill at the seed. You do **not** decide a game's authored systems on day one —
most of them **emerge** once the game is concrete and you've played it and *felt* a gap ("this day is thin,"
"she needs a way to pass as staff," "the fight needs stakes"). That's normal, good design. This file is the
**cookbook you open when the itch hits** — so you grab a proven shape instead of reinventing one live (which is
how the early games burned whole sessions).

> **Distinct from `references/systems.md`.** That file is the five **ENGINE** systems (clothing / rent / phone /
> customization / HUD) — coarse on/off toggles you *can* decide early. This file is the finer **AUTHORED**
> subsystems you *build out of ordinary traits, activities, and gates* as the game grows. They aren't toggles;
> they're patterns.

**How to use one:** pick the recipe that matches the gap, then fold it in through the four mid-stream passes
(`references/run-mode.md` → "Systems grow through iteration"): **what/why/how-it-feels → place it → build green →
fold the ripple back to the book.** Each recipe below is a *starting shape*, not a spec — deepen it as the game
needs. If the system you need isn't here, design it from first principles and **add its recipe here after**, so
the menu grows.

---

## 1. Disguise / cover / identity-access — *pass as someone*
- **When you reach for it:** the fantasy turns on passing — spy, honeypot, undercover, a staff badge, a stolen face.
- **The shape:** the disguise is a `clothing_item`; gate a **location entry** or an **NPC's first-contact door**
  on wearing it. Out of cover → author a **wrong-reaction fallback** (the mark reacts wrong, you're turned away,
  a guard clocks you). The cover gates **access**, never the escalation.
- **The trap:** clothing's two-part rule still holds — **never gate an NPC's arc spine on worn state** (that's the
  backwards on-ramp). The cover gates the *door*; the arc runs on its own trait. → `references/clothing.md`. And
  pressure-test the mark: an insider who'd recognize what she is breaks the premise (`content-framework.md` §1A).

## 2. Capability / skill track — *a stat you train*
- **When:** the game should reward practice — fighting, stealth, a craft, a seduction skill.
- **The shape:** a **Tier-3 custom trait**; a **training activity** raises it on a **diminishing curve with a
  plateau** (big early gains → small near the cap), costing energy + time; gate content on the trait with the
  ordinary `trait` predicate.
- **The trap:** ship the thing the skill **unlocks** in the *same* increment — a bar that gates nothing is the
  loudest dead meter. Clamp it (`references/trait-catalog.md` §4). Often paired with a crawl (#3).

## 3. A crawl / depth meter — *a place you push into by stages*
- **When:** a location explored in escalating stages — a dungeon, a burned yard, a deep dive.
- **The shape:** a **hidden depth counter**; threshold gates unlock deeper actions (slip / fight / grab at
  10 / 25 / 40); a **retreat fallback** at every depth; **depth-keyed auto-fire "finds"** reward progress.
  Usually gated behind a capability (#2).
- **The trap:** give a clear way back out at every depth or you strand the player; the finds must be worth the risk.

## 4. Secondary / closed economy — *a second-life currency*
- **When:** a separate world with its own money — an underworld, a black market, a fae court.
- **The shape:** a **second currency trait**; every **source** (a job, a fight-purse) balanced by a **sink** (a
  toll, a shop); **earned-there / spent-there / worthless elsewhere**; teach it in-fiction at the gate where it
  first matters.
- **The trap:** the default is **one wallet** — a second currency earns its place only for a real second-life
  loop. A source with no sink (or a sink with no source) is a dead meter. → `references/step-2-toplevel.md` §4.

## 5. Consumable / reload upkeep — *a tool with limited uses*
- **When:** a weapon with charges, a supply that depletes, anything you refill.
- **The shape:** a **bounded integer trait**; deplete on use (via `costs` for a location-routed action, a gated
  effect for a node-routed one); refill at a **dedicated station action**. Keep upkeep loops **separate** —
  don't fold a weapon reload into the sleep/shower loop.
- **The trap:** clamp it (`references/trait-catalog.md` §4); spend via `costs`, not a cosmetic effect
  (`references/toml-gotchas.md`). The spend idiom differs by routing — pick one and be consistent.

## 6. Loadout / carry-one-of-N — *pick one tool to carry*
- **When:** the player carries one of several tools at a time (which weapon, which gadget).
- **The shape:** **ONE hidden integer trait** whose value = which tool is carried (one value = mutual exclusion);
  a **free "swap" activity**; gate each tool's use on that trait; gate any **auto-fire capstone on the TRIGGER**
  so it *waits* for the right tool instead of soft-locking.
- **The trap:** you **cannot** add a real equip slot — the engine's clothing slots are a fixed 7 and reject an
  8th. A loadout is a **trait**, not a slot. → `references/trait-catalog.md`.

## 7. Day-depth — *a non-arc daily layer*
- **When:** the day feels thin — "there's nothing to do but grind the main NPC." (The **§2F day-breadth audit**,
  `references/content-framework.md`, is the review-time check that surfaces this *before* ship, not just in play;
  this section is the recipe to fix what it finds.)
- **The shape:** **parallel things to DO** each day that aren't the main climb — a solo activity, a capability
  drill (#2), a second-economy job (#4), an exploration crawl (#3) — each either a real **feeder** (raises a
  player stat toward content) or a **texture beat**. This is the "walk a representative day" breadth the day
  should pass.
- **The trap:** don't add a bar without content behind it. Ship the DO **and** its reward together.

---

**Deepening:** a recipe here is the starter shape. When a game leans hard on one, it earns its own fuller
reference over time (e.g. a dedicated `capability-ladders.md`). Until then, the recipe + the four fold-in passes
are enough to build it right.
