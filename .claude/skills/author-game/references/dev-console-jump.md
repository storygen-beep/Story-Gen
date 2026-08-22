# Dev console jump / arm scripts — fast-forward a built game to a target state

A **browser-console** technique for testing a built game: set `State.variables` directly and (optionally)
jump to a passage, so you reach a gated scene in seconds instead of grinding the whole path. Two shapes:

- **ARM** — set the gating state only, then hand control back. The user navigates in-game and triggers the
  target beat *themselves* (natural play). No `Engine.play`.
- **FIRE** — set the state **and** `Engine.play(...)` into the target node, so the beat is one click away
  (or renders immediately).

This is a headed, human-in-the-loop cousin of the automated Playwright harness (memory
`playwright-live-test-built-games`), which runs the *same* SugarCube API from Node for regression checks.

---

## ⚠️ On request ONLY

**Never generate one of these unprompted.** Only produce a jump/arm script when the user explicitly asks
for one (e.g. "give me the console script to get to X"). It is a dev/debug convenience, not part of the
authoring flow, and it writes directly into save state — offering it uninvited is noise. When asked, build
it fresh against the **current** build (canvas ids and gates change as the game is edited).

---

## Prerequisite — serve the built HTML over HTTP (not `file://`)

The game must be served from an HTTP origin. From the game's output dir:

```bash
cd games/<game>/output && python3 -m http.server 8080
```

Then open **`http://127.0.0.1:8080/index.html`**. (VS Code Live Server on `:5500` works too — any real
HTTP origin. `file://` breaks media/relative loads.)

**Console context must be `top` = the game page.** In Chrome DevTools the context dropdown (top-left of the
Console, says `top`) also lists browser *extensions* (Browser MCP, VeePN, etc.) — running in one of those is
the #1 reason `State`/`SugarCube` come back `undefined`. Select the entry whose URL is the game's
`index.html`. Sanity line:

```js
console.log(location.href, '| State:', typeof State, '| SugarCube:', typeof SugarCube,
            '| passages:', document.querySelectorAll('tw-passagedata').length);
```

`passages > 0` + `SugarCube: object` = you're on the game page.

---

## The SugarCube handle (this build)

This build does **not** expose bare `State` / `Engine` / `setup` as window globals — they live on the
`SugarCube` object. Always grab them off it:

```js
var SC = window.SugarCube;
var State = SC.State, Engine = SC.Engine, setup = SC.setup;
```

(If a future build exposes bare globals, `SC` still works — prefer it.)

**Same rule inside a headless test.** Playwright's `page.evaluate("setup.getTraitValue(...)")`
throws `ReferenceError: setup is not defined` — the story JS runs in SugarCube's own closure,
not on `window`. Use `SugarCube.setup.…` / `SugarCube.State.…` / `SugarCube.Engine.…` in every
evaluated string. (Hit live, 2026-08-23, testing Vesper's cheat box.)

---

## State read/write paths (code-verified against the generated `output/index.html`)

| What | Path | Notes |
|---|---|---|
| Player trait | `State.variables.player.core_traits.<key>` | every `subject:"player"` trait (money, `corruption`, and custom ones like `equipped_weapon`, `drain_charge`, `loop_npc_pleasure`, `sex_stage`, `anal_active`, `drains_done`) |
| Flag | `State.variables.flags.<key> = true` | object keyed by flag name; truthy = set. `is_false` gates want the key absent/false |
| NPC record | `State.variables.npcs["<slug>"].core_traits.<key>` (or `setup.resolveNpcId("<slug>")` → canonical slug, then index) | `$npcs` is keyed by the npc **slug** — stable across builds. `setup.npc_slug_map` is identity for canonical slugs + maps bare aliases (`"renner"`→`"npc_renner"`). Ids no longer regenerate, so old saves carry forward |
| Clothing equipped | `Object.values(State.variables.player.equipped).indexOf("<item_id>") !== -1` | the engine's `operator:"equipped"` test. Force-equip by assigning any slot key: `player.equipped.top = "<item_id>"` |
| Jump to a passage | `Engine.play("Canvas_<canvasId>_Node_<nodeSlug>")` | see naming below |

### Passage naming — stable slugs, no UUIDs, no positions
Canvas node passages are `Canvas_<canvasId>_Node_<nodeSlug>`:
- `<canvasId>` = the canvas's **authored `id`** string (e.g. `loop_renner_office_sex`) — **stable across builds**.
- `<nodeSlug>` = the node's **authored `id`** (e.g. `intro`, `base_doggy_r`) — also stable. (It used to be the
  node's 1-based *position*; that was changed to the slug so inserting/reordering a beat can't shift other
  nodes' passage names and break returning players' saves — see `references/save-safety.md`.)

Location passages are `Location_<locSlug>` (the location's authored `id`, not its display name).

Always confirm the exact name against the current build:
```bash
grep -oE 'name="Canvas_<canvasId>_Node_[a-z_0-9]+"' output/index.html
```

---

## Method — derive the gates, then arm or fire

1. **Find the target beat** in the game's TOML (`games/<game>/toml_phases/5_scenes.toml` etc.). Read the
   node/choice that *is* the payload and the conditions on the path into it — flags, traits (player + npc),
   clothing, weapon/charge, daily caps.
2. **List the exact gates.** For a FIRE-to-one-click, only the gates on the **final node + its trigger
   choice** matter. For an ARM (natural play), include every gate on the **whole path** from the hub in
   (hub visibility → register unlock → pose/tier unlock → finish condition).
3. **Set precisely those.** Don't over-set — but do set the whole chain for ARM, or the beat won't be
   reachable by walking in.
4. **ARM:** stop here (no `Engine.play`). **FIRE:** `Engine.play("Canvas_<id>_Node_<nodeSlug>")` into the node
   whose on-screen choice is the payload.
5. **ASCII only, straight quotes.** Rendered smart-quotes/em-dashes paste as invalid tokens. If Chrome
   refuses the paste, type `allow pasting` once (its self-XSS guard).

### ARM caveat — state doesn't re-eval the current canvas
Writing `State.variables` does **not** re-run gates on the passage you're already standing on. After an ARM,
**leave the location and re-enter** (or navigate somewhere and back) so the hub/register re-evaluates with
the new corruption/flags. (Same reason dev "+1hr" doesn't re-eval canvases — leave + re-enter.)

---

## Worked example — the Renner drain (Vesper)

The drain fires inside `loop_renner_finisher`: the **ass** finish with `drains_done < 1`, `equipped_weapon
== 1`, `drain_charge >= 1` routes to `renner_control_canvas.intro` (the full extraction). Path in: depot hub
(in cover) → "Take him in the office" (needs `renner_office_open` + `renner_oral_once` + npc
`corruption >= 40`) → loop → doggy pose ("give him your ass": npc `corruption >= 50` + cover) → build
`loop_npc_pleasure >= 50` → "finish in your ass".

**ARM** (walk in and trigger it yourself) — set the whole path open, no jump:

```js
(function () {
  var SC = window.SugarCube;
  if (!SC || !SC.State) { console.error("SugarCube not ready."); return; }
  var State = SC.State, setup = SC.setup, sv = State.variables;
  if (!sv || !sv.player || !sv.player.core_traits) { console.error("Start the game first."); return; }
  var t = sv.player.core_traits;
  t.equipped_weapon = 1; t.drain_charge = 3; t.drains_done = 0;   // gear: drain, charged, unused
  sv.flags = sv.flags || {};
  ["renner_hired","renner_office_open","renner_oral_once","renner_flirts_back"].forEach(function (f) { sv.flags[f] = true; });
  sv.flags.renner_drained = false;
  var rid = setup.resolveNpcId("npc_renner");
  if (rid && sv.npcs && sv.npcs[rid]) {                            // broken to 50 -> office + drain pose open
    sv.npcs[rid].core_traits = sv.npcs[rid].core_traits || {};
    sv.npcs[rid].core_traits.corruption = 50; sv.npcs[rid].core_traits.relation = 20;
  }
  sv.player.equipped = sv.player.equipped || {};                  // cover on (depot squints out of cover)
  if (Object.values(sv.player.equipped).indexOf("cover_dockhand") === -1) { sv.player.equipped.top = "cover_dockhand"; }
  console.log("Armed. Leave + re-enter the depot, then play into the office to the ass finish.");
})();
```

**FIRE** (one click from the drain) — add the loop-internal traits and jump onto the doggy pose
(node `base_doggy_r` of `loop_renner_office_sex`):

```js
  // ... same gear + flags + npc as above, plus:
  t.loop_npc_pleasure = 50; t.sex_stage = 2; t.anal_active = 1;   // he's close; anal allowed
  Engine.play("Canvas_loop_renner_office_sex_Node_base_doggy_r"); // on-screen "finish in your ass" -> drain
```

(The FIRE build also needs `renner_fucked_once`/`renner_anal_once` flags set only if a *later* gate reads
them; the drain itself branches on the `drains_done` trait, not `renner_drained` — see 5_scenes.toml.)

---

## Housekeeping
- The helper `.js` these get saved to is a debug artifact — keep it **out of commits** (media/output
  convention already ignores `output/`, but a loose `renner_drain_jump.js` in the game dir is not; delete it
  when done or don't stage it).
- Related: `engine-reference.md` (field/condition tables), memory `playwright-live-test-built-games`
  (automated variant), memory `quest-card-ladder-and-renderer` (quest-state reads).
