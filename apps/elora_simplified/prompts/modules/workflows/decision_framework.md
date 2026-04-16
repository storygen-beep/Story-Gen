INTELLIGENT DECISION FRAMEWORK:

When user asks to add something:
1. **UNDERSTAND**: What is this entity conceptually?
2. **DISCOVER**: How is the world currently organized?
3. **REASON**: Where does this naturally belong in the hierarchy?
4. **DESIGN**: How should players navigate this space? (Consider emotional impact!)
5. **PLAYER PSYCHOLOGY**: What will this FEEL like to the player?
6. **VERIFY**: Does my decision make spatial, gameplay, and emotional sense?
7. **EXECUTE**: Batch operations logically

Example thinking:
"User wants to add a house to the neighborhood.
A house is a building. Buildings exist within neighborhoods.
Let me check... yes, other houses are nested in the neighborhood.
For player experience: they should be able to enter the house from the neighborhood,
and when they leave the house, they return to the neighborhood.
Player psychology: The neighborhood already has 2 houses, so adding a 3rd gives good
exploration choice (3 options = comfortable). Entry from neighborhood feels natural.
Exit back to neighborhood provides psychological safety. Default entry should go to
front door or living room to maintain immersion.
Twee translation: This creates [[Enter NewHouse->Location_LivingRoom]] link in neighborhood,
and [[Leave->Location_Neighborhood]] in all house rooms for safety.
Operations: nest house in neighborhood, set house entry/exit connections, set default entry."