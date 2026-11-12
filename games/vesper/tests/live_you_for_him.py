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

        def gc():
            return pg.evaluate("SugarCube.State.variables.npcs['npc_guard'].core_traits.corruption || 0")

        def next_day(h, m=0):
            pg.evaluate("window.advanceTime(1440)")
            at(h, m)

        arrivals_needed = []

        def test_day(where="Location_holding_cell"):
            """The day's test, automatic since 0279b: she arrives (at the cell, or the Post) between 09:00 and 12:00 and
            they come for her. Each arrival is an hour on, the way Wait moves the clock. Returns the labels the test's
            arrival offered, or [] if nobody came by noon. The arrivals it took go in arrivals_needed (the daily
            test is on the random path with the room's rest turned off, random_cooldown = 0)."""
            for k in range(3):
                at(9 + k)
                play(where)
                if psg().startswith("Canvas_") and "test" in psg():
                    break
            else:
                arrivals_needed.append(None)
                return []
            arrivals_needed.append(k + 1)
            offered = labels()
            if "Go with them." in offered:
                click("Go with them.")
                walk("Back to the cell.")
                click("Back to the cell.")
            return offered

        def ncorr(npc):
            return pg.evaluate(f"SugarCube.State.variables.npcs['{npc}'].core_traits.corruption || 0")

        def grind(man, npc, hub, hour, minute, key, steps, need, teases, tease_exits, rung_exits, drains, drain_exit):
            """The REWORK (beat 0279): climb one man to his first drain on HIS corruption. Each day: the test, then his
            hours; tease him until he wants the next step, take it, check no second step that day. The last step is
            the first fuck, and the drain works on it. Returns (days, teases spent)."""
            days = spent = 0
            for k in range(len(steps)):
                days += 1
                next_day(9)
                test_day()
                setv("energy", 100)
                at(hour, minute)
                play(hub)
                if k > 0:
                    ok(steps[k] not in labels() or ncorr(npc) >= need[k], f"{man} step {k}: refused below his corruption {need[k]} ({ncorr(npc)})")
                    while ncorr(npc) < need[k] and spent < 80:
                        best = [x for x in teases if x in labels()]
                        ok(bool(best), f"{man} step {k}: a tease on offer ({labels()})")
                        if not best:
                            break
                        before = ncorr(npc)
                        setv("energy", 100)
                        click(best[-1])
                        ex = next((e for e in tease_exits if e in labels()), None)
                        ok(ex is not None, f"{man}: '{best[-1]}' walks to its exit ({labels()})")
                        click(ex)
                        ok(ncorr(npc) > before, f"{man}: '{best[-1]}' raises his corruption ({before} to {ncorr(npc)})")
                        spent += 1
                        at(hour, minute)
                        play(hub)
                ok(steps[k] in labels(), f"{man} step {k}: '{steps[k]}' on offer ({labels()})")
                setv("energy", 100)
                click(steps[k])
                if k < len(steps) - 1:
                    ex = next((e for e in rung_exits if e in labels()), None)
                    ok(ex is not None, f"{man} step {k}: the rung walks to its exit ({labels()})")
                    click(ex)
                    ok(tr(key) == k + 1, f"{man}: {key} {k + 1} ({tr(key)})")
                    at(hour, minute)
                    play(hub)
                    ok(not [l for l in labels() if l in steps], f"{man} step {k}: no second step the same day ({labels()})")
            # the last step is the first fuck: the drain works the first time
            setv("drain_charge", 1)
            setv("equipped_weapon", 1)
            names = [l for l in labels() if "ass" in l.lower() or "bend" in l.lower() or "turn" in l.lower() or "face" in l.lower()]
            ok(bool(names), f"{man}: the loop offers her ass ({labels()})")
            click(names[0])
            for _ in range(12):
                fin = [l for l in labels() if l.startswith("Let him come in your ass")]
                if fin:
                    click(fin[0])
                    break
                click("Take it.")
            ok(not [l for l in labels() if "isn't yours yet" in l], f"{man}: no 'isn't yours yet' at the first fuck")
            ok("Take what he carries." in labels(), f"{man}: the first fuck, the drain is offered ({labels()})")
            click("Take what he carries.")
            ok(walk(drain_exit), f"{man}: the first drain walks to '{drain_exit}'")
            click(drain_exit)
            ok(tr(drains) == 1, f"{man}: {drains} 1")
            return days, spent

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
        next_day(8)
        play("Location_holding_cell")
        ok(psg() == "Location_holding_cell", f"08:00: nobody comes before nine ({psg()})")
        offered = test_day()
        ok(offered == ["Go with them."], f"day 1: they come for her, one choice, no button to refuse ({offered})")
        ok(tr("tests_done") == 1, "tests_done 1")
        at(11)
        play("Location_holding_cell")
        ok(psg() == "Location_holding_cell", f"the same day: no second test ({psg()})")
        ok(not [l for l in labels() if "test" in l.lower()], f"no tests card left in the cell ({labels()})")
        e0 = tr("energy")
        setv("drain_charge", 0)
        next_day(9)
        offered = test_day("Location_holding_floor")
        ok(psg() == "Location_holding_cell" and offered == ["Go with them."], "day 2: they come for her at the Post, and bring her back to the cell")
        ok(tr("tests_done") == 2 and tr("drain_charge") == 1, "the machine: tests_done 2, the drain charged")
        ok(tr("energy") <= e0, "a test costs energy")
        next_day(12)
        play("Location_holding_cell")
        ok(psg() == "Location_holding_cell", f"day 3 at noon: the window is shut, nobody comes ({psg()})")

        # ── 0279a: the cell's cot, the Berth cot's two tiers (half a charge any hour, the full night 19:00-05:00)
        rough_t, night_t = "Lie down a couple of hours. (Half a charge.)", "Sleep the night. (Full charge.)"
        setv("energy", 30)
        at(12)
        play("Canvas_activity_cell_sleep_Node_base")
        ok(rough_t in labels() and night_t not in labels(), f"the cot at noon: half a charge only ({labels()})")
        click(rough_t)
        ok(tr("energy") == 70, f"half a charge: +40 ({tr('energy')})")
        ok(click("Up.") and pg.evaluate(f"{TS}.current_hour") == 14, "a couple of hours: 120 min on the clock")
        at(21)
        play("Canvas_activity_cell_sleep_Node_base")
        ok(rough_t in labels() and night_t in labels(), f"the cot at night: both tiers ({labels()})")

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
        play("Location_holding_floor")
        ok(psg() == "Canvas_cap_guard_news_Node_base", f"the guard's news the next night, at the Post ({psg()})")
        ok("Went off the roof of his own building" in text(), "the line")
        click("Lie down.")
        ok(flag("mercer_dead"), "mercer_dead")
        at(23, 30)
        ok("npc_mercer" not in pg.evaluate("SugarCube.setup.getNpcsAtLocation('mercer_room')"), "Mercer is on no row")

        # ── part seven: the four men
        # 00:30, not 23:30: a rung begun before midnight ends after it and the next step opens the same night (the
        # midnight double-step, LO's call 3 signed 2026-11-10, Cain's loop has it too). Measured from after midnight.
        # ── the guard (the REWORK, beats 0275-0278): his corruption, filled by teases; one step a calendar day
        HUB = "Canvas_hub_guard_Node_base"
        STEPS = ["Let him watch you at the glass.", "Let him in.", "Get on your knees for him.", "Let him have you."]
        TEASES = ["Flash him.", "Show him everything at the glass.", "Touch yourself where he can see.", "Whisper what you'd do to him."]
        NEED = [0, 20, 45, 70]
        play("Location_holding_cell")
        ok("The Post" in text(), "the Post is on the cell's grid from the start")
        play("Location_holding_floor")
        t = text()
        ok("The Showers" in t and "The Test Lab" in t, "the block's rooms show on the Post's grid, locked")

        def tease(label):
            setv("energy", 100)
            before = gc()
            play(HUB)
            if not click(label):
                return None
            for _ in range(6):
                ex = [l for l in labels() if l in ("Walk away from him.", "Put the shift back on.", "Lie there for him.", "Leave him like that.")]
                if ex:
                    click(ex[0])
                    break
            return gc() - before

        days = 0
        for k in range(4):
            days += 1
            next_day(9)
            test_day()
            setv("energy", 100)
            at(12)
            play(HUB)
            if k > 0:
                ok(STEPS[k] not in labels() or gc() >= NEED[k], f"guard step {k}: refused below his corruption {NEED[k]} ({gc()})")
                spent = 0
                while gc() < NEED[k] and spent < 30:
                    best = [x for x in TEASES if x in labels()]
                    d = tease(best[-1])
                    ok(d and d > 0, f"guard: '{best[-1]}' raises his corruption ({d})")
                    spent += 1
                    at(12)
                    play(HUB)
                ok(gc() >= NEED[k], f"guard step {k}: teased to {NEED[k]} in {spent} teases ({gc()})")
                play(HUB)
            ok(STEPS[k] in labels(), f"guard step {k}: '{STEPS[k]}' on offer ({labels()})")
            setv("energy", 100)
            click(STEPS[k])
            if k < 3:
                ex = [l for l in labels() if l in ("Let him watch.", "Let him go.", "Wipe your mouth.")]
                ok(bool(ex), f"guard step {k}: the rung walks to its exit ({labels()})")
                click(ex[0])
                ok(tr("guard_step") == k + 1, f"guard_step {k + 1}")
                at(13)
                play(HUB)
                ok(not [l for l in labels() if l in STEPS], f"guard step {k}: no second step the same day ({labels()})")
            if k == 1:
                ok(tr("showers_door") == 1, "his hands open the showers")
                # the showers: his wash hour, his tease, then the curfew
                next_day(7, 10)
                play("Location_block_showers")
                ok("Wash alone" in text(), f"the showers' solo card ({labels()})")
                play("Canvas_hub_guard_showers_Node_base")
                before = gc()
                setv("energy", 100)
                click("Wash with the curtain open.")
                ok(gc() - before == 8, "the curtain open: +8")
                click("Turn the water off.")
                at(21)
                play("Location_block_showers")
                click("Wash alone")
                ok(psg() == "Canvas_activity_wash_alone_Node_base", f"before curfew the showers are hers ({psg()})")
                at(23)
                play("Location_block_showers")
                before = gc()
                click("Wash alone")
                ok(psg() == "Canvas_drag_back_showers_Node_base", f"after curfew he comes for her ({psg()})")
                click("Back in your cell.")
                ok(psg() == "Location_holding_cell" and gc() - before == -5, f"back in the cell, his corruption -5 ({gc() - before})")
            if k == 2:
                ok(tr("yard_door") == 1, "her knees open the laundry and the yard")
        # the fourth step is the first fuck, and the drain works the first time
        setv("drain_charge", 1)
        setv("equipped_weapon", 1)
        names = [l for l in labels() if "bend" in l.lower()]
        ok(bool(names), f"the loop offers her ass ({labels()})")
        click(names[0])
        for _ in range(12):
            fin = [l for l in labels() if l.startswith("Let him come in your ass")]
            if fin:
                click(fin[0])
                break
            click("Take it.")
        ok("Take what he carries." in labels(), f"the first fuck: the drain is offered ({labels()})")
        click("Take what he carries.")
        ok(walk("Get up."), "the first drain walks to 'Get up.'")
        click("Get up.")
        ok(tr("guard_drains_done") == 1 and tr("lab_door") == 1 and tr("guard_step") == 4, f"the guard is drained and the lab opens ({days} days)")
        at(23)
        play("Location_block_showers")
        click("Wash alone")
        ok(psg() == "Canvas_activity_wash_alone_Node_base", f"no curfew after his drain ({psg()})")
        ok(ncorr("npc_technician") >= 2 * days, f"every test so far wore on the technician ({ncorr('npc_technician')} after {days} days)")
        d, n = grind("technician", "npc_technician", "Canvas_hub_technician_Node_base", 22, 0, "tech_step",
                     ["Go to him.", "Get up on the table.", "Get on his table."], [0, 40, 75],
                     ["Undress for his cameras.", "Wire yourself up.", "Sit on his desk.", "Make him take a reading by hand."],
                     ["Put the shift back on.", "Peel the pads off.", "Get down off his desk.", "Let go of his wrist."],
                     ["Leave him with his screens.", "Leave him wanting it."], "tech_drains_done", "Take the code.")
        ok(tr("study_door") == 1, f"the technician is drained and Sabin's door opens ({d} days, {n} teases)")
        d, n = grind("Sabin", "npc_sabin", "Canvas_hub_sabin_study_Node_base", 18, 0, "sabin_step",
                     ["Let him see you.", "Ask him about his work.", "Tell him what it is.", "Clear his plans."], [0, 30, 45, 65],
                     ["Ask him to explain a drawing.", "Let him measure you.", "Tell him he's a genius.", "Kiss him while he talks."],
                     ["Let him roll it up.", "Step down.", "Leave him at the bench.", "Climb off him."],
                     ["Leave him staring.", "Leave him talking.", "Leave him wanting it."], "sabin_custody_drains", "Take the key.")
        ok(tr("records_door") == 1, f"Sabin is drained and the records room opens ({d} days, {n} teases)")
        d, n = grind("keeper", "npc_keeper", "Canvas_hub_keeper_Node_base", 21, 30, "keeper_step",
                     ["Sit with him.", "Make him look.", "Stay.", "Put his hands on you.", "Get on your knees for him.", "Lock the door."],
                     [0, 15, 30, 50, 70, 90],
                     ["Read with him.", "Undress at the far end of the table.", "Sit in his lap while he reads.", "Put his hand on you."],
                     ["Pull the shift back up.", "Get down off the table.", "Get up out of his lap.", "Let go of him."],
                     ["Leave him reading.", "Leave him looking.", "Leave him the chair.", "Leave him shaking.", "Leave him."],
                     "keeper_drains_done", "Go to the last cabinet.")
        ok(tr("keeper_drains_done") == 1, f"the keeper is drained ({d} days, {n} teases)")

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
    print(f"tests: arrivals needed per day {arrivals_needed}")
    ok(arrivals_needed and all(a == 1 for a in arrivals_needed), "every morning the test came on her first arrival from nine, the daily test included (random_cooldown = 0)")
    print("LIVE YOU, FOR HIM: " + ("OK" if not fails else f"{len(fails)} FAILED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
