# /edit_game - Game Editing Session

## Purpose

Set up a Claude Code session for editing an interactive game. Loads all context so you can make changes effortlessly.

## Usage

```
/edit_game [game_folder]
```

**Example:**
```
/edit_game step_sister_wedding
```

---

## When This Command Runs

Read and understand these files:

### Generation Prompts (How content was created)
1. `game_book_prompt_v3_story_first.txt` - Story generation rules
2. `toml_generation_prompt.txt` - TOML structure rules

### Game Content (What we're editing)
3. `[game_folder]/*.toml` - The game definition file
4. `[game_folder]/*.md` or `[game_folder]/book.*` - The story book (if exists)

---

## Context to Understand

**Two-stage generation:**
1. **Book Prompt** → generates **Book** (narrative, story beats, character dynamics)
2. **TOML Prompt** → generates **TOML** (structured game from Book)

**5-tier affection system:**
- T1: Friendly, casual
- T2: Flirty, tension building
- T3: Intimate, crossing boundaries
- T4: Passionate, explicit
- T5: Intense, most explicit

---

## Ready for Edits

After reading all files, you're ready. Handle requests like:
- "Change the dialog in scene X"
- "Make activity Y more flirty at T3"
- "Add a new choice in canvas Z"
- "Adjust pacing in the morning routine"

Keep changes consistent with established voice and TOML structure.
