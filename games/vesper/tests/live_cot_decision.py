#!/usr/bin/env python3
"""
"GO AND GET HIM OUT" (rev 228) — LIVE guard, in the built game.

⚠️ WHY THIS EXISTS BESIDE check_bunker_route.py §12. The static guard proves the SHAPE: the decision is a
one-shot, it waits `days_since_flag gte 1` on bastien_alive_known, it owns the coveralls, the old coveralls
canvas is retired. It cannot prove the WAIT, because the wait is arithmetic done in JavaScript that only
exists once the game is built: setup.triggerConditionsSatisfied reads $flags_meta[flag].set_day, which only
applyFlagEffect writes, against $game_state.time_state.day. A flag set any other way has no set_day and the
condition fails CLOSED — the decision would then never fire at all, and the build would still be green.

So this gets there the way a tester does — the real "0.2.2: Cain brings the news" dev jump, then the real
news scene walked to its exit, whose own flag effect writes set_day — and walks into the cot the way a player
does. (A hand-set flag on a fresh save proves nothing: the cot is gated `berth_home`, so no auto-fire runs
there at all, including the shipped news scene. The first cut of this script fell into exactly that.)

  * same calendar day  -> nothing fires, and there is no link to click either;
  * the next day       -> the decision fires by itself;
  * it walks into the folded coveralls node and sets rescue_agreed there;
  * back at the cot, the RETIRED coveralls canvas does not play a second copy of the same scene, and the
    decision does not fire again.

Needs playwright and a BUILT game:
    python manage.py package_from_toml --file games/vesper/toml_phases/7_final_game.toml \\
      --output games/vesper/output_dev --video-folder games/vesper/videos --dev --debug
    python games/vesper/tests/live_cot_decision.py
Exits 0 on pass, 1 on any failure.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

GAME = pathlib.Path(__file__).resolve().parent.parent / "output_dev" / "index.html"
fails = []


def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond:
        fails.append(msg)


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page()
        page.goto(GAME.as_uri())
        page.wait_for_function("typeof SugarCube !== 'undefined' && SugarCube.State.variables.player",
                               timeout=30000)

        def passage():
            return page.evaluate("() => SugarCube.State.passage")

        def body():
            return page.inner_text("body")

        def go(name):
            page.evaluate("p => SugarCube.Engine.play(p)", name)
            page.wait_for_timeout(350)

        def flag(name):
            return page.evaluate("n => !!SugarCube.State.variables.flags[n]", name)

        def click(pattern):
            """Only ever click what a player can see. The whole story source sits in the DOM as
            <tw-passagedata>, so a text locator would happily click a hidden copy and prove nothing."""
            hit = page.evaluate("""pat => {
                const re = new RegExp(pat);
                const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
                const el = Array.from(document.querySelectorAll('#passages a, #passages button'))
                    .filter(vis).find(e => re.test((e.innerText || '').trim()));
                if (!el) return false; el.click(); return true; }""", pattern)
            page.wait_for_timeout(300)
            return hit

        def walk_cascade(until):
            """Advance a cascade one visible beat at a time until the exit labelled `until` shows."""
            for _ in range(20):
                if until in body():
                    return True
                adv = page.evaluate("""() => {
                    const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
                    const el = Array.from(document.querySelectorAll('#passages .cascade-advance, #passages a, #passages button'))
                        .filter(vis).filter(e => !e.classList.contains('link-external'))
                        .filter(e => !/^(Back|Save|Journal|Cheat|Quests|Schedule)$/i.test((e.innerText||'').trim()))
                        .pop();
                    if (!el) return false; el.click(); return true; }""")
                page.wait_for_timeout(250)
                if not adv:
                    break
            return until in body()

        # ── get there the way a tester does: the real dev jump, then the real news scene ──
        # ⚠️ NOT a hand-set flag on a fresh save. The cot is gated `berth_home is_true` (its
        # entry_conditions), so a fresh save cannot enter it and NO auto-fire runs there — the first
        # cut of this script did exactly that and "proved" the decision never fires, when in fact the
        # shipped news scene did not fire either. The jump seeds the end of 0.2.1, and the news scene's
        # own exit sets bastien_alive_known through applyAndNotifyFlag, which is what writes set_day.
        go("Canvas_dev_jump_way_down_start_Node_seed")
        check(click("^To the cot\\.$"), "took the 0.2.2 dev jump to the cot")
        page.wait_for_timeout(400)
        check(passage() == "Canvas_cap_bastien_alive_Node_base",
              f"the news fires on arrival — the control (on {passage()})")
        check(walk_cascade("Let him go."), "walked the news to its exit")
        check(click("^Let him go\\.$"), "Cain leaves")
        page.wait_for_timeout(400)
        check(flag("bastien_alive_known"), "the news scene's own exit set bastien_alive_known")
        meta = page.evaluate("() => (SugarCube.State.variables.flags_meta || {}).bastien_alive_known")
        today = page.evaluate("() => SugarCube.State.variables.game_state.time_state.day")
        check(bool(meta) and meta.get("set_day") == today,
              f"and it carries the day it was set (set_day {meta and meta.get('set_day')}, today {today})")

        print("\n[1] the same day — nothing happens")
        p = passage() or ""
        check("go_after_him" not in p, f"landing back at the cot, the decision does NOT fire (on {p})")
        go("Location_the_cot")
        check("go_after_him" not in (passage() or ""), f"the decision does NOT fire the same day (on {passage()})")
        check("Go and get him out" not in body(), "and there is no link to click either")
        check(not flag("rescue_agreed"), "rescue_agreed is still unset")

        print("\n[2] the next day — it happens by itself")
        page.evaluate("() => { const t = SugarCube.State.variables.game_state.time_state; "
                      "t.day = t.day + 1; t.current_hour = 9; t.current_minute = 0; }")
        go("Location_the_cot")
        check(passage() == "Canvas_activity_go_after_him_Node_base",
              f"the decision auto-fires on the first cot visit a day later (on {passage()})")
        check("since yesterday" in body().lower(), "and the prose knows a day has passed")

        print("\n[3] the decision, then the coveralls, as one scene")
        check(walk_cascade("The bag under the bench."), "the decision's cascade reaches its exit")
        check(click("^The bag under the bench\\.$"), "clicked into the coveralls")
        check(passage() == "Canvas_activity_go_after_him_Node_coveralls",
              f"the coveralls are the decision's second node (on {passage()})")
        check(flag("rescue_agreed"), "rescue_agreed is set at the moment she decides")
        check("twice already" not in body(), "the folded copy lost the count that contradicted 'once'")
        check(walk_cascade("The depot opens at nine."), "the coveralls cascade reaches its exit")
        check(click("^The depot opens at nine\\.$"), "left the scene")

        print("\n[4] back at the cot — nothing plays twice")
        page.wait_for_timeout(400)
        p = passage() or ""
        check("cap_back_into_cover" not in p,
              f"the RETIRED coveralls canvas does not fire a second copy (on {p})")
        check("go_after_him" not in p, f"and the decision does not fire again (on {p})")
        go("Location_the_cot")
        p = passage() or ""
        check("cap_back_into_cover" not in p and "go_after_him" not in p,
              f"nor on the next visit (on {p})")

        b.close()
    print("\n" + ("LIVE COT DECISION: OK" if not fails else f"LIVE COT DECISION: {len(fails)} FAILED"))
    for f in fails:
        print("  - " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
