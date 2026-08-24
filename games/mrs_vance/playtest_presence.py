"""Live presence check for Mrs. Vance — does the ambient gate actually hold?

REVIEW.md §12 P1 is the item this proves. Its first draft recorded the mechanism from
the runtime source and said outright that "a captured instance is not in hand", because
ambient chances run 0.26-0.35 and a walker almost never catches one in the act. This
drives setup.checkRandomEncounters() directly, 400 times per hour, and reads which
canvases come back — so the gate is observed rather than inferred, in both directions.

    python3 games/mrs_vance/playtest_presence.py <path-to-index.html>

⚠️ games/mrs_vance/output/index.html is the PRE-P1 artefact and will fail this.
   Per REVIEW.md §1 B1 that build is deliberately not refreshed until release, so
   build to a scratch directory and point this at that:

     python3 manage.py package_from_toml \
         --file games/mrs_vance/toml_phases/7_final_game.toml \
         --output /tmp/mv --gen-version v2 --dev --debug
     python3 games/mrs_vance/playtest_presence.py /tmp/mv/index.html

The two rooms are chosen because each carries its own control:

  the_bunk_room  three gated ambients and amb_bunk_partition, which is ungated BY
                 DESIGN (nobody speaks in it). If the gated three go quiet at an hour
                 where the control still fires, the gate is what silenced them and not
                 some unrelated filter.

  the_office     amb_office_close needs Cade HERE; amb_office_phone needs him on the
                 SHOP FLOOR and Dorn away. They are true at opposite hours, so one
                 room proves both the requires_npc path and the two-item
                 npc_at_location path. amb_office_wrecker is left ungated on purpose —
                 its prose is a man arriving in the small hours from somewhere it
                 declines to name — and it firing at 02:00 is the check that this
                 harness is not simply silencing everything.
"""

import sys, pathlib, collections
from playwright.sync_api import sync_playwright

DEFAULT = "games/mrs_vance/output/index.html"
GAME = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT).resolve()
if not GAME.exists():
    sys.exit(f"no build at {GAME} — see the module docstring")
results = []

def check(name, ok, detail=""):
    results.append((ok, name, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}\n        {detail}")

SAMPLE = """([loc, day, hour, minute, n]) => {
    const S = SugarCube.State.variables, setup = SugarCube.setup;
    const ts = S.game_state.time_state;
    ts.current_day = day; ts.current_hour = hour; ts.current_minute = minute;
    const out = {};
    for (let i = 0; i < n; i++) {
        // clear every per-day / cooldown latch so each call is an independent roll
        S.game_state.random_cooldowns = {};
        S.game_state.trigger_history = {};
        S.game_state.activity_trigger_history = {};
        const p = setup.checkRandomEncounters(loc);
        if (p) out[p] = (out[p] || 0) + 1;
    }
    return out;
}"""

def sample(page, loc, day, hour, minute=0, n=400):
    raw = page.evaluate(SAMPLE, [loc, day, hour, minute, n])
    # passage name -> canvas id
    return {k.replace("Canvas_", "").replace("_Node_base", ""): v for k, v in raw.items()}

def npc_at(page, slug, day, hour, minute=0):
    return page.evaluate("""([s,d,h,m]) => {
        const ts = SugarCube.State.variables.game_state.time_state;
        ts.current_day=d; ts.current_hour=h; ts.current_minute=m;
        const r = SugarCube.setup.getNpcLocation(s);
        return r && r.location ? r.location : null; }""", [slug, day, hour, minute])

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"file://{GAME}")
    page.wait_for_timeout(700)
    page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('#story a.link-internal'));
        const el = els.find(e => e.textContent.includes('18 or older'));
        if (el) el.click(); }""")
    page.wait_for_timeout(400)

    # ── A. the bunk room — Isaac gates three, one ungated control ──────────
    print("\n── the_bunk_room · gated: radio, stairs, two_of_them · control: partition\n")
    away = npc_at(page, "npc_isaac", "Monday", 10)
    home = npc_at(page, "npc_isaac", "Monday", 22)
    check("isaac is elsewhere at Mon 10:00, in the bunk room at Mon 22:00",
          away != "the_bunk_room" and home == "the_bunk_room",
          f"10:00 -> {away} | 22:00 -> {home}")

    off = sample(page, "the_bunk_room", "Monday", 10)
    on  = sample(page, "the_bunk_room", "Monday", 22)
    GATED = ["amb_bunk_radio", "amb_bunk_stairs", "amb_bunk_two_of_them"]
    check("gated bunk ambients CANNOT fire while isaac is at the shop",
          all(g not in off for g in GATED), f"400 rolls at Mon 10:00 -> {off}")
    check("the ungated control still fires at the same hour",
          "amb_bunk_partition" in off, f"amb_bunk_partition x{off.get('amb_bunk_partition',0)}")
    check("the same three DO fire once isaac is on his bed",
          all(g in on for g in GATED), f"400 rolls at Mon 22:00 -> {on}")

    # ── B. the office — two gates that are true at opposite hours ──────────
    print("\n── the_office · close needs cade HERE · phone needs cade on the SHOP FLOOR + dorn away\n")
    c02 = npc_at(page, "npc_cade", "Monday", 2)
    c10 = npc_at(page, "npc_cade", "Monday", 10)
    c19 = npc_at(page, "npc_cade", "Monday", 19)
    check("cade: nowhere at 02:00, shop floor at 10:00, office at 19:00",
          c02 is None and c10 == "the_shop_floor" and c19 == "the_office",
          f"02:00 -> {c02} | 10:00 -> {c10} | 19:00 -> {c19}")

    o02 = sample(page, "the_office", "Monday", 2)
    o10 = sample(page, "the_office", "Monday", 10)
    o19 = sample(page, "the_office", "Monday", 19)
    check("amb_office_close cannot fire at 02:00 (cade is nowhere)",
          "amb_office_close" not in o02, f"400 rolls at Mon 02:00 -> {o02}")
    check("amb_office_close fires at 19:00, the hour its prose describes",
          "amb_office_close" in o19, f"amb_office_close x{o19.get('amb_office_close',0)}")
    check("amb_office_phone fires at 10:00 — cade in bay two, dorn on the road",
          "amb_office_phone" in o10, f"amb_office_phone x{o10.get('amb_office_phone',0)}")
    check("amb_office_phone cannot fire at 19:00 — cade is in the office, not bay two",
          "amb_office_phone" not in o19, f"400 rolls at Mon 19:00 -> {o19}")

    check("no page errors", not errors, "; ".join(errors[:2]) or "clean")
    browser.close()

npass = sum(1 for ok, *_ in results if ok)
print(f"\n{npass}/{len(results)} checks pass")
sys.exit(0 if npass == len(results) else 1)
