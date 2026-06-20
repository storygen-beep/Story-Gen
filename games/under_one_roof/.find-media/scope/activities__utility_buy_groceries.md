# Scope: activities/utility_buy_groceries.jpg

**file_path:** activities/utility_buy_groceries.jpg
**type:** image
**content_rating:** SFW
**toml_line:** 7758

## Original queries
- general store grocery aisle fluorescent
- small store grocery aisle shopping

## Narrative context
```
  { type = "flag", subject = "player", flag_key = "town_access", operator = "is_true" }
] }

[[canvases.nodes]]
id = "base"
name = "The General Store"
blocks = [
  { type = "paragraph", content = "General store. Fluorescent lights, linoleum floors. The kind of place that sells everything and specializes in nothing." },
  { type = "image", props = { file = "activities/utility_buy_groceries.jpg", search_queries = ["general store grocery aisle fluorescent", "small store grocery aisle shopping"] } },
  { type = "paragraph", content = "She grabs a basket. Eggs, bread, pasta, chicken, vegetables. The basics." }
]
exit_block = { type = "choices", choices = [ { text = "Buy groceries ($15)", targetType = "trigger", time_progression_minutes = 30, effects = [ { targetType = "player", trait = "money", op = "add", value = -15, clamp = false } ], itemEffects = [{ item_id = "groceries", action = "add", quantity = 5 }], conditions = { version = "1.0", items = [ { type = "trait", subject = "player", trait_key = "money", operator = "gte", value = 15 } ] } }, { text = "Just browsing.", targetType = "trigger", time_progression_minutes = 5 } ] }
```
