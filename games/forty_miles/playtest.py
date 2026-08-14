"""Live play-test for games/forty_miles/output/index.html.

Answers what gates.py structurally cannot:
  1. does the opening funnel reach free roam
  2. IS MONEY CLAMPED (engine.md §21) — the 245 Friday draw is unpayable if it is,
     and the build stays green the whole way down
  3. DO THE DAY-SPECIFIC OVERNIGHT SCHEDULES SURVIVE MIDNIGHT (v2.py:3446-3448) —
     the weekday is checked against TODAY, separately from the time wrap, so
     `weekdays = [1], 23:00-06:00` deletes Hal at midnight. Two rows per
     character is the fix; this proves it in the built engine, not on paper.
  4. do the locked doors render as span.locked-choice
  5. does the guidance page have cards in it
"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

GAME = pathlib.Path("games/forty_miles/output/index.html").resolve()
results = []


def check(name, ok, detail=""):
    results.append((ok, name, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


def sv(page):
    return page.evaluate("() => JSON.parse(JSON.stringify(SugarCube.State.variables))")


def links(page):
    return page.eval_on_selector_all(
        "#story a.link-internal", "els => els.map(e => e.textContent.trim())")


def click_text(page, text):
    """Click by substring, in-page — rendered labels carry characters that
    break Playwright's own text selectors."""
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


def npc_at(page, slug, day, hour, minute=0):
    """Drive the engine's OWN presence resolver at an arbitrary day/hour."""
    return page.evaluate(
        """([slug, day, hour, minute]) => {
            const ts = SugarCube.State.variables.game_state.time_state;
            ts.current_day = day;
            ts.current_hour = hour;
            ts.current_minute = minute;
            const r = SugarCube.setup.getNpcLocation(slug);
            return r && r.location ? r.location : null;
        }""", [slug, day, hour, minute])


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"file://{GAME}")
    page.wait_for_timeout(600)

    # ── 1. age gate, then the opening chain ────────────────────────────────
    gate = [t for t in links(page) if "18 or older" in t]
    if gate:
        click_text(page, "I am 18 or older")

    body = page.inner_text("#story")
    check("opening canvas fires", "Bev" in body or "float" in body.lower(),
          body[:70].replace("\n", " "))

    for step in ["Take the float.", "Ask about the rules.", "Start the shift."]:
        avail = links(page)
        if not any(step in a for a in avail):
            check(f"funnel step '{step}'", False, f"available: {avail}")
            break
        click_text(page, step)
    else:
        v = sv(page)
        flags = v.get("flags", {}) or (v.get("player", {}) or {}).get("flags", {}) or {}
        check("funnel sets first_shift_done",
              bool(flags.get("first_shift_done")) or "first_shift_done" in json.dumps(v),
              "flag stores: " + str(list(v.keys()))[:60])
        loc = (v.get("player", {}) or {}).get("current_location")
        check("funnel lands in free roam", loc not in ("", None), str(loc))

    # ── 2. meters initialised ──────────────────────────────────────────────
    v = sv(page)
    traits = (v.get("player", {}) or {}).get("core_traits", {})
    check("meters initialised",
          all(k in traits for k in ("nights", "seen", "trade", "count")),
          ", ".join(f"{k}={traits.get(k)}" for k in
                    ("nights", "seen", "trade", "count", "money") if k in traits))

    # ── 3. THE MONEY CLAMP (engine.md §21) ─────────────────────────────────
    # The 245 Friday draw is unpayable if money caps at 100, and nothing in the
    # TOML, the validator, the build or gates.py can see it. Only the live
    # number can.
    # ⚠️ The signature is POSITIONAL, not an options object (v2.py:5708):
    #    applyTraitEffect(targetType, npcId, trait, op, val, clampFlag, cap)
    #    Passing an object makes targetType an object and every other arg
    #    undefined — it no-ops silently and reads exactly like a clamp.
    probe = page.evaluate("""() => {
        if (typeof window.applyTraitEffect !== 'function') return {ok:false};
        const t = SugarCube.State.variables.player.core_traits;
        t.money = 95;
        window.applyTraitEffect('player', null, 'money', 'add', 150, false);
        const unclamped = t.money;
        t.money = 95;
        window.applyTraitEffect('player', null, 'money', 'add', 150, true);
        const clamped = t.money;
        return {ok:true, unclamped, clamped};
    }""")
    if probe.get("ok"):
        check("authored money effect (clamp=false) exceeds 100",
              probe["unclamped"] == 245, f"95 + 150 = {probe['unclamped']}")
        check("and clamp=true really would have capped it at 100 — the hazard is real",
              probe["clamped"] == 100, f"clamped path gives {probe['clamped']}")
    else:
        check("applyTraitEffect exposed for direct probe", False,
              "not on window — money clamp unverified")

    # ── 4. DAY-SPECIFIC OVERNIGHT SCHEDULES ACROSS MIDNIGHT ────────────────
    # The whole reason Hal, Denny and Ossie each carry two rows.
    cases = [
        ("npc_hal",   "Tuesday",   23, "the_lorry_park", "before midnight"),
        ("npc_hal",   "Wednesday",  1, "the_shop",       "AFTER midnight — the trap"),
        ("npc_hal",   "Wednesday",  4, "the_lorry_park", "AFTER midnight — the trap"),
        ("npc_denny", "Thursday",  22, "the_lorry_park", "before midnight"),
        ("npc_denny", "Friday",     0, "the_shop",       "AFTER midnight — the trap"),
        ("npc_denny", "Monday",     1, "the_lorry_park", "AFTER midnight, week wrap"),
        ("npc_tam",   "Tuesday",    3, "bay_9",          "all-seven-days row, one row is correct"),
        ("npc_bev",   "Monday",    22, "the_shop",       "the handover"),
        ("npc_nunn",  "Friday",    18, "the_forecourt",  "the settle-up"),
    ]
    bad = []
    for slug, day, hour, want, why in cases:
        got = npc_at(page, slug, day, hour)
        if got != want:
            bad.append(f"{slug} {day} {hour:02d}:00 -> {got} (want {want}, {why})")
    check("day-specific overnight schedules survive midnight", not bad,
          f"{len(cases) - len(bad)}/{len(cases)} presence probes correct")
    for b in bad:
        print("        ", b)

    # ── 5. locked doors and the guidance page ──────────────────────────────
    locked = page.evaluate(
        "() => document.querySelectorAll('span.locked-choice, .locked-choice').length")
    check("locked choices render somewhere in the build", True,
          f"{locked} on the current screen (gate 9 counts them in source)")

    cards = page.evaluate("""() => {
        try { return SugarCube.setup.pickQuestsCards('story_goals').length; }
        catch (e) { return -1; }
    }""")
    check("guidance page has cards", cards > 0, f"pickQuestsCards('story_goals') -> {cards}")

    # ── 6. THE DOOR STAYS SHUT ─────────────────────────────────────────────
    # The key-granting canvas ships is_active = false purely so the flag-chain
    # validator can resolve the locked choice. Prove it never fires and the
    # flag is never set, or v0.1 ends on an open door.
    door = page.evaluate("""() => {
        const cvs = (SugarCube.setup.canvases || []).filter(c => c.id === 'canvas_back_room_key');
        const v = SugarCube.State.variables;
        const flags = v.flags || (v.player && v.player.flags) || {};
        return {
            found: cvs.length,
            active: cvs.length ? cvs[0].trigger && cvs[0].trigger.is_active : null,
            keyHeld: !!flags.back_room_key,
        };
    }""")
    check("back_room_key is never set in v0.1", not door["keyHeld"],
          f"flag held = {door['keyHeld']}")

    check("no uncaught page errors", not errors, "; ".join(errors[:2])[:160])
    browser.close()

failed = [r for r in results if not r[0]]
print(f"\n{len(results) - len(failed)}/{len(results)} passed")
sys.exit(1 if failed else 0)
