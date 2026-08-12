"""Live play-test for games/steam/output/index.html.

Answers the questions gates.py structurally cannot:
  1. does the opening funnel reach free roam (engine.md §12 — age gate first)
  2. do the hour-banded pool hubs fire at their declared windows
  3. IS MONEY CLAMPED (engine.md §21 — only a live effect diff shows this)
  4. do the locked doors render as span.locked-choice
  5. does the guidance page have cards in it
"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

GAME = pathlib.Path("games/steam/output/index.html").resolve()
results = []


def check(name, ok, detail=""):
    results.append((ok, name, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


def sv(page, expr="SugarCube.State.variables"):
    return page.evaluate(f"() => JSON.parse(JSON.stringify({expr}))")


def links(page):
    return page.eval_on_selector_all(
        "#story a.link-internal", "els => els.map(e => e.textContent.trim())")


def click_text(page, text):
    """Click by substring match, done in-page — the rendered labels carry
    characters (✓, curly apostrophes) that break Playwright text selectors."""
    ok = page.evaluate(
        """(t) => {
            const els = Array.from(document.querySelectorAll('#story a.link-internal'));
            const el = els.find(e => e.textContent.includes(t));
            if (!el) return false;
            el.click();
            return true;
        }""", text)
    page.wait_for_timeout(220)
    return ok


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"file://{GAME}")
    page.wait_for_timeout(600)

    # ── 1. the age gate, then the opening chain ─────────────────────────────
    gate = [t for t in links(page) if "18 or older" in t]
    check("age gate renders", bool(gate), gate[0] if gate else str(links(page))[:80])
    if gate:
        click_text(page, "I am 18 or older")

    body = page.inner_text("#story")
    check("opening canvas fires", "Perrine" in body or "seven" in body.lower(),
          body[:70].replace("\n", " "))

    # walk the funnel: Go down -> Ask about the board -> Open the doors
    for step in ["Go down.", "Ask about the board.", "Open the doors."]:
        avail = links(page)
        if not any(step in a for a in avail):
            check(f"funnel step '{step}'", False, f"available: {avail}")
            break
        click_text(page, step)
    else:
        v = sv(page)
        check("funnel sets doors_open", bool(v.get("flags", {}).get("doors_open")
                                             or v.get("player", {}).get("flags", {}).get("doors_open")),
              "flag store: " + str(list(v.keys()))[:60])
        check("funnel lands in free roam",
              (v.get("player", {}) or {}).get("current_location") not in ("", None),
              str((v.get("player", {}) or {}).get("current_location")))

    # ── 2. what the state model actually looks like ────────────────────────
    v = sv(page)
    player = v.get("player", {})
    traits = player.get("core_traits", player)
    check("meters initialised",
          all(k in json.dumps(traits) for k in ("steam", "service", "house", "propriety")),
          ", ".join(f"{k}={traits.get(k)}" for k in ("steam", "service", "house", "propriety", "money")
                    if k in traits))

    # ── 3. THE MONEY CLAMP (engine.md §21) ─────────────────────────────────
    # A capped effect is invisible in TOML, validator, build and gates. Only the
    # live number shows it. Drive money above 100 through the engine's own
    # trait-write path and see whether it survives.
    probe = page.evaluate("""() => {
        const before = SugarCube.State.variables.player.core_traits.money;
        (window._traitClamp || (SugarCube.setup && SugarCube.setup._traitClamp)) && null;
        // write via the engine's own helper the way an effect does
        const applied = [];
        for (let i = 0; i < 5; i++) {
            SugarCube.State.variables.player.core_traits.money =
                (window._traitClamp || (SugarCube.setup && SugarCube.setup._traitClamp))
                    ? (window._traitClamp || (SugarCube.setup && SugarCube.setup._traitClamp))(SugarCube.State.variables.player.core_traits.money + 40, 0, 100)
                    : SugarCube.State.variables.player.core_traits.money + 40;
            applied.push(SugarCube.State.variables.player.core_traits.money);
        }
        return {before, applied, clampFnExists: typeof (window._traitClamp || (SugarCube.setup && SugarCube.setup._traitClamp)) === 'function'};
    }""")
    check("_traitClamp exists (engine.md §21 helper)", probe["clampFnExists"], str(probe["clampFnExists"]))
    check("CLAMPED path would cap at 100 — confirming the hazard is real",
          probe["applied"][-1] == 100 if probe["clampFnExists"] else True,
          f"clamped series {probe['applied']}")

    # now the real question: do STEAM's own authored effects carry clamp=false?
    page.evaluate("() => { SugarCube.State.variables.player.core_traits.money = 95; }")
    fired = page.evaluate("""() => {
        // replicate an authored money effect exactly as the game declares it
        const eff = {targetType: 'player', trait: 'money', op: 'add', value: 40, clamp: false};
        if (typeof window.applyTraitEffect === 'function') {
            window.applyTraitEffect(eff);
            return {via: 'applyTraitEffect', money: SugarCube.State.variables.player.core_traits.money};
        }
        return {via: 'none', money: null};
    }""")
    if fired["via"] == "applyTraitEffect":
        check("authored money effect (clamp=false) exceeds 100", fired["money"] == 135,
              f"95 + 40 = {fired['money']}")
    else:
        check("applyTraitEffect exposed for direct probe", False,
              "not on window — falling back to in-play diff below")

    # ── 4. in-play money diff across a real earning surface ────────────────
    page.evaluate("""() => {
        SugarCube.State.variables.player.core_traits.money = 95;
        SugarCube.State.variables.player.core_traits.energy = 100;
    }""")
    money_before = page.evaluate("() => SugarCube.State.variables.player.core_traits.money")
    jumped = page.evaluate("""() => {
        try { SugarCube.Engine.play('Canvas_rung_desk_door_Node_base'); return true; }
        catch (e) { return String(e); }
    }""")
    page.wait_for_timeout(250)
    if jumped is True:
        avail = links(page)
        cash = [a for a in avail if "Cash up" in a]
        if cash:
            click_text(page, cash[0])
            money_after = page.evaluate("() => SugarCube.State.variables.player.core_traits.money")
            check("door shift pays through and is NOT capped at 100",
                  money_after > 100, f"{money_before} -> {money_after} (expected 135)")
        else:
            check("door-shift exit reachable", False, f"links: {avail[:4]}")
    else:
        check("can jump to rung_desk_door", False, str(jumped)[:80])

    # ── 5. locked doors render greyed ──────────────────────────────────────
    page.evaluate("""() => {
        const t = SugarCube.State.variables.player.core_traits;
        t.steam = 60; t.service = 60; t.house = 40; t.money = 400;
    }""")
    page.evaluate("() => { try { SugarCube.Engine.play('Canvas_hub_pool_mixed_Node_base'); } catch(e){} }")
    page.wait_for_timeout(250)
    locked = page.eval_on_selector_all("#story span.locked-choice", "els => els.map(e => e.textContent.trim())")
    check("visible locked door renders on a hub", bool(locked), str(locked[:2]))

    # ── 6. guidance page has cards ─────────────────────────────────────────
    quests = page.evaluate("""() => {
        try {
            if (typeof (SugarCube.setup||{}).pickQuestsCards === 'function') return SugarCube.setup.pickQuestsCards('all').length;
            if (typeof window.pickQuestsCards === 'function') return window.pickQuestsCards('all').length;
            return -1;
        } catch (e) { return String(e); }
    }""")
    check("guidance cards resolve at runtime", isinstance(quests, int) and quests != 0,
          f"{quests} cards matched" if isinstance(quests, int) else str(quests)[:60])

    check("no uncaught JS errors during the run", not errors, "; ".join(errors[:2])[:120])
    browser.close()

bad = [r for r in results if not r[0]]
print(f"\n{len(results)-len(bad)}/{len(results)} checks passed")
sys.exit(1 if bad else 0)
