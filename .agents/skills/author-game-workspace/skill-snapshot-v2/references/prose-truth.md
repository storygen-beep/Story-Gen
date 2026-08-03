# prose-truth — the prose quotes the fields; when a field moves, the prose lies

**Read this before you change a `costs`, an `amount`, a `due_day`, an `entry_from`/`parent`, a schedule, or a
display `label` on content that already ships prose.** It is the maintenance layer under the legibility mandate
(`step-2-toplevel.md` §5): that mandate tells you to write the place / window / requirement into the prose
**verbatim**, and it is right to — but every one of those lines is a **copy of a field**, and a copy is a debt.
Everything here **passes the build**: flag chains validate, no warning fires, a fresh player never crashes. The
damage is that the game **tells the player something that isn't true**.

Sibling file: `save-safety.md` guards the player's *save*. This one guards the game's *truth*. (Note
`save-safety.md` §5 lists "fix prose" and "rename any display `name`/`title`" as ship-freely — correct, for
saves. Those same edits are exactly what desynchronises a `goals[].label` that named the old trait.)

## Why prose goes stale (the model)
The engine renders a fact from the field **only in narrow frames**, and hand-written prose everywhere else:
- `renderQuestsGoalBlock` shows the derived `📍 location` + `🕒 window` **only** in Frame 2, gated
  `goalState.allMet && card.ready_canvas` (`v2.py:14479`) — i.e. once the capstone is *already launchable*.
  Through the whole climb it takes Frame 3 (`!allMet`, `:14494`) and renders `label — current / value` bullets
  and nothing else.
- `setup.getCostBlockedMessage` (`v2.py:4527`) prints a live cost **only on a choice you can't afford** — it's
  emitted into `<span class="locked-choice">` (`:12233`). Affordable → it says nothing.
- `setup._formatCanvasSchedule` (`v2.py:6842`) can only emit machine register — `"Mon–Fri 18:00–23:00"`,
  `"every day"`. It cannot write *"evenings 6 pm–close"*.

**So the authored line is usually the only thing there, and nothing re-derives it.** Your `tip` is what the
player reads for the entire arc. That is why the mandate exists, and why the copy has to stay true by hand.

---

## §1 — An authored line that states a fact a field encodes is a copy of that field
Not a metaphor — a literal duplicate with no link back. `costs = [{ trait = "coin", value = 10 }]` and Kess
saying *"Ten a session"* are two independent strings that happen to agree today.

**So:** re-price the `costs` and the build stays green while the NPC quotes last week's price. Re-parent a
location and the `tip` sends the player to a room that isn't there any more.

**The rule:** keep writing the copy — it's mandated and load-bearing (the model above). Just know that writing it
opens an obligation: **the field and its prose are now one edit, not two.**

---

## §2 — The field is truth; the copy cannot self-correct
This skill already runs exactly this protocol one level down. Engine citations go stale when `v2.py` regenerates,
so `engine-reference.md` says: *"Number = hint, symbol = truth"* — re-`grep -n` the symbol. Player-facing prose is
the same shape: the TOML field is the symbol, the prose is the citation.

**But the analogy has a limit you must not import.** That protocol *tolerates* stale line numbers because the
reader is **you**, and you can re-grep. The reader of prose is the **player**. They cannot grep, cannot diff, and
have no way to know the game is wrong — they just follow the instruction and find nothing. Prose truth is
therefore stricter than citation accuracy, not looser.

**Worked example — the block this skill ships as canonical.** `rent.md` calls
`games/late_shifts/toml_phases/0_systems_spec.toml` the *"verbatim shipped block to copy."* It sets `amount = 125`
and authors `greeting = "Rent. Hundred and twenty-five. …"`. The engine's *default* greeting interpolates the live
value, but **an authored override is a literal string** — `<<print _rt.greeting || "Rent. $" + _rent + …>>`
(`v2.py:15367`) — while two lines below it the engine prints the live number unconditionally
(`Rent is $<<print _rent>>`) and again on the `Pay $N rent` button. Re-price to 150 and Vince says *"Hundred and
twenty-five"* directly above *"Rent is $150."* **The NPC contradicts the UI in a single screenshot.**

Note also that `125` never appears as a digit in that prose — it's spelled out, in voice, as it should be. That's
why you cannot find these by grepping the prose for the value (§4).

**The rule:** when a field and a line disagree, the **field** is what the game does; the prose is just what it
claims. Fix the prose to match — never the reverse, unless you meant to re-price.

---

## §3 — MOVE · RE-PRICE · RE-SCHEDULE · RENAME-a-label are amendments too
"Done WHOLE" (`SKILL.md` → stable-and-extensible; `beat-authoring.md` step 3) is **ADD-only** today: it covers a
*new* location / NPC / flag. But the four edits below change something that already has prose pointing at it, and
each one's *whole*-ness includes that prose:

| the change | what it silently invalidates |
|---|---|
| **MOVE** — `entry_from` / `parent` re-parented | every `tip` / `text` / `label` / dialogue naming the old parent or route |
| **RE-PRICE** — `costs`, rent `amount` | any line stating the price, spelled out or in digits |
| **RE-SCHEDULE** — `start_time` / `end_time` / `weekdays`, rent `due_day` | *"Nine sharp"*, *"evenings 6 pm–close"*, *"Same Friday next week"* |
| **RENAME a display label** — a trait/NPC `name`, `[[traits.labels]]` | `goals[].label` that named the trait; any prose using the old name |

**The rule:** one of these four is not a field edit, it's an amendment — do it whole, prose included, in the same
turn. Then run §4 before you call it done.

---

## §4 — Pre-change checklist
**Scope by the diff, not by the prose.** `games/` is git-tracked, so the diff knows which coupled fields moved
**and knows the OLD value** — which is the search key, and is otherwise unrecoverable once you've saved the file.

```bash
# What coupled fields did I just move? (drop the range to scan uncommitted work)
git diff -U0 [<since>..<until>] -- games/<slug>/toml_phases/ ':!*7_final_game.toml' \
| grep -E '^(\+\+\+|[-+][^-+#])' \
| grep -Ev '^[-+]\s*(#|description\s*=)' \
| grep -E '^\+\+\+|costs|amount|due_day|grace_periods|entry_from|parent|start_time|end_time|weekdays|value|label' \
| sed -e 's|^+++ b/games/[^/]*/toml_phases/|\n── |' -e 's/^-/  OLD  /' -e 's/^+/  NEW  /'

# Then grep the prose for each OLD value — that string is what went stale:
#   OLD entry_from = "the_waterfront"  ->  grep -rni 'waterfront' games/<slug>/toml_phases/
#   OLD costs value = 20               ->  grep -rniE '20|twenty' games/<slug>/toml_phases/
```
A beat moves 1–5 coupled fields, so this is a 1–5 line report, each line actionable. **It's a scanner, not a
verdict** — it tells you which facts moved, not whether the prose is wrong; you still read the lines. It skips the
generated `7_final_game.toml` (double hits), `#` comments, and canvas `description` (author-facing — keep those
honest too, they're how the next author learns the design).

**The usual suspects** — not an index (a hand-copied index of facts living elsewhere would *be* this bug class,
applied to the doctrine). The test is generative: **any authored string that states a fact a field encodes.** The
repeat offenders: the rent `[settings.rent.text]` block · quest-card `text` / `tip` · `goals[].label` ·
`blocked_message` / `locked_text` · NPC dialogue quoting a price, a place, or a schedule (`npc-intro.md`'s hook
line — *"Depot. Nine sharp."* — is a schedule citation by design).

**Use the derived render as an oracle.** Where the engine *does* derive the fact (Frame 2's `📍`/`🕒`), it reads
straight from the canvas. If your `tip` disagrees with the Ready frame, your `tip` is the stale one. This checks
the copy — it never replaces it (Frame 2 only fires at `allMet`; drop the tip and the whole climb goes bare).

---

**Cross-references (in-skill):** `save-safety.md` (the sibling — same "green build, quiet break" shape) ·
`beat-authoring.md` (step 3 amendments; the legibility self-audit row) · `step-2-toplevel.md` §5 (the legibility
mandate this maintains) · `quests.md` §2–§3 (the card fields + render frames) · `rent.md` §4 (the authored-override
literal) · `engine-reference.md` (symbol-over-line-number, the protocol this generalises).
