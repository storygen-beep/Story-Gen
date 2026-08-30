#!/usr/bin/env python3
"""
pitch_pack.py — the world a Pitcher is allowed to pitch into.

Usage:
    python3 scripts/pitch_pack.py <game-slug>        # the pack, as text
    python3 scripts/pitch_pack.py <path/to/game.toml>
    python3 scripts/pitch_pack.py <slug> --json      # machine-readable

WHY THIS EXISTS, and why it is a script and not a paragraph in the agent's prompt.

`the-release.md:39` tells the author to run three Pitcher agents with NO SHARED
CONTEXT — independence is the whole point, because common context yields three
shades of one idea. That design has a cost nobody had paid: a Pitcher with no
context does not know what the game already contains. It will pitch a location
that exists, a character who does not, or a mechanic the engine cannot run.

So the pack IS the Pitcher's world. Everything it may name is in here and
nothing else is.

And the shape it must feed is not general. `the-release.md:20-28` walks ten real
content commits from a shipped game and finds:

    Every single one is an event at an existing place with an existing
    character. No new location. No new character. No plot advancement.
    Three of the ten are keyed to player state.

That sentence is the whole specification for this file. It needs to make three
things complete and concrete — PLACES, PEOPLE, and the STATE a pitch can key
to — plus what the release owes (the Want, the open promises) and what a pitch
may cost (the economy).

⚠️ IT SCORES NOTHING AND ALWAYS EXITS 0.

This is the same rule `--words` carries (`gates.py:6663`) and for a harder reason
here. Four checks in this project's history were withdrawn for failing something
correct — study 2's R4, study 6's anchoring check, P0, and the rule-pointer scan's
first cut, which failed an accurate history entry. A fact pack that graded would
be that mistake with no code to fix, because "this location is too thin" is an
opinion and `gates.py <slug>` is where opinions with evidence behind them live.

Every number below is a COUNT or the author's OWN declared figure from
`v2_state.json`. Where the two disagree the pack prints both and says nothing
about which is right.

⚠️ IT REUSES `gates.build()` AND DOES NOT RE-PARSE.

Same argument that made `playtest.py` the right shape: every signature somebody
re-derives is a signature somebody gets wrong. In this file's own subject matter
the traps are live —

  · a condition names its trait `trait_key`, an effect names it `trait`
  · a condition names its owner `subject`/`npc_id`, an effect `targetType`/`npcId`
  · a triggerless canvas inherits its location from whatever links to it
    (`gates.build`'s `resolve`), so reading `trigger.location` alone loses them
  · a group's children live at `blocks` OR at `props.blocks`

`gates.build()` already knows all four. Nothing here re-implements one.
"""

import sys
import os
import json
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gates                                                    # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# Loading — the two halves of a game, and neither one is optional to READ
# ─────────────────────────────────────────────────────────────────────────────
# The TOML is what was BUILT. `v2_state.json` is what was DECLARED — the Want,
# the board, the promises, the releases. A pitch has to serve the second and
# land on the first, so the pack carries both and marks which side each fact
# came from. The state file is missing for 22 of 30 games in `games/`, so its
# absence is normal and never an error.

def _paths(arg):
    if arg.endswith(".toml"):
        toml = arg
        slug = os.path.basename(os.path.dirname(os.path.dirname(arg)))
    else:
        slug = arg
        toml = f"games/{slug}/toml_phases/7_final_game.toml"
    return slug, toml, f"games/{slug}/v2_state.json"


def _state(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


# ─────────────────────────────────────────────────────────────────────────────
# The board's shape is NOT uniform, and pretending otherwise loses games
# ─────────────────────────────────────────────────────────────────────────────
# Measured across the eight games that carry a `v2_state.json`: only four keys
# are universal on `board` — `ascent_tiers`, `ceilings`, `characters`,
# `locations`. `economy` is in seven, `map` in six, and the declared meter ladder
# appears under THREE different keys in three shapes:
#
#   forty_miles / the_allowance / seventh_day   board.rungs        [15, 35, 55]
#   the_season                                  board.tier_rungs   {trait: [...]}
#   mrs_vance                                   board.cast_meters.rungs {npc: [...]}
#
# So every reader below is tolerant by construction. A key that is not there is
# reported as not declared — never defaulted, never inferred, and never a defect.

def _declared_rungs(board):
    """[(label, owner, traits, rungs)] from whichever of the three shapes was used.

    ⚠️ RETURNS THE OWNER AND THE TRAIT SEPARATELY, deliberately. The first cut of
    this function returned a formatted label and the caller matched the built
    ladder against it with `owner in label or trait in label`. On mrs_vance that
    starred `npc_cade · want` rung 5 — a number no canvas gates cade's `want` at.
    It came from npc_tobin, because the substring `want` is in every cast label.
    The pack printed a fact that was not true of the game, which is the one thing
    it may never do.

    `traits` is a LIST because the flat-list shape names its tiers separately in
    `ascent_tiers` and shares one set of rungs across all of them.
    """
    out = []
    cast = board.get("cast_meters")
    if isinstance(cast, dict) and isinstance(cast.get("rungs"), dict):
        word = cast.get("word") or "the cast meter"
        for k, v in cast["rungs"].items():
            if isinstance(v, list):
                out.append((f"{k} · {word}", str(k), [word], list(v)))
    for key in ("tier_rungs", "rungs"):
        val = board.get(key)
        if isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, list):
                    out.append((f"player · {k}", "player", [str(k)], list(v)))
    rungs = board.get("rungs")
    if isinstance(rungs, list) and rungs:
        tiers = [str(t) for t in (board.get("ascent_tiers") or [])]
        label = "player · " + (" / ".join(tiers) if tiers else "ascent")
        out.append((label, "player", tiers, list(rungs)))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# The built side
# ─────────────────────────────────────────────────────────────────────────────

def _schedule_index(game):
    """{location_id: [npc_id]} and {npc_id: [(location, days, window, activity)]}.

    Presence is read from the DECLARED schedule rows, which is what the navigation
    panel reads too. It is not a claim about where a character can actually be
    found at a given hour — `playtest.py` answers that against a running engine,
    and the two have disagreed before.

    ⚠️ AND IT IS NOT A CANVAS TRIGGER. On this pack's first live run a Pitcher read
    npc_cade's `the_bar FS 21:00-23:59` row back as the gate on `hub_cade_bar` and
    wrote "already runs weekdays = [4, 5], 21:00-23:59" into its pitch. That canvas
    carries no weekdays and no times at all. The row was true; the sentence built on
    it was not. The output now says so in as many words, because a fact that invites
    a wrong inference is the pack's problem and not the agent's.
    """
    at_loc = collections.defaultdict(list)
    by_npc = collections.defaultdict(list)
    for npc in game.get("npcs") or []:
        nid = npc.get("id")
        for row in npc.get("schedules") or []:
            loc = row.get("location")
            if not loc:
                continue
            if nid not in at_loc[loc]:
                at_loc[loc].append(nid)
            by_npc[nid].append((loc,
                                row.get("weekdays") or [],
                                f"{row.get('start_time', '?')}-{row.get('end_time', '?')}",
                                (row.get("activity") or "")))
    return at_loc, by_npc


def _condition_sites(canvas):
    """Every condition in a canvas, tagged with WHICH GATE it is.

    ⚠️ THE FIRST CUT READ TWO SITES AND MISSED FOUR FIFTHS OF THE GAME. It walked
    the canvas trigger and the exit block's config and choices, which is what
    `gates.build()` flattens, and reported that mrs_vance gates NOTHING on
    `player.standing`. A full walk of the same file finds 22 `standing` condition
    sites. They are in `trigger.substitutions[].conditions` and in
    `nodes[].blocks[].conditions` — Lane 3 dispatch, and the prose bands, which is
    where a colour meter does all of its work.

    A pack that omits a meter's only 22 uses has asserted something false by
    silence, which is worse than printing it wrong: nothing in the output invites
    the reader to check.

    The four kinds are NOT interchangeable and the tag is the point:

      entry     `trigger.conditions`          whether the canvas can fire at all
      dispatch  `trigger.substitutions[]`     which canvas a Lane 3 host swaps to
      choice    `exit_block` config/choices   whether a link is offered
      band      `nodes[].blocks[]`            which prose variant renders

    Yields (kind, condition_item).
    """
    trig = canvas.get("trigger") or {}
    for it in gates._conditions_of(trig):
        yield "entry", it
    for sub in (trig.get("substitutions") or []):
        for it in gates._conditions_of(sub):
            yield "dispatch", it

    def blocks(bl):
        for b in bl or []:
            if not isinstance(b, dict):
                continue
            for it in gates._conditions_of(b):
                yield it
            props = b.get("props") or {}
            # Both shapes: a group's children live at `blocks` or at `props.blocks`,
            # and a cascade's beats carry their own block lists.
            for nested in (b.get("blocks"), props.get("blocks")):
                yield from blocks(nested)
            for cb in (props.get("beats") or []):
                yield from blocks(cb.get("blocks"))

    for n in canvas.get("nodes") or []:
        eb = n.get("exit_block") or {}
        for holder in [eb.get("config") or {}] + list(eb.get("choices") or []):
            for it in gates._conditions_of(holder):
                yield "choice", it
        for it in blocks(n.get("blocks")):
            yield "band", it


def _ladders(model):
    """Every meter threshold the game GATES on, by owner and by which gate it is.

    Keyed (subject, npc_id, trait) read off the condition itself — `subject` and
    `npc_id`, never inferred from the canvas's own `npc` binding. A canvas bound
    to one character routinely gates on another's meter or on the player's, and
    inferring the owner from the binding silently files those under the wrong name.
    """
    lad = collections.defaultdict(lambda: collections.defaultdict(set))
    kinds = collections.defaultdict(collections.Counter)
    for c in model:
        for kind, it in _condition_sites(c["raw"]):
            key = it.get("trait_key")
            if not key:
                continue
            owner = it.get("npc_id") if it.get("subject") == "npc" else "player"
            val = it.get("value")
            kinds[(owner, key)][kind] += 1
            if isinstance(val, (int, float)):
                lad[(owner, key)][val].add(c["id"])
    return lad, kinds


def _flag_reads(model):
    """{flag: {kind: count}} across all four gate kinds, not just the two."""
    reads = collections.defaultdict(collections.Counter)
    for c in model:
        for kind, it in _condition_sites(c["raw"]):
            if it.get("flag_key"):
                reads[it["flag_key"]][kind] += 1
    return reads


def _sign(val):
    """+1 / -1 / 0 for an effect value, INCLUDING the random shape.

    ⚠️ An effect value is not always a number. `vesper` writes 32 of them as
    `{ type = "random", min = 8, max = 14 }`, and an `isinstance(val, (int, float))`
    filter drops every one of them silently. That exact filter, in a throwaway probe,
    reported `player.loop_npc_pleasure` as "gated at 50 but only ever set, max 0" —
    a meter the game climbs 8-14 at a time, and the only "finding" a nine-game sweep
    produced. It was the probe, not the game.

    Today no game randomises money, so nothing downstream changes; this is here so
    that the first one that does is not silently uncounted.
    """
    if isinstance(val, (int, float)):
        return (val > 0) - (val < 0)
    if isinstance(val, dict):
        lo, hi = val.get("min"), val.get("max")
        for v in (lo, hi):
            if isinstance(v, (int, float)) and v:
                return (v > 0) - (v < 0)
    return 0


def _movers(game):
    """Which canvases MOVE a meter, and by how much — the other half of a ladder.

    An effect names its trait `trait` and its owner `targetType`/`npcId`. The
    condition side uses `trait_key` and `subject`/`npc_id`. Reading one side's
    key names against the other returns nothing and looks exactly like a game
    with no effects in it.
    """
    mv = collections.defaultdict(list)
    flags_set = collections.defaultdict(list)
    for c in game.get("canvases") or []:
        cid = c.get("id")
        for n in c.get("nodes") or []:
            eb = n.get("exit_block") or {}
            for h in [eb.get("config") or {}] + list(eb.get("choices") or []):
                for ef in (h.get("effects") or []):
                    key = ef.get("trait") or ef.get("trait_key")
                    if not key:
                        continue
                    owner = ef.get("npcId") if ef.get("targetType") == "npc" else "player"
                    mv[(owner, key)].append((cid, ef.get("op"), ef.get("value")))
                for fe in (h.get("flagEffects") or []):
                    if fe.get("flag"):
                        flags_set[fe["flag"]].append((cid, fe.get("op")))
    return mv, flags_set


# ─────────────────────────────────────────────────────────────────────────────
# Rendering
# ─────────────────────────────────────────────────────────────────────────────

def _rule(title):
    print()
    print(title)
    print("─" * max(len(title), 60))


def _wrap(text, width=88, indent="      ", first=None):
    """Hanging indent. `first` is the bullet; continuation lines get `indent`.

    The first cut printed `indent` on every line, so a wrapped promise came out as
    four bullets instead of one and read as four separate promises.
    """
    words, line, out = str(text).split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        out.append(line)
    for i, ln in enumerate(out):
        print((first if i == 0 and first else indent) + ln)


def _want_value(v, indent="      "):
    """One Want field, whatever shape the author wrote it in.

    ⚠️ NOT string-only. The first cut printed `isinstance(v, str)` fields and
    silently dropped everything else, which on mrs_vance meant `crude_ceiling`
    — the field that says how far this game's prose may go — rendered as a bare
    heading with nothing under it. A Pitcher reading that pack would have had
    the ceiling withheld from it.
    """
    if isinstance(v, str):
        if v.strip():
            _wrap(v, indent=indent)
    elif isinstance(v, dict):
        for kk, vv in v.items():
            if isinstance(vv, (str, int, float, bool)):
                _wrap(f"{kk}: {vv}", indent=indent)
            else:
                print(f"{indent}{kk}:")
                _want_value(vv, indent=indent + "  ")
    elif isinstance(v, list):
        for item in v:
            _want_value(item, indent=indent)
    elif v is not None:
        _wrap(str(v), indent=indent)


DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _days(idx):
    if not idx:
        return "—"
    if len(idx) == 7:
        return "daily"
    try:
        return "".join(DAYS[i][0] for i in sorted(idx))
    except (IndexError, TypeError):
        return str(idx)


def pack(slug, toml_path, state_path, as_json=False):
    game = gates._load(toml_path)
    model, _ = gates.build(game)
    st = _state(state_path) or {}
    board = st.get("board") or {}
    want = st.get("want") or {}

    at_loc, by_npc = _schedule_index(game)
    lad, kinds = _ladders(model)
    mv, flags_set = _movers(game)

    declared_loc = {d.get("id"): d for d in (board.get("locations") or [])
                    if isinstance(d, dict)}
    declared_npc = {d.get("id"): d for d in (board.get("characters") or [])
                    if isinstance(d, dict)}

    # Per-location build facts.
    by_loc = collections.defaultdict(list)
    for c in model:
        by_loc[c["loc"]].append(c)

    locs = []
    for loc in game.get("locations") or []:
        lid = loc.get("id")
        here = by_loc.get(lid, [])
        words = sum(b.words for c in here for b in c["beats"])
        locs.append(dict(
            id=lid, name=loc.get("name") or lid,
            canvases=len(here),
            repeatable=sum(1 for c in here if c["rep"]),
            random=sum(1 for c in here if c["random"]),
            words=words,
            people=at_loc.get(lid, []),
            declared_fill=(declared_loc.get(lid) or {}).get("fill"),
            declared_finished=(declared_loc.get(lid) or {}).get("fill_finished"),
            anchor=bool((declared_loc.get(lid) or {}).get("anchor")),
            job=(declared_loc.get(lid) or {}).get("job"),
        ))
    # Canvases whose location resolved to nothing are still content somebody wrote.
    unplaced = by_loc.get("(unplaced)", [])

    npcs = []
    for npc in game.get("npcs") or []:
        nid = npc.get("id")
        bound = [c for c in model if nid in (c["npc"], c["requires_npc"])]
        npcs.append(dict(
            id=nid, name=npc.get("name") or nid,
            role=npc.get("role") or "",
            relationship=npc.get("relationship") or "",
            traits=npc.get("core_traits") or {},
            canvases=len(bound),
            repeatable=sum(1 for c in bound if c["rep"]),
            rows=by_npc.get(nid, []),
            declared_surfaces=(declared_npc.get(nid) or {}).get("surfaces"),
            why_wanted=(declared_npc.get(nid) or {}).get("why_wanted"),
        ))

    if as_json:
        print(json.dumps(dict(
            slug=slug, locations=locs, characters=npcs,
            unplaced=[c["id"] for c in unplaced],
            ladders={f"{o}.{t}": {str(k): sorted(v) for k, v in d.items()}
                     for (o, t), d in lad.items()},
            movers={f"{o}.{t}": [c for c, _, _ in v] for (o, t), v in mv.items()},
            promises=[p for p in (st.get("promises") or []) if not p.get("paid_in")],
            releases=st.get("releases") or [],
        ), indent=2))
        return 0

    proj = game.get("project") or {}
    print(f"PITCH PACK — {proj.get('title') or slug}  ({slug})")
    print("=" * 72)
    print(f"  phase           {st.get('phase') or '(no v2_state.json)'}")
    print(f"  version         {proj.get('version') or '(unset)'}")
    print(f"  protagonist     {st.get('protagonist') or (game.get('player') or {}).get('name') or '?'}")
    print(f"  narration        {(game.get('settings') or {}).get('narration_person') or '?'} person")
    print(f"  built            {len(model)} canvases · {len(locs)} places · {len(npcs)} people")
    print()
    print("  A pitch is an event at a place and a person BELOW. Nothing here is a score;")
    print("  every figure is a count, or the author's own declared number. Judge nothing.")

    # ── the Want ────────────────────────────────────────────────────────────
    if want:
        _rule("THE WANT — the lines a release has to serve, verbatim")
        for k, v in want.items():
            print(f"  §{k}")
            _want_value(v)
    else:
        _rule("THE WANT")
        print("  no v2_state.json — the Want is not on disk for this game, and a pitch")
        print("  that cannot name the line it serves is unfocused by `the-release.md:36`.")

    # ── releases and promises ───────────────────────────────────────────────
    rels = st.get("releases") or []
    if rels:
        _rule(f"SHIPPED ALREADY — {len(rels)} release(s). Do not re-pitch these.")
        for r in rels:
            print(f"  v{r.get('version')}  {str(r.get('subject') or '')[:100]}")
            if r.get("want_line"):
                _wrap(f"serves: {r['want_line']}", indent="        ")

    proms = st.get("promises") or []
    openp = [p for p in proms if not p.get("paid_in")]
    if proms:
        _rule(f"OPEN PROMISES — {len(openp)} unpaid of {len(proms)} made")
        for p in openp:
            _wrap(f"[{p.get('made_in')}] {p.get('text')}",
                  first="  · ", indent="    ")
        if not openp:
            print("  every promise made has been paid.")

    # ── places ──────────────────────────────────────────────────────────────
    _rule(f"PLACES — {len(locs)}. A pitch names one of these and opens no new one.")
    print(f"  {'id':<22}{'canv':>5}{'rep':>5}{'rand':>6}{'words':>8}   who is scheduled here")
    for l in sorted(locs, key=lambda x: -x["words"]):
        star = "*" if l["anchor"] else " "
        who = ", ".join(l["people"]) if l["people"] else "—"
        print(f" {star}{l['id']:<22}{l['canvases']:>5}{l['repeatable']:>5}"
              f"{l['random']:>6}{l['words']:>8}   {who[:34]}")
    print("  * = the anchor.  rep = repeatable canvases.  rand = random ambients.")

    # ⚠️ BOTH BUDGETS, and the second one is why. A location declares `fill` (the
    # budget for now) and `fill_finished` (the budget for the finished world). This
    # printed `fill` alone until 2026-08-29, when the Attack Panel's first run found
    # that `fill_finished` is read by NOTHING — grep returns 0 in `gates.py` and, at
    # that point, here. Unread for long enough, it rotted: `mrs_vance`'s
    # `kerr_crossing` declares `fill = 620` and `fill_finished = 300`, a finished
    # budget BELOW its working one with 588 words already written. A Pitcher choosing
    # what to build next was seeing "588 / 620 — nearly full" and half the plan.
    #
    # The `!` is a FACT, not a threshold: finished below working is incoherent on the
    # author's own terms, whatever the numbers are. Nothing here is scored.
    declared = [l for l in locs if isinstance(l["declared_fill"], (int, float))]
    if declared:
        print()
        print("  built words against the author's OWN declared budgets (v2_state.json):")
        print(f"    {'':<24}{'built':>7}   {'now':>7}{'finished':>10}")
        tot_now = tot_fin = 0
        for l in sorted(declared, key=lambda x: x["words"] - (x["declared_fill"] or 0)):
            now = int(l["declared_fill"])
            fin = l["declared_finished"]
            tot_now += now
            tot_fin += int(fin) if isinstance(fin, (int, float)) else now
            fin_s = f"{int(fin):>10}" if isinstance(fin, (int, float)) else f"{'—':>10}"
            odd = "  !  finished budget is BELOW the working one" if (
                isinstance(fin, (int, float)) and fin < now) else ""
            print(f"    {l['id']:<24}{l['words']:>7}   {now:>7}{fin_s}{odd}")
        print(f"    {'TOTAL':<24}{sum(l['words'] for l in declared):>7}   "
              f"{tot_now:>7}{tot_fin:>10}")
    if unplaced:
        print()
        print(f"  {len(unplaced)} canvas(es) resolve to no location — they are reached by link only:")
        _wrap(", ".join(c["id"] for c in unplaced), indent="    ")

    # ── people ──────────────────────────────────────────────────────────────
    _rule(f"PEOPLE — {len(npcs)}. A pitch names one of these and invents no one.")
    print("  `schedule` is where the CHARACTER stands, not when a canvas fires. The two are")
    print("  different gates and this pack does not carry canvas triggers — if a pitch depends")
    print("  on when an existing surface plays, open the TOML and read that canvas's trigger.")
    print()
    for n in npcs:
        dec = f" (board declared {n['declared_surfaces']})" if n["declared_surfaces"] else ""
        print(f"  {n['id']}  ·  {n['name']}  ·  {n['canvases']} canvases, "
              f"{n['repeatable']} repeatable{dec}")
        if n["role"] or n["relationship"]:
            _wrap(n["relationship"] or n["role"])
        if n["why_wanted"]:
            _wrap(f"wanted for: {n['why_wanted']}")
        if n["traits"]:
            print(f"      meters: " + ", ".join(f"{k}={v}" for k, v in n["traits"].items()))
        if n["rows"]:
            print(f"      schedule: " + "; ".join(
                f"{loc} {_days(d)} {win}" for loc, d, win, _ in n["rows"][:6]))
        else:
            print("      schedule: no rows — placed by canvas, not by clock")

    # ── the state a pitch can key to ────────────────────────────────────────
    _rule("STATE A PITCH CAN KEY TO — meters the game already gates on")
    pl = (game.get("player") or {}).get("core_traits") or {}
    if pl:
        print("  the player carries: " + ", ".join(f"{k}={v}" for k, v in pl.items()))
        print()
    if not kinds:
        print("  nothing in this game reads a meter in any condition.")
    for (owner, trait) in sorted(kinds):
        rungs = lad.get((owner, trait), {})
        moves = mv.get((owner, trait), [])
        where = " ".join(f"{k}x{n}" for k, n in sorted(kinds[(owner, trait)].items()))
        at = ", ".join(str(v) for v in sorted(rungs)) if rungs else "no numeric rung"
        print(f"  {owner + '.' + trait:<30}{at}")
        print(f"  {'':<30}{where}   ({len(moves)} canvas(es) move it)")
    print()
    print("  entry = whether the canvas fires · dispatch = which canvas a Lane 3 host")
    print("  swaps to · choice = whether a link is offered · band = which prose variant")
    print("  renders. A meter with bands and no entry gate COLOURS the game, locks nothing.")

    dec_r = _declared_rungs(board)
    if dec_r:
        print()
        print("  the ladder the board DECLARED (v2_state.json), for comparison only:")
        wide = max(len(l) for l, _, _, _ in dec_r) + 2
        for label, owner, traits, vals in dec_r:
            # Exact keys only. A substring match here printed a rung against the
            # wrong character on the first run — see _declared_rungs.
            gated = set()
            for t in traits:
                gated |= set(lad.get((owner, t), {}))
            if not traits:
                gated = set()
            marks = " ".join(f"{v}{'*' if v in gated else '·'}" for v in vals)
            print(f"    {label:<{wide}}{marks}")
        print("    * = a canvas gates THIS owner's THIS meter at exactly this number.")
        print("    · = no canvas does. Neither is right or wrong — a rung can be reached")
        print("    by prose that is not gated on it. This is a fact, not a finding.")

    # ── flags ───────────────────────────────────────────────────────────────
    reads = _flag_reads(model)
    only_set = sorted(f for f in flags_set if f not in reads)
    _rule(f"FLAGS — {len(flags_set)} set by content, {len(reads)} read by a gate")
    if only_set:
        print(f"  {len(only_set)} flag(s) are set and nothing reads them yet. Each one is a")
        print("  door the game already opens and has not walked through:")
        _wrap(", ".join(only_set), indent="    ")
    else:
        print("  every flag the content sets is read somewhere.")

    # ── economy ─────────────────────────────────────────────────────────────
    _rule("ECONOMY — what a pitch may cost, and what already earns")
    econ = board.get("economy") or {}
    cur = econ.get("currency") or "money"
    rent = (game.get("settings") or {}).get("rent") or {}
    if rent.get("enabled"):
        print(f"  obligation      {rent.get('currency_symbol', '')}{rent.get('amount')} "
              f"every {rent.get('due_day')}, collected by {rent.get('collector_npc')}")
    moves = mv.get(("player", cur), [])
    earners = [(c, op, v) for c, op, v in moves if _sign(v) > 0 and op in ("add", None)]
    spenders = [(c, op, v) for c, op, v in moves if _sign(v) < 0 or op == "subtract"]
    print(f"  {cur} moves on {len(moves)} canvas(es) — "
          f"{len(earners)} add, {len(spenders)} take")
    unread = len(moves) - len(earners) - len(spenders)
    if unread:
        print(f"  ({unread} carry a value shape this split cannot read — counted in the "
              f"total, in neither column)")
    costed = [c for c in model if c["costs"]]
    print(f"  {len(costed)} canvas(es) carry an engine `costs` gate (the engine blocks "
          f"on affordability)")
    capped = [c for c in model if c["perday"]]
    print(f"  {len(capped)} canvas(es) carry max_triggers_per_day")
    if econ.get("sinks"):
        print("  sinks the board declared:")
        for s in econ["sinks"]:
            _wrap(str(s), first="    · ", indent="      ")

    # ── surfaces ────────────────────────────────────────────────────────────
    _rule("SURFACES THIS GAME HAS")
    settings = game.get("settings") or {}
    print(f"  guidance cards   {len(game.get('quest_cards') or [])}")
    print(f"  phone            {'declared' if game.get('phone') else 'none'}")
    print(f"  clothing         {'on' if settings.get('clothing_enabled') else 'off'}")
    print(f"  cheat page       {'declared' if (game.get('ui') or {}).get('cheat_page') else 'none'}")
    print(f"  cast page        {'declared' if (game.get('ui') or {}).get('cast_page') else 'none'}")

    print()
    print("─" * 72)
    print("  Pitch an event at one of these places with one of these people, keyed to")
    print("  state that already exists. `the-release.md:47` — default to zero new")
    print("  locations. Nothing above is a verdict; LO judges the pitch.")
    return 0


def main():
    argv = [a for a in sys.argv[1:] if a != "--json"]
    if not argv:
        print(__doc__)
        return 2
    slug, toml_path, state_path = _paths(argv[0])
    if not os.path.exists(toml_path):
        print(f"not found: {toml_path}")
        return 2
    return pack(slug, toml_path, state_path, as_json="--json" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
