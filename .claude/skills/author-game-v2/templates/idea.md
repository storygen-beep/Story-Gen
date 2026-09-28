# The idea — <game title>: her moment

> One page, written after the Want and before the world: what this game promises, and the first
> moment that proves it. Doctrine: `references/the-want.md` §0 and §6. The eight lines:
> `references/the-release.md`, "Her moment — eight lines". LO picks it before the board starts.
> The ledger keys are unchanged (`want.*`), so `scripts/pitch_pack.py` reads them as before.

---

## 1. The fantasy — what the player comes here to feel

**Which shape?** Pick one, or name a mix. Each has its own engine:

- [ ] **Fall by need** — she is short of money or a place, and the world prices her body *(rent, a price list)*
- [ ] **Rise by want** — she picked a goal and goes after it *(the goal, a rival, a clock)*
- [ ] **Taboo at home** — the house, and who is in the next room
- [ ] **Mystery** — she investigates, and something works on her while she does *(secrets she buys)*

**In one sentence, what does the player come here to feel?** <…>

**The model to beat:** <one named game> — **what ours does better:** <one line>

**Which moments does this game promise?** Tick the kinds it will keep delivering
(`references/moment-library.md` has ten of each):

- [ ] her firsts
- [ ] being seen
- [ ] her body as the price for something she needs
- [ ] taboo at home
- [ ] a consequence she has to live with

Record these as `want.fantasy_shape`, `want.model_to_beat` and `want.moment_kinds`.

## 2. The promise — what keeps pulling the player forward

- **The goal:** <a named goal> **by** <a date or a moment>
- **The mystery:** <what she does not know yet> — **it pays out** <roughly when>
- **The rival:** <who wants the same thing, or stands in her way>

The hold may go quiet; **the goal or the mystery stays alive**, and the guidance page carries it. A goal
announced and then forgotten is a named player complaint. Record it as `want.promise`.

## 3. The people who carry it

**The companion:** <who leads her, or whom she leads — the friend one step ahead, or one step behind>

**The pressure-man:** <optional — the man whose demand drives her choices; the price of her no, and her way out>

**Her face:** <one performer or one look, kept across the game — players notice when it changes>

Record them as `want.companion`, `want.pressure` and `want.face` (`references/the-want.md` §6).

## 4. The first step — her moment in eight lines

<the eight lines from `references/the-release.md`, "Her moment — eight lines", for the game's first
step: one sentence each>

Record them as the first release's `her_moment` (`references/state.md`).

---

**Then:** when LO has picked it, set `phase = "idea"` in `v2_state.json` and move to
`references/the-systems.md`, then `templates/board.toml`.
