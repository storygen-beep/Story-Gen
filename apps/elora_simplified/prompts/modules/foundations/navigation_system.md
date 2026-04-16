HIERARCHICAL NAVIGATION SYSTEM:

NEW ADVANCED NAVIGATION - Use these operations for better player experience:

Entry Connections: {"op": "set_entry_from", "data": {"location": "B", "from": "A"}} - Set that location B can be entered from location A
Clear Entry: {"op": "clear_entry_from", "data": {"location": "B"}} - Remove entry connection from location B
Default Entry: {"op": "set_default_entry", "data": {"container": "A", "entry": "B"}} - Where player goes when ENTERING container A

HOW THE NEW NAVIGATION WORKS:

1. **Entry_From** (one-way): Define inbound access for each location
   - Rooms set entry_from to a hub (e.g., Kitchen entry_from Living Room)
   - Hubs present multiple destinations to the player

2. **Reverse Travel**: implied via container default entry
   - No mirrored entry_from needed back to hub

3. **Default Entry for Containers**: Where you go when entering a container
   - Enter House → automatically go to Front Door or Living Room
   - Enter Neighborhood → automatically go to Main Street

NAVIGATION DESIGN PRINCIPLES:

- **Containers organize spaces**: Neighborhoods contain houses, houses contain rooms
- **Entry connections define movement options**: Where can I go from here?
- **Exit connections define departure**: How do I leave this area?
- **Hierarchical flow**: Enter container → default entry location → explore via entries → exit when done

NAVIGATION OPERATION SELECTION:

For SPATIAL ORGANIZATION:
- Different levels → nest (house into neighborhood - creates spatial context)
- Same level → set_entry_from connections (room to room - creates exploration choices)

For PLAYER NAVIGATION & PSYCHOLOGY:
- Movement options → set_entry_from (kitchen to living room, dining room - creates comfortable choices)
- Container entry → set_default_entry (enter house → front door - maintains immersion)
- Choice count consideration: 2-3 entries = good, 5+ = overwhelming, 0 = trapped feeling

CONTAINER WITH DEFAULT ENTRY RULES:
When a container has a default entry (like Home → Living Room):

✅ CORRECT: Connect rooms to each other INSIDE the container
   - Kitchen → Living Room (one-way, since Living Room is default entry)
   - {"op": "set_entry_from", "data": {"location": "Kitchen", "from": "Living Room"}}
   - NOTE: Living Room cannot have entry_from because it's the default entry

❌ WRONG: Connect INSIDE rooms directly to the container (bypassing default entry)
   - Kitchen entry_from Home (FAILS - inside locations cannot bypass default entry)

✅ CORRECT: OUTSIDE locations can connect to containers with default entries
   - Mall entry_from Home (SUCCEEDS - outside locations can connect to containers with default entry)

KEY INSIGHT: Default entries handle container access automatically - no manual connections needed

CRITICAL NAVIGATION RULES:
1. Default entry locations CANNOT have entry_from set (they are automatically entered)
2. INSIDE locations CANNOT bypass their container's default entry (must go through default entry)
   OUTSIDE locations CAN connect to containers with default entries (for world-to-world travel)
3. To connect to a default entry location, connect FROM it, not TO it
4. Example: Kitchen connects from Living Room (default entry), but Living Room cannot connect from anywhere
5. Example: Mall (outside) CAN connect to Home even if Home has Living Room as default entry
