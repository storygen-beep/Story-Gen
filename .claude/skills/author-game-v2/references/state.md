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
> check-nothing: a `fill` copied from the delivered word count makes gate 1 compare the game against
> a record of itself. **A declaration only works if it can be wrong.** Write these before the
> prose; gate 1 now refuses to credit a budget that looks back-filled.

---

## Schema

```jsonc
{
  "slug": "…",
  "phase": "want" | "idea" | "spine" | "board" | "sheets" | "release",  // the dispatcher reads THIS.
                                            //   `sheets` was added 2026-08-31: the board
                                            //   phase ends in a signed design, not in TOML.
                                            //   the-sheets.md.
  "narration_person": "second",             // immutable once a release has shipped
  "protagonist": "…",                       // her name. Read by `gates.py --words` as a
                                            //   name the fiction teaches — she is not in
                                            //   board.characters[], so without this her
                                            //   own name tops her own vocabulary report.

  "want": {
    // THE FANTASY AND THE PROMISE — written on the idea page (templates/idea.md), the-want.md §0.
    // All optional; no gate reads them yet.
    "fantasy_shape": "fall_by_need" | "rise_by_want" | "taboo_at_home" | "mystery" | "mix: …",
    "model_to_beat": { "game": "…", "better": "one line — what ours does better" },
    "moment_kinds":  ["firsts" | "being_seen" | "body_as_payment" | "taboo_at_home" | "consequence"],
    "promise":       { "goal": "…", "mystery": "…", "payout": "…", "rival": "npc_id",
                       "goals": [ { "goal": "…", "ends_when": "…", "ends_flag": "flag_id",
                                    "next": "…" } ] },
                                 // no date (D8). A goal with ends_when names next (shape.py),
                                 // and ends_flag: the flag set when it is met (planned check: some choice sets it).
    "companion":     "npc_id",   // who leads her, or whom she leads
    "companion_is_rival": true,  // only when declared; her scenes show help AND competition (D15)
    "pressure":      "npc_id",   // the man whose demand drives her choices — the-want.md §6
    "face":          "…",        // one performer or one look, kept across the game
    "toggles":       [ { "id": "…", "flag": "…", "turns_off": "…" } ],
                                 // content toggles — the-surfaces.md R5b.4; lint · toggles declared

    // WHO THE PLAYER IS — declared BEFORE she is described. the-want.md §1.
    // The default `female` is EVIDENCED (49 comments for a female lead, 11 against).
    "player": {
      "who":        "female" | "male" | "picked",   // field: 20 male · 6 picked · 4 female (SUPPLY, not a verdict)
      "definition": "written" | "blank",            // field: 19 blank · 10 written; blank holds 80.4% of engagement
      // The start choice. `freedom` is the male-heavy top 30's largest bucket (25.9%);
      // for a female lead the premise matters too (the-want.md §0). A MEMORY, NOT A SLIDER:
      // ask what the scene already asks, set a flag, never show a stat screen.
      // Omit the key entirely for a game with no start choice; gate
      // `the start choice is read` then reports n/a, which is NOT a pass.
      "start_choice": { "asked_at": "canvas.node", "flags": ["…", "…"] }
    },

    "who_she_is":      "…",
    "obligation":      "…",   // the hold, in her nouns, with a face and a due day that repeats
    "hold_kind":       "ambition" | "bill" | "order" | "body" | "subsistence"
                     | "appetite" | "job" | "erosion" | "displacement",   // the-want.md §1b
    "hold_collector":  "npc_id",  // who enforces it, when a person does; omit when nothing does.
                              // Read by the lint `the collector is also the target` (§4a).
    "appetite":        "…",   // must not be completable. A DESTINATION, not the opening
                              // position and not the content schedule — the tiers are that
                              // (the-want.md §2)
    "ascent":          "…",   // stated as ACCESS: what she can reach at the top
    "charge":          "reversal" | "taboo" | "transformation" | "…",
    "cast":            [ { "id": "npc_id", "age": 18, "keeps": "step counter + memory flags"
                                                  | "want + warmth" | "want + power"
                                                  | "none — <why: he is part of a system>" } ],
                              // `none — …`: he does not climb; he sits in a system card's
                              // `people[]` (the-meters.md W1, "What each man keeps score of").
                              // the-want.md §6. shape.py FAILS a person (here or in
                              // board.characters[]) with no age or under 18.
    "why_this_person": { "npc_id": "one line — why she wants them, or why being wanted lands" },
    "crude_ceiling":   { "npc_id": ["the actual words permitted, per rung band"],
                         "role:night man": ["…"] },   // SP2 · a walk-on with no id: `role:<name>`
    "places":          [ { "id": "location_id", "name": "…" } ],   // read by `gates.py --words`
    "threads":         [ { "id": "job", "name": "…", "person": "npc_id", "place": "location_id",
                           "system": "…", "link": "one line — how it feeds the hook" } ],
                              // her life, 4–6 threads — the-want.md §6. person is in `cast`,
                              // place is in `places`.
    "last_read_at_release": "0.4"           // ← the anti-drift field. Bump it every release.
  },

  // THE SPINE — the-spine.md. Page status and sign-off ONLY; each decision lives in the key
  // its page names (board.*, dependencies, release_page), never copied here.
  "spine": {
    "pages": [ { "id": "SP1", "status": "REVIEW" | "READY", "drafted_at": "YYYY-MM-DD",
                 "signed_by": "LO", "signed_at": "YYYY-MM-DD" } ]   // shape.py: a READY page is signed
  },

  // SP3 — a step that needs another person's step, a window, or a place.
  "dependencies": [ { "from": { "npc": "npc_id", "step": 3 },
                      "needs": { "npc": "npc_id", "step": 2 } } ],   // or { "window": {…} } · { "place": "location_id" }

  "board": {
    // WHAT SHE DOES AGAIN AND AGAIN — answered BEFORE the locations exist, because the
    // location count is derived from what a place is FOR and that derivation is circular
    // without it. the-systems.md SY1-SY3. Three lists, never merged:
    // SYSTEMS — one design card each (templates/sheets/system.md; worked cards in
    // templates/cards/). A system is a place she goes or a thing she does, again and again.
    //   `pay_ladder` / `lewd_ladder` — one ladder by default (`one_ladder: true`); each lewd
    //               rung lists its `acts`. `pool` — canvas ids; `daily: true` when the pool is
    //               clicked every day. `growth` — "climbs" | "decays". `sink` / `deadline` —
    //               where its money goes and when. `feeds` / `reads` — system or meter ids.
    //               `leads_to` — npc ids or canvas ids.
    "systems": [
      { "id": "…", "name": "…", "place": "location_id", "hours": "Mon-Fri 18:00-02:00",
        "cost": "60 min · energy", "one_ladder": true,
        "pay_ladder":  [ { "gate": "…", "pay": 0 } ],
        "lewd_ladder": [ { "gate": "…", "acts": ["…", "…"] } ],
        "people": ["npc_id"], "pool": ["canvas_id"], "daily": true,
        "memory": "…", "growth": "climbs", "sink": "…", "deadline": "…",
        "feeds": ["meter_id"], "reads": ["meter_id"], "hook_link": "…",
        "leads_to": ["npc_id"] }
    ],
    // METERS — what systems write and read.
    //   `kind`    — SY1's fork, answered per meter, not per game. A game needs both.
    //               "ambient" is fed by nearly every room (time, money, the body);
    //               "sourced" is fed in one or two places and read all over.
    //   `key`     — the trait or flag the game actually keeps. This is what the lint reads.
    //   `fed_at`  — location ids. On a `sourced` meter this should usually be ONE; if it
    //               is five, the thing is probably ambient (SY2).
    //   `labels`  — which room labels this meter attaches to. ⚠️ In THIS engine that is a
    //               design statement, not wiring: a canvas belongs to exactly one location
    //               (template_import.py:2193), so the row is authored per room. SY4.
    // ⚠️ An older ledger keeps these rows in `systems` (an entry with `kind` and no card
    //   fields). It is read as a meter until the game moves it here.
    "meters": [
      { "id": "look", "kind": "sourced", "key": "grooming",
        "fed_at": ["the_office"], "labels": ["has_mirror"],
        "read_by": "one line — what changes because of it" }
    ],
    // INFRASTRUCTURE — clocks, views and channels, named and counted apart (SY1).
    "infrastructure": [ { "name": "energy", "kind": "clock" | "view" | "channel" } ],

    // WHO CLIMBS — answered BEFORE any meter is named. the-meters.md W1, gate 34.
    // The field splits 8 roster / 9 ladder with nothing between 15% and 65%.
    "who_climbs": "player" | "cast" | "both",

    // gate 10 judges THESE by name instead of guessing the top-gated traits
    "ascent_tiers": ["nerve", "exposure", "need"],
    "ceilings": { "nerve": 100, "exposure": 100, "need": 100 },
    "locations": [
      // `fill` — the word budget, in ROUND numbers, declared BEFORE the prose. Gate 1 checks
      //   each location against its own figure; it refuses to credit a set that is mostly
      //   non-round, because that is a post-hoc record and cannot fail. (`budget` is an
      //   observed drift of the same key — accepted on read, but write `fill`.)
      // `serves` — the three kinds a room's list may hold, and nothing else (`work` lists the
      //   systems that live here; a job is a system with a card, SY8). THIS is the
      //   room's menu and its length. the-surfaces.md R2. (It replaced `objects` on 2026-08-18;
      //   the old key stays readable in shipped ledgers but nothing reads it.)
      // `labels` — what KIND of place this is. the-systems.md SY3. ⚠️ NOT the same field as
      //   `serves` and it must not be merged with it: `serves` is what HAPPENS here, `labels`
      //   is what would let anything happen here at all. A room carrying `has_mirror` with no
      //   mirror row is a room whose systems have not arrived yet — a finding, not an error.
      //   Half of these are read by the map (hours, zone) and half by the systems
      //   (`home_base`, `she_can_undress`); a few by both. Keep ONE list, not two.
      { "id": "…", "job": "…", "anchor": false, "fill": 3200, "has_cycling_pool": false,
        "labels": ["private", "has_mirror"],
        "serves": { "needs": ["hygiene"], "work": ["the Saturday shift"], "people": ["npc_…"] } }
    ],

    // the body's clock. Declared here, gated by gate 29. the-meters.md M8-M10.
    // `shuts` is the load-bearing field: a need that shuts nothing is a chore.
    "needs": [
      { "key": "energy", "falls": "8 a day", "fills": "her_room · Sleep · 8 hours",
        "costs": "nothing", "shuts": "under 20 she will not go out" }
    ],
    // SP5 and SP6 — the cast's width and the rule for adding one; where it is played, and clips.
    "cast":  { "width": 4, "adding_rule": "a new person brings a thread (or joins one), a ladder, and why she wants them" },
    "media": { "platform": "…", "clips": "…" },

    "characters": [
      // `meters` — which numbers THIS person owns and what each one gates: what his
      //   want.cast[].keeps declares (the-meters.md W1 · W6).
      { "id": "npc_…", "surfaces": 2, "schedule_rows": 3, "why_wanted": "…",
        "meters": { "want":   { "type": "opens his next step", "min": 0, "max": 100 },
                    "warmth": { "type": "lover vs user", "min": 0, "max": 100 } } }
    ],

    // the map, as a place — declared BEFORE locations are written, and the SHAPE
    // before anything else. Fields only: this block carried a filled-in example world
    // until 2026-08-18 and three games copied its shape. See the-map.md R0.
    "map": {
      "archetype":  "nested_zones | two_hub | map_hotspots | street_mesh | time_slot",
      "shape":      "one sentence a stranger could draw from",
      "home_base":  "location_id",
      "exterior":   "location_id — MUST be a root, not a leaf off an interior room",
      "roots":      ["location_id", "…"],   // every root; a second one is joined by a travel canvas
                                            //   and marked offscreen or sealed for gate 11 (the-map.md R3)
      "homes":      { "npc_…": "location_id", "npc_…": "offscreen" },
      "scale":      "one street · a district · a town",
      "alive":      "tight slice" | "living world"        // the-map.md, "Aliveness"
      // travel costs live on the area: [[locations]] crossing_costs (engine.md §22). A place's
      // `name` comes from want.places[].
    },

    // SP4 — the hold's pressure, money or not. `stages` mirrors [settings.rent] stages;
    //   shape.py reads it when present.
    "pressure": { "what_repeats": "…", "who_collects": "npc_id", "cost_of_a_miss": "…",
                  "stages": [ { "amount": 100, "after_total_paid": 0 } ] },

    // what money is FOR — the question asked while it is still cheap to answer
    "economy": {
      "currency":   "money",
      // ⚠️ The NOTATION every button, every paragraph and [settings.rent] currency_symbol
      //    has to agree with. Undeclared, the rent pages print "$" (v2.py:1195) while the
      //    buttons print whatever each was typed with. the-economy.md R7.
      "symbol":     "$",
      // ⚠️ THE MONEY CASE ONLY — this block and gate 24 exist for `want.hold_kind = "bill"`.
      //    A game held by an ambition, an order, a body or a place declares its hold in
      //    `want` and leaves these three keys out; gate 24 then reports n/a, which the-want.md
      //    §1b says is a choice and not an omission.
      "obligation": "rent — Monday, from the landlord, in person",
      // ⚠️ The PRICE, as a number. Prose alone cannot be checked. Gate 24.
      "obligation_amount": 200,
      // ⚠️ THE OTHER HALF OF THAT NUMBER. What a full week of the income rungs actually pays —
      //    the honest maximum with its working, not a guess at what a player will earn.
      //    the-economy.md R3 says "price it against the income channels in both directions";
      //    this is the field that makes the sum checkable instead of a prose comment. Printed
      //    by the obligation-against-the-week LINT, never judged: the lint prints the ratio
      //    and leaves it to you.
      "week_income": 350,
      // ⚠️ R3b. Present ONLY if the obligation moves, and it names the mechanism in one
      //    line. A constant obligation against a rising income is soft at whatever value
      //    it is set to, so this is the field's answer and not a nicety. Declaring it
      //    also tells the obligation-against-the-week lint that a low baseline ratio is
      //    by construction rather than an oversight.
      "obligation_moves": "<the mechanism, in one line — what raises it and when>",
      // SP4, read by shape.py: how often the obligation falls due (default every week), and — only
      //    when the week's income is MEANT not to cover it — why, in one line.
      "obligation_every_weeks": 1,
      "shortfall": "<optional — why the pressure is meant not to be met>",
      "sinks":      ["rent", "the boiler", "the bus fare"]
    }
  },

  "releases": [
    {
      "version": "0.3",
      "subject": "…",                        // ONE named subject
      "want_line": "…",                      // which line of the Want this served
      "moment_kind": "firsts" | "being_seen" | "body_as_payment" | "taboo_at_home" | "consequence",
      "her_moment": { "person": "npc_id", "step_n": 4, "pays": "flag or canvas it pays",
                      "fantasy": "…", "temptation": "…", "answers": ["…"], "voice": { "low": "…",
                      "high": "…" }, "noticed": "…", "sticks": "…", "remember": "…", "door": "…",
                      "opens": "the next step, named" },
                                             // the step as shipped (the-release.md, "The next
                                             //   step"). Optional; the pitch pack reads person to
                                             //   count releases since each person's last step.
                                             //   Unshipped: `release_page.her_moment`.
      "added":   { "units": 0, "words": 0, "locations": 0, "characters": 0 },
      "opened":  ["the thing now visible and locked"],
      "gates":   { "passed": 10, "of": 10 },
      "shipped": "2026-08-10",
      "commit":  "abc1234"                   // the HEAD the build was made from (before the ship
                                             //   commit); the reader's
                                             //   "touched" diffs against it (the-release.md 6b)
    }
  ],

  "promises": [
    { "text": "…", "made_in": "0.2", "paid_in": null }   // null = still owed
  ],

  // WHAT PLAYERS SAID — the-release.md loop step 8, written by the v2-listener agent.
  "listen_sources": { "mopoga": "page-slug", "f95": "thread url", "gamcore": "url" },  // optional
  "listen": [
    { "release": "0.3", "read_on": "2026-10-12",
      "sources": { "mopoga": 41, "f95": 12, "not read": ["gamcore"] },
      "praised": [{ "quote": "…", "count": 3 }], "asked_for": [{ "quote": "…", "count": 5 }],
      "complained": [{ "quote": "…", "count": 2 }], "stuck": [{ "quote": "…", "count": 7 }] }
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
this shape: the Want is read every release. *(LO decided.)* If
this field is behind the current version, the Want has not been read this cycle and the
release is not ready.

**`board.locations[].fill`** — the word budget you are writing TO, in round numbers, set at board
phase before the prose exists. ⚠️ This entry used to read *"words currently placed there, recompute
from gates.py"*, which turns the budget into a record of the delivered count. Gate 1 now
refuses to credit a budget that is mostly non-round. Hand-maintain the *job*, the *anchor* flag and `serves` too. Exactly one location should carry
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

**`board.systems[]`** — one design card per system (what she does again and again), filled before
the locations are written. `the-systems.md` SY1; the sheet is `templates/sheets/system.md`.

**`board.meters[]`** — what the systems write and read. The load-bearing field is **`kind`**: an
`ambient` meter is fed by nearly every room and therefore cannot make any room special; a room
needs a meter about who she is. A `sourced` meter is fed in one or two places and read all over:
Course of Temptation reads her inclinations (`has_inclination`) in **218** of its 5,294 passages,
e.g. [ClassroomMenu] `<<if $pc.has_inclination("Knowledge from the Deep")`.
⚠️ **`fed_at` on a `sourced` meter should usually name ONE location** — if it names five, the
thing is ambient and the ledger is the cheapest place to find that out. A meter-shaped entry
still in `board.systems[]` (a `kind`, no card fields) is read as a meter until it moves.

**`board.infrastructure[]`** — the clocks, views and channels (`kind`: `clock` · `view` ·
`channel`), named so they are not counted as systems.

**`board.locations[].labels`** — what kind of place each room is. `the-systems.md` SY3. Read the
label menu there and **cut it down**; a label no system reads is dead weight, and the lint prints it
as such. ⚠️ **Declaring more is worse, not better** — this field is not a score and cannot be
gamed upward, which is the only reason it is checked at all.

**`board.map.homes`** — where every declared character sleeps, or the literal `"offscreen"`.
**This cannot be inferred and must not be guessed.** A tenant working nights legitimately has no
night schedule row; a shopkeeper legitimately has no bed in the player's house. Only a declaration
separates *lives elsewhere* from *was never given a room*. Gate 12.

**`board.needs[]`** — the body's clock, declared at board phase. Five fields per need: `key`,
`falls`, `fills`, `costs`, **`shuts`**. Gate 29 reads `key` and fails any need that no condition
anywhere in the game reads — a restore that gates nothing is a chore, not a need. Needs are per game,
never a fixed list. `the-meters.md` M8–M10.

**`board.locations[].serves`** — which needs / work / people this room's list holds.
`the-surfaces.md` R2. Replaced `objects` on 2026-08-18; the old key remains readable in older
ledgers and **nothing reads it**, the same treatment `dwelling` got in the map pass.

**`board.map.archetype`** — which of the five map shapes this world is, picked from the premise
before the cast exists. Deriving the location count from where the cast goes is circular on its own:
the premise fixes the cast, the cast fixes the map, and a household returns a house every time. The
shape is the input that breaks that circle. Gate 28 fails a board that has not chosen.
`the-map.md` R0.

**`board.map.exterior`** — the ground the rest of the world sits on. If any destination is away from
home, this is what the player crosses to reach it, and it is where the ascent tiers get a
consequence surface beyond the household. A premise with no exterior can only recycle its own
interior, so it is also the only renewable source of new characters.

⚠️ **It must be a ROOT.** Gate 28 reads `entry_from` and fails a leaf. `the-map.md` R3.

**`board.map.home_base`** — where she sleeps. Older ledgers may carry the retired key `dwelling`;
nothing reads it.

**`board.economy.currency`** — declaring it is strictly better than letting the gates infer one
from `player.core_traits`; the headline says which was used, and inference picks wrong on a game
with two currencies. **`board.economy.symbol`** is the notation that currency is written in, and it
is what `[settings.rent] currency_symbol` must be set to (`the-economy.md` R7). **`board.economy.sinks`** is the useful half: it lists what money is actually
*for*.

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
must be logged **with what replaces it**. *(LO decided.)*

---

## Relationship to the gates

`scripts/gates.py` is the truth about what the game **is**. This file is the truth about what
was **decided** and what is **owed**.

When the two disagree, the gates win and the ledger gets corrected.

---

## The `board` keys the GATES actually read

`[added 2026-08-31]` Six gates read this file, and a ledger written to a schema they do not consume
degrades them to backstops **silently** — one prints *"[top-3 guess — no v2_state.json]"* while the
file sits there being read by a different gate. These are the exact paths:

| key | read by | shape |
|---|---|---|
| `board.ascent_tiers` | *ascent tiers expand the world* | `["corruption", "exhibitionism"]` — a list of trait keys, **not** rung numbers, and **not** at the top level |
| `board.map` | *the map is a place* · *residents have homes* | `{ archetype, shape, home_base, exterior, homes{npc_id: location_id} }`; archetype is one of `nested_zones` / `two_hub` / `map_hotspots` / `street_mesh` / `time_slot` |
| `board.characters` | *residents have homes* · *guidance exists* | `[{ id, name, role }]` |
| `board.locations[].fill` | *location fill* | a LIST of `{id, fill}`, **not** a dict — and declared before the prose, or the gate says so |
| `board.economy` | four economy gates | `{ currency, symbol, week_income, obligation }`; `currency` is the trait key, and without it the economy channel is *"not counted"* |
| `board.needs[]` | *a need shuts a door* | `[{ key, falls, fills, costs, shuts }]` — and every key must be READ by a condition somewhere in the game |
| `board.door` | *ends on an opening* | `{ canvas, choice, node? }` — the door this release ends on; `choice` is the choice's text. **A ledger without it or `release_page.door` FAILS the gate** (LO, 2026-09-26). `release_page.door` (SP7) is read first once a release page is written |
| `board.characters[].address` · `board.resetting_flags` | *pitch pack* NAMING · lint *a flag that never resets* | what this person calls her (`"love"`, her surname, nothing) — the pack prints it so a pitch uses it; and flags meant to reset that are not named `*_today`/`*_week` |
| `board.characters[].schedule` | `shape.py` *the person is there at the step's hour* | `[{ where, weekdays, from, to }]` — the person's hours, optional (weekdays as a step's `when.days`; absent = every day). Each ladder step's window must be fully covered by the union of the person's rows at its place, past midnight included; a `fires_from = "opening"` step is exempt. A row it cannot read (an unknown weekday, or the TOML's `location`/`start_time`/`end_time`) is bad input, and that person's steps are not judged. The per-room count stays `occupancy_rows` |
| `board.characters[].occupancy_rows` | *standing surface* | `[{ location, start_time, reason }]` — a schedule row whose job is to put a body in a room (asleep, in the bath, blocking a door), backed by that job and not by a canvas. Keyed by the row's start time, never the room, and always with its reason |
| `board.characters[].ladder` | *ladders move forward* · *`--ship`* (each step fires when unlocked) · *repeatables without a step* | `{ counter, steps: [{ n, canvas, where, when: { days, from, to }, gate: [ { flag, op? } \| { trait, op, value, npc? } ] }] }` — since 2026-09-26 (PRD WS4). `counter` is the player trait the steps read and set (an NPC's `arc_stages` gives `<slug>_stage`). Steps are numbered 1..K. `when` is ONE window — days (`"Mon"` or 0 = Monday) and from/to as `"HH:MM"` — and must equal the canvas's `[[canvases.trigger.schedules]]` exactly. `gate` lists every trigger condition except the counter's, and nothing else. Nothing here is trusted: the gate reads the canvas and fails on any difference. Optional per step (SP2, recorded and not gated): `hint`, `her_line_low`, `her_line_high`, `who_notices`, `refusal: "parked" \| "final"`. Optional `raises = {trait: amount}` — what the step adds. `shape.py` *a step's gate can be reached* checks each gate against the trait's start (his: `meters[k].start`, else `.min`; hers, a gate with no `npc`: `board.player_start = {trait: n}`, listed as bad input when malformed; else 0) plus the steps before it; a gate with `npc` counts only his steps. A trait in `board.daily_raises = {trait: per_day}` (the daily tick) or `board.repeat_raises = {trait: per_visit}` (a repeatable in the TOML raises it) is not judged. `fires_from: "opening"` (step 1 only) marks a step the opening plays: it needs no `where` or `when`, and its canvas must be the starting canvas or a capstone the opening walks into |
| `releases[].repeatables` · `releases[].ladder_steps` | *repeatables without a step* | written when a release ships: the repeatable canvas ids, and the count of declared steps. The next release is compared against them |
| `release_page` | *`--ship`* (the build matches the release page · LO signed the playtest · the reader passed) | `{ version, people[], door{canvas, choice}, signed_by_lo, signed_at, reader{canvas: {test: PASS\|FAIL\|N/A}}, reader_waivers[{canvas_id, test, why}] }` — `--ship` reads these. SP7 (`the-spine.md`) adds optional `steps{npc: max_step}`, `places[]`, `weeks`, `promise_alive`, `replay_ready` (yes/no), `block[]`, `report[]`, `rebuild` (the one planned rebuild, `the-release.md`), `her_moment` (the chosen step, unshipped; same shape as `releases[].her_moment`), recorded and not gated. `reader` = `{canvas_id: {test: "PASS" \| "FAIL" \| "N/A"}}` (the `v2-reader` verdicts on touched canvases, `the-release.md` 6b) and `reader_waivers` = `[{canvas_id, test, why}]` (LO's). Absent means `--ship` FAILS: nothing says what the release is |
| `parked.files` | *the tally* (parked, not judged) · *`--ship`* | optional globs relative to `games/<slug>/`, for parked TOML fragments kept outside `parked/`. The `parked/` folder is always read without this. Parked content is scored, never hidden: a gate it would judge counts as not passing |
| `board.economy.settle_canvas` | *the obligation is charged* | optional canvas id; when declared, the obligation's charge must sit on that canvas |
| `board.meters[]` | lint *the labels and the systems agree* | `[{ id, kind, key, fed_at, labels, read_by }]`. The lint also reads an old meter-shaped row still in `board.systems[]` |
| `board.systems[]` | no gate yet | the cards: `[{ id, name, place, hours, cost, pay_ladder[], lewd_ladder[]{acts[]}, one_ladder, people[], pool[], daily, memory, growth, sink, deadline, feeds[], reads[], hook_link, leads_to[] }]`. An entry with `kind` and no card fields is a meter |
| `board.infrastructure[]` | no gate (recorded) | `[{ name, kind: clock \| view \| channel }]` |

⚠️ **`needs` has no TOML table.** The importer reads 24 top-level tables and `needs` is not one of
them. A need exists in the game as `[player.core_traits]` + `[player.trait_decay]` plus the
conditions that read it; this ledger is where it is *declared*. A key the engine does not consume
fails silently.

⚠️ **The decision sheet and this file are one document written twice** — `the-sheets.md` S7.
