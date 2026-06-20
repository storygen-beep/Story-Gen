# Scope: activities/solo_grooming.jpg

**file_path:** activities/solo_grooming.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 5628

## Original queries
- woman bathroom mirror self care grooming
- woman bathroom getting ready mirror

## Narrative context
```
start_time = "06:00"
end_time = "07:30"

[[canvases.nodes]]
id = "base"
name = "Mirror Time"
blocks = [
  { type = "paragraph", content = "Shower. Steam fills the bathroom — the lock doesn't catch but she's learned to wedge a towel under the door." },
  { type = "image", props = { file = "activities/solo_grooming.jpg", search_queries = ["woman bathroom mirror self care grooming", "woman bathroom getting ready mirror"] } },
  { type = "paragraph", content = "Skincare. The stuff she brought from the dorm. Her face in the mirror looks different than it did eight weeks ago. Sharper. More aware of being looked at." }
]
exit_block = { type = "location", text = "Done.", config = { destinationType = "trigger", time_progression_minutes = 45, effects = [ { targetType = "player", trait = "beauty", op = "add", value = 2 } ] } }
```
