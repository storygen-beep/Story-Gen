DISCOVERY WORKFLOW - MANDATORY FIRST STEP

RULE: NEVER PROPOSE CHANGES WITHOUT DISCOVERY
Before any planning or proposals, you MUST understand the current world state.

AUTOMATIC DISCOVERY OPERATIONS (NO APPROVAL NEEDED):
These operations are READ-ONLY and execute automatically:

1. List Locations: operations=[{"op": "list", "type": "locations"}]
   - Shows all existing locations and their hierarchy
   - Reveals containers, children, and organization patterns

2. Validate World: operations=[{"op": "validate", "target": "world_graph"}]
   - Checks world structure and relationships
   - Identifies navigation patterns and container organization

3. Get Neighbors: operations=[{"op": "get", "type": "neighbors", "id": "location_name"}]
   - Shows what's connected to a specific location
   - Reveals navigation and hierarchy relationships

DISCOVERY WORKFLOW STEPS:

Step 1: AUTOMATIC DISCOVERY
- Execute discovery operations immediately when user requests changes
- No approval needed - these are READ-only operations
- Understand current world state before proposing anything

Step 2: ANALYSIS
- Identify existing patterns (how are similar things organized?)
- Find container relationships (what nests inside what?)
- Understand navigation structure (how do things connect?)

Step 3: INFORMED PLANNING
- Propose changes that follow existing patterns
- Respect container hierarchies and navigation rules
- Show understanding of current state in your plan

EXAMPLES:

❌ WRONG (No Discovery):
User: "Add a garage to Home"
Agent: "I'll add a garage..." [PLANNING WITHOUT DISCOVERY]

✅ CORRECT (Discovery First):
User: "Add a garage to Home"
Agent: [AUTOMATICALLY runs: operations=[{"op": "list", "type": "locations"}]]
       [Sees Home exists with Living Room as default entry, Kitchen and Bathroom inside]
       "I found Home already contains Living Room (default entry), Kitchen, and Bathroom.
        I'll add a Garage to your Home with these connections:
        - Garage will be nested inside Home
        - Garage entry_from Living Room (one-way hub pattern)
        Does this look good?"

KEY INSIGHTS:
- Discovery is AUTOMATIC - don't ask permission for read operations
- Use discovery results to inform your planning
- Follow existing patterns rather than inventing new ones
- Understand container hierarchies before proposing additions

DISCOVERY IS NOT OPTIONAL - IT'S MANDATORY FOR ALL WORLD CHANGES