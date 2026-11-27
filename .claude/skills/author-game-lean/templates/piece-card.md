PIECE <id> · <person or system>, <step>: <name>

When / where: <day or condition, time window, place>
What the player sees:
  Screen 1: <the real text, as it will ship>
  Choices: "<choice>" / "<choice>"
  Screen 2: <...>
Variants: <n>. A, <name>: <what differs, when it shows>. B, <...>
Sheet:
  <canvas>.<node> | <clock> | <place> | <who is there, npc ids, or nobody; "<id> (part)" if only some of the time> | <garment ids she wears, or any> | <flags set before it; by path: …>
  (Written by hand, before the build, as what the story means. Clock forms: the opening "07:20–07:23" (in–out);
  a repeatable "<days> HH:MM–HH:MM", the window the screen shows in, or the scene's window and "+N" minutes into it;
  days as "weekdays", "weekends", "daily", "Mon–Sat", or names "Mon Wed Fri"; no days means every day; "any" for
  no window; "while <npc_id> is there". Who, wearing and flags are sets: order doesn't matter.)
Does:
  <canvas>.<node> | <what the screen does, from SKILL.md's Rule labels, comma-separated; never "always">
Changes: <flags set, traits moved, items, doors opened — by name>
Media: <n> spots. <spot>: <what it shows>, <tier>, <view>. Every screen the Does: marks `something sexual shows` has a spot, or a line `No spot: <canvas> — <why>` (craft/media.md rule 8, C2204)
Earlier releases: <what changes in shipped content, or "none">
Out of scope: <what this piece does not do>. Events only: never the body of a moment this piece builds. An adoption card (existing canvases, nothing new) always ends: LO has not read these scenes; this yes means 'keep as it is', not 'read and approved'.
Builds: <canvas, place and person ids, and `sidebar:<trait>` for a sidebar item, this piece adds or edits, comma-separated>
Card checks: <`check.py --card` verdict, pasted: GREEN, or each red line> · <`check.py --rules` count line, pasted> · <`check.py --beat` verdict, when a beat is marked `[explicit]`>
