# Scope Brief — `lab_alley_t5`  (slot 4 of 10)

## Identity
- **file_path**: `scenes/lab_alley_t5.webm`   ← verbatim key for options store / review store / dedupe
- **type**: video | **category**: Other | **canvas_id**: canvas_lab
- **tier**: t5 | **content_rating**: nsfw
- **scene_id**: `scenes`
- **discovered_by**: game_review
- **probes**: Outdoor night where the dark IS the meaning. The one load-bearing setting on an NSFW slot.
- **query style**: NEW

## Beat (verbatim from TOML `description`)
> A couple fucking outdoors at night against a wall in a filthy back alley, both bodies visible, lit only by whatever streetlight reaches them. The squalor and the risk of being seen are the charge — a clean bright room would kill this beat entirely. Must show: outdoors, night, a wall or alley, both people visible. Avoid: any interior, daylight, studio lighting, POV that hides one of them.

## Demand

### setting_is_load_bearing: `true`
> Squalor + risk of being seen. A clean bright room kills the beat entirely. Bright clips were rejected twice on this band before.
Setting axis SCORED at 25; HEAT 60; CRAFT 15. Spend query words on the setting.

### intended_heat
Squalor and risk. The place is wrong for this and it is happening anyway.

### POV case
DEFECT. Both bodies must be visible — a POV that hides one of them destroys the beat.

### must_show
- outdoors
- night
- a wall or alley
- both people visible

### avoid
- any interior
- daylight
- studio lighting
- POV that hides one of them

### strip checklist (derived — hold this against the 4-frame strip)
1. MUST: outdoors
2. MUST: night
3. MUST: a wall or alley
4. MUST: both people visible
5. AVOID: any interior
6. AVOID: daylight
7. AVOID: studio lighting
8. AVOID: POV that hides one of them

## Queries — Google (Chrome), as declared in the TOML
- **q1**: `alley night outdoor sex against wall amateur`
- **q2**: `public street night couple fucking wall voyeur`
- **q3 (sibling, if shelf < floor)**: write it in the SAME style as above — `NEW`.
  For the three OLD-style control slots a NEW-style sibling would contaminate the control.

## Mode
`wide` — stock **12** options, strip top **6** by rank.


PHASE: scope_complete
NEXT_PHASE: plan
OPTIONS_STOCKED: 0
INSTALLED: no
