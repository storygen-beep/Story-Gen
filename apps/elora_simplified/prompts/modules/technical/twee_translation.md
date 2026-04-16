HOW WORLD OPERATIONS BECOME TWEE GAMEPLAY:

Understanding the critical translation from abstract world operations to concrete player experience:

ENTRY-FROM → CLICKABLE NAVIGATION (one-way):
- `{"op": "set_entry_from", "data": {"location": "Kitchen", "from": "Living Room"}}`
- Becomes: `[[Go to Kitchen->Location_Kitchen]]` when viewed from Living Room (depending on generator’s rendering)
- Player sees: "Available destinations:" with bulleted clickable options
- Psychology: Each entry = one navigation choice (2-3 = comfortable, 5+ = overwhelming)

Reverse travel: implied via container default entry
- No mirrored `entry_from` needed back to hub; exiting container auto-routes to its default entry

DEFAULT ENTRY → SEAMLESS CONTAINER FLOW:
- `{"op": "set_default_entry", "data": {"container": "House", "entry": "Living Room"}}`
- Becomes: `[[Enter House->Location_Living_Room]]` (jumps directly to room)
- Player sees: "Enter House" → automatically goes to Living Room (not generic House page)
- Psychology: Maintains immersion with realistic entry flow

NESTING → SPATIAL CONTEXT:
- `{"op": "nest", "data": {"child": "Kitchen", "parent": "House"}}`
- Becomes: Spatial organization (Kitchen exists inside House concept)
- Player sees: Contextual understanding of "where am I in the world"
- Psychology: Provides spatial grounding and logical organization

CONTAINER STATUS → HIERARCHICAL OPTIONS:
- `is_container: true` + `default_entry_location`
- Becomes: "Enter [Container]" links that provide deeper exploration
- Player sees: Ability to go "into" spaces rather than just "between" spaces
- Psychology: Creates depth and exploration layers

CRITICAL TRANSLATION EXAMPLES:

Example 1 - Good Navigation Flow (one-way hub pattern):
Operations: create Kitchen → nest in House → set_entry_from Kitchen from Living Room
Twee Result: From Living Room, player can go to Kitchen. Reverse is implied via default entry when leaving the container.
Player Experience: Comfortable navigation without illegal mirrored links

Example 2 - Container Entry Flow:
Operations: create House (container) → create Living Room → nest Living Room in House → set_default_entry House→Living Room
Twee Result: "Enter House" link goes directly to Living Room passage
Player Experience: Seamless "enter building → appear in logical room" immersion

Example 3 - Poor Navigation (What NOT to do):
Operations: create Kitchen → nest in House (no connections)
Twee Result: Kitchen page with only "Back to Navigation" link
Player Experience: Trapped feeling, broken spatial logic

KEY INSIGHT: Every world operation becomes actual gameplay mechanics that players interact with. The abstract database relationships become the concrete navigation UI, clickable links, and spatial flow in the generated Twee game.
