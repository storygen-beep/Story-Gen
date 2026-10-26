#!/usr/bin/env python3
"""
0.2.5 — THE FITTING — the whole chapter, live, end to end.

dev_jump_fitting_start (the end of 0.2.4) -> the strip is safe before the parts -> Kess fits strength, then
armour (the pain line) -> Cain's knife at the Site -> the blade -> Cain's loop over four nights (one new thing a
night: his mouth / her mouth / under him, then on top, then "Again.", then the ask) -> card T -> Lyra and Nova on
the strip by a real entry -> the first loss carries her to the Site -> the ending -> end card U -> a later loss is
the lost day home to the cot -> Kess's repair says "they".

Shortcuts, stated: the run starts from the 0.2.5 dev jump (the end of 0.2.4 is played for real by
live_the_transfer.py); the clock moves only through advanceTime or by setting the hour before an entry; the
random roll is pinned by stubbing Math.random to 0 for the strip entries, so "she walks onto the strip and they
are there" is a real entry and not an Engine.play of the scene.

Run from the repo root against output_dev (built --dev):
    python games/vesper/tests/live_the_fitting.py
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

        def text():
            return pg.inner_text("#passages")

        def at(h, m=0):
            pg.evaluate(f"{TS}.current_hour={h}; {TS}.current_minute={m}")

        def mins():
            return pg.evaluate(f"{TS}.current_hour*60+{TS}.current_minute")

        def play(passage):
            pg.evaluate(f"SugarCube.Engine.play('{passage}')")
            pg.wait_for_timeout(300)
            return text()

        def links():
            return [l for l in pg.query_selector_all("#passages a") if l.is_visible()]

        def labels():
            # The --debug build draws a media-finder link (🔍) for every missing image; those are not choices.
            return [l.inner_text().strip() for l in links() if not l.inner_text().strip().startswith("🔍")]

        def click(t):
            el = [l for l in links() if l.inner_text().strip() == t]
            if not el:
                return False
            el[0].click()
            pg.wait_for_timeout(300)
            return True

        def walk(exit_text):
            for _ in range(40):
                if exit_text in labels():
                    return True
                ls = links()
                if not ls:
                    return False
                ls[-1].click()
                pg.wait_for_timeout(150)
            return False

        def next_day(h):
            pg.evaluate("window.advanceTime(1440)")
            at(h)

        def strip_entry():
            """A real entry onto the strip with the random roll pinned to 0 (it always succeeds when eligible)."""
            pg.evaluate("window.__rnd = Math.random; Math.random = function(){ return 0; }")
            play("Location_underworld_strip")
            pg.evaluate("Math.random = window.__rnd")
            return psg()

        def fit(price, exit_text):
            at(12)
            play("Canvas_hub_kess_berth_Node_base")
            ok("Have him fit the next part." in labels(), f"Kess's card offers the fitting (before the {price})")
            click("Have him fit the next part.")
            pays = [l for l in labels() if l.startswith("Pay him.")]
            ok(pays == [f"Pay him. ({price} coin.)"], f"exactly one price on the bench: {price} (got {pays})")
            c0, m0 = tr("coin"), mins()
            click(f"Pay him. ({price} coin.)")
            ok(walk(exit_text), f"the {price} session walks to '{exit_text}'")
            t = text()
            click(exit_text)
            ok(tr("coin") == c0 - price, f"{price} coin paid ({c0} -> {tr('coin')})")
            # 240 on the exit, plus the engine's minute per cascade click.
            ok(240 <= mins() - m0 <= 250, f"the session takes four hours ({mins() - m0} min)")
            return t

        pg.goto(URL)
        pg.evaluate("localStorage.clear()")
        pg.reload()
        pg.wait_for_function("window.SugarCube && SugarCube.State.variables.player", timeout=30000)

        # ── the start: the 0.2.5 jump
        play("Canvas_dev_jump_fitting_start_Node_seed")
        click("To the Berth.")
        ok(psg() == "Location_kess_berth" and flag("cain_chosen") and not flag("in_vega"), f"the jump lands at the Berth after 0.2.4 ({psg()})")
        qt = play("QuestsPage")
        ok("three things in it that can go into you" in qt and "Chapter complete" not in qt, "card S (the fitting) is live")
        ok("taking out what can go into you" in qt, "Kess's card: the fitting")

        # ── the strip is safe before the parts
        at(14)
        ok(strip_entry() != "Canvas_rand_units_street_Node_base", "no hunt on the strip before the three parts")

        # ── strength, armour
        t = fit(40, "Put it down.")
        ok("It's not even heavy." in t, "strength: she lifts the pump housing")
        ok(tr("parts_fitted") == 1, "parts_fitted 1")
        t = play("Canvas_kess_the_wreck_Node_base")
        ok("Her back is open and empty" in t and "the blade folded inside it" not in t, "the wreck shows the back gone")
        t = fit(60, "Sit up.")
        ok("She never did that." in t and "can't build is the bit of you that just flinched" in t, "armour: Kess sees the pain and says it")
        ok(tr("parts_fitted") == 2, "parts_fitted 2")

        # ── the knife, at the Site, the first night Cain is there
        at(21, 30)
        play("Location_the_site")
        ok(psg() == "Canvas_cap_the_knife_Node_base", f"cap_the_knife fires at the Site with Cain there ({psg()})")
        ok(walk("Stay with him."), "the knife scene walks through")
        t = text()
        ok("They can't make you once." in t, "Cain: they can't make you once")
        click("Stay with him.")
        ok(flag("knife_tested"), "knife_tested")
        play("Location_the_site")
        ok(psg() == "Location_the_site", "the knife does not fire twice")

        # ── the blade
        next_day(12)
        t = fit(80, "Get up.")
        ok("It's actually mine." in t, "the blade: it's hers")
        ok(tr("parts_fitted") == 3, "parts_fitted 3")
        play("Canvas_hub_kess_berth_Node_base")
        hub_labels = labels()
        ok("Have him fit the next part." not in hub_labels, "nothing left to fit: the choice is gone")
        ok(len(hub_labels) <= 8, f"Kess's card shows at most 8 things at once in play ({len(hub_labels)}: {hub_labels})")
        t = play("Canvas_kess_the_wreck_Node_base")
        ok("A shell now." in t and "I keep her for the spares." in t, "the wreck is a shell; Kess keeps it for spares")
        qt = play("QuestsPage")
        ok("they are looking for you" in qt and "three things in it" not in qt, "card T replaces card S")
        ok("Three of Vega's parts are in you now" in qt, "Kess's after-the-fitting card")

        # ── Cain's nights: one new thing a night
        def lie_down():
            play("Canvas_activity_cain_trains_Node_base")
            n = labels().count("Lie down with him.")
            ok(n == 1, f"exactly one 'Lie down with him.' on his card (got {n})")
            click("Lie down with him.")
            return labels()

        def finish(pose_label, act, finish_label):
            click(pose_label)
            for _ in range(12):
                if finish_label in labels():
                    break
                click(act)
            ok(finish_label in labels(), f"'{finish_label}' opens once he is close")
            click(finish_label)
            return labels()

        # Night 1 starts at 21:00 so the loop's two hours end before midnight and the same-day re-entry below is
        # really the same calendar day (the ladder steps on days_since_flag cain_lay, a calendar-day count).
        at(21)
        t = play("Canvas_activity_cain_trains_Node_base")
        ok("Show me." in t, "Cain's card leads with the blade band")
        intro = lie_down()
        ok(tr("cain_nights") == 1, "night 1")
        ok("Get on top of him." not in intro and "Ask him for it." not in intro, "night 1: no on top, no ask")
        ok({"Let him put his mouth on you.", "Take him in your mouth.", "Let him have you."} <= set(intro), "night 1: his mouth, her mouth, under him")
        fl = finish("Take him in your mouth.", "Suck him.", "Let him come in your mouth.")
        ok("Again." not in fl, "night 1: no second round")
        click("Lie with him.")
        ok(psg() == "Location_the_site", "back to the Site")
        ok(all(tr(k) == 0 for k in ("loop_npc_pleasure", "sex_stage", "sex_finisher_type", "cain_round")), "the loop traits reset on the way out")
        ok(pg.evaluate(f"{TS}.current_hour") == 23, "night 1 ended before midnight")
        lie_down()
        ok(tr("cain_nights") == 1, "the same day again does not step the ladder")
        click("Take him in your mouth.")
        fl = finish("Take him in your mouth.", "Suck him.", "Let him come in your mouth.")
        click("Lie with him.")
        next_day(22)
        intro = lie_down()
        ok(tr("cain_nights") == 2 and "Get on top of him." in intro, "night 2: on top opens")
        fl = finish("Get on top of him.", "Ride him.", "Let him finish inside you.")
        click("Lie with him.")
        next_day(22)
        lie_down()
        fl = finish("Let him have you.", "Take it.", "Let him finish inside you.")
        ok(tr("cain_nights") == 3 and "Again." in fl, "night 3: 'Again.' on the finisher")
        click("Again.")
        ok(psg() == "Canvas_loop_cain_site_Node_again", "the second round")
        fl = finish("Get on top of him.", "Ride him.", "Let him finish inside you.")
        ok("Again." not in fl, "only one second round a sitting")
        click("Lie with him.")
        next_day(22)
        intro = lie_down()
        ok(tr("cain_nights") == 4 and "Ask him for it." in intro, "night 4: the ask")
        click("Ask him for it.")
        ok(walk("Ride him."), "the ask walks to the act")
        t = text()
        ok("I want your cock in me." in t and "the first thing that was mine" in t, "she asks; the meaning comes after")
        ok(tr("cain_asked") == 1, "cain_asked")
        fl = finish("Ride him.", "Ride him.", "Let him finish inside you.")
        t = text()
        ok("Mine. I asked for that." in t, "the finish after the ask is hers")
        click("Lie with him.")
        next_day(22)
        intro = lie_down()
        ok("Ask him for it." not in intro and "Say you heard me." in text(), "after the ask: no second ask; she says it every time")
        click("Take him in your mouth.")
        ok(not [w for w in text().split() if w.strip('.,').lower() in ("ass", "anal")], "no anal word in the loop")

        # ── the hunt: a real entry, the first loss, the ending
        at(14)
        ok(strip_entry() == "Canvas_rand_units_street_Node_base", f"Lyra and Nova on the strip ({psg()})")
        t = text()
        ok("Lyra and Nova" in t and "For a whole minute she is winning." in t, "the first fight: two of them, and she holds them a minute")
        ok(labels() == ["Run."], f"the only choice is Run ({labels()})")
        d0 = tr("vega_damage")
        click("Run.")
        click("Let him carry you.")
        ok(tr("vega_damage") >= 60, f"the first loss leaves her Badly hurt ({d0} -> {tr('vega_damage')})")
        ok(flag("units_first_loss"), "units_first_loss")
        ok(psg() == "Canvas_cap_more_coming_Node_base", f"the ending fires at the Site ({psg()})")
        ok(walk("Sleep."), "the ending walks through")
        t = text()
        ok("Bastien's men saw them" in t and "There'll be twenty, and then two hundred." in t and "can't make" in t, "Cain: why he came, the line, what she is")
        click("Sleep.")
        ok(flag("more_coming"), "more_coming")
        qt = play("QuestsPage")
        ok(qt.count("Chapter complete") == 1 and "That is where this build ends" in qt and "still hunting you" in qt, "end card U, once")
        ok("&amp;#x27;" not in qt and "&#x27;" not in qt, "no escaped apostrophes")

        # ── after the end: a later loss is the lost day home to the cot; Kess's repair says "they"
        # The engine skips a few visits after a random scene fires (game_state.random_cooldowns, per visit, not per
        # day), so walk on and off the strip until they come.
        next_day(14)
        hit = False
        for _ in range(8):
            if strip_entry() == "Canvas_rand_units_street_Node_base":
                hit = True
                break
            play("Location_the_site")
        ok(hit, "they still hunt her after the end card")
        ok("She knows the shape of it now" in text(), "the later-fight band")
        click("Run.")
        click("Home.")
        ok(psg() == "Location_the_cot" and tr("vega_damage") == 100, f"a later loss: home to the cot, damage clamped at 100 ({psg()}, {tr('vega_damage')})")
        play("Location_the_site")
        ok(psg() == "Location_the_site", "the ending does not fire twice")
        next_day(12)
        play("Canvas_hub_kess_berth_Node_base")
        ok("Have him fix what they did." in labels() and "Have him fix what she did." not in labels(), "the repair says 'they'")
        click("Have him fix what they did.")
        ok("Two of them did this." in text(), "Kess: two of them did this")
        click("Pay him. (10 coin.)")
        ok("Tell them that." in text() and "Tell her that." not in text(), "her answer names them")
        b.close()
    ok(not errs, f"js errors {errs[:3]}")
    print("LIVE THE FITTING: " + ("OK" if not fails else f"{len(fails)} FAILED"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
