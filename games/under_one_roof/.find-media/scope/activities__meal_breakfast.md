# Scope: activities/meal_breakfast.jpg

**file_path:** activities/meal_breakfast.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 6559

## Original queries
- family breakfast kitchen table morning coffee

## Narrative context
```
name = "Morning Table"
blocks = [
  { type = "group", blocks = [
    { type = "paragraph", content = "@jake doesn't look up. Sketchbook propped against the salt shaker. Pencil moving. Earbuds in. She might as well not be in the room." }
  ], conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "drawing_started", operator = "is_false" }
  ] } },
  { type = "paragraph", content = "Kitchen. Coffee maker still hissing. @frank at the head of the table, paper open. @ryan inhaling eggs." },
  { type = "image", props = { file = "activities/meal_breakfast.jpg", search_queries = ["family breakfast kitchen table morning coffee"] } }
]
exit_block = { type = "choices", choices = [ { text = "Eat quietly.", targetType = "trigger", time_progression_minutes = 45, effects = [{ targetType = "player", trait = "energy", op = "add", value = 15 }] }, { text = "Talk to @jake about his drawing.", targetType = "trigger", time_progression_minutes = 45, effects = [ { targetType = "player", trait = "energy", op = "add", value = 15 }, { targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 1 } ], conditions = { version = "1.0", items = [ { type = "flag", subject = "player", flag_key = "drawing_started", operator = "is_true" } ] } }, { text = "Ask @ryan about his plans today.", targetType = "trigger", time_progression_minutes = 45, effects = [ { targetType = "player", trait = "energy", op = "add", value = 15 }, { targetType = "npc", npcId = "npc_ryan", trait = "love", op = "add", value = 1 } ] }, { text = "Offer to pour @frank's coffee.", targetType = "trigger", time_progression_minutes = 45, effects = [ { targetType = "player", trait = "energy", op = "add", value = 15 }, { targetType = "npc", npcId = "npc_frank", trait = "trust", op = "add", value = 1 } ] } ] }

```
