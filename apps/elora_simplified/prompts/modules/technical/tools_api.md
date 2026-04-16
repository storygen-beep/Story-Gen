HOW TO USE execute_world_operations:

IMPORTANT: This tool has ONE parameter called "operations" which must be a list of operation dictionaries.

This single tool handles EVERYTHING about the world. Always pass operations as a named parameter:

BATCHING LOGIC:

Batch operations when:
- One operation depends on another's result
- Multiple changes form a logical unit
- You need to reference a just-created entity (use @ prefix)

Example batched operation:
operations=[
    {"op": "list", "type": "locations"},
    {"op": "create", "type": "location", "data": {"name": "NewPlace"}},
    {"op": "set_entry_from", "data": {"location": "ExistingPlace", "from": "@NewPlace"}}
]

The @ reference ONLY works within the same batch - this is why dependent operations must be together.

DISCOVERY IS ESSENTIAL:

Never assume - always discover the existing world structure first.
Use discovery to understand:
- What type each location is
- How locations relate to each other
- The established hierarchy patterns

This isn't just data gathering - it's learning the world's spatial logic.

OPERATION PATTERNS:

Discovery: {"op": "list", "type": "locations"} - Understand what exists
Creation: {"op": "create", "type": "location", "data": {...}} - Add new entity
Connection: DEPRECATED - Use entry/exit connections instead
Nesting: {"op": "nest", "data": {"child": "A", "parent": "B"}} - Establish hierarchy
Templates: {"op": "create_from_template", "template": "type", "params": {...}} - Use predefined patterns
