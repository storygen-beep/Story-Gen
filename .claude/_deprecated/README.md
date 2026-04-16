# Deprecated

Files here were replaced by `.claude/skills/find-media/` on 2026-04-14.

## Why deprecated, not deleted

Not git-tracked in this repo. Kept here as an archival reference for the transition. Delete once you've run the new skill against 2–3 games and confirmed parity.

## What was replaced

| Old file | Replaced by | Why |
|----------|-------------|-----|
| `commands/find-media.md` | `skills/find-media/SKILL.md` + references | Depended on disconnected `mcp__browsermcp__*` tools. Confidence thresholds diverged from the real prompt (80% here, 60% in image_finder_prompt.md). GIPHY/Tenor source paths never worked in practice. |
| `agents/media-finder.md` | `skills/find-media/SKILL.md` §Subagent dispatch | Same browsermcp dependency. Overlapped with find-media.md command — two docs saying similar things with drift between them. |

The canonical source (`prompts/image_finder_prompt.md`) stays for now as transitional reference, to be deleted once the skill is verified.
