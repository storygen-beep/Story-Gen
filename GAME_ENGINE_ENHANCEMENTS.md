# Game Engine Technical Enhancements

This document tracks planned technical enhancements to the game generation engine to support "Become Someone" style sandbox dating sim games.

**Status Legend**:
- ⬜ Not Started
- 🟡 In Progress
- ✅ Complete

---

## Enhancement List

### 1. ⬜ NPC & Player Portrait System
**Priority**: High | **Effort**: Medium

Display character portraits in the UI sidebar and during dialogue.

**Requirements**:
- Player portrait in sidebar (customizable or default)
- NPC portraits in sidebar "Girls Locations" section
- Portrait display during dialogue blocks
- Support for multiple expressions per character (happy, sad, angry, aroused, etc.)
- Fallback placeholder for missing portraits

**TOML Schema**:
```toml
[player]
name = "John"
portrait = "player_default.jpg"
portraits = { default = "player_default.jpg", confident = "player_confident.jpg" }

[[npcs]]
id = "elena"
name = "Elena"
portrait = "elena_default.jpg"
portraits = {
  default = "elena_default.jpg",
  happy = "elena_happy.jpg",
  sad = "elena_sad.jpg",
  aroused = "elena_aroused.jpg",
  angry = "elena_angry.jpg"
}
```

**UI Display**:
- Sidebar: Small circular portrait next to NPC name in location tracker
- Dialogue: Larger portrait (left for NPC, right for player) during conversations
- Stats Page: Portrait header for each character section

**Files to Modify**:
- `apps/game_generation/twee_comprehensive/generators/v1.py`
- `apps/projects/services/template_import.py`
- `apps/npcs/models.py`

---

### 2. ⬜ NPC Location Tracker (Real-time Sidebar)
**Priority**: High | **Effort**: Low

Show where each NPC currently is based on schedule and time.

**Requirements**:
- Sidebar section "Girls Locations" showing all tracked NPCs
- Real-time location based on current game time + NPC schedule
- Click NPC name to fast-travel to their location
- Show "(Private)" or "(Busy)" status when not interactable

**Implementation**:
```javascript
setup.getNpcCurrentLocation = function(npcId) {
  const schedule = $npcs[npcId].schedule;
  const hour = $game_state.time_state.hour;
  const day = $game_state.time_state.day_of_week;
  // Match schedule slot to current time
};
```

---

### 3. ⬜ Fast Travel Hub System
**Priority**: High | **Effort**: Low

Central navigation hub with quick access to major locations.

**Requirements**:
- Dedicated "Map" or "Fast Travel" button in sidebar
- Grid/list of major locations with icons
- Unlock conditions for certain locations
- Show NPC count at each location
- Time cost for travel (optional)

---

### 4. ⬜ Relationship State Machine
**Priority**: High | **Effort**: Medium

Explicit relationship progression states beyond numeric traits.

**Requirements**:
- States: stranger → acquaintance → friend → romantic → intimate
- Milestone tracking (first_meeting, first_date, first_kiss, first_intimate)
- State-based canvas unlocking
- UI display of current relationship state
- Automatic state transitions based on trait thresholds + milestones

**TOML Schema**:
```toml
[[npcs]]
id = "elena"
relationship_config = {
  acquaintance_threshold = 20,
  friend_threshold = 40,
  romantic_requires = ["first_date_complete"],
  intimate_requires = ["first_kiss", "affection >= 70", "trust >= 50"]
}
```

---

### 5. ⬜ Locked Choice Display with Unlock Hints
**Priority**: High | **Effort**: Low

Show locked choices with clear requirements instead of hiding them.

**Requirements**:
- Locked choices visible but greyed out
- Hover/tooltip shows unlock requirement
- Progress indicator (e.g., "Affection 35/50")
- Optional: "How to unlock" activity suggestions

**Display Example**:
```
[✓] Chat with her
[✓] Compliment her
[🔒] Kiss her (Need Affection 50+, currently 35)
[🔒] Invite to bedroom (Need Romantic relationship)
```

---

### 6. ⬜ Location Discovery System
**Priority**: Medium | **Effort**: Low

Progressive world unlock - not all locations available from start.

**Requirements**:
- Locations can be hidden until discovered
- Discovery conditions (time, flags, NPC interactions)
- "???" placeholder for undiscovered locations
- Discovery notifications ("You've discovered the Red Light District!")

---

### 7. ⬜ Privacy Awareness System
**Priority**: Medium | **Effort**: Medium

Activities aware of public/private context.

**Requirements**:
- Locations marked as private/public
- Intimate activities require private locations
- Public displays affect reputation/gossip (optional)
- Alternative "subtle" scenes for public contexts

---

### 8. ⬜ Activity Prerequisites & Chaining
**Priority**: Medium | **Effort**: Medium

Explicit canvas prerequisites for progression gating.

**Requirements**:
- Canvases can require other canvases completed first
- Canvases can require relationship states
- Clear prerequisite display in "What's Next" guide
- Prerequisite chains for intimacy progression

---

### 9. ⬜ Enhanced Stats Page
**Priority**: Medium | **Effort**: Low

Rich character stats display with progression info.

**Requirements**:
- Character portrait header
- Relationship state badge
- Trait bars with numeric values
- Milestone checklist (✓/○)
- "Next Steps" suggestions
- Unlock progress indicators

---

### 10. ⬜ Sub-Location Depth & Interior Navigation
**Priority**: Low | **Effort**: Medium

Multi-level location hierarchy for immersive world.

**Requirements**:
- Locations can have sub-locations (Bedroom → Bed, Desk, Closet)
- Interior navigation within locations
- Context-sensitive activities per sub-location
- "Look around" default action to see sub-locations

---

## Implementation Order

**Phase 1 - Core UX** (Items 1, 2, 3, 5):
- NPC & Player Portraits
- NPC Location Tracker
- Fast Travel Hub
- Locked Choice Display

**Phase 2 - Progression Systems** (Items 4, 8):
- Relationship State Machine
- Activity Prerequisites

**Phase 3 - World Depth** (Items 6, 7, 9, 10):
- Location Discovery
- Privacy Awareness
- Enhanced Stats Page
- Sub-Location Depth

---

## Notes

- All enhancements should be backwards-compatible with existing TOML files
- New fields should have sensible defaults
- Dev mode should allow bypassing locks for testing
- Each enhancement should include unit tests

---

## Related Files

**Core Generator**:
- `apps/game_generation/twee_comprehensive/generators/v1.py`

**Template Import**:
- `apps/projects/services/template_import.py`

**Models**:
- `apps/npcs/models.py`
- `apps/world/models.py`
- `apps/stories/models.py`

**Example TOML**:
- `apps/game_generation/game_example.toml`
