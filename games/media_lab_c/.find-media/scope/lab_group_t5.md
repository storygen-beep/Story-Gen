# Scope Brief — `lab_group_t5`

Slot 7 — count gate. A visible three-plus, where the multi-man word gets dropped.

> **TOOL TRAP: arm B found a 390x909 candidate here that is unreadable squeezed into a default 320px board row — the men could not be counted. Re-check tall candidates at --tile-px 480 before calling a count.**

## Identity

- **item_id**: `lab_group_t5`
- **file_path**: `scenes/lab_group_t5.webm`
- **type**: `video`
- **category**: `Activities`
- **canvas_id**: `canvas_lab`
- **order**: 7
- **tier**: `t5`
- **content_rating**: `nsfw`
- **required_format**: animated (`.webm`/`.mp4`/`.gif`) — frame strip MANDATORY
- **discovered_by**: `toml_walker` (Django not installed in this cloud session; the walker is
  the authoritative missing list here — 10 refs, 10 missing, `videos/` absent entirely)
- **scene_id for capture**: `scenes/lab_group_t5`

## Narrative context

This game is a test rig, not a story — one canvas, ten slots, no surrounding prose. The
beat below IS the full narrative context.

> One woman and a ring of at least three men around her, all clearly in frame at the same time.

## Demand — what this slot has to deliver

### setting_is_load_bearing: `false`

> Why: The count is the content; the room is irrelevant.

**Axis split for this slot: HEAT 85 / SETTING null (skipped) / CRAFT 15**

### intended_heat

POWER / being surrounded. The number is the beat.

### must_show

- 3+ men visible SIMULTANEOUSLY in one frame
- exactly one woman

### avoid

- one or two men
- a POV crop that hides how many there are
- cutting between men so the group is never seen together

### POV case

DEFECT. You cannot count a crew you cannot see.

### strip checklist (derived)

1. MUST: 3+ men visible SIMULTANEOUSLY in one frame
2. MUST: exactly one woman
3. AVOID: one or two men
4. AVOID: a POV crop that hides how many there are
5. AVOID: cutting between men so the group is never seen together

## Derived facts

act: group / count: 1F + 3M MINIMUM, simultaneous / setting: not scored. Count is a Gate-1/Gate-3 binary in BOTH directions — two men fails no matter how good the clip is.

## Queries

**FROZEN — experiment constant. Do not edit, do not rewrite.** The shelf is pre-stocked
from these; SEARCH does not run in this arm (no Chrome in a cloud session).

## Mode

Selected mode: `wide` — option target 12, strip top 6 by rank.

## Resume marker

```
PHASE: scope_complete
NEXT_PHASE: judge
OPTIONS_STOCKED: pre-stocked (experiment constant)
INSTALLED: no
```
