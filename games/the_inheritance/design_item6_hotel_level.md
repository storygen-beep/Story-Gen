# Item 6 — The Hotel Accumulation Loop (`hotel_level`)

> **What this is.** The build spec for `design_mopoga_alignment.md` Item 6. Source of truth
> for the session. Research: `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/` (report
> F2/F4), memory `mopoga-top30-twine-study`. Author-game Batch-B doctrine ("what compounds —
> declare it; each growth state opens content"). Built 2026-07-26, book rev 21 → 22.

## The finding that shaped the design

The mopoga winners are **engines of accumulation** — the save file *becoming yours* is the
pull. The Inheritance's fantasy is "this hotel becomes yours," but a read-only audit (3
workflow + 3 explore agents, all cited in-code) found **the compounding loop already exists,
invisibly:**

- `richard_signed` (Act-2 story) unlocks the back office →
- `back_office_numbers` sells upgrades: **$500 → `escort_upgrade`** ($400/day escort) and
  **$2000 → `private_floor_open`** (the private floor + income apex $800/$1500/$3000) →
- the hinge `p_take_purse` fires at money ≥ $500 → `hotel_in_hand`.

*Earn → spend into upgrade flags → unlock higher-income tiers → earn more* is wired. What's
missing is the **face**: no named growth object, hubs never change, no ledger, no post-apex
"it's all mine" state. So Item 6 = **give the existing engine a name, visible states, and a
face** — not build a new loop.

**LO's locked calls:** passive sleep-income YES; 4 states (the $500 escort step folds into
the level-1 era, not its own level). **Media-neutral** (hub reskins reuse existing images;
per-level images are Item 3).

## The design — `hotel_level`, a hidden derived 4-state dial

Hidden int trait 0→3, **set** (not bought/grinded) at three existing flag-setters, so it never
competes with `corruption` as a grind axis. `corruption` gates the earners; `hotel_level`
gates the venue's look + passive income. Orthogonal.

| Lvl | Name | Gate (already in-game) | Money's role |
|-----|------|------------------------|--------------|
| 0 | The dust sheets | default (pre-`hotel_in_hand`) | — |
| 1 | The books in your name | `hotel_in_hand` | story + $500 floor |
| 2 | The private floor earns | `private_floor_open` | story (`richard_signed`) + $2000 |
| 3 | The house full | `margaret_broken` | pure story apex |

**Monotonic-up guaranteed** except one edge: `private_floor_open` is an optional sink buyable
*after* the apex → would `set` 3 back to 2. **Guard:** the $2000 choice gets `margaret_broken
is_false` appended to its `conditions` (hides post-apex). The only thing it "locks" is opening
a mid-game income floor after you've already won — nothing left to fund. Level 2 is legitimately
**skippable**; every read uses `gte`, so a 1→3 jump renders cleanly.

## What ships

1. **Trait** — `1_metadata` `[player.core_traits]` `hotel_level = 0`; `0_systems`
   `[[traits.labels]] key="hotel_level" hidden=true`.
2. **Setters** (`op="set"`, `5_scenes.toml`): `p_take_purse` "Take the books in hand" (:232) → 1;
   back-office "$2000" (:4373) → 2; `marg_cap_breaking` "Break her." (:3998) → 3.
3. **Regression guard** — append `margaret_broken is_false` to the $2000 choice conditions (:4379).
4. **Hub reskin** (prose-only, raw `<<if>>` in `description`, in-place every entry): `loc_hotel`,
   `loc_hotel_bar`, `loc_hotel_guest_rooms` each get 4 bands turning as the house does.
5. **Passive income** — `[engine.daily_tick]` two gated money effects: `eq 2` → +$100, `gte 3`
   → +$300 (mutually exclusive; daily_tick items don't short-circuit). Ties to the nightly cycle
   (fires only on a midnight-crossing sleep — same as the existing arousal/energy drift).
6. **Nightly ledger line** — a `gte-3-first` group prose ladder in `activity_sleep` blocks.
7. **Quest spine** — split the Act-2 "take the family" card on **`richard_signed`** (the real
   phase boundary — the back office opens there): Band A = take the family; Band B = open the
   private floor ($2000) + finish Grayson/Margaret. Spine style, no `goals` (would leak the
   hidden number), no `npc_id`, priority 100.

## Engine facts relied on (verified)
- `description` emitted **raw** (`v2.py:9524`); raw SugarCube macros survive + evaluate every
  entry, in-place. Use **named operators** (`gte`), ladder highest→lowest, inline branches.
- `op="set"` writes the literal (`v2.py:5606`); precedent `grayson_stage` op=set `5_scenes:1948`.
- Canvas/exit effects compile **unconditionally** (`v2.py:12943`) → income can't be a
  conditional sleep effect; `daily_tick` per-effect `conditions` DO gate (`v2.py:5436`).
- Adjacent `[group]` blocks merge into one if/elseif chain (`v2.py:13653`) — only ONE group
  ladder in the sleep node here (income is in daily_tick), so no collision.
- Every `conditions` block needs `version="1.0"` or FAILS OPEN (`v2.py:3683`). Quest-card `when`
  is a different evaluator — **no** `version` key, `{flag=..., op=...}` shape.

## Out of scope
Per-level images / wallpaper (Item 3), full daily-flag ledger (Item 5), production build / media
harvest / re-list (ship-gate), any new NPC / sink / management UI, decay (Item 7, parked).

## Verify
Build green; `grep hotel_level` shows 3 setters + reads; playwright: drive 0→3, hubs change
in-place, sleep income/ledger at 2 & 3 (none at 0–1), one spine card/stage (no blank rows),
regression guard holds (set `margaret_broken` → $2000 choice gone, level stays 3).
