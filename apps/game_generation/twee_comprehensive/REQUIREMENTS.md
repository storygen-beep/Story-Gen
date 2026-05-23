# Comprehensive Game Generation Requirements

> **🧊 v1 frozen 2026-05-14 — v2 is now the default generator.**
>
> The generator was forked from `generators/v1.py` to `generators/v2.py` on 2026-05-14 as a wholesale copy. All new engine work (NPC location schedules, `requires_npc` presence-detection on Lane 2/3 triggers, single-canvas hubs with conditional button injection per RTS doctrine) lands in v2. v1 exists only as a safe-mode rollback path during the v2 transition — invoke with `--gen-version v1` on `package_from_toml` / `package_game`. Once v2 is stable for ≥2 weeks, v1 (and its dormant `*_backup.py` siblings) will be deleted.
>
> The byte-equality regression test `apps/game_generation/tests.py::TestV1V2ByteEquality` proves v1 and v2 produce identical output at fork time; it will be scoped (or replaced with version-specific equivalence tests) when v2 deliberately diverges.

## Overview
This document defines the requirements and expectations for the comprehensive game generation system. This serves as our reference for what we're building and helps identify unnecessary complexity to remove.

## Core Game Flow Requirements

### 1. Game Entry Point
**What happens when player starts the game:**
- Display project name as game title
- Show project description
- Present "Start Game" link/button
- No complex intro sequences or character creation

### 2. Starting Canvas Integration
**How the game begins:**
- Project must have a designated "starting canvas"
- Starting canvas is displayed immediately after game entry
- Starting canvas should have a defined trigger location
- This trigger location becomes the player's initial location in the world

### 3. Canvas-to-Navigation Transition
**How gameplay progresses:**
- When starting canvas completes/ends, transition to Navigation system
- Player appears in the location specified by the canvas trigger
- Navigation system takes over from this point
- Example: If starting canvas trigger was "Jake's Room", player starts navigation from Jake's Room

## What We DON'T Need (Complexity to Remove)

### Character System Complexity
- Complex character creation or customization
- Multiple character types or classes
- Character progression systems
- Relationship tracking systems

### Advanced Narrative Features
- Multiple dialogue trees
- Complex branching storylines
- Character relationship mechanics
- Advanced conversation systems

### Complex World Systems
- Time management systems
- Resource management
- Inventory systems (unless absolutely basic)
- Complex NPC interaction systems
- Activity scheduling systems

### Advanced Game Mechanics
- Combat systems
- Skill systems
- Achievement systems
- Save/load systems (beyond basic browser storage)

## Simplified Architecture Requirements

### Core Components Needed
1. **Game Entry** - Simple title/description/start flow
2. **Starting Canvas Display** - Show the designated starting canvas
3. **Location Navigation** - Basic location-to-location movement
4. **Canvas Integration** - Seamless transition from canvas to navigation

### Data Dependencies
- Project metadata (name, description)
- Starting canvas identification and content
- Canvas trigger location mapping
- Basic location/navigation structure

## Success Criteria
A successful comprehensive game generation should:
1. ✅ Display project info and start the game
2. ✅ Show the starting canvas correctly
3. ✅ Transition smoothly to navigation at the correct location
4. ✅ Allow basic location-based exploration
5. ✅ Generate valid SugarCube-compatible code
6. ✅ Compile to working HTML without JavaScript errors

## Technical Constraints
- Must be SugarCube 2.36.1 compatible
- Must compile cleanly with Tweego
- Should generate minimal, clean code
- Must handle missing data gracefully (no crashes)
- Should work with existing canvas/location data structures

---

This document should guide all development decisions for the comprehensive game generation system. Any features not listed here should be considered out of scope for the current iteration.
