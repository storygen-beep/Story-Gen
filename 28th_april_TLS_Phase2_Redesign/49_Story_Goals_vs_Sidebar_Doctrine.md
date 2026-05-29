# Doc 49 — Story Goals vs Sidebar Doctrine

**Session:** 2026-05-24
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Doctrine — applies to all current and future TLS-engine games
**Supersedes:** nothing. Codifies an unwritten rule.
**Triggered by:** the shower/rest quest-card swap shipped 2026-05-24 — the second TLS quest-card doctrine correction in two weeks (first was the `group_settled_in` strip-down on 2026-05-17). Two corrections in two weeks → the rule belongs on paper.

---

## 1. The question this doc answers

You're authoring a TLS game. You want to surface something to the player — a need, a milestone, a state. You're staring at the TOML wondering: does this go in `[[quest_cards]]` or `[[sidebar_items]]`?

The one-line rule:

> **Story Goals carry narrative arcs the player is pursuing. The sidebar carries body-state status that fluctuates.**

Everything below explains what that means in practice, why both surfaces exist, and how to decide quickly when a new case comes up.

---

## 2. Story Goals — what they ARE

A Story Goal is **one directive sentence per narrative arc, in first-person Maya voice, backed by a single in-world milestone the player reaches by playing**.

Frames (PRD 48 single-path renderer, see doc 48):
- 🎯 active — the arc is open, the player should be working toward it
- 🔓 ready — the milestone scene is reachable right now
- ✓ complete — the arc closes

Live TLS examples (from `games/the_long_summer_test/toml_phases/7_final_game.toml` SG1–SG3, post-strip):

```toml
# SG1 — Rent (Sunday morning rent scene)
[[quest_cards]]
text         = "Rent's coming due and I've got next to nothing. No money, no roof — I need work, fast."
tip          = "Odd jobs, anyone who'll pay — start asking around."
group        = "rent"
ready_canvas = "scene_kitchen_diana_morning"
when = [
  { flag = "first_rent_paid", op = "is_false" },
]

# SG2 — Settle in (one-shot auto-fire after Sunday passes)
[[quest_cards]]
text         = "I'm new under this roof. Give it a week — get to know the people I'm living with: Frank, his wife Diana, and Jake."
tip          = "Settle in. A week here and the house stops being a place you're visiting."
ready_canvas = "transition_group_settled_in"
when = [
  { flag = "group_settled_in", op = "is_false" },
]

# SG3 — First Sunday with Diana (church or stay-home; both clear first_sunday_passed)
[[quest_cards]]
text         = "Diana keeps bringing up church. The first Sunday service with her would count for something in a town this small."
tip          = "Go with Diana to the first Sunday service."
ready_canvas = "scene_kitchen_diana_morning"
when = [
  { flag = "first_sunday_passed", op = "is_false" },
]
```

What every one of these has in common:
- **One sentence**, written in Maya's voice. Not a status report; a thing she wants.
- **One flag** (`first_rent_paid`, `group_settled_in`, `first_sunday_passed`) — set by **one** in-world scene she'll play.
- **A `ready_canvas`** that points at the actual scene where the milestone happens.
- **No `op = "lte"` against a recovering trait.** No daily latch. No proxy chain.

Schema reference: `[[quest_cards]]` requires `text`, takes `tip`, `group`, `ready_canvas`, and `when = [...]` for conditions. The condition list is **AND**ed; an empty list means always-show.

---

## 3. Story Goals — what they are NOT

Hard rules. None of these belong in `[[quest_cards]]`:

| ✗ Don't | Because |
|---|---|
| Body-state reminders ("you're tired", "you're dirty") | The state fluctuates and recovers on action — quests are permanent arcs, not heartbeat signals. |
| Chore-gated proxies ("did 3 sub-things today, therefore X is ready") | The quest panel ends up tracking arithmetic, not narrative. |
| Daily-reset flag latches dressed as permanent milestones | A `*_today` flag flips back at midnight, so any quest gated on it gets misleading frames. |
| Multi-flag silent-derivation cards | If a quest needs more than one flag to know it's done, the quest design is wrong, not the flag machinery. |
| Two cards sharing the same `condition.missing_flag` | Mutex impossible at render — two cards both think they're "the current one." |

These rules were not invented in the abstract. They come from the 2026-05-17 `group_settled_in` failure (see §7 case 2) and the 2026-05-24 shower/rest failure (see §7 case 1).

---

## 4. Sidebar primitives — the body-state surface

The sidebar is where **passive, continuous, state-driven** information lives. It updates on every render. It carries no flag bookkeeping — it reads the player or NPC state directly.

Three banded-text primitives currently exist alongside the structural ones (`passes`, `inventory`, `stage_label`):

| Primitive            | Driven by              | Author or auto?     | Visual            | Use for                          |
|----------------------|------------------------|---------------------|-------------------|----------------------------------|
| `trait_bar`          | trait value (with bar) | author              | Bar + bands       | Always-visible meters (arousal)  |
| `trait_status_text`  | trait value (text only)| author              | Cool blue banner  | Need-state banded warnings       |
| `trait_decay_warning`| stat dropped today     | auto-emitted        | Amber banner      | "Hygiene fell to 27 today"       |

`trait_status_text` vs `trait_decay_warning`: similar visual language, **opposite temporal model**. Status = continuous threshold ("right now you're below 30"). Decay = event ("today you dropped, and you're near the next gate"). They can coexist on the same trait — one nags continuously below threshold, the other flashes once on a drop.

---

## 5. The `trait_status_text` primitive (shipped 2026-05-24)

### TOML schema

```toml
[[sidebar_items]]
type        = "trait_status_text"
trait_owner = "player"            # optional; defaults "player"; "npc" + npc_id supported
trait       = "hygiene"           # required; must exist in core_traits of the owner
bands = [
  { max = 30, icon = "💧", text = "Ugh, I really need a shower." },   # severe first
  { max = 60, icon = "💧", text = "I'm starting to feel grimy." },     # softer after
]
```

Required: `type`, `trait`, `bands` (non-empty). Each band needs `text` and at least one of `min`/`max`.

Optional: `trait_owner` (defaults `"player"`), `npc_id` (required when owner is `"npc"`), `icon` per band.

### Render semantics (load-bearing)

1. **Bands evaluated in author order; first match wins.** Author severe-to-soft so the worst applicable message rises to the top.
2. **`min` optional → sentinel −1e9; `max` optional → sentinel +1e9.** Most authoring uses just `max` ("below N"). One-sided bands are idiomatic.
3. **No band matches → the wrapper div is NOT rendered.** Sidebar stays silent on healthy stats. This is the entire UX point of the primitive — silence is the default state.
4. **NPC owner mode reuses `trait_bar`'s slug→UUID lookup** (`setup.npc_slug_map`). Not yet used in TLS; documented for future "NPC suspicion is rising" style surfaces.

### Visual identity

`.trait-status-text-item` carries a cool blue tint:

```css
.trait-status-text-item {
    margin-top: 0.5rem;
    padding: 6px 10px;
    background: rgba(99, 179, 237, 0.14);
    border-left: 3px solid rgba(99, 179, 237, 0.75);
    border-radius: 4px;
    color: var(--theme-text);
    font-size: 0.78rem;
    line-height: 1.35;
}
```

Distinct from `.trait-decay-warning-item` (amber + ⚠ glyph + `var(--theme-warning)` border). Players should read status-text as "this is the current state" and decay-warning as "this just dropped" — different colors, different glyphs, different mental models.

### File pointers

| Concern | Path |
|---|---|
| v2 render branch | `apps/game_generation/twee_comprehensive/generators/v2.py` (next to the `trait_bar` branch, before `trait_decay_warning`) |
| v1 render branch (frozen-mirrored) | `apps/game_generation/twee_comprehensive/generators/v1.py` |
| v2 CSS rule | same file, near `.trait-decay-warning-item` |
| Validator | `apps/projects/services/template_import.py` (`elif itype == "trait_status_text":` block) |
| Tests (validator) | `apps/projects/tests.py::TraitStatusTextSidebarTests` (16 tests) |
| Tests (render template) | `apps/projects/tests.py::TraitStatusTextRenderTemplateTests` (11 tests) |

Full pytest projects suite: **362 / 362 green** (was 335, +27 new).

---

## 6. The decision rule (the load-bearing section)

When you're about to author a new player-facing surface, run it through these three questions in order. Stop at the first **YES**.

1. **Is this a narrative arc the player is pursuing in the world?**
   *(Examples: "find work to pay rent", "settle in with the family", "first Sunday with Diana".)*
   → If yes, it's a **Story Goal**.

2. **Does the player close it by acting in the world** *(talking to an NPC, completing a scene)* **AND does completion mark a permanent milestone?**
   *(Examples: "first kiss with Frank", "Jake's debt collected", "fired from the diner".)*
   → If yes, it's a **Story Goal**.

3. **Is this a body state** *(or world state)* **that fluctuates, addressed by a recurring activity** *(showering, sleeping, eating, masturbating)*, **and that comes back if neglected?**
   *(Examples: hygiene, energy, hunger, horniness, "you're cold and it's raining".)*
   → If yes, it's a sidebar `trait_status_text`. **Never a quest card.**

If a surface seems to want both treatments — pause. It's almost certainly two surfaces being conflated. Split them. (Example: "Maya is hungry AND that's why she takes the diner job" → the *hunger* is a sidebar status; the *diner job* is a Story Goal. Two separate surfaces, one driving the other.)

---

## 7. Worked TLS examples

### Case 1 (2026-05-24, today) — Shower + Rest cards

**Before:**
```toml
# SG4 — Hygiene crisis
[[quest_cards]]
text = "Ugh, I really need a shower."
when = [{ trait = "hygiene", subject = "player", op = "lte", value = 60 }]

# SG5 — Energy crisis
[[quest_cards]]
text = "I'm wiped. I need to rest before I can think straight."
when = [{ trait = "energy", subject = "player", op = "lte", value = 40 }]
```

User-observed bug: after showering (hygiene → 100), the SG4 card was still in the Story Goals panel. The surface explanation was a dismiss-eval bug; the deeper explanation was that **these were never quests to begin with**. Hygiene fluctuates 100 → 80 → 60 → 30 → 100 → 80 → 60... A quest panel that flips a card in and out forever is not surfacing a story arc.

**After:**
```toml
[[sidebar_items]]
type        = "trait_status_text"
trait_owner = "player"
trait       = "hygiene"
bands = [
  { max = 30, icon = "💧", text = "Ugh, I really need a shower." },
  { max = 60, icon = "💧", text = "I'm starting to feel grimy." },
]

[[sidebar_items]]
type        = "trait_status_text"
trait_owner = "player"
trait       = "energy"
bands = [
  { max = 20, icon = "😴", text = "I'm wiped. I need to rest before I can think straight." },
  { max = 50, icon = "😴", text = "Could use a break." },
]
```

Result: stat itself drives the text. Hygiene drops to 50 → sidebar shows "I'm starting to feel grimy." Drops to 25 → text swaps to "Ugh, I really need a shower." Maya showers (sets `hygiene` = 100) → sidebar text disappears on the very next render. **No flag. No dismiss bug possible.**

Bonus: by adding the softer band (`max = 60`), we get graceful escalation the original card didn't have — the player sees the state degrading instead of getting hit with a "crisis" message at the cliff edge.

### Case 2 (2026-05-17) — `group_settled_in` strip-down

**Before:** the SG2 "settle in" Story Goal was wired through five mechanisms:

1. A derivation canvas that ran daily to count NPC interactions
2. Three proxy flags (`frank_met`, `diana_met`, `jake_met`) — each gated on its own conditions
3. A daily-reset flag (`talked_to_resident_today`) being used as a permanent milestone
4. An `arc_closure_flag` pointing at a setter that wasn't a real player-actioned scene
5. The quest's render condition resolving to "🔓 Ready" on the same day Maya arrived — soft-lock by misleading frame

**After:** one directive sentence ("settle in, get to know Frank, Diana, Jake"), one flag (`group_settled_in`), set by one in-world scene (`transition_group_settled_in`), reached by playing through the first Sunday.

Lesson: **when a quest needs more than one flag to know it's done, the quest design is wrong, not the flag machinery.** Don't add mechanisms to support a quest shape that was never going to work — change the shape.

---

## 8. Anti-patterns (don't do this)

Quick-reference list of failures we've seen. If your authoring drifts toward any of these, the doctrine has already been violated.

- **Quest cards that fire on `op = "lte"` against a recovering stat.** Sidebar `trait_status_text` instead. (Case 1.)
- **Daily `*_today` flags used as permanent quest-completion gates.** Daily flags gate daily-repeatable content only. (Case 2.)
- **`arc_closure_flag` pointed at a setter that isn't a player-actioned scene.** The closure frame ("🔓 Ready") becomes a lie. Use the real milestone scene's flag.
- **Story Goals page used as a notification surface** ("oh by the way you're tired"). Notifications belong in the sidebar or the in-passage notify rail.
- **Co-rendered Story Goals cards sharing the same `condition.missing_flag`.** Two cards both think they're "the current one"; render order decides who wins, which is arbitrary.
- **Multi-flag silent-derivation canvases just to populate a quest field.** If you find yourself authoring a canvas whose only job is to set a flag for another quest's `ready_canvas`, the second quest is the wrong shape.

---

## 9. Forward compatibility — primitives to add (not building today)

When future authoring needs surface, prefer **adding another sibling primitive** over stretching an existing one. The shape of each:

- **`world_status_text`** — bands keyed off a world variable instead of a player trait. For weather, season, time-of-day ambient cues ("It's pouring outside.", "First snow of the year."). Same bands grammar as `trait_status_text`; the only delta is the data source. Not built; not yet needed.
- **NPC-mood surfaces** ("Frank's been quiet today") — already covered by `trait_status_text` with `trait_owner = "npc"`. No new primitive required; just use it.
- **Inventory-state surfaces** ("you're out of cash") — existing `passes` / `inventory` items cover most cases; a banded variant could be added if a future game wants graduated messaging ("low on cash" → "broke" → "in debt"). Don't preempt.

If a future surface doesn't fit any existing primitive's shape: add a new primitive, give it a distinct CSS class so players read it as a distinct signal, write a §5-shaped section here, run the §6 decision rule against it before shipping.

---

## 10. References

**Memory entries (in `/Users/a0000/.claude/projects/.../memory/`):**
- [`feedback_rts_objective_quest_doctrine`](../../../.claude/projects/-Users-a0000-Desktop-Desktop-Archive-Backup-story-gen-story-gen-web-app-story-gen-django/memory/feedback_rts_objective_quest_doctrine.md) — the 2026-05-17 doctrine that triggered case 2
- [`trait_status_text_primitive`](../../../.claude/projects/-Users-a0000-Desktop-Desktop-Archive-Backup-story-gen-story-gen-web-app-story-gen-django/memory/trait_status_text_primitive.md) — the 2026-05-24 implementation log

**Adjacent docs in this folder:**
- Doc 47 — Quests Page Unified Card Design (card-shape mechanics, single-path render)
- Doc 48 — Quests Engine V2 PRD (the V2 engine, `quests_engine = "v2"` opt-in)

**Live TLS author file:**
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — search for `[[sidebar_items]]` (line ~806) and `[[quest_cards]]` (line ~2440) for current examples

**Engine code:**
- Validator: `apps/projects/services/template_import.py` (per-type sidebar branches around line 2380; per-type quest_cards validation elsewhere)
- Generators: `apps/game_generation/twee_comprehensive/generators/v1.py` + `v2.py` (sidebar render dispatcher around line 13720 / 14390 respectively)

**Tests:**
- `apps/projects/tests.py::TraitStatusTextSidebarTests`
- `apps/projects/tests.py::TraitStatusTextRenderTemplateTests`
- `apps/projects/tests.py::TraitBarSidebarTests`
- `apps/projects/tests.py::TraitBarRenderTemplateTests`
- `apps/projects/tests.py::TraitWordsSidebarTests`

---

## Appendix A — The check before shipping

Before opening a PR that touches `[[quest_cards]]` or `[[sidebar_items]]`, run through this:

- [ ] Every quest card answers YES to question 1 or 2 of §6.
- [ ] No quest card answers YES to question 3 of §6.
- [ ] Every quest card's `when` condition resolves on **one** flag set by **one** in-world scene.
- [ ] No quest card uses `op = "lte"` / `op = "gte"` against a recovering trait.
- [ ] No two co-rendered quest cards share a `condition.missing_flag`.
- [ ] Every `trait_status_text` band has `text` + at least one of `min`/`max`.
- [ ] Sidebar primitives chosen distinct from quest cards (no overlap of intent).

If any item fails, the change isn't ready. Either reshape the quest or move it to the sidebar.

---

*End of doc 49.*
