# `v2_state.json` — the small, enforceable ledger

Lives at `games/<slug>/v2_state.json`. Deliberately separate from anything the incumbent skill
keeps, so the two never collide.

**What it is for:** stopping release N+1 from being written against a world that stopped
existing at release N. It is the single source of truth about what exists, what is owed, and
what has been promised. Keep it current in the same turn you change the game — a stale ledger
is worse than none, because it is trusted.

Keep it small. Anything that can be recomputed from the TOML by `scripts/gates.py` does not
belong here; only decisions, debts, and promises do.

---

## Schema

```jsonc
{
  "slug": "…",
  "phase": "want" | "board" | "release",   // the dispatcher reads THIS
  "narration_person": "second",             // immutable once a release has shipped

  "want": {
    "who_she_is":      "…",
    "appetite":        "…",   // must not be completable
    "ascent":          "…",   // stated as ACCESS: what she can reach at the top
    "charge":          "reversal" | "taboo" | "transformation" | "…",
    "why_this_person": { "npc_id": "one line — why she wants them, or why being wanted lands" },
    "crude_ceiling":   { "npc_id": ["the actual words permitted, per tier"] },
    "last_read_at_release": "0.4"           // ← the anti-drift field. Bump it every release.
  },

  "board": {
    // gate 10 judges THESE by name instead of guessing the top-gated traits
    "ascent_tiers": ["nerve", "exposure", "need"],
    "ceilings": { "nerve": 100, "exposure": 100, "need": 100 },
    "locations": [
      { "id": "…", "job": "…", "anchor": false, "fill": 3200, "has_cycling_pool": false }
    ],
    "characters": [
      { "id": "npc_…", "surfaces": 2, "schedule_rows": 3, "why_wanted": "…" }
    ]
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

**`board.locations[].fill`** — words currently placed there. Recompute from `scripts/gates.py`;
hand-maintain only the *job* and the *anchor* flag. Exactly one location should carry
`anchor: true`, and it must be one the player can reach and re-enter.

**`board.ascent_tiers`** — names the three or four ratcheting tiers. Gate 10 reads this and
judges those meters by name; without it the gate falls back to a top-3 guess and says so in
its headline. Declaring is strictly better — skills and resources legitimately gate downward
and should not be mistaken for the spine.

**`board.ceilings`** — each tier's top band. If the highest authored gate on a tier sits below
its ceiling, the top of that bar buys nothing. Gate 8 fails and the player is being lied to.

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
