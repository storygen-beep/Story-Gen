# Scope: activities/solo_journal.jpg

**file_path:** activities/solo_journal.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 5659

## Original queries
- woman writing notebook bed lamp night
- woman journal writing bedroom evening

## Narrative context
```
start_time = "22:00"
end_time = "23:30"

[[canvases.nodes]]
id = "base"
name = "Writing"
blocks = [
  { type = "paragraph", content = "The notebook Mom gave her before Dubai. She writes. Not about the house — about herself. Who she was. Who she's becoming." },
  { type = "image", props = { file = "activities/solo_journal.jpg", search_queries = ["woman writing notebook bed lamp night", "woman journal writing bedroom evening"] } },
  { type = "paragraph", content = "The words come easier now than they did on day one." }
]
exit_block = { type = "location", text = "Close the notebook.", config = { destinationType = "trigger", time_progression_minutes = 30, effects = [ { targetType = "player", trait = "intelligence", op = "add", value = 1 }, { targetType = "player", trait = "confidence", op = "add", value = 1 } ] } }
```
