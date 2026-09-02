# The Want — <game title>

> Fill every field. Keep the whole thing to one page; longer means vaguer.
> Doctrine and the reasoning behind each field: `references/the-want.md`.
> **Re-read this before every release.** Bump `want.last_read_at_release` in `v2_state.json`.

---

## 1. Who the player is — answered BEFORE she is described

> ⚠️ **This block did not exist until 2026-08-27, and its absence is why eight v2 games shipped the
> same protagonist.** Nobody chose a woman eight times: this file wrote `she/her` twenty-one times and
> `he/him` zero, so the grammar answered before the author arrived. v1 asked this first of anything
> (`author-game/references/step-0-1-seed.md:17`) and v2 dropped the question.
> Doctrine and the measurements: `references/the-want.md` §1.

**Who is the player?** `female` · `male` · `picked at start`

> Default **`female`**, and the reason travels with it so it stays a choice rather than a habit. In
> ~22,600 corpus comments, **49 ask for a female lead against 11 opposed**, and the opposed get
> argued down. `female 4 of 30` in the top ranks is a **supply** figure, not a verdict — one player
> counted the tags at 44 female to 100 male. The strongest practical case is a player's own: *"as a
> guy I like to play female mc since we can get to the spicy part quicker."*

**Written character, or blank slate?** `written` · `blank`

> The field runs **19 blank to 10 written**, and blank carries **80.4%** of the top-30's engagement.
> ⚠️ **All eight v2 games are `written` and not one ledger records that anybody picked it.** `written`
> is a legitimate answer — it is what real-porn media and a named cast want — but write it down.

**What does the player choose about her at minute zero?** <the start choice, or `none`>

> **`freedom` is the largest single thing the field is loved for — 25.9%**, ahead of performers,
> systems and volume. **Not one game in thirty is loved for its premise.** So the choosing matters
> and the setup does not.
>
> **A memory, not a slider.** Do not build a stat screen. Ask her something the scene is already
> asking — the answer reveals what she did before — and set a flag from it. See §3: what the flag
> buys is *reach*.
>
> ⚠️ **Additive only.** Every rung the choice touches keeps its original version behind
> `<flag> is_false`. A start choice that takes content away is the version players punish, and a save
> made before it shipped must read exactly what it read yesterday.

Record all three in `v2_state.json` under `want.player`, with the start choice's flags — the gate
**"the start choice is read"** checks the game against that declaration and reports `n/a` if it is
missing, which is not a pass.

> **A note on this file's own pronouns.** Everything below is written `she/her` because that is the
> default above and the measured guidance in §3 is specific to it. **If you declared otherwise, swap
> them as you fill it in** — the pronoun is downstream of the declaration, never the other way round.

## 1b. Who she is

<Her situation at minute zero. Concrete: a job, a debt, a room, a reputation.>

**What she has to lose:** <the thing that makes the first transgression cost something>

**What she owes, who collects it, and when:** <a recurring demand with a face and a date — not a
mood. "Friday, $260, and he counts it at the desk." `the-economy.md` R3 owns the mechanism.>

## 2. The appetite — where she lands, not where she starts

<What she wants, phrased so it can never be finished.>

⚠️ **Do not copy the line below. It is a SHAPE, not an answer** — four games in this repo shipped
one sentence because this slot used to hold a filled-in example. Write hers, in her nouns, from
§1b's obligation.

- ✅ shape: an appetite the world can always supply one more of, stated in the vocabulary of the
  place she is actually standing in
- ❌ "get revenge on X" — that completes, and then there is nothing left to want

**Where the bill stops being the reason:** <the point where she is still paying it and it is no
longer why — §4's Transformation charge, stated as a moment>

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

**What does release 41 add?** <answer it against a named tier above, in one line. Asked HERE and
not of §2: the tiers are what still gate content that far out — 1,336 rung-gated sites in the
reference game against 57 conditions that read its rent.>

## 4. The charge

Pick and name it. "It's hot" is the absence of a charge, not one.

- [ ] **Reversal** — <who has power over her, and how it flips>
- [ ] **Taboo** — <what the relationship itself transgresses>
- [ ] **Transformation** — <what she becomes that she'd not have recognised>

## 5. The world

Answered **here**, before a single character exists — because the cast is derived from the world and
not the other way round. Deriving the map from the cast is circular: the premise fixes the cast, the
cast fixes the map, and a household returns a house every time. Two of the first five v2 games
shipped seven-rooms-of-one-house worlds because nothing ever asked this. `references/the-map.md` R0.

**Where does this happen?** <the ground the whole game sits on — a town, a site, a street, a compound>

**What is outside the door she wakes up behind?** <what she crosses to get anywhere. If the answer is
"nothing", the world can only ever recycle its own interior and it has no renewable source of new
people.>

**How far can she get from it, and what stops her?** <distance, money, time, permission>

**Which shape is this?** — pick one, and it goes in `board.map.archetype`:

- [ ] `nested_zones` — district → venue → room. A town or campus *plus* a home. **The default to beat.**
- [ ] `two_hub` — two strong places joined by a commute
- [ ] `map_hotspots` — a drawn map with clickable districts, 10+ zones
- [ ] `street_mesh` — named streets listing their neighbours
- [ ] `time_slot` — no geography at all; a scripted Morning → Work → Evening chain

**What does her body need here, and what stops when it goes unmet?** <sleep · eat · wash · plus
whatever the premise adds. Each one names the thing it SHUTS — *filthy means she will not go out*,
*broke means the bus is walking*. A need that shuts nothing is a chore, and a game whose anchor room
is a kitchen shipped with no food and no bed because nothing ever asked this.
`references/the-meters.md` M8.>

**How alive?** <tight slice — only what the content needs · living world — ambient traffic and
routines she did not trigger. A budget fork, not a quality dial. For a sandbox, lean alive.>

## 6. Why *this* person

One line each — not their plot role. **Why she wants them, or why being wanted by them lands.**
A character with no line here has no reason to exist: cut them, or write it.

| character | why they are wanted |
|---|---|
| `npc_<id>` | |
| `npc_<id>` | |

## 7. Register

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

1. **What does release 41 add?** (ask it of a named §3 tier. If no tier can answer, the tier is
   decorative — and note this used to be asked of §2, which cannot schedule content)
2. **What can she reach at the top that she cannot at the bottom?** (the ascent, §3)
3. **Which character would a player miss if deleted, and why?** (the product, §6)
4. **Which repeatable surface carries the crudest writing in the game?** (§7 — and if the
   answer is a one-time scene, the game is already cold)

5. **Run the vocabulary check and read what it prints.** Not a judgement call, and not optional:

   ```
   python3 scripts/gates.py --words games/<slug>/WANT.md
   ```

   A list, never a score. This page is where the game's nouns get chosen — its rooms, its work,
   its objects, its meters — so it is the cheapest place to catch a word the player does not
   already own. Catching one after the prose exists means renaming things.
   `references/the-want.md`, "The test before you leave this file".

---

**Then:** create `games/<slug>/v2_state.json` with `phase = "want"` per `references/state.md`,
and move to `templates/board.toml`.
