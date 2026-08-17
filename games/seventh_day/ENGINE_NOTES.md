# ENGINE_NOTES — findings from building `seventh_day`

Six defects found while building and auditing The Seventh Day (2026-08-16, extended 08-17). **None of them
is this game's authoring.** Two are engine bugs, two are in the skill, and the two engine bugs are
each compounded by the skill failing to document the behaviour.

The fourth was found *while writing this file*, by checking the citations I had just copied out of
`engine.md` — two of two pointed at the wrong line. That is the header warning below doing its job
on its own author.

Nothing here has been fixed. All four touch files shared by every game in the repo
(`generators/v2.py`, `scripts/gates.py`, `references/engine.md`), so they wait on LO.

> ⚠️ **How to read this file.** `author-game-v2/SKILL.md` names a game's own `ENGINE_NOTES.md` as a
> place where a **claim** gets mistaken for a **fact** — measured once at six claims checked, five
> held, one was a tooling note misfiled as engine behaviour. So every entry below carries its own
> `file:line` **and** the live-verification result that produced it. Re-run the probe before
> promoting any of this into `references/engine.md`; do not promote it on the strength of this file.

---

## 1 · A choice `costs` deduction is HARD-CLAMPED to 0–100 and the author cannot turn it off

**Layer: ENGINE** — plus a documentation gap in the skill.

```js
// generators/v2.py:4655-4661
setup.deductCostArray = function(costs) {
    if (!costs || costs.length === 0) return;
    setup.pendingEffects = [];
    for (var k = 0; k < costs.length; k++) {
        setup.applyAndNotifyTrait('player', null, costs[k].trait, 'add', -Number(costs[k].value), true, null);
    }                                                                                          // ^^^^ clampFlag
    setup.showEffectNotification();
};
```

The sixth positional argument is `clampFlag`, hardcoded `true`. `applyAndNotifyTrait` then runs
`window._traitClamp(next, 0, 100)` (`generators/v2.py:5761`). A `costs` entry is parsed as
`{trait, value}` only (`template_import.py:2133-2136`) — **there is no `clamp` field to set**, so
this cannot be opted out of in TOML.

**Verified live** (headless Chromium against the built `index.html`, calling
`setup.deductCostArray([{trait:'money', value:4}])`):

```
money   10  ->    6     correct
money   60  ->   56     correct
money  100  ->   96     correct
money  150  ->  100     expected 146   — LOSES 46
money  240  ->  100     expected 236   — LOSES 136
```

**Why it bites every v2 game.** `engine.md` §21 requires money *grants* to carry `clamp = false`,
precisely so a currency can exceed 100. The moment it does, the next priced purchase truncates the
balance to 100. Valid TOML, green build, green gates, no warning, no error — the player is silently
robbed.

`[settings.rent]` is **unaffected**: it subtracts directly (`generators/v2.py:15931`), verified live
at 300 → 55 on a 245 demand in an earlier game and 60 → 40 on this game's 20 tithe.

**Skill gap:** `engine.md` §21 is an entire section about this clamp and covers *effects* only.
The string `deductCostArray` appears nowhere in it.

**Impact on this game:** low but real. The economy runs ~£5/week surplus against a £20 weekly
tithe, so money sits far below 100 in normal play. A hoarding player would lose the excess.
Not worked around — worth fixing at the engine rather than designing around.

**Suggested fix:** let a `costs` entry carry `clamp`, defaulting to `true` for backward
compatibility, and pass it through in `deductCostArray`.

---

## 2 · The recurring-demand screen hardcodes the word "rent"

**Layer: ENGINE** — plus a documentation gap in the skill.

```
generators/v2.py:15916   <h2 class="rent-title"><<print _rt.title || "Monday Morning">> — Rent Day</h2>
generators/v2.py:15929   <<set _payText to "Pay " + _cur + _rent + " rent">>
```

`[settings.rent.text]` exposes **thirteen** authorable strings (title, scene, greeting, paid_scene,
paid_response, paid_closing, cant_pay, warning_scene, warning_response, warning_closing, and the
three soft-eviction beats). The heading's `— Rent Day` suffix and the pay button are not among them.

**Verified live:** this game's authored `title = "The Reading"` renders as
**`The Reading — Rent Day`**, and the button renders **`Pay £20 rent`**.

**Why it matters.** `the-voice.md` R1: a label is UI and must say what clicking does. This game's
obligation is a **tithe** — the father holds out a tin at a religious reading and every member of
the household turns in what they are holding. There is no rent, no landlord and no tenancy anywhere
in the fiction, and the player meets that screen once a week, every week, forever.

**Also affects the other v2 games**, whose obligations are likewise not rent: `steam` (a $135 weekly
draw on an inherited note) and `forty_miles` (a £245 Friday settle-up with the site owner).

**Skill gap:** `engine.md` §26 documents `[settings.rent]` thoroughly, lists the authorable strings,
and does not say which two are fixed.

**Suggested fix:** add `title_suffix` and `pay_label` to `[settings.rent.text]`, defaulting to the
current strings.

---

## 3 · Gate 10 fails a game for capping an income loop, which the economy doctrine REQUIRES

**Layer: SKILL** — this one is not the engine at all. `gates.py` lives inside the skill.

The contradiction, in three steps:

1. `the-economy.md` R5: *"A standing surface … that grants currency with neither a per-day cap nor a
   `costs` block is a money printer, and every other rule here is void beside it."*
2. The only author-side way to cap a **triggerless** rung is an `lt` condition on a counter trait —
   `max_triggers_per_day` is read per *trigger* (`v2.py:11017`) and a triggerless rung has none.
3. Gate 10's direction test then walks **every** player trait and fails the game because that
   counter "closes more than it opens":

```python
# .claude/skills/author-game-v2/scripts/gates.py:1154-1167
def _walk_player_traits(o):
    if o.get("type") == "trait" and o.get("trait_key") and o.get("subject") == "player":
        op = o.get("operator")
        if op in ("gte", "gt"):   p_expand[o["trait_key"]] += 1
        elif op in ("lt", "lte"): p_contract[o["trait_key"]] += 1
```

**Observed on this game.** `eggs_today` and `mending_today` are daily caps, declared
`hidden = true` in `[[traits.labels]]`, never rendered anywhere the player can see. Gate 10 reports
both as "a player meter that closes more than it opens" and fails, while the three declared ascent
tiers are all correctly `4+/0-`, `4+/0-`, `2+/0-`.

**Why the gate is written that way, and why that reasoning still holds.** Its own comment explains
it deliberately does *not* iterate the board's declaration, because "every gate that ITERATES a
declaration can be weakened by declaring less". That is right and should not change.

**Suggested fix:** exclude traits declared `hidden = true` in `[[traits.labels]]` from the descent
test. This keeps the anti-narrowing property: marking a trait hidden also removes it from the
sidebar, so it genuinely is not a meter the player can be lied to by — which is the only thing this
gate exists to catch.

**This is the third measured instance of its class.** `SKILL.md`: *"When a gate you just wrote fails
a game, check the skill before blaming the game… A check that fails a game for obeying the doctrine
is a bug in the check."* The two prior instances are recorded there — a locked-door gate that fired
on seven of eight correct games, and gate 24 failing a game whose obligation *was* charged.

---

## 4 · `engine.md`'s own `file:line` citations have drifted

**Layer: SKILL.**

Spot-checked while writing this file. **Two of two** citations copied out of `engine.md` pointed at
the wrong line — both off by exactly 6, in the same direction, consistent with an edit to `v2.py`
having shifted everything below it:

| `engine.md` says | actually at | what it is |
|---|---|---|
| `v2.py:11011` (§7) | **`v2.py:11017`** | `max_triggers_per_day` read off the trigger |
| `v2.py:15925` (§26) | **`v2.py:15931`** | `$player.core_traits.money -= _rent` |

The *claims* are correct — the code does what `engine.md` says it does. Only the line numbers are
stale, and I propagated both into this file before checking them, which is the exact failure this
file's own header warns about.

**Why it matters more than it looks.** `SKILL.md`'s first operating rule is *"Every engine claim
carries a `file:line`… Never assert engine behaviour from memory."* The whole mechanism assumes a
citation can be followed. A drifted line number sends the next reader to an unrelated statement —
`v2.py:11011` is `conditions = cond_obj`, which looks plausible enough to be believed.

**Suggested fix:** a cheap CI-style check that walks every `v2.py:NNNN` in `engine.md`, reads that
line, and flags any whose content no longer matches the surrounding claim. Failing that, re-verify
citations whenever `v2.py` is edited.

---

## 5 · The climb gate counts a ONE-SHOT canvas as farmable

**Layer: SKILL.** Found 2026-08-17.

Gate "the climb is paid for" walks every canvas that grants a gated meter and asks whether any
route into it is unbraked. Its grantor loop never checks `is_repeatable`:

```python
# .claude/skills/author-game-v2/scripts/gates.py:2033-2045
grantors = collections.defaultdict(list)
for c in (game.get("canvases") or []):
    got, minutes = _grants(c.get("nodes"))
    ...
    grantors[(subject, trait)].append((c["id"], amt, minutes, req, free))
```

**Observed, cleanly isolated.** After every genuinely repeatable grantor in this game was priced in
energy, the gate still failed — and the *only* remaining offender on both meters was
`canvas_opening`:

```
`cover`    0 → gate at 55, entirely for FREE — 14 clicks (canvas_opening ×14)
`relation` 0 → gate at 20, entirely for FREE —  7 clicks (canvas_opening ×7)
```

`canvas_opening` is the opening funnel. Verified from the built game:

```
trigger      = { location = "the_girls_room", is_repeatable = false, priority = 12 }
starting_canvas = "canvas_opening"      # it IS the start
canvases linking into it from outside: NONE
```

It is reachable **exactly once, at game start**. It cannot be clicked 14 times, so the 14 clicks the
gate is costing the player do not exist.

**Why this matters beyond one game.** The only way to satisfy the gate here is to put a `costs`
block on the game's opening — charging the player energy to read the intro — which would be a real
defect introduced purely to please a check. That is the same shape as the two prior instances
recorded in `SKILL.md` and as finding #3 above: *a check that fails a game for obeying the doctrine
is a bug in the check.*

`gates.py` already knows how to read this field correctly — it carries a whole constant and a
comment about it at line 158 (*"An ABSENT is_repeatable means REPEATABLE. Assuming false here is the
single…"*), and gate 1's own machinery resolves it at line 368. The climb gate simply does not
consult it.

**Suggested fix:** skip canvases whose trigger sets `is_repeatable = false` when building
`grantors`, using the same `IS_REPEATABLE_DEFAULT` resolution the rest of the file already uses.

---

## 6 · `gates.py` scores DEV SHORTCUTS as player-facing content

**Layer: SKILL.** Found 2026-08-17.

The engine treats dev shortcuts as a separate category and excludes them from a shipped game
three different ways:

```
v2.py:8428-8452   a canvas is a DEV SHORTCUT iff its trigger conditions contain
                  `dev_mode_enabled is_true` — a MARKER, not a gate
v2.py:1080        `dev_mode_enabled` is set at StoryInit ONLY in `--dev` builds
                  (no canvas sets it, and none should)
                  the flag-chain validator and the quest-hint index both SKIP them
```

**`gates.py` does none of this.** Verified: the string `dev_mode_enabled` does not appear anywhere
in it. So the moment `6_dev_shortcuts.toml` was added, two gates failed on a screen no player can
ever reach:

```
no free uncapped income   1 repeatable surface prints money without limit  (dev_shortcuts)
the climb is paid for     4 of 5 gated meters can be raised for free       (dev_shortcuts)
```

Both readings are literally true of the TOML and impossible in a shipped build.

**Worked around, not fixed.** Every dev choice now carries a 1-energy `costs` and the trigger a
`max_triggers_per_day`. That is harmless — nothing on that screen is player-facing, so braking it
distorts no design — but it is treating a symptom, and the next author who adds dev shortcuts will
hit the same two red gates with no idea why.

**Suggested fix:** skip canvases whose trigger conditions contain `dev_mode_enabled is_true` when
building the grantor and income sets, using the same test `v2.py:8440-8451` already implements.

**This is the second instance of the same class as #5**, and the class is now worth naming on its
own: *gates.py scores canvases the engine cannot reach in a shipped build.* One-shots (#5) and dev
shortcuts (#6) are both counted as farmable. A single guard covering "can this actually be entered
more than once by a player" would close both.

---

## Ownership summary

| # | fix lives in | cost | knock-on |
|---|---|---|---|
| 3 | `.claude/skills/author-game-v2/scripts/gates.py` | one line | kills the bug class for every future game that caps income |
| 1 | `references/engine.md` §21 | one paragraph | stops the next author finding it in a browser |
| 2 | `references/engine.md` §26 | one paragraph | same |
| 1 | `generators/v2.py:4659` | small | fixes a silent money-loss bug in every v2 game |
| 2 | `generators/v2.py:15916, :15929` | small | unblocks any game whose obligation is not rent — `steam` and `forty_miles` included |
| 4 | `references/engine.md` §7, §26 | two numbers | restores the one mechanism the skill's no-hallucination rule rests on |
| 5 | `.claude/skills/author-game-v2/scripts/gates.py:2034` | one condition | stops the climb gate charging the player for a one-shot intro |
| 6 | `.claude/skills/author-game-v2/scripts/gates.py` (grantor + income sets) | one guard | stops dev-only screens being scored as player content; closes the same class as #5 |

**Status: none applied.** All five touch shared files. Awaiting LO's call.

## How to re-verify

The probes that produced every result above are reproducible against any built game:

```bash
venv/bin/python manage.py package_from_toml \
    --file games/seventh_day/toml_phases/7_final_game.toml \
    --output games/seventh_day/output --gen-version v2
```

Then, in headless Chromium on the built `index.html` — click the age gate first
(`engine.md` §12), and note that `time_state` and `rent_state` live under
`State.variables.game_state`, **not** at the top level:

- **#1** — `setup.deductCostArray([{trait:'money', value:4}])` at money 150; read
  `State.variables.player.core_traits.money`.
- **#2** — `Engine.play('RentDay')` with `game_state.rent_state.is_due = true`; read the heading
  and the button text.
- **#3** — `venv/bin/python .claude/skills/author-game-v2/scripts/gates.py seventh_day`, read the
  `ascent tiers expand the world` line.
