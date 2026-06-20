# authoring_state.json — ledger schema (v2)

The ledger is the living source of truth for the **plan** and for **what structure exists**.
The skill reads and rewrites it directly each authoring turn (Read/Write) — it is a data file,
not managed by any code module. Follow the invariants below when editing it.

```jsonc
{
  "game_slug": "late_shifts",       // matches games/<slug>/
  "schema_version": 2,
  "book_revision": 1,               // bumped when design_book.md is amended
  "pipeline_phase": "authoring",    // which pipeline step we're in — the phase-aware dispatch reads THIS,
                                    //   not "does the file exist". One of: "setup" | "top_level" |
                                    //   "map_design" | "casting" | "deep_design" | "blueprint" |
                                    //   "feedback" | "authoring".
                                    //   The ledger is CREATED at setup carrying this; structure_registry
                                    //   .locations is SEEDED at "map_design" (Step 2b), the rest of
                                    //   structure_registry fills during "authoring", and plan is SEEDED at
                                    //   "blueprint" (Step 5 Pass 4). (Step 0 = fantasy is pre-ledger.)
                                    //   READ-ALIAS (backward-compat): an old ledger carrying "npc_arcs"
                                    //   is read as "deep_design"; an old "roster" is read as "feedback".
  "npcs": {                         // per-NPC intent (arc_shape/vocab from the Step-4 story brief; lane_budget from the Step-5 blueprint); sizes the continue loop
    "npc_sal": {
      "arc_shape": "slow-burn family",   // family/ambient|slow-burn family|peer/dating|service|antagonist
      "lane_budget": { "L1": 2, "L2": 1, "L3": 0, "capstones": 3 },  // target counts from the brief
      "vocab_ceiling": "explicit"        // this NPC's full-intensity ceiling (design brief; default max-explicit)
    }
  },
  "map_design": {                   // Step 2b STRUCTURE progress (meaningful only while "map_design")
    "topology": "pending",          // pending|active|done — archetype chosen + spatial graph drawn (location-design.md §1-§2)
    "roles_access": "pending",      // pending|active|done — per-location dramatic job + access category (§4, §6 room-content floor)
    "naming_travel": "pending"      // pending|active|done — naming contract + travel-friction decision (§3, §5)
  },
  "deep_design": {                  // Step 4 STORY progress (meaningful only while "deep_design")
    "player": "done",               // pending|active|done — §2 the player thread (Pass 1, FIRST)
    "npcs": "active",               // pending|active|done — §3 each NPC's story brief (Pass 2; START only when player=="done")
    "world": "pending",             // pending|active|done — §5 the world brief (Pass 3)
    "reactivity": "pending"         // pending|active|done — §4 reactivity-as-experience (Pass 4, LAST; START only when npcs+world done)
  },
  "blueprint": {                    // Step 5 STRUCTURE progress (meaningful only while "blueprint")
    "player": "done",               // pending|active|done — §2 mechanism: player scene list, lanes, thresholds, feeder count
    "npcs": "active",               // pending|active|done — §3 mechanism: each NPC's gated/placed/lane-tagged scene list (START only when player=="done")
    "world": "pending",             // pending|active|done — §5 mechanism: ceilings, schedules, systems, locks
    "wiring": "pending"             // pending|active|done — §4 wiring + DAG + opening scenes + plan-seeding (Pass 4, LAST; START only when npcs+world done)
  },
  "feedback": {                     // Step 6 review progress (meaningful only while "feedback")
    "subjects_reviewed": [],        // framework subjects already walked, e.g. ["1","2"]
    "open_gaps": []                 // [{ "id": "g1", "subject": "4", "note": "...", "status": "open" }]
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
    // locations: tag each with its category — "reachable" (needs a hub — the presence
    // floor, one Lane 1 hub per schedule row), "locked" (unlock contract,
    // references/location-design.md), or "offscreen" (away-label,
    // offscreen=true, exempt from the presence floor, references/location-design.md)
    "locations": [],                // e.g. [{ "id": "loc_npc_home", "category": "offscreen" }]
    "npcs": [], "flags": [], "schedules": []
  },
  "next_up": [],                    // ordered beat ids proposed next
  "decisions_log": [                // human-readable trail
    { "turn": 1, "note": "...", "book_revision": 1 }
  ]
}
```

**`pipeline_phase` + `npcs`** (v2): `pipeline_phase` is set when the ledger is created at setup and
updated as the pipeline advances; the **phase-aware dispatch reads it** to resume at the right step
(replacing the old "does `authoring_state.json` exist?" binary — slice was removed, so there is no
`scope_mode`). `npcs.<id>` carries each NPC's design-brief intent — `arc_shape`, `lane_budget` (target
counts the continue loop authors *toward*, decremented as beats land), and `vocab_ceiling`. (v1 ledgers
without these fields are fine — a missing `pipeline_phase` with a populated `plan` means `authoring`.)

**`deep_design` + `blueprint` + `feedback`** (Step 4/5/6 progress; all additive — absent on a pre-restructure
ledger just means "the phase's start"). `deep_design` tracks the four Step-4 STORY passes; `blueprint` tracks
the four Step-5 STRUCTURE passes; both **enforce the supply→demand→stage order**: don't start `npcs` until
`player == "done"`, and don't start the last pass (`reactivity` / `wiring`) until `npcs` and `world` are both
done (`step-4-deep-design.md` / `step-5-blueprint.md`). The **`plan` is seeded by `blueprint`'s last pass**
(Step 5 Pass 4), not at authoring-entry. `feedback` tracks the Step-6 review — which framework subjects are
walked + the `open_gaps` the navigation proposes from (`step-6-feedback.md`). **Phase aliases** keep old
ledgers readable: `"npc_arcs"` → `deep_design`, `"roster"` → `feedback` (no in-flight game is at those phases,
but the alias removes all risk). `schema_version` stays **2** — these are additive fields, not a format break.

**Statuses:** `planned` → `active` (being authored this turn) → `authored` (canvases written)
→ `validated` (passed merge + schema/flag-chain + doctrine self-audit).

**Anti-drift invariant:** nothing in the TOML may reference a location/NPC/flag absent from
`structure_registry`, and adding one is an explicit, logged amendment (register it here in the
same turn you author it). **Drift** = any `validated`/`authored` beat whose `produced_canvas_ids`
are missing from the merged TOML; the skill spot-checks this on resume — the real per-beat safety
net is `package_from_toml` (schema + flag-chain + broken-reference validation; `merge_toml_phases
--validate` only syntax-parses the merged file).
