---
name: author-game-v2-lean
description: Lean rebuild of author-game-v2 (same doctrine, smaller shape). Not usable yet — the exam baseline for v2 is being recorded first. Call it by name only.
disable-model-invocation: true
---

# author-game-v2-lean

**Status: not yet usable.** Use `/author-game-v2` for real work.

This skill is being rebuilt from `author-game-v2` in small, tested steps:

1. An exam of real past authoring mistakes scores the current v2 (`.claude/skill-evals/author-game/`).
2. This entry skill then becomes a short router into a few small shared skills, each under about 2,000 words.
3. Every step must score at least as well as v2 on the same exam before it replaces anything.

The doctrine is not copied here. When this skill needs a rule's reasoning, it reads it from
`.claude/skills/author-game-v2/references/`, which stays the single source.

If you were sent here for real authoring work, stop and tell LO this skill is still under construction.
