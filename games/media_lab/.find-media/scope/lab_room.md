# Scope Brief — `lab_room`  (slot 10 of 10)

## Identity
- **file_path**: `scenes/lab_room.jpg`   ← verbatim key for options store / review store / dedupe
- **type**: image | **category**: Other | **canvas_id**: canvas_lab
- **tier**: base | **content_rating**: sfw
- **scene_id**: `scenes`
- **discovered_by**: game_review
- **probes**: SFW static — proves the image path + contact-sheet judging.
- **query style**: NEW

## Beat (verbatim from TOML `description`)
> A small, bare, run-down room in daylight with nobody in it — a stripped mattress, a window with no curtain, marks on the wall. Empty and a little grim. The place is the subject, so a person in frame would be wrong. Must show: an interior, no people, visible wear. Avoid: anyone in shot, styled or staged interiors, a hotel-brochure look.

## Demand

### setting_is_load_bearing: `true`
> The place IS the subject. Squalor is the content.
Setting axis SCORED at 25; HEAT 60; CRAFT 15. Spend query words on the setting.

### intended_heat
LIFE (SFW name for heat): lived-in and specific, not a stock render of "empty room".

### POV case
n/a

### must_show
- an interior
- NO people
- visible wear (stripped mattress, curtainless window, marks on the wall)

### avoid
- anyone in shot
- styled or staged interiors
- a hotel-brochure look
- illustrations / 3D renders

### strip checklist (derived — hold this against the 4-frame strip)
1. MUST: an interior
2. MUST: NO people
3. MUST: visible wear (stripped mattress, curtainless window, marks on the wall)
4. AVOID: anyone in shot
5. AVOID: styled or staged interiors
6. AVOID: a hotel-brochure look
7. AVOID: illustrations / 3D renders

## Queries — Google (Chrome), as declared in the TOML
- **q1**: `empty run down room bare mattress daylight interior`
- **q2**: `abandoned apartment room peeling wall no people`
- **q3 (sibling, if shelf < floor)**: write it in the SAME style as above — `NEW`.
  For the three OLD-style control slots a NEW-style sibling would contaminate the control.

## Mode
`fill` — stock **6** options, strip top **0** by rank.
Static `.jpg`: nothing to strip — judged from the contact sheet.

PHASE: scope_complete
NEXT_PHASE: plan
OPTIONS_STOCKED: 0
INSTALLED: no
