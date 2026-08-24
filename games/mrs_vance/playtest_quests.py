"""Live quest-card check for Mrs. Vance — does the badge arrive after the content?

REVIEW.md §3 Q1 is the item this proves. v0.1 printed "✓ Arc complete" at or before
the click that opened each character's loop: two badges landed exactly ON the door,
three landed BEFORE it, and one of those forty points early. The repair moved the ✓ off
the meter entirely and onto a flag the loop sets on its way out, and put the engine's
middle frame (🔓 Ready + 📍 + 🕒) in the gap where the door is open and unplayed.

    python3 games/mrs_vance/playtest_quests.py <path-to-index.html>

⚠️ games/mrs_vance/output/index.html is the PRE-repair artefact and will fail this. Per
   REVIEW.md §1 B1 that build is not refreshed until release, so build to scratch:

     python3 manage.py package_from_toml \
         --file games/mrs_vance/toml_phases/7_final_game.toml \
         --output /tmp/mv --gen-version v2 --dev --debug
     python3 games/mrs_vance/playtest_quests.py /tmp/mv/index.html

It drives the same two functions the page and the sidebar both call — pickQuestsCard →
renderQuestsGoalBlock (v2.py:15454-15456, "there is no separate sidebar quest") — so a
pass here is a pass on both surfaces.

⚠️ The 🔓 Ready assertion checks for the 📍, not merely for a non-empty string.
   lookupCanvasBySlug walks help_data.locationCanvases, which is keyed by location UUID,
   so a ready_canvas naming a TRIGGERLESS canvas (every loop in this game) resolves to
   null and Frame 2 returns "" — the card would render no frame at all and a
   non-emptiness check would not notice. The 📍 only appears when the lookup resolved.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

DEFAULT = "games/mrs_vance/output/index.html"
GAME = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT).resolve()
if not GAME.exists():
    sys.exit(f"no build at {GAME} — see the module docstring")

results = []

def check(name, ok, detail=""):
    results.append((ok, name, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}\n        {detail}")

# slug, meeting flag, the meter and value the door reads, the played flag,
# and an optional lower rung that has to be satisfied first
CAST = [
    ("npc_cade",    "met_cade",    "want", 42, "cade_loop_played",    ("trust", 26)),
    ("npc_booth",   "met_booth",   "want", 50, "booth_loop_played",   ("trust", 30)),
    ("npc_isaac",   "met_isaac",   "want", 38, "isaac_loop_played",   None),
    ("npc_sherrod", "met_sherrod", "want", 34, "sherrod_loop_played", None),
    ("npc_tobin",   "met_tobin",   "want", 70, "tobin_loop_played",   None),
]

FRAME = """([slug, flags, traits]) => {
    const S = SugarCube.State.variables, setup = SugarCube.setup;
    S.flags = S.flags || {};
    for (const k in flags) S.flags[k] = flags[k];
    const map = setup.npc_slug_map || {};
    for (const t of traits) {
        const uuid = map[t[0]] || t[0];
        const npc = S.npcs && S.npcs[uuid];
        if (npc && npc.core_traits) npc.core_traits[t[1]] = t[2];
    }
    const card = setup.pickQuestsCard(slug);
    if (!card) return { html: null, priority: null };
    const html = setup.renderQuestsGoalBlock(card, setup.evaluateGoals(card));
    return { html: html, priority: card.priority, terminal: !!card.terminal };
}"""

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

    def frame(slug, flags, traits):
        return page.evaluate(FRAME, [slug, flags, traits])

    for slug, met, meter, door, played, rung in CAST:
        who = slug.replace("npc_", "")
        print(f"\n── {who}: door is {meter} >= {door}\n")
        base = {met: True, "opening_done": True, played: False}
        pre = [(slug, rung[0], rung[1])] if rung else []

        # 1 — below the door
        r = frame(slug, base, pre + [(slug, meter, door - 8)])
        h = r["html"] or ""
        check(f"{who}: climbing shows the goal frame with live progress",
              "🎯" in h and f"{door - 8} / {door}" in h and "✓" not in h,
              h.replace("\n", " ")[:150] or "(no frame at all)")

        # 2 — at the door, unplayed
        r = frame(slug, base, pre + [(slug, meter, door)])
        h = r["html"] or ""
        check(f"{who}: at the door and unplayed shows Ready WITH a location",
              "🔓" in h and "📍" in h and "✓" not in h,
              h.replace("\n", " ")[:170] or "(no frame at all)")

        # 3 — played
        r = frame(slug, {**base, played: True}, pre + [(slug, meter, door)])
        h = r["html"] or ""
        check(f"{who}: the tick arrives only after the loop has been played",
              "✓" in h and "As far as this build goes" in h and "Arc complete" not in h,
              h.replace("\n", " ")[:150] or "(no frame at all)")

    # ── Dorn: knowingly unbuilt, and his v0.1 card drew no frame at all ────
    print("\n── dorn: no loop, no door — the wall is stated, not hidden\n")
    r = frame("npc_dorn", {"opening_done": True}, [("npc_dorn", "want", 0)])
    h = r["html"] or ""
    check("dorn: below his one rung shows the goal frame",
          "🎯" in h and "0 / 12" in h, h.replace("\n", " ")[:130] or "(no frame at all)")
    r = frame("npc_dorn", {"opening_done": True}, [("npc_dorn", "want", 30)])
    h = r["html"] or ""
    check("dorn: past it states the wall instead of drawing nothing",
          "✓" in h and "As far as this build goes" in h,
          h.replace("\n", " ")[:130] or "(no frame at all)")

    # ── the chain is worthless if the flag never lands ────────────────────
    # Play each loop to its finish node and out the far side, and read the flag.
    # The `act` node's cum choice is gated `arousal gte 60` in four of the five,
    # so drive arousal first or the only rendered exits are the bail-out ones.
    print("\n── the flag the badge depends on: does finishing a loop set it?\n")
    for loop, flag in [(f"loop_{w}", f"{w}_loop_played")
                       for w in ("cade", "booth", "isaac", "sherrod", "tobin")]:
        node = "act_desk" if loop == "loop_cade" else "act"
        before = page.evaluate("""([f]) => {
            const S = SugarCube.State.variables;
            S.flags = S.flags || {}; S.flags[f] = false;
            if (S.player && S.player.core_traits) S.player.core_traits.arousal = 95;
            SugarCube.setup.commitMoment && SugarCube.setup.commitMoment();
            return !!S.flags[f]; }""", [flag])
        page.evaluate("([n]) => SugarCube.Engine.play(n)", [f"Canvas_{loop}_Node_{node}"])
        page.wait_for_timeout(300)
        to_finish = page.evaluate("""() => {
            const els=[...document.querySelectorAll('#story a.link-internal')];
            const el=els.find(e=>/_Node_finish$/.test(e.getAttribute('data-passage')||''));
            if(el){ el.click(); return el.textContent.trim(); } return null; }""")
        page.wait_for_timeout(300)
        out = page.evaluate("""() => {
            const els=[...document.querySelectorAll('#story a.link-internal')];
            if(els.length){ const t=els[0].textContent.trim(); els[0].click(); return t; }
            return null; }""")
        page.wait_for_timeout(400)
        after = page.evaluate("([f]) => !!SugarCube.State.variables.flags[f]", [flag])
        check(f"{loop}: playing it through sets {flag}",
              before is False and after is True,
              f"{before} -> {after} · to finish: {to_finish!r} · out: {out!r}")

    check("no page errors", not errors, "; ".join(errors[:2]) or "clean")
    browser.close()

npass = sum(1 for ok, *_ in results if ok)
print(f"\n{npass}/{len(results)} checks pass")
sys.exit(0 if npass == len(results) else 1)
