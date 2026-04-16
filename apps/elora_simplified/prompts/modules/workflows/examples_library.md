CONCRETE PLAYER EXPERIENCE EXAMPLES:

**Example 1: Adding Kitchen to House**
Player Request: "Add kitchen to the house"
LLM Reasoning:
- Kitchen = room-level entity → nest in House
- Player psychology: Kitchen should connect to 2-3 other rooms (comfortable)
- Twee translation: Will create [[Go to Kitchen->Location_Kitchen]] links
- Exit safety: Kitchen needs [[Leave Kitchen->Location_X]] escape
Operations: create Kitchen → nest in House → set_entry_from Kitchen from Living Room → set_entry_from Kitchen from Dining Room (if appropriate)
Player Sees in Game: From Living Room: "Go to Kitchen" link. Reverse to Living Room is implied via the container’s default entry.
Emotional Result: Comfortable navigation with clear connections and safety

**Example 2: Adding Mysterious Forest**
Player Request: "Create a mysterious forest for exploration"
LLM Reasoning:
- Forest = adventure space → needs multiple exploration paths (4-6 entries)
- Player psychology: Mystery requires choices but needs safety escape
- Twee translation: Multiple [[Path to X->Location_X]] options, [[Return to Safety->Location_Camp]]
Operations: create Mysterious Forest → set_entry_from from 4 different hubs/approaches → rely on safe hub default-entry for return
Player Sees in Game: "North Path", "Hidden Trail", "Old Road", "Shadowy Path" options, plus "Return to Camp" safety
Emotional Result: Exciting exploration with psychological security

**Example 3: Adding Cozy Bedroom**
Player Request: "Add a cozy bedroom for intimate conversations"
LLM Reasoning:
- Bedroom = intimate space → 1-2 connections only (focused experience)
- Player psychology: Privacy needs limited access but clear exit
- Twee translation: Minimal [[Go to X->Location_X]] options, clear [[Leave Bedroom->Location_Y]]
Operations: create Bedroom → nest in House → set_entry_from Bedroom from Hallway (one-way)
Player Sees in Game: "Go to Bedroom" from Hallway; reverse to Hallway is implied via container/hub default entry
Emotional Result: Private, focused space perfect for personal story moments
