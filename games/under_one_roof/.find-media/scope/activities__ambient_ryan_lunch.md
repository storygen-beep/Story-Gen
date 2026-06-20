# Scope: activities/ambient_ryan_lunch.jpg

**file_path:** activities/ambient_ryan_lunch.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 6381

## Original queries
- man open fridge kitchen standing
- kitchen fridge open man choosing food

## Narrative context
```
start_time = "12:00"
end_time = "13:00"

[[canvases.nodes]]
id = "base"
name = "Fridge Door Open"
blocks = [
  { type = "paragraph", content = "@ryan standing with the fridge open, staring into it like it owes him money. He takes up most of the kitchen just by existing. Pulls out three containers, sniffs each one, puts two back." },
  { type = "image", props = { file = "activities/ambient_ryan_lunch.jpg", search_queries = ["man open fridge kitchen standing", "kitchen fridge open man choosing food"] } },
]
exit_block = { type = "choices", choices = [
  { text = "Eat together.", targetType = "trigger", time_progression_minutes = 20, effects = [{ targetType = "npc", npcId = "npc_ryan", trait = "trust", op = "add", value = 1 }] },
```
