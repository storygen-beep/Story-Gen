#!/usr/bin/env python3
"""
THE RINGS (0.2.2 addendum, rev 226) — LIVE guard, in the built game.

⚠️ WHY THIS EXISTS BESIDE check_bunker_route.py. That guard reads the TOML and can prove SHAPE: that the
ring is not bypassable, that the door man is paid for, that the two clock windows tile the day. It cannot
prove BEHAVIOUR, because the conditions are evaluated by JavaScript that only exists once the game is
built. Three of the rings' rules are behaviour and nothing else:

  * the slab's band and its locked choice are decided by `time_of_day`, which no static read can evaluate;
  * one wait must clear a four-hour round — a two-hour wait started at 21:00 ends at 23:00, still inside
    it, and the prose would be lying. That arithmetic is the engine's (setup.isCurrentTimeSlot +
    window.advanceTime), not ours;
  * the door man is dozing at `bunker_noise lt 1` and sitting up above it, which is only visible as a
    choice appearing and disappearing.

So this drives the real engine: it sets state and calls SugarCube.Engine.play, and every gate below is
decided by setup.triggerConditionsSatisfied, never re-implemented here.

⚠️ IT ONLY EVER CLICKS WHAT A PLAYER COULD CLICK. The whole story source sits in the DOM as
<tw-passagedata>, so a plain text locator happily "clicks" a hidden copy of a passage and proves nothing.
`click()` below filters to visible elements for that reason.

Needs playwright and a BUILT game:
    python manage.py package_from_toml --file games/vesper/toml_phases/7_final_game.toml \
      --output games/vesper/output_dev --video-folder games/vesper/videos --dev --debug
    python games/vesper/tests/live_rings.py
Exits 0 on pass, 1 on any failure.
"""
import json, pathlib, sys
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
        page.wait_for_function("typeof SugarCube !== 'undefined' && SugarCube.State.variables.player", timeout=30000)

        def seed(hour=21, minute=0, **traits):
            page.evaluate("""([hour, minute, traits]) => {
                const V = SugarCube.State.variables;
                V.game_state.time_state.current_hour = hour;
                V.game_state.time_state.current_minute = minute;
                Object.assign(V.player.core_traits, traits);
            }""", [hour, minute, traits])

        def flag(name, on=True):
            page.evaluate("([n,o]) => { SugarCube.State.variables.flags[n] = o; }", [name, on])

        def go(passage):
            page.evaluate("p => SugarCube.Engine.play(p)", passage)
            page.wait_for_timeout(250)

        def click(label):
            hit = page.evaluate("""label => {
                const vis = e => { const r = e.getBoundingClientRect();
                    return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; };
                const el = Array.from(document.querySelectorAll('#passages a, #passages button, #passages .choice, a, button'))
                    .filter(vis).find(e => (e.innerText || '').trim().includes(label));
                if (!el) return false;
                el.click();
                return true;
            }""", label)
            if not hit:
                raise AssertionError(f"no visible clickable says {label!r}")
            page.wait_for_timeout(350)

        def body():
            return page.inner_text("body")

        def links():
            return page.evaluate("""() => Array.from(document.querySelectorAll('a, button'))
                .map(e => e.innerText.trim()).filter(Boolean)""")

        def locked():
            return page.evaluate("""() => Array.from(document.querySelectorAll('[class*=lock], .choice-locked, .disabled'))
                .map(e => e.innerText.trim()).filter(Boolean)""")

        # ── RING 1 — the slab at 21:00, the round is walking ─────────────────
        print("\n[1] the slab, 21:00, nothing found yet")
        seed(21, 0)
        flag("bunker_seen", False)
        go("Canvas_bunker_descent_Node_base")
        t = body()
        check("two of them on it tonight" in t.lower(), "the patrol band renders at 21:00")
        check("nobody on the slab" not in t.lower(), "the clear band does NOT render at 21:00")
        allt = " | ".join(links() + locked())
        check("Lie up in the frame" in allt, "the wait option is offered")
        check("Two of them on the slab, walking it end to end" in body(),
              "'Down.' is locked WITH its reason (time_of_day has no engine-generated text)")
        click("Lie up in the frame")
        hm = page.evaluate("() => { const t = SugarCube.State.variables.game_state.time_state; return [t.current_hour, t.current_minute]; }")
        check(hm[0] == 1, f"one wait clears the four-hour round from 21:00 (clock now {hm[0]:02d}:{hm[1]:02d})")
        go("Canvas_bunker_descent_Node_base")
        check("nobody on the slab" in body().lower(), "and the plate is walkable when she comes back to it")

        # ── RING 1 — the same slab at 02:00 ─────────────────────────────────
        print("\n[2] the slab, 02:00, the round is off")
        seed(2, 0)
        go("Canvas_bunker_descent_Node_base")
        t = body()
        check("nobody on the slab" in t.lower(), "the clear band renders at 02:00")
        check("two of them on it tonight" not in t.lower(), "the patrol band does NOT render at 02:00")
        check("Lie up in the frame" not in " | ".join(links()), "the wait option is gone when there is no round")

        # ── RING 1 — once they have found a body ────────────────────────────
        print("\n[3] the slab, 21:00, after a body was found")
        seed(21, 0)
        flag("bunker_seen", True)
        go("Canvas_bunker_descent_Node_base")
        t = body()
        check("they found the one she left down there" in t.lower(), "the watched-round band renders")
        check("Lie up in the frame" not in " | ".join(links()), "waiting no longer works once bunker_seen is set")

        # ── the descent zeroes the run ──────────────────────────────────────
        print("\n[4] the per-run reset")
        seed(2, 0, bunker_stealth_used=1, bunker_noise=2)
        flag("bunker_seen", True)
        go("Canvas_bunker_descent_Node_base")
        click("Down.")
        tr = page.evaluate("() => SugarCube.State.variables.player.core_traits")
        check(tr.get("bunker_stealth_used") == 0, f"'Down.' zeroes the quiet budget (got {tr.get('bunker_stealth_used')})")
        check(tr.get("bunker_noise") == 0, f"'Down.' zeroes the noise (got {tr.get('bunker_noise')})")

        # ── RING 2 — the far gate ───────────────────────────────────────────
        print("\n[5] the far gate: the correct door lands on a posted man")
        seed(2, 0, stealth=60, fighting=60, bunker_stealth_used=0, bunker_noise=0)
        go("Canvas_bunker_route_Node_t3")
        check("far gate, past the wedge" in body().lower(), "t3 still offers the far gate")
        click("The far gate, past the wedge.")
        check("man on the gate" in body().lower() or "stool" in body().lower(),
              "the far gate now opens on the man, not on the three doors")
        l = " | ".join(links() + locked())
        check("Round the back of the racking" in l, "quiet answer offered at 60 stealth")
        check("Put him down" in l, "fight answer offered at 60 fighting")
        check("Back out" in l, "the way out of the building is always there")

        print("\n[6] the quiet pass spends the one quiet thing")
        click("Round the back of the racking")
        tr = page.evaluate("() => SugarCube.State.variables.player.core_traits")
        check(tr.get("bunker_stealth_used") == 1, "the quiet pass spent the budget")
        check(tr.get("bunker_noise") == 0, "the quiet pass made no noise")
        check("three doors" in body().lower() or "conduit" in body().lower(), "it came out at t4")

        # ── RING 3 — the last corridor ──────────────────────────────────────
        print("\n[7] t5 is the scout, and it counts three")
        go("Canvas_bunker_route_Node_t5")
        t = body().lower()
        check("man on a chair" in t, "the door man is seen through the corridor")
        check("book open on his forearm" in t, "the clerk is seen through the glass")
        check("Go up the corridor" in " | ".join(links()), "t5 opens onto the corridor, not the room")

        print("\n[8] the door man is dozing on a silent run, awake after noise")
        seed(2, 0, stealth=60, fighting=60, bunker_stealth_used=0, bunker_noise=0)
        go("Canvas_bunker_rings_Node_door")
        check("He has not moved in ten minutes" in " | ".join(links()),
              "silent run + 60 stealth + unspent budget: the quiet option is live")
        seed(2, 0, stealth=60, fighting=60, bunker_stealth_used=0, bunker_noise=1,
             arousal_charge=3, equipped_weapon=2, emitter_broken=0)
        flag("arousal_weapon_ready", True)
        go("Canvas_bunker_rings_Node_door")
        check("He has not moved in ten minutes" not in " | ".join(links()),
              "one body anywhere on the route and the quiet option is gone")
        check("He is sitting up now" in body(), "and it says why")
        check("Put him down." not in " | ".join(links()), "the fight is locked at 60 fighting (needs 70)")
        check("Put the field on him." in " | ".join(links()), "the emitter is the answer left")

        print("\n[9] the emitter spends a shot and hands on to the clerk")
        seed(2, 0, stealth=60, fighting=60, bunker_noise=1, arousal_charge=3, equipped_weapon=2, emitter_broken=0)
        flag("arousal_weapon_ready", True)
        go("Canvas_bunker_rings_Node_door")
        click("Put the field on him.")
        tr = page.evaluate("() => SugarCube.State.variables.player.core_traits")
        check(tr.get("arousal_charge") == 2, f"a shot was spent (got {tr.get('arousal_charge')})")
        check(tr.get("bunker_noise") == 2, f"the shot made noise (got {tr.get('bunker_noise')})")
        check(page.evaluate("() => !!SugarCube.State.variables.flags.bunker_seen"), "the slab will hear about it")
        check("cock" in body().lower(), "the scene is on the body, not around it")

        print("\n[10] the clerk, and into the room")
        go("Canvas_bunker_rings_Node_panel")
        check("book open on his forearm" in body().lower(), "the clerk has his back turned")
        click("Put him down before he turns round.")
        n_before = page.evaluate("() => SugarCube.State.variables.player.core_traits.bunker_noise")
        check(n_before == 2, f"the quiet kill costs no noise (still {n_before})")
        click("Look at the frame.")
        check("bastien is in it" in body().lower(), "the plant room opens on Bastien")
        for _ in range(4):                       # walk the cascade to the beat that was amended
            adv = page.evaluate("""() => {
                const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
                const el = Array.from(document.querySelectorAll('a, button')).filter(vis)
                    .find(e => /Look at the rest of it|The panel|He is awake/.test(e.innerText || ''));
                if (!el) return false; el.click(); return true; }""")
            page.wait_for_timeout(300)
            if not adv:
                break
        check("since the door came off its seal" in body().lower(),
              "and the prose knows she did not walk into an empty room")

        b.close()
    print("\n" + ("LIVE RINGS: OK" if not fails else f"LIVE RINGS: {len(fails)} FAILED"))
    for f in fails:
        print("  - " + f)
    return 1 if fails else 0

sys.exit(main())
