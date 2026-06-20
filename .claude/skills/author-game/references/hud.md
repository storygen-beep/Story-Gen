# The HUD — the sidebar IS the world model

Read this when you place an NPC on the sidebar, wire the RTS House-card (`npc_panel`), or decide WHICH of
an NPC's traits the player gets to see. This file owns the **NPC-panel + per-arc-shape VISIBILITY** layer.
For the PLAYER stat → sidebar-primitive encode-by-type mapping (corruption→`trait_words`, arousal→`trait_bar`,
the doubling trap) it does NOT restate that — it lives in `references/trait-catalog.md` §5; cross-link there.

**Every engine claim here is verified against live code** (`v2.py` = comprehensive generator;
`template_import.py` = importer/validator), cited `file:line`. Where the old corpus drafts disagreed with the
code, **the code wins** and the divergence is flagged inline `*(code-vs-lore note: …)*`.

## Contents
- §1 — The design intent: the HUD exists so the player can PLAN Lane 3
- §2 — The `npc_panel` House-card (the per-NPC radar)
- §3 — Per-arc-shape sidebar VISIBILITY table (which NPC axes surface)
- §4 — Body-state vs progression surfacing + the away/offscreen label
- §5 — The global-hidden-name trap (npc_panel rows are hidden by NAME, not per-NPC)
- §6 — Authoring checklist + pointers (don't duplicate)

---

## §1 — The design intent: the HUD exists so the player can PLAN Lane 3

**The right sidebar is the world surfaced to the player — not chrome, a planning instrument.** Lane 3 is the
dispatcher: the player does a chore (shower, tea, dishes) and an NPC *happens* (`references/lanes.md`). That
texture only works if the player has the situational awareness to pick the chore *knowing* it might collide
with him. The sidebar is where that awareness lives. Without a per-NPC location/arousal radar the player
can't answer the only questions Lane 3 asks:

- "If I shower now, will he walk in?"
- "He's in the kitchen — should I go make tea?"
- "Wash dishes now, or wait until he's home?"

The mechanism still fires (the dice roll is inside the chore), but **the player can't predict or seek it** —
Lane 3 becomes undiscoverable. So the rule:

> **Surface each in-scope NPC's location (and, per arc shape, his arousal) so the player can decide WHERE and
> WHEN to act.** That is the whole job of the NPC panel. Energy + hygiene surface for the same reason on the
> player side — they're the body-state gates the player plans self-care around (`references/trait-catalog.md` §4).

The HUD does the heavy lifting: each click stays light in prose (RTS-flat, `references/lanes.md`) precisely
*because* the sidebar is carrying the world state the click would otherwise have to re-describe.

---

## §2 — The `npc_panel` House-card (the per-NPC radar)

The RTS House-card. One card per NPC: a header strip + an ordered subset of four rows.

```toml
[[sidebar_items]]
type   = "npc_panel"
npc_id = "npc_frank"
label  = "Frank"                                       # optional → falls back to NPC name → slug
rows   = ["arousal", "corruption", "location", "next"] # ordered subset of these four
# optional: arousal_bands, corruption_max_value, corruption_max_label, away_label, show_when
```

**Validation** (`template_import.py:3355-3385`): `npc_id` is required and must exist in the NPC definitions
(`:3361-3363`); `rows` must be a **non-empty list** (`:3367-3370`); each row must be one of
`arousal / corruption / location / next` (`:3373`); and an `arousal` or `corruption` row **requires that
trait declared in the NPC's `core_traits`** or it's a hard import error (`:3377-3385`). *(Code-vs-lore note:
the old draft cited the row validation at ~3373 — that's the row-loop line; the `elif itype == "npc_panel"`
block opens at `template_import.py:3355`.)*

**Render** (`v2.py:15058-15116`, the `sidebarItems` widget's `npc_panel` branch). The NPC object is resolved
via `setup.npc_slug_map` (`v2.py:15062`); if it can't resolve, the whole card is skipped (`:15063`). Each row:

| Row | What it renders | Verified |
|---|---|---|
| **`arousal`** | A band **glyph**, default `0→❄️ / 1→🔥 / 2→🔥🔥 / 3→🔥🔥🔥` (override with `arousal_bands` `[{min,max,text}]`). Label `🔥 Arousal`. The RTS-faithful range is 0–3 (`references/trait-catalog.md` §3). | `v2.py:15070-15082` |
| **`corruption`** | A **number**. At/above `corruption_max_value` it prints `corruption_max_label` (default `"MAX"`). Label `🫦 Corruption`. | `v2.py:15083-15091` |
| **`location`** | `setup.getNpcLocation(npc_id)` → the location name (`v2.py:3005`). **Same schedule source as the Schedule page** — both read `setup.npcSchedules` (Schedule page via `getNpcDaySchedule`/`getNpcAllSchedulesSorted`, `v2.py:3076`,`:3237`). Null-safe → `away_label` (default `"Away"`). Label `📍 Location`. | `v2.py:15092-15095` |
| **`next`** | The **Quests-page goal block, verbatim** — reuses `setup.renderQuestsGoalBlock` (`v2.py:15096-15108`), so the card shows the identical block the Quests page shows, minus flavor/tip prose. | `v2.py:15096-15108` |

**The `next` row is the planning payload** — it names PLACE + TIME-WINDOW + REQUIREMENT, not a vague "get
closer." `renderQuestsGoalBlock` (`v2.py:13924-13974`) emits exactly three frames:

- **🎯 To advance:** + a `◯`/`✓` bullet per goal, each with **live progress** while climbing
  (`◯ My corruption — 12 / 20`, the `currentValue / value` print at `v2.py:13962-13963`).
- **🔓 Ready** + `📍 <location>` + `🕒 <schedule window>` once all goals are met and a `ready_canvas` is set —
  the place and time-window come from the `ready_canvas` itself (`_locNameFromUuid` + `_formatCanvasSchedule`,
  `v2.py:13937-13947`).
- **✓ Arc complete** when the card is `terminal` (`v2.py:13928-13932`).

So a panel with `rows = ["arousal","corruption","location","next"]` reads, live:

```
FRANK
  🔥 Arousal      🔥🔥
  🫦 Corruption   12
  📍 Location     Kitchen
  ── next ──
  🎯 To advance:
  ◯ My corruption — 12 / 20
  …or once ready…
  🔓 Ready
  📍 Kitchen
  🕒 every day 22:00–02:00
```

That `🕒 every day 22:00–02:00` is the line that makes the schedule BITE — it tells the player not just *what*
to raise but *where to be and when* to cash it in. A cross-gated next-step inherits the gating arc's named
state through the same goal labels (author the goal's `label` to name the blocking arc).

**Surface only the rows that are LIVE for that NPC.** A slow-burn NPC whose corruption stays 0 by design
gets `rows = ["arousal","location","next"]` — keep `next` (it carries the planning payload that makes the
schedule bite) but drop `corruption` rather than show a number that never moves. `stage` and
antagonist `awareness` are **not selectable rows at all** (they're not in the validator's allowed set,
`template_import.py:3373`) — they can never surface here.

---

## §3 — Per-arc-shape sidebar VISIBILITY table

WHICH of an NPC's axes the player gets to see is **per arc shape** — not "show everything." The arc shape
(`references/trait-design.md`) sets the default; an NPC's design brief may override with a documented reason.

| Arc shape | Surfaces (default) | Why |
|---|---|---|
| **Family / ambient** | location + **arousal** + **corruption** + relation | Player plans Lane 3 (arousal), Lane 1 escalation (corruption), late-game intimacy (relation). All three are mechanically live. |
| **Slow-burn family** | location + **arousal** + relation | Corruption stays low by design — surfacing it would mislead ("why isn't this moving?"). Show the warm-up (arousal) and the bond (relation). |
| **Peer / dating** | location + **relation** | The chain is relation-driven. Arousal is bounded + less player-steerable; corruption isn't meaningful for a peer arc. |
| **Service** | location + **relation** only | The workplace bond is the only operative axis. Arousal/corruption don't apply to the service register. |
| **Antagonist / witness** | **location only** | The `awareness`/scandal accumulator stays HIDDEN — the dramatic surprise depends on the player NOT seeing how close confrontation is. |
| **ALL shapes** | `stage` + `awareness` NEVER surface | Internal-only across every NPC (see §4.3 + §5). |

**How each axis surfaces.** Of those, only **arousal / corruption / location** are `npc_panel` rows. The other
two surfacing axes use a per-NPC `trait_*` item:

- **relation** → a `trait_bar` (or `trait_words`) with `trait_owner = "npc"` + `npc_id` (the per-NPC variant,
  `references/trait-catalog.md` §5; render `v2.py:14887`+ honors `trait_owner`). Add this for peer/dating +
  service NPCs (who get no `npc_panel` arousal/corruption rows) and for family NPCs whose relation you want shown.
- **location** → the `npc_panel` `location` row (every in-scope NPC should have at least this).

So an **antagonist** panel is just `rows = ["location"]` — nothing else. A **service** NPC is
`rows = ["location"]` plus a `trait_owner="npc"` relation bar. A **family** NPC is the full
`rows = ["arousal","corruption","location","next"]` plus an optional relation bar.

*(Code-vs-lore note: the visibility table is **authoring doctrine, not engine validation** — the engine will
happily render a corruption row for a service NPC if you declare the trait. The discipline is yours; the
engine only enforces "trait must be declared.")*

---

## §4 — Body-state vs progression surfacing + the away/offscreen label

Two stat axes surface by opposite rules.

### §4.1 — Body-state (energy + hygiene) — MUST surface
These are the player's, not the NPC's, and they're the gates the player plans self-care around. The player
needs to know when to sleep/shower or Lane 3's hijack hosts never get visited (`references/lanes.md`). Render
as `trait_status_text` with author bands (`references/trait-catalog.md` §4, §5). **Hiding body-state breaks
basic planning — always surface it.**

### §4.2 — Progression — banded, numbered, or hidden
Player `corruption` → `trait_words` (banded identity word); `arousal` → `trait_bar` + `hide_value=true`;
`money` → a `trait_bar` shown as a number (`hide_value=false`, no bands) — there is **no dedicated money/number
primitive** (see `trait-catalog.md` §5). The full encode-by-type table + the doubling trap (band a stat ⇒ `hidden=true` the
same key or it prints twice) is **owned by `references/trait-catalog.md` §5** — do not restate it here.

### §4.3 — Internal-only (NEVER surface)
`<slug>_stage` and antagonist `awareness` never render anywhere. The mechanism: a `[[traits.labels]]` entry
with `hidden = true` becomes `setup.hiddenTraits` (`v2.py:950-953`, emitted `:2730`), which the trait-dump
loops honor (`v2.py:14315`,`:14341`,`:14362`+) so the number never prints. The player feels stage progression
through what the world DOES — new menu items, shifted NPC behavior, opened locations — not a number.
`<slug>_stage` is additionally impossible to put on an `npc_panel` (not an allowed row), so it's doubly safe.

### §4.4 — The away / offscreen label
When `getNpcLocation` returns null — the NPC has a declared schedule but **no entry matches the current
day+time** (`v2.py:3032`), i.e. he's genuinely absent/offscreen — the `location` row prints
`away_label` (default `"Away"`, `v2.py:15094`). Set a flavored one per NPC so the radar reads in-world:

```toml
rows      = ["arousal", "corruption", "location", "next"]
away_label = "out — across town"
```

This is the panel's half of the Day System's offscreen model: schedule an NPC's sleep/home/work block at an
`offscreen = true` location and the panel shows that location's NAME during those hours (it resolves on the
Schedule page too); only the gaps with no schedule entry at all fall through to `away_label`
(`references/toml-gotchas.md` "Day System shapes"). Pair the two so the NPC always reads *somewhere* —
a named place when scheduled, your `away_label` when truly gone — never a dead blank.

---

## §5 — The global-hidden-name trap (npc_panel rows are hidden by NAME, not per-NPC)

A real code behavior to plan around. The `npc_panel` `arousal` and `corruption` rows each gate on
`setup.hiddenTraits` by **bare trait name**, not per-NPC namespace:

- arousal row: `<<if not (setup.hiddenTraits && setup.hiddenTraits.includes("arousal"))>>` (`v2.py:15071`)
- corruption row: `<<if not (setup.hiddenTraits && setup.hiddenTraits.includes("corruption"))>>` (`v2.py:15084`)

So if you `[[traits.labels]] hidden = true` the **player's** `corruption` to kill the §5 doubling
(`references/trait-catalog.md` §5), you ALSO suppress the `corruption` row on **every** `npc_panel` —
the same name, hidden globally, hides everywhere. Same for `arousal`.

**Consequence + workaround:**

- If you want the player corruption WORD-banded (hidden number) AND NPC corruption NUMBERS on House-cards,
  you can't share the key name through the simple hide. Options: (a) accept that hiding player `corruption`
  drops NPC corruption rows and lean on the `next` row / Quests page to convey NPC progress; or (b) keep
  player `corruption` un-hidden and de-dup another way (band only NPC-side, or live with the player number).
- The **`location`** and **`next`** rows are NOT gated by `hiddenTraits` (`v2.py:15092`,`:15096`) — they
  always render regardless of any hidden label. So the location radar survives any hide.

*(Code-vs-lore note: no corpus draft documented this name-collision — the §5 doubling fix and the §3
visibility model interact through one global name list. Verify with `grep 'hiddenTraits.includes' v2.py`
before hiding a key that an `npc_panel` also reads.)*

---

## §6 — Authoring checklist + pointers

**Per in-scope NPC:**
- [ ] Emit an `npc_panel` with `npc_id` and at least a `location` row.
- [ ] Choose `rows` by arc shape (§3): family `["arousal","corruption","location","next"]`; slow-burn
      `["arousal","location","next"]`; peer/dating + service `["location"]` (+ a `trait_owner="npc"` relation
      bar); antagonist `["location"]` only.
- [ ] Declare every `arousal`/`corruption` row's trait in that NPC's `core_traits` (else hard import fail,
      `template_import.py:3377-3385`).
- [ ] Set a flavored `away_label`; pair with an `offscreen=true` schedule block so the NPC always reads
      somewhere (§4.4).
- [ ] Author the `next` row's source quest card so its goals name PLACE + WINDOW + REQUIREMENT (§2).
- [ ] Never add a `stage` or `awareness` surface (not selectable rows; keep them `hidden=true`).
- [ ] Check the §5 name-collision before hiding a key any `npc_panel` reads.

**Don't duplicate — pointers:**
- **PLAYER stat → sidebar primitive encode-by-type, the doubling trap, `hidden=true` de-dup, the
  no-dedicated-money-type fact** → `references/trait-catalog.md` §5.
- **Trait ranges/defaults/bands, energy/hygiene body-state spec, NPC arousal 0–3 throttle, `<slug>_stage`
  storage** → `references/trait-catalog.md` §2–§4.
- **Which trait drives which arc (the spine by shape), throttle-vs-odometer** → `references/trait-design.md`.
- **`npc_panel` placement under `[[sidebar_items]]`, per-NPC-sidebar-supported note, offscreen Day System
  shape** → `references/toml-gotchas.md`.
- **Lane 3 dispatcher + self-care hijack hosts the radar exists to support** → `references/lanes.md`.
- **The HUD-always-on system row** → `references/systems.md`.
