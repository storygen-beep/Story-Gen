# Customization — player/NPC personalization + the `@`-token output contract

Read this when the seed says the player or any NPC is **customizable** — name, build, a
portrait look, an NPC rename, a relationship label — or when you're about to write prose
that mentions a customizable name. The screen is **auto-built**; the work is two-sided:
**declare the inputs (TOML) AND emit the output tokens (`@player` / `@<npc>` in prose).**
Declaring the field is *half* the job — a customized value only appears where you wrote a
token. The other half is keeping the chosen name OFF un-tokenized surfaces (location names,
sidebar labels) that print the raw default.

No engine change is needed — the whole system ships. Every engine claim below is cited
`file:line` against live code (`v2.py` = comprehensive generator, `template_import.py` =
importer/validator). Cross-link: the one-line trap is the Customization row in
`references/systems.md`.

## Contents
- §1 — What it is (two opt-in surfaces)
- §2 — The `@`-token output contract (the heart) — every form + where it resolves
- §3 — The un-tokenizable-surface trap (R2)
- §4 — TOML: `[[player.customization_fields]]` + per-NPC shape
- §5 — Engine guard-rails (verified line numbers)
- §6 — When to make it customizable (and when not)
- §7 — Enabling checklist

---

## §1 — What it is

Two independent, opt-in surfaces. If **either** exists, the engine inserts an auto-built
`CustomizeCharacters` passage and redirects `Start` to it — `if customizable_npcs or
has_player_customization: start_target = "CustomizeCharacters"` (`v2.py:933-934`); the
passage is emitted at `v2.py:8729` (`_generate_customize_passage`). You author **zero** passage plumbing.

- **Player customization** — a start-of-game screen where the player sets fields you declare
  (`name`, `build`, a portrait `look`). The RTS-genre opener: name yourself, pick a body
  type, choose a starting look. A `text`/`select` value lands in `$player.<id>`; `id="name"`
  writes `$player.name` (the canonical name the whole engine reads).
- **NPC customization** — per-NPC, the player **renames** the character and picks a
  **relationship label** from a list you supply (`step-dad` / `mom's boyfriend` /
  `landlord`). The genre's relationship toggle: the same arc, reframed by player choice. The
  chosen name lands in `$npcs[slug].name`, the relationship in `$npcs[slug].relationship`.

---

## §2 — The `@`-token output contract (the part everyone forgets)

A customized value appears in the story ONLY where you wrote the substitution token. There
is **exactly one token syntax**, and it is resolved in **two twin places** depending on the
render path:

| Token in your prose | Becomes (gen-time) | Reads |
|---|---|---|
| `@player` | `<<print $player.name>>` | the player's chosen name |
| `@player.<field>` | `<<print $player.<field> \|\| "">>` | any player field (`@player.build`) |
| `@<npc>` | `<<print $npcs["<slug>"].name>>` | that NPC's chosen name |
| `@<npc>.rel` | `<<print $npcs["<slug>"].relationship \|\| "">>` | that NPC's relationship label |

`<npc>` is the slug **without** the `npc_` prefix — `@cole` for `npc_cole`, `@frank` for
`npc_frank`. **An unrecognized `@word` is left untouched** (`if not uuid: return
match.group(0)`, `v2.py:13303-13304`) — safe to write literal `@`s, but see the handle
collision below. **Possessives just work:** `@cole's place` → `<<print …name>>'s place` →
"Jamie's place". Dialog **speaker labels** are already dynamic (rendered from `npcId`) —
tokenize only the dialog *body*, never the speaker tag.

### Where each form resolves — two twins, by render path

The token grammar is `@(\w+(?:\.\w+)?)` in both. The difference is *who runs it*:

| Render path | Resolver | `file:line` | Surfaces it covers |
|---|---|---|---|
| **Passage-body text** (gen-time, → `<<print>>` macro) | `_resolve_at_references` | `v2.py:13266`; called on block content `v2.py:13824`, location description `v2.py:9267`/`:9314`, blocked-message `v2.py:9276` | paragraph / heading / **dialog body** / location description / blocked-passage message |
| **`<<link>>` / choice text** (gen-time, → JS concat expr) | `_resolve_at_references_expr` | `v2.py:13313`; called `v2.py:11899` | choice / link button text (can't take `<<print>>`, so it builds a JS string expression) |
| **Phone authored text** (runtime, JS — rendered as DATA, not a passage body) | `setup.resolveAtRefs` | `v2.py:2925`; called at every phone render point — notify toasts `v2.py:1877`/`:1888`, message bubbles `:2217`, reply buttons `:2242`, daily-chat `:2253`/`:2255`, daily-topic buttons `:2287`/`:2307`, thread preview `:2153` | phone `notify`, message `content`, `daily_topics`, reply text |

*The phone is the latent leak site.* Phone content renders as JavaScript data, so the
gen-time `_resolve_at_references` never touches it — that's why a **runtime twin**
(`setup.resolveAtRefs`, `v2.py:2925`) exists and is now wired into every phone render point
above. So `@<npc>` / `@player` tokens **do** resolve in phone `notify` / message `content` /
`daily_topics`. The thread title, avatar, and preview read live `$npcs[slug].name`, so they
honor a rename even *without* a token.

Both resolvers rely on `setup.npc_slug_map` (slug→canonical slug — identity now that npc ids ARE slugs; it
also maps bare aliases like `"renner"`→`"npc_renner"`), populated at `v2.py:802`/`:806` and
emitted to JS at `v2.py:2818` — so `@<npc>` works the same gen-time and runtime.

> **Rule R1 — if a character is `customizable`, EVERY player-visible mention of their name in
> prose MUST be the token.** Renamed-Cole game with a hardcoded "Cole" left in a paragraph =
> a visible bug. Same for `@player` once the player can rename themselves. Every relationship
> mention → `@<npc>.rel`.

**The `@handle` collision (R4):** the regex matches any `@word`. Social-feed handles in phone
content — `@lexiluv_`, `@samantha_x` — that don't match a known NPC slug are left as literal
text (fine). **But** a handle that collides with an NPC short-name *will* be substituted
(`uuid` found → rewritten). Keep social handles distinct from NPC slugs, or accept the
rewrite.

---

## §3 — The un-tokenizable-surface trap (R2)

The `@`-token fires only where a resolver runs (§2). It does **NOT** reach structural labels
the engine prints **raw**. Verified raw surfaces:

- **Location names** — `<h2>{location.name}</h2>` (`v2.py:9204`, `:9266`, `:9286`, `:9313`)
  is the literal TOML name; no resolver in the title path. (The location *description* below
  it IS resolved, `v2.py:9267` — so the prose tokenizes, the title doesn't.)
- **Sidebar item `label`s** — printed as raw text content (e.g. the `trait_bar` label at `v2.py:15275`, `<<print _traitLabel>>` raw),
  never wrapped in `resolveAtRefs`. A `"Cole Relation"` bar label stays "Cole Relation".
- **Quest / stage / arc_stage display strings** — printed raw.
- The customize-screen NPC `description` intro — printed raw (html-escaped).

> **Rule R2 — never bake a customizable name into a location name / sidebar label / quest
> label.** A location `"Cole's Apartment"` stays "Cole's Apartment" after the rename — the
> exact leak the feature exists to prevent. **Genericize the label, carry the specificity in
> the prose** (which tokenizes): location → `"The Apartment Across Town"`; sidebar bar →
> `"Closeness"`; locked tooltip → `"Once he's noticed you"`.

*(Canvas/node `name` fields are dev-only — Canvas-Review page + dev banner, never a
production player build — so those may keep the literal name.)*

---

## §4 — TOML: declare the inputs

### Player fields — `[[player.customization_fields]]`

Array-of-tables, placed **after** every `[player.*]` subtable (TOML scoping — a bare
`[[player.customization_fields]]` after a `[player.core_traits]` table is correct; before it
would re-open the wrong scope). Parsed at `template_import.py:1492-1518`.

```toml
[player]
id          = "player"
name        = "MC"
customizable = true        # turns the screen on

# ... [player.core_traits] etc. ...

[[player.customization_fields]]
id    = "name"             # id="name" → writes $player.name (canonical)
type  = "text"             # → a textbox
label = "Your name"
default = "Alex"

[[player.customization_fields]]
id    = "build"
type  = "select"           # → a dropdown; needs options
label = "Body type"
options = ["slim", "average", "curvy", "athletic"]
default = "average"        # must be in options

[[player.customization_fields]]
id    = "look"
type  = "image_select"     # → clickable image grid; each option {id,image,label}
label = "Starting look"
sets_portrait = true       # image_select-ONLY: the pick becomes $player.portrait
options = [
  { id = "look_a", image = "looks/a.png", label = "Soft" },
  { id = "look_b", image = "looks/b.png", label = "Sharp" },
]
```

Field types (validator `template_import.py:3018`): `text` → textbox · `select` →
dropdown (needs `options`, `default` must be a member) · `image_select` → image grid (each
option a table with `id` + `image`; `sets_portrait` makes the pick `$player.portrait`).
Missing art degrades gracefully (the `<img>` hides on error, the label still shows) — safe
to ship the field before art lands.

### NPC customization — per-NPC

Parsed at `template_import.py:1604-1606`. **Rename and relationship-picker ship together —
there is no rename-only mode.** A `customizable` NPC MUST declare `relationship` (the
default) AND `relationship_options` (the picker list), and the default must be in the list:

```toml
[[npcs]]
id   = "npc_cole"
name = "Cole"                      # the seed/default name; the rename textbox is seeded with it
customizable = true                # → rename textbox + relationship dropdown on the screen
relationship = "boyfriend"         # the default (must be a member of relationship_options)
relationship_options = ["boyfriend", "old flame", "ex", "roommate"]
```

Then in prose: `@cole` for his name, `@cole.rel` for the relationship label.

---

## §5 — Engine guard-rails (verified line numbers)

The corpus draft's line numbers had drifted; these are read from current code.

| Guard-rail | What it enforces | `file:line` (verified) |
|---|---|---|
| **Reserved `$player` IDs** | a field `id` may not be `portrait`, `current_location`, `core_traits`, `flags`, `wardrobe`, `equipped` → error | `template_import.py:3005` (set), `:3016-3017` (check) |
| **Field id is lowercase snake_case + unique** | bad id / dup id → error | `:3011-3014` |
| **`select` needs `options`; `default` ∈ options** | missing options / out-of-set default → error | `:3020-3024` |
| **`image_select` needs `options` with `id`+`image`** | missing → error | `:3025-3036` |
| **`sets_portrait` is `image_select`-only** | `sets_portrait` on a text/select field → error | `:3037-3038` |
| **Customizable-NPC hard-fail** | `customizable` NPC missing `relationship` OR `relationship_options`, OR default ∉ options → error | `:3417-3429` |

All raise through the validator's `errors.append(...)` path → the import fails (not a silent
no-op). *(Code-vs-lore note: the corpus cited reserved-IDs ~3005 ✓ exact, NPC hard-fail
~3420-3429 → real block is `3417-3429`, `sets_portrait` ~3037 → `3037-3038`. The token
processor it placed at `v2.py:12658` is now `v2.py:13266`, and the JS twin `v2.py:2722` is
now `v2.py:2925`. Code wins; numbers above are live.)*

---

## §6 — When to make it customizable (and when not)

Keep it **narrow + non-destructive**. The cheap, natural wins:

- **Player** — name + build + look, when the protagonist is a blank-ish self-insert (the RTS
  default). **Don't** sweep `@player` across a written, named protagonist whose prose leans
  on third-person narration by name — retrofitting `@player` over hundreds of "she did X"
  lines fights the grain and buys little. Demonstrate the field types in one arc rather than
  rewriting the whole third-person script (a deliberate, scoped choice).
- **NPC** — customizable when the relationship framing is a genuine player fantasy axis (the
  step-relative toggle) **and** the cost is bounded — the name isn't baked into many
  structural labels (§4) and isn't **premise-load-bearing**. A dating love-interest is the
  cheapest candidate. A sibling whose siblinghood *is* the story is the most expensive and
  most destructive — if the relationship the plot depends on can be renamed to "roommate,"
  the premise breaks. **Fixed, premise-load-bearing identities should NOT be customizable.**

---

## §7 — Enabling checklist

1. `[player].customizable = true` + ≥1 `[[player.customization_fields]]` (array-of-tables
   **after** every `[player.*]` subtable).
2. For each customizable NPC: `customizable = true` + `relationship` + `relationship_options`
   (default ∈ options) — both required or the import hard-fails (§5).
3. Every player-visible name mention → `@player` / `@<npc>`; every relationship → `@<npc>.rel`
   (R1) — across prose, dialog bodies, choice text, AND phone content (§2).
4. Every structural label that named the character → genericized (R2): location names,
   sidebar labels, quest/stage strings.
5. No engine wiring — the `CustomizeCharacters` screen and the `Start` redirect are automatic
   (`v2.py:933`).

**Pre-build greps:** for each customizable NPC slug, `grep -n '\bCole\b'
games/<slug>/toml_phases/*.toml` should return only structural-label lines you deliberately
genericized — any prose hit is a missed `@cole` (R1). Confirm no customizable name survives
in a `[[locations]] name` or `[[sidebar_items]] label`.

---

## Cross-references
- **The one-line trap + system index:** `references/systems.md` (Customization row).
- **Sibling opt-in systems** (same "declare-the-input, write-the-output" shape):
  `references/clothing.md`, `references/toml-gotchas.md` (rent `[settings.rent]`, phone
  `[phone]`, day-system shapes).
- **`version = "1.0"` on every conditions block, declare-before-use, field-name reference**
  → `references/toml-gotchas.md`.
- **Sidebar primitives the labels live on** (and why a banded label must stay generic) →
  `references/trait-catalog.md` §5.
