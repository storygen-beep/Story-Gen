"""Live test for 0.2.6 YOU, FOR HIM (design_the_offer.md BLUEPRINT, beats 0263-0274).

Plays the whole chapter headless against output_dev/index.html (build with --dev --debug first), from the
"0.2.6: start" dev jump: the night nobody comes, the wrecked Site, Mercer's offer, the answer and its warning, the
Chairman, the tests (one a day, the charge refill), Mercer's last visit and the guard's news, the four men in order
(guard, technician, Sabin, the keeper; one step a calendar day; the drain only at the top of each ladder; each drain
opens the next door), and the wife's file with end card AB. Energy is topped up by hand between nights so the run
measures the ladders, not the meter; the meter itself is checked once.
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
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "Failed to load resource" not in m.text else None)

        def flag(f):
            return pg.evaluate(f"(function(){{var F=SugarCube.State.variables.flags; return Array.isArray(F)?F.includes('{f}'):!!F['{f}'];}})()")

        def tr(k):
            return pg.evaluate(f"{CT}.{k}")

        def setv(k, v):
            pg.evaluate(f"{CT}.{k}={v}")

        def psg():
            return pg.evaluate("SugarCube.State.passage")

        def text():
            return pg.inner_text("#passages")

        def at(h, m=0):
            pg.evaluate(f"{TS}.current_hour={h}; {TS}.current_minute={m}")

        def play(passage):
            pg.evaluate(f"SugarCube.Engine.play('{passage}')")
            pg.wait_for_timeout(250)
            return text()

        def links():
            return [l for l in pg.query_selector_all("#passages a") if l.is_visible()]

        def labels():
            return [l.inner_text().strip() for l in links() if not l.inner_text().strip().startswith("🔍")]

        def click(t):
            el = [l for l in links() if l.inner_text().strip() == t]
            if not el:
                return False
            el[0].click()
            pg.wait_for_timeout(250)
            return True

        def walk(exit_text):
            for _ in range(40):
                if exit_text in labels():
                    return True
                ls = [l for l in links() if not l.inner_text().strip().startswith("🔍")]
                if not ls:
                    return False
                ls[-1].click()
                pg.wait_for_timeout(120)
            return False

        def next_day(h, m=0):
            pg.evaluate("window.advanceTime(1440)")
            at(h, m)

        def test_day():
            """The day's test, from the cell's card. Returns the label set offered first."""
            at(10)
            play("Canvas_activity_the_tests_Node_base")
            offered = labels()
            if "Go with them." in offered:
                click("Go with them.")
                walk("Back to the cell.")
                click("Back to the cell.")
            return offered

        def ladder(man, hub, hour, minute, loop_label, drains, top, rung_exits, drain_exit):
            """Climb one man to his first drain, one step per calendar day. Returns the number of nights it took."""
            nights = 0
            for _ in range(top + 4):
                nights += 1
                next_day(9)
                test_day()
                setv("energy", 100)
                at(hour, minute)
                play(hub)
                ls = labels()
                if loop_label in ls:
                    click(loop_label)
                    names = [l for l in labels() if "ass" in l.lower() or "bend" in l.lower() or "turn" in l.lower() or "face" in l.lower()]
                    click(names[0])
                    for _ in range(12):
                        fin = [l for l in labels() if l.startswith("Let him come in your ass")]
                        if fin:
                            click(fin[0])
                            break
                        click("Take it.")
                    if "Take what he carries." in labels():
                        click("Take what he carries.")
                        ok(walk(drain_exit), f"{man}: the first drain walks to '{drain_exit}'")
                        click(drain_exit)
                        return nights
                    notyet = [l for l in labels() if l.startswith("Let it go. He isn't yours yet")]
                    ok(bool(notyet), f"{man}: before the top of his ladder the ass finish does not drain ({labels()})")
                    click(notyet[0])
                else:
                    step = [l for l in ls if l not in ("Turn your back on him.", "Not tonight.")]
                    ok(len(step) == 1, f"{man}: exactly one step on offer on night {nights} ({ls})")
                    click(step[0])
                    ex = next((e for e in rung_exits if e in labels()), None)
                    ok(ex is not None, f"{man}: the rung on night {nights} walks to its exit")
                    click(ex)
                    # same night again: no second step
                    play(hub)
                    ok(not [l for l in labels() if l not in ("Turn your back on him.", "Not tonight.", loop_label)],
                       f"{man}: the same night offers no second step ({labels()})")
            return nights

        pg.goto(URL)
        pg.evaluate("localStorage.clear()")
        pg.reload()
        pg.wait_for_function("window.SugarCube && SugarCube.State.variables.player", timeout=30000)

        # ── the start: the 0.2.6 jump
        play("Canvas_dev_jump_offer_start_Node_seed")
        click("To the cot.")
        ok(psg() == "Location_the_cot" and flag("more_coming") and not flag("cain_taken"), f"the jump lands at the cot after 0.2.5 ({psg()})")
        qt = play("QuestsPage")
        ok("Walk the strip at night" in qt and "Chapter complete" not in qt, "card U is live and no longer terminal")

        # ── part one: the night nobody comes
        at(14)
        play("Location_underworld_strip")
        ok(psg() != "Canvas_rand_units_no_show_Node_base", "nobody-comes does not fire by day")
        at(21, 30)
        play("Location_underworld_strip")
        ok(psg() == "Canvas_rand_units_no_show_Node_base", f"at night the hunt does not come ({psg()})")
        click("Run to the Site.")
        ok(psg() == "Canvas_cap_site_wrecked_Node_base", f"the wrecked Site fires on arrival ({psg()})")
        ok("her designation" in text().lower() or "designation" in text(), "the sign on his bench")
        click("Go home.")
        ok(flag("cain_taken") and psg() == "Location_the_cot", "cain_taken, home to the cot")
        at(22)
        ok("npc_cain" not in pg.evaluate("SugarCube.setup.getNpcsAtLocation('the_site')"), "Cain is on no row")
        ok("Somebody will come for you in the morning" in play("QuestsPage"), "card V")

        # ── part two: the offer, the answer
        next_day(7)
        play("Location_the_cot")
        ok(psg() == "Canvas_cap_mercer_brings_offer_Node_base", f"Mercer at the cot in the morning ({psg()})")
        ok("You, for him." in text(), "the offer in his words")
        click("Sit with it.")
        ok(flag("offer_made") and flag("mercer_found"), "offer_made + mercer_found")
        ok("Give him your answer there" in play("QuestsPage"), "card W")
        at(23, 30)
        play("Canvas_hub_mercer_room_Node_base")
        ok("Give him your answer." in labels(), f"his room offers the answer ({labels()})")
        click("Give him your answer.")
        ok("Once you go in, the city is closed until the next release." in text(), "the plain warning")
        setv("equipped_weapon", 2)
        click("Go with him.")
        ok(flag("in_custody") and tr("equipped_weapon") == 1, "in_custody, and the drain is what she carries in")

        # ── part five: the Chairman
        ok(psg() == "Canvas_cap_chairman_talk_Node_base", f"the Chairman's room fires the talk ({psg()})")
        ok("Sit. You've been running a long time." in text(), "line 1")
        click("Look at him.")
        t = text()
        ok("I want to know how it was put in you. All of it." in t and "That's not a question you get to ask yet." in t and "Ask Mr. Mercer." in t and "Try to be useful." in t, "lines 3-6")
        click("Go down with them.")
        ok(psg() == "Location_holding_cell" and flag("chairman_met"), f"down to the cell ({psg()})")
        cell = text()
        ok("All locations" not in cell and "Waterfront" not in cell and "The Underground" not in cell, "the cell is sealed: no city on its grid")

        # ── part six: the tests, one a day
        offered = test_day()
        ok(offered.count("Go with them.") == 1, f"one test on offer on day 1 ({offered})")
        ok(tr("tests_done") == 1, "tests_done 1")
        play("Canvas_activity_the_tests_Node_base")
        ok(labels() == ["Wait for the night."], f"the same day: no second test ({labels()})")
        e0 = tr("energy")
        setv("drain_charge", 0)
        next_day(9)
        test_day()
        ok(tr("tests_done") == 2 and tr("drain_charge") == 1, "the machine: tests_done 2, the drain charged")
        ok(tr("energy") <= e0, "a test costs energy")

        # ── part four: Mercer's last visit, the guard's news
        at(20, 30)
        play("Location_holding_cell")
        ok(psg() == "Canvas_cap_mercer_last_visit_Node_base", f"Mercer comes to the glass ({psg()})")
        ok("Take him at the finish." in labels() and "Let him." in labels(), "let him / drain him")
        click("Let him.")
        walk("Let him go back up.")
        click("Let him go back up.")
        ok(flag("mercer_last_visit"), "mercer_last_visit")
        next_day(0, 30)
        play("Location_holding_cell")
        ok(psg() == "Canvas_cap_guard_news_Node_base", f"the guard's news the next night ({psg()})")
        ok("Went off the roof of his own building" in text(), "the line")
        click("Lie down.")
        ok(flag("mercer_dead"), "mercer_dead")
        at(23, 30)
        ok("npc_mercer" not in pg.evaluate("SugarCube.setup.getNpcsAtLocation('mercer_room')"), "Mercer is on no row")

        # ── part seven: the four men
        # 00:30, not 23:30: a rung begun before midnight ends after it and the next step opens the same night (the
        # midnight double-step, LO's call 3 signed 2026-11-10, Cain's loop has it too). Measured from after midnight.
        n = ladder("guard", "Canvas_hub_guard_Node_base", 0, 30, "Let him have you.", "guard_drains_done", 6,
                   ["Let him watch.", "Let him go.", "Wipe your mouth."], "Get up.")
        ok(tr("guard_drains_done") == 1 and tr("floor_door") == 1, f"the guard is drained and the floor opens ({n} nights)")
        play("Location_holding_cell")
        ok("The Floor at Night" in text(), "the floor is on the cell's grid")
        n = ladder("technician", "Canvas_hub_technician_Node_base", 22, 30, "Get on his table.", "tech_drains_done", 4,
                   ["Leave him with his screens.", "Leave him wanting it."], "Take the code.")
        ok(tr("tech_drains_done") == 1 and tr("study_door") == 1, f"the technician is drained and Sabin's door opens ({n} nights)")
        n = ladder("Sabin", "Canvas_hub_sabin_study_Node_base", 19, 0, "Clear his plans.", "sabin_custody_drains", 4,
                   ["Leave him staring.", "Leave him talking.", "Leave him wanting it."], "Take the key.")
        ok(tr("sabin_custody_drains") == 1 and tr("records_door") == 1, f"Sabin is drained and the records room opens ({n} nights)")
        n = ladder("keeper", "Canvas_hub_keeper_Node_base", 21, 30, "Lock the door.", "keeper_drains_done", 7,
                   ["Leave him reading.", "Leave him looking.", "Leave him the chair.", "Leave him shaking.", "Leave him."], "Go to the last cabinet.")
        ok(tr("keeper_drains_done") == 1, f"the keeper is drained ({n} nights)")

        # ── part eight: the file
        ok(psg() == "Canvas_cap_the_wifes_file_Node_base", f"the file fires in the records room ({psg()})")
        ok(walk("Close the file."), "the file walks through")
        t = text()
        ok("subject did not survive transfer" in t and "A. Vance" in t and "a transfer can be survived" in t.lower() or "I did it." in t, "what the file says")
        click("Close the file.")
        ok(flag("wife_file_read"), "wife_file_read")
        qt = play("QuestsPage")
        ok(qt.count("Chapter complete") == 1 and "That is where this build ends" in qt, "end card AB, once")
        ok("&#x27;" not in qt, "no escaped apostrophes")
        b.close()
    ok(not errs, f"js errors {errs[:3]}")
    print("LIVE YOU, FOR HIM: " + ("OK" if not fails else f"{len(fails)} FAILED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
