# Scope Brief — `lab_room`

Slot 10 — SFW static. Proves the image path and contact-sheet judging.

> **WATERMARK RISK. The shelf for this slot is dominated by stock-photo hosts (dreamstime 50, alamy 22, shutterstock 21, istock 20, vecteezy 17) whose previews carry watermarks ACROSS the subject — a Gate-1 fail, not a craft deduction. Expect to reject a lot of this pool on that alone.**

## Identity

- **item_id**: `lab_room`
- **file_path**: `scenes/lab_room.jpg`
- **type**: `image`
- **category**: `Activities`
- **canvas_id**: `canvas_lab`
- **order**: 10
- **tier**: `base`
- **content_rating**: `sfw`
- **required_format**: static `.jpg` — NO strip, judged from the contact sheet
- **discovered_by**: `toml_walker` (Django not installed in this cloud session; the walker is
  the authoritative missing list here — 10 refs, 10 missing, `videos/` absent entirely)
- **scene_id for capture**: `scenes/lab_room`

## Narrative context

This game is a test rig, not a story — one canvas, ten slots, no surrounding prose. The
beat below IS the full narrative context.

> A small, bare, run-down room in daylight with nobody in it — a stripped mattress, a window with no curtain, marks on the wall. Empty and a little grim.

## Demand — what this slot has to deliver

### setting_is_load_bearing: `true`

> Why: The room IS the subject. Squalor is the explicit ask ('empty and a little grim'), so the setting axis is scored, not skipped.

**Axis split for this slot: LIFE 50 / SETTING 25 / CRAFT 25 (SFW axis set)**

### intended_heat

LIFE (heat's SFW name) — does it look like a real room somebody left, or like a stock render of the concept 'abandoned room'?

### must_show

- an interior
- NO people
- visible wear — marks, peeling, stains
- daylight

### avoid

- anyone in shot
- styled or staged interiors
- a hotel-brochure look
- a heavy watermark across the subject
- obvious AI artifacts

### POV case

N/A — no people.

### strip checklist (derived)

1. MUST: an interior
2. MUST: NO people
3. MUST: visible wear — marks, peeling, stains
4. MUST: daylight
5. AVOID: anyone in shot
6. AVOID: styled or staged interiors
7. AVOID: a hotel-brochure look
8. AVOID: a heavy watermark across the subject
9. AVOID: obvious AI artifacts

## Derived facts

type: static image, SFW. Axes are the SFW set: LIFE 50 / SETTING 25 / CRAFT 25. Resolution DOES cost real craft points here — a nav-style image renders large and static, so softness shows.

## Queries

**FROZEN — experiment constant. Do not edit, do not rewrite.** The shelf is pre-stocked
from these; SEARCH does not run in this arm (no Chrome in a cloud session).

## Mode

Selected mode: `fill` — option target 6, strip top 0 by rank.

## Resume marker

```
PHASE: scope_complete
NEXT_PHASE: judge
OPTIONS_STOCKED: pre-stocked (experiment constant)
INSTALLED: no
```
