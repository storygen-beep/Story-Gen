# Scope: activities/ambient_frank_lunch.jpg

**file_path:** activities/ambient_frank_lunch.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 6244

## Original queries
- kitchen counter sandwich making older man
- man making sandwich kitchen counter sleeves rolled

## Narrative context
```
start_time = "12:00"
end_time = "13:00"

[[canvases.nodes]]
id = "base"
name = "Standing Lunch"
blocks = [
  { type = "paragraph", content = "@frank at the counter, sleeves rolled, assembling sandwiches with the same precision he uses on a table saw. He slides one toward her without asking. Turkey. Extra mustard. He remembered." },
  { type = "image", props = { file = "activities/ambient_frank_lunch.jpg", search_queries = ["kitchen counter sandwich making older man", "man making sandwich kitchen counter sleeves rolled"] } },
]
exit_block = { type = "choices", choices = [
  { text = "Eat together.", targetType = "trigger", time_progression_minutes = 30, effects = [{ targetType = "npc", npcId = "npc_frank", trait = "trust", op = "add", value = 1 }] },
```
