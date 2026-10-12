#!/usr/bin/env python3
"""
0.2.4 — THE TRANSFER — the whole chapter, live, end to end.

dev_jump_hunt_take -> the take -> the table -> the cradles (0.2.3's end, played for real) -> the study: three
nights with Kess and Cain at the Site and nine reads of Vega's records (the twice-a-day cap checked on the
Site's own card list) -> the last night -> the transfer -> the Rise -> the plan -> the Tower (the "wait" branch
taken, so the second door node is walked too) -> Lyra and Nova -> Dace -> home -> the memory -> Cain -> end card O
-> what stands after: the empty cradle by day and Cain at night, the wreck at Kess's, Bastien's Dace band and card.

Shortcuts, stated: fighting is seeded to 85 for the take (0.2.3 content), energy is topped up between sessions,
and the clock moves only through advanceTime (waiting / sleeping) or by setting the hour before an entry.

Run from the repo root against output_dev (built --dev):
    python games/vesper/tests/live_the_transfer.py
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

        def hour():
            return pg.evaluate(f"{TS}.current_hour")

        def text():
            return pg.inner_text("#passages")

        def at(h, m=0):
            pg.evaluate(f"{TS}.current_hour={h}; {TS}.current_minute={m}")

        def play(passage):
            pg.evaluate(f"SugarCube.Engine.play('{passage}')")
            pg.wait_for_timeout(300)
            return text()

        def links():
            return [l for l in pg.query_selector_all("#passages a") if l.is_visible()]

        def click(t):
            el = [l for l in links() if l.inner_text().strip() == t]
            if not el:
                return False
            el[0].click()
            pg.wait_for_timeout(300)
            return True

        def walk(exit_text):
            """Advance a cascade to its exit link and stop there (the exit is not clicked)."""
            for _ in range(40):
                if any(l.inner_text().strip() == exit_text for l in links()):
                    return True
                ls = links()
                if not ls:
                    return False
                ls[-1].click()
                pg.wait_for_timeout(150)
            return False

        def scene(cid, exit_text, must=()):
            """The run's links: assert the scene is on screen, walk it, check lines, take the exit."""
            ok(psg() == f"Canvas_{cid}_Node_base", f"{cid} fires (on {psg()}, hour {hour()})")
            h0 = pg.evaluate(f"{TS}.current_hour*60+{TS}.current_minute")
            ok(walk(exit_text), f"{cid}: walked to '{exit_text}'")
            h1 = pg.evaluate(f"{TS}.current_hour*60+{TS}.current_minute")
            print(f"     clock {cid}: start {h0//60:02d}:{h0%60:02d}, at exit {h1//60:02d}:{h1%60:02d}")
            t = text()
            for line in must:
                ok(line in t, f"{cid} renders: {line}")
            click(exit_text)
            pg.wait_for_timeout(300)
            return t

        pg.goto(URL)
        pg.evaluate("localStorage.clear()")
        pg.reload()
        pg.wait_for_function("window.SugarCube && SugarCube.State.variables.player", timeout=30000)

        # ── 0.2.3's end, played for real: take -> table -> cradles
        play("Canvas_dev_jump_hunt_take_Node_seed")
        click("To the berth.")
        at(13)
        play("Canvas_activity_draw_her_out_Node_base")
        click("Draw her out.")
        walk("Get Kess.")
        click("Get Kess.")
        pg.wait_for_timeout(300)
        walk("Carry her to the Site.")
        click("Carry her to the Site.")
        walk("Not tonight.")
        click("Not tonight.")
        ok(flag("cradles_ready"), "0.2.3 end reached: cradles_ready")
        qt = play("QuestsPage")
        ok("Read Vega's records" in qt and "Chapter complete" not in qt, "card M (the study) is live; nothing says the chapter is complete")

        # ── the reading card: twice a day, then gone from the Site's list until midnight
        pg.evaluate("window.advanceTime(1440)")
        at(9)
        reads_today = 0
        for _ in range(3):
            pg.evaluate(f"{CT}.energy=100")
            t = play("Location_the_site")
            if "Vega's records" not in t:
                break
            click("Vega's records")
            if not click("Read her records."):
                break
            reads_today += 1
            click("Unplug the reader.")
        ok(reads_today == 2, f"the reading card opens twice in one day, got {reads_today}")
        ok(tr("vega_records") == 2, f"vega_records 2 after the first day, got {tr('vega_records')}")

        # ── three study nights, the records to 9 alongside (direct opens after the cap was proven)
        for night, (cid, exit_text, must) in enumerate([
            ("cap_study_blade", "Leave her for tonight.", ("That's new.", "Plate. Under the skin.")),
            ("cap_study_signal", "Leave the damper on.", ("She's calling home.", "Not long if you fight.")),
            ("cap_study_method", "Open your eyes.", ("The neck. Always the neck first.", "Keep going. He needs all of it.")),
        ]):
            pg.evaluate("window.advanceTime(1440)")
            for _ in range(3):
                if tr("vega_records") >= 9:
                    break
                pg.evaluate(f"{CT}.energy=100")
                at(10 + _)
                play("Canvas_activity_read_vega_Node_base")
                click("Read her records.")
                click("Unplug the reader.")
            at(22, 5)
            play("Location_the_site")
            scene(cid, exit_text, must)
            ok(hour() >= 4 and hour() < 6, f"{cid}: 360 minutes carry the clock past both men (hour {hour()})")
        while tr("vega_records") < 9:
            pg.evaluate(f"{CT}.energy=100")
            play("Canvas_activity_read_vega_Node_base")
            click("Read her records.")
            click("Unplug the reader.")
        ok(tr("vega_records") == 9, "nine reads")
        t = play("Canvas_activity_read_vega_Node_base")
        ok("She has read all of it." in t and "Read her records." not in t, "after nine, the read is no longer offered")
        qt = play("QuestsPage")
        ok("One more night as yourself" in qt, "card M's ready_text once every goal is met")

        # ── Kess's own card on a night with nothing due (records full, method done, last night not yet: Cain absent)
        # is covered statically; here, the last night fires with Cain alone.
        pg.evaluate("window.advanceTime(1440)")
        at(21, 10)
        play("Location_the_site")
        scene("cap_last_night", "Morning.", ("I'm scared, Cain.", "Hold me anyway.", "Tonight I'll sit with you."))
        ok(flag("last_night_held"), "last_night_held")

        # ── THE RUN: the transfer needs both men; everything after fires on arrival with no gate
        pg.evaluate("window.advanceTime(720)")
        at(22, 10)
        play("Location_the_site")
        scene("cap_the_transfer", "Morning. The Rise.", ("Fuck me. It worked.", "I'm still scared, Cain."))
        ok(flag("transferred"), "transferred")
        ok(8 <= hour() <= 10, f"the Rise renders in Sabin's floor hours, 08:00-11:00 (hour {hour()})")
        scene("cap_the_rise", "Back to the Site.", ("He's downstairs until eleven", "Vance Tower", "This is the eleven thousand.", "You never look at anybody."))
        scene("cap_tower_plan", "Night. The Tower.", ("Of course it's the bloody Tower.", "by three"))
        # the Tower: take the WAIT branch first
        ok(psg() == "Canvas_cap_the_vault_Node_base", f"cap_the_vault fires ({psg()})")
        walk("Step back. Wait for the change.")
        click("Step back. Wait for the change.")
        ok(psg() == "Canvas_cap_the_vault_Node_wait" and "two fresh men" in text(), "the wait branch: a fresh pair, the same door")
        click("Turn the wrist down.")
        walk("Go in.")
        ok("You're one of ours." in text(), "the blade node renders")
        click("Go in.")
        walk("Run.")
        ok("Vesper" in text() and "Don't open it." in text(), "the vault: her drawer, carried out unopened")
        click("Run.")
        ok(hour() < 3, f"the fight renders before three (hour {hour()})")
        scene("cap_lyra_and_nova", "Don't let go.", ("Lyra and Nova", "shut her signal off"))
        ok(hour() >= 3, f"the save renders after three: she was late (hour {hour()})")
        scene("cap_dace_falls", "Home.", ("Not her. Go on. Not her.", "I did not think I would pay for his."))
        ok(flag("dace_dead"), "dace_dead")
        scene("cap_back_in_body", "Remember.", ("I can feel my own hands.", "Dace died for it."))
        ok(flag("back_in_body"), "back_in_body")
        scene("cap_the_whole_memory", "Wake up.", ("twenty-four", "Your mouth on my cock", "None of us can be left", "I'll find you!"))
        scene("cap_cain_for_real", "Morning.", ("I don't hate you", "I'm choosing you anyway"))
        ok(flag("cain_chosen"), "cain_chosen")
        qt = play("QuestsPage")
        ok("That is where this build ends" in qt and "Chapter complete" in qt and "army of empty bodies" in qt, "end card O")
        ok("&amp;#x27;" not in qt and "&#x27;" not in qt, "no escaped apostrophes")
        ok("All but one." in qt, "Bastien's card 27 (Dace)")

        # ── what stands after
        at(14)
        t = play("Canvas_site_the_cradles_Node_base")
        ok("The second cradle is empty." in t and "Vega lies" not in t and "folded on his chair" in t, "day: the empty cradle, the folded blanket")
        at(22)
        t = play("Canvas_site_the_cradles_Node_base")
        ok("Cain is on the blanket between the cradles." in t and "Still here" not in t, "night: Cain her lover, not the waiting band")
        t = play("Location_the_site")
        ok(psg() == "Location_the_site", f"no 0.2.4 scene fires again on a later night ({psg()})")
        ok("Kess" not in [l.inner_text().strip() for l in links()], "Kess's Site card is gone with his row")
        t = play("Canvas_activity_cain_trains_Node_base")
        ok("I keep expecting you not to." in t, "Cain's card leads with the cain_chosen band")
        at(12)
        t = play("Location_kess_berth")
        ok("The wreck" in t, "the wreck card at Kess's berth")
        t = play("Canvas_kess_the_wreck_Node_base")
        ok("I'm learning her." in t, "the wreck, Kess present at noon")
        at(15)
        t = play("Canvas_amb_bastien_cot_Node_base")
        ok("One fewer on my books." in t and "Dace is very good" not in t and "Marrow's cradle" not in t, "Bastien's Dace band wins")
        # ── the 0.2.4 start jump, from a FRESH browser context, the way LO uses it. A fresh context, not a reload:
        # SugarCube restores the session on reload, and one-time scenes remember having fired, which no dev jump
        # resets. So the jump works on a new game; a save that already played 0.2.4 will not replay its one-shots.
        b.close()
        b = p.chromium.launch()
        pg = b.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL)
        pg.wait_for_function("window.SugarCube && SugarCube.State.variables.player", timeout=30000)
        play("Canvas_dev_jump_transfer_start_Node_seed")
        click("To the Site.")
        ok(psg() == "Location_the_site" and flag("cradles_ready") and not flag("study_blade"), f"the start jump lands at the Site at the end of 0.2.3 ({psg()})")
        ok("Vega's records" in text() and "The cradles" in text(), "the Site shows the reading card and the cradles card")
        at(22, 5)
        play("Location_the_site")
        ok(psg() == "Canvas_cap_study_blade_Node_base", f"study night 1 fires at 22:05 after the jump ({psg()})")
        qt = play("QuestsPage")
        ok("Read Vega's records" in qt, "card M is live after the jump")
        b.close()
    ok(not errs, f"js errors {errs[:3]}")
    print("LIVE THE TRANSFER: " + ("OK" if not fails else f"{len(fails)} FAILED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
