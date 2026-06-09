# Economy / income — how the sandbox games do it (research for Gap 5)

Grounded study (RTS source 2026-06-09 + the survey) of how the reference games handle money/income,
before designing Gap 5 (`08` — the economy could be a grind-wall). Verdict: the games solve it the same
way, and the solution is *better* than "just add multiple jobs" — **the economy is itself a corruption
ladder.**

---

## RTS (source-verified) — the reference economy

**Two currencies + a laundering loop:**
- `money` (clean) — from legit work.
- `dirtyMoney` (lewd income) — from sex work; you **launder** it into clean money at a cut
  (`cleanMoney = dirtyMoneyToLaunder * (1 - cut)`). Lewd money is a *separate, corruption-flavored*
  currency you must process to spend cleanly.

**Income paths (multi-path, escalating, increasingly lewd):**
1. **Legit gig jobs** — `addMoney(job.income)`, escalating: **DogWalking 45 → HouseCleaning 75 →
   BabySitting / ElderlyCare 110.** Safe, low-pay, early.
2. **Lewd work — the big one** — pays `dirtyMoney`: a full **camgirl system** (`xcam` = 161 refs),
   **prostitution / clients** (`client` = 167 refs), **stripping** (11). Higher pay, gated on
   corruption/exhibitionism, and these *are* the lewd content (camming/escorting/stripping = the scenes).
3. **Scene / event payouts** — `addMoney(moneyValue)` from gigs and lewd scenes (e.g. discount sex).

**Spends (sinks):** rent/debt, property, clothing, lessons, the laundering cut.

---

## The KEY insight — the economy IS a corruption ladder
RTS doesn't just offer many jobs; it makes income **escalate from legit-low-pay to lewd-high-pay as you
fall.** So **making money and corrupting yourself are the SAME act.** The money pressure (rent/debt)
literally *pushes you toward the lewd paths because that's where the money is.* This is why it isn't a
grind:
- **Multiple paths** (do X or Y — the anti-grind fix), AND
- **the paths ARE content** (the camgirl/escort scenes), AND
- **they escalate** (each tier opens better-paying, dirtier work — a curve, not a flat repeat).
Earning *is* playing the fantasy, and the economy *drives the cascade* instead of sitting beside it.

---

## Cross-game confirmation (same pattern)
- **Lustbound:** cash + **OnlyFans** (`ofFollowers`) + **prostitution** (`prosRep` / `clientsServiced`)
  + a coffee job. Multi-path, lewd income paths dominate.
- **Gakko:** the **corporate-career ladder IS the income spine** (corporank → salary) — a career-ladder
  economy (legit), with the lewd as a parallel track.
- **The Company:** Money / Paycheck + a **slave economy** (buy/sell — `pitSlaves`/`SlavePrice`).
- **Back to Freedom:** money → **gifts** → raises NPC love/lust (spend-to-progress sink).
- **Generic Porn Game:** legit jobs + **interview** minigame + bank/sub-systems (life-sim portfolio).
**Universal:** income is multi-path and turns **increasingly lewd as you progress**, with **earning fused
to content** (the sex-work scenes are the income). Career-ladder is the legit variant; sex-work is the
corruption variant; gifts/laundering/slaves are sinks/twists.

---

## Implications for the Gap-5 design (next)
1. **Make the economy a corruption ladder, not a job list:** legit-low-pay early → lewd-high-pay as she
   falls. Money pressure should *pull her down the lewd path* (where the money is) — this fuses Gap 5
   with the cascade (`04`) and the desire ladder (`09`).
2. **Multiple income paths** (anti-grind: blocked/bored on X → do Y), each a *different* activity.
3. **Earning = content** (R7 from `09`): the paying activities are the lewd/reactive-world scenes
   (working the floor, camming, escorting) — never a chore-click that just adds cash.
4. **Tiered/escalating pay** so it's a curve, not a flat repeat (RTS 45→75→110 legit; lewd pays more).
5. **A dirty-vs-clean split + laundering** is an optional richening (RTS) — adds a corruption-flavored
   money loop + a sink; consider per-game, don't hardcode.
6. **Sinks that matter** (rent/debt deadline = the pressure; clothing access = the reactive-world dial
   `11`; gifts/property) so money always has a *wanted* use (ties to desire ladder).
7. **Clothing tie-in:** the lewd income paths require/benefit from the exposure dial (`11`) — working
   the floor revealing earns more *and* triggers the reactive-world content. Income, content, and
   reactivity are the same beats.

## Cross-references
- `08` Gap 5 (this) · `04` cascade (money pressure drives it) · `09` desire ladder (earning serves wants,
  R7) · `11` reactive world (lewd income = the clothing-triggered content) · `05` quality #3 (no grind).
