#!/usr/bin/env python3
"""
0.2.3 — HER FATHER'S HOUSE and THE HUNT — the whole chapter, live, end to end.

dev_jump_hunt_start -> end card L through real locations and real choices, in a real browser:
Cain at the cot -> the Site -> the ambush -> Kess and the seam -> four street losses with repairs at Kess's ->
Cain's training 70 -> 85 -> Bastien hears about Vega -> the Undertow rebuilt in three stages -> Bastien's list ->
Rue puts the word out -> the men refuse -> Dace's price -> the crew night -> the plan at the cot -> repaired ->
the take -> the table -> the cradles -> the end card.

Shortcuts, stated: fighting is seeded to 70 (the drills are 0.2.2 content), energy and coin are topped up between
sessions, and the clock moves only through advanceTime (waiting / sleeping).

Run from the repo root against output_dev (built --dev --debug):
    python games/vesper/tests/live_the_hunt.py
Exits 0 on pass, 1 on any failure.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

URL = (pathlib.Path(__file__).resolve().parent.parent / "output_dev" / "index.html").as_uri()
TS = "SugarCube.State.variables.game_state.time_state"
CT = "SugarCube.State.variables.player.core_traits"
fails, errs = [], []


def ok(cond, msg):
    print(("OK   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))

        def flag(f):
            return pg.evaluate(f"(function(){{var F=SugarCube.State.variables.flags; return Array.isArray(F)?F.includes('{f}'):!!F['{f}'];}})()")

        def tr(k):
            return pg.evaluate(f"{CT}.{k}")

        def psg():
            return pg.evaluate("SugarCube.State.passage")

        def wait_until(h):
            cur = pg.evaluate(f"{TS}.current_hour*60+{TS}.current_minute")
            pg.evaluate(f"window.advanceTime({(h * 60 - cur) % 1440 or 1440})")

        def enter(loc):
            pg.evaluate(f"SugarCube.Engine.play('Location_{loc}')")
            pg.wait_for_timeout(300)
            return psg()

        def click(text):
            el = [l for l in pg.query_selector_all("#passages a") if l.is_visible() and l.inner_text().strip() == text]
            if not el:
                return False
            el[0].click()
            pg.wait_for_timeout(300)
            return True

        def walk(exit_text):
            for _ in range(30):
                if click(exit_text):
                    return True
                links = [l for l in pg.query_selector_all("#passages a") if l.is_visible()]
                if not links:
                    return False
                links[-1].click()
                pg.wait_for_timeout(200)
            return False

        def hub(cid):
            pg.evaluate(f"SugarCube.Engine.play('Canvas_{cid}_Node_base')")
            pg.wait_for_timeout(300)

        def repair_to_under_30():
            wait_until(12)
            enter("kess_berth")
            hub("hub_kess_berth")
            while tr("vega_damage") >= 30 and click("Have him fix what she did."):
                click("Pay him. (10 coin.)")
                click("Get up.")
                hub("hub_kess_berth")

        pg.goto(URL)
        pg.evaluate("localStorage.clear()")
        pg.reload()
        pg.wait_for_function("window.SugarCube && SugarCube.State.variables.player", timeout=30000)
        pg.evaluate("SugarCube.Engine.play('Canvas_dev_jump_hunt_start_Node_seed')")
        pg.wait_for_timeout(300)
        click("To the cot.")

        # ── part one
        pg.evaluate("window.advanceTime(1440)")
        wait_until(7)
        ok(enter("the_cot") == "Canvas_cap_cain_comes_Node_base", "cap_cain_comes on a later morning")
        ok(walk("Go with him."), "Cain's scene")
        ok(psg() == "Canvas_cap_the_site_Node_base", "the Site scene on arrival")
        ok(walk("Walk back with him."), "the Site")
        ok(psg() == "Canvas_cap_the_ambush_Node_base", "the ambush on the walk back")
        ok(walk("Get down to Kess."), "the ambush")
        if psg() != "Canvas_cap_kess_seam_Node_base":
            wait_until(11)
            enter("kess_berth")
        ok(psg() == "Canvas_cap_kess_seam_Node_base", "Kess and the seam")
        walk("Get up.")
        ok(flag("seam_known") and tr("vega_damage") == 35, f"seam_known, damage {tr('vega_damage')}")

        # ── the hunt: four street losses
        pg.evaluate(f"{CT}.coin=600")
        losses = tries = 0
        while tr("vega_habits") < 4 and tries < 80:
            tries += 1
            pg.evaluate("window.advanceTime(1440)")
            wait_until(12)
            enter("kess_berth")
            if enter("underworld_strip") == "Canvas_rand_vega_street_Node_base":
                click("Run.")
                click("Home.")
                losses += 1
                repair_to_under_30()
        ok(tr("vega_habits") == 4, f"four habits from {losses} street losses in {tries} days")

        # ── Cain: 70 -> 85
        pg.evaluate(f"{CT}.fighting=70")
        sessions = 0
        while tr("fighting") < 85 and sessions < 20:
            pg.evaluate(f"{CT}.energy=100")
            wait_until(22)
            enter("the_site")
            hub("activity_cain_trains")
            if not click("Train with him."):
                break
            click("Enough for tonight.")
            sessions += 1
        ok(tr("fighting") == 85 and flag("cain_rule_heard"), f"fighting 85 after {sessions} sessions with Cain")

        # ── Bastien, the bar, the call, the men, Dace, the night
        wait_until(15)
        enter("the_cot")
        hub("amb_bastien_cot")
        ok(click("Tell him about Vega."), "tell Bastien about Vega")
        click("Go and see Sol.")
        for stage in ("Pay for the clearing. (40 coin.)", "Pay for the floor and the counter. (60 coin.)",
                      "Pay for the back wall, and open the doors. (80 coin.)"):
            wait_until(12)
            enter("underworld_bar")
            hub("activity_rebuild_undertow")
            ok(click(stage), stage)
            click("Leave him to it.")
        ok(flag("undertow_open"), "the Undertow open")
        wait_until(15)
        enter("the_cot")
        hub("amb_bastien_cot")
        ok(click("Tell him the bar is open."), "tell Bastien the bar is open")
        click("Take it to Rue.")
        wait_until(12)
        ok(enter("underworld_brothel") == "Canvas_cap_rue_takes_the_list_Node_base", "Rue takes the list")
        click("Leave her to it.")
        pg.evaluate("window.advanceTime(1440)")
        wait_until(19)
        ok(enter("underworld_bar") == "Canvas_cap_crew_refuses_Node_base", "the men refuse, the next evening")
        walk("Go and find Dace.")
        wait_until(20)
        ok(enter("underworld_pit") == "Canvas_cap_dace_price_Node_base", "Dace at the pit")
        walk("Tomorrow night.")
        pg.evaluate("window.advanceTime(1440)")
        wait_until(23)
        ok(enter("underworld_bar") == "Canvas_cap_the_crew_night_Node_base", "the crew night")
        walk("Go home to the cot.")
        ok(flag("crew_back"), "crew_back")
        ok(psg() != "Canvas_cap_the_plan_Node_base", "the plan does not fire in the crew night's breath")
        pg.evaluate("window.advanceTime(1440)")
        wait_until(15)
        ok(enter("the_cot") == "Canvas_cap_the_plan_Node_base", "the plan at the cot, the next day")
        walk("When she's ready.")
        ok(flag("vega_plan"), "vega_plan")

        # ── in one piece, then the take, the table, the cradles
        repair_to_under_30()
        ok(tr("vega_damage") < 30, f"repaired to {tr('vega_damage')}")
        wait_until(13)
        if enter("underworld_strip") == "Canvas_rand_vega_street_Node_base":
            click("Run.")
            click("Home.")
            repair_to_under_30()
            pg.evaluate("window.advanceTime(1440)")
            wait_until(13)
            enter("kess_berth")
            enter("underworld_strip")
        hub("activity_draw_her_out")
        ok(click("Draw her out."), "Draw her out.")
        walk("Get Kess.")
        ok(flag("vega_taken"), "vega_taken")
        ok(psg() == "Canvas_cap_the_table_Node_base", "the table, straight after the take")
        walk("Carry her to the Site.")
        ok(flag("vega_dismantled"), "vega_dismantled")
        ok(psg() == "Canvas_cap_the_cradles_Node_base", "the cradles, straight after the table")
        walk("Not tonight.")
        ok(flag("cradles_ready"), "cradles_ready")
        pg.evaluate("SugarCube.Engine.play('QuestsPage')")
        pg.wait_for_timeout(300)
        qt = pg.inner_text("#passages")
        ok("That is where this build ends" in qt and "Chapter complete" in qt, "the end card")
        print(f"  coin left {tr('coin')} | day {pg.evaluate(TS + '.day')}")
        b.close()
    ok(not errs, f"js errors {errs[:3]}")
    print("LIVE THE HUNT: " + ("OK" if not fails else f"{len(fails)} FAILED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
