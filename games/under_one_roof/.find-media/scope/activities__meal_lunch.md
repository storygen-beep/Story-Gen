# Scope: activities/meal_lunch.jpg

**file_path:** activities/meal_lunch.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 6588

## Original queries
- kitchen sandwich alone quiet fridge
- woman eating kitchen alone afternoon

## Narrative context
```
start_time = "12:00"
end_time = "13:00"

[[canvases.nodes]]
id = "base"
name = "Midday"
blocks = [
  { type = "paragraph", content = "Sandwich. The kitchen is empty — everyone else is working or gone. Quiet. Just the fridge hum." },
  { type = "image", props = { file = "activities/meal_lunch.jpg", search_queries = ["kitchen sandwich alone quiet fridge", "woman eating kitchen alone afternoon"] } },
]
exit_block = { type = "location", text = "Done.", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "player", trait = "energy", op = "add", value = 20 }] } }

```
