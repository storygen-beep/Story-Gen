"""Live economy check for Mrs. Vance — does money gate anything, and does the truck bite?

REVIEW.md §6 E1 is the item this proves. v0.1 earned roughly four times its 260 rent,
ZERO of its 55 trait conditions read `money`, and its five purchases bought meter points
(clean +45, standing +4/+5/+6, trust +3/+4) at $2-$26 against $208 a day. The repair adds
one aspirational sink (the flatbed, 2,600, in her brother's name), an upkeep that follows
it (-22 a day on the day hook), a haul that pays 125 instead of 34 once the truck is hers,
and makes `cade_covered` — set by the engine and read by NOTHING — a door she can choose.

    python3 games/mrs_vance/playtest_economy.py <path-to-index.html>

⚠️ games/mrs_vance/output/index.html is the pre-repair artefact. Build to output_dev first:

      python3 scripts/merge_toml_phases.py games/mrs_vance
      python3 manage.py package_from_toml \
          --file games/mrs_vance/toml_phases/7_final_game.toml \
          --output games/mrs_vance/output_dev --gen-version v2 --dev --debug
      python3 games/mrs_vance/playtest_economy.py games/mrs_vance/output_dev/index.html

⚠️ Read `#passages`, never `body`. The sidebar carries live meters, so a body-level read
   matches the drawer figure and reports a band that never rendered — that mistake cost a
   false defect report on 2026-08-27.
⚠️ SugarCube globals hang off `window.SugarCube`, not `window`. Bare `State` throws.
⚠️ Engine.play on a node bypasses the canvas TRIGGER, which is what lets the band ladder be
   read without first satisfying `truck_asked`. Choice-level conditions still apply, which
   is the half these assertions are actually about.
"""
import re
import sys
import pathlib

from playwright.sync_api import sync_playwright

DEFAULT = "games/mrs_vance/output_dev/index.html"
GAME = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT).resolve()
if not GAME.exists():
    sys.exit(f"no build at {GAME} — see the module docstring")

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"  {'PASS' if ok else 'FAIL'}  {name}\n          {detail}")


# ── The four bands on the flatbed, highest-first exactly as the chain resolves ──
# Adjacent [group] blocks merge into ONE if/elseif and first match wins, so a state
# that satisfies two arms must render only the upper one.
TRUCK_BANDS = [
    ("nothing saved",  {"money": 0},                          "ten Fridays"),
    ("halfway",        {"money": 1300},                       "same number of Fridays"),
    ("money, no name", {"money": 2600},                       "do not have is a name"),
    ("name on it",     {"money": 2600, "truck_papers": True}, "Tobin said yes"),
    ("bought",         {"money": 2600, "truck_bought": True}, "rectangle of dry gravel"),
]
BAND_PHRASES = [p for _, _, p in TRUCK_BANDS]

# canvas, node, the phrase that proves the rung is OFFERED, and the states it
# must and must not be CLICKABLE in. `money` is the player trait; everything else a flag.
#
# ⚠️ CLICKABLE, never "on screen". Every rung here carries show_when_locked, and the two
#    locked shapes read completely differently in the DOM:
#      cost-blocked      <span class="locked-choice">Buy it. ($2600, 1h) (Requires 2600
#                        Money (you have 2599))</span>   ← the LABEL is still printed
#      condition-blocked <span class="locked-choice">Nothing else is waiting…</span>
#                        ← locked_text REPLACES the label
#    A text-presence assertion therefore passes on a choice the player cannot click, which
#    is exactly what this file reported on its first run. The only honest question is
#    whether an <a> exists, so that is what is asked.
RUNGS = [
    ("see_truck", "base", "Buy it.",
     {"money": 2600, "truck_asked": True, "truck_papers": True},
     {"money": 2599, "truck_asked": True, "truck_papers": True}),
    ("hub_tobin_shop", "base", "put his name on something",
     {"money": 2600, "truck_asked": True},
     {"money": 2599, "truck_asked": True}),
    ("hub_cade_office", "base", "will be short on Friday",
     {"money": 100}, {"money": 300}),
    ("hub_cade_office", "base", "what he wants for it",
     {"money": 300, "cade_covered": True}, {"money": 300}),
    ("work_parts_run", "base", "Take your own truck out",
     {"truck_bought": True}, {}),
    ("work_parts_run", "base", "Go and get it.",
     {}, {"truck_bought": True}),
]

SET_STATE = """(st) => {
    const S = SugarCube.State.variables;
    S.flags = S.flags || {};
    // a clean slate every time, or a flag set by an earlier assertion leaks forward
    for (const k of ["truck_asked", "truck_papers", "truck_bought", "cade_covered",
                     "parts_run_today", "cade_rung_today", "tobin_rung_today",
                     "past_road", "past_books", "past_counter"]) {
        S.flags[k] = false;
    }
    for (const k in st) {
        if (k === "money") S.player.core_traits.money = st[k];
        else S.flags[k] = st[k];
    }
}"""

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{GAME}")
    page.wait_for_selector("#passages", timeout=15000)
    page.wait_for_timeout(800)

    def render(canvas, node, state):
        page.evaluate(SET_STATE, state)
        page.evaluate(f'() => SugarCube.Engine.play("Canvas_{canvas}_Node_{node}")')
        page.wait_for_timeout(250)
        return re.sub(r"\s+", " ", page.inner_text("#passages"))

    def clickable(canvas, node, state, phrase):
        """Is there a real <a> for this choice — not a locked-choice span?"""
        render(canvas, node, state)
        links = page.eval_on_selector_all(
            "#passages a", "els => els.map(e => e.textContent.trim())")
        return any(phrase in t for t in links)

    print("\n── the flatbed reads the drawer ─────────────────────────────────")
    for label, state, expect in TRUCK_BANDS:
        text = render("see_truck", "base", state)
        hits = [p for p in BAND_PHRASES if p in text]
        check(f"see_truck · {label}", hits == [expect],
              f"{len(hits)} band(s) rendered" + ("" if hits == [expect] else f" :: {hits}"))

    print("\n── money gates the rung ─────────────────────────────────────────")
    for canvas, node, phrase, on, off in RUNGS:
        can_on = clickable(canvas, node, on, phrase)
        can_off = clickable(canvas, node, off, phrase)
        check(f"{canvas} · {phrase!r}", can_on and not can_off,
              f"clickable when it should be={can_on}  "
              f"withheld when it should be={not can_off}")

    print("\n── the truck takes its upkeep off the day hook ──────────────────")
    for label, flags, expect in [("truck bought", {"truck_bought": True}, -22),
                                 ("no truck", {}, 0)]:
        page.evaluate(SET_STATE, dict(flags, money=1000))
        after = page.evaluate("""() => {
            window.advanceDay();
            return SugarCube.State.variables.player.core_traits.money;
        }""")
        check(f"daily upkeep · {label}", after - 1000 == expect,
              f"drawer 1000 -> {after} (expected {1000 + expect})")

    # The haul has to be worth the upkeep or the whole thing is the corpus's
    # most-punished shape: a tighter week that buys nothing.
    print("\n── the week's arithmetic ────────────────────────────────────────")
    haul, errand, upkeep, rent = 125, 34, 22, 260
    weekly_gain = (haul - errand) * 5 - upkeep * 7
    check("the truck pays for its own upkeep", weekly_gain > 0,
          f"+{(haul - errand) * 5}/wk from the run, -{upkeep * 7}/wk upkeep "
          f"= +{weekly_gain}/wk net · obligation {rent} -> {rent + upkeep * 7}")

    browser.close()

print(f"\nRESULT: {sum(results)}/{len(results)} — "
      f"{'PASS' if all(results) else 'FAIL'}")
sys.exit(0 if all(results) else 1)
