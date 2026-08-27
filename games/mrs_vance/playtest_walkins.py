"""Measure the Lane 3 walk-in rates at each `standing` band, in the built game.

REVIEW.md §5 S1b is the item this proves. `standing` swapped a line and decided
nothing; it now DELIVERS PEOPLE, which is how the field gives a rising audience meter
consequence without ever printing a refusal (`the-meters.md`, "Rarely a lock is not the
same as never mechanical" — patriarch's `$Reputation gt 5` → Marlene knocks).

    python3 games/mrs_vance/playtest_walkins.py <path-to-index.html> [rolls]

⚠️ Build to a scratch directory rather than pointing this at games/mrs_vance/output —
   per REVIEW.md §1 B1 that artefact is deliberately not refreshed until release.

The claim has two halves and BOTH are asserted, because proving only the first would
hide a regression in the second:

    below standing 40   the four nameless walk-ins fire MORE often
    at or above 40      every rate is UNCHANGED, the named walk-ins included

⚠️ The bonus rules are APPENDED to their exclusive_group, never prepended. Group rules
   share one dice over cumulative buckets (v2.py:5345), so an appended rule takes a
   bucket that today falls through to solo, and a claimed-but-failed slot falls to solo
   rather than promoting the next rule (v2.py:5378). Prepending would have stolen the
   bucket in FRONT of an NPC walk-in and cut its rate at every band. That is why the
   second half is asserted over every outcome the host produces and not just the four.

This drives `setup.checkAndSubstituteCanvas` directly rather than playing the canvas:
it is the function that owns the dice, so calling it in a loop measures the
distribution instead of sampling one draw of it. Presence is a function of the clock
here — NPCs carry no settable location, only schedules — so each host is measured at an
hour where its group's presence gates hold, and the clock is held fixed across bands.
"""
import sys
import pathlib
from playwright.sync_api import sync_playwright

GAME = pathlib.Path(sys.argv[1]).resolve()
ROLLS = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
TOL = 0.030               # 3 sigma of binomial noise at n=6000 is ~0.019

LOW, HIGH = 20, 60        # inside the two bands the `lt 40` rule divides, never on it

# host -> (day, hour, minute, the walk-in `standing` should deliver, expected lift)
#
# ⚠️ THE HOUR IS CHOSEN SO THE HOST'S *NAMED* WALK-IN FIRES TOO. An hour where only the
#    standing-gated rule can fire would make the second half of this harness vacuous:
#    every named rule would read 0.000 in both bands and "flat" would prove nothing.
#    Measured from `setup.getNpcLocation` on a Monday --
#      19:30  Cade in the office        -> walkin_office_cade   live at work_counter
#      11:30  Isaac in the wash bay,    -> walkin_bay_isaac*    live at act_wash_bay
#             Cade and Tobin on the shop floor for the bay's own presence gate
#      10:30  Tobin on the shop floor   -> walkin_shop_tobin    live at work_parts_run
#      22:30  Tobin on the back row     -> walkin_row_tobin     live at work_walkround
#
# ⚠️ THE PLAYER'S LOCATION IS PART OF THE SETUP, not decoration. A walk-in that names
#    `requires_npc` is checked as "is that NPC standing where the PLAYER is"
#    (v2.py:5340), so with `player.current_location` left at its initial "" every named
#    walk-in silently returns null and the harness measures a world with nobody in it.
HOSTS = [
    ('work_counter',   'the_office',     'Monday', 19, 30, 'walkin_office_driver', 0.15),
    ('act_wash_bay',   'the_wash_bay',   'Monday', 11, 30, 'walkin_bay_seen',      0.15),
    ('work_parts_run', 'the_shop_floor', 'Monday', 10, 30, 'walkin_shop_watched',  0.15),
    ('work_walkround', 'the_back_row',   'Monday', 22, 30, 'walkin_row_cab',       0.15),
]

MEASURE = """([host, where, day, hour, minute, standing, n]) => {
    const sv = SugarCube.State.variables, S = SugarCube.setup;
    const ts = sv.game_state.time_state;
    ts.current_day = day; ts.current_hour = hour; ts.current_minute = minute;
    sv.player.current_location = where;
    sv.player.core_traits.standing = standing;
    // The named walk-ins gate on trust/want as well as presence. Max them so the
    // only thing separating the two bands is `standing` -- which is the point.
    for (const n in sv.npcs) {
        const t = sv.npcs[n].core_traits || {};
        for (const k in t) if (typeof t[k] === 'number') t[k] = 100;
    }
    const out = {};
    for (let i = 0; i < n; i++) {
        // clear every per-day / cooldown latch so each call is an independent roll
        sv.game_state.random_cooldowns = {};
        sv.game_state.trigger_history = {};
        sv.game_state.activity_trigger_history = {};
        const p = S.checkAndSubstituteCanvas(host);
        const k = p ? p.replace('Canvas_', '').replace('_Node_base', '') : '(the canvas itself)';
        out[k] = (out[k] || 0) + 1;
    }
    for (const k in out) out[k] = out[k] / n;
    return out;
}"""

with sync_playwright() as pw:
    browser = pw.chromium.launch()
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

    ok = True
    for host, where, day, hour, minute, target, lift in HOSTS:
        low = page.evaluate(MEASURE, [host, where, day, hour, minute, LOW, ROLLS])
        high = page.evaluate(MEASURE, [host, where, day, hour, minute, HIGH, ROLLS])
        print(f"\n{host}  (in {where}, {day} {hour:02d}:{minute:02d}, "
              f"{ROLLS} rolls per band)")

        got_low, got_high = low.get(target, 0.0), high.get(target, 0.0)
        got_lift = got_low - got_high
        good = abs(got_lift - lift) <= TOL and got_high > 0
        ok &= good
        print(f"  {'OK ' if good else 'BAD'} {target:24} {got_high:.3f} at {HIGH} "
              f"-> {got_low:.3f} at {LOW}   lift {got_lift:+.3f} (want {lift:+.2f})")

        # everything else this host can produce must be identical across the two bands
        for k in sorted(set(low) | set(high)):
            if k == target:
                continue
            a, b = high.get(k, 0.0), low.get(k, 0.0)
            # the plain canvas absorbs the lift by construction — check the mirror
            want = -lift if k == '(the canvas itself)' else 0.0
            flat = abs((b - a) - want) <= TOL
            ok &= flat
            note = "absorbs the lift" if want else "flat, both bands"
            print(f"  {'OK ' if flat else 'BAD'} {k:24} {a:.3f} -> {b:.3f}   "
                  f"delta {b - a:+.3f} (want {want:+.2f}, {note})")

    print(f"\n  page errors: {'; '.join(errors[:2]) or 'clean'}")
    ok &= not errors
    browser.close()
    print('\nRESULT:', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
