# The state-reactive player portrait — the resolver, the TOML, the traps, enabling

Read this when the game shows a **player portrait in the sidebar that changes with state** — a different
finished image as she dresses/undresses, changes outfit, corrupts, or gets pregnant (the Road-to-Success
discrete-swap pattern: one finished image per state, NOT a layered paperdoll). It is an **opt-in** engine
feature: author a `[player_portrait]` block and it appears in the sidebar just below the time display; omit it
and the game is byte-identical (feature off, no error). It is the reactive *extension* of the single static
`$player.portrait` that `references/customization.md` owns (that one is set once at character creation and
only renders on the Stats page; this one re-renders every passage).

**Every engine claim here is verified against live code** (`v2.py` = the comprehensive generator;
`template_import.py` = the importer/validator), cited `file:line`.

## Contents
- §1 — What it reacts to (the four axes) + where it renders
- §2 — The resolver (`getPlayerPortrait()`) — priority order + dominant-slot keying
- §3 — The `[player_portrait]` TOML
- §4 — The traps (corruption is a LEVEL; Preg is dressed-only; images must be declared)
- §5 — Image budget + the missing-image fallback
- §6 — Enabling / scoping checklist

---

## §1 — What it reacts to, and where it renders

The portrait resolves ONE image filename from up to four axes:

| Axis | Source | Read via |
|---|---|---|
| **Undress level** | which of `top`/`bottom`/`dress`/`bra`/`underwear` slots in `$player.equipped` are filled | `setup.getUndressLevel()` (`v2.py:1454`) → `naked`/`topless`/`bottomless`/`underwear`/`dressed`. **Only meaningful when clothing is enabled** — returns `null` otherwise. |
| **Worn outfit type** | the `type` tag of the **dominant** worn garment (`equipped.dress \|\| top \|\| bottom`) | looked up in `setup.clothing_data` (the same map `getWornTypes` uses, `v2.py:1388-1407`) |
| **Corruption** | `$player.core_traits.corruption` bucketed to a **LEVEL 0–4** | `setup.getCorruptionLevel()` (`v2.py:5622`, tiers `[0,5,15,30,45]`) |
| **Pregnancy** | a hidden `$player.core_traits.<pregnancy_trait>` int (declared + suppressed like any stage trait) | read directly in the resolver |

**It renders in `StoryCaption` just below the `<<timeDisplay>>`** (the time/clock stays at the very top) and
above the stats + the configurable `<<sidebarItems>>` — via the `<<playerPortrait>>` widget (`v2.py:15615`),
mounted by a `portrait_line` fragment gated on the enable flag (`v2.py:14850`), the exact idiom the phone
button uses. The widget is a thin
`<img @src="_pimg">` (SugarCube attribute directive — `@src="_pimg"`, NEVER `src="@_pimg"`, `v2.py:14778`)
that hides itself via `onerror` if a file is missing. The engine emits `setup.player_portrait` +
`setup.player_portrait_enabled` **unconditionally** (`v2.py:2951`) so a disabled game never throws.

**Framing (baked into the engine, `.sidebar-player-portrait img`).** The widget carries its own CSS: the image
is fit to the sidebar width and cropped to a **3:4 portrait box, `object-fit: cover`, centred a touch high
(`object-position: 50% 18%`)** — so a square or tall source shows the **face/torso**, not the legs or a
background edge (without this the raw img renders at natural size and overflows the narrow sidebar). **Author
implication:** source portrait-composition art — subject centred, face in the upper third — and any aspect works;
a full-figure or landscape shot will be cropped to her middle-upper region.

---

## §2 — The resolver (`getPlayerPortrait()`, `v2.py:1466`) — priority order

The engine walks these in order and returns the FIRST image it resolves (then applies the Preg suffix):

1. **Undress override — only when `clothing_enabled`.** `getUndressLevel()` reads `$player.equipped` and asks,
   per body-area, *is anything covering it?* — **the bra covers the top, the briefs (`underwear` slot) cover the
   bottom**, and a `top`/`bottom`/`dress` covers the corresponding outer area (`v2.py:1454`):
   `topCovered = top||dress||bra`, `bottomCovered = bottom||dress||underwear`, `hasOuter = top||bottom||dress`.
   → both bare → `naked_image`; top bare (not even a bra) → `topless_image`; bottom bare (not even briefs) →
   `bottomless_image`; both covered by ONLY bra/briefs (no outer) → `underwear_image`; else **dressed** (fall
   through). So on a dress+bra+briefs wardrobe: dress off = underwear, + bra off = topless, + briefs off =
   bottomless, all off = naked — no split top/bottom garments required. When clothing is off this whole branch
   is skipped (there is no `equipped` object). *(Fires only if that image key is declared — an undeclared axis
   falls through to the outfit rules / `default_image`.)*
2. **Dressed → the outfit rules.** One canonical outfit type is taken from the **dominant slot**
   (`equipped.dress || top || bottom`) → its `.type` in `setup.clothing_data`. The engine walks
   `[[player_portrait.outfits]]` **first-match-wins**; each rule's `when` = `{ worn_type?,
   corruption?:{operator,value}, flag? }`. `worn_type` must equal the dominant type; `corruption` compares
   the **LEVEL** (see §4) with `operator` ∈ `gte/gt/lte/lt/eq`; `flag` checks `$flags`. No rule matches →
   `default_image`.
3. **Pregnancy suffix.** If `pregnancy_trait` is set and truthy on `$player.core_traits`, the engine
   inserts `pregnancy_suffix` before the file extension (split on the last dot, so `.jpg/.png/.webp` all
   work): `casual.jpg → casualPreg.jpg`. **Applied to dressed/outfit images only** — undress overrides
   (naked/topless/…) are never suffixed.

Nothing resolves → returns `''` and the widget renders nothing (the static `$player.portrait` on the Stats
page is untouched).

> **Why dominant-slot, not "worn types include X":** the resolver keys on ONE garment (`dress||top||bottom`),
> not the *set* of all worn `type` tags. If it used set-membership, a schoolwear top + casual bottom would
> match whichever rule the author happened to list first — the image would depend on rule order, not on
> what she's actually wearing. Dominant-slot gives one deterministic answer per render.

---

## §3 — The `[player_portrait]` TOML

Top-level block (like `[phone]`, NOT under `[settings]`). Image paths are relative to the game's media
folder (the same place clothing/NPC images live); the engine prefixes `video_path` and tracks them for
copying, so **every image you name gets copied into the build** — but only if it's actually declared here
(a runtime-only path won't copy; see §4 on Preg).

```toml
[player_portrait]
enabled          = true
# generic undress overrides (shown regardless of outfit; only fire when clothing is enabled)
naked_image      = "portraits/naked.webp"
topless_image    = "portraits/topless.webp"
bottomless_image = "portraits/bottomless.webp"
underwear_image  = "portraits/underwear.webp"
# fallback when dressed but no outfit rule matches
default_image    = "portraits/casual.webp"
# pregnancy: insert this suffix before the extension of the DRESSED image when the trait is set
pregnancy_trait  = "pregnancy"
pregnancy_suffix = "Preg"          # casual.webp -> casualPreg.webp

# outfit rules — FIRST MATCH WINS, so order specific -> general
[[player_portrait.outfits]]
image = "portraits/school_slutty.webp"
when  = { worn_type = "school", corruption = { operator = "gte", value = 3 } }   # LEVEL 3, not 30 points

[[player_portrait.outfits]]
image = "portraits/school.webp"
when  = { worn_type = "school" }

[[player_portrait.outfits]]
image = "portraits/swim.webp"
when  = { worn_type = "swim" }
```

For an outfit rule to fire, a `[[clothing]]` item in the dominant slot must carry the matching `type`
tag (`references/clothing.md` §6 — the `type` catalog). The whole undress axis needs `clothing_enabled`
in `[settings]`; without clothing, only `default_image` + corruption/flag outfit rules apply.

---

## §4 — The traps (green build, silent wrong image)

- **`corruption.value` is a LEVEL 0–4, NOT raw points.** It's compared against `getCorruptionLevel()`
  (`v2.py:5622`), which buckets points via tiers `[0,5,15,30,45]` → 0/1/2/3/4. Writing `value = 30`
  (thinking "30 corruption points") is a rule that **never matches** — `getCorruptionLevel` never returns
  more than 4. Use the LEVEL: `value = 3` ≈ 30 points on default tiers.
- **First-match ordering.** `[[player_portrait.outfits]]` is walked top-to-bottom; put the most specific
  rule (e.g. `worn_type` + high `corruption`) ABOVE the bare `worn_type` catch-all, or the general rule
  eats the specific one.
- **Preg variants must exist + be findable.** The `<name><suffix>.<ext>` file is a *runtime-derived*
  path — the engine also asset-tracks it, but **only if the file is present in the media folder** at build
  time. Ship `casualPreg.webp` next to `casual.webp`; a missing Preg file just falls back via `onerror`.
- **Dominant-slot, not mixed.** See §2 — the outfit image reflects `dress || top || bottom`, so a
  top-only outfit change won't switch the image if a `dress` is (still) equipped.
- **Keep `worn_type` coverage in sync with the wardrobe — the drift that rots over time.** Because the
  portrait keys on the clothing item's `type` (not per-item), adding a garment of an **existing** type
  needs no new art — but **adding a garment of a NEW `type` with no matching `[[player_portrait.outfits]]`
  rule silently shows `default_image`** (wrong picture, green build). The importer catches it: a build
  **warning** `player_portrait: clothing type 'X' has no outfit rule …` (and a `worn_type` no clothing
  carries is flagged a **dead rule**) — `template_import.py` validator. **The discipline: every time you
  add a clothing `type`, add a portrait rule + image for it.** This is the #1 way a portrait rots as the
  wardrobe grows.

---

## §5 — Image budget + fallback

Keep it to **one dominant axis + generic undress**: ~one image per named outfit (Road to Success ships
~31) + the **4 generic undress** images (naked/topless/bottomless/underwear) + a `default`. That's ~35 base.
Pregnancy roughly doubles the *dressed* set if you ship Preg variants (undress overrides don't get them).
Do NOT cross axes into per-outfit-per-undress art (31×5 explosion) — undress overrides are generic by
design. Any missing file degrades gracefully: the `<img onerror>` hides itself, so a partial set is safe to
ship and grow (`references/media.md` — art acquisition + the silhouette fallback pattern).

---

## §6 — Enabling / scoping checklist

- **OFF until declared.** No `[player_portrait]` block → the widget/mount aren't emitted; the sidebar is
  unchanged. There is nothing to "turn off."
- **Enable** with `enabled = true` in the top-level `[player_portrait]` table (NOT under `[settings]`;
  `references/engine-reference.md` §7).
- **The undress axis needs clothing** (`clothing_enabled` in `[settings]`, `references/clothing.md` §9).
  A corruption-only game can still use the portrait — it just resolves via outfit rules keyed on
  corruption/flags + `default_image`, with no undress overrides.
- **Declare every image** in the block (undress + default + each outfit + any Preg variant) and drop the
  files under the media folder, or they won't copy into the build.
- **Keep it in sync as the wardrobe grows** — every new clothing `type` wants a matching outfit rule +
  image, or wearing it shows `default_image` (the importer warns at build; §4).
- **Seed decision:** whether the game has a reactive portrait is a `references/step-0-1-seed.md` yes/no;
  place the outfit/image set at blueprint time (`references/step-5-blueprint.md` §5F).

## Cross-references
- `references/customization.md` — the static `$player.portrait` (set once at creation) this feature extends.
- `references/clothing.md` — the `type` tags + undress states the resolver reads; the `[settings]` enable.
- `references/hud.md` / `references/trait-catalog.md` §5 — the always-on sidebar surface this sits atop.
- `references/media.md` — sourcing the images + the `onerror` fallback.
- `references/engine-reference.md` §7 — the `[player_portrait]` enable-switch home + field map.
