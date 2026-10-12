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
        scene("cap_the_transfer", "Go.", ("Fuck me. It worked.", "I'm still scared, Cain."))
        ok(flag("transferred") and flag("in_vega") and flag("rise_door") and not flag("face_worn"), "in Vega: in_vega + rise_door set, the bought face off")
        ok(tr("vega_cell") == 100, f"Vega's cell full ({tr('vega_cell')})")

        # ── THE PLAYER PLAYS VEGA: by nav links and card links, the way a player does ──
        def nav(name):
            """Click a nav card by its location name (enabled cards only)."""
            el = [l for l in links() if name in l.inner_text() and not l.get_attribute("disabled")]
            if not el:
                return False
            el[0].click()
            pg.wait_for_timeout(400)
            return True

        def side():
            return pg.inner_text("#ui-bar")

        ok(psg() == "Location_the_site", f"the transfer drops into free play at the Site ({psg()})")
        t = text()
        ok("Your body" in t, "the Site: Vega's card")
        click("Leave The Site")
        ok(psg() == "Location_underworld_strip" and "Not in this body." in text() and "Go back" in text()
           and "The House" not in text(), "the strip is shut to Vega: its message and Go back, none of Wren's places")
        click("Go back")
        ok(psg() == "Location_the_site", f"Go back returns her to the Site ({psg()})")
        ok("Vega's records" not in t and "The cradles" not in t, "Wren's Site cards are closed in Vega")
        ok("Vega's cell: full" in side() and "Charge:" not in side(), "sidebar: Vega's cell shows, Wren's Charge does not")
        click("Your body")
        ok("Her own body lies in her cradle" in text(), "Vega's card at the Site")
        click("Out to the gate.")
        click("Out at the gate.")
        ok(psg() == "Location_underworld_gate", f"at the gate ({psg()})")
        t = text()
        ok("The man at the door" in t and "Take the car" not in t, "the gate: Vega's card only (Wren's car and toll are closed)")
        click("The man at the door")
        ok("goes flat against the wall" in text(), "the doorman steps back from the company's face")
        click("Ride up to the Spire.")
        click("Out on the plaza.")
        ok(psg() == "Location_spire_plaza", f"on Spire Plaza ({psg()})")
        ok(nav("The Second Tower"), "the Rise's door is open to Vega")
        ok(psg() == "Location_the_rise_floor", f"on the Rise floor ({psg()})")
        # before eight: Sabin is not on the floor yet, so the lab is locked with the reason
        if hour() < 8:
            click("Sabin's lab")
            ok("Come back in the morning" in text() and not click("Up to his lab."), "before eight the lab is locked, with the reason")
            click("Not now.")
        cur = pg.evaluate(f"{TS}.current_hour*60+{TS}.current_minute")
        pg.evaluate(f"window.advanceTime({(9 * 60 - cur) % 1440})")
        play("Location_the_rise_floor")
        click("Sabin's lab")
        ok(click("Up to his lab."), "at nine, with Sabin on the floor, the lab opens")
        walk("Back down to the floor.")
        ok("He's downstairs until eleven" in text() and "Vance Tower" in text(), "the lab: empty because he is downstairs; the slip names Vance Tower")
        click("Back down to the floor.")
        ok(flag("rise_slip"), "rise_slip")
        ok(psg() == "Location_the_rise_floor", "back on the floor, no look yet (the top floors are still to see)")
        click("The top floors")
        click("Ride to the top.")
        walk("Back down.")
        ok("This is the eleven thousand." in text(), "the production floor")
        click("Back down.")
        ok(tr("vega_cell") == 90, f"the top floors cost 10 of the cell ({tr('vega_cell')})")
        scene("cap_sabin_notices", "Out onto the plaza.", ("You never look at anybody.", "I'll make a note."))
        ok(flag("rise_searched") and psg() == "Location_spire_plaza", "Sabin's look, then out on the plaza")
        qt = play("QuestsPage")
        ok("Chairman's vault in Vance Tower" in qt and "He made a note." in qt, "card Q, and Sabin's new card")
        play("Location_spire_plaza")
        click("Take the car")
        click("Down to the gate.")
        click("Out at the gate.")
        click("The man at the door")
        click("Back to the Site.")
        click("Back to the Site.")
        ok(psg() == "Location_the_site", f"home by the service way ({psg()})")
        cur = pg.evaluate(f"{TS}.current_hour*60+{TS}.current_minute")
        pg.evaluate(f"window.advanceTime({(22 * 60 + 5 - cur) % 1440})")
        play("Location_the_site")
        scene("cap_tower_plan", "Go.", ("Of course it's the bloody Tower.", "Bastien's men and I will be waiting there."))
        ok(flag("tower_planned") and tr("vega_cell") == 100, "the plan; the cell topped up")
        # the Tower at night, walked
        click("Your body")
        click("Out to the gate.")
        click("Out at the gate.")
        click("The man at the door")
        click("Ride up to the Spire.")
        click("Out on the plaza.")
        ok(nav("The Atrium"), "into the Atrium")
        ok(22 <= hour() or hour() < 4, f"it is night ({hour()})")
        ok(nav("The Chairman's Floor"), "the Chairman's floor opens to Vega after the plan, at night")
        ok(psg() == "Canvas_cap_the_vault_Node_base", f"cap_the_vault fires on the Chairman's floor ({psg()})")
        walk("Step back. Wait for the change.")
        click("Step back. Wait for the change.")
        ok(psg() == "Canvas_cap_the_vault_Node_wait" and "two fresh men" in text(), "the wait branch: a fresh pair, the same door")
        click("Turn the wrist down.")
        ok(tr("vega_cell") == 70, f"the blade costs 30 of the cell ({tr('vega_cell')})")
        walk("Go in.")
        ok("You're one of ours." in text(), "the blade node renders")
        click("Go in.")
        walk("Run.")
        ok("Vesper" in text() and "Don't open it." in text(), "the vault: her drawer, carried out unopened")
        click("Run.")
        ok(psg() == "Canvas_cap_lyra_and_nova_Node_base", f"Lyra and Nova fire on Spire Plaza ({psg()})")
        scene("cap_lyra_and_nova", "Don't let go.", ("Lyra and Nova", "shut her signal off"))
        scene("cap_dace_falls", "Home.", ("Not her. Go on. Not her.", "I did not think I would pay for his."))
        ok(flag("dace_dead"), "dace_dead")
        scene("cap_back_in_body", "Remember.", ("I can feel my own hands.", "Dace died for it."))
        ok(flag("back_in_body") and not flag("in_vega"), "back_in_body; out of Vega")
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
