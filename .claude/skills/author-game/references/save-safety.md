# save-safety — what you may NOT change once a game has shipped

**Read this before editing a game that players may already have saves for** (anything you've published to
itch / gamcore / mopoga, or shared a build of). It is the release-discipline layer: the engine makes updates
save-safe, but only if you don't move the identifiers a save is *joined on*. Everything here is a **runtime**
break — the build passes clean and the game plays fine on a fresh start; the damage only shows when a
**returning player loads an old save** against the new build.

## Why saves can break at all (the model)
A SugarCube save stores the **passage the player is parked on** (by name) plus **`State.variables`** — `$player`,
`$npcs`, `$flags`, `$game_state`. On load the engine restores that state and re-renders the passage; it does
**not** re-run `:: Start`. So a save is joined to the new build through four keys: **passage names**, the
**`$npcs` key**, the **flag/trait key**, and the **stat's meaning**. The engine now keeps three of those stable
for you (passages and `$npcs` are keyed by your authored **slugs**, not regenerated ids; a migration backfill
adds new content into old saves). The four rules below are the part **you** own — the changes that still move a
key out from under an existing save.

**One-time note:** the first build on the slug-id / slug-passage engine is a clean baseline. Publishing it over
an *older-scheme* build resets those players once (unavoidable — the id scheme changed). Every build after that
follows these rules and carries saves forward.

---

## §1 — Slugs are immutable release ids
The engine names **every passage** by slug — `Canvas_<canvasSlug>_Node_<nodeSlug>` and `Location_<locSlug>`
(`v2.py:_node_passage_name` :11246, `_location_passage_name` :11259) — and keys `$npcs` and item sub-state by
the item's TOML **`id`** (`game_graph.py` mints `npc.id = <slug>` :144, `loc.id = <slug>` :182,
`node.id = "<canvas>.<node>"` :363). A save stores the passage it's on (e.g. `Location_wren_room`,
`Canvas_loop_renner_office_sex_Node_base_doggy_r`) and its NPC/wardrobe/quest state under those slugs.

**So:** rename a `[[canvases]]`, `[[canvases.nodes]]`, `[[locations]]`, `[[npcs]]`, `[[clothing_items]]`,
`[[quests]]`, or `[[fast_jobs]]` **`id`** on a shipped game and the save points at a passage / `$npcs` entry
that no longer exists — the player lands nowhere, or an NPC / outfit / quest silently vanishes.

**The rule:** treat every TOML `id` as a permanent release identifier. **Change display names freely**
(`name`, `title`, prose — players never see the id); **never change the `id`.** Reordering, inserting, or
deleting nodes inside a canvas is safe *because* passages are slug-named, not positional — only a **rename**
of an id breaks.

---

## §2 — Never rename or repurpose a live flag or trait key
`$flags` is keyed by flag name and traits by their key; that string **is** the runtime join between the scene
that SET it and the later gate that READS it (`is_true` / `trait gte N` etc.). Rename `met_renner` →
`knows_renner` on a shipped game and the earned `true` reads as `undefined` → the prerequisite re-locks → a
one-way arc looks **reset**. **Repurposing** an existing key to a new meaning silently corrupts gate state.

The save-migration backfill (`setup.backfillStateDefaults`, `v2.py:14549`) **adds** any new flag/trait key to
an old save at its default — so *adding* a flag or trait is safe — but it **cannot follow a rename**: to it, the
old key is orphaned data and the new key is just another addition.

*(This "adding is safe" guarantee covers **flags and traits only.** The backfill has no wardrobe/inventory branch,
so **adding a clothing/inventory item** that gates progression is a separate hazard — see §5.)*

**The rule:** on a shipped game, **deprecate-and-add** — leave the old key (or keep its name), add a new one;
never rename or repurpose a live flag/trait key.

---

## §3 — Don't rescale a stat's range or move its tier/stage thresholds
A save preserves the **old number**; the new build **reinterprets** it. Rescale `corruption` 0–100 → 0–10, or
move a `[engine].corruption_tiers` / `<stat>_stage` threshold (`references/trait-catalog.md` §4 — ranges/bands),
and a saved `48` blows past every new tier → the returning player is instantly maxed (or mis-tiered). The
backfill can't help here: the key is present, only its *meaning* changed, so fill-if-absent leaves the stale
number untouched.

**The rule:** once a stat has shipped, freeze its **range** and its **tier/stage thresholds**. Retuning a
one-off numeric *gate* value (`trait gte 40` → `gte 45`) is fine — that's re-evaluated live against the saved
number; it's the stat's own scale/bands that must stay put.

---

## §4 — Don't change the game title
SugarCube namespaces a player's in-browser saves by `Story.domId` = `slugify(StoryTitle)` = `slugify([project].title)`
(the built runtime default `Config.saves.id=Story.domId`). Change the title on a shipped game and the browser
looks under a **new namespace** → the player's existing save slots are gone.

We pin `Config.saves.id` to the stable **project slug** (`v2.py:980` → `:2812`), so *exported* `.save` files
still validate across a title change — but the **in-browser slot namespace is still title-derived**, so a title
change still strands slots.

**The rule:** keep a shipped game's `[project].title` fixed. Iterate the marketing / version label somewhere
else (store page, a `$display_title` line), never the story title.

---

## §5 — A gate-item's grant must be re-assertable, not a one-shot a carried save already burned
The backfill (§2) adds new **flags and traits** to an old save — but it touches `$flags`, player core traits, and
`$npcs` only (`setup.backfillStateDefaults`, `v2.py:14549`); it has **no wardrobe/inventory branch**. So a
**clothing / inventory item you add in a later release than the beat that grants it never reaches a save that
already passed that beat.** Three things line up to strand the player: the flag the grant rides on is already set;
the grant is usually a **one-shot** gated on that very flag (`is_repeatable=false` + `flag is_false`, then it
*sets* the flag), so it can never re-fire; and nothing hands the item over on load. If that item merely flavors a
scene, the returning player loses a costume. If it **gates progression** — a cover, a key, a tool the next beat
requires `equipped` or owned — the save is **soft-locked**: every forward canvas stays shut, and the "go get it"
reaction points at an item that isn't in the wardrobe.

Live-shipped example. Vesper's `cover_analyst` (the Vance disguise) was granted only on the one-shot
`salvage_relaunch` dispatch, which also sets `salvage_relaunched`. The item + its grant landed a release *after*
that dispatch shipped, so every 0.1.4→0.1.5 carry-over had the flag set, never received the kit, and jammed on the
floor forever — `react_calloway_precover` fires on `cover_analyst unequipped` with **no ownership check**, so the
never-granted case looks identical to the took-it-off case, and there was no path to the missing kit.

**The rule:** any item that GATES progression must have its grant **re-assertable at the point of need**, never a
lone burn-once grant. Put an idempotent `wardrobeEffects = [ { action = "add", item_id = "…" } ]` on the
**repeatable** canvas that already reacts to "you don't have it / it's not equipped" (the out-of-cover reaction,
the locked-door bounce, the wardrobe room). `addToWardrobe` is a **no-op if the item is already owned** (the runtime
returns early on a present key), so a normal player who simply took the item off is untouched and sees no
notification — only the stranded save is healed, the instant it lands on that screen. Vesper's fix added exactly
that `add` to `react_calloway_precover`'s `exit_block.config` — the sole canvas a stranded player can reach on that
floor, `is_repeatable=true`, so the heal is guaranteed to find them. Ship the grant on the point-of-need reaction
from the start and the version boundary can never strand it.

---

## §6 — Pre-update checklist (before you re-ship)
*(This file owns what may not CHANGE between releases. The rest of what a release has to clear — meter
ceilings, unpaid promises, the cheat page, the publish flags, the scanners — is `references/ship-gate.md`;
run both.)*
Diff the merged TOML against the **last shipped** one and confirm none of the join keys moved:

```bash
# ids — none renamed/removed (added is fine)
grep -oE '^\s*id\s*=\s*"[^"]+"' games/<slug>/toml_phases/*.toml | sort   # compare vs last ship
# flag + trait keys — none renamed/removed
grep -oE '(flag|trait)\s*=\s*"[^"]+"' games/<slug>/toml_phases/*.toml | sort
# stat ranges + tiers — unchanged
grep -nE 'corruption_tiers|_stage|min\s*=|max\s*=' games/<slug>/toml_phases/*.toml
# game title — unchanged
grep -n 'title\s*=' games/<slug>/toml_phases/1_metadata*.toml
```

**Save-safe to ship freely** (the slug passages + the backfill carry these): add scenes / canvases / NPCs /
traits / flags / locations / quests; insert, reorder, or delete beats inside a canvas; rename any display
`name`/`title`; retune a numeric gate value; fix prose; swap media.

**Save-breaking — needs a deliberate reset (or don't):** rename any `id`; rename or repurpose a live flag/trait
key; rescale a stat or move a tier/stage threshold; change the game title.

When a rename is genuinely unavoidable, treat it as a **major version with an announced save reset** — one clean
break, noted in the release notes — not a silent update.
