# Elora Dynamic Commands

This directory contains dynamic slash commands for the Elora CLI. Commands are automatically loaded from markdown files and made available in the interactive session.

## Command Format

Each command is a markdown file with optional frontmatter:

```markdown
---
description: Brief description of what the command does
---

[Prompt content that gets sent to the LLM]
```

### Frontmatter (Optional)

- `description`: A brief explanation shown in the help system

### File Naming

- File name becomes the command name (e.g., `storyteller.md` → `/storyteller`)
- Command names are case-insensitive
- Use lowercase filenames with hyphens for multi-word commands

## How Commands Work

1. User types `/commandname` in the CLI
2. System loads the corresponding `.md` file
3. Frontmatter is parsed for metadata
4. Content is sent to the LLM as a behavior transformation prompt
5. LLM acknowledges the new mode and adopts the specified behavior

## Creating New Commands

1. Create a new `.md` file in this directory
2. Add optional frontmatter with description
3. Write the transformation prompt content
4. The command becomes immediately available in the CLI

## Examples

### Simple Command (no frontmatter)
```markdown
You are now in debug mode. Provide detailed technical analysis for all requests.
```

### Command with Description
```markdown
---
description: Switch to world-building focused mode
---

You are now a world-building specialist. Focus on consistency, lore, and immersive details when creating content.
```

## Built-in vs Dynamic Commands

**Built-in Commands** (handled in Python code):
- `/help` - Show help message
- `/quit`, `/exit` - Exit the CLI
- `/caps on/off` - Toggle uppercase mode

**Dynamic Commands** (loaded from this directory):
- `/storyteller` - Collaborative storytelling mode
- Any other `.md` files you create

## Best Practices

1. **Clear Identity**: Start with "You are now..." to establish the new persona
2. **Specific Behavior**: Define how the LLM should approach different types of requests
3. **Integration**: Explain how to use existing tools within the new mode
4. **Acknowledgment**: Include what response the LLM should give to confirm activation
5. **Concise**: Keep commands focused on a single transformation/mode

## Files to Ignore

- `README.md` - This documentation file
- Files starting with `.` (hidden files)
- Files without `.md` extension

## Error Handling

The system gracefully handles:
- Missing or malformed YAML frontmatter
- File permission issues
- Invalid markdown syntax

Errors are logged but don't crash the CLI.