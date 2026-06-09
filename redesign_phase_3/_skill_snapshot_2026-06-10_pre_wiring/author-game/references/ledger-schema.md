# authoring_state.json — ledger schema (v2)

The ledger is the living source of truth for the **plan** and for **what structure exists**.
The skill reads and rewrites it directly each authoring turn (Read/Write) — it is a data file,
not managed by any code module. Follow the invariants below when editing it.

```jsonc
{
  "game_slug": "late_shifts",       // matches games/<slug>/
  "schema_version": 2,
  "book_revision": 1,               // bumped when design_book.md is amended
  "scope_mode": "full_game",        // "full_game" | "slice" — set at setup; drives budgets + Phase 2+ flow
  "npcs": {                         // per-NPC intent from the R7 brief; sizes the continue loop
    "npc_sal": {
      "arc_shape": "slow-burn family",   // family/ambient|slow-burn family|peer/dating|service|antagonist
      "lane_budget": { "L1": 2, "L2": 1, "L3": 0, "capstones": 3 },  // target counts from the brief
      "vocab_ceiling": "explicit"        // this NPC's full-intensity ceiling (R7 brief; default max-explicit)
    }
  },
  "plan": [                         // the living roadmap; ordered, reorderable
    {
      "id": "beat_0001",            // stable, zero-padded, monotonic
      "type": "npc_intro",          // npc_intro|location_reveal|arc_escalation|
                                    //   cross_npc|economic|story_turn|capstone
      "title": "Hank hires the player at the diner",
      "desc": "One-line summary of the beat.",
      "status": "planned",          // planned|active|authored|validated
      "deps": [],                   // beat ids / flags that must exist first
      "target_phase": "5_scenes.toml",
      "introduces": { "locations": [], "npcs": ["hank"], "flags": ["hired_at_diner"] },
      "produced_canvas_ids": [],    // filled when authored; reconcile checks these exist
      "decided_at": null            // turn number when LO chose/locked it
    }
  ],
  "structure_registry": {           // what EXISTS; every amendment is checked against this
    // locations: tag each with its category — "reachable" (needs a hub per D72-R6),
    // "locked" (unlock contract, doctrine/10 §5.4), or "offscreen" (away-label,
    // offscreen=true, exempt from the presence floor, doctrine/10 §5.5)
    "locations": [],                // e.g. [{ "id": "loc_npc_home", "category": "offscreen" }]
    "npcs": [], "flags": [], "schedules": []
  },
  "next_up": [],                    // ordered beat ids proposed next
  "decisions_log": [                // human-readable trail
    { "turn": 1, "note": "...", "book_revision": 1 }
  ]
}
```

**`scope_mode` + `npcs`** (v2): `scope_mode` (`full_game` | `slice`) is set at setup and read before
sizing any arc. `npcs.<id>` carries each NPC's R7-brief intent — `arc_shape`, `lane_budget` (target
counts the continue loop authors *toward*, decremented as beats land), and `vocab_ceiling`. (v1
ledgers without these fields are fine — treat missing `scope_mode` as `full_game`.)

**Statuses:** `planned` → `active` (being authored this turn) → `authored` (canvases written)
→ `validated` (passed merge + schema/flag-chain + doctrine self-audit).

**Anti-drift invariant:** nothing in the TOML may reference a location/NPC/flag absent from
`structure_registry`, and adding one is an explicit, logged amendment (register it here in the
same turn you author it). **Drift** = any `validated`/`authored` beat whose `produced_canvas_ids`
are missing from the merged TOML; the skill spot-checks this on resume — the real per-beat safety
net is `package_from_toml` (schema + flag-chain + broken-reference validation; `merge_toml_phases
--validate` only syntax-parses the merged file).
