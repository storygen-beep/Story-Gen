# The Returning Player — what a new release does to an old save

Every release after v0.1 lands on people who are already playing. They open the new build with a
save written by the old one, and nothing about that is visible to you: the build passes clean, the
gates go green, a fresh start plays perfectly. The damage only exists for the player who loads.

**This file owns what may not CHANGE between releases.** What a release has to *clear* before it
ships is `the-release.md` § Shipping the build. Both, every time.

> v1 carried this as `save-safety.md`. v2 shipped without it for its whole life, which is why
> nothing in this skill could tell an author that renaming an id strands a save. Restored
> 2026-08-29, corrected against the engine as it stands today — five of v1's `file:line`s had
> drifted and one of its central claims had stopped being true.

---

## The model — why a save can break at all

A SugarCube save stores two things: the **passage the player is parked on**, by name, and
**`State.variables`** — `$player`, `$npcs`, `$flags`, `$game_state`. On load the engine restores
that state and re-renders that passage.

**It does not re-run `:: Start`.** That single fact is the whole subject. Every default your new
release writes in `:: Start` — a new flag, a new meter, a new NPC, a whole new system — is invisible
to a save that predates it. The variable is not zero. It is `undefined`, and the first thing that
reads it throws.

So a save is joined to the new build through four keys: **passage names**, the **`$npcs` key**, the
**flag/trait key**, and **the meaning of a number**. The engine holds the first two stable for you
(both are your authored slugs, never regenerated ids) and repairs a growing part of the third. The
sections below are the part **you** own — the changes that still move a key out from under a save
that already exists.

---

## §1 — What the engine repairs for you, and what it cannot

`setup.backfillStateDefaults` (`v2.py:16011`) runs from the `:passagestart` handler (`v2.py:16164`)
on **every passage**, and fill-if-absent merges the current default skeleton
(`setup.stateDefaults`, `v2.py:3244`) into whatever the save carries. It never overwrites a value
the player earned, and it is idempotent.

**Add these freely. They reach an existing save on the next screen.**

| | |
|---|---|
| a new flag | ✅ |
| a new player meter | ✅ |
| a whole new NPC | ✅ — the entire record, deep-copied |
| a new meter or flag on an existing NPC | ✅ |
| a new `$game_state` sub-map | ✅ |
| **turning on a whole system** — phone, rent, passes, inventory, clothing | ✅ |
| a new key inside an engine sub-map (`phone.matches`, `fast_jobs.cooldowns`) | ✅ |

That last block is new as of 2026-08-29. Before it, the backfill knew three keys, and switching the
phone on in a patch release left `$game_state.phone` undefined in every save in the wild — with no
symptom until a player opened the phone.

**The depth is deliberately not uniform, and you should know which side you are on.**
`$game_state` sub-maps are filled one level in, because everything non-empty down there is engine
bookkeeping. **`$player` is filled at the top level only**, because `$player.wardrobe` is an
id → garment map: filling into it would hand back a garment the player sold, discarded or was
stripped of. Same for `equipped`.

**Nothing below is repaired, by this or anything else:**

- a key you **renamed** — the old one is orphaned data, the new one is just another addition
- a key you **removed** — the save keeps it forever, and any gate still reading it is now lying
- a key whose **meaning** you changed — the number is present, so fill-if-absent leaves it alone
- **anything the save already consumed** — see §6, which is the one that has actually bitten us

---

## §2 — Slugs are immutable release ids

Every passage is named from slugs: `Canvas_<canvasSlug>_Node_<nodeSlug>`
(`v2.py:12376`) and `Location_<locSlug>` (`v2.py:12389`). `$npcs` is keyed by the NPC's TOML `id`
(`game_graph.py:144`), locations by theirs (`:190`), nodes by `"<canvas>.<node>"` (`:376`).

A save stores the passage it is parked on — `Location_wren_room`,
`Canvas_loop_renner_office_Node_base_r` — and its NPC, wardrobe and quest state under those slugs.

**So:** rename the `id` of a `[[canvases]]`, `[[canvases.nodes]]`, `[[locations]]`, `[[npcs]]`,
`[[clothing_items]]`, `[[quests]]` or `[[fast_jobs]]` on a shipped game, and the save points at a
passage that no longer exists — the player lands nowhere — or an NPC, outfit or quest silently
vanishes.

**The rule: every TOML `id` is a permanent release identifier.** Change display names freely — `name`,
`title`, every word of prose; players never see an id. Never change the `id` itself. Inserting,
reordering and deleting nodes inside a canvas is safe *because* passages are slug-named rather than
positional. Only a rename breaks.

---

## §3 — Never rename or repurpose a live flag or trait key

`$flags` is keyed by flag name, traits by their key. That string **is** the runtime join between the
scene that SET it and the gate that READS it. Rename `met_renner` → `knows_renner` on a shipped game
and the earned `true` reads as `undefined`: the prerequisite re-locks, and a one-way arc looks to the
player like it reset. **Repurposing** a live key to a new meaning is worse — it corrupts gate state
without leaving a mark.

**The rule: deprecate and add.** Leave the old key where it is, add a new one beside it. The backfill
adds; it cannot follow a rename.

---

## §4 — Don't rescale a stat, or move its tier thresholds

A save preserves the **old number**; the new build **reinterprets** it. Rescale `corruption` from
0–100 to 0–10, or move a `[engine] corruption_tiers` band, and a saved `48` blows past every new
tier — the returning player is instantly maxed, or mis-tiered into content they never earned.

The backfill cannot see this: the key is present, only its meaning moved, so fill-if-absent leaves
the stale number exactly where it is.

**The rule: once a stat ships, freeze its range and its bands.** Retuning an individual gate value
(`trait gte 40` → `gte 45`) is fine — that is re-evaluated live against the saved number. It is the
stat's own scale that must stay put.

---

## §5 — Don't change the game title

We pin `Config.saves.id` to the stable project slug rather than the SugarCube default
(`v2.py:3208`), so an **exported** `.save` file still validates across a title change.

The in-browser slots are a different store. SugarCube namespaces them by `Story.domId`, which is
`Util.slugify(title)` — the save store is created as `SimpleStore.create(Story.domId, …)` in
`format.js`. Change `[project] title` on a shipped game and the browser looks under a new namespace:
every existing slot is simply gone.

**The rule: a shipped game's `[project] title` is fixed.** Version labels and marketing names live on
the portal entry and in `[project] version` (`engine.md` §38), never in the story title.

---

## §6 — A gate-item's grant must be re-assertable, not a one-shot the save already burned

This is the one that has actually shipped and stranded real players, and §1's improvements do **not**
fix it. The backfill fills `$player.wardrobe` only when the map is absent entirely, and it fills it
with the game's *starting* garments. An item granted by a beat is not in that skeleton and never
will be.

Three things line up to strand the player:

1. the flag the grant rides on is **already set** in the old save
2. the grant is a **one-shot** gated on that very flag (`is_repeatable = false`, `flag is_false`, and
   then it *sets* the flag) — so it can never fire again
3. nothing hands the item over on load

If the item flavours a scene, the returning player loses a costume. If it **gates progression** — a
cover, a key, a tool the next beat needs owned or equipped — the save is **soft-locked**: every
forward canvas stays shut, and the "go and get it" reaction points at something not in the wardrobe.

> **Shipped example.** Vesper's `cover_analyst` was granted only on the one-shot `salvage_relaunch`
> dispatch, which also sets `salvage_relaunched`. The item and its grant landed a release *after*
> that dispatch shipped. Every 0.1.4 → 0.1.5 carry-over had the flag set, never received the kit, and
> jammed on that floor forever — `react_calloway_precover` fires on `cover_analyst unequipped` with
> **no ownership check**, so never-granted and took-it-off look identical, and there was no path to
> the missing kit. Fixed in 0.1.6.

**The rule: any item that gates progression carries its grant on the repeatable point-of-need
reaction, never on a lone burn-once grant.** Put an idempotent
`wardrobeEffects = [ { action = "add", item_id = "…" } ]` on the canvas that already reacts to *you
don't have it / it isn't on* — the out-of-cover reaction, the locked-door bounce, the wardrobe room.
`setup.addToWardrobe` returns early when the item is already owned (`v2.py:1555`), so a normal player
who merely took it off is untouched and sees no notification. Only the stranded save is healed, the
instant it lands on that screen.

Ship the grant that way from the start and the version boundary can never strand it.

---

## §7 — Every save says which release wrote it

`$game_state` carries four provenance fields, and they are the first thing to ask a bug reporter for:

| | |
|---|---|
| `origin_version` / `origin_schema` | the release the playthrough **started** on. Written once by `:: Start`; the backfill can never overwrite it. **`null` means the save predates the stamp** — honestly unknown, not "started here". |
| `last_version` / `last_schema` | the release **currently running**, restamped by `:passagestart` whenever it changes |

`*_schema` is a fingerprint of the trait/flag key surface and the corruption tiers
(`Config.saves.version`, `v2.py:3209`). Two builds with the same number are join-compatible on
everything §3 and §4 govern; two different numbers mean something in that surface moved.

**A mismatch is recorded, never refused.** `Config.saves.onLoad` (`v2.py:3230`) logs the comparison
and returns. Throwing from there would abort the load with a dialog — that *is* the reject-on-mismatch
handler the stamp was minted for, and it stays unused on purpose: the backfill heals the mismatches a
player can actually hit, and refusing a save costs somebody their whole run over a difference they
cannot act on.

---

## §8 — Before you re-ship

The comparison that matters is against **the last build you actually shipped**, which is why
`the-release.md` step 3 archives it to `games/<slug>/releases/v<version>.html`. Without that file
there is nothing to diff and this section cannot be done at all.

What must not have moved, in order of how badly it hurts:

- **ids** — canvases, nodes, locations, NPCs, clothing items, quests, fast jobs. Added is fine;
  renamed or removed is not.
- **flag and trait keys** — same rule.
- **stat ranges and `corruption_tiers` bands** — frozen.
- **`[project] title`** — frozen.

Safe to ship freely, because the slug passages and the backfill carry them: new scenes, canvases,
NPCs, meters, flags, locations, quests, whole systems; inserting, reordering or deleting beats inside
a canvas; renaming any display `name` or `title`; retuning a numeric gate value; prose; media.

⚠️ **There is no machine check for this yet**, and that is a stated gap rather than an oversight —
`DOCTRINE_GAPS.md`. Four greps in a row would be a checklist, and this skill's evidence on checklists
is unambiguous: v1's thirteen-point pre-ship audit was followed by the exact bug it existed to
prevent. Until a `gates.py` mode reads the archived build and compares its join keys to the current
one, this is a human diff, and the honest thing to do is say so.

When a rename is genuinely unavoidable, it is a **major version with an announced save reset** — one
clean break in the release notes, never a silent update.
