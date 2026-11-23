"""The measured scene checks check.py runs on the merged TOML. Each returns (status, rows), like check.py's own.

  talk      every path through a scene, counted over the screens with someone else in them, keeps narration to
            speech at or under 5 : 1 (craft/voice.md, the shape, rule 5, which says how to count)
  length    no screen is over 150 words of story text (C519, C520; reader.md part A)
  presence  a person who speaks on a repeatable scene at a place is there at every minute it can show, by their
            schedule rows (who_is_where.py), unless the scene is bound to them or checks they're present
  creation  every creation field the player fills in (her name, a nickname) is printed back somewhere (C48)
  saves     against the last build LO played (the last commit of games/<slug>/output/index.html): no id or key is
            removed, no meter's range changed, and no flag is set by a different choice than before, unless
            NOTES.md says `Same meaning: <flag>` (C1656, C1658, C1659; craft/returning-player.md)
  speakers  every dialog block names its speaker, and a person speaker is a person in the game (v2's
            `speakers are named`, gates.py:9500)
  goals     a quest-card goal line reads the way it works (v2's `a goal line reads the way it works`, gates.py:18911)

What these can't see is still the writer's and the reader's: whether a line is true in what it says, a screen's
one job, a person named in narration (only speakers are placed), and the opening's own clock. `talk` counts a
screen as having someone in it only by a line from them, a presence check, or their name or one-word role in the
prose: a screen that has them only as "she" is not counted.
"""
import json
import re
import subprocess
import tomllib
from pathlib import Path

import who_is_where

GREEN, RED, INCOMPLETE = "green", "red", "incomplete"
TALK_CEILING = 5.0      # craft/voice.md rule 5; v2 gate 32 (register.md:658)
SCREEN_WORDS = 150      # reader.md, part A: over about 150 words is a FAIL
PATH_CAP = 500          # paths walked per scene; past it the scene is INCOMPLETE, never green
TEXT = ("paragraph", "dialog", "thought_bubble", "heading")
NOT_PERSON = ("player",)


def words(s):
    return len(re.sub(r"@[\w.]+", "x", str(s or "")).split())


def children(b):
    props = b.get("props") or {}
    return b.get("blocks") or props.get("blocks") or []


def walk(blocks, cond=()):
    """Every block, with the conditions of the groups around it."""
    for b in blocks or []:
        if not isinstance(b, dict):
            continue
        yield b, cond
        if b.get("type") in ("group", "block_pool"):
            c = (b.get("props") or {}).get("conditions") or b.get("conditions")
            yield from walk(children(b), cond + ((c,) if c else ()))


def items(conditions):
    """Condition items, flattened."""
    out = []

    def visit(d):
        if isinstance(d, dict):
            if d.get("type"):
                out.append(d)
            for v in d.values():
                visit(v)
        elif isinstance(d, list):
            for v in d:
                visit(v)
    visit(conditions)
    return out


def canvases(game, dev=()):
    return [c for c in game.get("canvases") or [] if isinstance(c, dict) and c.get("id") and c["id"] not in dev]


# ── talk ──────────────────────────────────────────────────────────────────────────────────────────────────

def people(game):
    """[(npc id, regex on their name or one-word role)]: how prose names a person."""
    out = []
    for n in game.get("npcs") or []:
        names = [str(n.get("name") or "")]
        role = str(n.get("role") or "")
        if role and " " not in role and "-" not in role:
            names.append(role)  # "Mom"; "Step-brother" is a description, not a name
        names = [re.escape(x) for x in names if len(x) >= 3]
        if n.get("id") and names:
            out.append((n["id"], re.compile(r"\b(?:%s)\b" % "|".join(names))))
    return out


QUOTED = re.compile(r"[\"“]([^\"“”]+)[\"”]")


def text_split(b):
    """(narration words, speech words) in one text block: a dialog block is speech, and so is a quoted line inside a
    paragraph, because the player reads it as someone talking (L163: measure it the way the player sees it)."""
    content = str(b.get("content") or "")
    if b.get("type") == "dialog":
        return 0, words(content)
    spoken = sum(words(q) for q in QUOTED.findall(content))
    return words(content) - spoken, spoken


def screen_split(blocks):
    """(narration, speech) a screen shows on its worst variant: adjacent groups are one if/elseif chain, so a chain
    counts the one group that leans most on narration."""
    narr = speech = 0
    chain = []
    for b in list(blocks or []) + [None]:
        if isinstance(b, dict) and b.get("type") == "group":
            chain.append(screen_split(children(b)))
            continue
        if chain:
            n, s = max(chain, key=lambda x: x[0] - TALK_CEILING * x[1])
            narr, speech, chain = narr + n, speech + s, []
        if isinstance(b, dict):
            if b.get("type") in TEXT:
                n, s = text_split(b)
                narr, speech = narr + n, speech + s
            elif b.get("type") == "block_pool":
                n, s = max([screen_split([x]) for x in children(b)] or [(0, 0)], key=lambda x: x[0] - TALK_CEILING * x[1])
                narr, speech = narr + n, speech + s
    return narr, speech


def has_company(c, node, who):
    trig = c.get("trigger") or {}
    if trig.get("npc") or trig.get("requires_npc"):
        return True
    absent = {i.get("npc_id") for i in items(node.get("blocks")) if i.get("type") == "npc_at_location"
              and i.get("operator") == "is_absent"}
    for b, _ in walk(node.get("blocks")):
        props = b.get("props") or {}
        if b.get("type") == "dialog" and props.get("speaker") not in NOT_PERSON:
            return True
        if b.get("type") == "npc_at_location" and b.get("operator") == "is_present":
            return True
    if any(i.get("type") == "npc_at_location" and i.get("operator") == "is_present" for i in items(node.get("blocks"))):
        return True
    text = " ".join(str(b.get("content") or "") for b, _ in walk(node.get("blocks")))
    return any(rx.search(text) and pid not in absent for pid, rx in who)


def graph(c):
    """{node id: [next node ids in this scene]}, and the first node."""
    nodes = {n.get("id"): n for n in c.get("nodes") or [] if n.get("id")}
    nxt = {}
    for nid, n in nodes.items():
        out = []
        for ch in ((n.get("exit_block") or {}).get("choices") or []):
            t = str(ch.get("nodeId") or "")
            t = t.split(".", 1)[1] if t.startswith(c["id"] + ".") else t
            if ch.get("targetType", "node") == "node" and t in nodes:
                out.append(t)
        nxt[nid] = out
    first = (c.get("nodes") or [{}])[0].get("id")
    return nodes, nxt, first


def paths(c):
    """Every path from the first screen to one with no next screen in the scene (loops cut). None past PATH_CAP."""
    nodes, nxt, first = graph(c)
    if first is None:
        return []
    out, stack = [], [[first]]
    while stack:
        p = stack.pop()
        ahead = [t for t in nxt[p[-1]] if t not in p]
        if not ahead:
            out.append(p)
            if len(out) > PATH_CAP:
                return None
        stack += [p + [t] for t in ahead]
    return out


def check_talk(game, dev=()):
    who = people(game)
    rows, inc = [], []
    for c in canvases(game, dev):
        nodes, _, _ = graph(c)
        ps = paths(c)
        if ps is None:
            inc.append(f"{c['id']}: over {PATH_CAP} paths, not counted")
            continue
        worst = None
        for p in ps:
            narr = speech = 0
            for nid in p:
                if has_company(c, nodes[nid], who):
                    n, s = screen_split(nodes[nid].get("blocks"))
                    narr, speech = narr + n, speech + s
            if not narr:
                continue
            ratio = narr / speech if speech else float("inf")
            if ratio > TALK_CEILING and (worst is None or ratio > worst[0]):
                worst = (ratio, p, narr, speech)
        if worst:
            r, p, n, s = worst
            shown = "no speech" if not s else f"{r:.1f} : 1"
            rows.append(f"{c['id']}: {shown} on the path {' > '.join(p)} ({n} words of narration, {s} spoken, "
                        f"on the screens with someone in them; ceiling {TALK_CEILING:.0f} : 1)")
    if rows:
        return RED, rows + inc
    return (INCOMPLETE, inc) if inc else (GREEN, [])


# ── length ────────────────────────────────────────────────────────────────────────────────────────────────

def screen_words(blocks):
    """Story words a screen can show at once: adjacent groups are one if/elseif chain (only one shows), so a chain
    counts its longest group."""
    total, chain = 0, []
    for b in list(blocks or []) + [None]:
        if isinstance(b, dict) and b.get("type") == "group":
            chain.append(screen_words(children(b)))
            continue
        if chain:
            total, chain = total + max(chain), []
        if isinstance(b, dict):
            if b.get("type") in TEXT:
                total += words(b.get("content"))
            elif b.get("type") == "block_pool":
                total += max([screen_words([x]) for x in children(b)] or [0])
    return total


def check_length(game, dev=()):
    rows = []
    for c in canvases(game, dev):
        for n in c.get("nodes") or []:
            w = screen_words(n.get("blocks"))
            if w > SCREEN_WORDS:
                rows.append(f"{c['id']} · {n.get('id')}: {w} words on one screen (cap {SCREEN_WORDS}); split it")
    return (RED, rows) if rows else (GREEN, [])


# ── presence ──────────────────────────────────────────────────────────────────────────────────────────────

def fire_slots(trig):
    """The (day, minute) slots a scene's trigger can show at, by its clock conditions (who_is_where.when_slots,
    shared with sheet.py so the two can't drift)."""
    return who_is_where.when_slots(trig.get("conditions"))


def check_presence(game, dev=()):
    where = who_is_where.where(game)
    names = {n.get("id"): n.get("name") for n in game.get("npcs") or []}
    rows = []
    for c in canvases(game, dev):
        trig = c.get("trigger") or {}
        place = trig.get("location")
        if not place or str(trig.get("is_repeatable", "true")).lower() == "false":
            continue
        bound = {trig.get("npc"), trig.get("requires_npc")}
        checked = {i.get("npc_id") for i in items(trig.get("conditions")) if i.get("type") == "npc_at_location"}
        slots = fire_slots(trig)
        for n in c.get("nodes") or []:
            for b, cond in walk(n.get("blocks")):
                props = b.get("props") or {}
                pid = props.get("npcId")
                if b.get("type") != "dialog" or props.get("speaker") != "npc" or pid in bound or pid in checked:
                    continue
                if any(i.get("type") == "npc_at_location" and i.get("npc_id") == pid for i in items(list(cond))):
                    continue
                # A line inside a group shows only when its groups' conditions hold too, so its slots are the
                # trigger's narrowed by each enclosing group's clock conditions (the same when_slots, OR widened).
                # Adjacent groups merge into one if/elseif chain, so a later group also needs the earlier ones to
                # fail; that isn't modelled. Its own conditions are a superset of when it really shows, so this can
                # only keep a red too long, never hide one.
                line_slots = set(slots)
                for gc in cond:
                    line_slots &= who_is_where.when_slots(gc)
                table = where.get(pid)
                gone = sorted(s for s in line_slots if not table or place not in {p for p, _ in table.get(s, ())})
                if gone:
                    d, m = gone[0]
                    rows.append(f"{c['id']} · {n.get('id')}: {names.get(pid, pid)} speaks at {place}, but isn't there "
                                f"{who_is_where.DAYS[d]} {m // 60:02d}:{m % 60:02d} ({len(gone)} of {len(line_slots)} "
                                f"five-minute slots); bind the scene to them, check they're present, or fix their rows")
    return (RED, rows) if rows else (GREEN, [])


# ── creation ──────────────────────────────────────────────────────────────────────────────────────────────

def check_creation(game):
    fields = [f for f in (game.get("player") or {}).get("customization_fields") or [] if isinstance(f, dict)]
    shown = json.dumps({k: v for k, v in game.items() if k != "player"}, default=str)
    rows = []
    for f in fields:
        fid = f.get("id")
        # @player alone prints the name; @player.<id> prints a field (`_resolve_at_references`, v2.py:18608-18653)
        pat = r"@player(?!\w|\.\w)|@player\.name\b" if fid == "name" else rf"@player\.{re.escape(str(fid))}\b"
        if fid and not re.search(pat, shown):
            rows.append(f"creation field `{fid}` (\"{f.get('label', '')}\") is asked and never printed back (C48)")
    return (RED, rows) if rows else (GREEN, [])


# ── saves ─────────────────────────────────────────────────────────────────────────────────────────────────

def played(game_dir, ref=None):
    """(ref, merged TOML of the last build LO played) or (None, None) when nothing was played yet. The last build LO
    played is the last commit of output/index.html: LO plays output/ through the portal (SKILL.md)."""
    game_dir = Path(game_dir).resolve()
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=game_dir, capture_output=True, text=True,
                             check=True).stdout.strip()
        rel = game_dir.relative_to(Path(top).resolve())
        if not ref:
            ref = subprocess.run(["git", "log", "-1", "--format=%h", "--", f"{rel}/output/index.html"], cwd=top,
                                 capture_output=True, text=True, check=True).stdout.strip()
        if not ref:
            return None, None
        text = subprocess.run(["git", "show", f"{ref}:{rel}/toml_phases/7_final_game.toml"], cwd=top,
                              capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, ValueError, OSError):
        return None, None
    return ref, tomllib.loads(text)


def setters(game, dev=()):
    """{flag: set of choice texts that set it}."""
    out = {}
    for c in canvases(game, dev):
        for n in c.get("nodes") or []:
            for ch in ((n.get("exit_block") or {}).get("choices") or []):
                for ef in ch.get("flagEffects") or []:
                    if isinstance(ef, dict) and ef.get("flag") and ef.get("op", "set") == "set":
                        out.setdefault(ef["flag"], set()).add(str(ch.get("text") or ""))
    return out


def keys(game, dev=()):
    """{kind: set of ids} a save joins on (C1654)."""
    cs = canvases(game, dev)
    return {
        "scene": {c["id"] for c in cs},
        "screen": {f"{c['id']}.{n.get('id')}" for c in cs for n in c.get("nodes") or [] if n.get("id")},
        "person": {n.get("id") for n in game.get("npcs") or [] if n.get("id")},
        "place": {l.get("id") for l in game.get("locations") or [] if l.get("id")},
        "flag": set((game.get("player") or {}).get("flag_keys") or []) | set(setters(game, dev)),
        "meter": {t.get("key") for t in (game.get("traits") or {}).get("labels") or [] if isinstance(t, dict)}
        | set((game.get("player") or {}).get("core_traits") or {}) - {None},
        "garment": {i.get("id") for i in game.get("clothing") or [] if isinstance(i, dict)} - {None},
    }


def ranges(game):
    """{meter: (its bar's max, its bands' numbers)} from the sidebar: what a shipped meter freezes (C1659)."""
    return {s.get("trait"): (s.get("max"), tuple((b.get("min"), b.get("max")) for b in s.get("bands") or []))
            for s in game.get("sidebar_items") or [] if isinstance(s, dict) and s.get("trait")}


def same_meaning(game_dir):
    path = Path(game_dir) / "NOTES.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    return set(re.findall(r"Same meaning:\s*`?([\w]+)`?", text))


def check_saves(game_dir, game, dev=(), baseline=None, ref=None):
    if baseline is None:
        ref, baseline = played(game_dir, ref)
    if baseline is None:
        return GREEN, []  # nothing played yet: the save rules start at LO's first dev build (C1652)
    rows = []
    was, now = keys(baseline, dev), keys(game, dev)
    for kind in was:
        for k in sorted(was[kind] - now[kind]):
            rows.append(f"{kind} `{k}` was in the build LO played ({ref}) and is gone: an old save loses it (C1656)")
    old_r, new_r = ranges(baseline), ranges(game)
    for k in sorted(set(old_r) & set(new_r)):
        if old_r[k] != new_r[k]:
            rows.append(f"meter `{k}`: its range or bands changed from {old_r[k]} to {new_r[k]}; a shipped meter's are frozen (C1659)")
    ok = same_meaning(game_dir)
    old_s, new_s = setters(baseline, dev), setters(game, dev)
    for k in sorted(set(old_s) & set(new_s)):
        if k not in ok and old_s[k] and not (old_s[k] & new_s[k]):
            rows.append(f"flag `{k}` is now set by {sorted(new_s[k])}, not {sorted(old_s[k])}: if its meaning changed, "
                        f"add a new flag (C1658); if not, write `Same meaning: {k}` in NOTES.md with LO's yes")
    return (RED, rows) if rows else (GREEN, [])


# ── speakers and goals ────────────────────────────────────────────────────────────────────────────────────

def check_speakers(game, dev=()):
    ids = {n.get("id") for n in game.get("npcs") or []}
    rows = []
    for c in canvases(game, dev):
        for n in c.get("nodes") or []:
            for b, _ in walk(n.get("blocks")):
                if b.get("type") not in ("dialog", "thought_bubble"):
                    continue
                props = b.get("props") or {}
                spk = props.get("speaker")
                where = f"{c['id']} · {n.get('id')}: \"{str(b.get('content', ''))[:40]}\""
                if not spk:
                    rows.append(f"{where} names no speaker (it renders as \"Npc\")")
                elif spk == "npc" and props.get("npcId") not in ids:
                    rows.append(f"{where}: speaker npcId `{props.get('npcId')}` is not a person in the game")
    return (RED, rows) if rows else (GREEN, [])


NEGATED = re.compile(r"\b(?:not|no|never|without|before|until)\b|n't", re.I)  # gates.py:18908


def check_goals(game):
    """Ported from v2's _goal_line_reads_true (gates.py:18911-18938)."""
    rows = []
    for c in game.get("quest_cards") or []:
        if not isinstance(c, dict):
            continue
        who = c.get("npc_id") or c.get("id") or "a card"
        for g in c.get("goals") or []:
            if not isinstance(g, dict):
                continue
            label, op = str(g.get("label") or ""), g.get("op") or g.get("operator")
            if (g.get("flag") or g.get("flag_key")) and op == "is_false" and not NEGATED.search(label):
                rows.append(f"{who}: \"{label[:60]}\" is an is_false goal, so it shows a check while she has not done it")
            counted = g.get("trait") or g.get("trait_key") or g.get("days_since_flag") or g.get("hours_since_flag")
            if counted and (op in ("lte", "lt") or (isinstance(g.get("value"), (int, float)) and g["value"] < 0)):
                rows.append(f"{who}: \"{label[:60]}\" counts down ({op} {g.get('value')}); count up to a positive number")
            if re.search(r"\d", " ".join(label.split()[:3])):
                rows.append(f"{who}: \"{label[:60]}\" opens with a number; the engine prints the count after the line")
    return (RED, rows) if rows else (GREEN, [])


def run(game_dir, game, dev=(), ref=None):
    """Every scene check, keyed by name. None for game means the merged TOML didn't parse."""
    names = ("talk", "length", "presence", "creation", "saves", "speakers", "goals")
    if game is None:
        return {k: (INCOMPLETE, ["the merged TOML did not parse"]) for k in names}
    dev = set(dev or ())
    return {
        "talk": check_talk(game, dev),
        "length": check_length(game, dev),
        "presence": check_presence(game, dev),
        "creation": check_creation(game),
        "saves": check_saves(game_dir, game, dev, ref=ref),
        "speakers": check_speakers(game, dev),
        "goals": check_goals(game),
    }
