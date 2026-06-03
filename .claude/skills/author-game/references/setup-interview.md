# Setup mode — the one-time interview

Goal: lock the structural skeleton + per-NPC R7 briefs + a loose, revisable roadmap, then emit a
buildable scaffold (skeleton + the minimal boot canvas + the spine quest card) + a seeded ledger.
**No STORY canvases in setup** (NPC arcs/hubs/ambients/capstones) — those are beats.

## Step 1 — Load the doctrine you need
Read the relevant parts of `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md`: arc shapes, the time
model, location design (containers / hubs / locks + the unlock contract), `[settings]` scoping
(clothing / rent / phone), and the Phase 2+ decisions (pregnancy / scandal / gallery / tracker).
Use `games/late_shifts/toml_phases/` as the structural reference for TOML table shapes.

## Step 1.5 — Determine scope mode (do this BEFORE the interview)
Read `scope_mode` from the concept input; if absent, **default to `full_game`** (`stages/01` §0.5).
It drives budgets, the Phase 2+ flow, and depth — record it in the ledger (`scope_mode`).
- **`full_game`** (default) — the COMPLETE game. Full per-arc-shape canvas budgets
  (`doctrine/03` §2 / `lanes.md`). Full Stage 0→4 per NPC, full capstone chains. The Phase 2+ Q&A
  (Step 2 item 5) RUNS.
- **`slice`** — a shippable validating chunk (~10–14 day window): **1 NPC at full (gold-standard)
  depth + 4–5 at minimum-contract depth** (~30–50% of budget), with locked-visible rungs
  telegraphing the deferred remainder. **All four Phase 2+ decisions default to defer — SKIP the
  Q&A.** State this; don't ask.

## Step 2 — Interview (one question at a time, via AskUserQuestion)
Each question: 2–4 concrete options + a recommendation. **Skip any question already answered by
the concept input or with a safe doctrine default — state the default, don't ask.**

1. **Premise / setting / player character** — who the player is, where, the hook.
2. **Economic engine + time model** — money pressure + day/period structure (offer the doctrine
   default time model; only ask if the concept overrides it).
3. **Cast** — propose 4–6 NPCs with arc shapes (from the arc-shapes doctrine); LO reshapes.
4. **Location graph** — propose hubs / containers / locks from cast + premise; LO reshapes. Apply
   the unlock contract to any locked location that will host an NPC schedule.
5. **Phase 2+ decisions (full_game only — slice defers all four, no Q&A).** Ask ONE at a time, in
   order: **pregnancy → scandal → gallery → tracker** (`stages/01` §0.5.2). Skip any the concept
   already declared. **An `include` is not a toggle — the design book MUST name HOW it's mechanized,
   or it ships dormant and the validator won't catch it** (the Late Shifts pregnancy-with-no-setter
   precedent). For each `include`, record:
   - **Pregnancy** → the setter (e.g. an `had_unprotected_sex` flag from first-full-sex capstones →
     a hidden onset canvas that sets `player.pregnancy`) + which NPCs get pregnant-variant content
     (each needs an ongoing sex surface for the variants to attach to).
   - **Scandal** → the awareness-accumulator owner (an antagonist/witness NPC), which beats raise
     awareness, and the confrontation capstone's threshold + (shared/public) location.
   - **Gallery** → confirm the trigger is met (9+ once-only capstones planned). **Tracker** → the
     per-canvas `guide` field.
6. **Per-NPC vocab / kink ceiling** — for each NPC, declare the kink area + its full-intensity
   ceiling (recorded in that NPC's R7 brief, Step 3). **Default to the MOST explicit interpretation**
   in any ambiguity (`doctrine/08` §2/§3 — the 2026-05-16 maximum-explicit pattern). Per-NPC, not
   one register across the cast (Frank-full-explicit vs Marcus-peer). When you offer a recommendation
   on a content question, the doctrine default is *more* explicit, never softer.
7. **The loose end-to-end roadmap** — draft an ordered, sketchy, fully-reorderable beat list
   (intro → first job → meet X → unlock downtown → buy home → … → endgame); LO reorders / cuts /
   adds. This seeds the ledger `plan`. It is a hypothesis, not a contract.

## Step 3 — Write `design_book.md`
To `games/<slug>/design_book.md` — the intent record (a NEW artifact; LS's nearest equivalent is its
`concept.md`). Sections:
- **World setup** — premise, player, economic engine, time model, `scope_mode`, the four Phase 2+
  calls (with the mechanization recorded for any `include`), and the locked-in loose roadmap.
- **Locations** — the graph (hubs / containers / locks).
- **Per-NPC R7 brief** (one per NPC — the corpus's core Stage-1 deliverable, `doctrine/06` /
  `stages/01` Step 5). Each brief commits the intent the continue loop must honor:
  - **Arc shape + lane budget** (the specific numbers within the shape's range, per `lanes.md`).
  - **Voice spec** — how this NPC sounds; RTS-flat register for Lane 1/2/3.
  - **Per-tier vocab ceiling** — what's allowed at full intensity (from interview item 6;
    default-to-maximum-explicit), tier by tier.
  - **Stat ladder** — the stage flags + the corruption/relation thresholds each rung gates on.
  - **Per-NPC anti-patterns** — what NOT to do for this NPC (e.g. empty Lane 3 for peer/dating).
  This is where voice/ceiling/ladder intent lives; the per-beat loop reads it instead of re-deriving.

## Step 4 — Write the scaffold TOML (skeleton + the opening canvas only)
- `games/<slug>/toml_phases/0_systems_spec.toml` — `[settings]` (correct clothing/rent/phone
  scoping if used) + engine config.
- `games/<slug>/toml_phases/1_metadata_and_locations.toml` — metadata, locations (with
  `entry_conditions` + `blocked_message` for locks), npcs, `[[npcs.schedules]]`.
- The **minimal intro / Start canvas** the engine needs to open the game (Day-1 bootstrap that
  drops the player into the starting location). This is structural bootstrap, NOT story content —
  do not author any NPC arcs, hubs, ambients, or capstones in setup. Mirror the opening canvas in
  `games/late_shifts/toml_phases/` for the exact table shape.
- The **spine quest card** (one `[[quest_cards]]`, no `npc_id` → renders in the top "Story Goals"
  section). If you set `quests_engine = "v2"` you MUST populate the Quests page, or it renders empty
  and reads as broken. The spine = the game's central pressure from the economic engine / premise
  (e.g. "Pay Boyd $200 every Monday or lose the bar"). Use a mechanic-mode card (a `goals` trait
  gate like `money >= <amount>`, no `ready_canvas`) gated `when` the debt is active. Fields +
  shape: see `beat-authoring.md` "Quest cards" + `prompts_v2` `schema/02` §8. This is the ONLY
  story-bearing content setup authors — everything else is beats.
- Mirror all table shapes from `games/late_shifts/toml_phases/`.

## Step 5 — Seed the ledger (`authoring_state.json`, written directly)
Hand-construct `games/<slug>/authoring_state.json` by copying the v2 JSONC block in
`references/ledger-schema.md` and filling it in (there is no `init` tool — you write the file):
- `game_slug` = `<slug>`, `book_revision` = 1, `scope_mode` = `full_game` | `slice`.
- `npcs`: one entry per NPC with `{ arc_shape, lane_budget, vocab_ceiling }` from its R7 brief, so
  the continue loop knows each NPC's shape, how much is left to author, and its ceiling.
- `structure_registry`: list every location / npc / flag the scaffold declares.
- `plan`: one beat per roadmap item, `id` = `beat_0001`, `beat_0002`, … (zero-padded, monotonic),
  `status` = `planned`, `target_phase` set to where its canvases will go (e.g. `5_scenes.toml`),
  `introduces` filled if the beat will add new structure.
- `next_up`: the beat ids in intended authoring order.
- `decisions_log`: one entry noting setup completion.

## Step 6 — Prove green (the scaffold must build)
Run with the repo venv active (`source venv/bin/activate`):
```bash
python scripts/merge_toml_phases.py games/<slug> --validate   # syntax-parses the merged TOML only
python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml \
  --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/<slug>/output --dev
```
The second command does the REAL validation (schema + flag chains) and produces `index.html`;
both must pass before setup is "done".

**Owner-id note:** `--owner-id` must be an existing user in this DB. The UUID above is this
repo's known owner. If you hit `Owner with ID ... not found`, the DB isn't seeded with it — find
a real one (`python manage.py shell -c "from apps.authentication.models import User; print(User.objects.first().id)"`)
or create one (`createsuperuser`), and use that id.

## Step 7 — Report
Show the roadmap back and tell the user: **"Setup complete — say *continue* to author the first beat."**

## Anti-patterns
- Do NOT author STORY canvases (NPC arcs / hubs / ambients / capstones) in setup — only the
  minimal boot canvas + the spine quest card. Everything else is beats.
- Do NOT enable `quests_engine = "v2"` without authoring the spine quest card — an empty Quests
  page reads as broken.
- Do NOT ask questions with safe doctrine defaults — default and say so.
- Do NOT invent engine knobs; every option offered must be real (cite the doctrine/schema).
- Do NOT leave a locked location reachable only via itself, or a flag with no reachable setter.
