# Notes — Billable Hours

Decisions LO made in conversation that aren't on a signed page yet, or that explain one. Newest
first. Each line says who decided and when.

## 2026-09-30 — before the v0.1 build

- **Sheets written by the author, for this game only.** LO's standing rule for this skill test was
  "never write the game's sheets/". LO lifted it for billable_hours: "write them for this game".
  The drafts in `proposals/` were copied into `sheets/` and `DECISIONS.md`, marked [READY], signed
  LO 2026-09-30. `proposals/` stays as the record of what was drafted.
- **Traversal heat (gate check, item 1).** Explicit top bands were added to two walk-ins so the
  explicit floor reaches the traversal layer from minute one, as the first-release rule asks:
  - the hotel bar's walk-in, nerve 30+: a stranger in a suit (beat B11);
  - the firm's walk-in, nerve 30+: an unnamed associate in the copy room (beat B10).
  LO's approved reading said "Callahan, late" for the firm. The author used an associate instead,
  because Callahan has no ladder yet and the skill says a man's first third has no sex and his
  want is shown before he acts on it (`the-arc.md` A2, A13). **Open question to LO: keep the
  associate, or give Callahan a ladder first?** Callahan's "Stay tonight" line stays in the same
  band as a v0.2 hook.
  That puts 5 of 7 destinations with a sex scene (intent): her room, the landing, the club, the
  firm, the hotel bar.
- **What money buys opens a door (item 2).** Left for v0.1: no shop, so money buys drinks and pays
  Martin. Accepted as a REPORT red.
- **Theo's bold answer pays $250 (item 3).** `week_income` raised from $550 to $600 so the honest
  maximum is true. SP4 amended.
- **Jade's "Next one's yours" (item 4).** An open promise. Paid in v0.2 (Jade step 2, the stage).

## 2026-09-30 — earlier, already on signed pages

- Premise L, taboo at home plus the rise at work (WANT, IDEA).
- The bill is collected at breakfast by the engine's rent page, and rises $250 → $300 → $350
  (WANT §2 amended; SP4).
- The board split the house into rooms; SP2 and SP7 re-signed (F5).
- Skill-test findings live in `SKILL_TEST_FINDINGS.md`, not here.

## 2026-10-01 — found while writing the v0.1 TOML (author; LO to confirm)

- **Martin's step 3 is the door, and the lock moves to the choice.** A door has to render
  locked, so the step-3 canvas fires on `martin_stage` 2 (Fridays) and shows "Take the jacket
  off." locked on Martin's want ≥ 15. In v0.1 every raise of his want is capped at 14, so the door
  stays locked all release and the engine prints his need beside it. The v0.2 release lifts the
  cap together with the step's content. The martin_03 sheet said "reachable: yes", which
  contradicted SP7's "content ships in v0.2"; SP7 wins. Ledger: step 3 `gate = []`,
  `release_page.door = {martin_03_jacket_downstairs, "Take the jacket off."}`.
- **Day one at the firm starts at 10:00.** The gate "a meeting fires where they are" needs the
  firm scene inside both Callahan's hours (08–19) and Theo's (Mon 10–12). The opening now sends
  her in on the later bus ("Callahan said ten"). Screens 6–9 of OPENING move by about an hour.
- **Ethan eats dinner at home.** The dinner scene names him, so he gets a schedule row at the
  house, Mon–Fri 18:00–19:00.
- **Theo's step 1 and Jade's step 1 carry their dependency in the trigger** (`martin_stage ≥ 1`;
  `opening_done`), so the ledger's step gates list them.

## 2026-10-01 — the v0.1 build, where it differs from the signed sheets (author; LO to confirm)

Each change came out of a gate or the engine, and each one is noted here so the sheets can be
brought up to date in one pass.

- **Opening clock.** The bus home on day one lands at ~18:09, not 17:30 plus change. With +30
  the gate's funnel walk put her in the kitchen at 17:54, before dinner's 18:00 window, which meant
  dinner never fired and a new game stalled (`gates.py` `_funnel_walk`). Now +45.
- **Theo speaks as himself in the opening.** One line after Callahan names him ("I remember
  everything I pay for"). Without it the gate could not see him met: a Stranger line and a name in
  narration are not a meeting.
- **Walk-ins carry their host's day cap** (shower_today, eat_today, worked_today, drink_today,
  club_today on the walk-in's own trigger). Otherwise a walk-in read as free income / a free nerve raise.
- **Drinks cost $8 on the choice, not on the trigger.** A trigger cost clamps money to 0–100
  (`engine.md` §27). Each drink screen keeps a free way out.
- **The Velvet Room's stage opens after the opening, not after meeting Jade**, so the club is never
  open with nothing to do.
- **Callahan Reed closes at 19:00** (21:00 on Thursdays, for Ethan's late step).
- **Martin gets three more surfaces**: his house hub now runs whenever he is home (breakfast and
  evening lines), plus `hub_martin_firm` and `hub_martin_study`. Every schedule row needs something
  of his in the room.
- **Martin's numbers are read by a line and a gate each.** Want ≥ 10: his hand on her shoulder at the
  table. Power ≥ 10: she can no longer say she's busy and leave breakfast.
- **Nerve bands**: Careful 0–9 · Curious 10–29 · Bold 30–100. "Shameless" is gone until content
  exists at 60. A real gate at 30: Jade's "what Saturday is really like".
- **B12, a new explicit beat on the bus downtown** (nerve 30+), for the traversal layer.
  80 words · 7 explicit (ass, cock, grope, nipple, tit) · median 9 · last sentence on the body.
- **Ethan's memo reads all three start answers**, with a fallback line.
- **Jade has a card before she is met** (Monday after nine), so her step 1 has a guidance line.
- **Martin's step-3 card** is a goal card with his want as the goal, labelled "(opens in the next
  update)". His want stops at 14 in v0.1.

## Still open for LO

1. **Word budgets.** The build delivers 4,494 location words against the 27,800 declared on the
   board (gate `location fill`, a REPORT row). Either the prose grows toward the budgets before
   v0.1 ships, or the budgets are re-declared at what v0.1 is. Your call. It's a design number,
   and a budget moved after the fact is only a description.
2. **Who climbs.** Declared `both`, and the build puts 12% of the climb on the cast (gate needs
   ≥ 25% each side). With Ethan, Theo and Jade on counters only (approved at the Want), the
   build is really `player`. Either re-declare `player` (SP2), or give more men meters that gate.
3. **Callahan vs the associate** in the firm walk-in's top band (see above).

## 2026-10-01 — LO's calls on the open items, and the reader-fix pass

- **Budgets:** the 27,800 declared stay as the game's target. v0.1 ships under them, and
  `location fill` is a known REPORT red. Later releases grow toward them (LO approved the author's
  recommendation).
- **Who climbs:** re-declared `player` (SP2 amended).
- **Firm walk-in top band:** stays the unnamed associate.
- **Reader waivers** (LO): the three stranger "want" FAILs (F9) and the walk-in's week-income
  "numbers" FAIL, saved in `release_page.reader_waivers`.
- **Fix pass:** every other reader FAIL was addressed in the TOML: hooks and next steps on the hubs,
  written refusals that move a flag or a number (each flag is read by a line), her low-nerve voice on
  the open-door, corridor, Theo and shower-watch scenes, Martin noticing Theo's cash, Diane noticing
  the Fridays, Ethan's leak at breakfast, Jade's invitation answered at dinner, the stage needing Jade
  met, and the bus's woman across the aisle.
