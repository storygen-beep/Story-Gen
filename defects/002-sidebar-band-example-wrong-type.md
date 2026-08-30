# 002 · `engine.md` §30's band example fails on two of the three sidebar types

**Found:** 2026-08-30, in `games/commuter` at v0.1
**Status:** OPEN
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

| type | rule | line |
|---|---|---|
| `trait_status_text` | at least one of `min` / `max` — an open top band is **legal** | `:3574-3576` |
| `trait_words` | both required | `:3623` |
| `trait_bar` | both required | `:3681` |

## Why the author wrote it that way

`engine.md` §30 carries exactly one worked example, at `engine.md:1332-1341`:

```toml
[[sidebar_items]]
type  = "trait_status_text"
trait = "cover"
bands = [ { min = 0, max = 14, text = "…" }, { min = 15, text = "Apron off" } ]
```

That example is correct — for `trait_status_text`. Nothing beside it says the shape does not carry
to the other two types, and §30's own prose lists all three (`trait_status_text`, `trait_words`,
`trait_bar`) as though they behave alike. The board copied the open top band onto `trait_words`.

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
