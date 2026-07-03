# author-game — CHANGELOG

The ledger for this skill. Record **every** change to any file in this skill
(`SKILL.md`, `references/*`, `scripts/*`, etc.) — including small fixes and wording.
Newest first. One bullet per change; group bullets under the date they were made.
Per entry: **what** changed (name the file) — **why** (the motivation / root cause) — and
how it was verified if relevant (grep / build / live-play).

Convention lives in `story_gen_django/CLAUDE.md` → "Skill ledger".

<!-- entries recorded going forward; example shape:
## YYYY-MM-DD
- reworded dispatch note (`SKILL.md`) — clarified phase resume — n/a
-->

## 2026-07-03
- **NEW `references/save-safety.md`** + wiring in `SKILL.md` (Engine-ground-truth item 9, a Knowledge-base
  index bullet, and a reinforcement on the "Structure is stable-and-extensible" operating rule) — the skill
  had **no** release/save-safety doctrine, so after the engine shipped slug passage names + constant slug ids
  + a save-migration seam, nothing told an author which changes still break a *returning player's* save on an
  update. Documents the four join keys that must stay fixed on a shipped game (immutable slugs/ids · never
  rename/repurpose a live flag or trait key · don't rescale a stat range or move tier/stage thresholds · don't
  change the game title) + a pre-update grep-guard checklist + what IS safe (add content, insert/reorder/delete
  beats, rename display names). Verified: every `file:line` cite grepped against the shipped
  `games/vesper/output/index.html` + `v2.py` — slug passage naming (`_node_passage_name` :11246 /
  `_location_passage_name` :11259), `$npcs` slug keying + `npc_slug_map` identity, `Config.saves.id`/`version`
  (:2812), `setup.stateDefaults`/`backfillStateDefaults` (:14549), `npc.id = <slug>` (`game_graph.py:144`).
- **Corrected now-stale engine facts** the same fixes obsoleted (the skill must not teach false engine facts):
  `references/dev-console-jump.md` — node passages are `Node_<nodeSlug>` not the 1-based `Node_<n>`; `$npcs` is
  keyed by slug not `npcs[uuid]`; retired the "NPC uuids regenerate every build → stale-save" framing (the bug
  is fixed); fixed the grep guard (`[0-9]+`→`[a-z_0-9]+`) and the Renner worked example
  (`Node_4`→`Node_base_doggy_r`). `SKILL.md` — the dev-console bullet's `Canvas_<id>_Node_<n>`→`Node_<nodeSlug>`.
  `references/customization.md` — `$npcs[uuid]`→`$npcs[slug]`; `npc_slug_map` `slug→uuid`→identity. Doctrine +
  fact-correction only, zero engine change (the engine work shipped in commits 8446b3d + 1d9ce93).

## 2026-07-02
- **clamp-or-vanish lint** (backlog item #8 from the Vesper→skill analysis) — hardened the banded-stat clamp
  doctrine across 5 files after an unclamped banded body-stat shipped a **blank HUD twice** in Vesper
  (`decisions_log[64]` Charge went negative; `[66]` Condition/hygiene over-capped AND went negative — `[66]`
  records it as the SECOND time and asks for a lint that was never actioned). Root cause: effects run
  `eff.clamp || false` (unbounded by default), and a banded sidebar card only draws when the value lands inside a
  band (`trait_words` closed-match `v2.py:15252`; `trait_status_text` open-on-omit `v2.py:15183`) — out of range
  it renders **nothing**, reading as a *missing* HUD element, not a wrong number, so a quick playtest sails past
  it. Changes: (1) `references/trait-catalog.md` §4 — replaced the advisory "clamp recommended on a restore" with
  the hard two-part rule (bound the value on body-need/resource stats · cover the range for unbounded odometers),
  cross-citing the `engine-reference.md` Clamp trap; fixed the bare-`+N` energy-restore example to `cap = 100`;
  turned the §5 "renders nothing when no band matches" cell into an active pointer to the rule. (2)
  `references/beat-authoring.md` — added a hard clamp row to the Step-7 resource self-audit. (3)
  `references/step-6-feedback.md` — added the review-time "no unclamped banded stat" lint (the hard lint begged
  for twice). (4) `references/toml-gotchas.md` — capped the bare-`+N` Sleep/Shower restore example so it stops
  contradicting the rule. (5) `references/engine-reference.md` — one-clause pointer at the corruption Clamp-trap
  line so mechanism + application agree. Reconciles the "unbounded is correct for corruption" carve-out
  (completes it — the value may climb, but the top band must still cover it) rather than contradicting it; `money`
  stays exempt (unbanded number, never vanishes). Verified: engine facts read from `v2.py` this session;
  grep-consistency across `references/` (no surviving "recommended on a restore" or bare-`+N` counter-example);
  the two load-bearing engine cites re-checked against the current `v2.py` after HEAD moved to `8446b3d`
  (`trait_words` closed-match `:15252`, `trait_status_text` open-bound `:15183`). Doctrine only, zero engine change.

## 2026-07-01
- NEW `references/dev-console-jump.md` + one index line in `SKILL.md` — LO asked to save the browser-console
  "jump/arm" testing technique (fast-forward a built game to a gated state via `State.variables`) as a
  reference, **on-request only**. Documents: serve over `python3 -m http.server 8080` (not `file://`) +
  console context = `top` (not an extension); the `SugarCube` API handle (this build hides bare
  `State`/`Engine`/`setup` globals); the code-verified write paths (`player.core_traits.<k>`,
  `flags.<k>`, `setup.resolveNpcId(slug)`→`npcs[uuid].core_traits`, `Object.values(player.equipped)` for
  equip); `Canvas_<authoredId>_Node_<n>` passage naming (authored ids, stable — NPC uuids are not); ARM vs
  FIRE + the "leave/re-enter to re-eval" caveat; Renner-drain worked example. All paths verified by grepping
  the live `games/vesper/output/index.html` (evaluator branches, passage-name stems all authored-id, no
  uuid). Dev convenience, explicitly gated off the authoring flow.
## 2026-06-23
- NEW `references/onboarding.md` + `references/npc-intro.md` — closed two recurring doctrine gaps an
  adversarially-verified audit found behind LO's "set the player up properly / a new character can't start
  randomly". The skill *declared* the opening must "teach with no tutorial" (step-2 §8, content-framework §1E)
  but never taught the **method**, and treated `npc_intro` as hub-plumbing with no **dramatic** first-encounter
  craft. `onboarding.md` owns the linear-funnel machine-teaching method (surface each live system once in a
  fiction beat; sidebar at value-zero; named next-action on frame one; the three why-locked surfaces; the
  win/fail contract) + a HARD-gate Step-6 rubric. `npc-intro.md` owns the first-encounter craft (pretext +
  name-on-page + hook-as-want → fire once → open the hub; the 7-step Renner template
  `vesper/5_scenes.toml:315-346`; the Hank cold-spawn anti-pattern `late_shifts/5_scenes.toml:14-35`) on top of
  the intact mechanical on-ramp doctrine. LO's locked calls: linear-funnel is the ONLY opening shape; files
  kept split (different lifecycles — onboarding fires once/game, npc-intro every NPC); rubric is a hard gate on
  load-bearing rows. Every engine knob code-verified this session (starting_canvas hard-error
  `template_import.py:6104-6118`; auto-fire `v2.py:4025`; locked_text/cost/blocked_message
  `v2.py:11762/11756/4329`; `start_after_flag`; advanceDay-only-past-24h `v2.py:4958-4999`; quest
  goals/ready_canvas/tip; sidebar bands; `speaker=unknown` `v2.py:13590`; getNpcsWithSchedules leak
  `v2.py:3132`; conditions fail-open `v2.py:3398`; is_container swallow `template_import.py:3506`) — n/a
  (doctrine; dogfooded read-only by running the rubric against Vesper's opening → flags its known machine gaps)
- wired both files in (`SKILL.md` doctrine-library bullets; `step-2-toplevel.md` §8 method pointer;
  `step-5-blueprint.md` Pass-4 opening bullet; `content-framework.md` §1E machine clause + §3B on-ramp pointer;
  `step-6-feedback.md` two self-check rubric rows; `hud.md` §1 persistent-tutorial note; `lanes.md` `npc_intro`
  beat-type expanded from plumbing to designed-encounter; `beat-authoring.md` cold-start firewall + cold-spawn
  ban; `step-3-casting.md` hook→first-encounter forward wire) — why: a reference is dead unless the steps cite
  it where the author works — grep-verified the pointers resolve to the new files

## 2026-06-22
- NEW `references/media.md` — the skill had almost NO media doctrine (its whole footprint was a 1-line block-
  vocab mention + 1 location field in `engine-reference.md`), so authors hand-rolled media and missed the
  acquisition layer: Vesper (and Last Call, Late Shifts) shipped image refs with no `search_queries`, no video,
  silently-skipped media. media.md owns it: the 3 block types (`image`/`video`/`clip`) from engine truth, the
  extension-agnostic resolve law, the silent-skip-when-missing model, the `search_queries` craft (grafted from
  `prompts/toml_generation_prompt_v4.txt:905-1001`), the tier→format contract, the text-media-text rhythm
  (`prompts/media_writing_guide.md:657-705`), folder/naming, the `find-media` hand-off — with 4 corpus lies
  explicitly corrected (clip-uses-`file`; extension-is-authoritative; "t5+ must be webm or it won't render";
  inline `[image:]` syntax). Every engine claim re-verified against `v2.py`/`template_import.py` this session —
  n/a (doctrine; dogfooded by rebuilding Vesper with `search_queries` → Missing-Media page populated)
- wired media.md in (`SKILL.md` doctrine-library bullet; `engine-reference.md` §2.5 clip `{props.file}`→
  `{props.clipId}` fix + media.md pointer, and the `image_search_queries` row's key-name-trap note;
  `beat-authoring.md` Step-7 media instruction; `step-5-blueprint.md` Pass-2 **Media** placement bullet;
  `rts-flat-prose.md` Rule 8 — flagged the `[image:]` shorthand as non-engine, point to real TOML) — why: a
  reference is dead unless the steps cite it where the author works — grep-verified pointers resolve to media.md

## 2026-06-18
- added skill-ledger pointer note in the State section (`SKILL.md`) — distinguishes the game ledger
  (`authoring_state.json`) from this skill's own ledger (`CHANGELOG.md`); part of introducing the
  per-skill CHANGELOG convention (documented in `CLAUDE.md` → "Skill ledger") — n/a (docs only)
