#!/usr/bin/env python3
"""shape.py — checkpoint A: do the spine's decisions hold together?

Reads `games/<slug>/v2_state.json` ONLY, so it runs before a line of TOML exists. It judges the
spine (`references/the-spine.md`, SP1–SP7), never the prose or the built game — that is
`gates.py`'s job. Every row prints PASS / FAIL / n/a; any FAIL exits 1.

    python3 scripts/shape.py <slug>             # strict once the phase is `spine` or later
    python3 scripts/shape.py <slug> --finish    # strict now: run it to finish the spine phase
    python3 scripts/shape.py <slug> --json

⚠️ LENIENT BEFORE, STRICT AFTER (LO, 2026-09-28). While the spine is being written (phase `idea`)
a missing piece is n/a: there is nothing to check yet. Once the game is finishing the spine
(`--finish`) or past it (phase `spine`, `board`, `sheets`, `release`), the required pieces must
exist — every SP page READY, signed and dated, the release page, a ladder for each person on it, the
promise and the beat that keeps it alive — and a missing one FAILS. An empty ledger never passes a
finished spine: an absence is not a pass.

One row is strict in every mode: every person is an adult. A person in `want.cast` or
`board.characters` with no age, or under 18, FAILS while the spine is still being written too.

Flags in a step's gate are LISTED, not failed: the ledger does not record which canvas sets a
flag, so "undeclared" cannot be told from "set by a canvas not written yet". The TOML-side
`ladders move forward` gate proves every unlock is earnable once the canvases exist.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gates  # noqa: E402

SP_IDS = [f"SP{i}" for i in range(1, 8)]
STRICT_PHASES = {"spine", "board", "sheets", "release"}


def _ladders(state):
    """{npc_id: ladder} for every declared ladder with at least one step."""
    board = (state or {}).get("board") or {}
    return {c.get("id"): c["ladder"] for c in (board.get("characters") or [])
            if isinstance(c, dict) and isinstance(c.get("ladder"), dict)
            and (c["ladder"].get("steps") or [])}


def _person(p):
    return p if isinstance(p, str) else (p or {}).get("id") or (p or {}).get("npc")


KEEPS = ("step counter + memory flags", "want + warmth", "want + power")


def check(state, strict=False, slug=None):
    """[(name, ok, headline, detail)] — ok True / False / None (n/a) / "warn" (listed, never a FAIL).

    `slug` (else the ledger's own `slug`) names the game: a game in `gates.SHIP_GRANDFATHERED`
    WARNS where the newer rows (keeps, a card per system) would FAIL it, until it next ships.
    """
    state = state or {}
    grandfathered = (slug or state.get("slug")) in gates.SHIP_GRANDFATHERED
    board = state.get("board") or {}
    want = state.get("want") or {}
    rp = state.get("release_page") or {}
    ladders = _ladders(state)
    steps = [(npc, s) for npc, lad in ladders.items() for s in (lad.get("steps") or [])
             if isinstance(s, dict)]
    rows = []

    def row(name, ok, head, detail=None):
        rows.append((name, ok, head, detail or []))

    # 1 · a step's place is declared (SP2). Places come with the board, which follows the spine.
    # THIS release's places when the release page lists them (PRD v2 CK5 · H11): a place cut
    # from the release is still on the board, and a step there cannot be played.
    rp_places = [p if isinstance(p, str) else (p or {}).get("id")
                 for p in (rp.get("places") or []) if isinstance(p, (str, dict))]
    if rp_places:
        locs, src = set(rp_places), "release_page.places"
    else:
        locs = {l.get("id") for l in (board.get("locations") or []) if isinstance(l, dict)}
        src = "board.locations"
    if not steps:
        row("a step's place is declared", None, "n/a — no ladder steps")
    elif not locs:
        row("a step's place is declared", None, "n/a — no board.locations yet (places come with the board)")
    else:
        bad = [f"{n} step {s.get('n')}: `{s.get('where')}` is not in {src}"
               for n, s in steps if s.get("where") not in locs and s.get("fires_from") != "opening"]
        row("a step's place is declared", not bad,
            f"{len(steps) - len(bad)}/{len(steps)} steps (read from {src})", bad)

    # 2 · a step's hours are a window (SP2). A step with `fires_from = "opening"` fires at a
    # new game, not at an hour, so it has no window to check (PRD v2 CK1 · H3).
    if not steps:
        row("a step's hours are a window", None, "n/a — no ladder steps")
    else:
        bad = []
        for n, s in steps:
            if s.get("fires_from") == "opening":
                continue
            w = s.get("when") or {}
            days = [gates._ladder_day(d) for d in (w.get("days") or [])]
            if not days or None in days or not w.get("from") or not w.get("to"):
                bad.append(f"{n} step {s.get('n')}: `when` must be days, from and to — got {w}")
        row("a step's hours are a window", not bad, f"{len(steps) - len(bad)}/{len(steps)} steps", bad)

    # 3 · a step's variables are declared (SP2) — traits fail, flags are listed
    declared = {lad.get("counter") for lad in ladders.values() if lad.get("counter")}
    declared |= set(board.get("ascent_tiers") or [])
    declared |= set((board.get("ceilings") or {}).keys())
    declared |= {n.get("key") for n in (board.get("needs") or []) if isinstance(n, dict)}
    for c in board.get("characters") or []:
        if isinstance(c, dict):
            declared |= set((c.get("meters") or {}).keys())
    if (board.get("economy") or {}).get("currency"):
        declared.add(board["economy"]["currency"])
    # The meters (`board.meters[].key`, and an old meter-shaped row in `board.systems[]`) and what
    # each system card feeds and reads are declared too (the-systems.md S2a).
    declared |= {m.get("key") for m in gates._meters_of_board(board) if m.get("key")}
    for card in board.get("systems") or []:
        if isinstance(card, dict):
            declared |= {k for k in (card.get("feeds") or []) + (card.get("reads") or [])
                         if isinstance(k, str)}
    flags = set()
    if not steps:
        row("a step's variables are declared", None, "n/a — no ladder steps")
    else:
        bad = []
        for n, s in steps:
            for it in s.get("gate") or []:
                if not isinstance(it, dict):
                    continue
                if it.get("trait") and it["trait"] not in declared:
                    bad.append(f"{n} step {s.get('n')}: trait `{it['trait']}` is declared nowhere in the ledger")
                if it.get("flag"):
                    flags.add(it["flag"])
        row("a step's variables are declared", not bad,
            f"{len(steps)} steps · traits checked, {len(flags)} flag(s) listed below", bad)

    # 3b · a person's meter has a type and a range (PRD v2 DC9d · H29). `meters[k]` is
    # `{type, min, max}`; the older bare description string still declares the name (row 3), so
    # it WARNS here rather than failing — a name alone says nothing about its range or reader.
    mdecl = [(c.get("id"), k, v) for c in (board.get("characters") or []) if isinstance(c, dict)
             for k, v in ((c.get("meters") or {}).items())]
    if not mdecl:
        row("a person's meter has a type and range", None, "n/a — no board.characters[].meters")
    else:
        bare = [f"{who}.{k}: a description string — write {{type, min, max}}"
                for who, k, v in mdecl
                if not (isinstance(v, dict) and v.get("type") and "min" in v and "max" in v)]
        row("a person's meter has a type and range", "warn" if bare else True,
            f"{len(mdecl) - len(bare)}/{len(mdecl)} meters typed", bare)

    # 4 · dependencies resolve (SP3)
    deps = [d for d in (state.get("dependencies") or []) if isinstance(d, dict)]
    if not deps:
        row("dependencies resolve", None, "n/a — no dependencies declared")
    else:
        have = {(n, s.get("n")) for n, s in steps}
        bad, edges = [], {}
        for d in deps:
            frm, nd = d.get("from") or {}, d.get("needs") or {}
            a = (frm.get("npc"), frm.get("step"))
            if a not in have:
                bad.append(f"from {a[0]} step {a[1]}: no such step")
            if "step" in nd:
                b = (nd.get("npc"), nd.get("step"))
                if b not in have:
                    bad.append(f"{a[0]} step {a[1]} needs {b[0]} step {b[1]}: no such step")
                edges.setdefault(a, []).append(b)
            elif not (nd.get("window") or nd.get("place")):
                bad.append(f"{a[0]} step {a[1]}: `needs` names no step, window or place")
        seen, stack, cyc = set(), set(), []

        def visit(v):
            if v in stack:
                cyc.append(v)
                return
            if v in seen:
                return
            seen.add(v)
            stack.add(v)
            for w in edges.get(v, []):
                visit(w)
            stack.discard(v)

        for v in list(edges):
            visit(v)
        bad += [f"a dependency cycle runs through {v[0]} step {v[1]}" for v in cyc[:3]]
        row("dependencies resolve", not bad, f"{len(deps)} declared", bad)

    # 5 · the pressure can be met (SP4)
    eco = board.get("economy") or {}
    money = want.get("hold_kind") == "bill" or "obligation_amount" in eco
    if not money:
        row("the pressure can be met", None, "n/a — the hold is not money")
    elif not isinstance(eco.get("week_income"), (int, float)) or not isinstance(eco.get("obligation_amount"), (int, float)):
        row("the pressure can be met", False if strict else None,
            "board.economy has no week_income or obligation_amount (SP4)")
    elif not isinstance(rp.get("weeks"), (int, float)):
        row("the pressure can be met", False if strict else None, "release_page.weeks is not declared (SP7)")
    else:
        every = eco.get("obligation_every_weeks") or 1
        due = math.ceil(rp["weeks"] / every)
        # A RISING BILL (PRD v2 CK5 · I12). `board.pressure.stages` mirrors the engine's
        # `[settings.rent] stages` (EN2a): each payment is the amount of the highest stage
        # whose `after_total_paid` has been reached, so the bill is walked week by week.
        # Without stages it is today's starting amount times the due weeks.
        stages = [st for st in (((board.get("pressure") or {}).get("stages")) or [])
                  if isinstance(st, dict) and isinstance(st.get("amount"), (int, float))]
        if stages:
            owed, paid = 0, 0
            for _ in range(due):
                reached = [st for st in stages if (st.get("after_total_paid") or 0) <= paid]
                amt = max(reached, key=lambda st: st.get("after_total_paid") or 0)["amount"] \
                    if reached else eco["obligation_amount"]
                owed += amt
                paid += amt
            how = f"rising in {len(stages)} stage(s)"
        else:
            owed, how = eco["obligation_amount"] * due, "flat"
        earned = eco["week_income"] * rp["weeks"]
        # `obligation_moves` is free text: printed beside the sum, never judged.
        moves = f" · moves: {eco['obligation_moves']}" if eco.get("obligation_moves") else ""
        if earned >= owed:
            row("the pressure can be met", True,
                f"{earned} earnable against {owed} owed ({how}) over {rp['weeks']} week(s){moves}")
        elif eco.get("shortfall"):
            row("the pressure can be met", True,
                f"{earned} against {owed} ({how}) — short on purpose: {eco['shortfall']}{moves}")
        else:
            row("the pressure can be met", False,
                f"{earned} earnable against {owed} owed ({how}) over {rp['weeks']} week(s), and no "
                f"board.economy.shortfall says it is on purpose{moves}")

    # 6 · everyone on the release page has a ladder (SP7)
    people = [_person(p) for p in (rp.get("people") or [])]
    if not rp:
        row("everyone on the release page has a ladder", False if strict else None,
            "no release_page (SP7)")
    elif not people:
        row("everyone on the release page has a ladder", False if strict else None,
            "release_page.people is empty (SP7)")
    else:
        bad = [f"{p}: no ladder with steps (SP2)" for p in people if p not in ladders]
        row("everyone on the release page has a ladder", not bad,
            f"{len(people) - len(bad)}/{len(people)} people", bad)

    # 7 · every step has a guidance line (SP2)
    if not steps:
        row("every step has a guidance line", False if strict else None, "no ladder steps (SP2)")
    else:
        bad = [f"{n} step {s.get('n')}: no `hint`" for n, s in steps if not str(s.get("hint") or "").strip()]
        row("every step has a guidance line", not bad, f"{len(steps) - len(bad)}/{len(steps)} steps", bad)

    # 8 · the door is a declared step (SP7)
    door = rp.get("door") if isinstance(rp.get("door"), dict) else {}
    canvases = {s.get("canvas") for _n, s in steps}
    if not door.get("canvas"):
        row("the door is a declared step", False if strict else None, "release_page.door is not declared (SP7)")
    else:
        ok = door["canvas"] in canvases
        row("the door is a declared step", ok, f"door {door['canvas']}",
            [] if ok else [f"`{door['canvas']}` is not a ladder step's canvas"])

    # 9 · the promise has a beat this release (IC16, SP7)
    prom_raw = want.get("promise")
    prom = prom_raw if isinstance(prom_raw, dict) else {}       # a string used to crash here
    if not (prom.get("goal") or prom.get("mystery")):
        row("the promise has a beat this release", False if strict else None,
            "want.promise names no goal or mystery (the idea page §2)")
    elif not str(rp.get("promise_alive") or "").strip():
        row("the promise has a beat this release", False if strict else None,
            "release_page.promise_alive is empty — which beat keeps the goal or mystery alive?")
    else:
        row("the promise has a beat this release", True, str(rp["promise_alive"])[:80])

    # 9b · the goal chain (PRD v2 NC5 · D8a · D8b · C2). The goal has no date (LO decided, D8): a
    # sidebar countdown only displays, so a date promises an ending the engine never runs. And a
    # goal that can end names the next one (`want.promise.goals[] = {goal, ends_when, next}`),
    # because the game never stalls. `the-want.md` §2.
    raw_goals = prom.get("goals")
    goals = [g for g in raw_goals if isinstance(g, dict)] if isinstance(raw_goals, list) else []
    bad = []
    if prom_raw not in (None, "", {}) and not isinstance(prom_raw, dict):
        bad.append(f"want.promise must be a table — got {prom_raw!r} (bad input)")
    if raw_goals is not None and not isinstance(raw_goals, list):
        bad.append(f"want.promise.goals must be a list of tables — got {raw_goals!r} (bad input)")
    elif isinstance(raw_goals, list):
        bad.extend(f"want.promise.goals[{i}] must be a table — got {g!r} (bad input)"
                   for i, g in enumerate(raw_goals) if not isinstance(g, dict))
    if prom.get("date") not in (None, ""):
        bad.append(f"want.promise.date = {prom['date']!r} — the goal has no date (D8)")
    for i, g in enumerate(goals):
        label = str(g.get("goal") or f"goals[{i}]")[:50]
        if g.get("date") not in (None, ""):
            bad.append(f"\"{label}\": has a date ({g['date']!r}) — the goal has no date (D8)")
        if str(g.get("ends_when") or "").strip() and not str(g.get("next") or "").strip():
            bad.append(f"\"{label}\": ends_when is set and next is not — a goal that can end names "
                       f"the next one")
    if not (prom.get("goal") or prom.get("mystery") or goals or bad):
        row("the goal chain holds", None, "n/a — want.promise names no goal yet")
    else:
        ending = sum(1 for g in goals if str(g.get("ends_when") or "").strip())
        row("the goal chain holds", not bad,
            f"{len(goals)} goal(s), {ending} can end · no date" if not bad else
            f"{len(bad)} problem(s) in want.promise", bad)

    # 10 · a READY page is signed (the spine's page rules).
    # D13 (LO decided, 2026-09-30): LO signs whenever LO has read the page. The day-after
    # compare of `signed_at` with `drafted_at` is gone; it blocked a real same-day approval
    # and had no evidence behind it (review G1), and with it went the need for a waiver
    # key (H15). H7: in lenient mode, no READY page is n/a — "0/7 READY" is not a pass.
    pages = {p.get("id"): p for p in ((state.get("spine") or {}).get("pages") or []) if isinstance(p, dict)}
    ready = sum(1 for p in pages.values() if p.get("status") == "READY")
    bad = []
    for sp in SP_IDS:
        p = pages.get(sp)
        if p is None:
            if strict:
                bad.append(f"{sp}: not written")
            continue
        if p.get("status") != "READY":
            if strict:
                bad.append(f"{sp}: status {p.get('status') or 'unset'}, not READY")
            continue
        if not p.get("signed_by") or not p.get("signed_at"):
            bad.append(f"{sp}: READY but not signed")
    if not pages and not strict:
        row("every spine page is signed", None, "n/a — no spine pages yet")
    elif not ready and not strict:
        row("every spine page is signed", None, "n/a — no spine page READY yet")
    else:
        row("every spine page is signed", not bad, f"{ready}/{len(SP_IDS)} READY", bad)

    # 11 · the person is there at the step's hour (PRD v2 CK5 · I13). Optional
    # `board.characters[].schedule = [{where, weekdays, from, to}]` is the person's hours.
    # Each step's window, on each of its days, must be FULLY covered by the union of that
    # person's rows at the step's place (`gates._window_uncovered`, past midnight included).
    # A step the opening plays is exempt: it has no hour.
    scheds = {c.get("id"): c["schedule"] for c in (board.get("characters") or [])
              if isinstance(c, dict) and isinstance(c.get("schedule"), list)}
    # A row the check cannot read is bad input, never "does not cover" (phase 5): a misspelled
    # weekday, or a row in the TOML's own words (`location`/`start_time`/`end_time`), used to
    # drop out silently and blame the person's hours. That person's steps are not judged.
    sched_bad, unreadable = [], set()
    for n, rws in scheds.items():
        before = len(sched_bad)
        for i, r in enumerate(rws):
            if not isinstance(r, dict):
                sched_bad.append(f"{n} schedule[{i}] must be a table — got {r!r}")
                continue
            toml_words = [k for k in ("location", "start_time", "end_time") if k in r]
            if toml_words:
                sched_bad.append(f"{n} schedule[{i}]: {', '.join(toml_words)} are the TOML's names — "
                                 "this row is read as {where, weekdays, from, to}")
            elif not r.get("where"):
                sched_bad.append(f"{n} schedule[{i}]: no `where`")
            wd = r.get("weekdays")
            if wd is not None and not isinstance(wd, list):
                sched_bad.append(f"{n} schedule[{i}]: weekdays must be a list — got {wd!r}")
            elif wd:
                sched_bad.extend(f"{n} schedule[{i}]: unknown weekday {d!r}"
                                 for d in wd if gates._ladder_day(d) is None)
        if len(sched_bad) > before:
            unreadable.add(n)
    judged, bad = 0, list(sched_bad)
    for n, s in steps:
        if n not in scheds or n in unreadable or s.get("fires_from") == "opening":
            continue
        w = s.get("when") or {}
        days = [gates._ladder_day(d) for d in (w.get("days") or [])]
        if not days or None in days or not w.get("from") or not w.get("to"):
            continue                                   # row 2 reports a broken window
        rows_here = []
        for r in scheds[n]:
            if not isinstance(r, dict) or r.get("where") != s.get("where"):
                continue
            wd = r.get("weekdays")
            rows_here.append((None if wd is None else [gates._ladder_day(d) for d in wd],
                              r.get("from", "00:00"), r.get("to", "23:59")))
        judged += 1
        missing = gates._window_uncovered(days, w["from"], w["to"], rows_here)
        if missing:
            bad.append(f"{n} step {s.get('n')}: {n}'s schedule does not cover {s.get('where')} "
                       f"{w['from']}-{w['to']} on {', '.join(gates._PR_DAYS[d] for d in missing)}")
    if not judged and not sched_bad:
        row("the person is there at the step's hour", None,
            "n/a — no step belongs to a person with board.characters[].schedule")
    else:
        row("the person is there at the step's hour", not bad,
            f"{judged - (len(bad) - len(sched_bad))}/{judged} steps"
            + (f" · {len(sched_bad)} bad input" if sched_bad else ""), bad)

    # 12 · a step's gate can be reached (PRD v2 DC9b · H31). Optional step `raises = {trait: n}`,
    # `board.daily_raises = {trait: per_day}` and `board.repeat_raises = {trait: per_visit}` (a
    # repeatable in the TOML raises it). Only traits a step's `raises` names are judged; a trait the
    # daily tick or a repeatable raises can always be reached, and any other trait is not this
    # check's to fail. A gte/gt gate passes if the trait's starting value (his: `meters[k].start`,
    # else `.min`; hers, a gate with no `npc`: `board.player_start[k]`; else 0) plus the raises of
    # the steps before it reaches the value. "Before" = the same
    # person's lower steps, plus every step it depends on (SP3), transitively; a gate with `npc`
    # counts only that person's raises. Bad input is listed, never a crash.
    def _num(v):
        if isinstance(v, bool):
            return None
        if isinstance(v, (int, float)):
            return v
        try:
            return float(v) if isinstance(v, str) and v.strip() else None
        except ValueError:
            return None

    def _raise_table(key):
        t = (board.get(key) or {})
        return {k: v for k, v in t.items() if (_num(v) or 0) > 0} if isinstance(t, dict) else {}

    always = set(_raise_table("daily_raises")) | set(_raise_table("repeat_raises"))
    bad_input, by_key = [], {}
    for n, s in steps:
        sn = _num(s.get("n"))
        if sn is None:
            bad_input.append(f"{n} step {s.get('n')!r}: `n` is not a number — skipped")
            continue
        r = s.get("raises")
        if r is not None and not isinstance(r, dict):
            bad_input.append(f"{n} step {s.get('n')}: `raises` must be a table — got {r!r}")
        elif isinstance(r, dict):
            for t, v in r.items():
                if _num(v) is None:
                    bad_input.append(f"{n} step {s.get('n')}: `raises.{t}` is not a number — got {v!r}")
        by_key[(n, sn)] = s

    def _raises(step):
        r = step.get("raises")
        return {t: _num(v) for t, v in r.items() if _num(v) is not None} if isinstance(r, dict) else {}

    raised = {t for s in by_key.values() for t in _raises(s)}
    meters = {c.get("id"): (c.get("meters") or {}) for c in (board.get("characters") or [])
              if isinstance(c, dict)}

    # A malformed board.player_start used to read silently as 0; it is bad input now (NC5 batch).
    player_start = board.get("player_start")
    if player_start is not None and not isinstance(player_start, dict):
        bad_input.append(f"board.player_start must be a table — got {player_start!r}")
        player_start = {}
    for t, v in (player_start or {}).items():
        if _num(v) is None:
            bad_input.append(f"board.player_start.{t} is not a number — got {v!r}")
    player_start = player_start or {}

    def _start(npc, trait):
        if npc is None:
            return _num(player_start.get(trait)) or 0          # her own trait
        m = (meters.get(npc) or {}).get(trait)
        if isinstance(m, dict):
            for k in ("start", "min"):
                if _num(m.get(k)) is not None:
                    return _num(m.get(k))
        return 0

    needs = {}
    for d in (state.get("dependencies") or []):
        if isinstance(d, dict) and "step" in (d.get("needs") or {}):
            frm, nd = d.get("from") or {}, d["needs"]
            needs.setdefault((frm.get("npc"), _num(frm.get("step"))), []).append(
                (nd.get("npc"), _num(nd.get("step"))))

    def before(key, seen):
        """Every step that must have happened before `key` — excluding `key` itself."""
        npc, n = key
        out = {k for k in by_key if k[0] == npc and n is not None and k[1] < n}
        for dep in needs.get(key, []):
            out |= {k for k in by_key if k[0] == dep[0] and dep[1] is not None and k[1] <= dep[1]}
        for k in list(out):
            if k not in seen:
                seen.add(k)
                out |= before(k, seen)
        return out

    ps_bad = [b for b in bad_input if b.startswith("board.player_start")]
    if not any(s.get("raises") for _n, s in steps) and ps_bad:
        # A bad player_start is shown even with nothing to judge it against.
        row("a step's gate can be reached", False, f"{len(ps_bad)} bad input", ps_bad)
    elif not any(s.get("raises") for _n, s in steps):
        row("a step's gate can be reached", None, "n/a — no ladder step declares `raises`")
    else:
        judged, bad = 0, list(bad_input)
        for (n, sn), s in by_key.items():
            for it in s.get("gate") or []:
                if not isinstance(it, dict) or it.get("trait") not in raised:
                    continue
                v = _num(it.get("value"))
                if it.get("op") not in ("gte", "gt") or v is None:
                    continue
                judged += 1
                t = it["trait"]
                if t in always:
                    continue
                who = it.get("npc")
                earlier = [k for k in before((n, sn), set()) if who is None or k[0] == who]
                got = _start(who, t) + sum(_raises(by_key[k]).get(t, 0) for k in earlier)
                if got < v or (it["op"] == "gt" and got == v):
                    bad.append(f"{n} step {s.get('n')}: `{t} {it['op']} {it.get('value')}` but the "
                               f"start plus the steps before it reach {got:g}")
        ok = None if not judged and not bad_input else not bad
        row("a step's gate can be reached", ok,
            f"{judged - (len(bad) - len(bad_input))}/{judged} gates reachable"
            + (f" · {len(bad_input)} bad input" if bad_input else "") if judged or bad_input
            else "n/a — no gate reads a trait the ledger raises", bad)

    # 13 · every person is an adult (PRD v2 DC2a · B2). `want.cast[] = {id, age, keeps}` holds the
    # ages; a board character with no cast entry has no age. Not a missing piece that lenient mode
    # waits for: a person declared without an age FAILS in both modes (LO, 2026-09-30).
    cast = {c.get("id"): c for c in (want.get("cast") or []) if isinstance(c, dict) and c.get("id")}
    people = list(cast) + [c.get("id") for c in (board.get("characters") or [])
                           if isinstance(c, dict) and c.get("id") and c.get("id") not in cast]
    bad = []
    for pid in people:
        age = (cast.get(pid) or {}).get("age")
        if pid not in cast:
            bad.append(f"{pid}: on the board but not in want.cast — no age declared")
        elif age is None:
            bad.append(f"{pid}: want.cast has no age")
        elif isinstance(age, bool) or not isinstance(age, (int, float)):
            bad.append(f"{pid}: age must be a number — got {age!r}")
        elif age < 18:
            bad.append(f"{pid}: age {age} is under 18")
    if not people:
        row("every person is an adult", None, "n/a — no person declared yet")
    else:
        row("every person is an adult", not bad, f"{len(people) - len(bad)}/{len(people)} people 18+", bad)

    # 13b · her life's threads (the-want.md §6): each thread's person is in want.cast with an age,
    # and the count is reported — 4–6 is the direction, so outside it WARNS, never fails.
    threads = [t for t in (want.get("threads") or []) if isinstance(t, dict)]
    if not threads:
        row("her life has threads", "warn" if strict else None,
            "no want.threads[] — her life, 4–6 threads (the-want.md §6)" if strict
            else "n/a — no want.threads[] yet")
    else:
        bad = []
        for t in threads:
            pid = t.get("person")
            if pid not in cast:
                bad.append(f"thread {t.get('id')}: person `{pid}` is not in want.cast")
            elif (cast[pid] or {}).get("age") is None:
                bad.append(f"thread {t.get('id')}: `{pid}` has no age in want.cast")
        n = len(threads)
        ok = False if bad else (True if 4 <= n <= 6 else "warn")
        row("her life has threads", ok, f"{n} thread(s)" + ("" if 4 <= n <= 6 else " — the direction is 4–6"), bad)

    # 13c · what each man keeps (the-want.md §6, the-meters.md W1): one of the three, or
    # `none — <why>`. A grandfathered game WARNS. A missing `keeps` fails only when strict.
    kept = [(pid, c.get("keeps")) for pid, c in cast.items()]
    bad = []
    for pid, k in kept:
        if k is None:
            if strict:
                bad.append(f"{pid}: no `keeps`")
        elif not (k in KEEPS or (isinstance(k, str) and k.startswith("none — "))):
            bad.append(f"{pid}: keeps {k!r} — one of {', '.join(KEEPS)}, or `none — <why>`")
    if not kept:
        row("each man's keeps is named", None, "n/a — no want.cast yet")
    else:
        row("each man's keeps is named", ("warn" if grandfathered else False) if bad else True,
            f"{len(kept) - len(bad)}/{len(kept)} people"
            + (" · grandfathered: warns until it next ships" if bad and grandfathered else ""), bad)

    # 14 · every declared system has a card (the-systems.md S2a), strict only. At least one card
    # in `board.systems[]` (an old meter-shaped row is a meter, not a card), and every system a
    # thread names (`want.threads[].system`, except `none …`) is a card. A grandfathered game WARNS.
    cards = {c.get("id") for c in (board.get("systems") or []) if isinstance(c, dict)
             and any(f in c for f in gates._SYSTEM_CARD_FIELDS)}
    named = {t.get("system") for t in threads if isinstance(t.get("system"), str)
             and t["system"].strip() and not t["system"].startswith("none")}
    if not strict:
        row("every system has a card", None, "n/a — checked once the spine is finished")
    else:
        bad = [] if cards else ["board.systems[] holds no system card (a meter-shaped row is a meter)"]
        bad += [f"thread system `{sid}` has no card in board.systems[]" for sid in sorted(named - cards)]
        row("every system has a card", ("warn" if grandfathered else False) if bad else True,
            f"{len(cards)} card(s), {len(named)} named by a thread"
            + (" · grandfathered: warns until it next ships" if bad and grandfathered else ""), bad)

    return rows, sorted(flags)


def is_strict(state, finish=False):
    return finish or (state or {}).get("phase") in STRICT_PHASES


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    target = args[0]
    path = target if target.endswith(".json") else os.path.join("games", target, "v2_state.json")
    if not os.path.exists(path):
        print(f"no ledger at {path}")
        return 2
    state = json.load(open(path))
    strict = is_strict(state, "--finish" in argv)
    rows, flags = check(state, strict, None if target.endswith(".json") else target)
    failed = [r for r in rows if r[1] is False]
    if "--json" in argv:
        print(json.dumps({"strict": strict, "rows": [dict(name=n, ok=o, headline=h, detail=d)
                                                      for n, o, h, d in rows],
                          "flags": flags, "failed": len(failed)}, indent=2))
        return 1 if failed else 0
    print(f"\n  shape.py — does the spine hold together? ({'strict' if strict else 'lenient'}: "
          f"phase {state.get('phase') or 'unset'}{', --finish' if '--finish' in argv else ''})")
    print(f"  {path}")
    print(f"  {'─'*72}")
    for name, ok, head, detail in rows:
        tag = "n/a " if ok is None else "WARN" if ok == "warn" else "PASS" if ok else "FAIL"
        print(f"  [{tag}]  {name:42s} {head}")
        for d in detail[:10]:
            print(f"          · {d}")
    print(f"  {'─'*72}")
    if flags:
        print(f"  flags a step's gate reads — listed, not judged: {', '.join(flags)}")
    warned = sum(1 for r in rows if r[1] == "warn")
    print(f"  {len(rows) - len(failed) - warned - sum(1 for r in rows if r[1] is None)} pass · "
          f"{len(failed)} fail · {warned} warn · {sum(1 for r in rows if r[1] is None)} n/a")
    print()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
