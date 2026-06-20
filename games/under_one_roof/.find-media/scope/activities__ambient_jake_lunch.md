# Scope: activities/ambient_jake_lunch.jpg

**file_path:** activities/ambient_jake_lunch.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 6484

## Original queries
- young man stove ramen cooking kitchen
- man cooking ramen kitchen stove reading

## Narrative context
```
start_time = "12:00"
end_time = "13:00"

[[canvases.nodes]]
id = "base"
name = "Boiling Water"
blocks = [
  { type = "paragraph", content = "@jake at the stove, reading the back of a ramen packet like it's literature. The water is already boiling over. He hasn't noticed." },
  { type = "image", props = { file = "activities/ambient_jake_lunch.jpg", search_queries = ["young man stove ramen cooking kitchen", "man cooking ramen kitchen stove reading"] } },
]
exit_block = { type = "choices", choices = [
  { text = "\"Want help?\"", targetType = "trigger", time_progression_minutes = 20, effects = [{ targetType = "npc", npcId = "npc_jake", trait = "trust", op = "add", value = 1 }, { targetType = "npc", npcId = "npc_jake", trait = "love", op = "add", value = 1 }] },
```
