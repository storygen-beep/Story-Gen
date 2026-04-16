UNDERSTANDING YOUR WORLD'S SPATIAL HIERARCHY:

Think of the world as nested containers, like Russian dolls:
- Regions contain neighborhoods
- Neighborhoods contain buildings (houses, stores, parks)
- Buildings contain rooms
- Rooms contain furniture and items

Every entity has a natural level in this hierarchy. When adding something new,
consider: "What level does this belong to?" and "What should contain it?"

A house is a building-level entity that naturally belongs inside a neighborhood.
A park is also building-level, existing within a neighborhood.
A bedroom is room-level, existing within a house.

This mirrors the real world - use your understanding of how spaces naturally organize.

HIERARCHICAL REASONING FOR WORLD OPERATIONS:

Before adding anything, understand the hierarchy:
1. What type of thing am I adding? (building, room, furniture?)
2. What contains things of this type? (neighborhoods contain buildings)
3. How do existing similar things relate? (discover and follow patterns)

Key Insight: Most world operations involve placing things inside their natural containers.
- Adding a house? It goes inside a neighborhood (nest)
- Adding a bedroom? It goes inside a house (nest)
- Linking two houses? Use entry connections for movement

Discovery is crucial - see how the world is already organized and follow that pattern.

Core Principles:
- **Hierarchy First**: Understand where things naturally belong
- **Discovery Before Action**: Always understand current state before modifying
- **Pattern Following**: Learn from existing organization
- **Atomic Operations**: Related changes should be batched together

SPATIAL INTELLIGENCE WITH HIERARCHICAL NAVIGATION:

When designing world navigation, think about PLAYER EXPERIENCE:

1. **Identify the entity's level**: Is this a region, building, room, or item?
2. **Find its natural container**: What typically contains this type of thing?
3. **Design player movement flow**: How should players navigate this space?
4. **Consider player psychology**: What emotions will this navigation create?
5. **Choose the right operations**:
   - Different levels → nest (establish hierarchy and spatial context)
   - Same level movement → set_entry_from (create exploration choices)
   - Container entry → set_default_entry (maintain immersion with realistic entry points)
   - Container entry → set_default_entry (maintain immersion with realistic entry points)

Remember: The world has THREE aspects:
1. **Spatial hierarchy** (containers) - How spaces are organized
2. **Movement flow** (entry/exit) - How players navigate
3. **Player psychology** (emotions) - How navigation makes players FEEL

Buildings exist within neighborhoods (nesting for context),
Players navigate between rooms via one-way entry_from (movement for choice),
Navigation patterns create emotions (psychology for engagement) and reverse travel is implied via default entry.
