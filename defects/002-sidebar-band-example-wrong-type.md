# 002 · `engine.md` §30's band example fails on two of the three sidebar types

**Found:** 2026-08-30, in `games/commuter` at v0.1
**Status:** FIXED 2026-08-30
**Layer:** skill / reference (`.claude/skills/author-game-v2/references/engine.md` §30)

## What happened

`commuter`'s board wrote its top sidebar bands open-ended — a `min` and no `max` — and the build
refused to compile:

```
sidebar_items[0] (trait_words) bands[3]: missing 'max'
sidebar_items[1] (trait_words) bands[3]: missing 'max'
sidebar_items[2] (trait_words) bands[3]: missing 'max'
sidebar_items[7] (trait_bar)   bands[2]: requires both 'min' and 'max'
```

## The rule is per item type, and the skill does not say so

`apps/projects/services/template_import.py`:

⚠️ **Two of these three rows were WRONG when written; corrected 2026-08-30 against source.**

| type | rule | line |
|---|---|---|
| `trait_status_text` | at least one of `min` / `max` — an open top band is **legal** | `:3751-3757` (was cited `:3574-3576`, which is loop preamble — drift ~180 lines) |
| `trait_words` | `flag` **XOR** range; in range mode both required. **A flag-only band is legal** | `:3613-3623` (bare `:3623` dropped the flag escape hatch) |
| `trait_bar` | both required; `flag` rejected outright; `bands` itself optional (`:3659`) | `:3680-3681` ✓ |

## Why the author wrote it that way

`engine.md` §30 carries exactly one worked example, at `engine.md:1332-1341`:

```toml
[[sidebar_items]]
type  = "trait_status_text"
trait = "cover"
bands = [ { min = 0, max = 14, text = "…" }, { min = 15, text = "Apron off" } ]
```

That example is correct — for `trait_status_text`.

⚠️ **The diagnosis in the sentence that used to stand here was WRONG, corrected 2026-08-30.** It read
*"Nothing beside it says the shape does not carry to the other two types."* **Something does.** §30
already drew the exact distinction, two lines below the example:

> `trait_status_text` treats an omitted `min`/`max` as open-ended … `trait_words` needs a **closed**
> `[min, max]` to match

The real cause is the **very next clause**:

> **Leave the top band's `max` off**, or `cap` the terminal add (§29).

Type-blind instruction, no type attached, sitting immediately after the sentence saying it is safe on
only one of the three. The author followed the instruction rather than the distinction. That makes
the fix smaller and more precise than "the docs never said": the docs said it, then contradicted it
one clause later, and the imperative won.

The ledger even wrote the reasoning down as if it were doctrine: *"the sidebar's top band carries
no `max` so a value landing above it still renders (engine.md §30)."*

## This is the skill's own named failure mode

`SKILL.md`, operating rules: **"An example outranks every rule beside it."** The example was read
as the shape; the type it was attached to was not. Same family as the British-noun leak
(`airer` ×9) and the `15/35/55/75` rung table.

## Proposed fix

1. Put the per-type table above into §30, next to the example.
2. Change the example to the type most games actually use for a banded ascent tier — `trait_words` —
   with both bounds, so the copied shape is the safe one.
3. Keep §30's existing warning that a value outside every band renders nothing: with a closed top
   band that warning now has teeth, because the top `max` must sit at or above the trait's ceiling.
   `commuter` uses `max = 100` against declared ceilings of 88 / 86 / 80.

## The tired-author test

An author who copies the fixed example gets a legal, non-blank sidebar on all three types. Passes.

---

## Fixed — 2026-08-30

**1 · The blanket clause is gone.** *"Leave the top band's `max` off"* is replaced by a per-type
table stating the validator's real rules, with the correct `template_import.py` and `v2.py` anchors,
and by the positive instruction that actually holds on all three types: give the top band a `max` at
or above the trait's ceiling, or `cap` the terminal add.

**2 · The worked example is now `trait_words` with both bounds closed**, so the shape that gets
copied blindly is legal everywhere. The `[[traits.labels]] hidden = true` half is unchanged — that
part was always correct and is why the example exists. §30 now carries a `⚠️` recording that the
section taught this bug, naming `SKILL.md`'s own rule as the diagnosis: *an example outranks every
rule beside it.*

**3 · Four more stale citations found while verifying, all off by ~682 lines** — a block insertion
nobody re-anchored. Every one corrected:

| §30 cited | what was actually at that line | true anchor |
|---|---|---|
| `v2.py:16251` (`trait_status_text`) | a `<<for>>` loop | **`16933`** |
| `v2.py:16314` (`trait_words`) | `npc_traits_widget = ""` | **`16996`** |
| `v2.py:16266` (open-ended defaults) | a blank line | **`16948-16949`** |
| `v2.py:16335-16336` (closed range) | the version-footer widget | **`17017-17018`** |

`trait_bar` was listed with no citation at all; it now carries **`v2.py:16886`**.
