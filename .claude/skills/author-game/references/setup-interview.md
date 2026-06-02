# Setup mode — the one-time interview

Goal: lock the structural skeleton + seed a loose, revisable roadmap, then emit a buildable
**empty** game + a seeded ledger. **No canvases are authored in setup.**

## Step 1 — Load the doctrine you need
Read the relevant parts of `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md`: arc shapes, the time
model, location design (containers / hubs / locks + the unlock contract), `[settings]` scoping
(clothing / rent / phone), and the Phase 2+ decisions (pregnancy / scandal / gallery / tracker).
Use `games/late_shifts/toml_phases/` as the structural reference for TOML table shapes.

## Step 2 — Interview (one question at a time, via AskUserQuestion)
Each question: 2–4 concrete options + a recommendation. **Skip any question already answered by
the concept input or with a safe doctrine default — state the default, don't ask.**

1. **Premise / setting / player character** — who the player is, where, the hook.
2. **Economic engine + time model** — money pressure + day/period structure (offer the doctrine
   default time model; only ask if the concept overrides it).
3. **Cast** — propose 4–6 NPCs with arc shapes (from the arc-shapes doctrine); LO reshapes.
4. **Location graph** — propose hubs / containers / locks from cast + premise; LO reshapes. Apply
   the unlock contract to any locked location that will host an NPC schedule.
5. **Phase 2+ decisions** — pregnancy / scandal / gallery / tracker (include vs defer).
6. **Kink / vocab ceilings.**
7. **The loose end-to-end roadmap** — draft an ordered, sketchy, fully-reorderable beat list
   (intro → first job → meet X → unlock downtown → buy home → … → endgame); LO reorders / cuts /
   adds. This seeds the ledger `plan`. It is a hypothesis, not a contract.

## Step 3 — Write `design_book.md`
To `games/<slug>/design_book.md`: premise, player, economic engine, time model, cast + arc
shapes, location graph, and the locked-in loose roadmap. This is the intent record.

## Step 4 — Write the scaffold TOML (no canvases)
- `games/<slug>/toml_phases/0_systems_spec.toml` — `[settings]` (correct clothing/rent/phone
  scoping if used) + engine config.
- `games/<slug>/toml_phases/1_metadata_and_locations.toml` — metadata, locations (with
  `entry_conditions` + `blocked_message` for locks), npcs, `[[npcs.schedules]]`.
- No `[[canvases]]` yet. Mirror the table shapes in `games/late_shifts/toml_phases/`.

## Step 5 — Seed the ledger (`authoring_state.json`, written directly)
Create `games/<slug>/authoring_state.json` per `references/ledger-schema.md`:
- start from the v1 shape (`init`-equivalent), `game_slug` = `<slug>`, `book_revision` = 1.
- `structure_registry`: list every location / npc / flag the scaffold declares.
- `plan`: one beat per roadmap item, `id` = `beat_0001`, `beat_0002`, … (zero-padded, monotonic),
  `status` = `planned`, `target_phase` set to where its canvases will go (e.g. `5_scenes.toml`),
  `introduces` filled if the beat will add new structure.
- `next_up`: the beat ids in intended authoring order.
- `decisions_log`: one entry noting setup completion.

## Step 6 — Prove green (the empty scaffold must build)
```bash
python scripts/merge_toml_phases.py games/<slug> --validate
python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml \
  --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/<slug>/output --dev
```
Both must pass (validation + flag chains; `index.html` produced) before setup is "done".

## Step 7 — Report
Show the roadmap back and tell the user: **"Setup complete — say *continue* to author the first beat."**

## Anti-patterns
- Do NOT author canvases in setup.
- Do NOT ask questions with safe doctrine defaults — default and say so.
- Do NOT invent engine knobs; every option offered must be real (cite the doctrine/schema).
- Do NOT leave a locked location reachable only via itself, or a flag with no reachable setter.
