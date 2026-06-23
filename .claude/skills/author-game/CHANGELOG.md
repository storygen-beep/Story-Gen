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
