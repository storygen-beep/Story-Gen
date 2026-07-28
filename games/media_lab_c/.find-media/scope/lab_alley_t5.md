# Scope Brief — `lab_alley_t5`

Slot 4 — dark outdoors. The one slot where the setting IS the meaning.

## Identity

- **item_id**: `lab_alley_t5`
- **file_path**: `scenes/lab_alley_t5.webm`
- **type**: `video`
- **category**: `Activities`
- **canvas_id**: `canvas_lab`
- **order**: 4
- **tier**: `t5`
- **content_rating**: `nsfw`
- **required_format**: animated (`.webm`/`.mp4`/`.gif`) — frame strip MANDATORY
- **discovered_by**: `toml_walker` (Django not installed in this cloud session; the walker is
  the authoritative missing list here — 10 refs, 10 missing, `videos/` absent entirely)
- **scene_id for capture**: `scenes/lab_alley_t5`

## Narrative context

This game is a test rig, not a story — one canvas, ten slots, no surrounding prose. The
beat below IS the full narrative context.

> A couple fucking outdoors at night against a wall in a filthy back alley, both bodies visible, lit only by whatever streetlight reaches them.

## Demand — what this slot has to deliver

### setting_is_load_bearing: `true`

> Why: The squalor and the risk of being seen ARE the charge. The beat says a clean bright room would kill it entirely. This is the documented load-bearing case — bright clips were rejected twice on this beat class.

**Axis split for this slot: HEAT 60 / SETTING 25 / CRAFT 15**

### intended_heat

SQUALOR plus EXPOSURE/RISK. The room is wrong for this and it is happening anyway.

### must_show

- outdoors
- night
- a wall or alley visible
- both people visible

### avoid

- any interior
- daylight
- studio lighting
- POV framing that hides one of them

### POV case

DEFECT. The beat requires both bodies visible; a POV camera removes one of them.

### strip checklist (derived)

1. MUST: outdoors
2. MUST: night
3. MUST: a wall or alley visible
4. MUST: both people visible
5. AVOID: any interior
6. AVOID: daylight
7. AVOID: studio lighting
8. AVOID: POV framing that hides one of them

## Derived facts

act: penetrative, standing against a wall / count: 2 / setting: SCORED, 25 pts — night, alley, grime, streetlight. A bright or interior clip scores 0-5 here, not a gate fail (wrong_setting is not a valid gate reason).

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
