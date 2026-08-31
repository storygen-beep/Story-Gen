# Build log — every red, in the order it appeared

Running notes kept while driving `night_desk` 0.0.1 to a green build, so
`BUILD_VS_SHEET.md` is written from what happened rather than reconstructed from
a diff. Each entry: what failed, what it actually was, and whether the sheet
format had anywhere to catch it.

---

## 1 · `op = "sub"` is discarded by the engine — 9 canvases

**The error**

> trait effect uses op='sub', which the engine discards (applyTraitEffect runs only
> ['add', 'set'], generators/v2.py:5742-5751)

**What it was.** A translation error, not a design error. `applyTraitEffect` runs
`add` and `set` and nothing else; `sub` parses, imports, and silently does nothing.
Every `energy` cost in the game was written as `sub` and every one of them would
have been free.

**Caught by:** the importer's own validator, before the build. It is a hard fail
with the fix in the message, which is the good version of this.

**Did the sheet format have a row for it?** ⚠️ **No, and it is a real gap.** The
place sheets carry a cost column — `20m`, `+energy`, `hunger half` — and nothing
that says how a cost is *written*. The format describes the economics and stops
one level above the mechanism, so an author fills the gap from memory. Nine
canvases, one habit, one wrong guess.

**Fix:** `op = "add"` with a negative value, everywhere.

---

## 2 · `v2_state.json` was written to a schema nothing reads

**What it was.** The first ledger declared `board.fill` as a dict, `ascent_tiers` at
the top level, and no `board.map`, `board.characters` or `board.economy`. Six gates
degraded to "no ledger" backstops and one printed *"[top-3 guess — no
v2_state.json]"* while the file sat right there being read by a different gate.

**Did the sheet format have a row for it?** ⚠️ **No.** The sheets are the design;
`v2_state.json` is the ledger the scoreboard reads, and **nothing in the format
connects the two.** A design can be complete, signed off and correct and still
declare nothing the instrument can check against.

---

## 3 · `op = "sub"` on the walk-in effects — the same fix, twice

Caught by grep after entry 1, not by a second build. Nine sites the first time,
none the second, because the habit had already been broken.

---

## 4 · Quest-card conditions use `trait`; canvas conditions use `trait_key`

**The error**

> quest_cards[0].when[0]: condition item must set either `flag` or `trait`

**What it was.** Two parsers, one word. A canvas condition is
`{ type = "trait", subject = "player", trait_key = "corruption", … }` and a quest
card condition is `{ type = "trait", subject = "player", trait = "corruption", … }`
(`template_import.py:1361`). The error message names the key it wants and gives no
hint that the other half of the same file uses a different one.

**Did the sheet format have a row for it?** No — and it should not. This is an
engine asymmetry, not a design question. It belongs in `engine.md`, and it is the
kind of thing that costs one build every time somebody meets it for the first
time.

---

## 5 · Quest goals need a `label`; every card needs a `when`

Two more validation rounds on the same block. `label` renders next to the ◯ bullet on the quest page;
a card with no `when` is refused outright — *"Every card must scope itself to a state-window."*

---

## 6 · `hide_value` on a sidebar item does not hide the value

`engine.md` §30: the sidebar prints two things about a trait from two places that do not know about
each other — the auto Traits dump, and whatever `[[sidebar_items]]` you wrote. Suppression is
`[[traits.labels]] hidden = true` and nothing else. Guessed `hide_value` first; it parsed, imported,
built, and did nothing.

---

## 7 · The brake has to be on the TRIGGER — three rounds lost to this

`the climb is paid for` kept failing while costs were being added to choice after choice. `_is_free`
(`gates.py:2913`) reads `trigger.costs`, `trigger.max_triggers_per_day`, or a day-cap flag condition
on the trigger. *"One unbraked door makes the whole rung farmable, no matter how well priced the
other doors are."* Moving the same costs to the triggers fixed five meters at once.

⚠️ **The sheets say "caps at 44" and "+2 a visit, caps at 10"**, which reads as a property of the
rung. It is a property of the way in. `BUILD_VS_SHEET.md` §9.

---

## 8 · Two duplicate-key parse failures, both from scripted edits

`costs` written twice into one choice by two passes that each thought they were adding it. TOML says
*"Cannot overwrite a value"* with a line number and no key name. A dedupe pass over every phase file
found three more.

---

## 9 · The money was in the wrong place, and the gate found the design error

`no free uncapped income` flagged the check-in as a faucet: +$6 per click, no cap. The fix was not a
cap — it was that **decision 11 says the pay rides on OCCUPANCY at midnight**, not on the act of
checking somebody in. The check-in now fills a room; the audit counts the drawer, after midnight,
day-capped, banded on how full the motel is.

**The gate caught a translation that contradicted a signed decision**, and the sheets did not.

---

## Final state

```
merge          6 phases → 7_final_game.toml, 152 KB
build          ✓ validation passed, 1141 KB
gates          39/40 · only `location fill` red
--release      4/6 · 35/35 canvases reached the build
```

`location fill` is the size floor and cannot be edited green: 4,590 words, mean 656 per location,
against a backstop expecting 4,500. The two release-check reds are expected — no media in a
testing-stage build, and 0.0.1 is not filed as published.
