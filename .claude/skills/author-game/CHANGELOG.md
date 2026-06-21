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
