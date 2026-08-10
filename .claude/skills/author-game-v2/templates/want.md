# The Want — <game title>

> Fill every field. Keep the whole thing to one page; longer means vaguer.
> Doctrine and the reasoning behind each field: `references/the-want.md`.
> **Re-read this before every release.** Bump `want.last_read_at_release` in `v2_state.json`.

---

## 1. Who she is

<Her situation at minute zero. Concrete: a job, a debt, a room, a reputation.>

**What she has to lose:** <the thing that makes the first transgression cost something>

## 2. The appetite that never fills

<What she wants, phrased so it can never be finished.>

- ✅ "be wanted by people who shouldn't want her"
- ❌ "get revenge on X" — that completes, and then release 41 has nothing to do

**What does release 41 add?** <answer it here, now, in one line>

## 3. What she is becoming — as ACCESS

**Bottom:** <what she can do, in which places, at zero>
**Top:** <what she can do, in which places, at the ceiling>

### The ascent tiers

Three or four ratcheting tiers, each a *different kind* of going-further. One
undifferentiated "corruption" hands every player the same ladder; several tiers let a player
who doesn't want one still climb another. Rungs at **15 / 35 / 55 / 75**.

| tier key | what going further means on this axis | rung 15 | rung 35 | rung 55 | rung 75 |
|---|---|---|---|---|---|
| `<tier_1>` | | | | | |
| `<tier_2>` | | | | | |
| `<tier_3>` | | | | | |

**Counterweight (optional):** `<key>` — <what it protects, and what spends it>

## 4. The charge

Pick and name it. "It's hot" is the absence of a charge, not one.

- [ ] **Reversal** — <who has power over her, and how it flips>
- [ ] **Taboo** — <what the relationship itself transgresses>
- [ ] **Transformation** — <what she becomes that she'd not have recognised>

## 5. Why *this* person

One line each — not their plot role. **Why she wants them, or why being wanted by them lands.**
A character with no line here has no reason to exist: cut them, or write it.

| character | why they are wanted |
|---|---|
| `npc_<id>` | |
| `npc_<id>` | |

## 6. Register

- **`narration_person`** = `second` — declared once, **immutable** after the first release.
- **Crude-vocabulary ceiling** — write the actual words, per character, per tier. A ceiling
  described abstractly gets written around.

| character | tier 1 | tier 2 | tier 3 |
|---|---|---|---|
| `npc_<id>` | | | |

- **Where the crude register lives:** <name the repeatable surfaces>

  This is the correction the whole skill exists for. The measured failure wrote its explicit
  register only into scenes the player sees once, and wrote its fifty-times-replayed loops as
  literary character study.

---

## The four checks — answer out loud before leaving this file

1. **What does release 41 add?** (if unanswerable, the appetite terminates — rewrite §2)
2. **What can she reach at the top that she cannot at the bottom?** (the ascent, §3)
3. **Which character would a player miss if deleted, and why?** (the product, §5)
4. **Which repeatable surface carries the crudest writing in the game?** (§6 — and if the
   answer is a one-time scene, the game is already cold)

---

**Then:** create `games/<slug>/v2_state.json` with `phase = "want"` per `references/state.md`,
and move to `templates/board.toml`.
