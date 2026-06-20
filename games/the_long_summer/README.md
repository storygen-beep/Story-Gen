# The Long Summer

Rural coming-of-age + economic pressure hybrid. Female protagonist (Maya, 18) arrives in a small Southern town with a permissive moral register, staying at her stepfather Frank's house alongside her mother Diana and Frank's two grown sons (Ryan, Jake). As she learns what her body and her wits can earn, the player decides which parts of herself she keeps — and how much she walks away with.

Adult interactive fiction. Multi-NPC parallel-arc architecture. Corruption-driven progression with economic pressure as motivator.

## Project stage

**Pre-content.** Design is locked; engine is ready; book-phase content generation is the active work.

- **Design:** ✅ Locked in `../19th_april_UOR_Redesign_Session/Game_Redesign.md` (1,460 lines, 12 sections).
- **Engine:** ✅ F1–F4 changes shipped (see `../19th_april_UOR_Redesign_Session/Engine_PRD.md`).
- **Book:** 🔄 In progress. See `session_state.yaml` for per-phase status.
- **TOML:** 🔒 Not started. Runs after book is complete.

## Folder map

```
the_long_summer/
├── book_phases/              ← CURRENT WORK — phase files being generated
│   ├── 1_foundation.md
│   ├── 2_characters_and_stats.md
│   ├── 2b_systems_budget.md
│   ├── 3_world_design.md
│   ├── 4_story_events.md
│   ├── 5_activities.md
│   ├── 6_story_arc.md
│   └── final_book.md         ← compiled at end
├── toml_phases/              ← NEXT STAGE — filled by TOML translator after book
├── integrations/             ← FUTURE — reserved for video integrations
├── concept.md                ← 1-page pointer to redesign doc
├── session_state.yaml        ← lifecycle + locked constraints
└── README.md                 ← this file
```

## How to work on this

1. **Read** `session_state.yaml`'s `locked_constraints` block. Every phase honors them.
2. **Read** `../19th_april_UOR_Redesign_Session/Game_Redesign.md` for design detail.
3. **Reference** `../../prompts/game_book_prompt_v6.txt` for phase structure and `../../prompts/game_design_rules.md` for the 17 rules enforced on every beat.
4. **Do NOT** modify the redesign doc, the engine code, or the prompts. Those are fixed inputs.
5. **Resolve placeholders** (town name, rent amount, cast names, etc.) per `session_state.yaml:placeholders_to_resolve` in the phase each is assigned to.
6. **Update** `session_state.yaml:phase_progress` when each phase is completed.

## Locked constraints — highlights

The following MUST NOT be re-designed during book generation (see `session_state.yaml:locked_constraints` for full list):

- **10 player traits only:** energy, hygiene, fitness, beauty, corruption, calculation, money, rep_church, rep_road, rep_college. Corruption is bundled (not split).
- **Frank's trigger:** Maya masturbating in the living room. Fixed.
- **Ryan's Crack:** Beach proposal after the big-ticket sex-closed deal. Fixed shape.
- **Jake's arc:** hostile → noticed → peek+draw → caught → hand. Fixed.
- **Diana:** household anchor only. NO confrontation in Phase 1.
- **Marge:** simple employer. NO sexual arc (deferred).
- **Shadow layer:** deferred. NO criminal plot in Phase 1.
- **Calendar:** Sunday only in Phase 1. Friday football / Saturday market / fair / bar are Phase 2+.

## Reference (structural model, NOT content input)

- `../under_one_roof/final_book.md` — completed UOR book for scale/format/depth calibration
- `../under_one_roof/book_phases/` — per-phase file structure

UOR is a structural cousin (shared-house, parallel NPC arcs, corruption-driven) but its cast, specific scenes, and register are different. Do not let UOR content bleed into The Long Summer content.

## Governance

- Design PRD: `../../../.claude/plans/lets-create-a-prd-staged-salamander.md`
- Status: PRD approved 2026-04-22
- Current phase: see `session_state.yaml`
