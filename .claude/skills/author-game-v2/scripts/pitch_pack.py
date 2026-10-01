#!/usr/bin/env python3
"""
pitch_pack.py — the world a Pitcher is allowed to pitch into.

Usage:
    python3 scripts/pitch_pack.py <game-slug>        # the pack, as text
    python3 scripts/pitch_pack.py <path/to/game.toml>
    python3 scripts/pitch_pack.py <slug> --json      # machine-readable
    python3 scripts/pitch_pack.py <slug> --kind being_seen   # + that kind's library slice
    python3 scripts/pitch_pack.py <slug> --person <npc_id>   # RELATIONSHIPS: one person only
    python3 scripts/pitch_pack.py <slug> --thread <id>       # the her-life Pitcher: one thread
                                                             #   (+ --person <new_id> for its new person)

WHY THIS EXISTS, and why it is a script and not a paragraph in the agent's prompt.

`the-release.md` loop step 2 tells the author to run three Pitcher agents with NO
SHARED CONTEXT — independence is the whole point, because common context yields
three shades of one idea. That design has a cost nobody had paid: a Pitcher with
no context does not know what the game already contains. It will pitch a location
that exists, a character who does not, or a mechanic the engine cannot run.

So the pack IS the Pitcher's world. Everything it may name is in here and
nothing else is.

A pitch is HER MOMENT, in eight lines (`the-release.md`, "Her moment — eight lines"). Each
Pitcher is assigned a relationship or a thread; a moment kind (--kind) is a hint, not
the assignment. So the pack opens with what a moment needs, in this order
(PRD_IDEAS_AND_CRAFT IC2):

    THE PROMISE                   the fantasy, the model to beat, the live goal /
                                  mystery / rival, the moment kinds promised
    LAST LISTEN                   what players said after the last release
    MOMENT KINDS ALREADY SHIPPED  counted from releases[].moment_kind
    THE MOMENT LIBRARY            the one kind this Pitcher was hinted (--kind)
    CLIPS ON THE SHELF            media files on disk, per person and pool

and then WHERE and WHO: PLACES, PEOPLE and the STATE a pitch can key to (by
default zero new places — `the-release.md`, "Where a release happens"), plus what
the release owes (the Want, the open promises) and what it may cost (the economy).

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
# came from. The state file is often missing, so its absence is normal and
# never an error.

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
# Not every key is present on every `board`, and the declared meter ladder
# appears under THREE keys in three shapes:
#
#   board.rungs              [15, 35, 55]
#   board.tier_rungs         {trait: [...]}
#   board.cast_meters.rungs  {npc: [...]}
#
# So every reader below is tolerant by construction. A key that is not there is
# reported as not declared — never defaulted, never inferred, and never a defect.

def _declared_rungs(board):
    """[(label, owner, traits, rungs)] from whichever of the three shapes was used.

    ⚠️ RETURNS THE OWNER AND THE TRAIT SEPARATELY, deliberately. The first cut of
    this function returned a formatted label and the caller matched the built
    ladder against it with `owner in label or trait in label`. Substring matching
    starred a rung from the wrong character, because `want` is in every cast label.
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
    `gates.build()` flattens, and reported a colour meter gated nowhere that a full
    walk finds gated in over twenty places. They are in `trigger.substitutions[].conditions` and in
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

    ⚠️ An effect value is not always a number. It can be
    `{ type = "random", min = 8, max = 14 }`, and an `isinstance(val, (int, float))`
    filter drops every one of them silently — a meter climbed by random ranges then
    reads as never raised.

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
# Her moment — the promise, the kinds shipped, the library, the clips
# ─────────────────────────────────────────────────────────────────────────────
# Every reader below prints what is DECLARED and says "not declared" otherwise.
# The fields are new (the-want.md §0, IC1), so for every game written before them
# the honest answer is "not declared" — never a guess from the prose.

MOMENT_KINDS = [
    ("firsts", "her firsts"),
    ("being_seen", "being seen"),
    ("body_as_payment", "her body as the price for something she needs"),
    ("taboo_at_home", "taboo at home"),
    ("consequence", "a consequence she lives with"),
]
KIND_KEYS = [k for k, _ in MOMENT_KINDS]

LIBRARY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "references", "moment-library.md")


def _shipped(releases):
    """The releases that shipped: an entry with a `shipped` date (state.md).

    A planned release, or the idea page's first step written into `releases[]`, is
    not a shipped one, and counting it told the Pitchers a kind had been delivered
    that no player had seen (PRD v2 DC1 · E4 · H30).
    """
    return [r for r in releases or [] if isinstance(r, dict) and r.get("shipped")]


def _kinds_shipped(releases):
    """({kind: count}, unrecorded, [three least used]) from SHIPPED releases' moment_kind.

    A release with no `moment_kind` is UNRECORDED, not guessed — the field is new,
    and inferring a kind from a subject line is an opinion the pack may not hold.
    Ties among the least used keep MOMENT_KINDS order, so the pick is stable.
    """
    counts = {k: 0 for k in KIND_KEYS}
    unrecorded = 0
    for r in _shipped(releases):
        k = (r or {}).get("moment_kind")
        if k in counts:
            counts[k] += 1
        else:
            unrecorded += 1
    least = sorted(KIND_KEYS, key=lambda k: (counts[k], KIND_KEYS.index(k)))[:3]
    return counts, unrecorded, least


def _library_slice(kind, path=None):
    """The entries under `## <kind> · …` in the moment library, or None if absent.

    Parsed by heading, so the pack prints ten moments and not fifty — the Pitcher
    is given one kind, and the other forty are other Pitchers' business.
    """
    path = path or LIBRARY_PATH
    if not os.path.exists(path):
        return None
    out, inside = [], False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("## "):
                inside = line[3:].strip().split(" ")[0] == kind
                continue
            if inside and line.strip():
                out.append(line.rstrip("\n"))
    return out


def _media_refs(game, model):
    """{person: [(pool_or_file, is_pool)]} for every media block the TOML names.

    Walks every dict in each canvas for `pool_dir` / `file`, because media sits
    in node blocks, in group children and in cascade beats alike. The person is
    the canvas's bound npc, or `(no one)`.
    """
    who = {c["id"]: (c["npc"] or c["requires_npc"] or "(no one)") for c in model}
    refs = collections.defaultdict(list)

    def walk(obj, cid):
        if isinstance(obj, dict):
            props = obj.get("props") if isinstance(obj.get("props"), dict) else {}
            for holder in (obj, props):
                if isinstance(holder.get("pool_dir"), str):
                    refs[who.get(cid, "(no one)")].append((holder["pool_dir"], True))
                elif (isinstance(holder.get("file"), str)
                      and obj.get("type") in ("video", "image")):
                    refs[who.get(cid, "(no one)")].append((holder["file"], False))
            for v in obj.values():
                walk(v, cid)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, cid)

    for c in game.get("canvases") or []:
        walk(c.get("nodes") or [], c.get("id"))
    return refs


def _media_roots(slug):
    """Every folder a build copied media into.

    `package_from_toml --video-folder <dir>` copies the folder into the output
    under its own basename (`video_path = "./" + name`), so the name varies by
    game. Every sub-folder of
    `output/` and `output_dev/` is a candidate root; a pool that is not under
    any of them counts 0.
    """
    roots = []
    for base in (f"games/{slug}/output", f"games/{slug}/output_dev"):
        if os.path.isdir(base):
            roots += sorted(os.path.join(base, d) for d in os.listdir(base)
                            if os.path.isdir(os.path.join(base, d)))
    return roots


def _count_on_disk(roots, ref, is_pool):
    """Files under the first root that has them. A count, never a judgement."""
    for root in roots:
        target = os.path.join(root, ref)
        if is_pool and os.path.isdir(target):
            return sum(1 for _, _, files in os.walk(target)
                       for f in files if not f.startswith("."))
        if not is_pool and os.path.isfile(target):
            return 1
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# Relationships — each person's steps so far, so a pitch can be the NEXT one
# ─────────────────────────────────────────────────────────────────────────────
# A pitch is the next step on a named relationship (`the-release.md`, "The next
# step"; `the-arc.md` A13-A14): it pays something already shipped and opens the
# step after. So the Pitcher needs, per person, what has shipped, in order, and
# which set-ups nothing has paid yet.
#
# ⚠️ ATTRIBUTION IS DECLARED, NOT GUESSED FROM PROSE. Arc canvases often bind no
# `npc` at all, so binding alone finds a person's hubs and none of their steps. So a
# one-time canvas belongs to a person if the board's declared ladder lists it, or it
# binds them, or its id starts with the person's short name (`npc_jo` -> `jo_`). The rule used is printed per step.

def _short(npc_id):
    return npc_id[4:] if str(npc_id).startswith("npc_") else str(npc_id)


def _chain_order(steps):
    """Order steps so one that reads a flag another sets comes after it.

    Kahn's sort, ties broken by id so the output is stable. Returns (ordered,
    unclear) — `unclear` is True when a cycle left steps unplaced; they are
    appended in id order and the caller says the order is unclear.
    """
    ids = sorted(c["id"] for c in steps)
    by = {c["id"]: c for c in steps}
    after = {i: set() for i in ids}                      # i must come after these
    for a in ids:
        for b in ids:
            if a != b and (by[a]["flags_set"] & by[b]["reads"]):
                after[b].add(a)
    done, out = set(), []
    while len(out) < len(ids):
        ready = [i for i in ids if i not in done and after[i] <= done]
        if not ready:
            rest = [i for i in ids if i not in done]
            return [by[i] for i in out + rest], True
        out.append(ready[0]); done.add(ready[0])
    return [by[i] for i in out], False


def _closing_line(canvas):
    """The last sentence on the last beat — SCREEN TEXT, not a quote of the person's."""
    beats = canvas.get("beats") or []
    if not beats:
        return ""
    text = beats[-1].text
    if isinstance(text, list):
        text = text[-1] if text else ""
    parts = [p.strip() for p in str(text).replace("\n", " ").split(". ") if p.strip()]
    line = parts[-1] if parts else ""
    return (line[:117] + "…") if len(line) > 118 else line


def _scene_line(c):
    """What a shipped scene IS, in the author's own words: its name and description."""
    raw = c.get("raw") or {}
    name = str(raw.get("name") or "").strip()
    desc = " ".join(str(raw.get("description") or "").split())
    if len(desc) > 110:
        desc = desc[:109] + "…"
    return " — ".join(x for x in (f"“{name}”" if name else "", desc) if x)


def _relationships(game, model, st):
    """[{id, name, steps[], surfaces[], unread, promises[], since_last, order_unclear}]."""
    _, flags_set = _movers(game)
    sets_of = collections.defaultdict(set)
    for flag, rows in flags_set.items():
        for cid, _op in rows:
            sets_of[cid].add(flag)
    readers = collections.defaultdict(set)                # flag -> canvases reading it
    for c in model:
        for f in c["reads"]:
            readers[f].add(c["id"])
    board = st.get("board") or {}
    declared = {d.get("id"): d for d in (board.get("characters") or []) if isinstance(d, dict)}
    promises = [p for p in (st.get("promises") or []) if isinstance(p, dict) and not p.get("paid_in")]
    releases = _shipped(st.get("releases"))
    out = []
    for npc in game.get("npcs") or []:
        nid = npc.get("id")
        name = npc.get("name") or nid
        ladder = (declared.get(nid) or {}).get("ladder") or {}
        on_ladder = {s.get("canvas") for s in (ladder.get("steps") or []) if isinstance(s, dict)}
        steps, surfaces = [], []
        for c in model:
            if c["id"] in on_ladder:
                how = "declared ladder"
            elif nid in (c["npc"], c["requires_npc"]):
                how = "binds " + nid
            elif c["id"].startswith(_short(nid) + "_"):
                how = "id prefix"
            else:
                continue
            if c["rep"]:
                surfaces.append(c)
            else:
                steps.append(dict(c, flags_set=sets_of.get(c["id"], set()), how=how))
        ordered, unclear = _chain_order(steps)
        rows, unread = [], 0
        for c in ordered:
            fl = []
            for f in sorted(c["flags_set"]):
                read = bool(readers.get(f, set()) - {c["id"]})
                unread += 0 if read else 1
                fl.append((f, read))
            rows.append(dict(id=c["id"], how=c["how"], flags=fl, scene=_scene_line(c)))
        named = [p for p in promises
                 if nid in str(p.get("text", "")) or str(name).lower() in str(p.get("text", "")).lower()]
        last = max((i for i, r in enumerate(releases)
                    if ((r or {}).get("her_moment") or {}).get("person") == nid), default=None)
        since = (len(releases) - 1 - last) if last is not None else None
        out.append(dict(id=nid, name=name, steps=rows, unread=unread,
                        surfaces=[dict(id=c["id"], scene=_scene_line(c))
                                  for c in sorted(surfaces, key=lambda x: x["id"])],
                        promises=[p.get("text") for p in named], since_last=since,
                        order_unclear=unclear,
                        closing=_closing_line(ordered[-1]) if ordered else "",
                        address=(declared.get(nid) or {}).get("address"),
                        renameable=bool(npc.get("customizable"))))
    # MOST OWED is a sort, not a score: open promises naming them, then set-ups
    # nothing pays, then releases since their last step (never recorded counts as
    # most), then fewest steps shipped. The caller hands the top two to two Pitchers;
    # the third gets a thread (THREADS).
    out.sort(key=lambda r: (-len(r["promises"]), -r["unread"],
                            -(r["since_last"] if r["since_last"] is not None else 10 ** 6),
                            len(r["steps"]), r["id"]))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Naming — the game's own names and words, so a pitch gets them right first time
# ─────────────────────────────────────────────────────────────────────────────
# The first IC3 dry run's pitches were caught by the excitement lens for three
# things the pack could have told them: re-staging a shipped scene, "Mum" in a game
# that says "your mother" 34 times and "Mum" 0, and a person who calls her by a
# name when the cast rule is that he uses nothing at all. Scenes are now listed
# per person with their own descriptions; the rest is here.

KIN_FORMS = [
    ("mother", ["your mother", "your mum", "your mom", "mum", "mom", "mam", "mommy", "mummy"]),
    ("father", ["your father", "your dad", "dad", "daddy", "pop"]),
    ("stepfather", ["stepfather", "stepdad", "step-dad"]),
    ("stepbrother", ["stepbrother", "step-brother", "stepbro"]),
]


def _prose(model):
    """All player-facing beat text in the build, as one lowercase string."""
    out = []
    for c in model:
        for b in c["beats"]:
            t = b.text
            out.extend(t if isinstance(t, list) else [str(t)])
    return " \n".join(str(x) for x in out).lower()


def _kin_counts(model):
    """[(group, [(form, n)])] for every kin group the prose uses at all."""
    import re as _re
    text = _prose(model)
    rows = []
    for group, forms in KIN_FORMS:
        counts = [(f, len(_re.findall(r"(?<![\w-])" + _re.escape(f) + r"(?![\w-])", text))) for f in forms]
        # "your mother" also matches inside nothing else; bare "mother" is not listed on purpose,
        # because it is the word the longer forms share.
        if any(n for _, n in counts):
            rows.append((group, counts))
    return rows


def _address_comment(toml_path):
    """A 'term of address' note in the TOML's own comments, verbatim — or ''."""
    try:
        lines = open(toml_path, encoding="utf-8").read().split("\n")
    except OSError:
        return ""
    def is_text(ln):                               # a comment line with words on it
        s = ln.strip()
        return s.startswith("#") and s.lstrip("#").strip() != "" and set(s) - set("#=-─ ")

    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("#") and "term of address" in ln.lower():
            a = i
            while a > 0 and is_text(lines[a - 1]):
                a -= 1
            b = i
            while b + 1 < len(lines) and is_text(lines[b + 1]):
                b += 1
            return " ".join(x.strip().lstrip("#").strip() for x in lines[a:b + 1])
    return ""


def _print_relationship(r, full=True):
    since = ("not recorded" if r["since_last"] is None
             else f"{r['since_last']} release(s) since the last step")
    print(f"  {r['id']}  ·  {r['name']}  ·  {len(r['steps'])} step(s) shipped · "
          f"{r['unread']} set-up(s) nothing reads · {len(r['promises'])} open promise(s) · {since}")
    if not full:
        return
    addr = r.get("address") or "not declared (board.characters[].address) — see NAMING below"
    _wrap(f"calls her: {addr}", first="      ", indent="        ")
    if r.get("renameable"):
        _wrap(f"the player can rename them — prose writes @{_short(r['id'])}, never a typed name",
              first="      ", indent="        ")
    if r["order_unclear"]:
        print("      order unclear — the steps' flags form a cycle; listed by id after the break")
    print("      SCENES ALREADY SHIPPED — do not restage one; a pitch is the step after them:")
    for i, s in enumerate(r["steps"], 1):
        flags = ", ".join(f"{f}{'' if read else ' (NOT READ)'}" for f, read in s["flags"]) or "sets no flag"
        _wrap(f"{i}. {s['id']}  [{s['how']}]  {s.get('scene') or ''}", first="      ", indent="         ")
        _wrap(f"sets: {flags}", first="         ", indent="           ")
    if not r["steps"]:
        print("      (no one-time steps yet)")
    if r["closing"]:
        _wrap(f"last step ends on (screen text, not a quote of theirs): \"{r['closing']}\"",
              first="      ", indent="        ")
    for p in r["promises"]:
        _wrap(f"open promise: {p}", first="      ", indent="        ")
    for s in r["surfaces"]:
        _wrap(f"surface (repeatable): {s['id']}  {s['scene']}", first="      ", indent="        ")


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
    silently dropped everything else, which dropped a non-string `crude_ceiling`
    — the field that says how far a game's prose may go — to a bare heading with
    nothing under it. A Pitcher reading that pack would have had
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


def _print_promise(want):
    _rule("THE PROMISE — the fantasy this game already made (want; the idea page, the-want.md §0, §6)")
    for key, label in (("fantasy_shape", "fantasy shape"), ("model_to_beat", "model to beat"),
                       ("promise", "the promise"), ("moment_kinds", "moment kinds promised"),
                       ("face", "her face"), ("companion", "the companion"),
                       ("pressure", "the pressure-man")):
        val = want.get(key)
        if val in (None, "", [], {}):
            print(f"  {label:<22}not declared")
        else:
            print(f"  {label}:")
            _want_value(val, indent="      ")
    threads = _threads(want)
    print(f"  {'her life, the threads':<22}"
          + (f"{len(threads)} declared (THREADS below)" if threads else "not declared"))


def _threads(want):
    """want.threads[] — her life (the-want.md §6), dict rows with an id only."""
    return [t for t in (want.get("threads") or []) if isinstance(t, dict) and t.get("id")]


def _print_threads(want, thread=None, place_ids=None):
    """THREADS — her life. The third Pitcher pitches a step in one of these (--thread).

    Facts only: a thread's person missing from want.cast, or its place missing from the
    places a pitch may name, is printed as a fact, never scored.
    """
    threads = _threads(want)
    cast = {c.get("id") for c in (want.get("cast") or []) if isinstance(c, dict)}
    _rule(f"THREADS — {len(threads)}, her life (want.threads[], the-want.md §6). "
          "The third Pitcher pitches a step in one.")
    if not threads:
        print("  none declared — want.threads[] = [{id, name, person, place, system, link}]"
              " (templates/want.md §5).")
        return
    if thread and thread not in {t["id"] for t in threads}:
        print(f"  unknown thread `{thread}`. Threads: {', '.join(t['id'] for t in threads)}")
        return
    for t in threads:
        if thread and t["id"] != thread:
            continue
        notes = []
        if t.get("person") and t.get("person") not in cast:
            notes.append("person not in want.cast")
        if place_ids is not None and t.get("place") and t.get("place") not in place_ids:
            notes.append("place not among PLACES")
        mark = "  <- your thread" if thread else ""
        print(f"  {t['id']}  ·  {t.get('name') or ''}  ·  person {t.get('person') or '?'}  ·  "
              f"place {t.get('place') or '?'}  ·  system {t.get('system') or '?'}{mark}")
        if t.get("link"):
            _wrap(f"link into the hook: {t['link']}")
        if notes:
            print(f"      ({'; '.join(notes)})")
    if thread:
        print("  A step in this thread may add ONE new person who belongs to it: name, age (18+),")
        print("  thread. Zero new places.")


def _print_kinds(kinds_count, kinds_unrec, kinds_least):
    _rule("MOMENT KINDS ALREADY SHIPPED — from shipped releases[].moment_kind")
    for k, label in MOMENT_KINDS:
        print(f"  {k:<18}{kinds_count[k]:>3}   {label}")
    if kinds_unrec:
        print(f"  {'unrecorded':<18}{kinds_unrec:>3}   releases with no moment_kind (not guessed)")
    print(f"  three least used: {', '.join(kinds_least)}  — a hint for a Pitcher, not its assignment")


def _print_library(kind):
    _rule("THE MOMENT LIBRARY — EVIDENCE, NOT A TEMPLATE. Take the kind, never an entry.")
    if not kind:
        print("  no kind given. Run with --kind <" + "|".join(KIND_KEYS) + ">")
    elif kind not in KIND_KEYS:
        print(f"  unknown kind `{kind}`. Kinds: {', '.join(KIND_KEYS)}")
    else:
        entries = _library_slice(kind)
        if entries is None:
            print("  references/moment-library.md not found.")
        elif not entries:
            print(f"  the library has no `## {kind}` section.")
        else:
            print(f"  kind: {kind}")
            for line in entries:
                print(f"  {line}")


def _print_shipped(st):
    shipped = _shipped(st.get("releases"))
    if shipped:
        _rule(f"SHIPPED ALREADY — {len(shipped)} release(s). Do not re-pitch these.")
        for r in shipped:
            print(f"  v{r.get('version')}  {str(r.get('subject') or '')[:100]}")
            if r.get("want_line"):
                _wrap(f"serves: {r['want_line']}", indent="        ")


def _read_page(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# The idea phase — no build yet (PRD v2 DC1 · E2 · D14)
# ─────────────────────────────────────────────────────────────────────────────
# The first step is pitched by three `v2-pitcher`s on the idea page, before a line of
# TOML exists. The pack used to stop at "not found: …/7_final_game.toml", so the tool
# built to keep Pitchers from inventing places was missing exactly when nothing is
# built yet. With no TOML it prints what does exist: the ledger, `WANT.md`, `IDEA.md`,
# and the Want's own places and people (`want.places[]`, `want.cast[]`).

def idea_pack(slug, state_path, as_json=False, kind=None, person=None, thread=None):
    st = _state(state_path) or {}
    want = st.get("want") or {}
    game_dir = os.path.dirname(state_path)
    want_md = _read_page(os.path.join(game_dir, "WANT.md"))
    idea_md = _read_page(os.path.join(game_dir, "IDEA.md"))
    kinds_count, kinds_unrec, kinds_least = _kinds_shipped(st.get("releases"))
    places = [p for p in (want.get("places") or []) if isinstance(p, dict)]
    why = want.get("why_this_person") or {}
    people = [dict(c, why=why.get(c.get("id"))) for c in (want.get("cast") or [])
              if isinstance(c, dict) and c.get("id")]

    if as_json:
        print(json.dumps(dict(
            slug=slug, phase=st.get("phase"), built=False, want_page=want_md, idea_page=idea_md,
            places=places, people=people,
            promise={k: want.get(k) for k in
                     ("fantasy_shape", "model_to_beat", "promise", "moment_kinds", "threads")},
            moment_kinds_shipped=dict(kinds_count, unrecorded=kinds_unrec, least_used=kinds_least),
            releases=_shipped(st.get("releases")),
        ), indent=2, default=list))
        return 0

    print(f"PITCH PACK — {slug}  (idea phase: no build yet)")
    print("=" * 72)
    print(f"  phase           {st.get('phase') or '(no v2_state.json)'}")
    print(f"  protagonist     {st.get('protagonist') or '?'}")
    print()
    print("  No TOML exists, so there are no scenes, flags or schedules to read. A pitch here is")
    print("  STEP 1 with its person: show his want first. Places and people come from the Want.")

    _print_promise(want)
    _print_kinds(kinds_count, kinds_unrec, kinds_least)
    _print_library(kind)

    _rule(f"PLACES — {len(places)}, from want.places[]. A pitch names one of these.")
    if not places:
        print("  none declared — want.places[] = [{id, name}] (templates/want.md §1).")
    for p in places:
        print(f"  {str(p.get('id')):<22}{p.get('name') or ''}")

    _print_threads(want, thread, {p.get("id") for p in places})

    _rule(f"PEOPLE — {len(people)}, from want.cast[]. A pitch names one of these, or a thread"
          " pitch one new person in its thread.")
    if person and person not in {p["id"] for p in people}:
        if thread:
            print(f"  new person `{person}` — joins thread `{thread}`; the pitch gives name, age, thread.")
        else:
            print(f"  unknown person `{person}`. People: {', '.join(p['id'] for p in people) or 'none'}")
    for p in people:
        mark = "  <- your person" if person and p["id"] == person else ""
        print(f"  {p['id']}  ·  age {p.get('age', '?')}  ·  keeps: {p.get('keeps') or 'not declared'}{mark}")
        if p.get("why"):
            _wrap(f"wanted for: {p['why']}")

    for title, page, name in (("THE WANT PAGE — verbatim", want_md, "WANT.md"),
                              ("THE IDEA PAGE — verbatim", idea_md, "IDEA.md")):
        _rule(title)
        if page is None:
            print(f"  games/{slug}/{name} not found.")
        else:
            for line in page.rstrip().splitlines():
                print(f"  {line}")

    _print_shipped(st)
    print()
    print("─" * 72)
    print("  Pitch step 1 in eight lines, with one of these people at one of these places")
    print("  (a thread pitch may add one new person in its thread). Zero new places. LO picks")
    print("  one of the three; the others become later steps.")
    return 0


def pack(slug, toml_path, state_path, as_json=False, kind=None, person=None, thread=None):
    game = gates._load(toml_path)
    model, _ = gates.build(game)
    st = _state(state_path) or {}
    board = st.get("board") or {}
    want = st.get("want") or {}
    kinds_count, kinds_unrec, kinds_least = _kinds_shipped(st.get("releases"))
    media = _media_refs(game, model)
    roots = _media_roots(slug)
    rels = _relationships(game, model, st)

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
            releases=_shipped(st.get("releases")),
            promise={k: want.get(k) for k in
                     ("fantasy_shape", "model_to_beat", "promise", "moment_kinds", "threads")},
            moment_kinds_shipped=dict(kinds_count, unrecorded=kinds_unrec,
                                      least_used=kinds_least),
            clips={who: {ref: _count_on_disk(roots, ref, pool) for ref, pool in rs}
                   for who, rs in media.items()},
            relationships=[{k: v for k, v in r.items()} for r in rels],
        ), indent=2, default=list))
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
    print("  A pitch is her moment (the-release.md, \"Her moment — eight lines\"). Where and who come from")
    print("  the lists below. Nothing here is a score; every figure is a count, or the")
    print("  author's own declared number. Judge nothing.")

    _print_promise(want)

    # ── what players said last time ─────────────────────────────────────────
    _rule("LAST LISTEN — what players said after the last release, verbatim")
    listens = [x for x in (st.get("listen") or []) if isinstance(x, dict)]
    if listens:
        for k, v in listens[-1].items():
            print(f"  {k}:")
            _want_value(v, indent="      ")
    else:
        print("  no listen yet — nothing recorded in v2_state.json `listen[]`.")

    _print_kinds(kinds_count, kinds_unrec, kinds_least)
    _print_library(kind)

    # ── clips on the shelf ──────────────────────────────────────────────────
    _rule("CLIPS ON THE SHELF — media files on disk, per person and pool (a count)")
    if not media:
        print("  the built game names no media.")
    else:
        if not roots:
            print(f"  no media on disk (no folder under games/{slug}/output or output_dev)")
        for who in sorted(media):
            seen = collections.OrderedDict()
            for ref, pool in media[who]:
                seen.setdefault(ref, pool)
            parts = [f"{ref} {_count_on_disk(roots, ref, pool)}" for ref, pool in seen.items()]
            _wrap(" · ".join(parts), first=f"  {who}: ", indent="      ")

    # ── relationships ───────────────────────────────────────────────────────
    _rule("RELATIONSHIPS — a pitch is the NEXT step on one of these (the-release.md, \"The next step\")")
    print("  Most owed first. The order is a sort, not a score: open promises naming them, then")
    print("  set-ups their steps made that nothing reads, then releases since their last step, then")
    print("  fewest steps. The caller gives the top two to two Pitchers, plus one thread")
    print("  (THREADS) to the third.")
    print()
    shown = [r for r in rels if not person or r["id"] == person]
    if person and not shown:
        if thread:
            print(f"  new person `{person}` — joins thread `{thread}`; no steps yet, so this is step 1.")
        else:
            print(f"  unknown person `{person}`. People: {', '.join(r['id'] for r in rels)}")
    for r in shown:
        _print_relationship(r, full=True)
        print()

    _print_threads(want, thread, {l["id"] for l in locs})

    # ── naming ──────────────────────────────────────────────────────────────
    _rule("NAMING — the game's own names and words. Write these, not your own.")
    declared_addr = [r for r in rels if r.get("address")]
    comment = _address_comment(toml_path)
    if declared_addr:
        for r in declared_addr:
            print(f"  {r['id']:<18} calls her: {r['address']}")
    elif comment:
        _wrap(f"terms of address — from a COMMENT in the game's TOML (not a declaration): {comment}",
              first="  ", indent="    ")
    else:
        print("  terms of address: not declared (board.characters[].address) and no comment found.")
    ren = [r for r in rels if r.get("renameable")]
    if ren:
        _wrap("renameable by the player — prose uses the token, never a typed name: "
              + ", ".join(f"{r['id']} → @{_short(r['id'])}" for r in ren), first="  ", indent="    ")
    kin = _kin_counts(model)
    if kin:
        print("  kin words the prose already uses (a count; the zero forms are not this game's):")
        for group, counts in kin:
            used = [f"\"{f}\" ×{n}" for f, n in counts if n]
            unused = [f"\"{f}\"" for f, n in counts if not n]
            _wrap(f"{group}: {' · '.join(used)}" + (f"   never: {', '.join(unused)}" if unused else ""),
                  first="    ", indent="      ")

    # ── the Want ────────────────────────────────────────────────────────────
    if want:
        _rule("THE WANT — the lines a release has to serve, verbatim")
        for k, v in want.items():
            print(f"  §{k}")
            _want_value(v)
    else:
        _rule("THE WANT")
        print("  no v2_state.json — the Want is not on disk for this game, and a pitch")
        print("  that cannot name the line it serves is unfocused (`the-release.md` loop step 1).")

    # ── releases and promises ───────────────────────────────────────────────
    _print_shipped(st)

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
    # that point, here. Unread for long enough, it rots: a location can declare a
    # finished budget BELOW its working one, and a Pitcher choosing what to build
    # next sees "nearly full" and half the plan.
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
    _rule(f"PEOPLE — {len(npcs)}. A pitch names one of these; only a thread pitch may add one"
          " new person, in its thread.")
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
    print("  Pitch her moment in eight lines, at one of these places with one of these")
    print("  people (or one new person in a thread pitch's thread), keyed to state that")
    print("  already exists. Default to zero new places")
    print("  (`the-release.md`, \"Where a release happens\"). LO judges the pitch.")
    return 0


def main():
    args = sys.argv[1:]
    opts = {}
    for flag in ("--kind", "--person", "--thread"):
        if flag in args:
            i = args.index(flag)
            opts[flag] = args[i + 1] if i + 1 < len(args) else ""
            del args[i:i + 2]
    kind, person, thread = opts.get("--kind"), opts.get("--person"), opts.get("--thread")
    argv = [a for a in args if a != "--json"]
    if not argv:
        print(__doc__)
        return 2
    slug, toml_path, state_path = _paths(argv[0])
    if not os.path.exists(toml_path):
        # The idea phase: no build yet. Read the ledger and the Want and idea pages instead.
        game_dir = os.path.dirname(state_path)
        if os.path.exists(state_path) or os.path.exists(os.path.join(game_dir, "WANT.md")):
            return idea_pack(slug, state_path, as_json="--json" in sys.argv, kind=kind, person=person,
                             thread=thread)
        print(f"not found: {toml_path}, and no v2_state.json or WANT.md in {game_dir}")
        return 2
    return pack(slug, toml_path, state_path, as_json="--json" in sys.argv, kind=kind, person=person,
                thread=thread)


if __name__ == "__main__":
    sys.exit(main())
