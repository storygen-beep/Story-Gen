# piece — card, show, yes

1. **Write** the card at `games/<slug>/cards/<id>.md` from `templates/piece-card.md`. Every slot is filled; "none" is an answer, an empty slot is not. What is not on the card is not built — an author who builds from a card fills its gaps from memory without noticing (C2058). `Builds:` lists every canvas id the piece adds or edits; `scripts/check.py` turns any canvas no approved card lists red, as "built but never approved".
2. **Check the card** before asking. Run every check that can judge a card; write the results in `Card checks:`. A card cannot leave out what a check needs (C2063). Numbers — word counts, explicit share, ceilings — belong to the checks at build, not to the card (C2069).
3. **Show** the file's own text, exactly, in a code block — no paraphrase. The hash covers the file, so LO sees what gets hashed. A long card goes in bites, one screen at a time, each the file's own text. End with one line of recommendation, then: "Yes, change, or drop?"
4. **Take the answer.**
   - **A plain yes:** `venv/bin/python .claude/skills/author-game-lean/scripts/approve.py games/<slug> <id> "<LO's exact words>"`, mark the piece approved in STATE.md, end with `Next step: build — <id>`.
   - **"Yes, but change X"**, "change …", "keep A, drop B": edit the card, then show only the changed lines, as before and after. LO has seen the rest. The old yes does not carry over; the new yes is recorded against the new file's hash.
   - **Drop:** remove the row from STATE.md; add a NOTES.md line in LO's words.
   - **Silence, "sounds good", an answer about something else:** not a yes. Ask again.
5. **Never build in the reply that shows the card.**

**Done when.** `approvals.json` holds this card's current hash, and STATE.md marks the piece approved.
