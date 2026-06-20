# Scope: activities/ambient_frank_workshop_pm.jpg

**file_path:** activities/ambient_frank_workshop_pm.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 6311

## Original queries
- workshop sanding wood sawdust man afternoon
- man workshop woodworking sawdust afternoon light

## Narrative context
```
start_time = "13:00"
end_time = "17:00"

[[canvases.nodes]]
id = "base"
name = "Sawdust"
blocks = [
  { type = "paragraph", content = "@frank sanding a cabinet door. Sawdust in the air, catching the light from the high windows. Sleeves rolled past the elbow. Radio playing something old and country. He works like nobody's watching — and he's better at it that way." },
  { type = "image", props = { file = "activities/ambient_frank_workshop_pm.jpg", search_queries = ["workshop sanding wood sawdust man afternoon", "man workshop woodworking sawdust afternoon light"] } },
]
exit_block = { type = "choices", choices = [
  { text = "Watch him work.", targetType = "trigger", time_progression_minutes = 20, effects = [{ targetType = "npc", npcId = "npc_frank", trait = "trust", op = "add", value = 1 }] },
```
