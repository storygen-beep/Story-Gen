#!/usr/bin/env python3
"""
playtest.py — the Player harness. Drives a BUILT game and reports numbers.

`gates.py` reads the source. This reads the running game, which is the only place
some defects exist at all: `forty_miles` 0.1 shipped 35 effects using `op = "subtract"`
— an op the runtime does not implement — and the TOML, the validator, the build and
every gate were green the whole way down. A live money diff was what found it.

Usage:
    python3 scripts/playtest.py <game-slug>          # the universal checks
    python3 scripts/playtest.py <path/to/index.html>
    python3 scripts/playtest.py <slug> --build /tmp/x/index.html   # a scratch artefact
    python3 scripts/playtest.py <slug> --headed      # watch it run

    from playtest import open_game, sv, click, play, report   # the library

Layer A is the library — the helpers below. Layer B is the universal checks in
`universal()`, which need no per-game code and run on any build.

WHY THIS EXISTS AS SHARED CODE
──────────────────────────────
Seven hand-written play-tests already live in `games/` (mrs_vance ×5, steam, forty_miles),
each re-deriving the engine's call signatures from scratch. Run 2026-08-29, `steam`
reported 2 failures and BOTH were the harness, not the game:

  · it called `applyTraitEffect` with one object; the engine takes seven positional
    args (v2.py:5883), so the call did nothing and money read 95 instead of 135
  · it called `pickQuestsCards('all')`; v2.py:15496 is `if (scope !== "story_goals")
    return [];`, so the answer is [] by construction, while gates.py reported 24 cards

A false alarm is worse than no answer: it sends a session hunting a bug that does not
exist. Every signature this file wraps is one nobody has to get right again.

THE TWO RULES, ENFORCED HERE IN CODE
────────────────────────────────────
1. ASSERT ON STATE, NEVER ON A RENDERED LABEL. A label is not the string that was
   authored — icons, spacing, cost suffixes and state decoration are added at render.
   Measured record of label assertions in this project: four false alarms, zero real
   findings. So there is no `assert_text` helper here and there never will be.
   `click()` navigates BY label, which is how a player moves and is fine; `body()`
   returns prose for "which VARIANT rendered", which is what `playtest_standing.py`
   proved six ladders with. Neither may decide whether a mechanic fired — ask `sv()`.

2. THE FIVE ENGINE FACTS THAT EACH FAKE A BROKEN GAME (engine.md §24 + §12) are owned
   below, not left to each author:
     · `State` / `Engine` / `setup` hang off `window.SugarCube`, not the bare global
     · `time_state.current_day` is a day NAME; an int makes indexOf return -1 and
       EVERY location reports nobody present (v2.py:3422)
     · presence is asked of `setup.getNpcsPresentAtLocation`, never recomputed —
       a hand-rolled `start <= now <= end` drops every overnight window
     · the built page is entity-encoded: 663 `&lt;&lt;set` against 3 literal ones,
       so `html.unescape()` before matching macro syntax in page source
     · a walk-in naming `requires_npc` asks whether that NPC is where the PLAYER is
       (v2.py:5432) — leave `player.current_location` at its initial "" and every
       named walk-in returns null and you measure a world with nobody in it

Requires playwright (`pip install playwright && playwright install chromium`).
"""

import sys
import os
import re
import html
import json
import contextlib

try:
    import tomllib as _toml          # py3.11+
    def _load(p): return _toml.load(open(p, "rb"))
except ImportError:
    import tomli as _toml            # py3.10 fallback
    def _load(p): return _toml.load(open(p, "rb"))


# The engine indexes the weekday by NAME (v2.py:3422). Anything not in this list
# makes indexOf return -1 at every schedule call site.
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"]

# engine.md §12: rendered links are `a.link-internal` inside `#story`. A bare
# `text=` selector also matches the embedded <tw-passagedata> source and resolves
# to an invisible element, so every selector here is scoped.
LINKS = "#story a.link-internal"
LOCKED = "#story span.locked-choice"
BODY = "#passages"

AGE_GATE = "18 or older"          # v2.py:8368


# ─────────────────────────────────────────────────────────────────────────────
# Opening the build
# ─────────────────────────────────────────────────────────────────────────────

@contextlib.contextmanager
def open_game(path, headless=True, pass_age_gate=True):
    """Launch the build and hand back (page, errors).

    `errors` is a live list of uncaught page errors — check it at the end of a run
    rather than sprinkling assertions, because a JS exception mid-run makes every
    later check meaningless and you want to know that happened.

    The age gate is clicked by default: `Start` renders a title screen and nothing
    auto-plays before the gate link, so a harness that skips it concludes the opening
    is broken when it is fine (engine.md §12).
    """
    from playwright.sync_api import sync_playwright

    game = os.path.abspath(path)
    if not os.path.exists(game):
        sys.exit(f"no build at {game}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        page = browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(f"file://{game}")
        # wait for the selector, not a fixed sleep — the seven hand-written scripts
        # use three different timeouts (600/700/800ms) and that is a race, not a policy
        page.wait_for_selector(BODY, timeout=15000)
        page.wait_for_timeout(300)
        if pass_age_gate:
            enter_game(page)
        try:
            yield page, errors
        finally:
            browser.close()


def enter_game(page):
    """Click the age gate. Returns True if a gate was found and clicked."""
    ok = page.evaluate(
        """(sel) => {
            const els = Array.from(document.querySelectorAll(sel[0]));
            const el = els.find(e => e.textContent.includes(sel[1]));
            if (!el) return false;
            el.click();
            return true;
        }""", [LINKS, AGE_GATE])
    page.wait_for_timeout(400)
    return ok


# ─────────────────────────────────────────────────────────────────────────────
# Reading the running game — state first, always
# ─────────────────────────────────────────────────────────────────────────────

def sv(page, expr="SugarCube.State.variables"):
    """The state variables, deep-copied out of the page. THE way to assert."""
    return page.evaluate(f"() => JSON.parse(JSON.stringify({expr}))")


def traits(page):
    """`player.core_traits` — where every player meter and the money live."""
    return sv(page, "SugarCube.State.variables.player.core_traits")


def flags(page):
    return sv(page, "SugarCube.State.variables.flags")


def links(page):
    """Clickable choice labels on the current screen."""
    return page.eval_on_selector_all(
        LINKS, "els => els.map(e => e.textContent.trim())")


def locked(page):
    """Choices rendered visible-but-locked (engine.md §15)."""
    return page.eval_on_selector_all(
        LOCKED, "els => els.map(e => e.textContent.trim())")


def body(page):
    """Whitespace-normalised prose on screen.

    For "WHICH VARIANT rendered" — a ladder rung, a pool member, a band. NOT for
    whether a mechanic fired: ask `sv()`. See rule 1 in the module docstring.
    """
    return re.sub(r"\s+", " ", page.inner_text(BODY))


def page_source(page):
    """The built page's own markup, entity-decoded (engine.md §24.4).

    A raw grep for `<<set` on a built page finds 3 where there are 663. Always
    unescape before matching macro syntax.
    """
    return html.unescape(page.content())


# ─────────────────────────────────────────────────────────────────────────────
# Moving through the game
# ─────────────────────────────────────────────────────────────────────────────

def click(page, text, settle=250):
    """Click a choice by substring, in-page.

    Navigating by label is how a player moves and is deliberately kept. Playwright's
    own text selectors break on the characters real labels carry (✓, curly
    apostrophes, cost suffixes), which is why this matches in-page instead.
    """
    ok = page.evaluate(
        """(a) => {
            const els = Array.from(document.querySelectorAll(a[0]));
            const el = els.find(e => e.textContent.includes(a[1]));
            if (!el) return false;
            el.click();
            return true;
        }""", [LINKS, text])
    page.wait_for_timeout(settle)
    return ok


def play(page, canvas, node="base", settle=250):
    """Jump straight to a canvas node. Returns True, or the error string."""
    out = page.evaluate(
        """(n) => { try { SugarCube.Engine.play(n); return true; }
                    catch (e) { return String(e); } }""",
        f"Canvas_{canvas}_Node_{node}")
    page.wait_for_timeout(settle)
    return out


def goto(page, passage, settle=250):
    """Jump to any passage by name — Location_<slug>, an info page, anything."""
    out = page.evaluate(
        """(n) => { try { SugarCube.Engine.play(n); return true; }
                    catch (e) { return String(e); } }""", passage)
    page.wait_for_timeout(settle)
    return out


def set_time(page, day, hour, minute=0):
    """Move the clock. `day` MUST be a day name (engine.md §24.2).

    Passing 0 for Monday is the single most expensive mistake available here: the
    engine does `["Monday",…].indexOf(current_day)`, gets -1, matches no schedule
    row, and the whole world reads as empty. Rejected loudly rather than silently.
    """
    if day not in DAYS:
        raise ValueError(
            f"day must be one of {DAYS}, got {day!r} — "
            "an index makes indexOf return -1 and every location reports nobody present")
    page.evaluate(
        """(a) => {
            const ts = SugarCube.State.variables.game_state.time_state;
            ts.current_day = a[0]; ts.current_hour = a[1]; ts.current_minute = a[2];
        }""", [day, hour, minute])


def stand_at(page, location_slug):
    """Put the player somewhere.

    Not decoration: a walk-in naming `requires_npc` is evaluated as "is that NPC
    standing where the PLAYER is" (v2.py:5432), so with `current_location` left at
    its initial "" every named walk-in returns null.
    """
    page.evaluate("(l) => { SugarCube.State.variables.player.current_location = l; }",
                  location_slug)


# ─────────────────────────────────────────────────────────────────────────────
# Asking the engine — never recompute what it will tell you
# ─────────────────────────────────────────────────────────────────────────────

def locations(page):
    """Location slugs, from the engine's own map (v2.py:3247).

    Read from the runtime, not rebuilt from the TOML: the passage slug is
    `properties['slug'] or loc_<id>` (v2.py:20072), and re-deriving that in Python
    is exactly the guesswork this file exists to delete.
    """
    return page.evaluate("() => Object.keys(SugarCube.setup.locations || {})")


def npcs_at(page, location_slug):
    """Who is here, per the engine (engine.md §24.3)."""
    return page.evaluate(
        """(l) => (SugarCube.setup.getNpcsPresentAtLocation(l) || [])
                    .map(n => n.id || n.npc_id || n)""", location_slug)


def npc_at(page, npc_slug):
    """Where one NPC is, per the engine. Returns a location slug or None."""
    return page.evaluate(
        """(s) => { const r = SugarCube.setup.getNpcLocation(s);
                    return r && r.location ? r.location : null; }""", npc_slug)


def quest_cards(page):
    """Guidance cards resolving right now, as {"story_goals": n, "<npc>": n, …}.

    TWO functions, and asking only one of them under-reports a working game:

      · `setup.pickQuestsCards(scope)` — v2.py:15495 — returns STORY cards, and
        "story_goals" is the only scope it answers (`if (scope !== "story_goals")
        return [];`, v2.py:15496). It also skips any card carrying an `npc_id`
        (v2.py:15501), so a game whose guidance is entirely per-character reads 0.
      · `setup.pickQuestsCard(npcSlug)` — v2.py:15470 — returns the one card for
        that character.

    `off_season` declares 14 cards, every one of them `npc_id`-bearing, so the
    story scope alone reports an empty guidance page on a game that has a full one.

    ⚠️ The per-character ids come from `setup.quests_cards[].npc_id`, which is exactly
    where the engine's own guidance page gets them (v2.py:15795). NOT from the keys of
    `State.variables.npcs`: in a `--use-db` build that map is keyed by UUID while the
    cards still say `npc_hank`, and the npc objects carry no id field to bridge it, so
    a runtime-keyed loop reports 0 cards on `late_shifts`, which has 22.
    """
    return page.evaluate(
        """() => { try {
              const S = SugarCube.setup || {}, out = {};
              if (typeof S.pickQuestsCards === 'function')
                  out.story_goals = S.pickQuestsCards('story_goals').length;
              if (typeof S.pickQuestsCard === 'function') {
                  const slugs = new Set();
                  for (const c of (S.quests_cards || []))
                      if (c && c.npc_id) slugs.add(c.npc_id);
                  for (const slug of slugs)
                      if (S.pickQuestsCard(slug)) out[slug] = 1;
              }
              return out;
           } catch (e) { return String(e); } }""")


def random_canvases(page):
    """Every `trigger_mode = "random"` canvas the runtime holds, with its chance.

    Read from `setup.help_data.locationCanvases` — the map the engine itself rolls
    against — as [{location, id, chance}, …].

    ⚠️ `chance` is the field the roll reads: `var chance = canvas.chance || 0`
    (v2.py:5452). A random canvas that never got one is not unlikely, it is
    IMPOSSIBLE, and nothing upstream says so — the TOML validates, the build is
    clean, and the source gate counts the declaration.
    """
    return page.evaluate(
        """() => {
            const lc = ((SugarCube.setup.help_data || {}).locationCanvases) || {};
            const out = [];
            for (const loc in lc)
                for (const c of lc[loc])
                    if (c.triggerMode === 'random')
                        out.push({location: loc, id: c.id, chance: c.chance});
            return out;
        }""")


def apply_effect(page, trait, op, value,
                 target="player", npc_id=None, clamp=True, cap=None):
    """Run one trait effect through the engine's own path, and return the new value.

    POSITIONAL, in this order — `applyTraitEffect(targetType, npcId, trait, op, val,
    clampFlag, cap)` (v2.py:5883). Handing it a single options object is a silent
    no-op: it returns without touching anything and the probe reads a number that
    never moved. That is one of the two false alarms this file was written after.
    """
    return page.evaluate(
        """(a) => {
            window.applyTraitEffect(a[0], a[1], a[2], a[3], a[4], a[5], a[6]);
            const t = a[0] === 'player'
                ? SugarCube.State.variables.player.core_traits
                : (SugarCube.State.variables.npcs[a[1]] || {}).core_traits || {};
            return t[a[2]];
        }""", [target, npc_id, trait, op, value, clamp, cap])


def sample_ambients(page, location_slug, rolls=400):
    """Roll the random-event table `rolls` times and return {canvas_id: hits}.

    Ambient chances run 0.26-0.35, so a walker almost never catches one in the act —
    driving the engine's own selector directly is the only way to observe the gate
    rather than infer it. The three latches are cleared between rolls or every call
    after the first is suppressed and the distribution is a lie.
    """
    raw = page.evaluate(
        """(a) => {
            const S = SugarCube.State.variables, setup = SugarCube.setup;
            const out = {};
            for (let i = 0; i < a[1]; i++) {
                S.game_state.random_cooldowns = {};
                S.game_state.trigger_history = {};
                S.game_state.activity_trigger_history = {};
                const p = setup.checkRandomEncounters(a[0]);
                if (p) out[p] = (out[p] || 0) + 1;
            }
            return out;
        }""", [location_slug, rolls])
    return {k.replace("Canvas_", "").replace("_Node_base", ""): v
            for k, v in raw.items()}


def sample_dispatch(page, canvas_id, rolls=400):
    """Roll a Lane 3 dispatcher and return {canvas_id: share}.

    `(the canvas itself)` is the no-substitution outcome — a dispatcher that never
    substitutes shows up as 1.0 there.
    """
    raw = page.evaluate(
        """(a) => {
            const S = SugarCube.State.variables, setup = SugarCube.setup;
            const out = {};
            for (let i = 0; i < a[1]; i++) {
                S.game_state.random_cooldowns = {};
                S.game_state.trigger_history = {};
                S.game_state.activity_trigger_history = {};
                const p = setup.checkAndSubstituteCanvas(a[0]);
                const k = p ? p.replace('Canvas_', '').replace('_Node_base', '')
                            : '(the canvas itself)';
                out[k] = (out[k] || 0) + 1;
            }
            for (const k in out) out[k] = out[k] / a[1];
            return out;
        }""", [canvas_id, rolls])
    return raw


# ─────────────────────────────────────────────────────────────────────────────
# Reporting
# ─────────────────────────────────────────────────────────────────────────────

class Report:
    """The collector every hand-written play-test grew independently.

    `na` is a first-class outcome and is NOT a pass: a game with quests off has no
    guidance page to check, and scoring that green would be a gate that passes by
    being blind — the failure this skill has refused four times.
    """

    def __init__(self, title=""):
        self.rows = []
        if title:
            print(f"\n  {title}\n  " + "─" * 72)

    def check(self, name, ok, detail=""):
        self.rows.append(("PASS" if ok else "FAIL", name, detail))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name:<44} {detail}")
        return ok

    def na(self, name, why=""):
        self.rows.append(("n/a", name, why))
        print(f"  [ n/a]  {name:<44} {why}")

    def note(self, text):
        print(f"          · {text}")

    def done(self):
        bad = [r for r in self.rows if r[0] == "FAIL"]
        na = [r for r in self.rows if r[0] == "n/a"]
        scored = len(self.rows) - len(na)
        print("  " + "─" * 72)
        print(f"  {scored - len(bad)}/{scored} checks passed"
              + (f" · {len(na)} n/a" if na else ""))
        return 1 if bad else 0


# ─────────────────────────────────────────────────────────────────────────────
# Layer B — the universal checks. No per-game code.
# ─────────────────────────────────────────────────────────────────────────────

def universal(page, errors, game=None, rep=None):
    """What only a live run can answer, on any build.

    Deliberately NOT here: anything gates.py already reads from the source. This
    asks whether the built thing runs, not whether it was authored well.
    """
    rep = rep or Report()

    # 1 · the age gate — open_game already clicked it, so this reads the result
    v = sv(page)
    rep.check("the age gate opened the game",
              bool(v.get("player")), "state initialised behind the gate")

    # 2 · the opening canvas actually rendered something
    text = body(page)
    rep.check("the opening canvas fires", len(text.strip()) > 40,
              f"{len(text)} chars on screen")

    # 3 · the funnel reaches free roam.
    #     `current_location` is "" until the first canvas or location passage runs
    #     (engine.md §12), so walking the opening chain is the check. Take the first
    #     link each time — the opening is a linear funnel by doctrine, so there is
    #     nothing to choose between.
    for _ in range(12):
        where = sv(page, "SugarCube.State.variables.player.current_location")
        if where:
            break
        avail = links(page)
        if not avail or not click(page, avail[0]):
            break
    where = sv(page, "SugarCube.State.variables.player.current_location")
    rep.check("the opening reaches free roam", bool(where),
              f"current_location = {where!r}" if where
              else "still empty after 12 steps — the funnel does not land anywhere")

    # 4 · declared meters exist at runtime
    if game:
        declared = list((game.get("player") or {}).get("core_traits", {}).keys())
        live = traits(page)
        missing = [k for k in declared if k not in live]
        rep.check("declared meters initialise", not missing,
                  ", ".join(f"{k}={live.get(k)}" for k in declared[:6])
                  if not missing else f"missing at runtime: {missing}")

    # 5 · every canvas's first node renders without throwing.
    #     A canvas the engine cannot reach is invisible to every source gate.
    if game:
        broken = []
        for c in game.get("canvases", []):
            nodes = c.get("nodes") or []
            if not nodes:
                continue
            out = play(page, c["id"], nodes[0].get("id", "base"), settle=0)
            if out is not True:
                broken.append(f"{c['id']}: {str(out)[:50]}")
        rep.check("every canvas renders", not broken,
                  f"{len(game.get('canvases', []))} canvases, none threw" if not broken
                  else f"{len(broken)} threw · " + " · ".join(broken[:3]))

    # 6 · every location the engine knows resolves
    locs = locations(page)
    dead = [l for l in locs if goto(page, f"Location_{l}", settle=0) is not True]
    rep.check("every location resolves", not dead,
              f"{len(locs)} locations" if not dead else f"dead: {dead[:4]}")

    # 7 · guidance. Both card functions, or a game whose guidance is entirely
    #     per-character reads as an empty page. n/a rather than green when the
    #     game ships no cards at all.
    declared_cards = len((game or {}).get("quest_cards", []) or [])
    if not declared_cards:
        rep.na("the guidance page resolves cards", "no [[quest_cards]] declared")
    else:
        got = quest_cards(page)
        if not isinstance(got, dict):
            rep.check("the guidance page resolves cards", False, str(got)[:60])
        else:
            n = sum(got.values())
            where = ", ".join(f"{k}:{v}" for k, v in got.items() if v)
            rep.check("the guidance page resolves cards", n > 0,
                      f"{n} of {declared_cards} declared cards resolve at turn one"
                      + (f" · {where}" if where else ""))

    # 8 · the world can interrupt the player.
    #     A random canvas rolls against `canvas.chance || 0` (v2.py:5452), so one
    #     with no chance can never fire however long you roll. Separated from the
    #     roll deliberately: "declared but impossible" and "declared and just did
    #     not come up" look identical in a sample and are completely different bugs.
    rc = random_canvases(page)
    if not rc:
        rep.na("the world interrupts the player", "no trigger_mode = \"random\" canvases")
    else:
        dead = [c for c in rc if not c.get("chance")]
        rep.check("every random event can fire at all", not dead,
                  f"{len(rc)} random canvases, all carry a chance" if not dead else
                  f"{len(dead)}/{len(rc)} have no `chance` — they can NEVER fire "
                  f"({', '.join(c['id'] for c in dead[:3])}"
                  f"{' …' if len(dead) > 3 else ''})")
        # Sweep the clock. One hardcoded hour reads a night game as a dead world:
        # `late_shifts` has 18 rollable ambients and `isCanvasValid` rejects every
        # one of them at Mon 12:00 because the whole game is scheduled after dark.
        rollable = sorted({c["location"] for c in rc if c.get("chance")})
        if rollable:
            fired, hours = set(), [2, 8, 12, 16, 20, 23]
            for hour in hours:
                set_time(page, "Monday", hour)
                for loc in rollable:
                    if loc not in fired and sample_ambients(page, loc, rolls=40):
                        fired.add(loc)
            rep.check("a random event actually fires", bool(fired),
                      f"{len(fired)}/{len(rollable)} locations resolved one "
                      f"across {len(hours)} hours of a Monday")

    # 9 · nothing threw during any of that
    rep.check("no uncaught page errors", not errors,
              "; ".join(errors[:2])[:120] if errors else "")

    return rep


# ─────────────────────────────────────────────────────────────────────────────

def _resolve(arg, build_override=None):
    """slug -> games/<slug>/output/index.html + its source, or an explicit path.

    `--build` keeps the slug's TOML while pointing at a different artefact, which is
    the normal case for anything mid-release: `games/mrs_vance/output/` is deliberately
    not refreshed until ship, so it is played from a scratch build. Without the source
    the meter and canvas checks have nothing to compare against and silently drop out.
    """
    if arg.endswith(".html"):
        return arg, None
    toml = f"games/{arg}/toml_phases/7_final_game.toml"
    build = build_override or f"games/{arg}/output/index.html"
    return build, (toml if os.path.exists(toml) else None)


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    override = None
    if "--build" in argv:
        i = argv.index("--build")
        if i + 1 >= len(argv):
            print("usage: playtest.py <slug> --build <path/to/index.html>")
            return 2
        override = argv[i + 1]
    build, toml = _resolve(argv[0], override)
    headed = "--headed" in argv
    if not os.path.exists(build):
        print(f"not found: {build}")
        return 2
    game = _load(toml) if toml else None

    print(f"\n  playtest — {build}")
    with open_game(build, headless=not headed) as (page, errors):
        rep = universal(page, errors, game,
                        Report("the universal checks — what only a live run answers"))
        return rep.done()


if __name__ == "__main__":
    sys.exit(main())
