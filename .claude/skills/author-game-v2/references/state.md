# `v2_state.json` — the small, enforceable ledger

Lives at `games/<slug>/v2_state.json`. Deliberately separate from anything the incumbent skill
keeps, so the two never collide.

**What it is for:** stopping release N+1 from being written against a world that stopped
existing at release N. It is the single source of truth about what exists, what is owed, and
what has been promised. Keep it current in the same turn you change the game — a stale ledger
is worse than none, because it is trusted.

Keep it small. Anything that can be recomputed from the TOML by `scripts/gates.py` does not
belong here; only decisions, debts, and promises do.

> ⚠️ **"Recomputed" means *derived*, not *measured after the fact*. The difference is the whole
> point of a declaration.** `fill` and `objects` look recomputable — you *can* count words and read
> nouns out of a finished game — but writing them that way turns declare-then-check into
> check-nothing. Measured: all three v2 games filled `board.locations[].fill` from the delivered
> word count (9,607 · 4,936 · 10,295 — 0 of 24 round to the nearest hundred), so gate 1 compared
> each game against a record of itself and passed 8/8 every time. **A declaration only works if it
> can be wrong.** Write these before the prose; gate 1 now refuses to credit a budget that looks
> back-filled.

---

## Schema

```jsonc
{
  "slug": "…",
  "phase": "want" | "board" | "release",   // the dispatcher reads THIS
  "narration_person": "second",             // immutable once a release has shipped
  "protagonist": "…",                       // her name. Read by `gates.py --words` as a
                                            //   name the fiction teaches — she is not in
                                            //   board.characters[], so without this her
                                            //   own name tops her own vocabulary report.

  "want": {
    // WHO THE PLAYER IS — declared BEFORE she is described. the-want.md §1.
    // Added 2026-08-27. Its absence is why eight v2 games shipped one protagonist:
    // templates/want.md wrote she/her 21 times and he/him zero, so the grammar
    // answered before the author arrived. The default `female` is EVIDENCED
    // (49 comments for a female lead, 11 against) — what was missing was the question.
    "player": {
      "who":        "female" | "male" | "picked",   // field: 20 male · 6 picked · 4 female (SUPPLY, not a verdict)
      "definition": "written" | "blank",            // field: 19 blank · 10 written; blank holds 80.4% of engagement
      // The start choice. `freedom` is the field's largest bucket (25.9%) and
      // premise is 0 of 30 — the choosing is the product. A MEMORY, NOT A SLIDER:
      // ask what the scene already asks, set a flag, never show a stat screen.
      // Omit the key entirely for a game with no start choice; gate
      // `the start choice is read` then reports n/a, which is NOT a pass.
      "start_choice": { "asked_at": "canvas.node", "flags": ["…", "…"] }
    },

    "who_she_is":      "…",
    "appetite":        "…",   // must not be completable
    "ascent":          "…",   // stated as ACCESS: what she can reach at the top
    "charge":          "reversal" | "taboo" | "transformation" | "…",
    "why_this_person": { "npc_id": "one line — why she wants them, or why being wanted lands" },
    "crude_ceiling":   { "npc_id": ["the actual words permitted, per tier"] },
    "last_read_at_release": "0.4"           // ← the anti-drift field. Bump it every release.
  },

  "board": {
    // WHO CLIMBS — answered BEFORE any meter is named. the-meters.md W1, gate 34.
    // The field splits 8 roster / 9 ladder with nothing between 15% and 65%; all
    // five v2 games landed at 19-29% because the question was never asked.
    "who_climbs": "player" | "cast" | "both",

    // gate 10 judges THESE by name instead of guessing the top-gated traits
    "ascent_tiers": ["nerve", "exposure", "need"],
    "ceilings": { "nerve": 100, "exposure": 100, "need": 100 },
    "locations": [
      // `fill` — the word budget, in ROUND numbers, declared BEFORE the prose. Gate 1 checks
      //   each location against its own figure; it refuses to credit a set that is mostly
      //   non-round, because that is a post-hoc record and cannot fail. (`budget` is an
      //   observed drift of the same key — accepted on read, but write `fill`.)
      // `serves` — the three kinds a room's list may hold, and nothing else. THIS is the
      //   room's menu and its length. the-surfaces.md R2. (It replaced `objects` on 2026-08-18;
      //   the old key stays readable in shipped ledgers but nothing reads it.)
      { "id": "…", "job": "…", "anchor": false, "fill": 3200, "has_cycling_pool": false,
        "serves": { "needs": ["hunger"], "work": ["the Saturday shift"], "people": ["npc_…"] } }
    ],

    // the body's clock. Declared here, gated by gate 29. the-meters.md M8-M10.
    // `shuts` is the load-bearing field: a need that shuts nothing is a chore.
    "needs": [
      { "key": "hygiene", "falls": "10 a day", "fills": "the_bathroom · Wash · 30 min",
        "costs": "$5 for the water heater", "shuts": "under 40 she will not go out in public" }
    ],
    "characters": [
      // `meters` — which numbers THIS person owns and what each one gates. In a
      //   who_climbs = "player" game one bond meter is a correct, deliberate answer;
      //   in a "cast" game an identical pair on everyone is the engine missing.
      //   the-meters.md W6.
      { "id": "npc_…", "surfaces": 2, "schedule_rows": 3, "why_wanted": "…",
        "meters": { "relation": "access — what she is allowed to be near",
                    "lust":     "willingness — how far he will go" } }
    ],

    // the map, as a place — declared BEFORE locations are written, and the SHAPE
    // before anything else. Fields only: this block carried a filled-in example world
    // until 2026-08-18 and three games copied its shape. See the-map.md R0.
    "map": {
      "archetype":  "nested_zones | two_hub | map_hotspots | street_mesh | time_slot",
      "shape":      "one sentence a stranger could draw from",
      "home_base":  "location_id",
      "exterior":   "location_id — MUST be a root, not a leaf off an interior room",
      "homes":      { "npc_…": "location_id", "npc_…": "offscreen" },
      "bridges":    [ { "from": "location_id", "to": "location_id", "costs": { "time": 0 } } ],
      "r1_signoff": "WHO signed it and WHEN, then what they saw"
    },

    // what money is FOR — the question asked while it is still cheap to answer
    "economy": {
      "currency":   "money",
      // ⚠️ The NOTATION every button, every paragraph and [settings.rent] currency_symbol
      //    has to agree with. Undeclared, the rent pages print "$" (v2.py:1190) while the
      //    buttons print whatever each was typed with. the-economy.md R7.
      "symbol":     "$",
      "obligation": "rent — Monday, from the landlord, in person",
      // ⚠️ The PRICE, as a number. Prose alone cannot be checked, and a game shipped with its
      //    central charge missing because only the prose existed. Gate 24.
      "obligation_amount": 245,
      "sinks":      ["rent", "the boiler", "the bus fare"]
    }
  },

  "releases": [
    {
      "version": "0.3",
      "subject": "…",                        // ONE named subject
      "want_line": "…",                      // which line of the Want this served
      "added":   { "units": 0, "words": 0, "locations": 0, "characters": 0 },
      "opened":  ["the thing now visible and locked"],
      "gates":   { "passed": 10, "of": 10 },
      "shipped": "2026-08-10"
    }
  ],

  "promises": [
    { "text": "…", "made_in": "0.2", "paid_in": null }   // null = still owed
  ],

  "decisions": [
    { "at": "0.2", "note": "what changed, why, and what it cost" }
  ]
}
```

---

## Field rules

**`phase`** — the only thing the dispatcher reads. Advance it deliberately.

**`want.last_read_at_release`** — the anti-drift mechanism, and the reason this file exists in
this shape. The documented failure was a fantasy spec written once and never opened again. If
this field is behind the current version, the Want has not been read this cycle and the
release is not ready.

**`board.locations[].fill`** — the word budget you are writing TO, in round numbers, set at board
phase before the prose exists. ⚠️ This entry used to read *"words currently placed there, recompute
from gates.py"*, and that instruction is why all three v2 games back-filled it from the delivered
count and gate 1 passed 8/8 against a record of itself. Gate 1 now refuses to credit a budget that
is mostly non-round. Hand-maintain the *job*, the *anchor* flag and `serves` too. Exactly one location should carry
`anchor: true`, and it must be one the player can reach and re-enter.

**`board.who_climbs`** — the fork that comes before every other meter decision: does the PLAYER
change (one or two deep tiers on her run the world) or does the CAST (the meters live on each
character)? Or `"both"` — a player tier as the *floor* under per-character arcs. **Gate 34** reads
this and checks the built game against it: `player` wants ≥60% of meter-gating on her own tiers,
`cast` ≥60% on the cast, `both` ≥25% each. The cut points sit inside the corpus's own empty band, so
what is judged is the game against its own declaration, never against an invented number.
`the-meters.md` W1.

**`board.ascent_tiers`** — names the ratcheting tiers, if this game has any: **15 of 27 shipped
sandboxes have no player ascent tier at all**, and an empty list is a legitimate declaration for a
`who_climbs = "cast"` game. Gate 10 reads this and
judges those meters by name; without it the gate falls back to a top-3 guess and says so in
its headline. Declaring is strictly better — skills and resources legitimately gate downward
and should not be mistaken for the spine.

**`board.ceilings`** — each tier's top band. If the highest authored gate on a tier sits below
its ceiling, the top of that bar buys nothing. Gate 8 fails and the player is being lied to.

**`board.map.homes`** — where every declared character sleeps, or the literal `"offscreen"`.
**This cannot be inferred and must not be guessed.** A tenant working nights legitimately has no
night schedule row; a shopkeeper legitimately has no bed in the player's house. Only a declaration
separates *lives elsewhere* from *was never given a room* — and the measured failure was a game
whose landing description counted "four doors" while three of its four men slept nowhere at all.
Gate 12.

**`board.needs[]`** — the body's clock, declared at board phase. Five fields per need: `key`,
`falls`, `fills`, `costs`, **`shuts`**. Gate 29 reads `key` and fails any need that no condition
anywhere in the game reads — a restore that gates nothing is a chore, not a need. Needs are per game,
never a fixed list. `the-meters.md` M8–M10.

**`board.locations[].serves`** — which needs / work / people this room's list holds.
`the-surfaces.md` R2. Replaced `objects` on 2026-08-18; the old key remains readable in the five
shipped ledgers and **nothing reads it**, the same treatment `dwelling` got in the map pass.

**`board.map.archetype`** — which of the five map shapes this world is, picked from the premise
before the cast exists. Deriving the location count from where the cast goes is circular on its own:
the premise fixes the cast, the cast fixes the map, and a household returns a house every time. The
shape is the input that breaks that circle. Gate 28 fails a board that has not chosen.
`the-map.md` R0.

**`board.map.exterior`** — the ground the rest of the world sits on. If any destination is away from
home, this is what the player crosses to reach it, and it is where the ascent tiers get a
consequence surface beyond the household. A premise with no exterior can only recycle its own
interior, so it is also the only renewable source of new characters.

⚠️ **It must be a ROOT.** A game declared one, priced it at 25 minutes, passed every gate — and its
exterior hung off the kitchen, so stepping outside meant stepping from one interior into a row of
shops. Gate 28 reads `entry_from` and fails a leaf. `the-map.md` R3.

**`board.map.home_base`** — where she sleeps. Called `dwelling` until 2026-08-18; the word presumed
a house before any decision was made and was already wrong for a truck stop and a bathhouse. The
five ledgers written before that date still carry the old key — nothing reads it, so they are stale
rather than broken.

**`board.map.r1_signoff`** — **who** signed the map off and **when**. A sign-off written by the
author of the map is not a sign-off; the game that shipped seven rooms of a house at 26/26 recorded
*"Signed off in the board phase"* with no name and no date. `the-map.md`, "What is checked".

**`board.economy.currency`** — declaring it is strictly better than letting the gates infer one
from `player.core_traits`; the headline says which was used, and inference picks wrong on a game
with two currencies. **`board.economy.symbol`** is the notation that currency is written in, and it
is what `[settings.rent] currency_symbol` must be set to — a shipped game wrote one click's price
six different ways and three of them were the engine's (`the-economy.md` R7). **`board.economy.sinks`** is the useful half: listing what money is actually
*for* is the question that, left unasked, produced a game with twelve ways to earn and one to spend.

**`releases[].opened`** — never empty. A release that opened nothing had no reason to ship.

**`releases[].added.locations`** — expected to be `0` most of the time. The measured reference
cycle added zero. A release adding a location must also have filled it — gate 1 judges the
whole distribution, so a new empty room drags the median and the mean down.

**`promises`** — every named-but-unpaid thread. Two measured failure modes this exists to
prevent: version-keyed stubs (`intro / release2 / release3`, whose game was finished "in one
minute" and is abandoned), and characters dangled for years (*"Are we EVER going to talk to
the university president?"*). Each promise is eventually **paid or cut**, and cutting is
logged like any other decision.

**`decisions`** — the trail. Especially: anything that removes or inverts a source of heat
must be logged **with what replaces it**. A measured pattern in a previous game was a series
of individually reasonable calls — removing an arousal stat, re-reading a beat as something
other than desire, making exhibition instrumental — that were jointly fatal, and no single one
was ever written down as a cost.

---

## Relationship to the gates

`scripts/gates.py` is the truth about what the game **is**. This file is the truth about what
was **decided** and what is **owed**.

When the two disagree, the gates win and the ledger gets corrected.
