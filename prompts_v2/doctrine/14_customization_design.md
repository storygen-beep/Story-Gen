# Doctrine 14 — Player & NPC Customization Design

How to let the player personalize themselves and the cast at game start — name, build,
look, NPC names, NPC relationship labels — and, critically, how to make those choices
actually **show up** in the writing. Sibling of [doctrine/11 clothing], [doctrine/12 rent],
[doctrine/13 phone]: another free engine surface that ships fully built but is easy to
half-use (declare the inputs, forget the output token).

The engine is fully shipped — importer `template_import.py:62–89` (player) / `:107–117`
(NPC), validator `:2906–2943` / `:3289–3304`, runtime `v2.py:8376` (the auto-built
`CustomizeCharacters` passage) + `v2.py:12658` (the `@`-token processor). **No engine
change is needed to use it.**

---

## §1 — What it is (and the RTS parallel)

Two independent surfaces, both opt-in:

- **Player customization** — a start-of-game screen where the player sets fields you
  declare (`name`, `build`, a portrait `look`, anything). RTS-of-this-genre games open on
  exactly this: name yourself, pick a body type, choose a starting look.
- **NPC customization** — per-NPC, the player can **rename** the character and pick a
  **relationship label** from a list you supply (e.g. `step-dad` / `mom's boyfriend` /
  `landlord`). This is the genre's relationship-toggle: the same arc, reframed as a
  step-brother *or* a roommate, by the player's choice.

The screen is **auto-generated and auto-wired**. If any `[player].customizable = true`
field or any `customizable` NPC exists, the engine inserts a `CustomizeCharacters` passage
and redirects `Start` to it (`v2.py:830–837`). You author **zero** passage plumbing — you
declare the fields and write the prose with tokens.

---

## §2 — The free engine features

| Feature | Declared in | Renders as |
|---|---|---|
| Player text field (name, etc.) | `[[player.customization_fields]]` `type="text"` | a textbox |
| Player choice field (build, etc.) | `type="select"` + `options` | a dropdown |
| Player portrait picker | `type="image_select"` + `options` + `sets_portrait` | an image grid; the pick can become `$player.portrait` |
| NPC rename | NPC `customizable = true` | a textbox seeded with the default name |
| NPC relationship label | NPC `relationship` + `relationship_options` | a dropdown |

A `text`/`select` value lands in `$player.<field_id>`. `id = "name"` is special — it writes
`$player.name` (the canonical name the whole engine reads). An NPC's chosen name lands in
`$npcs[uuid].name`, the relationship in `$npcs[uuid].relationship`.

---

## §3 — The `@`-token contract (the part everyone forgets)

Declaring the fields is half the job. A customized value only *appears* in the story if you
write the prose with the substitution token. **There is exactly one token syntax**, processed
at generation time (`_resolve_at_references`, `v2.py:12658`):

| Token in your prose | Becomes | Reads |
|---|---|---|
| `@player` | `<<print $player.name>>` | the player's chosen name |
| `@player.<field>` | `<<print $player.<field> \|\| "">>` | any player field (e.g. `@player.build`) |
| `@<npc_short>` | `<<print $npcs["uuid"].name>>` | that NPC's chosen name |
| `@<npc_short>.rel` | `<<print $npcs["uuid"].relationship \|\| "">>` | that NPC's relationship label |

`<npc_short>` is the NPC slug **without** the `npc_` prefix — `@cole` for `npc_cole`,
`@frank` for `npc_frank`. An unrecognized `@word` is left untouched (so it's safe to write
literal `@`s — but see §6 on the handle collision).

**Possessives and punctuation just work:** `@cole's place` → `<<print …name>>'s place`
→ "Jamie's place". Dialog speaker labels are already dynamic (they render from `npcId`), so
you only tokenize the *body* text, never the speaker tag.

**Rule R1 — if an NPC is `customizable`, every player-visible mention of their name in
prose MUST be `@<npc>` (and every relationship mention `@<npc>.rel`).** A single hardcoded
"Cole" left in a renamed-Cole game is a visible bug. Same for `@player` once the player can
rename themselves.

**Worked proof (Late Shifts, live-verified):** with the player renamed *Nadia* / build
*curvy* and Cole renamed *Jamie* / relationship *old flame*, the apartment scene renders
*"His eyes go over her **curvy** frame … **Jamie**: **Nadia**. Didn't think you'd come by."*
All four token forms resolving at once.

---

## §4 — The un-tokenizable-surface trap (R2)

The `@`-token only fires where the engine runs `_resolve_at_references`: **canvas prose,
dialog body, choice text, and location descriptions.** It does **NOT** reach structural
labels that the engine prints raw:

- **Location names** (`<h2>{location.name}>` — the navigation title)
- **Sidebar trait-bar `label`s** (e.g. a `"Cole Relation"` bar)
- **Locked-link tooltip text** (`locked_text_threshold`)
- **Quest/stage display strings** and **arc_stages** names
- The NPC's customize-screen `description` intro (printed raw, html-escaped)

**Rule R2 — never bake a customizable NPC's name into a structural label.** A location
called `"Cole's Apartment"` stays "Cole's Apartment" after the player renames Cole → the
leak the whole feature was supposed to avoid. **Genericize these instead:** the location
becomes `"The Apartment Across Town"`, the sidebar bar label becomes `"Closeness"`, the
locked tooltip becomes `"Once he's noticed you"`. Carry the specificity in the *prose*
(which tokenizes), keep the *labels* neutral.

(Canvas/node `name` fields are dev-only — they appear on the Canvas-Review page and the
dev-mode banner, never in a production player build — so those may keep the literal name.)

---

## §5 — Customizable-NPC required fields (R3)

A `customizable` NPC **must** declare both `relationship` (the default) and
`relationship_options` (the picker list), and the default must be a member of the options.
The importer **hard-fails** otherwise (`template_import.py:3289–3304`). There is no
rename-only mode — renaming and relationship-picking ship together.

Player `customization_fields` have their own guards (`:2906–2943`): field `id`s must be
lowercase snake_case, unique, and **not** one of the reserved `$player` properties
(`portrait`, `current_location`, `core_traits`, `flags`, `wardrobe`, `equipped`).
`select` needs `options` (and any `default` must be in them); `image_select` needs `options`
with `id` + `image` on each; `sets_portrait` is `image_select`-only.

---

## §6 — `image_select`, portraits, and the `@handle` collision

- **`image_select`** renders a clickable image grid; each option is `{ id, image, label }`.
  With `sets_portrait = true` the chosen image becomes `$player.portrait` (used everywhere
  the engine shows the player's face). Missing art degrades gracefully — the `<img>` hides
  on error and the label still shows — so it's safe to ship the field before the art lands
  (same missing-media convention as locations).
- **The `@handle` collision (R4):** the token regex matches any `@word`. Social-feed
  handles in phone content — `@samantha_x`, `@lexiluv_` — that don't resolve to a known NPC
  slug are left as literal text (fine), **but** a handle that happens to collide with an NPC
  short-name *will* be substituted. Keep social handles distinct from NPC slugs, or accept
  the rewrite.

---

## §7 — Composition with the phone (and other JS-rendered surfaces)

The phone renders authored text as **JavaScript data**, not passage bodies — so the
generation-time `@`-token processor never touches it. The runtime twin `setup.resolveAtRefs`
(same `@player`/`@npc` resolution, in JS) is now applied at every phone render point
(notify toasts, message bubbles, reply buttons, daily-chat history, daily-topic buttons —
`v2.py` + `v1.py`), so **you can use `@<npc>` / `@player` tokens in phone `notify`, message
`content`, and `daily_topics` text and they resolve to the customized name.** The thread
title, avatar, and preview already read the live `$npcs[uuid].name`, so they honor a rename
even without a token.

Doctrine still applies: keep names *out* of any future raw-printed surface, and prefer the
auto-dynamic thread name over hardcoding.

---

## §8 — When to make it customizable (and when not)

- **Make the player customizable** when the protagonist is a blank-ish self-insert (the
  RTS default): name + build + look is the standard opener. **Don't** when the protagonist
  is a written, named character central to the premise and the prose leans on third-person
  narration by name — retrofitting `@player` across hundreds of "she did X" lines fights the
  grain and buys little. (Late Shifts demonstrates the field types in one arc rather than
  sweeping the whole third-person script — a deliberate, scoped choice.)
- **Make an NPC customizable** when the relationship framing is a genuine player fantasy
  axis (the step-relative toggle) **and** the cost is bounded — i.e. the name isn't baked
  into many structural labels (§4) and isn't load-bearing for the premise. A dating
  love-interest is the cheapest, most natural candidate; a sibling whose siblinghood *is*
  the story is the most expensive and most destructive.

**Enabling checklist:**
1. `[player].customizable = true` + at least one `[[player.customization_fields]]` (array-of-
   tables placed **after** every `[player.*]` subtable — TOML scoping).
2. For each customizable NPC: `customizable = true` + `relationship` + `relationship_options`.
3. Every player-visible name mention → `@player` / `@<npc>`; every relationship → `@<npc>.rel` (R1).
4. Every structural label that named the NPC → genericized (R2).
5. No engine wiring — the `CustomizeCharacters` screen and the `Start` redirect are automatic.

---

## §9 — Cross-references

- **Schema:** [schema/02 §2.3] (player fields) + [schema/02 §3.1] (NPC customization fields);
  [schema/03 §15] (full worked example, all three field types + NPC rename + tokens).
- **Sibling doctrine:** [doctrine/11 clothing], [doctrine/12 rent], [doctrine/13 phone] —
  the other opt-in engine surfaces with the same "declare-the-input, write-the-output" shape.
- **Production reference:** `games/under_one_roof` — three customizable NPCs (Frank / Jake /
  Ryan), 400+ `@`-tokens; the largest real consumer. `games/test_customize` — the minimal
  purpose-built example. `games/late_shifts` — the scoped demonstrator (player name/build/look
  + Cole rename, this session).
- **Engine entry points:** importer `template_import.py:62`, validator `:2906`/`:3289`,
  runtime screen `v2.py:8376`, token processor `v2.py:12658`, JS twin `setup.resolveAtRefs`
  `v2.py:2722`.
